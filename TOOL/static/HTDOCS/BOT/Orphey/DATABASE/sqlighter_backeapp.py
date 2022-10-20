#python.exe C:\Users\Lenovo\Documents\Projekts\Python\BOT\BOTAY_BOT\THE_BEST\DATABASE\sqlighter.py

import sqlite3
import json
import datetime

#==================================== Генератор токенов ====================================
def TokenGenerator(data):
	token = '{0}:{1}'.format(
		str(datetime.datetime.now()).replace(' ','').replace(':','').replace('-','').replace('.','')
		, data)
	return token
#===========================================================================================

def ensure_connection(func):
	def inner(*args, **kwargs):
		with sqlite3.connect('DATABASE/users_data.sqlite') as conn:
			res = func(*args, conn = conn, **kwargs)
		return res
	return inner






@ensure_connection
def init_db_users(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS users')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id 					INTEGER PRIMARY KEY,
			user_token 			TEXT NOT NULL,

			page 				TEXT NOT NULL,
			data 				TEXT,

			user_id_vk 			INTEGER,
			user_id_telegram 	INTEGER
		)
	''')

	# Сохранить изменения
	conn.commit()


#============================================ Обработка пользователей ============================================



@ensure_connection
def set_user_page(conn, app_from: str, user_id: int, page: str):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('UPDATE users SET page = ? WHERE {0} = ?'.format(app), (page, user_id))
	conn.commit()

# СОЗДАЁТ НОВОГО ПОЛЬЗОВАТЕЛЯ, ЕСЛИ НЕТУ
@ensure_connection
def get_user_page(conn, app_from: str, user_id: int):
	cursor = conn.cursor()

	# Получает колличество пользователей с переданым user_id (0 или 1)
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('SELECT COUNT(*) FROM users WHERE {0} = ? LIMIT 1'.format(app), (user_id, ))

	(find_user, ) = cursor.fetchone()
	if(find_user == 0):
		print('Новый пользователь')

		user_id_vk = 0
		user_id_telegram = 0

		if app_from == 'vk':
			user_id_vk = user_id
		elif app_from == 'telegram':
			user_id_telegram = user_id

		token = TokenGenerator('USER:{0}'.format(user_id))

		start_page = 'main'
		balance = json.dumps({'sum': 0, 'random_key': '1234567'})

		cursor.execute('''INSERT INTO users (
			user_token,
			page,
			{0}
			) VALUES (?, ?, ?)'''.format(app)
			,(token, start_page, user_id, ))

	cursor.execute('SELECT page FROM users WHERE {0} = ?'.format(app), (user_id, ))
	(page, ) = cursor.fetchone()
	return page


# Получает указанное поле у пользователя
@ensure_connection
def get_user_data(conn, app_from: str, user_id: int, line: str):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('SELECT {0} FROM users WHERE {1} = ?'.format(line, app), (user_id, ))
	(data, ) = cursor.fetchone()
	return data


# Записывает информацию в указанное поле
@ensure_connection
def set_user_data(conn, app_from: str, user_id: int, line: str, data: str):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('UPDATE users SET {0} = ? WHERE {1} = ?'.format(line, app), (data, user_id))
	conn.commit()
#=================================================================================================================





@ensure_connection
def init_db_items(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS items')

	'''
	user_token 			TEXT NOT NULL,	# Токен того, кто добавил запрос

	link 				TEXT NOT NULL, 	# Словарь, содержащий ссылку на mp3 файл и сылку на файл соц. сетей
	confirmation 		TEXT			# Подтверждён ли
	'''
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS items (
			id 					INTEGER PRIMARY KEY,
			user_token 			TEXT NOT NULL,

			link 				TEXT,
			descript			TEXT,
			confirmation 		TEXT
		)
	''')

	# Сохранить изменения
	conn.commit()


#============================================ Обработка запросов ============================================

# СОЗДАЁТ НОВУЮ ЗАПИСЬ
@ensure_connection
def create_item(conn, app_from: str, user_token: str, link: str, descript: str):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO items (
			user_token,
			link,
			descript
			) VALUES (?, ?, ?)'''
			,(user_token, link, descript))
	return 'OK'


# Получает указанное поле
@ensure_connection
def get_item_data(conn, app_from: str, user_id: int, line: str, line_selector: str, line_selector_value: str):
	cursor = conn.cursor()
	cursor.execute('SELECT {0} FROM items WHERE {1} = {2}'.format(line, line_selector, line_selector_value))
	(data, ) = cursor.fetchone()
	return data


# Записывает информацию в указанное поле
@ensure_connection
def set_item_data(conn, app_from: str, user_id: int, line: str, data: str):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('UPDATE items SET {0} = ? WHERE {1} = ?'.format(line, app), (data, user_id))
	conn.commit()


# Случайная запись
@ensure_connection
def get_random_item(conn):
	cursor = conn.cursor()
	cursor.execute('SELECT id FROM items ORDER BY RANDOM() LIMIT 1')
	(data, ) = cursor.fetchone()
	return data


# Получает указанное поле у пользователя
@ensure_connection
def get_count_items(conn):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM items LIMIT 1')
	(data, ) = cursor.fetchone()
	return data
#=================================================================================================================





@ensure_connection
def init_db(conn, force: bool = False):
	init_db_users(force = force)
	init_db_items(force = force)



if __name__ == '__main__':
	print('Соединение с базой')
	init_db_users(force = False)
	#print(set_user_page(user_id = 123, page = 'page_new_2'))
	#print(set_user_page(user_id = 1234, page = 'page_new_3'))

	#print(get_user_page(user_id = 1235))