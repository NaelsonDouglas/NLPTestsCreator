import spacy
from spacy.matcher import Matcher
from tokenizer import Tokenizer
from templates import Templates
from word2number import w2n
import random
nlp = spacy.load('en_core_web_sm')

class TestsProducer:
        def __init__(self):
                self.templates = Templates()
                self.matcher = Matcher(nlp.vocab)
                self.tokenizer = Tokenizer()
                self.current_method_parts = None
                self.current_code = '\n'
                var_equals_number =     [       {'ORTH': '@throws'},
                                                {'POS': 'PROPN'},
                                                {'ORTH': 'if'},
                                                {'TEXT': {'REGEX': '\w*'}},
                                                {'TEXT': {'REGEX': '\s*'}},
                                                {'ORTH': '{'},
                                                {'ORTH': '@code'},
                                                {'POS': 'PROPN'},
                                                {'ORTH': '}'},
                                                {'TEXT': {'REGEX': '\w*'}},
                                                {'Pos': 'NUM'}
                                        ]

                self.matcher.add("var_equals_number", self.on_match_var_equals_number, var_equals_number)

        def produce_test(self,method_parts):
                self.current_method_parts = method_parts
                javadoc = nlp(method_parts['javadoc'])
                self.matcher(javadoc)

        #=======================\/Callbacks\/=======================
        def on_match_var_equals_number(self, matcher, doc, id, matches):
                for m in matches:
                        matched_text = doc[m[1]:m[2]]
                        str_m = str(matched_text)
                        var_name   = self.tokenizer.get_var_name_on_single_line(str_m)
                        exception  = self.tokenizer.get_inlined_exception_name(str_m)
                        right_side = self.tokenizer.get_inlined_right_value(str_m)
                        parameters = []
                        for parameter in self.current_method_parts['parameters']:
                                value = '-1'
                                if parameter[1] != var_name:
                                        value = self.get_random_value(parameter[0])
                                else:
                                        value = right_side
                                parameters.append(value)

                        method_name = self.current_method_parts['method']
                        method_call = self.templates.method_call(method_name,parameters)
                        exception_marker = self.templates.exception_marker(exception)
                        test_case = self.templates.test_case(exception_marker,method_name+'Test'+exception,method_call)
                        self.current_code = self.current_code + test_case
                        #print(method_call)
                        #print(matched_text)
                        #print(exception)
                        #print(var_name)
                        #print(right_side)
                        #print('-----')
                        #print(test_case)
                        #print('\n')
                test_content = self.templates.test_file('Test',self.current_code)
                print(test_content)
                print('\n')
        #=======================/\Callbacks/\=======================
        def get_random_value(self, value_type):
                if value_type == 'int':
                        return random.randrange(-100,100)
                elif value_type == 'long':
                        return random.random()