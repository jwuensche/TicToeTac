class Node:

	def __init__(self, type):
		self.type = type
		self.children = []

	def updateType(self, type):
		self.type = type

	def addChild(self, child):
		self.children.append(child)

import math

#variables for global use
part_unacc= 0
part_acc=0
part_good=0
part_vgood=0
amount=0

#standart stuff for xml files
def initialize(name_of_file):
	name_of_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

#Transfers data from plain text file in to matrix for algorithm
def readData(name_of_origin, name_of_destination, attributes):
	linenumber = 0
	for line in name_of_origin:
		data.append([0,0,0,0,0,0,0])
		#print(line)
		xpos = 0
		last = 0
		curAtr = 0
		for char in line:
			if char == ',' or char == '\n':
				name_of_destination[linenumber][curAtr] = checkEntry(line[last : xpos], attributes[curAtr])
				last = xpos + 1
				curAtr+=1
			xpos += 1
		linenumber += 1

	return name_of_destination

#gets index for current entry in regarding array
def checkEntry(goal, list):
	#print(goal)
	for idx,entry in enumerate(list):
		if entry == goal:
			return idx

	return -1

#def id3(data, root):
	# Search for best Category
	# Create new children nodes for current node
	# Test with data
	# return if perfect

# calculates entropy for definig values
def entropy(data_nums):
# 0 - unacc, 1 - acc, 2 - good, 3 - vgood
	global amount
	return (data_nums[0] / amount) * math.log((data_nums[0] / amount),4) - (data_nums[1] / amount) * math.log((data_nums[1] / amount),4) - (data_nums[2] / amount) * math.log((data_nums[2] / amount),4) - (data_nums[3] / amount) * math.log((data_nums[3] / amount),4)

#def informationGain():

#what do i actually need? count of things with this argument at attribute, size of list at child, size of list at parent 
def collectInformation(data):
	global amount
	information=[]
	information.append([0,0,0,0])
	information.append([0,0,0,0])
	information.append([0,0,0,0])
	information.append([0,0,0,0])
	information.append([0,0,0,0])
	information.append([0,0,0,0])
	information.append([0,0,0,0])
	for list in data:
		information[0][list[0]]+= 1
		information[1][list[1]]+= 1
		information[2][list[2]]+= 1
		information[3][list[3]]+= 1
		information[4][list[4]]+= 1
		information[5][list[5]]+= 1
		information[6][list[6]]+= 1
		amount += 1

	return information

#grading values
values = ['unacc', 'acc', 'good', 'vgood']
#decision attributes including grading values
attributes = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
#Root creation
root = Node('node')	
#Matrix for faster calculation of information gain
data = []
#Main working part
result = open('decision_tree.txt','w+')
initialize(result)
original_data = open('cardata/car.data','r')
data = readData(original_data, data, attributes)
#get data
qsave = (collectInformation(data))

test = [qsave[6][0],qsave[6][1],qsave[6][2],qsave[6][3]]

entropy = entropy(test)

print(entropy)

#print(entropy)
original_data.close()
result.close()