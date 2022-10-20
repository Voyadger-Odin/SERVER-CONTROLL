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



def get_item(item_id):
	#answers = [{'text': 'Если узнал что это, пиши название:', 'media': [], 'type': 'text'}]
	answers = []

	# Описание
	#descript = sqlighter.get_item_data(app_from = app_from, user_id = user_id, line = 'descript', line_selector = 'id', line_selector_value = data_page['id_item'])
	descript = sqlighter.get_data(table_name = 'items', line = 'descript', line_selector = 'id', line_selector_value = item_id)
	#print(descript)
	if (descript != None) and (descript != ''):
		answers.append(json.loads(descript))

	
	# Аудиосообщение
	links = sqlighter.get_data(table_name = 'items', line = 'link', line_selector = 'id', line_selector_value = item_id)
	if (links != None) and (links != ''):
		answers.append(json.loads(links))


	return answers


def change_item(app_from, user_id, data_page):
	id_new = int(data_page['id_item'])
	token_user = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
	count = int(sqlighter.get_count_items(token = token_user))

	if (count >= 2):
		while (data_page['id_item'] == id_new):
			id_new = int(sqlighter.get_random_item(token = token_user))
	elif (count == 1):
		id_new = int(sqlighter.get_random_item(token = token_user))
	else:
		return -1;

	return id_new



# Добавляет ответ в БД
def add_answer(app_from, user_id, data, id_query):
	data_page = json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data'))

	token_user_query = sqlighter.get_data(table_name = 'items', line = 'user_token', line_selector = 'id', line_selector_value = id_query)
	token_user_answer = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)

	#print('{}\n{}\n{}\n{}'.format(id_query, token_user_query, token_user_answer, data)) # id запроса

	# Создаёт запись в базе данных
	data.update({'type': 'text'})
	sqlighter.create_answer(token_user_query = token_user_query, id_query = id_query, token_user_answer = token_user_answer, answer = json.dumps(data))

	#------------------
	# Сообщение оставившему запрос
	user_query_answers = {'user_token': token_user_query, 'page': '-', 'page_data': '-', 'answers': [
		{'type': '-', 'text': 'На ваш запрос:\n\n', 'media': []},
	] + get_item(id_query) + [
		{'type': '-', 'text': 'дали ответ:\n\n{}'.format(data['text']), 'media': data['media']},
	]}



	# Сообщение тому, кто дал ответ
	data_page['id_item'] = int(change_item(app_from, user_id, json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')))) # Перелистование записи
	user_answer_answers = {'user_token': '-', 'page': '-', 'page_data': '-', 'answers': [
		{'type': '-', 'text': 'Ваш ответ успешно отправлен\n\nЕсли узнал что это, пиши название:', 'media': []},
	] + get_item(data_page['id_item'])}

	sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))

	return {'users': [user_query_answers, user_answer_answers]}
	

def data_clear(app_from, user_id):
	sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = '')

#------------------------------------- Слушать записи -------------------------------------

# Помогает приводить простой список ответов к стандартному виду
def ImportFromStandart(answers = [], page = '-'):
	answers_ = {'users': [{'user_token': '-', 'page': page, 'page_data': '-', 'answers': []}]}
	for i in answers:
		answers_['users'][0]['answers'].append({'type': '-', 'text': i, 'media': []})

	return answers_


