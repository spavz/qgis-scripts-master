class IntersectedArea:

    def __init__(self, id, interesctingCircleIds):
        self.id = id
        if interesctingCircleIds:
            self.interesctingCircleIds = set(interesctingCircleIds.split('|'))
        else:
            self.interesctingCircleIds = set()


intersectedAreas = [
    IntersectedArea('I1', 'C1'),
    IntersectedArea('I2', 'C1|C2'),
    IntersectedArea('I3', 'C2'),
    IntersectedArea('I4', 'C2|C3'),
    IntersectedArea('I5', 'C3'),
    IntersectedArea('I6', 'C2|C4'),
    IntersectedArea('I7', 'C4'),
]



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