from botToken import token

import UserClass
import pickle


import telebot
from telebot import types
from typing import Any, Callable, List, Optional, Union
REPLY_MARKUP_TYPES = Union[
    types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, 
    types.ReplyKeyboardRemove, types.ForceReply]



bot = telebot.TeleBot(token)
last_bot_messages = {}
authorized_users = UserClass.Users()
try:
    authorized_users = pickle.load(open('data.users','rb'))
except :
    print("out of users")

def bot_msg(message,chat_id: Union[int, str], text: str, 
            disable_web_page_preview: Optional[bool]=None, 
            reply_to_message_id: Optional[int]=None, 
            reply_markup: Optional[REPLY_MARKUP_TYPES]=None,
            parse_mode: Optional[str]=None, 
            disable_notification: Optional[bool]=None, 
            timeout: Optional[int]=None,
            entities: Optional[List[types.MessageEntity]]=None,
            allow_sending_without_reply: Optional[bool]=None):
    
    bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_web_page_preview=disable_web_page_preview,
        reply_to_message_id=reply_to_message_id,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
        disable_notification=disable_notification,
        timeout=timeout,
        entities=entities,
        allow_sending_without_reply=allow_sending_without_reply)
    global last_bot_messages
    if message.from_user.id in last_bot_messages:
        last_bot_messages[message.from_user.id] = text
    else:   
        last_bot_messages.update({message.from_user.id:text})

@bot.message_handler(commands=['start'])
def start_command(message):
    start(message)

@bot.message_handler(content_types=['text'])
def messege_analizer(message):
    bot.delete_message(message.chat.id,message.message_id)
    if message.text == "Log in":
        log_in(message)
    elif message.text == "Sign up":
        Sign_up(message)
    else:
        sign_in_check(message)

def sign_in_check(message):
    global authorized_users
    if  "Yes my pass would:" in message.text: 
        authorized_users.add_user("common",str(message.text).split(':',1)[1],message.from_user.id)
        pickle.dump(authorized_users,open('data.users','wb+'))
        bot.send_message(message.chat.id,"Now you may log in")
    elif message.text == "Change":
        Sign_up(message)
    elif message.text == "Exit":
        start(message)
    elif (message.from_user.id in last_bot_messages and 
    last_bot_messages[message.from_user.id] == "Please, сhoose your password"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Sure_button = types.KeyboardButton("Yes my pass would:{0}".format(message.text))
        Change_button = types.KeyboardButton("Change")
        Exit_button = types.KeyboardButton("Exit")
        markup.add(Sure_button,Change_button,Exit_button)
        bot_msg(message,message.chat.id,"Please, сhoose your password",reply_markup=markup)
        bot.delete_message(message.chat.id,message.message_id-1)
    else:
        log_in_check(message)

def log_in_check(message):
    if (last_bot_messages[message.from_user.id] == "Please, enter your password"
    and authorized_users.get_user(message.from_user.id).check_pass(message.text)):
        bot.send_message(message.chat.id,"Correct pass!\nYour are welcome")
    else:
        bot.send_message(message.chat.id,"invalid input")

def log_in(message):
    if authorized_users.check(message.from_user.id):
        bot_msg(message,message.chat.id,"Please, enter your password",reply_markup=types.ReplyKeyboardRemove())
    else:
        bot_msg(message,message.chat.id,"Sorry,you should be signed in",reply_markup=types.ReplyKeyboardRemove())
        start(message)

def Sign_up(message):
    bot_msg(message,message.chat.id,"Please, сhoose your password",reply_markup=types.ReplyKeyboardRemove())

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Login_button = types.KeyboardButton("Log in")
    SignUp_button = types.KeyboardButton("Sign up")
    markup.add(Login_button,SignUp_button)

    bot.send_message(message.chat.id,
    "Hello ,{0.first_name}!\n I'am {1.first_name}.".format(message.from_user,bot.get_me()),parse_mode='html',
    reply_markup=markup)


bot.polling(none_stop=True)
