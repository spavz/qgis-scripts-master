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




def get_directions_for_zones(fromZone, toZone, API_KEY, geoJsonOutput):

    fromZoneXCoordinate = fromZone['xCentroid5']
    fromZoneYCoordinate = fromZone['yCentroid5']
    toZoneXCoordinate = toZone['xCentroid5']
    toZoneYCoordinate = toZone['yCentroid5']
    
    fromZoneGoogleCoordinates = f'{str(fromZoneYCoordinate)},{str(fromZoneXCoordinate)}'
    toZoneGoogleCoordinates = f'{str(toZoneYCoordinate)},{str(toZoneXCoordinate)}'
    print('fromZoneGoogleCoordinates toZoneGoogleCoordinates', fromZoneGoogleCoordinates, toZoneGoogleCoordinates)

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

    pointsAlongLine = list(map(list, polyline.decode(pointsAlongLine)))

    with open(f'./data/pointsAlongLine.json', "w") as jsonFile:
        json.dump({'pointsAlongLine': pointsAlongLine}, jsonFile)

    javascriptString = check_output(f"node polyline/dead_battery_points.js ", shell=True).decode('ascii')

    print(javascriptString)
    try:
        deadBatteryPoint = ast.literal_eval(javascriptString)['deadBatteryPoint']
        print(deadBatteryPoint)
        geoJsonOutput['features'].append({'fromZoneGoogleCoordinates': fromZoneGoogleCoordinates, 'toZoneGoogleCoordinates': toZoneGoogleCoordinates, \
        'fromZoneId': fromZone['Id'], 'toZoneId': toZone['Id'], \
            'circleId': 'circle_' + str(len(geoJsonOutput['features'])), 'deadBatteryPointGoogleCoordinates': ','.join(map(str, deadBatteryPoint)), \
                'deadBatteryPointGqisCoordinates': [deadBatteryPoint[1], deadBatteryPoint[0]], })

    except SyntaxError:
        print('No dead battery point')






API_KEY = input('Enter API key\n')
geoJsonOutput = {'features': []}


# get_directions_for_zones([ 77.094360570152418, 28.84538240846951 ], [ 77.061270869848826, 28.850501811464319 ], API_KEY)


#Read centroids_in_zones.json
json_file = "centroids_in_zones.geojson"
zones = []

with open(json_file) as _Centroid_zones:
    zones = json.load(_Centroid_zones)['features']


for i in range(len(zones)):
    for j in range(len(zones)):
        if i != j:
            get_directions_for_zones(zones[i]['properties'], zones[j]['properties'], API_KEY, geoJsonOutput)

with open(f'deadBatteryPoints.geojson', "w") as jsonFile:
    json.dump(geoJsonOutput, jsonFile)
