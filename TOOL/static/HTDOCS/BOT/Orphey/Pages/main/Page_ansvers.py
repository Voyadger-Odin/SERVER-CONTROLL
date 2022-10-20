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



def get_items(app_from, user_id):
	token_user = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
	return sqlighter.get_all_answers_for_user(user_token = token_user)


def get_item(item_id):
	answers = []

	# Описание
	#descript = sqlighter.get_item_data(app_from = app_from, user_id = user_id, line = 'descript', line_selector = 'id', line_selector_value = data_page['id_item'])
	descript = sqlighter.get_data(table_name = 'items', line = 'descript', line_selector = 'id', line_selector_value = item_id)
	#print(descript)
	if (descript != None) and (descript != ''):
		#print(descript)
		answers.append(json.loads(descript))

	
	# Аудиосообщение
	links = sqlighter.get_data(table_name = 'items', line = 'link', line_selector = 'id', line_selector_value = item_id)
	if (links != None) and (links != ''):
		answers.append(json.loads(links))


	return answers




def OK_Button(app_from, user_id):
	data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
	if(data_page_str != None) and (data_page_str != ''):
		data_page = json.loads(data_page_str)

	item = json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data'))['item']
	user_answer_token = item[3]
	id_item = item[2]

	reting_str = sqlighter.get_user_data_from_token(token = user_answer_token, line = 'reting')
	if((reting_str == None) or (reting_str == '')):
		reting = {'confirmed': 1, 'non_confirmed': 0}
	else:
		reting = json.loads(reting_str)
		reting['confirmed'] += 1


	# Сохранение данных страницы
	sqlighter.set_user_data_from_token(token = user_answer_token, line = 'reting', data = json.dumps(reting))
	
	# Сообщение пользователю, давшему ответ
	answers = [{'type': 'text', 'text': 'Ваш ответ подтвердился.', 'media': []}]

	sqlighter.delete_answer(item_id = id_item)
	sqlighter.delete_item(item_id = id_item)

	return {'users': [
				# Сообщение пользователю, давшему ответ
				{'user_token': user_answer_token, 'page': '-', 'page_data': '-', 'answers': answers},
				# Сообщение пользователю, оставившему запрос
				{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': []},
			]}


def NO_Button(app_from, user_id):
	data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
	if(data_page_str != None) and (data_page_str != ''):
		data_page = json.loads(data_page_str)

	item = json.loads(sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data'))['item']
	user_answer_token = item[3]
	id_item = item[0]

	reting_str = sqlighter.get_user_data_from_token(token = user_answer_token, line = 'reting')
	if((reting_str == None) or (reting_str == '')):
		reting = {'confirmed': 0, 'non_confirmed': 1}
	else:
		reting = json.loads(reting_str)
		reting['non_confirmed'] += 1


	# Сохранение данных страницы
	sqlighter.set_user_data_from_token(token = user_answer_token, line = 'reting', data = json.dumps(reting))
	
	# Сообщение пользователю, давшему ответ
	answers = [{'type': 'text', 'text': 'Ваш ответ был не правильным.', 'media': []}]

	sqlighter.delete_answer_by_id(item_id = id_item)

	return {'users': [
				# Сообщение пользователю, давшему ответ
				{'user_token': user_answer_token, 'page': '-', 'page_data': '-', 'answers': answers},
				# Сообщение пользователю, оставившему запрос
				{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': []},
			]}
	

def data_clear(app_from, user_id):
	sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = '')

#------------------------------------- Слушать записи -------------------------------------
# Помогает приводить простой список ответов к стандартному виду
def ImportFromStandart(answers = [], page = '-'):
	answers_ = {'users': [{'user_token': '-', 'page': page, 'page_data': '-', 'answers': []}]}
	for i in answers:
		answers_['users'][0]['answers'].append({'type': '-', 'text': i, 'media': []})

	return answers_

class Page_ansvers():
	def __init__(self):
		self.pageName = 'answers'
		self.buttons = ['Назад', '👎', '👍', '🚫']

	def Keyboard(self, app_from, user_id):
		#Инициализация клавиатуры
		keyboard = []

		token_user_answer = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
		count = int(sqlighter.get_all_count_answers_for_user(token = token_user_answer))
		
		if(count != 0):
			keyboard.append([
				#{'text': self.buttons[3], 'color': 'negative'},
				{'text': self.buttons[1], 'color': 'negative'},
				{'text': self.buttons[2], 'color': 'positive'},
			])
		

		keyboard.append(
			[
				{'text': self.buttons[0], 'color': 'secondary'},
			],
		)



		return {'type': 'message', 'keyboard': keyboard}


	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		#20201011225424794983:USER:611375867
		
		
		data_page_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'data')
		if(data_page_str != None) and (data_page_str != ''):
			data_page = json.loads(data_page_str)
		else:
			data_page = {'item':''}


		ansvers = {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': 
				[{'type': '-', 'text': 'Пока нет ответов. Как кто-то ответит на ваш запрос, вам придёт уведомление.', 'media': []}]
			}]}

		items = get_items(app_from, user_id)
		if(len(items) > 0):
			(_id,_token,item_id,_token_user_answer,_answer) = items[0]
			# Получаем запись
			item = get_item(item_id)

			data_page['item'] = items[0]

			ansvers = {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': 
				[{'type': '-', 'text': 'На запись:', 'media': []}]
				+get_item(item_id)
				+[{'type': '-', 'text': 'Был дан ответ:', 'media': []}]
				+[json.loads(_answer)]
			}]}

		# Сохранение данных страницы
		sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = json.dumps(data_page))
		return ansvers



	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):
		
		# Меню
		if(data == self.buttons[0]):
			data_clear(app_from, user_id)
			return ImportFromStandart(page = 'main')

		# Кнопка подтверждения
		if(data == self.buttons[2]):
			return OK_Button(app_from, user_id)

		# Кнопка отклонения
		if(data == self.buttons[1]):
			return NO_Button(app_from, user_id)


		return '-'
	
#-----------------------------------------------------------------------------------