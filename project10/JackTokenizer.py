import sys
import os
import re

def tokenType( token ):
	if re.match('class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return', token) != None:
		return 'keyword'
	if re.match('[{}()\[\].,;+\-*/&|<>=~]', token) != None:
		return 'symbol'
	if re.match('[0-9]+', token) != None:
		return 'integerConstant'
	if re.match('".+"', token) != None:
		return 'StringConstant'
	if re.match('[a-zA-Z][a-zA-Z0-9_]*', token) != None:
		return 'identifier'

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
						xmlfile = open((filepath+inpath).partition('.jack')[0] + 'T.generated.xml', 'w')
					except:
						print("Could not open output file: " + filepath.partition('.jack')[0] + 'T.generated.xml')
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
			xmlfile = open(filepath.partition('.jack')[0] + 'T.generated.xml', 'w')
		except:
			print("Could not open output file: " + filepath.partition('.jack')[0] + 'T.generated.xml')
			quit()
		tokenizeFile ( jackfile, xmlfile )
		vmfile.close()
		asmfile.close()
		
def tokenizeFile ( jackfile, xmlfile ):
	return 0;

if len(sys.argv) != 2:
	print('Invalid syntax for JackTokenizer.py. Proper syntax is JackTokenizer.py [filepath | directory]')
	quit()
	
filepath = sys.argv[1]
initializer (filepath)