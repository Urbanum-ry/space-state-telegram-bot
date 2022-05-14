import os
import time
import sched
import json
import telebot

s = sched.scheduler(time.time,time.sleep)

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

previous_state = ' '

@bot.message_handler()
def check_state(sc):
    global previous_state
    with open('/var/www/html/state.json') as json_file:
        current_state = json.load(json_file)
        if current_state != previous_state:
            previous_state = current_state
            if current_state['state'] == 'on':
                bot.send_message(-764942799, 'Urbanum is open!')
            else:
                bot.send_message(-764942799, 'Urbanum is closed :(')
    s.enter(5, 1, check_state, (sc,))

#@bot.message_handler(commands=['Urbanum'])
#def state_request(message):
#    with open('/var/www/html/state.json') as json_file:
#        data = json.load(json_file)
#        if data['state'] == 'on':
#            bot.send_message(message.chat.id, 'Urbanum is open!')
#        else:
#            bot.send_message(message.chat.id, 'Urbanum is closed :(')
#bot.polling()

s.enter(5, 1, check_state, (s,))
s.run()
