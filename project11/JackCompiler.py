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
                        vmfile = open((filepath+inpath).partition('.jack')[0] + '.generated.vm', 'w')
                    except:
                        print("Could not open output file: " + filepath.partition('.jack')[0] + '.generated.vm')
                        quit()
                    parseFile ( jackfile, vmfile )
                    global tokencounter
                    tokencounter = 0
                    jackfile.close()
                    vmfile.close()
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
            vmfile = open(filepath.partition('.jack')[0] + '.generated.vm', 'w')
        except:
            print("Could not open output file: " + filepath.partition('.jack')[0] + '.generated.vm')
            quit()
        parseFile ( jackfile, vmfile )
        jackfile.close()
        vmfile.close()
        
def parseFile ( jackfile, vmfile ):
    jackcommands = jackfile.readlines()
    jackcommands = stripComments( jackcommands )
    tokenlist = []
    for command in jackcommands:
        for token in re.split('(".+"|[{}()\[\].,;+\-*/&|<>=~ ])', command):
            type = tokenType(token)
            if type != None:
                tokenlist.append(token)
    numtokens = len(tokenlist)
    if tokenlist[0] != 'class':
        print('Improper systax for '+os.path(jackfile)+'. Must begin file with class declaration.')
        return -1
    compileClass( vmfile, tokenlist)
    
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
    
def compileClass( vmfile, tokenlist ):
    global tokencounter, currentclass
    tokencounter = 1 #class must be the first token, checked in parseFile(...)
    currentclass = tokenlist[tokencounter]
    tokencounter += 1
    if tokenlist[tokencounter] != '{':
        print('Class name must be followed by bracketed block statements.\n')
        return -1
    tokencounter +=1
    while True:
        if tokenlist[tokencounter] == 'static' or tokenlist[tokencounter] == 'field':
            compileClassVarDec( vmfile, tokenlist )
        else:
            break
    while True:
        if tokenlist[tokencounter] == 'function' or tokenlist[tokencounter] == 'method':
            compileSubroutine( vmfile, tokenlist )
        else:
            break
        
    #if tokenlist[tokencounter] != '}':
        #print('Class must end with }.\n')
        #return -1
    
def compileClassVarDec( vmfile, tokenlist ):
    global tokencounter
    decstring = '<classVarDec>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    while True:
        type = tokenType(tokenlist[tokencounter])
        tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        tokencounter = tokencounter + 1
        vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
        if (tokenlist[tokencounter-1] == ';'):
            break
    decstring = '</classVarDec>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))

def compileSubroutine( vmfile, tokenlist ):
    global tokencounter, currentclass
    
    if tokenlist[tokencounter] == 'function':
        tokencounter += 1
        returntype = tokenlist[tokencounter]
        tokencounter += 1
        functionname = tokenlist[tokencounter]
        tokencounter += 2
        localTokens = {}
        compileParameterList( vmfile, tokenlist, localTokens )
        tokencounter += 2 # For the {
        numLocals = compileVarDec( vmfile, tokenlist, localTokens )
        vmfile.write('function ' + currentclass + '.' + functionname + ' ' + str(numLocals)+'\n')
        compileStatements( vmfile, tokenlist, localTokens )
        tokencounter += 1 # For the }
    else:
        # Compile method
        quit
    
def compileParameterList( vmfile, tokenlist, localTokens ):
    global tokencounter
    # decstring = '<parameterList>\n'
    # vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    # while tokenlist[tokencounter] != ')':
        # type = tokenType(tokenlist[tokencounter])
        # tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        # tokencounter = tokencounter + 1
        # vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    # decstring = '</parameterList>\n'
    # vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileVarDec( vmfile, tokenlist, localtokens ):
    global tokencounter
    numLocals = 0
    return numLocals
    # decstring = '<varDec>\n'
    # vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    # while True:
        # type = tokenType(tokenlist[tokencounter])
        # tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        # tokencounter = tokencounter + 1
        # vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
        # if (tokenlist[tokencounter-1] == ';'):
            # break
    # decstring = '</varDec>\n'
    # vmfile.write(decstring.rjust(len(decstring)+numtabs-2))

def compileStatements ( vmfile, tokenlist, localTokens ):
    global tokencounter, globalTokens
    #decstring = '<statements>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    while True:
        if (tokenlist[tokencounter] == 'let'):
            compileLet( vmfile, tokenlist, localTokens )
        elif (tokenlist[tokencounter] == 'do'):
            compileDo( vmfile, tokenlist, localTokens )
        elif (tokenlist[tokencounter] == 'if'):
            compileIf( vmfile, tokenlist, localTokens )
        elif (tokenlist[tokencounter] == 'while'):
            compileWhile( vmfile, tokenlist, localTokens )
        elif (tokenlist[tokencounter] == 'return'):
            compileReturn( vmfile, tokenlist, localTokens )
        else:
            break
    #decstring = '</statements>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))

