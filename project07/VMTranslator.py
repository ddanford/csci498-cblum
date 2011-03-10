import sys
import os

# PARSER MODULE

def initializer ( filename ):

	if (os.path.isdir(filepath)):
		print('Wanna see me comb my hair really fast?')
		quit()
	else:
		if (filepath.partition('.vm')[1] != '.vm'):
			print('Invalid file. Must be a .vm file')
			quit()
		try:
			vmfile = open(filepath, 'r')
		except:
			print("Could not open input file: " + filepath)
			quit()
		try:
			asmfile = open(filepath.partition('.vm')[0] + '.asm', 'w')
		except:
			print("Could not open output file: " + filepath.partition('.vm')[0] + '.hack.asm')
			quit()
		doTheThing ( vmfile, asmfile )
		vmfile.close()
		asmfile.close()

			
def doTheThing ( vmfile, asmfile ):
	vmcommands = vmfile.readlines()
	commandcounter = 0
	numberofcommands = len(vmcommands)
	commandtype = 0
	while ( hasMoreCommands ( commandcounter, numberofcommands ) ):
		commandtype = commandType (vmcommands[commandcounter])
		if (commandtype == 'C_ARITHMATIC'):
			writeArithmetic( asmfile, vmcommands[commandcounter] )
		if (commandtype == 'C_PUSH'):
			writePushPop( asmfile, vmcommands[commandcounter].split()[0], 
			arg1 (vmcommands[commandcounter]), 
			arg2 (vmcommands[commandcounter]))
		if (commandtype == 'C_POP'):
			writePushPop( asmfile, vmcommands[commandcounter].split()[0], 
			arg1 (vmcommands[commandcounter]), 
			arg2 (vmcommands[commandcounter]))
		commandcounter = advance( commandcounter )

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
	try:
		firstArg = codeline.partition('//')[0].split()[0]
		if (firstArg == 'add' or firstArg == 'sub' or firstArg == 'neg' or firstArg == 'eq' or firstArg == 'gt'
		or firstArg == 'lt' or firstArg == 'and' or firstArg == 'or' or firstArg == 'not'):
			return 'C_ARITHMATIC'
		if (firstArg == 'push'):
			return 'C_PUSH'
		if (firstArg == 'pop'):
			return 'C_POP'
		return 'OTHER_STUFF'
	except:
		return 'OTHER_STUFF'

# Returns the first argument of a line of code
def arg1 ( codeline ):
	return codeline.split()[1]
	
# Returns the second argument of a line of code
def arg2 ( codeline ):
	return codeline.partition('//')[0].split()[2]
	
#CODEWRITER MODULE

#Writes out the asm code for each of the arithmatic commands.
def writeArithmetic ( asmfile, command ):
	global labelcounter
	if (command.strip() == "add"):
		asmfile.write("//add\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M+D\n")
	if (command.strip() == "sub"):
		asmfile.write("//sub\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M-D\n")
	if (command.strip() == "neg"):
		asmfile.write("//neg\n@SP\nA=M-1\nM=-M\n")
	if (command.strip() == "eq"):
		asmfile.write("//eq\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=D-M\n@equals"
		+str(labelcounter)+"\nD;JEQ\n@SP\nA=M-1\nM=0\n@end"
		+str(labelcounter)+"\n0;JMP\n(equals"
		+str(labelcounter)+")\n@SP\nA=M-1\nM=-1\n(end"
		+str(labelcounter)+")\n")
	if (command.strip() == "gt"):
		asmfile.write("//gt\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\n@greaterthan"
		+str(labelcounter)+"\nD;JGT\n@SP\nA=M-1\nM=0\n@end"
		+str(labelcounter)+"\n0;JMP\n(greaterthan"
		+str(labelcounter)+")\n@SP\nA=M-1\nM=-1\n(end"
		+str(labelcounter)+")\n")
	if (command.strip() == "lt"):
		asmfile.write("//lt\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\n@lessthan"
		+str(labelcounter)+"\nD;JLT\n@SP\nA=M-1\nM=0\n@end"
		+str(labelcounter)+"\n0;JMP\n(lessthan"
		+str(labelcounter)+")\n@SP\nA=M-1\nM=-1\n(end"
		+str(labelcounter)+")\n")
	if (command.strip() == "and"):
		asmfile.write("//and\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D&M\n")
	if (command.strip() == "or"):
		asmfile.write("//or\n@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D|M\n")
	if (command.strip() == "not"):
		asmfile.write("//not\n@SP\nA=M-1\nM=!M\n")
	labelcounter = advance ( labelcounter )

