import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')



def callback( matcher, doc, id, matches):
        for m in matches:
                matched_text = doc[m[1]:m[2]]
                print(str(matched_text))
                #var_name = self.tokenizer.get_var_name_on_single_line(str(matched_text))"

matcher = Matcher(nlp.vocab)

pattern = [{'ORTH': '@throws'},
           {'POS': 'PROPN'},
           {'ORTH': 'if'},
           {'TEXT': {'REGEX': '\w*'}},
           {'TEXT': {'REGEX': '\s*'}},
           {'ORTH': '{'},
           {'ORTH': '@code'},
           {'POS': 'PROPN'},
           {'ORTH': '}'},
           {'TEXT': {'REGEX': '\w*'}},
           {'Pos': 'NUM'},]

matcher.add('1',callback,pattern)

doc = nlp('* @throws ArithmeticException if the divisor {@code y} is zero')
print(matcher(doc))