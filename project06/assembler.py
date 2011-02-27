import sys

# Opens the file and readys the .hack file for writing
# Begins translation of asm file and puts binary output in the .hack file
def initializer ( filename ):
	if (filepath.partition('.asm')[1] != '.asm'):
		print('Invalid file. Must be a .asm file')
		quit()
	
	try:
		asmfile = open(filepath, 'r')
	except:
		print("Could not open input file: " + filepath)
		quit()
	try:
		hackfile = open(filepath.partition('.asm')[0] + '.mine.hack', 'w')
	except:
		print("Could not open output file: " + filepath.partition('.asm')[0] + '.hack.mine')
		quit()
	
	asmcommands = asmfile.readlines()
	commandcounter = 0
	linecounter = 0
	numberofcommands = len(asmcommands)
	commandtype = 0
	
	while ( hasMoreCommands ( commandcounter, numberofcommands ) ):
		commandtype = commandType (asmcommands[commandcounter])
		if (commandtype == 'A_COMMAND'):
			linecounter = advance( linecounter )
		if (commandtype == 'C_COMMAND'):
			linecounter = advance( linecounter )
		if (commandtype == 'L_COMMAND'):
			addEntry(asmcommands[commandcounter].partition('(')[2].partition(')')[0], linecounter)
		commandcounter = advance( commandcounter )
		
	commandcounter = 0
	
	while ( hasMoreCommands ( commandcounter, numberofcommands ) ):
		commandtype = commandType (asmcommands[commandcounter])
		if (commandtype == 'A_COMMAND'):
			hackfile.write('0' + symbol(asmcommands[commandcounter]) + '\n')
		if (commandtype == 'C_COMMAND'):
			hackfile.write('111' + comp(asmcommands[commandcounter]) + dest(asmcommands[commandcounter]) + jump(asmcommands[commandcounter]) + '\n')
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
	if (codeline.partition('//')[1] == '//' and codeline.partition('//')[0] == ''):
		return 'COMMENT'
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
		if ( contains (codesymbol) ):
			return bin(GetAddress(codesymbol))[2:].zfill(15)
		else:
			global symbolcounter
			addEntry(codesymbol, symbolcounter)
			symbolcounter = advance ( symbolcounter )
			return bin(GetAddress(codesymbol))[2:].zfill(15)

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
		return destmap[code.partition('=')[0].replace('\t', '').strip()]
	return '000'

# Returns the 7 bit string of binary digits of the comp mnemonic based on the assembly code
def comp ( code ):
	compstring = code.partition('//')[0].partition('=')[2].partition('\n')[0].strip()
	if ( compstring in compmap ):
		return compmap[compstring]
	return compmap[code.partition(';')[0].replace('\t', '').strip()]

# Returns the 3 bit string of binary digits of the jump mnemonic based on the assembly code
def jump ( code ):
	jumpstring = code.partition('//')[0].partition(';')[2].partition('\n')[0].strip()
	if ( jumpstring in jumpmap ):
		return jumpmap[jumpstring]
	return '000'


# SymbolTable Module

symboltable = {
'SP': 0,
'LCL': 1,
'ARG': 2,
'THIS': 3,
'THAT': 4,
'R0': 0,
'R1': 1,
'R2': 2,
'R3': 3,
'R4': 4,
'R5': 5,
'R6': 6,
'R7': 7,
'R8': 8,
'R9': 9,
'R10': 10,
'R11': 11,
'R12': 12,
'R13': 13,
'R14': 14,
'R15': 15,
'SCREEN': 16384,
'KBD': 24
}
# adds a pair of a symbol and its value to the symbol table
def addEntry ( symbol, value ):
	symboltable[symbol] = value

# Checks to see if the symbol is in the symbol table
def contains ( symbol ):
	if ( symbol in symboltable ):
		return 1
	return 0

# Returns the value of the supplied symbol from the symbol table
def GetAddress ( symbol ):
	return symboltable[symbol]


# MAIN - begins the assembler
if len(sys.argv) != 2:
	print('Invalid syntax for assembler.py. Proper syntax is assembler.py [filepath]')
	quit()

filepath = sys.argv[1]

symbolcounter = 16
initializer (filepath)