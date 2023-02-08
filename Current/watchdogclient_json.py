import json
import logging
import sys
import time

import telegram
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, OrderInfo, ReplyKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import order_mod

previous_order = ""
strPrc = ''
exePrc = ''

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        lastOrder()

def lastOrder():
    global previous_order,strPrc,exePrc
    jsondata = [json.loads(line) for line in open("C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\signalsNF.json", 'r')]
    lastorder = ((jsondata)[-1])
    ordertype = ([value for value in lastorder.values()][0])
    strPrc = ([value for value in lastorder.values()][1])  
    if ordertype == 'goldenlong' or ordertype =='goldenlongcover' or ordertype =='goldenshort' or ordertype =='goldenshortcover':
        exePrc = 0
    else :
        exePrc = round(float([value for value in lastorder.values()][2]),2)  
    order_mod.setSymbols(strPrc)      
    print("ordertype : "+str(ordertype))
    

    if ordertype != previous_order:
        previous_order = ordertype
        if ordertype == "short":
            order_mod.placeHedge('HedgeEntry',strPrc)
            order_mod.opIntra_NF_SELL(ordertype,strPrc,exePrc)
            order_mod.json_file_dump()
            order_mod.masterLog_dump()
        elif ordertype == "shortcover":
            order_mod.opIntra_NF_BUY(ordertype,strPrc,exePrc)
            order_mod.remHedge("HedgeExit",strPrc,exePrc)
            order_mod.json_file_dump()  
            order_mod.masterLog_dump()      
        elif ordertype == "long":
            order_mod.opIntra_NF_BUY(ordertype,strPrc,exePrc)
            order_mod.json_file_dump()
            order_mod.masterLog_dump()
        elif ordertype == "longcover":
            order_mod.opIntra_NF_SELL(ordertype,strPrc,exePrc)
            order_mod.json_file_dump()
            order_mod.masterLog_dump()
        elif ordertype == "sarshort":
            order_mod.opIntra_NF_SELL("longcover",strPrc,exePrc)
            order_mod.json_file_dump()
            order_mod.masterLog_dump()

            order_mod.placeHedge('HedgeEntry',strPrc)
            order_mod.opIntra_NF_SELL("short",strPrc,exePrc)
            order_mod.json_file_dump()
            order_mod.masterLog_dump()
            #order_mod.opIntra_NF_SARShort(ordertype,strPrc)
        elif ordertype == "sarlong":
            order_mod.opIntra_NF_BUY("shortcover",strPrc,exePrc)
            order_mod.remHedge("HedgeExit",strPrc,exePrc)
            order_mod.json_file_dump()
            order_mod.masterLog_dump()

            order_mod.opIntra_NF_BUY("long",strPrc,exePrc)
            order_mod.json_file_dump()
            order_mod.masterLog_dump()
            #order_mod.opIntra_NF_SARLong(ordertype,strPrc)
            
        elif ordertype == "buy":
            order_mod.opIntra_NF_BUY(ordertype,strPrc,exePrc)
            order_mod.json_file_dump()
        elif ordertype == "sell":
            order_mod.opIntra_NF_SELL(ordertype,strPrc,exePrc)
            order_mod.json_file_dump()

        elif ordertype == 'goldenlong':
            order_mod.golden_long(strPrc)   # Spot price to be converted to strPrc
            order_mod.golden_file_dump()
            order_mod.goldenLog_dump()
        elif ordertype == 'goldenlongcover':
            order_mod.golden_long_cover(strPrc)
            order_mod.golden_file_dump()
            order_mod.goldenLog_dump()
        elif ordertype == 'goldenshort':
            order_mod.golden_short(strPrc)
            order_mod.golden_file_dump()
            order_mod.goldenLog_dump()
        elif ordertype == 'goldenshortcover':
            order_mod.golden_short_cover(strPrc)
            order_mod.golden_file_dump()
            order_mod.goldenLog_dump()
        else:
            print('Error: Could not read order file!')
    else:
        print("Duplicate Order")

def start(update,context):
    update.message.reply_text('Hi')

def help(update, context):
    update.message.reply_text('/buyorder \n/sellorder \n/selectStrPrc \n/allAccHedge \n/sellallAccHedge\n/cancelorders')

def selectStrPrc(update, context):
    update.message.reply_text(chat_id=update.message.reply_text(text='Select the Strike Price'))

def strPrcinfo(update, context):
    strPrc = update.message.text
    order_mod.setSymbols(strPrc)
    order_mod.hedgeStrPrc(strPrc)
    # order_mod.expiryCEstr(strPrc)    
    # order_mod.expiryPEstr(strPrc)    
    # answer = f'You have selected:{strPrc}'
    # update.message.reply_text(chat_id=update.message.reply_text(strPrc(answer)))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def sellorder(update, context):    
    order_mod.opIntra_NF_SELL('sell',strPrc,exePrc)

def buyorder(update, context):    
    order_mod.opIntra_NF_BUY('buy',strPrc,exePrc)

def allAccHedge(update, context):    
    order_mod.placeHedge('allAccH',strPrc)

def sellallAccHedge(update, context):    
    order_mod.remHedge('sellallAccH',strPrc,exePrc)

# def expiryCEHegde(update, context):
#     order_mod.expirytradeCE('expiryCE')

# def expiryPEHegde(update, context):
#     order_mod.expirytradePE('expiryPE')

def cancelorders(update, context):
    order_mod.cancelallorder('cancelorder')

# def main():
if __name__ == "__main__":
    # updater = Updater('1181910093:AAEZxu2JjdI93zn9cBUGbZQa9DJs6xt7HeQ',use_context=True)  #GoldenRatio Bot
    updater = Updater('807232387:AAF5OgaGJuUPV8xwDUxYFRHaOWJSU5pIAic',use_context=True)     #Algo Train Bot
    updater.dispatcher.add_handler(CommandHandler('start',start))
    updater.dispatcher.add_handler(CommandHandler('help',help))
    updater.dispatcher.add_handler(CommandHandler('buyorder',order_mod.buyorder))
    updater.dispatcher.add_handler(CommandHandler('sellorder',order_mod.sellorder))
    updater.dispatcher.add_handler(CommandHandler('allAccHedge',order_mod.allAccHedge))
    updater.dispatcher.add_handler(CommandHandler('sellallAccHedge',order_mod.sellallAccHedge))
    # updater.dispatcher.add_handler(CommandHandler('expiryCEHedge',order_mod.expiryCEHegde))
    # updater.dispatcher.add_handler(CommandHandler('expiryPEHedge',order_mod.expiryPEHegde))
    updater.dispatcher.add_handler(CommandHandler('cancelorders',order_mod.cancelorders))
    updater.dispatcher.add_handler(CommandHandler('setStrPrc', selectStrPrc))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, strPrcinfo))
    path = 'C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\'
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    updater.start_polling()
    observer.start()    
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    updater.idle()

# main()

print("Ready to take orders!")