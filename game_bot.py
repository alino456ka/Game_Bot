import telebot as tb
from telebot import types
import random as rm

token = '5997697981:AAF-_Nq-69GRJ9tszdmHQr5U8tbbyzTufqk'
bot = tb.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
  global hm_point
  global ai_point
  hm_point = 0 
  ai_point = 0
  name = message.from_user.first_name
  bot.send_message(message.chat.id, f' Привет, {name}!')


@bot.message_handler(commands=['game'])
def game(message):
  global hm_point
  global ai_point
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  button1 = types.KeyboardButton('Камень')
  button2 = types.KeyboardButton('Ножницы')
  button3 = types.KeyboardButton('Бумага')
  markup.add(button1)
  markup.add(button2)
  markup.add(button3)
  bot.send_message(message.chat.id, 'Сделайте свой ход', reply_markup=markup)
  bot.register_next_step_handler(message, game_run)

def game_run(message):
  global hm_point
  global ai_point
  km_list = ['Камень', 'Ножницы', 'Бумага']
  ai = rm.choice(km_list)
  if (ai == 'Камень' and message.text == 'Бумага') or (ai == 'Ножницы' and message.text == 'Камень') or (ai == 'Бумага' and message.text == 'Ножницы'):
    hm_point += 1
    bot.send_message(message.chat.id, f'Мои очки {ai_point}, твои {hm_point}')
    bot.send_message(message.chat.id, f'Я выбрал {ai}')
    bot.send_message(message.chat.id, 'Ура! Победа!')
  elif (ai == 'Камень' and message.text == 'Ножницы') or (ai == 'Ножницы' and message.text == 'Бумага') or (ai == 'Бумага' and message.text == 'Камень'):
    ai_point += 1
    bot.send_message(message.chat.id, f'Мои очки {ai_point}, твои {hm_point}')
    bot.send_message(message.chat.id, f'Я выбрал {ai}')
    bot.send_message(message.chat.id, 'Вы проиграли!')
  elif ai == message.text:
    ai_point += 1
    hm_point += 1
    bot.send_message(message.chat.id, f'Мои очки {ai_point}, твои {hm_point}')
    bot.send_message(message.chat.id, f'Я выбрал {ai}')
    bot.send_message(message.chat.id, 'Ничья!')
  bot.send_message(message.chat.id, 'Сыграем ещё?')
  bot.register_next_step_handler(message, repeat)

def repeat(message):
  global hm_point
  global ai_point
  if message.text == 'Да':
    game(message)
  elif message.text == 'Нет':
    if ai_point > hm_point:
      bot.send_message(message.chat.id, f'В этой тяжелой схватке победу одержал компьютер со счетом {ai_point}! Ваш счет: {hm_point}')
    elif ai_point < hm_point:
      bot.send_message(message.chat.id, f'В этой тяжелой схватке победу одержали вы со счетом {hm_point}! Счет компьютера: {ai_point}')
    elif ai_point == hm_point:
      bot.send_message(message.chat.id, f'Тяжелая схватка закончилась ничьей! Общий счет: {ai_point}')
    ai_point = 0
    hm_point = 0

bot.polling(none_stop=True)

#   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#   button_yes = types.KeyboardButton('Да')
#   button_no = types.KeyboardButton('Нет')
#   markup.add(button_yes)
#   markup.add(button_no)