import telebot as tb
from telebot import types
import random as rm

token = '5997697981:AAF-_Nq-69GRJ9tszdmHQr5U8tbbyzTufqk'
bot = tb.TeleBot(token)

hm_point = 0
ai_point = 0
km_list = ['Камень', 'Ножницы', 'Бумага']

def keyboard():
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
  button2 = types.InlineKeyboardButton(text='Нет', callback_data='no')
  markup.row(button1, button2)
  return markup


@bot.message_handler(commands=['start'])
def start(message):
  global hm_point
  global ai_point
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  button1 = types.KeyboardButton('Играть!')
  markup.add(button1)
  name = message.from_user.first_name
  bot.send_message(message.chat.id, f' Привет, {name}!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def answer(message):
  if message.text == 'Играть!':
    game(message)
    
def game(message):
  global hm_point
  global ai_point
  markup = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(text='Камень', callback_data='rock')
  button2 = types.InlineKeyboardButton(text='Ножницы', callback_data='scissors')
  button3 = types.InlineKeyboardButton(text='Бумага', callback_data='paper')
  markup.row(button1, button2, button3)
  bot.send_message(message.chat.id, 'Сделайте свой ход', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query_process(callback_query):
  global ai_point
  global hm_point
  if callback_query.data == 'rock':
    ai = rm.choice(km_list)
    if ai == 'Ножницы':
      hm_point += 1
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Ура! Победа!')
    elif ai == 'Бумага':
      ai_point += 1
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Вы проиграли!')
    elif ai == 'Камень':
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Ничья!')
    bot.send_message(callback_query.message.chat.id, 'Сыграем ещё?', reply_markup=keyboard())
  elif callback_query.data == 'scissors':
    ai = rm.choice(km_list)
    if ai == 'Бумага':
      hm_point += 1
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Ура! Победа!')
    elif ai == 'Камень':
      ai_point += 1
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Вы проиграли!')
    elif ai == 'Ножницы':
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Ничья!')
    bot.send_message(callback_query.message.chat.id, 'Сыграем ещё?', reply_markup=keyboard())
  elif callback_query.data == 'paper':
    ai = rm.choice(km_list)
    if ai == 'Камень':
      hm_point += 1
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Ура! Победа!')
    elif ai == 'Ножницы':
      ai_point += 1
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Вы проиграли!')
    elif ai == 'Бумага':
      bot.send_message(callback_query.message.chat.id, f'Я выбрал {ai}')
      bot.send_message(callback_query.message.chat.id, 'Ничья!')
    bot.send_message(callback_query.message.chat.id, 'Сыграем ещё?', reply_markup=keyboard())
  
  if callback_query.data == 'yes':
    bot.answer_callback_query(callback_query.id)
    game(callback_query.message)
  if callback_query.data == 'no':
    bot.answer_callback_query(callback_query.id)
    if ai_point > hm_point:
      bot.send_message(callback_query.message.chat.id, f'В этой тяжелой схватке победу одержал компьютер со счетом {ai_point}! Ваш счет: {hm_point}')
    elif ai_point < hm_point:
      bot.send_message(callback_query.message.chat.id, f'В этой тяжелой схватке победу одержали вы со счетом {hm_point}! Счет компьютера: {ai_point}')
    elif ai_point == hm_point:
      bot.send_message(callback_query.message.chat.id, f'Тяжелая схватка закончилась ничьей! Общий счет: {ai_point}')
    ai_point = 0
    hm_point = 0


bot.polling(none_stop=True)
