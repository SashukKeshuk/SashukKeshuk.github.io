from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, web_app_info
from config import API
from db import get_lines, get_saved, get_by_id, save
import asyncio

import os

#message.text

webApp = web_app_info.WebAppInfo(url="https://sashukkeshuk.github.io")

b1 = KeyboardButton('Изменить фильтры', web_app=webApp)

markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup.add(b1)

markup1 = InlineKeyboardMarkup()

b2 = InlineKeyboardButton('Далее', callback_data='next')
bb2 = InlineKeyboardButton('Подробное описание', callback_data='detail')
bbb2 = InlineKeyboardButton('Мне интересно', callback_data='interested')
bbbb2 = InlineKeyboardButton('Назад', callback_data='back')
save_btn = InlineKeyboardButton('Сохранить❤', callback_data='save')

markup1.add(b2).insert(bbbb2).add(bb2).insert(bbb2).add(save_btn)

markup2 = InlineKeyboardMarkup()
b3 = InlineKeyboardButton('Изменить фильтры', web_app=webApp)
b4 = InlineKeyboardButton('Искать заново', callback_data='again')
markup2.add(b3).insert(b4)

markup3 = InlineKeyboardMarkup()
markup3.add(b2).insert(bbbb2).add(bbb2)

markup4 = InlineKeyboardMarkup()
markup4.add(b3)

next_saved = InlineKeyboardButton('Далее', callback_data='next_saved')
previous_saved = InlineKeyboardButton('Назад', callback_data='previous_saved')

markup5 = InlineKeyboardMarkup()
markup5.add(previous_saved).insert(next_saved).add(b4).add(bb2).add(bbb2)

bot = Bot(token=API)
dp = Dispatcher(bot)

lines = []
chat_id = 0
channel_id = -1001802975422

n = 0
i = 0
j1 = 0
s1 = ""

async def on_startup(_):
	print('bot online')


@dp.message_handler(content_types=['web_app_data'])
async def get(msg: types.Message):
	global chat_id
	print(msg.web_app_data.data)
	data = msg.web_app_data.data
	if (data == "show"):
		global s1
		global j1
		j1 = 0
		s2 = get_saved(chat_id)
		for sx in s2:
			print(str(sx['article_id'][1]) + '|\n')
			s1 += str(sx['article_id'][1])
			s1 += ' '
		await send_saved(msg.from_user.id)
	else:
		a = []
		a = data.split(' ')
		j = 0
		HouseT = 0
		if (a[0] == 'new_building'):
			HouseT = 0
		else:
			HouseT = 1
		cost1 = int(a[1])
		cost2 = int(a[2])
		cities_get = ""
		f = 0
		for j in range(0, len(a)-1):
			if (a[j][0].isupper()):
				if (f == 0):
					cities_get = a[j]
					f = 1
				else:
					cities_get += ' '
					cities_get += a[j]

		f = 0
		for j in range(0, len(a)-1):
			if (a[j][0].isupper()):
				f = 1
			elif (f == 1):
				break

		Types = []
		for word in a:
			if (word == 'apartment'):
				Types.append(0)
			if (word == 'villa'):
				Types.append(1)
			if (word == 'townhouse'):
				Types.append(2)

		rooms_get = ""
		for j in range(0, len(a)-1):
			if (a[j][0].isnumeric() and j > 2):
				rooms_get = str(a[j])
				rooms_get += ' '

		rooms = rooms_get.split(' ')
		cities = cities_get.split(' ')
		print('houseT = ' + str(HouseT) + ' cost1 = ' + str(cost1) + ' cost2 = ' + str(cost2) + ' cities = ' + cities_get + ' rooms = ' + str(rooms_get))
		print('Types: ')
		for t in Types:
			print(str(t) + ' ')
		global lines
		lines.clear()
		for room in rooms:
			for city in cities:
				for Type in Types:
					q = f"SELECT * FROM `articles` WHERE (cost>={cost1} AND cost<={cost2} AND type={Type} AND house_type={HouseT} AND rooms='{room}' AND city='{city}');"
					print('#'*20)
					print(q)
					print('#'*20)
					q_get = get_lines(q)
					print(q_get)
					lines += q_get
		global n
		n = len(lines)
		print('*'*20+str(n))
		i = 0
		if (n == 0):
			await send_msg(0, msg.from_user.id)
		else:
			await send_msg(1, msg.from_user.id)



@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
	global chat_id
	global i
	i = 0
	chat_id = message.from_user.id
	print(chat_id)
	await bot.send_message(message.from_user.id, '''Дубай сегодня - это одна из самых быстрорастущих экономик мира, инновационные проекты, доступность и легкость ведение бизнеса задают темп современного общества предпринимателей. Высокодоходные инвестиции, высокий уровень зарплат, возможность получения международного образования детям, привлекают людей со всего мира приобретать недвижимость в ОАЭ.''', parse_mode='html')

	await bot.send_message(message.from_user.id, '''Осталось подобрать жильё!
На ваш выбор различные апартаменты, таунхаусы, роскошные виллы, напрямую от застройщиков. Ваш запрос мы напрямую отправляем в офис продаж топ менеджеру, который поможет в кратчайшие сроки забронировать для вас недвижимость!''', parse_mode='html', reply_markup=markup)
	#call()


