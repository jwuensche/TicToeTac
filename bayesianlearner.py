import math
import random
import sys

#for later output usage
attribute_name = ['buying','maint','doors','persons','lug_boot','safety','classvalue']


#select cases random
def selectCase(data, port):
	amount = len(data) * port
	choice = random.sample(data,int(amount))
	return choice

#Transfers data from plain text file in to matrix for algorithm
def readData(name_of_origin, name_of_destination, attributes):
	linenumber = 0
	for lineid,line in enumerate(name_of_origin):
		name_of_destination.append([0,0,0,0,0,0,0])
		line = line.strip('\n')
		date = line.split(',')

		for id,value in enumerate(date):
			name_of_destination[lineid][id] = checkEntry(value,attributes[id])

	return name_of_destination

#gets index for current entry in regarding array
def checkEntry(goal, list):
	for idx,entry in enumerate(list):
		if entry == goal:
			return idx

	return -1

#counts appearence of every attribute in a given set of data
def collectInformation(data):
	information=[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], 0]
	for list in data:
		for x in range(0,7):
			information[x][list[x]]+= 1
		information[7] += 1

	return information

#counts case shizzle
def collectSpecific(data,clval):
	information=[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], 0]

	for list in data:
		if list[6] == clval:
			for x in range(0,7):
				information[x][list[x]]+= 1
			information[7] += 1

	return information

def euclDistance(lh,rh):
	tmp = 0
	#magic offset -2 to exclude last statement
	for x in range(0,len(lh)-2):
		tmp += math.pow(lh[x] - rh[x],2)

	return math.sqrt(tmp)

def most_common(lst):
	return max(set(lst), key=lst.count)

def searchNearest(train, case, k):
	neighbours = []
	tmp = 0

	for exp in train:
		value = euclDistance(exp,case)
		if tmp < k:
			neighbours.append(value)
			tmp += 1
			neighbours = sorted(neighbours)
		if tmp == k and value < neighbours[-1]:
			neighbours[-1] = value
			neighbours = sorted(neighbours)

	return most_common(neighbours)


def kNN(data,k):
	trainSet = selectCase(data, 2/3)
	testSet = selectCase(data, 1/10)
	error = 0
	confuisonMatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

	for case in testSet:
		tmp = searchNearest(trainSet,case,k)
		if tmp == case[-1]:
			print('Hit!')
		else:
			print('Miss!')
			error += 1
		confuisonMatrix[case[-1]][tmp]

	print(confuisonMatrix)
	print(error / (1/10 * len(data)))

def main(argv):

	#class values
	values = ['unacc', 'acc', 'good', 'vgood']
	#decision attributes including class values,0 - buying, 1 - maint, 2 - doors, 3- persons, 4- lug_boot, 5- safety, 7- class value
	attributes = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
	#Matrix for faster calculation of information gain
	data = []
	#fetch data
	result = open('results.txt','w+')
	original_data = open('cardata/car.data','r')
	data = readData(original_data, data, attributes)
	kNN(data, int(argv[1]))

	original_data.close()
	result.close()

if __name__ == "__main__":
	main(sys.argv)
