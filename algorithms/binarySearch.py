def binarySearch(someList, target):
	lo = 0
	hi = len(someList)
	while lo+1 < hi:
		test = (lo + hi) / 2
		if someList[test] > target:
			hi = test
		else:
			lo = test
	if someList[lo] == target:
		return lo
	else:
		return -1
		
		

import random

def quickSort(someList):
	listSize = len(someList)
	if len(someList) == 0:
		return []
	less = []
	greater = []
	
	pivot = someList.pop(random.randint(0, listSize-1))
	for element in someList:
		if element <= pivot:
			less.append(element)
		else:
			greater.append(element)
	retList = quickSort(less) + [pivot] + quickSort(greater)
	#print("Return list:");print(retList)
	return retList