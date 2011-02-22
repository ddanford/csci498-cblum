import sys

if len(sys.argv) != 2:
	print('Invalid syntax for assembler.py. Proper syntax is assembler.py [filepath]')
	quit()

filepath = sys.argv[1]

asmfile = open(filepath, 'r')
hackfile = open(filepath.partition('.asm')[0] + '.hack', 'w')

asmfile.close()
hackfile.close()