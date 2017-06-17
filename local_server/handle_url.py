import re
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def write_url(text):
    with open(os.path.join(PATH, "local_url.txt"), 'w') as f:
        f.write(text)

def read_url():
    try:
        with open(os.path.join(PATH, "local_url.txt"), 'r') as f:
            text = f.read()
        return text
    except:
        return None
