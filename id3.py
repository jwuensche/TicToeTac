import math

#for later output usage
attribute_name = ['buying','maint','doors','persons','lug_boot','safety','classvalue']

class Node:

	def __init__(self, type, data):
		self.type = type
		self.children = []
		self.content = data
		self.entropy = 0
		self.attribute = 'leaf'
		self.value = ''

	def addChild(self, child):
		self.children.append(child)

	#no usage nowadays but remains for debug purposes
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

#implementation for id3 algorithm
def id3(root, attributes):
	# Search for best Category
	# Create new children nodes for current node
	# Test with data
	# return if perfect
	global attribute_name

	qsave = (collectInformation(root.content))
	test = [qsave[6][0],qsave[6][1],qsave[6][2],qsave[6][3],qsave[7]]
	root.entropy = entropy(test)

	if root.entropy == 0:
		return

	highestGain = [0,0]
	for id,list in enumerate(attributes):
		if highestGain[0] < informationGain(root.content, id) and id != 6:
			highestGain[0] = informationGain(root.content,id)
			highestGain[1] = id

	root.attribute = attribute_name[highestGain[1]]

	for id,stuff in enumerate(attributes[highestGain[1]]):
		child = Node('node', [])
		child.value = attributes[highestGain[1]][id]
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
		for x in range(0,7):
			information[x][list[x]]+= 1
		information[7] += 1

	return information

#Output for xml file
def printTree(root,name_of_destination,attribute,level):
	global attributes
	for x in range(0, level):
		name_of_destination.write('\t')

	if root.type == 'tree':
		initialize(name_of_destination)

	name_of_destination.write('<' + root.type + ' classes="')
	information = collectInformation(root.content)
	first = []
	for id,amount in enumerate(information[6]):
		if amount !=0:
			if first:
				name_of_destination.write(',')
			first = 1
			name_of_destination.write(attributes[6][id]+ ':' + str(amount))

	name_of_destination.write('" entropy="' + str(round(root.entropy,3)) + '"') 

	if root.type !='tree':
		name_of_destination.write(' ' + attribute + '="' + root.value + '"' +'>')

	else:
		name_of_destination.write('>')

	if not root.children:
		for id,amount in enumerate(information[6]):
			if amount !=0:
				name_of_destination.write(attributes[6][id])

	else:
		name_of_destination.write('\n')
		for child in root.children:
			printTree(child,name_of_destination,root.attribute,level+1)
		for x in range(0, level):
			name_of_destination.write('\t')

	name_of_destination.write('</'+ root.type + '>\n')


#class values
values = ['unacc', 'acc', 'good', 'vgood']
#decision attributes including class values,0 - buying, 1 - maint, 2 - doors, 3- persons, 4- lug_boot, 5- safety, 7- class value
attributes = [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'], ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
#Matrix for faster calculation of information gain
data = []
#Main working part
result = open('decision_tree.xml','w+')
original_data = open('cardata/car.data','r')
#get data
data = readData(original_data, data, attributes)
#Root creation
root = Node('tree', data)
id3(root, attributes)

printTree(root,result,'unused',0)
#print(entropy)
original_data.close()
result.close()