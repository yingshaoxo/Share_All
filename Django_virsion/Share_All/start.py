import time
import os

commands = '''
clear
python3 manage.py runserver 0:80 &
'''
commands = [c for c in commands.split('\n') if c != '']
for c in commands:
    os.system(c)
print('OK')
