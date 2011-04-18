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
	if re.match('".+"', token) != None or re.match('.*[\s]+.*', token.strip()) != None:
		return 'stringConstant'
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
						xmlfile = open((filepath+inpath).partition('.jack')[0] + '.generated.xml', 'w')
					except:
						print("Could not open output file: " + filepath.partition('.jack')[0] + '.generated.xml')
						quit()
					parseFile ( jackfile, xmlfile )
					global tokencounter
					tokencounter = 0
					jackfile.close()
					xmlfile.close()
	else:
		if (filepath.partition('.jack')[1] != '.jack'):
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
		jackfile.close()
		xmlfile.close()
		
def parseFile ( jackfile, xmlfile ):
	jackcommands = jackfile.readlines()
	jackcommands = stripComments( jackcommands )
	tokenlist = []
	for command in jackcommands:
		for token in re.split('(".+"|[{}()\[\].,;+\-*/&|<>=~ ])', command):
			type = tokenType(token)
			if type == 'stringConstant':
				token = token[1:len(token)-1]
			if type != None:
				if token == '<':
					token = '&lt;'
				elif token == '>':
					token = '&gt;'
				elif token == '&':
					token = '&amp;'
				elif token == '"':
					token = '&quot;'
				tokenlist.append(token)
	numtokens = len(tokenlist)
	if tokenlist[0] != 'class':
		print('Improper systax for '+os.path(jackfile)+'. Must begin file with class declaration.')
		return -1
	compileClass( xmlfile, tokenlist, numtokens, 2)
	
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
	
def compileClass( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	xmlfile.write('<class>\n')
	while True:
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if (tokenlist[tokencounter-1] == '{'):
			break
	while True:
		if (tokenlist[tokencounter] == 'static' or tokenlist[tokencounter] == 'field'):
			compileClassVarDec( xmlfile, tokenlist, numtokens, numtabs+2)
		else:
			break
	while True:
		if (tokenlist[tokencounter] == 'method' or tokenlist[tokencounter] == 'constructor' or tokenlist[tokencounter] == 'function'):
			compileSubroutine( xmlfile, tokenlist, numtokens, numtabs+2)
		else:
			break
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	xmlfile.write('</class>\n')
	
def compileClassVarDec( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<classVarDec>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while True:
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if (tokenlist[tokencounter-1] == ';'):
			break
	decstring = '</classVarDec>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))

def compileSubroutine( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<subroutineDec>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while True:
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if (tokenlist[tokencounter-1] == '('):
			break
	compileParameterList( xmlfile, tokenlist, numtokens, numtabs+2 )
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	decstring = '<subroutineBody>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs))
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs+2))
	while True:
		if (tokenlist[tokencounter] == 'var' ):
			compileVarDec( xmlfile, tokenlist, numtokens, numtabs+4)
		else:
			break
	compileStatements( xmlfile, tokenlist, numtokens, numtabs+4)
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs+2))
	decstring = '</subroutineBody>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs))
	decstring = '</subroutineDec>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileParameterList( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<parameterList>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while tokenlist[tokencounter] != ')':
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	decstring = '</parameterList>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileVarDec( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<varDec>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while True:
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if (tokenlist[tokencounter-1] == ';'):
			break
	decstring = '</varDec>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))

def compileStatements ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<statements>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while True:
		if (tokenlist[tokencounter] == 'let'):
			compileLet( xmlfile, tokenlist, numtokens, numtabs+2 )
		elif (tokenlist[tokencounter] == 'do'):
			compileDo( xmlfile, tokenlist, numtokens, numtabs+2 )
		elif (tokenlist[tokencounter] == 'if'):
			compileIf( xmlfile, tokenlist, numtokens, numtabs+2 )
		elif (tokenlist[tokencounter] == 'while'):
			compileWhile( xmlfile, tokenlist, numtokens, numtabs+2 )
		elif (tokenlist[tokencounter] == 'return'):
			compileReturn( xmlfile, tokenlist, numtokens, numtabs+2 )
		else:
			break
	decstring = '</statements>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))

