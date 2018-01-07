import math
import random

#for later output usage
attribute_name = ['buying','maint','doors','persons','lug_boot','safety','classvalue']

#select cases random
def selectCase(data, port, leng):
	amount = leng * port
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

#class values
values = ['unacc', 'acc', 'good', 'vgood']
#decision attributes including class values,0 - buying, 1 - maint, 2 - doors, 3- persons, 4- lug_boot, 5- safety, 7- class value
attributes = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
#Matrix for faster calculation of information gain
data = []


#Main working part
result = open('results.txt','w+')
original_data = open('cardata/car.data','r')

#get data
data = readData(original_data, data, attributes)
error_complete = 0

for x in range(0,100):
	information = collectInformation(data)
	train = selectCase(data,2/3,information[7])
	test = selectCase(data,1/3,information[7])
	error = 0
	information2 = collectInformation(train)
	confusion_matrix = [[0,0],[0,0],[0,0],[0,0]]
	perc = [0,0,0,0] #class value probability
	specInf = [collectSpecific(train,0), collectSpecific(train,1), collectSpecific(train,2), collectSpecific(train,3)]
	perc[0] = information2[6][0] / information2[7]
	perc[1] = information2[6][1] / information2[7]
	perc[2] = information2[6][2] / information2[7]
	perc[3] = information2[6][3] / information2[7]
	print(information2[6])
	for case in test:
		highest = 0
		for id,prob in enumerate(perc):
			tmp = 0
			if specInf[id][7] != 0:
				tmp = prob * (specInf[id][0][case[0]] / specInf[id][7]) * (specInf[id][1][case[1]] / specInf[id][7]) * (specInf[id][2][case[2]] / specInf[id][7]) * (specInf[id][3][case[3]] / specInf[id][7])* (specInf[id][4][case[4]] / specInf[id][7]) * (specInf[id][5][case[5]] / specInf[id][7])
			if tmp > highest:
				highest = id
		if highest != case[6]:
			error += 1
			confusion_matrix[case[6]][1] += 1
		else:
			confusion_matrix[case[6]][0] += 1

	errorrate = error/len(test)
	error_complete += errorrate
	print('Error rate:')
	print(str(errorrate))
	print('Confusion matrix [correct unacc, false unacc] , [correct acc, false acc]...:')
	print(confusion_matrix)

error_complete = error_complete /100
print('Average error rate:')
print(error_complete)
original_data.close()
result.close()