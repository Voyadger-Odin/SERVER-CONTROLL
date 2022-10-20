#python.exe C:\Users\Lenovo\Documents\Projekts\Python\BOT\Morty\main_vk.py


'''
-------------- Цветовая палитра кнопок ВК --------------
negative	-	Красный
positive	-	Зелёный
primary		-	Синий
secondary	-	Белый
--------------------------------------------------------
'''

'''

{'users': [{'user_token': '', 'page': '', 'page_data': '', 'answers': [{'type': '', 'text': '', 'media': []}]}]}

users - список с ответами и переходом на страницу для нескольких пользователей, зависящих от ответа
user_token - токен польователя, которому хотим отправить ответ ('-' - отправить текущему пользователю)
page - страница, на которую нужно отправить пользователя ('-' - не менять страницу)
page_data - параметры страницы пользователя ('-' - не менять параметры)
answers - список ответов
---------------------------
type - обязательный параметр при аудиосообщениях или каруселях. В остальных случаях можно не использовать (
		text - текстовый ответ (можно оставить пустым)
		carousel - карусель
		audio_msg - для аудиосообщений
		answer - заменить этот ответ на все стандартные ответы страницы (предыдущие ответы остаются, меняется только этот)
text - текст сообщения
media - вложения
'''


import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
import json
import requests
from threading import Thread
import datetime
import urllib
import urllib3
from pprint import pprint 

from config import TOKEN
from DATABASE import sqlighter
from keyboards import *

app_from = 'vk'

vk_session = vk_api.VkApi(token = TOKEN)
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

session = requests.Session()


# Конструктор клавиатуры
def Create_Keyboard(keyboard_request):
	# Пустая клавиатура
	if((type(keyboard_request) == str) and (keyboard_request == '-')):
		return 	json.dumps({
					"one_time":None,
					"buttons":[]
				}, ensure_ascii = False)

	# Клавиатура страницы
	if (keyboard_request['type'] == 'message'):
		keyboard = {
			"one_time":None,
			"buttons":[]
		}
		line_keys = []


		for keyboard_line in keyboard_request['keyboard']:
			line_keys = []
			for keyboard_key in keyboard_line:

				line_keys.append({
					"action":{
						"type": "text",
						"label": keyboard_key['text']
					},
					"color": keyboard_key['color'] if ('color' in keyboard_key) else "primary"
				})

			keyboard['buttons'].append(line_keys)

		keyboard = json.dumps(keyboard, ensure_ascii = False)

	elif (keyboard_request['type'] == 'inline'):
		keyboard = VkKeyboard(inline = True)
		for keyboard_line in keyboard_request['keyboard']:
			for keyboard_key in keyboard_line:
				keyboard.add_button(keyboard_key['text'])

		keyboard = keyboard.get_keyboard()

	return keyboard


def get_standart_answer(page, app_from, user_id):
	answer = Keyboard_Ansver(page, app_from, user_id)



def one_message(event, vk_session, user_id, data, keyboard):
	if ((data['type'] == '') or (data['type'] == 'text') or (data['type'] == '-')):
		# Текст сообщения
		text = data['text']
		# Вложения сообщения
		attachments = []
		for attach in data['media']:
			attachments.append('{}{}'.format(attach['type'], attach['link_vk']))

		if(keyboard != '-'):
			vk_session.method(	'messages.send', 
								{'peer_id': user_id,
								"message": text,
								'attachment': ','.join(attachments),
								'keyboard': keyboard,
								'random_id': vk_api.utils.get_random_id()}
							)
		else:
			vk_session.method(	'messages.send', 
								{'peer_id': user_id,
								"message": text,
								'attachment': ','.join(attachments),
								'random_id': vk_api.utils.get_random_id()}
							)


	# Аудиосообщения
	if (data['type'] == 'audio_msg'):
		link = data['media'][0]['link_vk']
		vk_session.method('messages.send', {'peer_id': user_id, 'attachment': link , 'random_id': vk_api.utils.get_random_id()})

	# Карусель
	elif (data['type'] == 'carousel'):
		#vk_session.method('messages.send', {'peer_id': user_id, "message": text, 'template': data['data'], 'random_id': vk_api.utils.get_random_id()})
		vk_session.method(	'messages.send',
					{
						'user_id': user_id,
						'message': data['text'][0],
						'template': data['data'],
						'random_id': vk_api.utils.get_random_id()
					}
				)
		vk_session.method(	'messages.send', 
							{'peer_id': user_id,
							"message": data['text'][1],
							'keyboard': keyboard,
							'random_id': vk_api.utils.get_random_id()}
						)
		'''
		if(event.object.client_info['carousel']):
			vk_session.method('messages.send', {'peer_id': user_id, "message": text, 'template': data['data'], 'random_id': vk_api.utils.get_random_id()})
		else:
			vk_session.method('messages.send', {'peer_id': user_id, "message": 'Карусель не поддерживается', 'random_id': vk_api.utils.get_random_id()})
		'''


