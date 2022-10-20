import os
import os.path
import sys
import json
import threading

import subprocess

from flask import render_template

from TOOL.CONSTANTS import *
from TOOL.DATABASE import sqlighter



SCRIPT_END = '{{SCRIPT END}}'

# Сохранение стандартного выходного потока
original_stdout = sys.stdout  # Save a reference to the original standard output
original_stderr = sys.stderr  # Save a reference to the original standard output

RUNProcess = {}


def getNameHash(name):
    startFileName = name.split('/')
    startFileName = startFileName[len(startFileName) - 1].split('.')
    startFileName = startFileName[0]

    name = name.replace('/', '__').replace('\\', '__')

    return f'{startFileName}-{name}.txt'


def getConsole(request):
    fullName = request.args.get('fullName')
    cmdfilename = getNameHash(fullName)
    cmd_path = f'{path_TOOL}\\cmd\\console'

    test_file = os.path.exists(f'{cmd_path}\\{cmdfilename}')

    data = ''

    if (test_file):
        with open(f'{cmd_path}\\{cmdfilename}', 'r') as f:
            data = f.read()

    test_end = data.find(SCRIPT_END)
    if (test_end >= 0):
        os.remove(f'{cmd_path}\\{cmdfilename}')

    if (test_file == False):
        return SCRIPT_END

    endline = '\n\n' + '='*80 + ' SCRIPT END ' + '='*80
    data = data.replace(SCRIPT_END, endline)
    return data


def cmd(request):

    fullName = request.args.get('fullName')

    startFileName = fullName.split('/')
    startFileName = startFileName[len(startFileName) - 1]
    filePathHash = getNameHash(fullName)

    if not(sqlighter.has_console(console_path_hash=filePathHash)):
        sqlighter.add_new_console(console_name=startFileName, console_path=fullName, console_path_hash=filePathHash)
        script = threading.Thread(target=startScript, args=(fullName, filePathHash,))
        script.start()
    return render_template('console.html')

def startAllConsoles():
    print('start consoles')
    consoles = sqlighter.get_all_console()
    for console in consoles:
        console_path =      console[2]
        console_path_hash = console[3]

        script = threading.Thread(target=startScript, args=(console_path, console_path_hash,))
        script.start()




class out():

    def __init__(self, cmdfilename):
        self.file = None
        self.cmd_path = f'{path_TOOL}\\cmd\\console'
        self.name = f'{self.cmd_path}\\{cmdfilename}'
        self.mode = 'a'

    def __del__(self):
        self.file.close()

    def write(self, data):
        self.file = open(self.name, self.mode)
        self.file.write(data)
        self.file.close()

    def flush(self):
        self.file.flush()


def stopscript(request):
    fullName = request.args.get('fullName')

    print(RUNProcess)
    filePathHash = getNameHash(fullName)
    if (sqlighter.has_console(console_path_hash=filePathHash)):
        RUNProcess[filePathHash].kill()

        # Удалить консоль
        out_obj = out(filePathHash)
        out_obj.write(SCRIPT_END)

        if (filePathHash in RUNProcess):
            RUNProcess.pop(filePathHash)

        sqlighter.close_console(console_path_hash=filePathHash)

    return 'ok'


def startScript(startFile, filePathHash):
    # Полный путь к файлу скрипта
    path_startFile = path + startFile

    path_startDir = path_startFile.split('/')[:-1]
    path_startDir = '\\'.join(path_startDir)

    if (filePathHash in RUNProcess):
        return

    # path_startDir = path_startDir.replace('/', '\\')
    # path_startFile = path_startFile.replace('/', '\\')

    com = [
        'cmd.exe',
        '/k',
        'cd',
        '/d',
        path_startDir,
        '&',
        'cd',
        '&',
        'python',
        '-u',
        path_startFile,
        '&',
        'echo',
        SCRIPT_END
    ]

    process = subprocess.Popen(com, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,
                               universal_newlines=True)

    out_obj = out(filePathHash)

    RUNProcess.update({filePathHash: process})

    # kill
    for line in process.stdout:
        if (filePathHash in RUNProcess):

            if (SCRIPT_END in line):
                out_obj.write(SCRIPT_END)
                sqlighter.close_console(console_path_hash=filePathHash)
                if filePathHash in RUNProcess:
                    RUNProcess.pop(filePathHash)
                break

            out_obj.write(line)
            # next = process.stdout.__next__().strip()
            # print(line)


        else:
            break

    return 'ok'
