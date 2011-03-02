import sys, os

# PARSER MODULE

def initializer ( filename ):

	if (os.path.isdir(filepath)):
		print('Wanna see me comb my hair really fast?')
		quit()
	else 
		if (filepath.partition('.asm')[1] != '.vm'):
			print('Invalid file. Must be a .vm file')
			quit()
		try:
			vmfile = open(filepath, 'r')
		except:
			print("Could not open input file: " + filepath)
			quit()
		try:
			asmfile = open(filepath.partition('.vm')[0] + '.mine.asm', 'w')
		except:
			print("Could not open output file: " + filepath.partition('.vm')[0] + '.hack.asm')
			quit()
		doTheThing ( vmfile, asmfile )
		vmfile.close()
		asmfile.close()

			
def doTheThing ( vmfile, asmfile )

# Checks to see if there are more commands to be assembled in the .vm file
def hasMoreCommands ( commandcounter, numberofcommands):
	if (commandcounter < numberofcommands):
		return 1
	return 0

# Advances to the next command in the .asm file if hasMoreCommands returns true
def advance ( commandcounter ):
	return (commandcounter + 1)

# Returns the command type of the next command: 
#	C_ARITHMATIC if it is an arithamtic call	C_PUSH if it is a push call		C_POP if it is a pop call
#	C_LABEL if it is creating a label			C_GOTO for a goto call			C_IF for an if statement
#	C_FUNCTION if it begins a function			C_RETURN to finish a function	C_CALL for function calls
def commandType ( codeline ):
	firstArg = codeline.split[0]
	if (firstArg == 'add' or firstArg == 'sub' or firstArg == 'neg' or firstArg == 'eq' or firstArg == 'gt'
	or firstArg == 'lt' or firstArg == 'and' or firstArg == 'or' or firstArg == 'not'):
		return 'C_ARITHMATIC'
	if (firstArg == 'push'):
		return 'C_PUSH'
	if (firstArg == 'pop'):
		return 'C_POP'
	return 'OTHER_STUFF'

# Returns the first argument of a line of code
def arg1 ( codeline ):
	return codeline.split[1]
	
# Returns the second argument of a line of code
def arg2 ( codeline ):
	return codeline.partition('//')[0].split[2]
	
#CODEWRITER MODULE

#Starts the codewriter module
def codewriterConstructor ( asmfile ):
	quit()

#Sets the filename of the .vm file	
def setFileName ( fileName ):
	quit()

#Writes out the asm code for each of the arithmatic commands.
def writeArithmetic ( command ):
	quit()

#Writes out the asm code for push and pop commands
def writePushPop ( command, segment, index )

#Closes the output file
def close():
	quit()

	
#MAIN Starts the Translator
if len(sys.argv) != 2:
	print('Invalid syntax for assembler.py. Proper syntax is VMTranslator.py [filepath | directory]')
	quit()
	
filepath = sys.argv[1]

initializer (filepath)