def compileDo ( vmfile, tokenlist, localTokens ):
    global tokencounter, currentclass
    #decstring = '<doStatement>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    while True:
        #type = tokenType(tokenlist[tokencounter])
        #tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        tokencounter = tokencounter + 1
        functionName = tokenlist[tokencounter]
        if tokenlist[tokencounter+1] == '.':
            tokencounter += 1
            functionName += tokenlist[tokencounter]
            tokencounter += 1
            functionName += tokenlist[tokencounter]
        else:
            functionName = currentclass + '.' + functionName
        tokencounter = tokencounter + 1
        numArgs = compileExpressionList( vmfile, tokenlist, localTokens )
        vmfile.write('call ' + functionName + ' ' + str(numArgs)+'\n' )
        if (tokenlist[tokencounter] == ';' or tokenlist[tokencounter-1] == ';'):
            tokencounter += 1
            break
    vmfile.write('pop temp 0\n')
        #vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
        
    #decstring = '</doStatement>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileLet ( vmfile, tokenlist, localTokens ):
    global tokencounter
    decstring = '<letStatement>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    while True:
        type = tokenType(tokenlist[tokencounter])
        tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        tokencounter = tokencounter + 1
        vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
        if tokenlist[tokencounter] == '[':
            type = tokenType(tokenlist[tokencounter])
            tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
            tokencounter = tokencounter + 1
            vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
            compileExpression( vmfile, tokenlist, localTokens)
            type = tokenType(tokenlist[tokencounter])
            tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
            tokencounter = tokencounter + 1
            vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
        if (tokenlist[tokencounter-1] == '='):
            compileExpression( vmfile, tokenlist, localTokens )
        if (tokenlist[tokencounter-1] == ';'):
            break
    decstring = '</letStatement>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileIf ( vmfile, tokenlist, localTokens ):
    global tokencounter
    decstring = '<ifStatement>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))

    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))

    compileExpression( vmfile, tokenlist, localTokens )

    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))	

    compileStatements( vmfile, tokenlist, localTokens)

    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    
    if tokenlist[tokencounter] == 'else':
        type = tokenType(tokenlist[tokencounter])
        tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        tokencounter = tokencounter + 1
        vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
        type = tokenType(tokenlist[tokencounter])
        tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        tokencounter = tokencounter + 1
        vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
        compileStatements(vmfile, tokenlist, localTokens)
        type = tokenType(tokenlist[tokencounter])
        tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
        tokencounter = tokencounter + 1
        vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))

    decstring = '</ifStatement>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileWhile ( vmfile, tokenlist, localTokens ):
    global tokencounter
    decstring = '<whileStatement>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    
    compileExpression( vmfile, tokenlist, localTokens )
    
    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))	

    compileStatements( vmfile, tokenlist, localTokens)

    type = tokenType(tokenlist[tokencounter])
    tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    
    decstring = '</whileStatement>\n'
    vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileReturn ( vmfile, tokenlist, localTokens ):
    global tokencounter
    vmfile.write('push constant 0\n')
    vmfile.write('return\n')
    tokencounter += 2
    
    # decstring = '<returnStatement>\n'
    # vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    # type = tokenType(tokenlist[tokencounter])
    # tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    # tokencounter = tokencounter + 1
    # vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    # if (tokenlist[tokencounter] != ';'):
        # compileExpression( vmfile, tokenlist, localTokens )
    # type = tokenType(tokenlist[tokencounter])
    # tokenstring = '<'+type+'> '+tokenlist[tokencounter]+' </'+type+'>\n'
    # tokencounter = tokencounter + 1
    # vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    # decstring = '</returnStatement>\n'
    # vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileExpression ( vmfile, tokenlist, localTokens ):
    global tokencounter
    #decstring = '<expression>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    #inparens = False
    while True:
        if (tokenType(tokenlist[tokencounter]) == 'identifier'):
            compileTerm( vmfile, tokenlist, localTokens)
        elif (tokenType(tokenlist[tokencounter]) == 'integerConstant'):
            compileTerm( vmfile, tokenlist, localTokens)
        elif (tokenType(tokenlist[tokencounter]) == 'stringConstant'):
            compileTerm( vmfile, tokenlist, localTokens)
        elif (tokenlist[tokencounter] == '('):
            tokencounter += 1
            compileExpression( vmfile, tokenlist, localTokens)
            break
        elif (tokenlist[tokencounter] == 'true' 
        or tokenlist[tokencounter] == 'false' 
        or tokenlist[tokencounter] == 'null' 
        or tokenlist[tokencounter] == 'this'):
            compileTerm( vmfile, tokenlist, localTokens)
        elif tokenlist[tokencounter] == '+':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('add\n')
        elif tokenlist[tokencounter] == '-':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('sub\n')
        elif tokenlist[tokencounter] == '*':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('call Math.multiply 2\n')
        elif tokenlist[tokencounter] == '/':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('call Math.divide 2\n')
        elif tokenlist[tokencounter] == '&':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('and\n')
        elif tokenlist[tokencounter] == '|':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('or\n')
        elif tokenlist[tokencounter] == '<':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('lt\n')
        elif tokenlist[tokencounter] == '>':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('gt\n')
        elif tokenlist[tokencounter] == '=':
            tokencounter += 1
            compileTerm(vmfile, tokenlist, localTokens)
            vmfile.write('eq\n')
            
            #writeXML(tokenlist[tokencounter], numtabs, vmfile)
        elif (tokenlist[tokencounter] == '-' or tokenlist[tokencounter] == '~'):
            compileTerm( vmfile, tokenlist, localTokens)
        else:
            break
    #decstring = '</expression>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileTerm ( vmfile, tokenlist, localTokens ):
    global tokencounter, globalTokens
    #decstring = '<term>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    if (tokenlist[tokencounter] == '('):
        #writeXML(tokenlist[tokencounter], numtabs, vmfile)
        tokencounter += 1
        compileExpression (vmfile, tokenlist, localTokens)
        tokencounter += 1 #Get rid of )
        #writeXML(tokenlist[tokencounter], numtabs, vmfile)
    elif (tokenType(tokenlist[tokencounter]) == 'identifier'):
        #writeXML(tokenlist[tokencounter], numtabs, vmfile)
        # if tokenlist[tokencounter] == '.':
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
            # compileExpressionList( vmfile, tokenlist, localTokens)
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
        # elif tokenlist[tokencounter] == '[':
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
            # compileExpression( vmfile, tokenlist, localTokens)
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
        # elif tokenlist[tokencounter] == '(':
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
            # compileExpressionList( vmfile, tokenlist, localTokens)
            # writeXML(tokenlist[tokencounter], numtabs, vmfile)
            quit
    elif (tokenlist[tokencounter] == '-'):
        tokencounter += 1
        compileTerm(vmfile, tokenlist, localTokens)
        vmfile.write('neg\n')
    elif (tokenlist[tokencounter] == '~'):
        tokencounter += 1
        compileTerm(vmfile, tokenlist, localTokens)
        vmfile.write('not\n')
    else:
        vmfile.write('push constant ' + tokenlist[tokencounter]+"\n")
        tokencounter += 1
        #writeXML(tokenlist[tokencounter], numtabs, vmfile)
    #decstring = '</term>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def compileExpressionList ( vmfile, tokenlist, localTokens ):
    global tokencounter
    #decstring = '<expressionList>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    numExpressions = 0
    while tokenlist[tokencounter] != ')':
        numExpressions += 1
        compileExpression( vmfile, tokenlist, localTokens )
        if tokenlist[tokencounter] == ',':
            tokencounter += 1
            #writeXML(tokenlist[tokencounter], numtabs, vmfile)
    tokencounter += 1
    return numExpressions
    #decstring = '</expressionList>\n'
    #vmfile.write(decstring.rjust(len(decstring)+numtabs-2))
    
def writeXML(mytoken, numtabs, vmfile):
    global tokencounter
    type = tokenType(mytoken)
    if type == 'stringConstant':
        mytoken = mytoken[1:len(mytoken)-1]
    if mytoken == '<':
        mytoken = '&lt;'
    elif mytoken == '>':
        mytoken = '&gt;'
    elif mytoken == '&':
        mytoken = '&amp;'
    elif mytoken == '"':
        mytoken = '&quot;'
    tokenstring = '<'+type+'> '+mytoken+' </'+type+'>\n'
    tokencounter = tokencounter + 1
    vmfile.write(tokenstring.rjust(len(tokenstring)+numtabs))
    
if len(sys.argv) != 2:
    print('Invalid syntax for JackTokenizer.py. Proper syntax is JackTokenizer.py [filepath | directory]')
    quit()

tokencounter = 0
currentclass = ''
filepath = sys.argv[1]
initializer (filepath)