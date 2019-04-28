import os
script_path = os.path.dirname(os.path.abspath(__file__))
path = 'token.txt'
abs_path = os.path.join(script_path,path)
print(abs_path)
f = open(abs_path,'r')
token = f.read()
print(token)