import re
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def reading():
    with open(os.path.join(PATH, "yingshaoxo's diary.txt"), 'r') as f:
        text = f.read()
    return text

def split(text):
    result = text.split('\n\n' + '——————————————' + '\n\n')
    if result == [text]:
        result = text.split('\n')
    result = [i.strip('  　\n ') for i in result if re.match(r'^\s*$', i) == None]
    return result

def get_content():
    list_ = split(reading())
    years = []
    content = []
    for i in list_:
        lines = i.split('\n')
        content.append({'time': lines[0], 'text': '\n'.join(lines[1:])})
        years.append(lines[0][:4])
    years = list(set(years))
    years.sort()

    content.reverse()
    return years, content
