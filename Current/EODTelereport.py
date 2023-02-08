from pya3 import *
import json
from datetime import date, timedelta
from collections import defaultdict
from babel.numbers import format_currency
import telegram
import calendar
import requests

########## sessionID ##########
with open('acc_config_qty.json') as acc_config_file: 
    acc_json = json.load(acc_config_file) 


bal = []
acc_names = []
session = []

def accPnl():
    global acc_names,bal,session
    for i in range(len(acc_json)):
        alice_obj = Aliceblue(user_id = acc_json[i]['username'], api_key= acc_json[i]['api_key'])
        acc_json[i]["alice_obj"] = alice_obj
        session_id = acc_json[i]["alice_obj"].get_session_id()
        session.append(session_id["sessionID"])
        acc_name = acc_json[i]["acc_name"]
        summary = acc_json[i]["alice_obj"].get_daywise_positions()
        for i in range(len(summary)):
            PnL = summary[i]['MtoM']
            print(PnL)
            bal.append(PnL)
            acc_names.append(acc_name)

accPnl()
########## extracting PnL ##########

# bal = []
# acc_names = []

print(acc_names)


PnL_list = defaultdict(list)
for key, value in zip(acc_names, bal):
    PnL_list[key].append(value)
PnL_dict = dict(PnL_list)
print(PnL_dict)
########## Telegram Bots ##########

def telegram_bot_sendtext_KH(bot_message):    
    bot_token = '1181910093:AAEZxu2JjdI93zn9cBUGbZQa9DJs6xt7HeQ'
    bot_chatID_KH = '-1001483256385'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_KH + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def telegram_bot_sendtext_BY(bot_message):    
    bot_token = '1181910093:AAEZxu2JjdI93zn9cBUGbZQa9DJs6xt7HeQ'
    bot_chatID_BY = '-1001494618225'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_BY + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def telegram_bot_sendtext_VH(bot_message):    
    bot_token = '1181910093:AAEZxu2JjdI93zn9cBUGbZQa9DJs6xt7HeQ'
    bot_chatID_VH = '-1001409873506'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_VH + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def telegram_bot_sendtext_HV(bot_message):    
    bot_token = '1181910093:AAEZxu2JjdI93zn9cBUGbZQa9DJs6xt7HeQ'
    bot_chatID_HV = '-1001324332104'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_HV + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def telegram_bot_sendtext_AK(bot_message):    
    bot_token = '1181910093:AAEZxu2JjdI93zn9cBUGbZQa9DJs6xt7HeQ'
    bot_chatID_AK = '-1001441818778'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_AK + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

########## Date format ##########

today = date.today()
calendar.day_name[today.weekday()]
month = str(today.strftime("%b"))
day = str(today.strftime("%d"))
year = str(today.strftime("%y"))
date = (day + month + year)

########## send message and write to file ##########
# telegram_bot_sendtext_KH
acc_list = [telegram_bot_sendtext_BY,telegram_bot_sendtext_HV]
total = []
f = open('eodSum.txt',"w+")
for i in range(len(acc_json)):
    acc_name = acc_json[i]["acc_name"]
    print(acc_name)
    eod = sum([int(float(i.replace(',',''))) for i in PnL_dict[acc_name]])
    PnL = format_currency(eod, 'INR', locale='en_IN')
    total.append(PnL)
    f.write(acc_name+"PnL:" + str(eod) + '\n')

f.close()

for i in range(len(acc_list)):
    msg = acc_list[i]("**EOD Report** " + date +'\n'+'\n'+'PnL : ' + total[i])
    

