file_name = "test.py"
python_code = """
import pandas as pd

test = "2"
print(test)
"""

with open('./app/package1/{}'.format(file_name), 'w', encoding='utf-8') as file:
    file.write(python_code)