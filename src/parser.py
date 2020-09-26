import re

class ClassTokenizer:
        def get_contract(self, code_string):
                #https://regex101.com/r/2l2ziE/5
                regex = r'((public|private|protected)+(\s)*(static|final|abstract)*(\s)*(boolean|byte|char|short|int|long|float|double)(\s)*(.*\(.*\)))'
                result = re.search(regex,code_string)
                if result != None:
                        result = result.group(1)
                return result

        def get_parameters(self, method_contract):
                #https://regex101.com/r/1tXDw3/4
                regex = r'((\()(((\s*)(boolean|byte|char|short|int|long|float|double))(\s*)(\w*)(\,*))*(\)))'
                result = re.search(regex,method_contract)
                if result != None:
                        result = result.group(1).replace('(','').replace(')','')
                return result

        def split_parameters(self, parameters_string):
                regex = r'((boolean|byte|char|short|int|long|float|double)(\s+)(\w*))'
                result = re.findall(regex,parameters_string)
                only_fst_group = []
                for r in result:
                        type_id_tuple = tuple(r[0].split(' '))
                        only_fst_group.append(type_id_tuple)
                return  only_fst_group

        def get_method_name(self, method_contract):
                regex = r'(\w*(?=\())'
                result = re.search(regex,method_contract).group(1)
                return result

        def get_chunks(self, code_text):
                chunks =  code_text.split('/**')
                return chunks


        def get_blocks(self, chunks):
                blocks = []
                for chunk in chunks:
                        parts = chunk.split('*/\n')
                        if len(parts) >=2:
                                javadoc = parts[0]
                                contract = self.get_contract(parts[1])
                                if (contract != None):
                                        blocks.append((parts[0],contract))
                return blocks

        def unzip_methods(self, blocks):
                methods = []
                for b in blocks:
                        method = {}
                        unsplited_parameters = self.get_parameters(b[1])
                        if unsplited_parameters != None:
                                method['method'] = self.get_method_name(b[1])
                                method['parameters'] = self.split_parameters(unsplited_parameters)
                                method['javadoc'] = b[0]
                                methods.append(method)
                return methods

        def read_class(self, filename='Math.java'):
                f = open(filename)
                text = f.read()
                f.close()
                return text

tokenizer = ClassTokenizer()
code_text = tokenizer.read_class()
chunks = tokenizer.get_chunks(code_text)
blocks = tokenizer.get_blocks(chunks)
methods = tokenizer.methods = tokenizer.unzip_methods(blocks)