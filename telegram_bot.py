'''
telegram bot
команды:
/start, /help
readme - регистрация пользователя:  readme <имя>
print - характеристики пользователей
time - текущее дата время
plan - смотреть план  на день от текущего:  plan <0/пусто-сегодня, 1-завтра...>
plan_add - добавить пункт плана: plan_add  < 0/пусто-сегодня, 1-завтра...> на новых строках: <ЧЧ:ММ - тема>
kvartira_min - минимальная цена квартиры
kvartira_max - максимальная цена квартиры
'''

import telebot
import pprint
from bot_handler import BotHandler
from plans import Plans
import datetime
from cost_apartment import CostApartment

def get_param( s ):
	lst = s.split(' ')[1:]
	text = ' '.join(lst)
	return text

def is_registration( bot : telebot.TeleBot, message : telebot.types.Message):
	text = message.text
	id_user = message.chat.id

	bot_handler.is_user( id_user )

	user = bot_handler.get_name_user(id_user)
	if user == '?':
		bot.reply_to( message, "Я с Вами не знаком. Представьтесь, пожалуста!\n(команда: /readme ВашеИмя)" )
		return False
	else:
		return True

plans = Plans()
bot_handler = BotHandler()

TOKEN = '2092869156:AAHxWOdhnufE8dB1a46fnQVnmbnSMHVoMDc'   # занятия

# экземпляр класса Telebot
bot = telebot.TeleBot( TOKEN, parse_mode=None )

# обработчики сообщений ( фильтр )
@bot.message_handler(commands=['start','help'])
def send_welcome( message ):
	bot.reply_to(message, "Вы находитесь в боте занятий по Python!")
	if is_registration( bot, message ):
		id_user = message.chat.id
		user = bot_handler.get_name_user(id_user)
		bot.reply_to( message, f'Приветствую,{user}!' )

@bot.message_handler(commands=['print'])
def user_print( message ):
	if is_registration(bot, message):
		bot.reply_to( message, str( bot_handler ) )

	bot_handler.calc_chat( message.chat.id )

@bot.message_handler(commands=['time'])
def my_time( message ):
	today = datetime.datetime.today()
	d1 = today.strftime("%d-%m-%Y")  # 2017-04-05-00.18.00
	d2 = today.strftime("%H:%M:%S")
	bot.reply_to( message, f'Сегодня: {d1}, время: {d2}' )
	bot_handler.calc_chat(message.chat.id)

@bot.message_handler(commands=['plan'])
def my_plan( message ):
	par = message.text.split(' ')
	if len( par ) > 1:
		lst = message.text.split(' ')[1:]
		text = ' '.join(lst)
	else:
		text = '0'
	s = plans.get_works_day( int(text) )
	bot.reply_to(message, s)
	bot_handler.calc_chat(message.chat.id)

@bot.message_handler(commands=['plan_add'])
def plan_add( message ):
	if is_registration( bot, message ):
		text = get_param(message.text)
		lst = text.split('\n')
		d = int( lst[0] )
		lst = lst[1:]
		plans.set_works_day( d, lst )
		bot_handler.calc_chat(message.chat.id)


@bot.message_handler( commands=['readme'] )
def my_read( message ):
	text = get_param( message.text )

	if not bot_handler.is_user( message.chat.id ):
		bot_handler.set_name_user( message.chat.id, text)
		bot_handler.calc_chat( message.chat.id )

		today = datetime.datetime.today()
		d = today.strftime("%d-%m-%Y %H:%M:%S")  # 2017-04-05-00.18.00
		bot_handler.set_beg_time( message.chat.id, d )

		bot.reply_to( message, f"Я Вас запомнил! Приветствую,{text}!")

	else:
		bot.reply_to(message, f"Да я Вас помню! Вы уже регистрировались,{text}!")
	bot_handler.calc_chat(message.chat.id)

@bot.message_handler( commands=['kvartira_min'] )
def cost_appart_min( message ):
	ca = CostApartment()
	sMin = ca.cost_min()
	bot.reply_to( message, sMin )
	bot_handler.calc_chat(message.chat.id)

@bot.message_handler( commands=['kvartira_max'] )
def cost_appart_max( message ):
	ca = CostApartment()
	sMax = ca.cost_max()
	bot.reply_to( message, sMax )
	bot_handler.calc_chat(message.chat.id)

@bot.message_handler( content_types=['text'] )
def my_text( message ):
	#print('content_types1',bot_handler)
	i = 1
	if is_registration( bot, message ):
		text = message.text
		id_user = message.chat.id
		user = bot_handler.get_name_user(id_user)

		bot.reply_to(message, f"Приветствую,{user}! Вы сказали:\'{text}\', а я повторил!")

		bot_handler.calc_chat(message.chat.id)
	#print('text',bot_handler)
	i = 1

bot.polling()


