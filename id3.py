import math

class Node:

	def __init__(self, type, data):
		self.type = type
		self.children = []
		self.content = data
		self.entropy = 0
		self.attribute = 'leaf'

	def updateType(self, type):
		self.type = type

	def addChild(self, child):
		self.children.append(child)

	def toString(self):
		result = 'Type: ' + self.type + ' Entropy: ' + str(self.entropy) + ' Attribute: ' + str(self.attribute) + ' Data: '
		qsave = collectInformation(self.content)
		qlist = [qsave[6][0],qsave[6][1],qsave[6][2],qsave[6][3],qsave[7]]
		result+= ','.join(str(e) for e in qlist)
		result+= ' '
		result += '\n'
		for child in self.children:
			result += child.toString()

		return result

#standart stuff for xml files
def initialize(name_of_file):
	name_of_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

#Transfers data from plain text file in to matrix for algorithm
#maybe use split -> Paul proposed this
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
	for idx,entry in enumerate(list):
		if entry == goal:
			return idx

	return -1


#currently overshoots by one so it just sorts by class attribute
def id3(root, attributes):
	# Search for best Category
	# Create new children nodes for current node
	# Test with data
	# return if perfect

	qsave = (collectInformation(root.content))
	test = [qsave[6][0],qsave[6][1],qsave[6][2],qsave[6][3],qsave[7]]
	root.entropy = entropy(test)

	if entropy(test) == 0:
		for id,num in enumerate(test):
			if num != 0 and id != 4:
				root.type = values[id]
		return

	highestGain = [0,0]
	for id,list in enumerate(attributes):
		if highestGain[0] < informationGain(root.content, id) and id != 6:
			highestGain[0] = informationGain(root.content,id)
			highestGain[1] = id

	root.attribute = attributes[highestGain[1]]

	for id,stuff in enumerate(attributes[highestGain[1]]):
		child = Node('Node', [])
		for list in root.content:
			if list[highestGain[1]] == id:
				child.content.append(list)
		root.addChild(child)
		id3(child, attributes)




# calculates entropy for definig values
# 0 - unacc, 1 - acc, 2 - good, 3 - vgood. 4 - amount
def entropy(data_nums):
	entropy = 0
	for id,num in enumerate(data_nums):
		if id != 4 and num != 0:
			entropy += - (num/data_nums[4]) * math.log(num/data_nums[4], 4)
	return entropy

#calculates informationGain value for given set of data for a specific attribute(distinguished by position in attribute array)
def informationGain(data, attribute):
	stats_data = collectInformation(data)
	sub_sets = [[],[],[],[]]
	entropy_sum_single_sets = 0

	qsave = collectInformation(data)
	qlist = [qsave[6][0],qsave[6][1],qsave[6][2],qsave[6][3],qsave[7]]
	data_entropy = entropy(qlist)
	
	for list in data:
		sub_sets[list[attribute]].append(list)

	for set in sub_sets:
		qsave = collectInformation(set)
		qlist2 = [qsave[6][0],qsave[6][1],qsave[6][2],qsave[6][3],qsave[7]]
		entropy_sum_single_sets += qlist2[4]/qlist[4] * entropy(qlist2)

	return data_entropy - entropy_sum_single_sets

#counts appearence of every attribute in a given set of data
def collectInformation(data):
	information=[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], 0]
	for list in data:
		information[0][list[0]]+= 1
		information[1][list[1]]+= 1
		information[2][list[2]]+= 1
		information[3][list[3]]+= 1
		information[4][list[4]]+= 1
		information[5][list[5]]+= 1
		information[6][list[6]]+= 1
		information[7] += 1

	return information

#def printTree(root):

#class values
values = ['unacc', 'acc', 'good', 'vgood']
#decision attributes including class values,0 - buying, 1 - maint, 2 - doors, 3- persons, 4- lug_boot, 5- safety, 7- class value
attributes = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
#Matrix for faster calculation of information gain
data = []
#Main working part
result = open('decision_tree.txt','w+')
initialize(result)
original_data = open('cardata/car.data','r')
#get data
data = readData(original_data, data, attributes)
#Root creation
root = Node('node', data)
id3(root, attributes)
result.write(root.toString())
#print(entropy)
original_data.close()
result.close()