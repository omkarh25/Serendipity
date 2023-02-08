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

# with open('V2/acc_config.json') as acc_config_file:
#     acc_json = json.load(acc_config_file)

bal = []
acc_names = []
session = []

def sessionID():
    global acc_names,bal,session
    for i in range(len(acc_json)):
        alice_obj = Aliceblue(user_id = acc_json[i]['username'], api_key= acc_json[i]['api_key'])
        acc_json[i]["alice_obj"] = alice_obj
        session_id = acc_json[i]["alice_obj"].get_session_id()
        session.append(session_id["sessionID"])
        acc_name = acc_json[i]["acc_name"]
        summary = acc_json[i]["alice_obj"].get_balance() 
        openingBal = summary[0]['cashmarginavailable']
        bal.append(openingBal)
        acc_names.append(acc_name)

sessionID()

########## creating Dicts ##########

balance = {acc_names[i]+'openingBal': bal[i] for i in range(len(acc_names))}

closing_bal = {}
closingBalDict = {}
balpath = "DailyBalSum.txt"
f = open(balpath)

for line in f:
    splitLine = line.split(":")
    closingBalDict[splitLine[0].strip()] = splitLine[1].strip()

prevOpenBal =  {k: v for k, v in closingBalDict.items() if k.endswith('openingBal')}
prev_val = list(prevOpenBal.values())
todayCloseBal = {acc_names[i]+'closingBal':prev_val[i] for i in range(len(acc_names))}

closing_bal = {k: v for k, v in closingBalDict.items() if k.endswith('closingBal')}

PnL = []

for i in range(len(balance)):
    netPnL = format_currency((float(list(balance.values())[i]) - float(list(todayCloseBal.values())[i])),'INR', locale='en_IN')
    PnL.append(netPnL)

####### Date #######

today = date.today()
calendar.day_name[today.weekday()]
yesterday = today - timedelta(days = 1)
yes_dayname = calendar.day_name[yesterday.weekday()]

if yes_dayname == 'Sunday':
    yesterday = (today - timedelta(days = 3))
else:
    yesterday = (today - timedelta(days = 1))   # change for holidays

month = str(yesterday.strftime("%b"))
day = str(yesterday.strftime("%d"))
year = str(yesterday.strftime("%y"))

date = (day +' '+ month +' '+ year)

###### Calcualtion ######

old_bal = {}
for i in range(len(acc_json)):
    old_bal[acc_json[i]["acc_name"]] = format_currency(list(todayCloseBal.values())[i], 'INR', locale='en_IN')

new_bal = {}
for i in range(len(acc_json)):
    new_bal[acc_json[i]["acc_name"]] = format_currency(list(balance.values())[i], 'INR', locale='en_IN')

####### Telegram messages ########

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

acc_list = [telegram_bot_sendtext_KH,telegram_bot_sendtext_BY,telegram_bot_sendtext_HV]

for i in range(len(acc_list)):
    msg = acc_list[i]("**Daily Summary** " + date +'\n'+'\n'+'Acc Open Value : ' + list(old_bal.values())[i] +'\n'+'Net PnL : ' + str(PnL[i]) +'\n'+ 'Current Acc Val :'+ list(new_bal.values())[i])


######### Writing to File #######
def Merge(balance, todayCloseBal):
    return(todayCloseBal.update(balance))

print(Merge(balance,todayCloseBal))

def file_write():
    f = open(balpath,"w+")
    for k in todayCloseBal.keys():
        f.write("{}:{}\n".format(k,todayCloseBal[k]))
    
    f.close()

file_write()


# import json

with open('acc_config_qty.json', 'r', encoding='utf-8') as f:
    my_list = json.load(f)

for idx, obj in enumerate(my_list):
        if obj['acc_name'] == "KH":
            my_list.pop(idx)

with open('acc_config_qty.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(my_list))

