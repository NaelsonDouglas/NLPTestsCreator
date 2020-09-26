import re

_regex = r'((public|private|protected)+(\s)*(static|final|abstract)*(\s)*(boolean|byte|char|short|int|long|float|double)(\s)*(.*\(.*\)))'
def get_contract(code_string,regex=_regex):
        return re.search(regex,code_string)



f = open('Math.java')
t = f.read()
f.close()
chunks =  t.split('/**')

blocks = []
for chunk in chunks:
        parts = chunk.split('*/\n')
        if len(parts) >=2:
                print(parts[0])
                print('\n\n')
                print(parts[1])
                print('----------')
                contract = get_contract(parts[1])
                if (contract != None):
                        blocks.append((parts[0],contract.group(1)))

for b in blocks:
        print(b[1])
        print('-------------')