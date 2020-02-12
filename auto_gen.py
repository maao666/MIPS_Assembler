from MIPS import mips
import sys

if len(sys.argv)!=2:
    print('Usage: python3 main.py ./sample.asm')

a = mips()
l = a.assemble(sys.argv[1],with_src=True).splitlines()
result = []
for i in range(len(l)):
    result.append('''rom[{0}] = 32'b{1};  // {2}'''.format(i, l[i][:l[i].find('|')].strip(), l[i][l[i].find('|')+1:].strip()))
print('\n'.join(result))
