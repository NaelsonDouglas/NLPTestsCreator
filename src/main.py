from tokenizer import Tokenizer
import pandas as pd
from templates import Templates
from tests_producer import TestsProducer

import spacy


tokenizer = Tokenizer()
code_text = tokenizer.read_class()
chunks = tokenizer.get_chunks(code_text)
blocks = tokenizer.get_blocks(chunks)
method_parts = tokenizer.method_parts = tokenizer.unzip_methods(blocks)
tests_producer = TestsProducer()

for m in method_parts:
        tests_producer.produce_test(m)