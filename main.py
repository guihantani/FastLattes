import os
import functions as functions

cur_path = os.path.dirname(__file__)
new_path = cur_path + '\lattes'

print(functions.extract_all_citations(new_path))