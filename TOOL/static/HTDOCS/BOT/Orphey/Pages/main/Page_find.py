'''
-------------- Цветовая палитра кнопок ВК --------------
negative	-	Красный
positive	-	Зелёный
primary		-	Синий
secondary	-	Белый
--------------------------------------------------------
'''



from DATABASE import sqlighter
import json


def data_clear(app_from, user_id):
	sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = '')



#---------------------------------- Ответы страниц ----------------------------------
def otv_page_confirm(data_page):
	answers_ = {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': []}]}
	answers_['users'][0]['answers'].append({'type': '-', 'text': 'Вы уверены, что хотите сохранить этот запрос:', 'media': []})
	

	# Добавление аудиосообщение в ответ
	if ('links' in data_page):
		answers_['users'][0]['answers'].append(data_page['links'])

	if ('descript' in data_page):
		answers_['users'][0]['answers'].append(data_page['descript'])

	return answers_
#------------------------------------------------------------------------------------


#------------------------------------- Главная -------------------------------------

# Помогает приводить простой список ответов к стандартному виду
def ImportFromStandart(answers = [], page = '-'):
	answers_ = {'users': [{'user_token': '-', 'page': page, 'page_data': '-', 'answers': []}]}
	for i in answers:
		answers_['users'][0]['answers'].append({'type': '-', 'text': i, 'media': []})

	return answers_

class Page_find():
	def __init__(self):
		self.pageName = 'find'
		self.buttons = ['Назад', 'Пропустить', 'Подтвердить', 'Отмена']
	def Keyboard(self, app_from, user_id):

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}
			data_page.update({'form' : 'enter_aud'})
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))


		keyboard = []


		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}

		if ('form' in data_page) and (data_page['form'] != 'confirm'):
			#Инициализация клавиатуры
			keyboard = [
				 [{'text': self.buttons[1], 'color': 'secondary'},]
				,[{'text': self.buttons[0], 'color': 'secondary'},]
			]

		# Подтверждение
		else:
			keyboard = [
				[
					{'text': self.buttons[2], 'color': 'positive'},
					{'text': self.buttons[3], 'color': 'negative'},
				]
			]

		return {'type': 'message', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):
		if(data == self.buttons[0]):
			data_clear(app_from, user_id)
			return ImportFromStandart(page = 'main')
		
		'''
		descript	- описания запроса
		links		- ссылки н mp3 файл и файл на серверах
		'''

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}

		# Ввод аудиосообщения
		# Исполняется в функции Audio_Message
		if ('form' in data_page) and (data_page['form'] == 'enter_aud'):
			# Кнопка пропустить
			if (data == self.buttons[1]):
				data_page['form'] = 'enter_text'
				sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))
				answers = 'Введите описание'
				return ImportFromStandart(answers = [answers])

		# Добавление текста запроса
		if ('form' in data_page) and (data_page['form'] == 'enter_text'):

			# Кнопка пропустить
			if (data == self.buttons[1]):
				data_page['form'] = 'confirm'
				sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))

				# Если ничего не ввели, то вернёт на главную
				if not('descript' in data_page) and not('links' in data_page):
					data_clear(app_from, user_id)
					answers = 'Был введён пустой запрос. Повторите попытку.'
					return ImportFromStandart(answers = [answers], page = 'main')

				return otv_page_confirm(data_page)

			# Ввод описания
			data_page.update({'descript' : {'type': 'text', 'text': data, 'media': []}})
			data_page['form'] = 'confirm'
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))

			return otv_page_confirm(data_page)


		# Подтверждение
		if ('form' in data_page) and (data_page['form'] == 'confirm'):

			# ПОДТВЕРДИТЬ
			if (data == self.buttons[2]):

				# Сохранение в базу
				user_token = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'user_token')
				links = ''
				descript = ''
				if ('links' in data_page):
					data_page['links'].update({'type': 'audio_msg'})
					links = json.dumps(data_page['links'])
				if ('descript' in data_page):
					data_page['descript'].update({'type': 'text'})
					descript = json.dumps(data_page['descript'])
				sqlighter.create_item(app_from = app_from, user_token = user_token, link = links, descript = descript)

				answers = 'Запрос сохранён. Ожидайте помощи.'
				data_clear(app_from, user_id)
				return ImportFromStandart(answers = [answers], page = 'main')

			# ОТМЕНА
			elif (data == self.buttons[3]):
				data_clear(app_from, user_id)
				return ImportFromStandart(page = 'main')


		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}

		if ('form' in data_page):
			if(data_page['form'] == 'enter_text'):
				return ImportFromStandart(answers = ['Добавьте описание:'])
			if(data_page['form'] == 'confirm'):
				return otv_page_confirm(data_page)


		ansver = 'Запишите голосовое сообщение (оно будет полностью анонимным)'
		return ImportFromStandart(answers = [ansver])

	#---------------------------------------------------------------
	# Обработка голосовых сообщений (Обрабатывает главный скрипт, а эта часть делает корректную запись в БД)
	def Audio_Message(self, app_from, user_id, data):

		print('aud_start')

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}

		if ('form' in data_page) and (data_page['form'] == 'enter_aud'):
			data_page.update({'links' : data})
			data_page['form'] = 'enter_text'
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))

			return ImportFromStandart(answers = ['Добавьте описание:'])

		else:
			return ImportFromStandart()


	# Обработка медиа сообщений (Обрабатывает главный скрипт, а эта часть делает корректную запись в БД)
	def Media_Message(self, app_from, user_id, data):

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}

		if (('form' in data_page) and (data_page['form'] != 'enter_text')
			or not('form' in data_page)):
			return ImportFromStandart()

		answers = ['Вы уверены, что хотите сохранить этот запрос:']

		answers_ = {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': []}]}
		answers_['users'][0]['answers'].append({'type': '-', 'text': 'Вы уверены, что хотите сохранить этот запрос:', 'media': []})


		

		# Добавление аудиосообщение в ответ
		if ('links' in data_page):
			answers_['users'][0]['answers'].append(data_page['links'])



		if ('form' in data_page) and (data_page['form'] == 'enter_text'):
			data_page.update({'descript' : data})
			data_page['form'] = 'confirm'
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))

			answers.append(data)


			media = []
			for i in data['media']:
				media.append(i)
			answers_['users'][0]['answers'].append({'type': 'text', 'text': data['text'], 'media': media})

		return answers_
#-----------------------------------------------------------------------------------