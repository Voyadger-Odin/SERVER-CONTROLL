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


@ensure_connection
def universal_db_edit(conn, query:str):
	cursor = conn.cursor()
	cursor.execute(query)


#============================================ Обработка пользователей ============================================



@ensure_connection
def set_user_page(conn, app_from: str, user_id: int, page: str):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('UPDATE users SET page = ? WHERE {0} = ?'.format(app), (page, user_id))
	conn.commit()

@ensure_connection
def set_user_page_from_token(conn, token: str, page: str):
	cursor = conn.cursor()
	cursor.execute('UPDATE users SET page = ? WHERE user_token = ?', (page, token))
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

@ensure_connection
def get_user_page_from_token(conn, token: str):
	cursor = conn.cursor()
	cursor.execute('SELECT page FROM users WHERE user_token = ?', (token, ))
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

# Получает указанное поле у пользователя
@ensure_connection
def get_user_data_from_token(conn, token: str, line: str):
	cursor = conn.cursor()
	cursor.execute('SELECT {0} FROM users WHERE user_token = ?'.format(line), (token, ))
	(data, ) = cursor.fetchone()
	return data


# Записывает информацию в указанное поле
@ensure_connection
def set_user_data(conn, app_from: str, user_id: int, line: str, data: str):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('UPDATE users SET {0} = ? WHERE {1} = ?'.format(line, app), (data, user_id))
	conn.commit()

# Записывает информацию в указанное поле
@ensure_connection
def set_user_data_from_token(conn, token: str, line: str, data: str):
	cursor = conn.cursor()
	cursor.execute('UPDATE users SET {0} = ? WHERE user_token = ?'.format(line, ), (data, token))
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
def get_item_data(conn, line: str, line_selector: str, line_selector_value: str):
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
def get_random_item(conn, token: str):
	cursor = conn.cursor()
	cursor.execute('SELECT id FROM items WHERE user_token != ? ORDER BY RANDOM() LIMIT 1', (token, ))
	#cursor.execute('SELECT id FROM items ORDER BY RANDOM() LIMIT 1')
	(data, ) = cursor.fetchone()
	return data


# Получает указанное поле у пользователя
@ensure_connection
def get_count_items(conn, token: str):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM items WHERE user_token != ? LIMIT 1', (token, ))
	(data, ) = cursor.fetchone()
	return data


# Удаляет запрос
@ensure_connection
def delete_item(conn, item_id: int):
	cursor = conn.cursor()
	cursor.execute('DELETE FROM items WHERE id = {}'.format(item_id))
	conn.commit()
#=================================================================================================================


#============================================ Список ответов ============================================
'''
token_user_query - токен пользователя, чей запрос
id_query - id запроса в базе
token_user_answer - токен польователя, чей ответ
answer - сам ответ
'''

@ensure_connection
def init_db_answers(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS answers')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS answers (
			id 					INTEGER PRIMARY KEY,

			token_user_query 	TEXT,
			id_query 			INTEGER,
			token_user_answer	TEXT,
			answer 				TEXT
		)
	''')

	# Сохранить изменения
	conn.commit()

# СОЗДАЁТ НОВУЮ ЗАПИСЬ
@ensure_connection
def create_answer(conn, token_user_query: str, id_query: int, token_user_answer: str, answer: str):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO answers (
			token_user_query,
			id_query,
			token_user_answer,
			answer
			) VALUES (?, ?, ?, ?)'''
			,(token_user_query, id_query, token_user_answer, answer))
	return 'OK'


# Получает указанное поле
@ensure_connection
def get_answer_data(conn, app_from: str, user_id: int, line: str, line_selector: str, line_selector_value: str):
	cursor = conn.cursor()
	cursor.execute('SELECT {0} FROM answers WHERE {1} = {2}'.format(line, line_selector, line_selector_value))
	(data, ) = cursor.fetchone()
	return data


# Записывает информацию в указанное поле
@ensure_connection
def set_answer_data(conn, app_from: str, user_id: int, line: str, data: str):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('UPDATE answers SET {0} = ? WHERE {1} = ?'.format(line, app), (data, user_id))
	conn.commit()

# Получает указанное поле у пользователя
@ensure_connection
def get_all_answers_for_user(conn, user_token: str):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM answers WHERE token_user_query = ?', (user_token, ))
	return cursor.fetchall()

# Получает указанное поле у пользователя
@ensure_connection
def get_all_count_answers_for_user(conn, token: str):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM answers WHERE token_user_query = ?', (token, ))
	(data, ) = cursor.fetchone()
	return data


# Получает указанное поле у пользователя
@ensure_connection
def get_count_answers(conn):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM answers LIMIT 1')
	(data, ) = cursor.fetchone()
	return data

# Удаляет ответ
@ensure_connection
def delete_answer(conn, item_id: int):
	cursor = conn.cursor()
	cursor.execute('DELETE FROM answers WHERE id_query = {}'.format(item_id))
	conn.commit()

