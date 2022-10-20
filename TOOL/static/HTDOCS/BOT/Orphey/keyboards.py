#Импорт телеграм кнопок
#from telegram import ReplyKeyboardMarkup
#from telegram import KeyboardButton

#from aiogram import types
import json
import os

from DATABASE import sqlighter

#Импорт страниц

'''
#---Главная---
from Pages import main
#from Pages.main import Page_main, Page_find, Page_listen, Page_ansvers
from Pages.main import Page_main
#from Pages.main import Page_find
from Pages.main import Page_listen
from Pages.main import Page_ansvers
#-------------
'''

pages= []

def Pages_Connect(path):
	for file_name in os.listdir(path):

		str_import_from = path.replace('\\', '.').replace('..', '.')
		if(str_import_from[-1] == '.'):
			str_import_from = str_import_from[0: -1]

		if(file_name != '__pycache__') and (file_name != 'STANDART.py'):

			file=os.path.join(path,file_name)


			# Если это папка
			if os.path.isdir(file):
				com = 'from {} import {}'.format(str_import_from, file_name)
				exec(com)

				Pages_Connect('{}\\{}'.format(path, file_name))

			# Если это файл
			else:
				if(file_name[-3:] == '.py'):
					file_name = file_name[:-3]
					com = 'from {} import {}'.format(str_import_from, file_name)
					exec(com)

					com = 'pages.append({}.{}())'.format(file_name, file_name)
					exec(com)
					



# Автоматическое подключение страниц
path = 'Pages\\'
print('Start loading pages...')
Pages_Connect(path)
print('Pages loaded.')


'''
pages = [
		#Главная
		Page_main.Page_main(), Page_find.Page_find(), Page_listen.Page_listen(), Page_ansvers.Page_ansvers()
		]
'''



#------------------------------------- Выборка страницы -------------------------------------
def Keyboard_keyboards(app_from, page, user_id):
	# app_from - Откуда пришёл запрос (телеграм, вк)
	for p in pages:
		if(page == p.pageName):
			keyboard_request = p.Keyboard(app_from, user_id)
			return keyboard_request
#--------------------------------------------------------------------------------------------

#------------------------------------- Обработчик нажатий -------------------------------------
def Keyboard_Events(app_from, page, user_id, data):
	p_ = [page]

	if(data == 'ПОМОГИ') or (data == '🆘'):
		sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = '')
		return {'users': [{'user_token': '-', 'page': 'main', 'page_data': '-', 'answers': []}]}

	for p in pages:
		if(page == p.pageName):
			p_ = p.Keyboard_Events(app_from, user_id, data)
			if(p_ == '-'):
				p_ = p.Ansver(app_from, user_id)
			return p_
#----------------------------------------------------------------------------------------------

#------------------------------------- Ответ -------------------------------------
def Keyboard_Ansver(page, app_from, user_id):
	for p in pages:
		if(page == p.pageName):
			return p.Ansver(app_from, user_id)
	#Стандартный ответ
	return 'Выбери пункт:'
#---------------------------------------------------------------------------------

#------------------------------------ Медиосообщение ------------------------------------
def Media_Message(app_from, user_id, page, media_data):
	p_ = [page]
	for p in pages:
		if(page == p.pageName):
			try:
				p_ = p.Media_Message(app_from, user_id, media_data)
				if(p_ != '-'):
					return p_
			except Exception as e:
				print(e)
	
			return p.Ansver(app_from, user_id)
#----------------------------------------------------------------------------------------


#------------------------------------ Аудиосообщение ------------------------------------
def Audio_Message(app_from, user_id, page, audio_data):
	p_ = [page]
	for p in pages:
		if(page == p.pageName):
			try:
				p_ = p.Audio_Message(app_from, user_id, audio_data)
				if(p_ != '-'):
					return p_
			except Exception as e:
				pass
	
			return p.Ansver(app_from, user_id)
#----------------------------------------------------------------------------------------