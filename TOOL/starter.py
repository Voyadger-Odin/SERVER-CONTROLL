import sys
import traceback
import os
import subprocess


def startScript():
    file = 'D:\Projects\Sites\Dividends\SCRIPTS-TOOL\TOOL\static\HTDOCS\\test.py'

    startCMD = 'C:\Windows\system32\cmd.exe'
    #comand = f'{startCMD} {startComand}'
    #print(comand)

    #p = subprocess.Popen(startComand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #result = p.communicate()[0]
    #print(result)

    programm_dop = 'a = 120\nb=15\nprint(a + b)\n\n'
    with open(file, 'r') as script:
        programm = script.read()
        programm = f'{programm_dop}\n{programm}'

        test_programm_file_path = 'D:\Projects\Sites\Dividends\SCRIPTS-TOOL\TOOL\static\HTDOCS\\test_programm_file.py'
        test_programm_file = open(test_programm_file_path, 'w+')
        test_programm_file.write(programm)
        test_programm_file.close()

        startComand = f'python {test_programm_file_path}'
        os.system(startComand)

    #subprocess.Popen([startCMD, startComand])

    return

    # os.startfile(r'C:\Windows\System32\cmd.exe', 'any-arg')  # Cmd.exe start-up
    os.system(comand)


if __name__ == '__main__':
    startScript()