def message_handler(event, vk, result = '-'):
	text = event.text
	user_id = event.user_id
	# Получает из базы страницу, на которой сейчас находится пользователь
	page = sqlighter.get_user_page(app_from = app_from, user_id = user_id)


	if((type(result) == str) and (result == '-')):
		# Обрабатывает нажатие кнопки. Получает страницу, на которую надо перейти и в некоторых случаях ответ пользователю (Если ответ не пришёл, отвечает стандартным ответом этой страницы)
		result = Keyboard_Events(app_from, page, user_id, text)


	# Перебор всех пользователей
	print(result)
	for user in result['users']:

		user_id = event.user_id
		# Меняем id пользователя, если указан конкретный токен
		if(('user_token' in user) and (user['user_token'] != '-')):
			user_id = sqlighter.get_user_data_from_token(token = user['user_token'], line = 'user_id_vk')
			# Получает из базы страницу, на которой сейчас находится пользователь
			page = sqlighter.get_user_page_from_token(token = user['user_token'])
		else:
			user['user_token'] = sqlighter.get_user_data(app_from = app_from, user_id = user_id, line = 'user_token')

		
		# Меняем страницу, если она указана, иначе остаёмся на этой же
		if(('page' in user) and (user['page'] != '-')):
			page = user['page']

			# Перезаписывает у пользователя страницу
			sqlighter.set_user_page(app_from = app_from, user_id = user_id, page = page)
		else:
			# Получает из базы страницу, на которой сейчас находится пользователь
			page = sqlighter.get_user_page(app_from = app_from, user_id = user_id)

		keyboard = Create_Keyboard(Keyboard_keyboards(app_from, page, user_id))


		
		answers = user['answers']
		# Если ответов нет, ответить стандартными
		if(len(answers) == 0):
			answers = Keyboard_Ansver(page, app_from, user_id)['users'][0]['answers']
		# Перебор ответов для этого пользователя
		for answer in answers:
			one_message(event, vk_session, user_id, answer, keyboard)

	#{'users': [{'user_token': '', 'page': '', 'page_data': '', 'answers': [{'type': '', 'text': '', 'media': []}]}]}
	


def media_Message(event):
	msg = vk.messages.getById(message_ids=event.message_id)
	# Список вложений
	attaches = []
	i = 0
	for attach in msg['items'][0]['attachments']:
		i += 1
		if(attach['type'] == 'photo'):
			photo_url = attach['photo']['sizes'][-1]['url']

			upload = VkUpload(vk_session)
			image = session.get(photo_url, stream=True)
			photo = upload.photo_messages(photos=image.raw)[0]

			d = 'photo{}_{}'.format(photo['owner_id'], photo['id']) # Будет сохранятся в базу

			# Получает из базы страницу, на которой сейчас находится пользователь
			page = sqlighter.get_user_page(app_from = app_from, user_id = event.user_id)
			attaches.append({'type': 'photo', 'link_vk': '{}_{}'.format(photo['owner_id'], photo['id'])})

		elif (attach['type'] == 'audio'):
			link_vk = '{}_{}'.format(attach['audio']['owner_id'], attach['audio']['id'])
			attaches.append({'type': 'audio', 'link_vk': link_vk})

	
	# Получает из базы страницу, на которой сейчас находится пользователь
	page = sqlighter.get_user_page(app_from = app_from, user_id = event.user_id)
	answer_data = {'text': event.raw[5], 'media': attaches}
	media_events = Media_Message(app_from, event.user_id, page, answer_data)

	message_handler(event = event, vk = vk, result = media_events)
	