async def send_saved(cid):
	global s1
	arr = s1.split(' ')
	global chat_id
	global j1
	operator = Bot(API)
	if (j1 == len(arr)):
		await operator.send_message(cid, 'это ваша последняя сохраненная статья!', parse_mode='html', reply_markup=markup4)
	else:
		p = get_by_id(arr[j1])
		print('\n\n' + str(p[0]['text']) + '\n\n')
		await operator.send_photo(cid, photo=open(f"img/{arr[j1]}.png", "rb"))
		await operator.send_message(cid, p[0]['text'], parse_mode='html', reply_markup=markup5)

@dp.callback_query_handler(text='next_saved')
async def send_next_saved(msg: types.Message):
	global chat_id
	global j1
	j1 += 1
	arr = s1.split(' ')
	for xx in arr:
		if (xx == ''):
			arr.remove(xx)
	print('*'*20 + str(j1))
	if (j1 >= len(arr)):
		await bot.send_message(msg.from_user.id, 'это последняя сохраненная статья!', parse_mode='html')
		j1 -= 1
	else:
		print(str(j1) + '       ' + str(len(arr)))
		p = get_by_id(arr[j1])
		await bot.send_photo(msg.from_user.id, photo=open(f"img/{arr[j1]}.png", "rb"))
		await bot.send_message(msg.from_user.id, p[0]['text'], parse_mode='html', reply_markup=markup5)


@dp.callback_query_handler(text='previous_saved')
async def send_previous_saved(msg: types.Message):
	global chat_id
	global j1
	j1 -= 1
	arr = s1.split(' ')
	for xx in arr:
		if (xx == ''):
			arr.remove(xx)
	if (j1 == -1):
		await bot.send_message(msg.from_user.id, 'это первая сохраненная статья!', parse_mode='html')
		j1 += 1
	else:
		p = get_by_id(arr[j1])
		await bot.send_photo(msg.from_user.id, photo=open(f"img/{arr[j1]}.png", "rb"))
		await bot.send_message(msg.from_user.id, p[0]['text'], parse_mode='html', reply_markup=markup5)
		j1 -= 1


async def send_msg(ok, cid):
	operator = Bot(API)
	print("called")
	global lines
	global i
	global chat_id
	if (ok == 0):
		await operator.send_message(cid, 'По данным фильтрам ничего найти не получилось', parse_mode='html')
		i = 0
	else:
		await operator.send_photo(cid, photo=open(f"img/{lines[i]['id']}.png", "rb"))
		await operator.send_message(cid, lines[i]['text'], parse_mode='html', reply_markup=markup1)

@dp.callback_query_handler(text='save')
async def save_article(msg : types.Message):
	global chat_id
	saved_art1 = get_saved(chat_id)
	saved_art = ""
	for art in saved_art1:
		print(str(art['article_id'][1]))
		saved_art += str(art['article_id'][1])
		saved_art += ' '
	lid = lines[i]['id']
	if (len(saved_art) == 0):
		f2 = 0
	else:
		arr = saved_art.split(' ')
		f2 = 0
		for art in arr:
			if (int(art) == lid):
				f2 = 1
				await bot.send_message(msg.from_user.id, 'статья уже сохранена', parse_mode='html')
				break

	if (f2 == 0):
		saved_art += ' '
		saved_art += str(lid)
		save(chat_id, saved_art)

@dp.callback_query_handler(text='next')
async def next(message: types.Message):
	global chat_id
	global i
	i += 1
	if (i == n):
		await bot.send_message(message.from_user.id, "вы просмотрели все варианты по данному запросу", parse_mode='html', reply_markup=markup)
		i = 0
	else:
		await send_msg(1, message.from_user.id)

@dp.callback_query_handler(text='detail')
async def send_detail(message: types.Message):
	global chat_id
	global i
	await bot.send_photo(message.from_user.id, photo=open(f"img/{lines[i]['id']}.png", "rb"))
	await bot.send_message(chat_id, lines[i]['text2'], parse_mode='html', reply_markup=markup3)

@dp.callback_query_handler(text='interested')
async def interested(msg: types.Message):
	global chat_id
	global channel_id
	global i
	await bot.send_message(msg.from_user.id, "мы позже свяжемся с вами!", parse_mode='html', reply_markup=markup)
	await bot.send_message(channel_id, f"{msg.from_user.first_name} {msg.from_user.last_name} (@{msg.from_user.username}) заинтересован во {lines[i]['id']}ом доме")

@dp.callback_query_handler(text='back')
async def again(msg: types.Message):
	global i
	global chat_id
	i -= 1
	if (i == -1):
		await bot.send_message(msg.from_user.id, "Это была первая квартира которую вы просмотрели 👆", parse_mode='html')
		i = 0
	else:
		await send_msg(1, msg.from_user.id)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
