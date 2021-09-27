import json 


def get(fromZoneGoogleCoordinate, toZoneGoogleCoordinate):
    try:
        fromZone = None
        with open(f'data/directions_cache/{fromZoneGoogleCoordinate}.json', "r") as jsonFile:
            fromZone = json.load(jsonFile)
    
        try:
            return fromZone[toZoneGoogleCoordinate]
        except KeyError:
            return None
    
    except FileNotFoundError:
        return None



def put(fromZoneGoogleCoordinate, toZoneGoogleCoordinate, directions):
    fromZone = None
    try:
        with open(f'data/directions_cache/{fromZoneGoogleCoordinate}.json', "r") as jsonFile:
            fromZone = json.load(jsonFile)

    except FileNotFoundError:
        fromZone = {}

    fromZone[toZoneGoogleCoordinate] = directions

    with open(f'data/directions_cache/{fromZoneGoogleCoordinate}.json', "w") as jsonFile:
        json.dump(fromZone, jsonFile)

