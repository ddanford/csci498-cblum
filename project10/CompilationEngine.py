import sys
import os
import re

def initializer ( filepath ):
	#Checks to see if the path given is a directory. If it is, it iterates through each file in the directory to see if it is a .jack file
	if (os.path.isdir(filepath)):
		for subdirs, dirs, files in os.walk(filepath):
			for inpath in files:
				if filepath.endswith("\\"):
					filepath = filepath.replace("\\", "/")
				elif not(filepath.endswith("/")):
					filepath = filepath+"/"
				if (inpath.partition('.jack')[1] == '.jack'):
					try:
						jackfile = open(filepath+inpath, 'r')
					except:
						print("Could not open input file: " + filepath)
						quit()
					try:
						xmlfile = open((filepath+inpath).partition('.jack')[0] + '.generated.xml', 'w')
					except:
						print("Could not open output file: " + filepath.partition('.jack')[0] + '.generated.xml')
						quit()
					tokenizeFile ( jackfile, xmlfile )
					jackfile.close()
					xmlfile.close()
	else:
		if (filepath.partition('.vm')[1] != '.jack'):
			print('Invalid file. Must be a .jack file')
			quit()
		try:
			jackfile = open(filepath, 'r')
		except:
			print("Could not open input file: " + filepath)
			quit()
		try:
			xmlfile = open(filepath.partition('.jack')[0] + '.generated.xml', 'w')
		except:
			print("Could not open output file: " + filepath.partition('.jack')[0] + '.generated.xml')
			quit()
		parseFile ( jackfile, xmlfile )
		vmfile.close()
		asmfile.close()
		
def parseFile ( jackfile, xmlfile ):
	jackcommands = jackfile.readlines()
	jackcommands = stripComments( jackcommands )
	tokenlist = []
	numtokens = 0
	for command in jackcommands:
		for token in re.split('(".+"|[{}()\[\].,;+\-*/&|<>=~ ])', command):
			type = tokenType(token)
			if type == 'StringConstant':
				token = token[1:len(token)-1]
			if type != None:
				tokenlist[numtokens] = token
				numtokens = numtokens + 1
	
def stripComments ( jackcommands ):
	commandcounter = 0
	numberofcommands = len(jackcommands)
	while ( commandcounter < numberofcommands ):
		jackcommands[commandcounter] = jackcommands[commandcounter].partition("//")[0].strip()
		if jackcommands[commandcounter].partition("/**")[1] == "/**":
			while (jackcommands[commandcounter].partition("*/")[1] != "*/"):
				jackcommands[commandcounter] = ""
				commandcounter = commandcounter + 1
			jackcommands[commandcounter] = ""
		commandcounter = commandcounter + 1
	return jackcommands

if len(sys.argv) != 2:
	print('Invalid syntax for JackTokenizer.py. Proper syntax is JackTokenizer.py [filepath | directory]')
	quit()
	
filepath = sys.argv[1]
initializer (filepath)