def audio_message(event):
	# Сообщение о загрузке
	vk_session.method('messages.send', {
		'peer_id': event.peer_id, 
		"message": 'Подождите, пока запись загрузится. Это займёт пару секунд.', 
		'random_id': vk_api.utils.get_random_id(),
		'keyboard': Create_Keyboard('-'),
		})

	# Ссылка на mp3 файл
	link = json.loads(event.raw[7]['attachments'])[0]['audio_message']['link_mp3'] # Файл на серверах VK

	# Ссылка для загрузки на сервера вк
	vk_session.method('messages.setActivity', {'user_id': event.user_id, 'type': 'audiomessage'})
	vk_session.method('messages.markAsRead', {'peer_id': event.peer_id})
	upload_url = vk_session.method("docs.getMessagesUploadServer", {"type": "audio_message", "peer_id": event.peer_id, "v": "5.103"})['upload_url']
	print(upload_url)
	
	# Загрузка файла с интернета
	file = urllib3.PoolManager().request('GET', link).data
	
	# ОТправка файл на сервера
	request = requests.post(upload_url, files={'file': file}, stream = True).json()

	# Данные о загрузки
	save = vk_session.method('docs.save', {"file": request['file']})['audio_message']
	d = 'doc' + str(save['owner_id']) + '_' + str(save['id'])

	# Получает из базы страницу, на которой сейчас находится пользователь
	page = sqlighter.get_user_page(app_from = app_from, user_id = event.user_id)
	data = {'text': '', 'media': [{'link' : link, 'link_vk' : d}], 'type': 'audio_msg'}
	audio_events = Audio_Message(app_from, event.user_id, page, data)

	'''
	# Если был передан ответ, ответить им, иначе ответить стандартным
	answers = Keyboard_Ansver(page, app_from, user_id) if((len(button_events) <= 1) or (type(button_events) == list and len(button_events) >= 2 and button_events[0] == '-')) else button_events[1]
	# Обновляем страницу
	page = audio_events[0].strip()
	# Перезаписывает у пользователя страницу
	sqlighter.set_user_page(app_from = app_from, user_id = event.user_id, page = page)
	# Устанавливаем клавиатуру
	keyboard = Create_Keyboard(Keyboard_keyboards(app_from, page, event.user_id))

	message_sticks(vk_session, event, answers, keyboard)
	'''

	message_handler(event = event, vk = vk, result = audio_events)



def main():

	
	while True:
		try:
			for event in longpoll.listen():
				#Если пришло новое сообщение
				if event.type == VkEventType.MESSAGE_NEW:
					if event.to_me:

						aud_msg = False
						aud_msg = True if ('attach1_kind' in event.raw[7]) and (event.raw[7]['attach1_kind'] == 'audiomsg') else False

						# Сообщения с медиавложениями
						if (aud_msg == False) and (len(event.raw) >= 8) and (event.raw[7] != {}):
							#print('Media')
							#media_Message(event)
							Thread(target=media_Message, args=[event]).start()

						# Текстовые сообщения
						else:

							if (len(event.raw[7]) > 0):
								type_msg = event.raw[7]['attach1_type']
								if (type_msg == 'doc'):
									if ('attachments' in event.raw[7]):
										d = json.loads(event.raw[7]['attachments'])[0]
										if(d['type'] == 'audio_message'):
											#print('audiomessage')
											# Переотправка голосового сообщения пользователя
											Thread(target=audio_message, args=[event]).start()
							else:
								Thread(target=message_handler, args=[event, vk]).start()
		except Exception as e:
			print(e)
		else:
			pass
		finally:
			pass



		
	
	
if __name__ == '__main__':
	print('Inicializ DB')
	sqlighter.init_db(force = False)

	# Добавить столбец в таблицу
	#sqlighter.universal_db_edit(query = 'ALTER TABLE table_name ADD new_column_name column_definition;')

	main()


'''
-------------------------------+ Пример кода +-------------------------------

[ КАРУСЕЛЬ ]
- Она пока не доконца готова

carousel = {
			"type": "carousel",
			"elements": [{
					"photo_id": "-109837093_457242811",
					"action": {
						"type": "open_photo"
					},
					"buttons": [{
						"action": {
							"type": "text",
							"label": "Текст кнопки 🌚",
							"payload": "{}"
						}
					}]
				},
				{
					"photo_id": "-109837093_457242811",
					"action": {
						"type": "open_photo"
					},
					"buttons": [{
						"action": {
							"type": "text",
							"label": "Текст кнопки 2",
							"payload": "{}"
						}
					}]
				},
				{
					"photo_id": "-109837093_457242811",
					"action": {
						"type": "open_photo"
					},
					"buttons": [{
						"action": {
							"type": "text",
							"label": "Текст кнопки 3",
							"payload": "{}"
						}
					}]
				}
			]
		}


answers = [{'type': 'carousel', 'text': ['Карусель', 'Выбери пункт'], 'data': json.dumps(carousel)}]
'''