#Writes out the asm code for push and pop commands
def writePushPop ( asmfile, command, segment, index ):
	if ( command == "push" ):
		if ( segment == "constant" ):
			asmfile.write("//push "+segment+" "+index+"\n@"+index+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
		if ( segment == "local" ):
			asmfile.write("//push "+segment+" "+index+"\n@"+index+"\nD=A\n@LCL\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
		if ( segment == "argument" ):
			asmfile.write("//push "+segment+" "+index+"\n@"+index+"\nD=A\n@ARG\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
		if ( segment == "this" ):
			asmfile.write("//push "+segment+" "+index+"\n@"+index+"\nD=A\n@THIS\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
		if ( segment == "that" ):
			asmfile.write("//push "+segment+" "+index+"\n@"+index+"\nD=A\n@THAT\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
		if ( segment == "temp" ):
			asmfile.write("//push "+segment+" "+index+"\n@"+str(5+int(index))+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
		if ( segment == "pointer" ):
			if ( index == "0" ):
				asmfile.write("//push "+segment+" "+index+"\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
			if ( index == "1" ):
				asmfile.write("//push "+segment+" "+index+"\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
		if ( segment == "static" ):
			asmfile.write("//push "+segment+" "+index+"\n@"
			+asmfile.name.split('/')[len(asmfile.name.split('/'))-1].partition('.')[0]+index
			+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
	if ( command == "pop" ):
		if ( segment == "local" ):
			asmfile.write("//pop "+segment+" "+index+"\n@"+index+"\nD=A\n@LCL\nD=D+M\n@CRAZYADDRESSINEED"
			+"\nM=D\n@SP\nA=M-1\nD=M\n@CRAZYADDRESSINEED\nA=M\nM=D\n@SP\nM=M-1\n")
		if ( segment == "argument" ):
			asmfile.write("//pop "+segment+" "+index+"\n@"+index+"\nD=A\n@ARG\nD=D+M\n@CRAZYADDRESSINEED"
			+"\nM=D\n@SP\nA=M-1\nD=M\n@CRAZYADDRESSINEED\nA=M\nM=D\n@SP\nM=M-1\n")
		if ( segment == "this" ):
			asmfile.write("//pop "+segment+" "+index+"\n@"+index+"\nD=A\n@THIS\nD=D+M\n@CRAZYADDRESSINEED"
			+"\nM=D\n@SP\nA=M-1\nD=M\n@CRAZYADDRESSINEED\nA=M\nM=D\n@SP\nM=M-1\n")
		if ( segment == "that" ):
			asmfile.write("//pop "+segment+" "+index+"\n@"+index+"\nD=A\n@THAT\nD=D+M\n@CRAZYADDRESSINEED"
			+"\nM=D\n@SP\nA=M-1\nD=M\n@CRAZYADDRESSINEED\nA=M\nM=D\n@SP\nM=M-1\n")
		if ( segment == "temp" ):
			asmfile.write("//pop "+segment+" "+index+"\n@SP\nA=M-1\nD=M\n@R"+str(5+int(index))+"\nM=D\n@SP\nM=M-1\n")
		if ( segment == "pointer"):
			if ( index == "0" ):
				asmfile.write("//pop "+segment+" "+index+"\n@SP\nA=M-1\nD=M\n@THIS\nM=D\n@SP\nM=M-1\n")
			if ( index == "1" ):
				asmfile.write("//pop "+segment+" "+index+"\n@SP\nA=M-1\nD=M\n@THAT\nM=D\n@SP\nM=M-1\n")
		if ( segment == "static" ):
			asmfile.write("//pop "+segment+" "+index+"\n@SP\nA=M-1\nD=M\n@"
			+(asmfile.name.split('/')[len(asmfile.name.split('/'))-1].partition('.')[0]+index)
			+"\nM=D\n@SP\nM=M-1\n")
			
#MAIN Starts the Translator
if len(sys.argv) != 2:
	print('Invalid syntax for VMTranslator.py. Proper syntax is VMTranslator.py [filepath | directory]')
	quit()
	
filepath = sys.argv[1]

labelcounter = 0
initializer (filepath)