class Page_listen():
	def __init__(self):
		self.pageName = 'listen'

		'''
		🚫 - Жалоба
		🔔 - Сообщить о выходе
		⏳ - Отложить и подсказать потом
		➡ - Следующая апись
		'''
		self.buttons = ['Назад', '⏳', '🚫', '🔔']

		self.BUTTON_NEXT = '➡'
		#self.BUTTON_PREV = '⬅'
	def Keyboard(self, app_from, user_id):
		#Инициализация клавиатуры
		keyboard = []

		'''
		keyboard.append([
			{'text': self.BUTTON_PREV, 'color': 'secondary'},
			{'text': self.BUTTON_NEXT, 'color': 'secondary'},
		])
		'''

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {'id_item': -1}
		item_id = change_item(app_from, user_id, data_page)

		if(item_id != -1):
			keyboard.append([
				# Жалоба
				#{'text': self.buttons[2], 'color': 'negative'},
				# Смотреть позже
				{'text': self.buttons[1], 'color': 'positive'},
				# Уведомить
				#{'text': self.buttons[3], 'color': 'positive'},
				# Сменить
				{'text': self.BUTTON_NEXT, 'color': 'secondary'},
			])


		keyboard.append(
			[
				{'text': self.buttons[0], 'color': 'secondary'},
			],
		)



		return {'type': 'message', 'keyboard': keyboard}


	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		answers = [{'text': 'Список запросов пуст, но вы можете оставить свой запрос.', 'media': [], 'type': 'text'}]

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}

		if not('id_item' in data_page):
			data_page.update({'id_item': -1})
			item_id = change_item(app_from, user_id, data_page)
			
			if (item_id != -1):
				data_page['id_item'] = item_id
				sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))

		#print('\n{}\n'.format(data_page['id_item']))

		if (data_page['id_item'] != -1):
			answers = [{'text': 'Если узнал что это, пиши название:', 'media': [], 'type': 'text'}]
			answers += get_item(data_page['id_item'])

		return {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': answers}]}



	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {}


		
		# Меню
		if (data == self.buttons[0]):
			data_clear(app_from, user_id)
			return ImportFromStandart(page = 'main')



		# Посмотреть позже
		if (data == self.buttons[1]):
			# Сохраняет запись
			
			count_item = sqlighter.get_count_look_leter_by_item(id_item = data_page['id_item']) 
			
			if (count_item <= 0):
				token_user = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
				sqlighter.save_item(id_query = data_page['id_item'], token_user_save = token_user)

				ansvers = ImportFromStandart(answers = ['Запись добавлена в раздел "Смотреть позже". В сможете вернуться к ней, когда вам станет удобно.'])
			else:
				ansvers = ImportFromStandart(answers = ['Эта запись уже у вас сохранена.'])

			id_new = change_item(app_from, user_id, json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')))
			data_page['id_item'] = id_new
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))


			ansvers['users'][0]['answers'] += self.Ansver(app_from, user_id)['users'][0]['answers']

			return ansvers




		# Следующая запись
		if(data == self.BUTTON_NEXT):
			id_new = change_item(app_from, user_id, json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')))
			data_page['id_item'] = id_new
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))
			return ImportFromStandart(page = '-')


		# Сообщить о выходе
		if (data == self.buttons[3]):
			# Сохранение в базу
			id_query = data_page['id_item']
			token_user_save = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)

			if (sqlighter.test_alarm_item_saved(id_query = id_query, token_user_save = token_user_save) == 0):
				id_user_save = sqlighter.get_data(table_name = 'users', line = 'id', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
				sqlighter.save_item_alarm(id_query = id_query, token_user_save = token_user_save, id_user_save = id_user_save)

				ansvers = ImportFromStandart(answers = ['Запись добавлена в список уведомений. Когда её найдут, вам сообщат.'])

			else:
				ansvers = ImportFromStandart(answers = ['Вы уже добавили эту запись.'])

			# Смена записи отображения
			id_new = change_item(app_from, user_id, json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')))
			data_page['id_item'] = id_new
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))


			ansvers['users'][0]['answers'] += self.Ansver(app_from, user_id)['users'][0]['answers']

			return ansvers



		# Ответ
		data = {'text': data, 'media': [], 'type': 'text'}
		return add_answer(app_from, user_id, data, data_page['id_item'])
		
		
		return '-'
	


	# Обработка медиа сообщений (Обрабатывает главный скрипт, а эта часть делает корректную запись в БД)
	def Media_Message(self, app_from, user_id, data):
		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		return add_answer(app_from, user_id, data, data_page['id_item'])
#-----------------------------------------------------------------------------------