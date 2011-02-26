import sys

# Opens the file and readys the .hack file for writing
def initializer ( filename ):
	if (filepath.partition('.asm')[1] != '.asm'):
		print('Invalid file. Must be a .asm file')
		quit()
	
	asmfile = open(filepath, 'r')
	hackfile = open(filepath.partition('.asm')[0] + '.hack', 'w')
	
	asmcommands = asmfile.readlines()
	commandcounter = 0
	linecounter = 0
	numberofcommands = len(asmcommands)
	commandtype = 0
	
	while ( hasMoreCommands ( commandcounter, numberofcommands ) ):
		commandtype = commandType (asmcommands[commandcounter])
		if (commandtype == 'A_COMMAND'):
			hackfile.write('0' + symbol(asmcommands[commandcounter]) + '\n')
		if (commandtype == 'C_COMMAND'):
			hackfile.write('111' + comp(asmcommands[commandcounter]) + dest(asmcommands[commandcounter]) + jump(asmcommands[commandcounter]) + '\n')
		if (commandtype == 'L_COMMAND'):
			print('L')
		if (commandtype == 'OTHER'):
			print('other')
		commandcounter = advance( commandcounter )
	
	asmfile.close()
	hackfile.close()
	
# Checks to see if there are more commands to be assembled in the .asm file
def hasMoreCommands ( commandcounter, numberofcommands):
	if (commandcounter < numberofcommands):
		return 1
	return 0
	
# Advances to the next command in the .asm file if hasMoreCommands returns true
def advance ( commandcounter ):
	return (commandcounter + 1)
	
# Returns the command type of the next command: A_COMMAND, C_COMMAND, or L_COMMAND
def commandType ( codeline ):
	if (codeline.partition('//')[1] == '//'):
		return 'OTHER'
	if (codeline.partition('@')[1] == '@'):
		return 'A_COMMAND'
	if (codeline.partition('=')[1] == '=' or codeline.partition(';')[1] == ';'):
		return 'C_COMMAND'
	if (codeline.partition('(')[1] == '(' and codeline.partition(')')[1] == ')'):
		return 'L_COMMAND'
	return 'OTHER'

# Returns the symbol used in the current command if the command is an A_COMMAND or an L_COMMAND
def symbol ( code ):
	codesymbol = code.partition('@')[2].partition('\n')[0]
	try:
		return bin(int(codesymbol))[2:].zfill(15)
	except:
		return '000000000000000'

destmap = {
'M': '001',
'D': '010',
'MD': '011',
'A': '100',
'AM': '101',
'AD': '110',
'AMD': '111'
}

compmap = {
'0': '0101010',
'1': '0111111',
'-1': '0111010',
'D': '0001100',
'A': '0110000',
'M': '1110000',
'!D': '0001101',
'!A': '0110001',
'!M': '1110001',
'D+1': '0011111',
'A+1': '0110111',
'M+1': '1110111',
'D-1': '0001110',
'A-1': '0110010',
'M-1': '1110010',
'D+A': '0000010',
'D+M': '1000010',
'D-A': '0010011',
'D-M': '1010011',
'A-D': '0000111',
'M-D': '1000111',
'D&A': '0000000',
'D&M': '1000000',
'D|A': '0010101',
'D|M': '1010101',
}

jumpmap = {
'JGT': '001',
'JEQ': '010',
'JGE': '011',
'JLT': '100',
'JNE': '101',
'JLE': '110',
'JMP': '111'
}

# Code Module

# Returns the 3 bit string of binary digits of the dest mnemonic based on the assembly code
def dest ( code ):
	if (code.partition('=')[1] == '='):
		return destmap[code.partition('=')[0]]
	return '000'

# Returns the 7 bit string of binary digits of the comp mnemonic based on the assembly code
def comp ( code ):
	compstring = code.partition('=')[2].partition('\n')[0]
	if ( compstring in compmap ):
		return compmap[compstring]
	return compmap[code.partition(';')[0]]

# Returns the 3 bit string of binary digits of the jump mnemonic based on the assembly code
def jump ( code ):
	jumpstring = code.partition(';')[2].partition('\n')[0]
	if ( jumpstring in jumpmap ):
		return jumpmap[jumpstring]
	return '000'


# SymbolTable Module

# Constructor, initializes the symbol table and gets it ready for additional entries
def symbolContructor ():
	quit()

# adds a pair of a symbol and its value to the symbol table
def addEntry ( symbol, value ):
	quit()

# Checks to see if the symbol is in the symbol table
def contains ( symbol ):
	quit()

# Returns the value of the supplied symbol from the symbol table
def GetAddress ( symbol ):
	quit()


	
if len(sys.argv) != 2:
	print('Invalid syntax for assembler.py. Proper syntax is assembler.py [filepath]')
	quit()

filepath = sys.argv[1]

initializer (filepath)






