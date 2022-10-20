

from flask import Flask, request, redirect

from TOOL.models import api
from TOOL.models import IndexModel, EditorModel, ConsoleModel

from TOOL import CONSTANTS

from TOOL.DATABASE import sqlighter



app = Flask(__name__)

'''
Главная страница
'''
@app.route('/')
@app.route('/index.html')
def index():
    GETPath = request.args.get('path')
    if (GETPath is None):
        return redirect('?path=')
    return IndexModel.index(request.args, CONSTANTS.path)


'''
Редактор кода
'''
@app.route('/editor')
def editor():
    return EditorModel.editor(request.args)



'''
Запуск консоли
'''
@app.route('/cmd')
def cmd():
    return ConsoleModel.cmd(request)




#=================== API ===================#


'''
Получение списка процессов
'''
@app.route('/api/getallprocess')
def getallprocess():
    return api.getAllProcess()

'''
Получение консоли
'''
@app.route('/api/getconsole')
def getconsole():
    return ConsoleModel.getConsole(request)

'''
Остановка консоли
'''
@app.route('/api/stopscript')
def stopscript():
    return ConsoleModel.stopscript(request)



'''
Управление файлами
'''
@app.route('/api/uploadfile', methods = ['GET', 'POST', 'DELETE'])
def uploadFile():
    return api.uploadFile(request)

'''
Разархивирование
'''
@app.route('/api/uparchiv')
def uparchiv():
    return api.uparchiv(request)

'''
Переиминовывание файла/папки
'''
@app.route('/api/renamefile')
def renameFile():
    return api.renameFile(request.args)

'''
Удаление файла/папки
'''
@app.route('/api/deletefile')
def deleteFile():
    return api.deleteFile(request.args)

'''
Создание новой папки
'''
@app.route('/api/createfolder')
def createFolder():
    return api.createFolder(request.args)

'''
Создание нового файла
'''
@app.route('/api/createfile')
def createFile():
    return api.createFile(request.args)

'''
Сохранение изменений в файле
'''
@app.route('/api/filesave', methods = ['GET', 'POST', 'DELETE'])
def fileSave():
    return api.fileSave(request)

#===========================================#




def start():
    print('Inicializ DB')
    sqlighter.init_db(force=False)
    ConsoleModel.startAllConsoles()
    app.run(debug=False)

if __name__ == '__main__':
    start()