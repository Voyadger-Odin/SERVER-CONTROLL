import sys
import time
import traceback

import threading
import subprocess
import queue as Queue

path_TOOL = 'D:\\Projects\\Sites\\Dividends\\SCRIPTS-TOOL\\TOOL'

def startScript():
    path = '/TOOL/static/HTDOCS'
    filename = 'filename.txt'

    original_stdout = sys.stdout  # Save a reference to the original standard output
    original_stderr = sys.stderr  # Save a reference to the original standard output

    # Переопределение выходного потока
    with open(f'{path}\\{filename}', 'a') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        sys.stderr = f

        #import test
        try:
            exec(open(f'{path}\\test.py').read())
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())

        sys.stdout = original_stdout  # Reset the standard output to its original value
        sys.stderr = original_stderr  # Reset the standard output to its original value





class out():

    def __init__(self, cmdfilename):
        self.file = None
        self.cmd_path = f'{path_TOOL}\\cmd\\console'
        self.name = f'{self.cmd_path}\\{cmdfilename}'
        self.mode = 'a'

    def __del__(self):
        try:
            self.file.close()
        except Exception:
            pass

    def write(self, data):
        print('write')
        self.file = open(self.name, self.mode)
        self.file.write(data)
        self.file.close()

    def flush(self):
        try:
            self.file.flush()
        except Exception:
            pass

    def fileno(self):
        return 1



class FlushPipe(object):
    def __init__(self, com):
        self.command = com
        self.process = None
        self.process_output = Queue.LifoQueue(0)
        self.capture_output = threading.Thread(target=self.output_reader)

    def output_reader(self):
        for line in iter(self.process.stdout.readline, b''):
            self.process_output.put_nowait(line)

    def start_process(self):
        self.process = subprocess.Popen(self.command,
                                        stdout=subprocess.PIPE)
        self.capture_output.start()

    def get_output_for_processing(self):
        line = self.process_output.get()
        print(">>>" + line)



def console():
    '''
    python D:\Projects\Sites\Dividends\SCRIPTS-TOOL\TOOL\HTDOCS\starter.py
    '''

    test_programm_file_path = r'C:\Users\Lenovo\Documents\Projekts\Python\BOT\Orphey\main_vk_orphey.py'
    test_programm_file_path_2 = r'C:\Users\Lenovo\Documents\Projekts\Python\BOT\Orphey\test.py'
    com = [
        'cmd.exe',
        '/k',
        'cd',
        r'C:\Users\Lenovo\Documents\Projekts\Python\BOT\Orphey',
        '&',
        'python',
        '-u',
        test_programm_file_path
    ]

    com2 = [
        'python',
        test_programm_file_path
    ]

    com3 = [
        'cmd.exe',
        '/k',
        'cd',
    ]

    out_obj = out('out_test.txt')

    process = subprocess.Popen(com, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    while True:
        print('OUT')

        output = process.stdout
        for line in output:
            print(line, end='')

        time.sleep(5)
        process.kill()
        break




if __name__ == '__main__':
    console()
