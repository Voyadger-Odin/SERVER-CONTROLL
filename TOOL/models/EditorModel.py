
from flask import render_template

from TOOL.CONSTANTS import *

def editor(args):
    pathFile = args.get('path')
    nameFile = args.get('name')
    fileType = nameFile.split('.')[-1]

    fullPath = f'{path}{pathFile}/{nameFile}'

    f = open(fullPath, "r", encoding='utf-8')
    data = f.read()
    f.close()

    #return data
    return render_template('editor.html', data=data, type=fileType)
