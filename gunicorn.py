import time
import os


commands = '''
pkill gunicorn
sudo nohup gunicorn -b 0.0.0.0:80 -w 4 app:app &
'''
commands = [c for c in commands.split('\n') if c != '']
for c in commands:
    os.system(c)
    time.sleep(1)
print('OK')
