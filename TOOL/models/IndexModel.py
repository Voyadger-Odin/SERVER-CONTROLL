
import os
from flask import render_template



def index(args, path):
    dirname = 'D:\\Projects\\Sites\\Dividends\\SCRIPTS-TOOL\\TOOL\\static'

    getpath = 'HTDOCS'
    if (args.get('path')):
        getpath += '' + args.get('path')

    pathview = []
    dirnow = ''
    if (getpath):
        doppath = args.get('path')
        dirname = f'{path}/{doppath}'
        pathview_split = getpath.split('/')[:-1]
        for i in range(len(pathview_split)):
            path = ''
            for j in range(len(pathview_split)):
                if (i == 0):
                    break
                if (j == 0):
                    continue
                if (j > i):
                    break
                path += '/' + pathview_split[j]

            item = {'name': pathview_split[i], 'path': path}
            pathview.append(item)
        dirnow = getpath.split('/')[-1]


    dirfiles = os.listdir(dirname)
    fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)

    dirs = []
    files = []

    for file in fullpaths:
        if os.path.isdir(file): dirs.append(file.split('/')[-1])
        if os.path.isfile(file):
            name = file.split('/')[-1]
            type = name.split('.')[-1]
            files.append({'name': name, 'type': type, 'file': getpath})

    return render_template('index.html', dirs=dirs, files=files, pathview=pathview, dirnow=dirnow)
