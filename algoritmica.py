import os
directory = os.getcwd()
files = os.listdir(directory)
if 'END_TABLE.xlsx' not in files:
    print(True)
else:
    print(False)