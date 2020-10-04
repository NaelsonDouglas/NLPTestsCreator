from string import Template
import spacy

class Templates:
        def __init__(self):
                self.nlp = spacy.load('en_core_web_sm')

        def test_file(self,test_name,code):
                test_content = Template('package junit;\n\npublic class $test_name {\n$code\n}\n\n').substitute(test_name=test_name, code=code)
                return test_content

        def exception_marker(self, exception_name):
                exception_marker = Template('@Test(expected = $exception_name.class)')
                exception_marker_body = exception_marker.substitute(exception_name=exception_name)
                return exception_marker_body

        def test_case(self,annotations,test_name,code):
                test_case = Template('public void $test_name(){\t\n$code\n}\n\n')
                test_case_body = test_case.substitute(test_name=test_name,code=code)
                return self.join_templates(annotations,test_case_body)

        def method_call(self,method_name,params):
                param_list = ''
                for p in params:
                        if param_list != '':
                                param_list = param_list+', '+str(p)
                        else:
                                param_list = str(p)
                method_call = Template('\t$method_name($param_list);').substitute(method_name = method_name, param_list=param_list)
                return method_call

        def test_with_exception(self, exception_name, test_name,code):
                exception_marker = self.exception_marker(exception_name)
                return self.test_case([exception_marker],test_name,code)

        def join_templates(self, *templates):
                return '\n'.join(templates)