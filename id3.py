class Node:

	def __init__(self, type):
		self.type = type
		self.children = []

	def updateType(self, type):
		self.type = type

	def addChild(self, child):
		self.children.append(child)

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

def id3(data, root):
	# Search for best Category
	# Create new children nodes for current node
	# Test with data
	# return if perfect


def entropy():
	

def informationGain():


#grading values
values = ['unacc', 'acc', 'good', 'vgood'] #0
#decision attributes including grading values
attributes = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
#Root creation
root = Node('node')	
#Matrix for faster usage
data = []
#Main working part
result = open('decision_tree.txt','w+')
initialize(result)
original_data = open('cardata/car.data','r')
data = readData(original_data, data, attributes)


print(data)
original_data.close()
result.close()