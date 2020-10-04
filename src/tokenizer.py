import re
from word2number import w2n

class Tokenizer:
        def get_contract(self, full_code_string):
                #https://regex101.com/r/2l2ziE/5
                regex = r'((public|private|protected)+(\s)*(static|final|abstract)*(\s)*(boolean|byte|char|short|int|long|float|double)(\s)*(.*\(.*\)))'
                result = re.search(regex,full_code_string)
                if result != None:
                        result = result.group(1)
                return result

        def get_var_name_on_single_line(self,doc):
                regex_var_name = r'((?<=@code\s)\w+)'
                var_name = re.search(regex_var_name,doc).group(0)
                return var_name

        def get_var_markers(self,javadoc):
                regex_var_marker = r'({@code\s+\w+})'
                var_markers = re.findall(regex_var_marker,javadoc)
                return var_markers

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

        def get_modifiers(self, method_contract):
                regex = r'((public|private|protected)(\s)*(static*)(\s*)(boolean|byte|char|short|int|long|float|double))'
                result = re.search(regex,method_contract)
                if result != None:
                        modifiers = result.group(1).split(' ')
                        modifiers = modifiers[0:len(modifiers)-1]
                        result = modifiers
                return result

        def get_return_type(self, method_contract):
                regex = r'((public|private|protected)(\s)*(static*)(\s*)(boolean|byte|char|short|int|long|float|double))'
                result = re.search(regex,method_contract)
                if result != None:
                        itens = result.group(1).split(' ')
                        result = itens[len(itens)-1]
                return result

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
                                contract = self.get_contract(parts[1])
                                if (contract != None):
                                        blocks.append((parts[0],contract))
                return blocks
        def get_inlined_exception_name(self, line):
                #https://regex101.com/r/2l2ziE/10
                regex = r'((?<=@throws ).*Exception)'
                exception_name = re.search(regex,line).group(0)
                return exception_name

        def get_inlined_right_value(self, line):
                regex = r'((?<={@code y} is )\w*)'
                value = re.search(regex,line).group(0)
                value = str(w2n.word_to_num(value))
                return value

        def get_exceptions(self, javadoc):
                #https://regex101.com/r/2l2ziE/6
                regex = r'(@throws \w* if .*)'
                exceptions_strings = re.findall(regex,javadoc)
                #https://regex101.com/r/2l2ziE/8
                condition_regex = r'((?<=(if\s)).*)'
                throws_exception_regex = r'@throws\s\w+Exception'
                result = []
                for es in exceptions_strings:
                        exception = re.search(throws_exception_regex,es).group(0)
                        exception = exception.split(' ')[1]
                        condition = re.search(condition_regex,es).group(1)
                        condition = condition#self.replace_variable_annotations(condition)
                        result.append((condition,exception))
                return result

        def unzip_methods(self, blocks):
                methods = []
                for b in blocks:
                        method = {}
                        unsplited_parameters = self.get_parameters(b[1])
                        if unsplited_parameters != None and '@throws' in b[0]:
                                method['modifiers'] = self.get_modifiers(b[1])
                                method['return_type'] = self.get_return_type(b[1])
                                method['method'] = self.get_method_name(b[1])
                                method['parameters'] = self.split_parameters(unsplited_parameters)
                                method['exceptions'] = self.get_exceptions(b[0])
                                method['javadoc'] = b[0]
                                methods.append(method)
                return methods

        def read_class(self, filename='Math.java'):
                f = open(filename)
                text = f.read()
                f.close()
                return text