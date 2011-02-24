import sys

if len(sys.argv) != 2:
	print('Invalid syntax for assembler.py. Proper syntax is assembler.py [filepath]')
	quit()

filepath = sys.argv[1]

initializer (filepath)

# Opens the file and readys the .hack file for writing
def initializer ( filename ):
	if (filepath.partition('.asm')[1] != '.asm'):
		print('Invalid file. Must be a .asm file')
		quit()
	
	asmfile.close()
	hackfile.close()

asmfile = open(filepath, 'r')
hackfile = open(filepath.partition('.asm')[0] + '.hack', 'w')

# Checks to see if there are more commands to be assembled in the .asm file
def hasMoreCommands ():

# Advances to the next command in the .asm file if hasMoreCommands returns true
def advance ():

# Returns the command type of the next command: A_COMMAND, C_COMMAND, or L_COMMAND
def commandType ():

# Returns the symbol used in the current command if the command is an A_COMMAND or an L_COMMAND
def symbol ():

# Returns the dest bits of the command if it is a C_COMMAND
def dest ():

# Returns the comp bits of the command if it is a C_COMMAND
def comp ():

# Returns the jump bits of the command if it is a C_COMMAND
def jump ():


# Code Module

# Returns the 3 bit string of binary digits of the dest mnemonic based on the assembly code
def dest ( code ):

# Returns the 7 bit string of binary digits of the comp mnemonic based on the assembly code
def comp ( code ):

# Returns the 3 bit string of binary digits of the jump mnemonic based on the assembly code
def jump ( code ):


# SymbolTable Module

# Constructor, initializes the symbol table and gets it ready for additional entries
def symbolContructor ():

# adds a pair of a symbol and its value to the symbol table
def addEntry ( symbol, value ):

# Checks to see if the symbol is in the symbol table
def contains ( symbol ):

# Returns the value of the supplied symbol from the symbol table
def GetAddress ( symbol ):