# Удаляет ответ
@ensure_connection
def delete_answer_by_id(conn, item_id: int):
	cursor = conn.cursor()
	cursor.execute('DELETE FROM answers WHERE id = {}'.format(item_id))
	conn.commit()
#=================================================================================================================





#============================================ Смотреть позже ============================================

@ensure_connection
def init_db_look_leter(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS look_leter')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS look_leter (
			id 					INTEGER PRIMARY KEY,

			id_query 			INTEGER,
			token_user_save		TEXT
		)
	''')

	# Сохранить изменения
	conn.commit()

# СОЗДАЁТ НОВУЮ ЗАПИСЬ
@ensure_connection
def save_item(conn, id_query: int, token_user_save: str):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO look_leter (
			id_query,
			token_user_save
			) VALUES (?, ?)'''
			,(id_query, token_user_save))
	return 'OK'


# Получает указанное поле у пользователя
@ensure_connection
def get_all_count_look_leter_for_user(conn, token: str):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM look_leter WHERE token_user_save = ?', (token, ))
	(data, ) = cursor.fetchone()
	return data

# Случайная запись
@ensure_connection
def get_random_item_saved(conn, token: str):
	cursor = conn.cursor()
	cursor.execute('SELECT id_query FROM look_leter WHERE token_user_save = ? ORDER BY RANDOM() LIMIT 1', (token, ))
	(data, ) = cursor.fetchone()
	return data

# Удаляет сохранённую запись
@ensure_connection
def delete_saved_item(conn, token: str, item_id: int):
	cursor = conn.cursor()
	cursor.execute('DELETE FROM look_leter WHERE (id_query = {} and token_user_save = ?)'.format(item_id), (token, ))
	conn.commit()


# Узнаёт, сколько запросов с таким id сохранено
@ensure_connection
def get_count_look_leter_by_item(conn, id_item: int):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM look_leter WHERE id_query = ?', (id_item, ))
	(data, ) = cursor.fetchone()
	return data

#=================================================================================================================





#============================================ Смотреть позже ============================================

@ensure_connection
def init_db_alarm(conn, force: bool = False):
	'''
	id_query - id записи, на выход которой подписывается пользователь
	token_user_save - токен пользователя, который подписывается
	id_user_save - id пользователя, который подписывается
	'''
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS alarm')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS alarm (
			id 					INTEGER PRIMARY KEY,

			id_query 			INTEGER,
			token_user_save		TEXT,
			id_user_save 		INTEGER
		)
	''')

	# Сохранить изменения
	conn.commit()



# СОЗДАЁТ НОВУЮ ЗАПИСЬ
@ensure_connection
def save_item_alarm(conn, id_query: int, token_user_save: str, id_user_save: int):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO alarm (
			id_query,
			token_user_save,
			id_user_save
			) VALUES (?, ?, ?)'''
			,(id_query, token_user_save, id_user_save))
	return 'OK'


# Узнаёт, сколько запросов с таким id сохранено
@ensure_connection
def test_alarm_item_saved(conn, id_query: int, token_user_save: str):
	cursor = conn.cursor()
	cursor.execute('SELECT COUNT(*) FROM alarm WHERE (id_query = ? and token_user_save = ?) LIMIT 1', (id_query, token_user_save))
	(data, ) = cursor.fetchone()
	return data

#=================================================================================================================










#======================================= STANDART QUEARY =======================================
# Получает указанное поле
@ensure_connection
def get_data(conn, table_name: str, line: str, line_selector: str, line_selector_value: str):
	'''
	table_name - название таблицы
	line - строка, которую нужно получить (например дату)
	line_selector - строка, по которой будем искать (например id)
	line_selector_value - значение, по которому будем искать
	'''
	cursor = conn.cursor()
	cursor.execute('SELECT {0} FROM {1} WHERE {2} = ?'.format(line, table_name, line_selector), (line_selector_value, ))

	data = cursor.fetchone()
	if (data != None):
		return data[0]
	else:
		return None


# Записывает информацию в указанное поле
@ensure_connection
def set_data(conn, table_name: str, line: str, line_selector: str, line_selector_value: str, data: str):
	cursor = conn.cursor()
	cursor.execute('UPDATE {0} SET {1} = {2} WHERE {3} = {4}'.format(table_name, line, data, line_selector, line_selector_value))
	conn.commit()
#===============================================================================================





@ensure_connection
def init_db(conn, force: bool = False):
	init_db_users(force = force)
	init_db_items(force = force)
	init_db_answers(force = force)
	init_db_look_leter(force = force)
	init_db_alarm(force = force)



if __name__ == '__main__':
	print('Соединение с базой')
	init_db_users(force = False)
	#print(set_user_page(user_id = 123, page = 'page_new_2'))
	#print(set_user_page(user_id = 1234, page = 'page_new_3'))

	#print(get_user_page(user_id = 1235))