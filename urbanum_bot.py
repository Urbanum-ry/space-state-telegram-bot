import os
import time
import sched
import json
import telebot

s = sched.scheduler(time.time,time.sleep)

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

previous_state = ' '
message_id = ' '

#@bot.message_handler()
@bot.channel_post_handler()
def check_state(sc):
    global previous_state
    global message_id
    with open('/home/urbanum/state.json') as json_file:
        current_state = json.load(json_file)
        if current_state != previous_state:
            previous_state = current_state
            try:
                bot.delete_message(-1001857650406, message_id)
            except:
                pass
            if current_state['state'] == 'on':
                message_id = bot.send_message(-1001857650406, 'Urbanum is open!').message_id
            else:
                message_id = bot.send_message(-1001857650406, 'Urbanum is closed :(').message_id
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
