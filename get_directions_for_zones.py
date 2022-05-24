import requests
import json
import directions_cache
import polyline
from subprocess import check_output
import ast

# get centroids for all zones with 5 decimal point accuracy
# set batteryRange, remainingBatteryRange in config.json
# get Google maps directions, demand points (at batteryRange - remainingBatteryRange) for all pairs of centroids
# With remainingBatteryRange as radius, draw circles and find intersections of those circles
# Run set cover greedy and find the best set of intersections
# Place charging stations in ther centroids of those intersections, this satisfies demand of all demand points with minimum charging stations




def get_directions_for_zones(fromZone, toZone, fromZoneId, toZoneId, API_KEY, geoJsonOutput):
    fromZoneGoogleCoordinates = f'{str(fromZone[1])},{str(fromZone[0])}'
    toZoneGoogleCoordinates = f'{str(toZone[1])},{str(toZone[0])}'

    if not directions_cache.get(fromZoneGoogleCoordinates, toZoneGoogleCoordinates):
        directions = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin={fromZoneGoogleCoordinates}&destination={toZoneGoogleCoordinates}&key={API_KEY}')
        directionsDict = directions.json()
        if directionsDict.get('error_message'):
            print(directionsDict)
            return

        directions_cache.put(fromZoneGoogleCoordinates, toZoneGoogleCoordinates, directions.json())
    
        print('Received data from Google maps')

    summary = directions_cache.get(fromZoneGoogleCoordinates, toZoneGoogleCoordinates)['routes'][0]['summary']
    pointsAlongLine = directions_cache.get(fromZoneGoogleCoordinates, toZoneGoogleCoordinates)['routes'][0]['overview_polyline']['points']
    print(json.dumps(summary, indent=4))
    print('fromZone toZone', fromZone, toZone)

    pointsAlongLine = list(map(list, polyline.decode(pointsAlongLine)))

    with open(f'./data/pointsAlongLine.json', "w") as jsonFile:
        json.dump({'pointsAlongLine': pointsAlongLine}, jsonFile)

    javascriptString = check_output(f"node polyline/dead_battery_points.js ", shell=True).decode('ascii')

    print(javascriptString)
    deadBatteryPoint = ast.literal_eval(javascriptString)['deadBatteryPoint']
    print(deadBatteryPoint)

    geoJsonOutput['features'].append({'fromZone': fromZone, 'toZone': toZone, \
        'fromZoneId': fromZoneId, 'toZoneId': toZoneId, \
            'circleId': 'circle_' + str(len(geoJsonOutput['features'])), 'deadBatteryPoint': deadBatteryPoint})





API_KEY = input('Enter API key\n')
geoJsonOutput = {'features': []}


# get_directions_for_zones([ 77.094360570152418, 28.84538240846951 ], [ 77.061270869848826, 28.850501811464319 ], API_KEY)


#Read centroids_in_zones.json
json_file = "centroids_in_zones.geojson"
Centroids_zones = dict()

with open(json_file) as _Centroid_zones:
    Centroids_zones = json.load(_Centroid_zones)

ZoneId_ = []
Coordinate_ = []

for point in Centroids_zones['features']:
    zoneId = point['properties']['Id']
    ZoneId_.append(zoneId)

for coordinate in Centroids_zones['features']:
    coordinate_ = coordinate['geometry']['coordinates'][0]
    Coordinate_.append(coordinate_)


for i in range(len(ZoneId_)):
    for j in range(len(ZoneId_)):
        if i != j:
            get_directions_for_zones(Coordinate_[i], Coordinate_[j], ZoneId_[i], ZoneId_[j], API_KEY, geoJsonOutput)

with open(f'deadBatteryPoints.geojson', "w") as jsonFile:
    json.dump(geoJsonOutput, jsonFile)
