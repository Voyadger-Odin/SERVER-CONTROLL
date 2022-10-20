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




#------------------------------------- Главная -------------------------------------

# Помогает приводить простой список ответов к стандартному виду
def ImportFromStandart(answers = [], page = '-'):
	answers_ = {'users': [{'user_token': '-', 'page': page, 'page_data': '-', 'answers': []}]}
	for i in answers:
		answers_['users'][0]['answers'].append({'type': '-', 'text': i, 'media': []})

	return answers_


class Page_main():
	def __init__(self):
		self.pageName = 'main'
		self.buttons = [
			'Найти музыку', 
			'Помочь найти другим', 
			'Раздел СМОТРЕТЬ ПОЗЖЕ', 
			'Найденные',
		]
	def Keyboard(self, app_from, user_id):
		
		#Инициализация клавиатуры
		keyboard = [
			[
				{'text': self.buttons[0], 'color': 'positive'},
				{'text': self.buttons[3], 'color': 'positive'},
			],
			[
				{'text': self.buttons[1], 'color': 'primary'},
				{'text': self.buttons[2], 'color': 'secondary'},
			],
		]

		return {'type': 'message', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		

		# Оставить запрос
		if (data == self.buttons[0]):
			return ImportFromStandart(page = 'find')

		# Помочь найти другим
		if (data == self.buttons[1]):
			return ImportFromStandart(page = 'listen')

		# Смотреть позже
		if (data == self.buttons[2]):
			return ImportFromStandart(page = 'look_later')

		# Ответы на запросы
		if (data == self.buttons[3]):
			return ImportFromStandart(page = 'answers')


		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		reting = {'confirmed': 0, 'non_confirmed': 0}

		try:
			reiting_str = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'reting')
			if(reiting_str != None and reiting_str != ''):
				reting = json.loads(reiting_str)
		except Exception:
			pass

		text = 'Добро пожаловать\n\n' + 'На данный момент у вас:\n' + str(reting['confirmed']) + ' правильных ответов\n'+ str(reting['non_confirmed']) + ' не правильных ответов'

		ansvers = {'users': [{'user_token': '-', 'page': '-', 'page_data': '-', 'answers': [
			{'type': '-', 'text': text, 'media': []}
		]}]}
		return ansvers
#-----------------------------------------------------------------------------------