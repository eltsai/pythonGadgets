#!/usr/bin/env python3

from telegram.ext import Updater
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import logging

token_content = ''

with open("token","r") as file:
    token_content = str(file.read())
    #print(token_content)

updater = Updater(token=token_content, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="beep boop. I'm a bot. I archive snippets for my human.")

def echo2c(update, context):
    '''echo to channel'''
    context.bot.send_message(chat_id='@ElisaArchive', 
                             text=' '.join(context.args))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = CommandHandler('echo2c', echo2c)
dispatcher.add_handler(echo_handler)

updater.start_polling()