import json
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
with open('intersectedCircles.geojson') as json_file:
    rawAreas = json.load(json_file)['features']

    for rawArea in rawAreas:
        intersectedAreas.append(IntersectedArea(rawArea['properties']['Unique_ID'], rawArea['properties']['circles']))



finalIntersectedAreas = []
currentUnionOfCircles = set()

for i in range(len(intersectedAreas)):
    currentBestCandidate = getBestCandidate(intersectedAreas, currentUnionOfCircles)

    if currentBestCandidate.interesctingCircleIds:
        currentUnionOfCircles = currentUnionOfCircles.union(currentBestCandidate.interesctingCircleIds)
        finalIntersectedAreas.append(currentBestCandidate)

geoJsonOutput = {'features': []}

print('Minimized intersectedArea list covering all circles')
for area in finalIntersectedAreas:
    print(area.id, area.interesctingCircleIds)
    geoJsonOutput['features'].append({'Unique_ID': area.id, 'circles': '|'.join(list(area.interesctingCircleIds)) })
print()

print('Union of intersected circles')
print(currentUnionOfCircles)

with open(f'subsetOfIntersectedCircles.geojson', "w") as jsonFile:
    json.dump(geoJsonOutput, jsonFile)
