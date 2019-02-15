'''#############################################################

			Created by: 	Rafael Breno Rocha Reis

#############################################################'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


class Molecule():

	def __init__(self):
		self.moleculeSymbol   = ""
		self.moleculeElements = 0

def getMoleculeSymbol(content_file, current_position):
	symbol = content_file[current_position]
	if(content_file[current_position+1] != '\n'):
		checklowercase = content_file[current_position+1]
		checklowercase = ord(checklowercase)
		if((checklowercase >= 97) and (checklowercase <= 122)):
			current_position = current_position + 1
			symbol = symbol + content_file[current_position]
			
	return symbol, current_position

def getMoleculeElements(content_file,current_position):
	number = content_file[current_position]
	current_position = current_position + 1
	while(content_file[current_position].isdigit()):
		number = number + content_file[current_position]
		current_position = current_position + 1
	return number,current_position


def getSpecialChrPosition(content, left_special_caracter):
	return left_special_caracter.index(content)

def getExpressionLevelMultipliers(content_file,current_position,left_special_caracter,right_special_caracter):
	count_special_char = 1
	multiplicationList = []
	
	positionToTurn = getSpecialChrPosition(content_file[current_position], left_special_caracter)
	
	while (content_file[current_position]!=right_special_caracter[positionToTurn]):
		current_position = current_position + 1
		if(content_file[current_position] in left_special_caracter):
			count_special_char = count_special_char + 1
		if(content_file[current_position] in right_special_caracter): 
			if(content_file[current_position+1] != '\n'):
				if(content_file[current_position+1].isdigit()):
					multiplicationList.append(int(content_file[current_position+1]))
				else:
					multiplicationList.append(1)

	return count_special_char, multiplicationList


def doMultiplicationList(content):
	content = content[::-1]
	value = 1
	for i in range(len(content)):
		value = value * content[i]
		content[i] = value
	content = content[::-1]
	return content

def mergeList(content):
	helperList = []
	for x in content:
		find = False
		if(len(helperList) == 0):
			helperList.append(x)
		else:
			for i in helperList:
				if(i.moleculeSymbol == x.moleculeSymbol):
					value = int(i.moleculeElements) + int(x.moleculeElements)
					i.moleculeElements = value
					find = True
			if(not find):
				helperList.append(x)
	return helperList

def convertOutput(content):
	output = ''
	for i in range(len(content)-1):
		output = output + content[i].moleculeSymbol +': '+str(content[i].moleculeElements) +','
	i = i + 1
	output = output + content[i].moleculeSymbol +': '+str(content[i].moleculeElements)
	return output




if __name__ == '__main__':
	param = sys.argv[1:]
	file = open(param[0],'r')
	content_file = file.read()
	file.close()

	left_special_caracter  = ['{','[','(']
	right_special_caracter = ['}',']',')']

	molecule_list = []
	current_position = 0

	########Read chr by chr till end of line ############
	while(content_file[current_position] != '\n'):
		#######Normal molecule without special chr#######
		if(content_file[current_position].isalpha()):
			moleculeSymbol,current_position = getMoleculeSymbol(content_file,current_position)
			newMolecule = Molecule()
			newMolecule.moleculeSymbol = moleculeSymbol
			current_position = current_position + 1
			if(content_file[current_position].isdigit()):
				elementsnumber,current_position = getMoleculeElements(content_file,current_position)
				newMolecule.moleculeElements = elementsnumber
				molecule_list.append(newMolecule)
			else:
				newMolecule.moleculeElements = 1
				molecule_list.append(newMolecule)

		########Handle with special chr###########Very sorry about this, here i dicided to buy a course in Udemy about Regex ):
		elif(content_file[current_position] in left_special_caracter):
			numberSpecialLeftChr = 0
			multiplicationList   = []
			numberSpecialLeftChr, multiplicationList = getExpressionLevelMultipliers(content_file,current_position,left_special_caracter,right_special_caracter)

			multiplicationList = doMultiplicationList(multiplicationList)

			numberSpecialRightChr   = numberSpecialLeftChr + 1
			indexMultiplicationList = numberSpecialLeftChr
			find_firstrightChr = 0
			while(numberSpecialRightChr != find_firstrightChr):
				if(content_file[current_position].isalpha()):
					moleculeSymbol,current_position = getMoleculeSymbol(content_file,current_position)
					newMolecule = Molecule()
					newMolecule.moleculeSymbol = moleculeSymbol
					current_position = current_position + 1
					if(content_file[current_position].isdigit()):
						elementsnumber,current_position = getMoleculeElements(content_file,current_position)
						newMolecule.moleculeElements = int(elementsnumber) * int(multiplicationList[indexMultiplicationList])
						molecule_list.append(newMolecule)
					else:
						newMolecule.moleculeElements = int(multiplicationList[indexMultiplicationList])
						molecule_list.append(newMolecule)
				elif(content_file[current_position] in left_special_caracter) or (content_file[current_position] in right_special_caracter):
					indexMultiplicationList = indexMultiplicationList - 1  
					current_position = current_position + 1
					find_firstrightChr = find_firstrightChr + 1
				else:
					current_position = current_position + 1
		else:
			current_position = current_position + 1

	molecule_list = mergeList(molecule_list)



	outputName = param[0].split('.')
	outputName = outputName[0] + '.out'



	file = open(outputName,'w')
	output = convertOutput(molecule_list)
	file.write(output)
	file.close()
