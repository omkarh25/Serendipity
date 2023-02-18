import requests
import json

balpath = "DailyBalSum.txt"
acc_config = "/Users/amolkittur/Documents/Trading/Serendipity/two/acc_config.json"

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