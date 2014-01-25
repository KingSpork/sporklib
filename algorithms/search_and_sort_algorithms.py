import random


'''Binary Search'''
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


'''Find duplicates in array/list'''
def findDupes(someList):
	dupes = []
	hashTable = {}
	uniques = set(someList)
	if len(uniques) != len(someList):
		for item in someList:
			if hashTable.has_key(item) == True:
				dupes.append(item)
			else:
				hashTable[item] = 0
	return dupes


	
'''QuickSort, f yeah'''
def quickSort(someList):
	listSize = len(someList) #get the length of the list
	if len(someList) == 0: #if the list is empty... 
		return [] #...return an empty list
	#ok, it gets real	
	less = [] #make an empty list for less
	greater = [] #make an empty liss for greater
	
	pivot = someList.pop(random.randint(0, listSize-1))
	for element in someList:
		if element <= pivot:
			less.append(element)
		else:
			greater.append(element)
	retList = quickSort(less) + [pivot] + quickSort(greater)
	#print("Return list:");print(retList)
	return retList

	
''' Heap Sort '''

def swap(someList, i, j):
	someList[i], someList[j] = someList[j], someList[i]

def heapify(someList):
	length = len(someList)
	start = (length - 1) / 2
	while start >= 0:
		siftDown(someList, start, length-1)
		start = start - 1
	
def siftDown(someList, start, end):
	root = start #integers for indexes, remember
	while (root * 2 + 1) <= end: #while root has at least one child
		child = root * 2 + 1
		swapper = root
		if someList[swapper] < someList[child]:
			swapper = child
		if child+1 <= end and someList[swapper] < someList[child+1]:
			swapper = child + 1
		if swapper != root:
			print("root: " + str(root) + " swapper: " + str(swapper))
			try:
				print("values: " + str(someList[root]) + " , " + str(someList[swapper]))
			except:
				print("Root or swapper out of range")
			swap(someList, root, swapper)
			root = swapper
		else:
			return

def heapSort(someList):
	end = len(someList) -1
	heapify(someList)

	while end > 0:
		swap(someList, end, 0)
		end = end - 1
		siftDown(someList, 0, end)
        

def isEqual(int1, int2, int3):
    if int1 == int2 == int3:
        return True
    else:
        return False