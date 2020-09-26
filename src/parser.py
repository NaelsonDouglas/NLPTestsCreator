import re

def get_contract(code_string):
        #https://regex101.com/r/2l2ziE/5
        regex = r'((public|private|protected)+(\s)*(static|final|abstract)*(\s)*(boolean|byte|char|short|int|long|float|double)(\s)*(.*\(.*\)))'
        result = re.search(regex,code_string)
        if result != None:
                result = result.group(1)
        return result

def get_parameters(method_contract):
        #https://regex101.com/r/1tXDw3/4
        regex = r'((\()(((\s*)(boolean|byte|char|short|int|long|float|double))(\s*)(\w*)(\,*))*(\)))'
        result = re.search(regex,method_contract)
        if result != None:
                result = result.group(1).replace('(','').replace(')','')
        return result

def split_parameters(parameters_string):
        regex = r'((boolean|byte|char|short|int|long|float|double)(\s+)(\w*))'
        result = re.findall(regex,parameters_string)
        only_fst_group = []
        for r in result:
                type_id_tuple = tuple(r[0].split(' '))
                only_fst_group.append(type_id_tuple)
        return  only_fst_group

def get_method_name(method_contract):
        regex = r'(\w*(?=\())'
        result = re.search(regex,method_contract).group(1)
        return result

def get_chunks(full_code):
        chunks =  t.split('/**')
        return chunks


def get_blocks(chunks):
        blocks = []
        for chunk in chunks:
                parts = chunk.split('*/\n')
                if len(parts) >=2:
                        javadoc = parts[0]
                        contract = get_contract(parts[1])
                        if (contract != None):
                                blocks.append((parts[0],contract))
        return blocks

def unzip_methods(blocks):
        methods = []
        for b in blocks:
                method = {}
                unsplited_parameters = get_parameters(b[1])
                if unsplited_parameters != None:
                        method['method'] = get_method_name(b[1])
                        method['parameters'] = split_parameters(unsplited_parameters)
                        method['javadoc'] = b[0]
                        methods.append(method)
        return methods

f = open('Math.java')
t = f.read()
f.close()

chunks = get_chunks(t)
blocks = get_blocks(chunks)
methods = unzip_methods(blocks)