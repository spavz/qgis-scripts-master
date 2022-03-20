
sets = [ {4,1,3}, {2,5}, {1,4,3,2}]



def getBestCandidate(sets, currentUnion):

    currentBestSet = set()
    for _set in sets:
        if len(currentUnion.union(_set)) > len(currentUnion.union(currentBestSet)):
            currentBestSet = _set

    return currentBestSet


minSetsToFormUniversal = []
minSetsUnion = set()

for i in range(len(sets)):
    currentBestCandidate = getBestCandidate(sets, minSetsUnion)

    if currentBestCandidate:
        minSetsUnion = minSetsUnion.union(currentBestCandidate)
        minSetsToFormUniversal.append(currentBestCandidate)



print('minimum number of candidate sets forming full universal set')
print(minSetsToFormUniversal)

print()

print('Final universal set')
print(minSetsUnion)