def compileDo ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<doStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while True:
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if (tokenlist[tokencounter-1] == '('):
			compileExpressionList( xmlfile, tokenlist, numtokens, numtabs+2 )
		if (tokenlist[tokencounter-1] == ';'):
			break
	decstring = '</doStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileLet ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<letStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while True:
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if tokenlist[tokencounter] == '[':
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
			compileExpression( xmlfile, tokenlist, numtokens, numtabs+2)
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if (tokenlist[tokencounter-1] == '='):
			compileExpression( xmlfile, tokenlist, numtokens, numtabs+2 )
		if (tokenlist[tokencounter-1] == ';'):
			break
	decstring = '</letStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileIf ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<ifStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))

	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))

	compileExpression( xmlfile, tokenlist, numtokens, numtabs+2 )

	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))	

	compileStatements( xmlfile, tokenlist, numtokens, numtabs+2)

	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	
	if tokenlist[tokencounter] == 'else':
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		compileStatements(xmlfile, tokenlist, numtokens, numtabs+2)
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))

	decstring = '</ifStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileWhile ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<whileStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	
	compileExpression( xmlfile, tokenlist, numtokens, numtabs+2 )
	
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))	

	compileStatements( xmlfile, tokenlist, numtokens, numtabs+2)

	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	
	decstring = '</whileStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileReturn ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<returnStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	if (tokenlist[tokencounter] != ';'):
		compileExpression( xmlfile, tokenlist, numtokens, numtabs+2 )
	type = tokenType(tokenlist[tokencounter])
	tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
	tokencounter = tokencounter + 1
	xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	decstring = '</returnStatement>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileExpression ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<expression>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	inparens = False
	while True:
		if (tokenType(tokenlist[tokencounter]) == 'identifier'):
			compileTerm( xmlfile, tokenlist, numtokens, numtabs+2)
		elif (tokenType(tokenlist[tokencounter]) == 'integerConstant'):
			compileTerm( xmlfile, tokenlist, numtokens, numtabs+2)
		elif (tokenType(tokenlist[tokencounter]) == 'stringConstant'):
			compileTerm( xmlfile, tokenlist, numtokens, numtabs+2)
		elif (tokenlist[tokencounter] == '('):
			compileTerm( xmlfile, tokenlist, numtokens, numtabs+2)
		elif (tokenlist[tokencounter] == 'true' 
		or tokenlist[tokencounter] == 'false' 
		or tokenlist[tokencounter] == 'null' 
		or tokenlist[tokencounter] == 'this'):
			compileTerm( xmlfile, tokenlist, numtokens, numtabs+2)
		elif (tokenlist[tokencounter] == '+'
		or tokenlist[tokencounter] == '-'
		or tokenlist[tokencounter] == '*'
		or tokenlist[tokencounter] == '/'
		or tokenlist[tokencounter] == '&amp;'
		or tokenlist[tokencounter] == '|'
		or tokenlist[tokencounter] == '&lt;'
		or tokenlist[tokencounter] == '&gt;'
		or tokenlist[tokencounter] == '='):
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		elif (tokenlist[tokencounter] == '-' or tokenlist[tokencounter] == '~'):
			compileTerm( xmlfile, tokenlist, numtokens, numtabs+2)
		else:
			break
	decstring = '</expression>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileTerm ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<term>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	if (tokenlist[tokencounter] == '('):
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		compileExpression (xmlfile, tokenlist, numtokens, numtabs+2)
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	elif (tokenType(tokenlist[tokencounter]) == 'identifier'):
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		if tokenlist[tokencounter] == '.':
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
			compileExpressionList( xmlfile, tokenlist, numtokens, numtabs+2)
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		elif tokenlist[tokencounter] == '[':
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
			compileExpression( xmlfile, tokenlist, numtokens, numtabs+2)
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		elif tokenlist[tokencounter] == '(':
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
			compileExpressionList( xmlfile, tokenlist, numtokens, numtabs+2)
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	elif (tokenlist[tokencounter] == '-' or tokenlist[tokencounter] == '~'):
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
		compileTerm(xmlfile, tokenlist, numtokens, numtabs+2)
	else:
		type = tokenType(tokenlist[tokencounter])
		tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
		tokencounter = tokencounter + 1
		xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	decstring = '</term>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
def compileExpressionList ( xmlfile, tokenlist, numtokens, numtabs ):
	global tokencounter
	decstring = '<expressionList>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	while tokenlist[tokencounter] != ')':
		compileExpression( xmlfile, tokenlist, numtokens, numtabs+2 )
		if tokenlist[tokencounter] == ',':
			type = tokenType(tokenlist[tokencounter])
			tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
			tokencounter = tokencounter + 1
			xmlfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
	decstring = '</expressionList>\n'
	xmlfile.write(decstring.rjust(len(decstring)+numtabs-2))
	
if len(sys.argv) != 2:
	print('Invalid syntax for JackTokenizer.py. Proper syntax is JackTokenizer.py [filepath | directory]')
	quit()

tokencounter = 0
filepath = sys.argv[1]
initializer (filepath)