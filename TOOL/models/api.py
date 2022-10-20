
import os
import shutil
import zipfile
import json

from TOOL import CONSTANTS
from TOOL.DATABASE import sqlighter


'''
Получение списка процессов
'''
def getAllProcess():
    process = sqlighter.get_all_console()
    result = []
    for proces in process:
        result.append({
            'console_name': proces[1],
            'console_path': proces[2],
            'console_path_hash': proces[3]
        })
    return json.dumps(result)

'''
Загрузка файлов
'''
def uploadFile(request):
    getPath = request.args.get('path')
    file = request.files['files']

    fullPath = f'{CONSTANTS.path}{getPath}'
    fileName = file.filename
    fullName = os.path.join(fullPath, fileName)

    file.save(fullName)

    return 'ok'

'''
Разархивирование файла
'''
def uparchiv(request):

    GETName = request.args.get('name')
    GETPath = request.args.get('path')

    fullPath = f'{CONSTANTS.path}{GETPath}'
    fullName = os.path.join(fullPath, GETName)

    file_zip = zipfile.ZipFile(fullName)
    file_zip.extractall(fullPath)
    file_zip.close()

    return 'ok'


'''
Переиминовывание файлов и папок
'''
def renameFile(args):
    getPath = args.get('path')
    getName = args.get('name')
    getNewName = args.get('newname')

    file_oldname = os.path.join(f'{CONSTANTS.path}{getPath}', getName)
    file_newname_newfile = os.path.join(f'{CONSTANTS.path}{getPath}', getNewName)

    os.rename(file_oldname, file_newname_newfile)

    return 'ok'


'''
Удаление файлов и папок
'''
def deleteFile(args):
    getPath = args.get('path')
    getName = args.get('name')

    filePath = f'{CONSTANTS.path}{getPath}\\{getName}'

    # Удаление файла
    if os.path.isfile(filePath):
        os.remove(filePath)

    # Удаление папки
    if os.path.isdir(filePath):
        shutil.rmtree(filePath, ignore_errors=True)
        #os.rmdir(filePath)

    return 'ok'


'''
Создание папки
'''
def createFolder(args):
    getPath = args.get('path')
    getName = args.get('name')
    os.mkdir(f'{CONSTANTS.path}{getPath}\\{getName}')
    return 'ok'

'''
Создание файла
'''
def createFile(args):
    getPath = args.get('path')
    getName = args.get('name')

    filePath = f'{CONSTANTS.path}{getPath}\\{getName}'

    my_file = open(filePath, "w+")
    my_file.close()

    return 'ok'


'''
Сохранение изменений в файле
'''
def fileSave(request):
    getPath = request.args.get('path')
    getName = request.args.get('name')
    getData = request.form['data']
    getData = getData.replace('\r', '')
    print({'data': getData})

    fullName = f'{CONSTANTS.path}{getPath}/{getName}'

    '''
    f = open(fullName, 'w')
    f.close()
    '''

    with open(fullName, "w", encoding='utf-8') as f:
        f.write(getData)


    return 'ok'