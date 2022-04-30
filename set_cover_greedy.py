import json
class IntersectedArea:

    def __init__(self, id, interesctingCircleIds):
        self.id = id
        if interesctingCircleIds:
            self.interesctingCircleIds = set(interesctingCircleIds.split('|'))
        else:
            self.interesctingCircleIds = set()


intersectedAreas = []
with open('inputToSetCover.json') as json_file:
    intersectedAreaJson = json.load(json_file)

    for intersectionId in intersectedAreaJson:
        intersectedAreas.append(IntersectedArea(intersectionId, intersectedAreaJson[intersectionId]))



def getBestCandidate(intersectedAreas, currentUnion):

    currentBestIntersectedArea = IntersectedArea(0, '')
    for intersectedArea in intersectedAreas:
        if len(currentUnion.union(intersectedArea.interesctingCircleIds)) > len(currentUnion.union(currentBestIntersectedArea.interesctingCircleIds)):
            currentBestIntersectedArea = intersectedArea

    return currentBestIntersectedArea



finalIntersectedAreas = []
currentUnionOfCircles = set()

for i in range(len(intersectedAreas)):
    currentBestCandidate = getBestCandidate(intersectedAreas, currentUnionOfCircles)

    if currentBestCandidate.interesctingCircleIds:
        currentUnionOfCircles = currentUnionOfCircles.union(currentBestCandidate.interesctingCircleIds)
        finalIntersectedAreas.append(currentBestCandidate)



print('Minimized intersectedArea list covering all circles')
for area in finalIntersectedAreas:
    print(area.id, area.interesctingCircleIds)
print()

print('Union of intersected circles')
print(currentUnionOfCircles)