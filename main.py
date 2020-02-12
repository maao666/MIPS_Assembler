from MIPS import mips
import sys

if len(sys.argv)!=2:
    print('Usage: python3 main.py ./sample.asm')

a = mips()
print(a.assemble(sys.argv[1]))
