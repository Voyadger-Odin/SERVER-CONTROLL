'''
-------------- Цветовая палитра кнопок ВК --------------
negative	-	Красный
positive	-	Зелёный
primary		-	Синий
secondary	-	Белый
--------------------------------------------------------

{'type': 'message', 'keyboard': keyboard}
'type' - 'message' - Клавиатура в сообщении
'type' - 'inline'  - Клавиатура снизу
'keyboard' - разметка клавиатуры

'''



from DATABASE import sqlighter
import json



def get_items_count(app_from, user_id):
	token_user = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
	return sqlighter.get_all_count_look_leter_for_user(token = token_user)


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


def change_item(app_from, user_id, data_page, count):
	id_new = int(data_page['id_item'])
	token_user = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)

	if (count >= 2):
		while (data_page['id_item'] == id_new):
			id_new = int(sqlighter.get_random_item_saved(token = token_user))
	elif (count == 1):
		id_new = int(sqlighter.get_random_item_saved(token = token_user))
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

	# Удаляет из сохранённого списка
	sqlighter.delete_saved_item(token = token_user_answer, item_id = id_query)

	#------------------
	
	# Сообщение оставившему запрос
	user_query_answers = {'user_token': token_user_query, 'page': '-', 'page_data': '-', 'answers': [
		{'type': '-', 'text': 'На ваш запрос:\n\n', 'media': []},
	] + get_item(id_query) + [
		{'type': '-', 'text': 'дали ответ:\n\n{}'.format(data['text']), 'media': data['media']},
	]}

	count = get_items_count(app_from, user_id)


	#----- Сообщение тому, кто дал ответ -----
	data_page['id_item'] = int(change_item(		# Перелистование записи
		app_from, 
		user_id, 
		json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')), 
		get_items_count(app_from, user_id)
	))

	if (count > 0):
		user_answer_answers = {'user_token': '-', 'page': '-', 'page_data': '-', 'answers': [
			{'type': '-', 'text': 'Ваш ответ успешно отправлен\n\nЕсли узнал что это, пиши название:', 'media': []},
		] + get_item(data_page['id_item'])}
	else:
		user_answer_answers = {'user_token': '-', 'page': '-', 'page_data': '-', 'answers': [
			{'type': '-', 'text': 'Ваш ответ успешно отправлен\n\nРадел пока пуст, вы ответели на все сохранённые вопросы. Вы можете ответить на вопросы из общего списка', 'media': []},
		]}

	sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))

	return {'users': [user_query_answers, user_answer_answers]}




def data_clear(app_from, user_id):
	sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = '')
#------------------------------------- Главная -------------------------------------

# Помогает приводить простой список ответов к стандартному виду
def ImportFromStandart(answers = [], page = '-'):
	answers_ = {'users': [{'user_token': '-', 'page': page, 'page_data': '-', 'answers': []}]}
	for i in answers:
		answers_['users'][0]['answers'].append({'type': '-', 'text': i, 'media': []})

	return answers_


class Page_look_later():
	def __init__(self):
		self.pageName = 'look_later'
		self.buttons = ['Назад', '♻', '🚫', '🔔', 'Общий список']

		self.BUTTON_NEXT = '➡'
		#self.BUTTON_PREV = '⬅'
	def Keyboard(self, app_from, user_id):
		keyboard = []

		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {'id_item': -1}
		
		count = get_items_count(app_from, user_id)
		if(count > 0):
			if (count > 1):
				keyboard.append([
						# Жалоба
						#{'text': self.buttons[2], 'color': 'negative'},
						# Удалить
						{'text': self.buttons[1], 'color': 'negative'},
						# Уведомить
						#{'text': self.buttons[3], 'color': 'positive'},
						# Сменить
						{'text': self.BUTTON_NEXT, 'color': 'secondary'}
					])
			else:
				keyboard.append([
						# Удалить
						{'text': self.buttons[1], 'color': 'negative'},
						# Уведомить
						#{'text': self.buttons[3], 'color': 'positive'},
					])

		else:
			keyboard.append([
					# Общий список
					{'text': self.buttons[4], 'color': 'primary'},
				])

		keyboard.append([
					{'text': self.buttons[0], 'color': 'secondary'},
				])

		return {'type': 'message', 'keyboard': keyboard}



	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {'id_item': -1}

		count = get_items_count(app_from, user_id)
		if(count > 0):
			answers = [{'text': 'Если узнал что это, пиши название:', 'media': [], 'type': 'text'}]
			data_page['id_item'] = change_item(app_from, user_id, data_page, count)
			sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))
			return {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': answers + get_item(data_page['id_item']) }]}
		else:
			text = 'Радел пока пуст'
			ansvers = {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': [{'type': '-', 'text': text, 'media': []}]}]}
			return ansvers




	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		# Назад
		if (data == self.buttons[0]):
			data_clear(app_from, user_id)
			return ImportFromStandart(page = 'main')




		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {'id_item': -1}

		# Удалить
		if (data == self.buttons[1]):
			token = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
			sqlighter.delete_saved_item(token = token, item_id = data_page['id_item'])
			answers = ImportFromStandart(answers = ['Запись удалена из вашего списка'])
			answers['users'][0]['answers'] += self.Ansver(app_from, user_id)['users'][0]['answers']
			return answers

		count = get_items_count(app_from, user_id)


		if (count > 1):
			# Следующая запись
			if(data == self.BUTTON_NEXT):
				return ImportFromStandart(page = '-')

		elif (count == 1):
			pass
		else:
			# Общий список
			if (data == self.buttons[4]):
				data_clear(app_from, user_id)
				return ImportFromStandart(page = 'listen')


		# Ответ
		if (count >= 1):
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