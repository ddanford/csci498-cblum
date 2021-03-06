import sys
import os

# PARSER MODULE

def initializer ( filepath ):
	global current_file
	#Checks to see if the path given is a directory. If it is, it iterates through each file in the directory to see if it is a .vm file
	if (os.path.isdir(filepath)):
		for subdirs, dirs, files in os.walk(filepath):
			if filepath.endswith("/"):
				try:
					asmfile = open(filepath[0:len(filepath)-1]+".asm", 'w')
				except:
					print("Could not open input file: " + filepath[0:len(filepath)-1] +".asm")
					quit()
			elif filepath.endswith("\\"):
				filepath = filepath.replace("\\", "/")
				try:
					asmfile = open(filepath[0:len(filepath)-1]+".asm", 'w')
				except:
					print("Could not open input file: " + filepath[0:len(filepath)-1] +".asm")
					quit()
			else:
				try:
					asmfile = open(filepath+".asm", 'w')
					filepath = filepath+"/"
				except:
					print("Could not open input file: " + filepath +".asm")
					quit()
			for inpath in files:
				if (inpath.partition('Sys.vm')[1] == 'Sys.vm'):
					try:
						asmfile.write('//Bootstrap\n@256\nD=A\n@SP\nM=D\n@5\nD=A\n@SP\nM=D+M\n@Sys.init\n0;JMP\n')
					except:
						print("Could not open input file: " + filepath)
						quit()
			for inpath in files:
				if (inpath.partition('.vm')[1] == '.vm'):
					try:
						vmfile = open(filepath+inpath, 'r')
						current_file = vmfile.name.split('/')[len(vmfile.name.split('/'))-1].partition('.')[0]
					except:
						print("Could not open input file: " + filepath)
						quit()
					asmfile.write("//Translating "+inpath+"\n")
					doTheThing ( vmfile, asmfile )
		vmfile.close()
		asmfile.close()
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
		if (commandtype == 'C_GOTO' or commandtype == 'C_IF' or commandtype == 'C_LABEL'):
			writeIfGotoLabel( asmfile, vmcommands[commandcounter].split()[0], arg1 (vmcommands[commandcounter]) )
		if (commandtype == 'C_FUNCTION'):
			writeFunction( asmfile, vmcommands[commandcounter].split()[0],
			arg1 (vmcommands[commandcounter]), 
			arg2 (vmcommands[commandcounter]))
		if (commandtype == 'C_RETURN'):
			writeReturn( asmfile, vmcommands[commandcounter].split()[0] )
		if (commandtype == 'C_CALL'):
			writeCall ( asmfile, vmcommands[commandcounter].split()[0], 
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
		if (firstArg == 'label'):
			return 'C_LABEL'
		if (firstArg == 'goto'):
			return 'C_GOTO'
		if (firstArg == 'if-goto'):
			return 'C_IF'
		if (firstArg == 'function'):
			return 'C_FUNCTION'
		if (firstArg == 'return'):
			return 'C_RETURN'
		if (firstArg == 'call'):
			return 'C_CALL'
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
def writeArithmetic ( asmfile, codeline ):
	command = codeline.partition('//')[0].split()[0]
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
	global current_file
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
			+current_file+"."+index
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
			+current_file+"."+index
			+"\nM=D\n@SP\nM=M-1\n")
			
def writeIfGotoLabel ( asmfile, command, segment ):
	global current_function
	if (command == 'if-goto'):
		asmfile.write("@SP\nM=M-1\nA=M\nD=M\n@"+current_function+"$"+segment+"\nD;JNE\n")
	if (command == 'goto'):
		asmfile.write("@"+current_function+"$"+segment+"\n0;JMP\n")
	if (command == 'label'):
		asmfile.write("("+current_function+"$"+segment+")\n")
		
def writeFunction ( asmfile, command, name, numOfArgs ):
	global current_function
	current_function = name
	asmfile.write('//'+command+' '+name+' '+numOfArgs+'\n'
	+'('+name+')\n')
	for i in range(0, int(numOfArgs)):
		asmfile.write("@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
	
def writeReturn ( asmfile, command ):
	asmfile.write('//return\n@LCL\nD=M\n@FRAME\nM=D\n@5\nA=D-A\nD=M\n@RET\nM=D\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n'
	+'@FRAME\nAM=M-1\nD=M\n@THAT\nM=D\n@FRAME\nAM=M-1\nD=M\n@THIS\nM=D\n@FRAME\nAM=M-1\nD=M\n@ARG\nM=D\n@FRAME\nAM=M-1\nD=M\n@LCL\nM=D\n'
	+'@RET\nA=M\n0;JMP\n')
	
def writeCall ( asmfile, command, name, numOfArgs ):
	global labelcounter
	global current_function
	asmfile.write('//'+command+' '+name+' '+numOfArgs+'\n'
	+'@'+current_function+str(labelcounter)+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
	+'@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
	+'@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
	+'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
	+'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
	+'@SP\nD=M\n@5\nD=D-A\n')
	for i in range(0, int(numOfArgs)):
		asmfile.write('D=D-1\n')
	asmfile.write('@ARG\nM=D\n'
	+'@SP\nD=M\n@LCL\nM=D\n'
	+'@'+name+'\n0;JMP\n'
	+'('+current_function+str(labelcounter)+')\n')
	labelcounter = advance ( labelcounter )
			
#MAIN Starts the Translator
if len(sys.argv) != 2:
	print('Invalid syntax for VMTranslator.py. Proper syntax is VMTranslator.py [filepath | directory]')
	quit()
	
filepath = sys.argv[1]

current_class = ''
current_function = 'main'
labelcounter = 0
initializer (filepath)