import json
from traceback import print_tb
class IntersectedArea:

    def __init__(self, id, interesctingCircleIds):
        self.id = id
        if interesctingCircleIds:
            self.interesctingCircleIds = set(interesctingCircleIds.split('|'))
        else:
            self.interesctingCircleIds = set()



def getBestCandidate(intersectedAreas, currentUnion):

    currentBestIntersectedArea = IntersectedArea(0, '')
    for intersectedArea in intersectedAreas:
        if len(currentUnion.union(intersectedArea.interesctingCircleIds)) > len(currentUnion.union(currentBestIntersectedArea.interesctingCircleIds)):
            currentBestIntersectedArea = intersectedArea

    return currentBestIntersectedArea



intersectedAreas = []
with open('io/intersectedCircles.geojson') as json_file:
    rawAreas = json.load(json_file)['features']

    for rawArea in rawAreas:
        intersectedAreas.append(IntersectedArea(rawArea['properties']['Unique_ID'], rawArea['properties']['circles']))



finalIntersectedAreas = []
currentUnionOfCircles = set()
allUnionOfCircles = set()

for i in range(len(intersectedAreas)):
    currentBestCandidate = getBestCandidate(intersectedAreas, currentUnionOfCircles)
    allUnionOfCircles = allUnionOfCircles.union(intersectedAreas[i].interesctingCircleIds)

    if currentBestCandidate.interesctingCircleIds:
        currentUnionOfCircles = currentUnionOfCircles.union(currentBestCandidate.interesctingCircleIds)
        finalIntersectedAreas.append(currentBestCandidate)

geoJsonOutput = {'features': []}

print('\nMinimized charging station list: \n')
for area in finalIntersectedAreas:
    print(area.id, 'covers', len(area.interesctingCircleIds), 'circles')
    geoJsonOutput['features'].append({'Unique_ID': area.id, 'circles': '|'.join(list(area.interesctingCircleIds)) })

if len(allUnionOfCircles) == len(currentUnionOfCircles):
    print('\nUnion of circles is valid\n')
else:
    print('\nUnion FAILED. Check union again \n')

print('Final number of charging stations: ', len(finalIntersectedAreas))


with open(f'io/subsetOfIntersectedCircles.json', "w") as jsonFile:
    json.dump(geoJsonOutput, jsonFile, indent=4)

with open(f'io/subsetOfIntersectedCircles.geojson', "w") as jsonFile:
    json.dump(geoJsonOutput, jsonFile)

