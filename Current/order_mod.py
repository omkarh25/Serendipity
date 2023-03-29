# STATUS : Working
import configparser
import datetime
import json
import logging
import os
import sys
import time
import warnings
from pprint import pprint
import math
import pickle

import dateutil.parser
import requests
import telegram
from pya3 import *
from nt import close
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, OrderInfo, ReplyKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

################ Telegram Bot ################(Golden Ratio Bot)

##### Option Intra Bot #####
def telegram_bot_sendtext(bot_message):
    
    bot_token = '756533942:AAGfU0QEWZxUsGYHwSOBaRaOPZLjULVA7Kc'
    bot_chatID = '-1001481581102'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message


    response = requests.get(send_text)

    return response.json()


############ Reading Access Token #############
with open('acc_config_qty.json') as acc_config_file: 
    acc_json = json.load(acc_config_file) 


for i in range(len(acc_json)):
            alice_obj = Aliceblue(user_id = acc_json[i]['username'], api_key = acc_json[i]["api_key"])
            acc_json[i]["alice_obj"] = alice_obj
            session_id = acc_json[i]["alice_obj"].get_session_id()
            nfo_contract = alice_obj.get_contract_master("NFO")
            nse_contract = alice_obj.get_contract_master("NSE")

###################### Order Placement Functions - START ##################################
# CHECKLIST: Set below params and execute from here everyday

str_prc_default = 11500.0 # Don't forget to add .0 for Alice Blue NIFTY Symbols # .0 to be removed for monthly expiry

exp_yr = 2023
exp_mnth = 3     # for monthly series expiry, don't change to 0   
exp_date = 29       # Use single digit for dates before 10th of a month / monthly expiry use expiry date 

expiry = f"{exp_yr}-{exp_mnth}-{exp_date}"

base_symbol = 'NIFTY'
ce_syntx = 'CE'
pe_syntx = 'PE'

call_sym_alBlue = ''
put_sym_alBlue = ''
call_hed_sym = ''
put_hed_sym = ''
call_exp_sym = ''
put_exp_sym = ''
strPrc = ''
exePrc = ''

def setSymbols(strPrc):
    global call_sym_alBlue,put_sym_alBlue,call_hed_sym,put_hed_sym
    if float(strPrc) < 10000:
        str_prc_string = strPrc[:4] 
    else:
        str_prc_string = strPrc[:5]

    for i in range(len(acc_json)): 
        call_sym_alBlue = acc_json[i]["alice_obj"].get_instrument_for_fno(exch="NFO",symbol=base_symbol, expiry_date=expiry,
        is_fut=False, strike=float(strPrc), is_CE=True)
        put_sym_alBlue = acc_json[i]["alice_obj"].get_instrument_for_fno(exch="NFO",symbol=base_symbol, expiry_date=expiry, 
        is_fut=False, strike=float(strPrc), is_CE=False)
        call_hed_sym = acc_json[i]["alice_obj"].get_instrument_for_fno(exch="NFO",symbol=base_symbol, expiry_date=expiry, 
        is_fut=False, strike=float(strPrc)+600, is_CE=True)
        put_hed_sym = acc_json[i]["alice_obj"].get_instrument_for_fno(exch="NFO",symbol=base_symbol, expiry_date=expiry, 
        is_fut=False, strike=float(strPrc)-600, is_CE=False)

ordersNF_json = []
orderNF = {}
orderNo = 1
omsIDlist = []
hedgeEntry = ''
hedgeExit = ''
shortcoverexe = ''

nfOrderpath = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\NiftyOrders.txt"
GROrderpath = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\GROrders.txt"
tradeLogpath = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\tradeLog.txt"
goldenLogpath =  "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\goldenLog.txt"

# SECTION:: Alice Blue Orders(BNB)

def opIntra_NF_SELL(ordertype,strPrc,exePrc):
    global omsIDlist
    omsIDdict = {}
    
    for i in range(len(acc_json)):
        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=call_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=put_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)
        
        omsIDdict['acc_name'] = acc_json[i]["acc_name"]
        omsIDdict['order_id_CE'] = order_id_CE['NOrdNo']
        omsIDdict['order_id_PE'] = order_id_PE['NOrdNo']
        omsIDdict['ordertype'] = ordertype
        omsIDdict['strPrc'] = strPrc
        omsIDdict['alice_obj'] = acc_json[i]["alice_obj"]
        omsIDlist.append(omsIDdict.copy())

    get_order_details(omsIDlist)
    trade_log_details(omsIDlist,ordertype,strPrc,exePrc)
    # json_file_dump()


def opIntra_NF_BUY(ordertype,strPrc,exePrc):
    global omsIDlist
    omsIDdict = {}
    for i in range(len(acc_json)):
        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=call_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=put_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)
        
        omsIDdict['acc_name'] = acc_json[i]["acc_name"]
        omsIDdict['order_id_CE'] = order_id_CE['NOrdNo']
        omsIDdict['order_id_PE'] = order_id_PE['NOrdNo']
        omsIDdict['ordertype'] = ordertype
        omsIDdict['strPrc'] = strPrc
        omsIDdict['alice_obj'] = acc_json[i]["alice_obj"]
        omsIDlist.append(omsIDdict.copy())

    get_order_details(omsIDlist)
    if ordertype == 'long':
        trade_log_details(omsIDlist,ordertype,strPrc,exePrc)

def opIntra_NF_SARLong(ordertype,strPrc):
    global omsIDlist
    omsIDdict = {}
    for i in range(len(acc_json)):
        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=call_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=call_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=put_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=put_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)
        
        omsIDdict['acc_name'] = acc_json[i]["acc_name"]
        omsIDdict['order_id_CE'] = order_id_CE['NOrdNo']
        omsIDdict['order_id_PE'] = order_id_PE['NOrdNo']
        omsIDdict['ordertype'] = ordertype
        omsIDdict['strPrc'] = strPrc
        omsIDdict['alice_obj'] = acc_json[i]["alice_obj"]
        omsIDlist.append(omsIDdict.copy())

    get_order_details(omsIDlist)


def opIntra_NF_SARShort(ordertype,strPrc):
    global omsIDlist
    omsIDdict = {}
    for i in range(len(acc_json)):
        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=call_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=call_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=put_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=put_sym_alBlue,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)


        omsIDdict['acc_name'] = acc_json[i]["acc_name"]
        omsIDdict['order_id_CE'] = order_id_CE['NOrdNo']
        omsIDdict['order_id_PE'] = order_id_PE['NOrdNo']
        omsIDdict['ordertype'] = ordertype
        omsIDdict['strPrc'] = strPrc
        omsIDdict['alice_obj'] = acc_json[i]["alice_obj"]
        omsIDlist.append(omsIDdict.copy())

    get_order_details(omsIDlist)

def placeHedge(ordertype,strPrc):
    global omsIDlist
    omsIDdict = {}    

    for i in range(len(acc_json)):
        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=call_hed_sym,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=put_hed_sym,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)
        omsIDdict['acc_name'] = acc_json[i]["acc_name"]
        omsIDdict['order_id_CE'] = order_id_CE['NOrdNo']
        omsIDdict['order_id_PE'] = order_id_PE['NOrdNo']
        omsIDdict['ordertype'] = 'HedgeEntry'
        omsIDdict['strPrc'] = strPrc
        omsIDdict['alice_obj'] = acc_json[i]["alice_obj"]
        omsIDlist.append(omsIDdict.copy())
        
    get_order_details(omsIDlist)

def remHedge(ordertype,strPrc,exePrc):
    global omsIDlist
    omsIDdict = {}    

    for i in range(len(acc_json)):
        order_id_CE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=call_hed_sym,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        order_id_PE = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=put_hed_sym,
                                      quantity=int(acc_json[i]["qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        omsIDdict['acc_name'] = acc_json[i]["acc_name"]
        omsIDdict['order_id_CE'] = order_id_CE['NOrdNo']
        omsIDdict['order_id_PE'] = order_id_PE['NOrdNo']
        omsIDdict['ordertype'] = 'HedgeExit'
        omsIDdict['strPrc'] = strPrc
        omsIDdict['alice_obj'] = acc_json[i]["alice_obj"]
        omsIDlist.append(omsIDdict.copy())
        
    get_order_details(omsIDlist)
    trade_log_details(omsIDlist,'shortcover',strPrc,exePrc)


def cancelallorder(ordertype):    
    for i in range(len(acc_json)):
        acc_json[i]["alice_obj"].cancel_all_orders()

golden_symbol = 'BANKNIFTY'
golden_option_CE = ''
golden_option_PE = ''
golden_buy = ''
golden_sell = ''
goldenRatio_json = []
goldenlogNF = {}
goldenlist = []

def golden_long(spotPrc):
    global golden_option_CE,goldenlist,golden_buy
    goldendict = {}
    golden_buy_temp = int(math.ceil(float(spotPrc) / 100))*100
    golden_buy =  str(golden_buy_temp) + '.0'
    for i in range(len(acc_json)):
        golden_option_CE = acc_json[i]["alice_obj"].get_instrument_for_fno(symbol = golden_symbol, expiry_date= datetime.date(exp_yr, exp_mnth, exp_date), is_fut=False, strike=golden_buy, is_CE = True)

        order_id = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=golden_option_CE,
                                      quantity=int(acc_json[i]["golden_qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        goldendict['acc_name'] = acc_json[i]["acc_name"]
        goldendict['order_id'] = order_id['data']['oms_order_id']
        goldendict['ordertype'] = 'golden_long'
        goldendict['strPrc'] = golden_buy
        goldendict['alice_obj'] = acc_json[i]["alice_obj"]
        goldenlist.append(goldendict.copy())
    
    golden_order_details(goldenlist)
    gr_trade_log_details(goldenlist,spotPrc)

def golden_long_cover(spotPrc):
    global golden_option_CE,goldenlist,golden_buy
    goldendict = {}
    for i in range(len(acc_json)):        
        order_id = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=golden_option_CE,
                                      quantity=int(acc_json[i]["golden_qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        goldendict['acc_name'] = acc_json[i]["acc_name"]
        goldendict['order_id'] = order_id['data']['oms_order_id']
        goldendict['ordertype'] = 'golden_long_cover'
        goldendict['strPrc'] = golden_buy
        goldendict['alice_obj'] = acc_json[i]["alice_obj"]
        goldenlist.append(goldendict.copy())
    
    golden_order_details(goldenlist)
    gr_trade_log_details(goldenlist,spotPrc)

def golden_short(spotPrc):
    global golden_option_PE,goldenlist,golden_sell
    goldendict = {}
    golden_sell_temp = int(math.ceil(float(spotPrc) / 100))*100
    golden_sell =  str(golden_sell_temp) + '.0'
    for i in range(len(acc_json)):
        golden_option_PE = acc_json[i]["alice_obj"].get_instrument_for_fno(symbol = golden_symbol, expiry_date= datetime.date(exp_yr, exp_mnth, exp_date), is_fut=False, strike=golden_sell, is_CE = False)

        order_id = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Buy,
                                      instrument=golden_option_PE,
                                      quantity=int(acc_json[i]["golden_qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)
        
        goldendict['acc_name'] = acc_json[i]["acc_name"]
        goldendict['order_id'] = order_id['data']['oms_order_id']
        goldendict['ordertype'] = 'golden_short'
        goldendict['strPrc'] = golden_sell
        goldendict['alice_obj'] = acc_json[i]["alice_obj"]
        goldenlist.append(goldendict.copy())
    
    golden_order_details(goldenlist)
    gr_trade_log_details(goldenlist,spotPrc)

def golden_short_cover(spotPrc):
    global golden_option_PE,goldenlist,golden_sell
    goldendict = {}
    for i in range(len(acc_json)):        
        order_id = acc_json[i]["alice_obj"].place_order(transaction_type=TransactionType.Sell,
                                      instrument=golden_option_PE,
                                      quantity=int(acc_json[i]["golden_qty"]),
                                      order_type=OrderType.Market,
                                      product_type=ProductType.Intraday,
                                      price=0.0,
                                      trigger_price=None,
                                      stop_loss=None,
                                      square_off=None,
                                      trailing_sl=None,
                                      is_amo=False)

        goldendict['acc_name'] = acc_json[i]["acc_name"]
        goldendict['order_id'] = order_id['data']['oms_order_id']
        goldendict['ordertype'] = 'golden_short_cover'
        goldendict['strPrc'] = golden_sell
        goldendict['alice_obj'] = acc_json[i]["alice_obj"]
        goldenlist.append(goldendict.copy())
    
    golden_order_details(goldenlist)
    gr_trade_log_details(goldenlist,spotPrc)


########################################## Logging Functions  #################################

def get_order_details(omsIDlist):
    global ordersNF_json, orderNF, orderNo, acc_json,hedgeEntry,hedgeExit,shortcoverexe
    # sleep / order status check else telegram message    
    for i in range(len(omsIDlist)):
        orderNF['acc_name'] = omsIDlist[i]['acc_name']
        orderNF['order_type'] = omsIDlist[i]['ordertype']
        orderNF['order_no'] = orderNo
        orderNF['strPrc'] = omsIDlist[i]['strPrc']
        orderNF['order_id_CE'] = omsIDlist[i]['order_id_CE']
        if orderNF['acc_name'] == "BY":
            alice = acc_json[0]["alice_obj"]
        elif orderNF['acc_name'] == "HV":
            alice = acc_json[1]["alice_obj"]
        order_details_CE = alice.get_order_history(orderNF['order_id_CE'])
        # dateandtime = order_details_CE['OrderedTime'].split(' ')
        orderNF['timestamp'] = order_details_CE['OrderedTime']
        orderNF['CE_prc'] = order_details_CE['Avgprc']
        orderNF['qty'] = order_details_CE['Qty']
        # if order_details_CE['reporttype'] != 'fill' : 
        #     telegram_bot_sendtext('Account: '+orderNF['acc_name']+','+ 'Error: '+order_details_CE['reporttype']) 

        orderNF['order_id_PE'] = omsIDlist[i]['order_id_PE']  
        order_details_PE = alice.get_order_history(orderNF['order_id_PE'])
        orderNF['PE_prc'] = order_details_PE['Avgprc']
        orderNF['exe_prc'] = float(orderNF['CE_prc'])+ float(orderNF['PE_prc'])
        # if order_details_PE['reporttype'] != 'fill' : 
        #     telegram_bot_sendtext('Account: '+orderNF['acc_name']+','+ 'Error: '+order_details_PE['reporttype'])    
        
        if orderNF['acc_name'] == 'BY' and orderNF['order_type'] == 'HedgeEntry':
            hedgeEntry = orderNF['exe_prc']
        elif orderNF['acc_name'] == 'BY' and orderNF['order_type'] == 'HedgeExit':
            hedgeExit = orderNF['exe_prc']
        if orderNF['acc_name'] == 'BY' and orderNF['order_type'] == 'shortcover':
            shortcoverexe = orderNF['exe_prc']

        ordersNF_list = []
        ordersNF_list.append(orderNF.copy())
        for i in ordersNF_list:
            if i not in ordersNF_json:
                ordersNF_json.append(i)

def golden_order_details(goldenlist):
    global goldenRatio_json,goldenlogNF,acc_json
    for i in range(len(goldenlist)):
        goldenlogNF['acc_name'] = goldenlist[i]['acc_name']
        goldenlogNF['order_type'] = goldenlist[i]['ordertype']
        goldenlogNF['strPrc'] = goldenlist[i]['strPrc']
        goldenlogNF['order_id'] = goldenlist[i]['order_id']   
        order_details = alice_obj.get_order_history(goldenlogNF['order_id'])
        goldenlogNF['timestamp'] = order_details['data'][0]['exchange_time']
        goldenlogNF['prc'] = order_details['data'][0]['average_price']
        goldenlogNF['qty'] = order_details['data'][0]['quantity']
        if order_details['data'][0]['order_status'] != 'complete' : 
            telegram_bot_sendtext('Account: '+goldenlogNF['acc_name']+','+ 'Error: '+order_details['data'][0]['order_status']) 

        goldenOrder_list = []
        goldenOrder_list.append(goldenlogNF.copy())
        for i in goldenOrder_list:
            if i not in goldenRatio_json:
                goldenRatio_json.append(i)

tradeLog_json = []
tradelogNF = {}

def trade_log_details(omsIDlist,ordertype,strPrc,exePrc):
    global tradeLog_json, tradelogNF,hedgeEntry,hedgeExit,shortcoverexe
    tradelogNF['order_type'] = ordertype

    if float(strPrc) < 10000:
        str_prc_string = strPrc[:4] 
    else:
        str_prc_string = strPrc[:5]
    tradelogNF['strPrc'] = float(str_prc_string)

    tradelogNF['order_id_CE'] = omsIDlist[0]['order_id_CE']   
    order_details_CE = alice_obj.get_order_history(orderNF['order_id_CE'])
    # dateandtime = order_details_CE['OrderedTime'].split(' ')
    tradelogNF['timestamp'] = order_details_CE['OrderedTime']
    tradelogNF['exePrc'] = exePrc
    if tradelogNF['order_type'] == "short":
        tradelogNF['hedgeEntryPrc']= hedgeEntry
    elif tradelogNF['order_type'] == "shortcover":
        tradelogNF['exePrc']= exePrc
        tradelogNF['hedgeExitPrc']= hedgeExit
    if tradelogNF['order_type'] == "long":
        tradelogNF['hedgeEntryPrc']= 0.00
    if tradelogNF['order_type'] == "longcover":
        tradelogNF['hedgeExitPrc']= 0.00

    tradeLog_list = []
    tradeLog_list.append(tradelogNF.copy())
    for i in tradeLog_list:
        if i not in tradeLog_json:
            tradeLog_json.append(i)

goldenLog_json = []
grlogNF = {}

def gr_trade_log_details(goldenlist,spotPrc):
    global goldenLog_json,grlogNF
    grlogNF['order_type'] = goldenlist[0]['ordertype']
    grlogNF['order_id'] = goldenlist[0]['order_id']   
    order_details = alice_obj.get_order_history(grlogNF['order_id'])
    grlogNF['timestamp'] = order_details['data'][0]['exchange_time']
    grlogNF['spotPrc'] = float(spotPrc)

    goldenLog_list = []
    goldenLog_list.append(grlogNF.copy())
    for i in goldenLog_list:
        if i not in goldenLog_json:
            goldenLog_json.append(i)

def json_file_dump():
    global ordersNF_json,nfOrderpath, omsIDlist, orderNo
    
    jsonData = json.dumps(ordersNF_json, indent=2)    
    
    with open(nfOrderpath ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    lstOrder =  jsonData # assign last order
    omsIDlist.clear()
    ordersNF_json.clear()
    orderNo = orderNo+1 

def golden_file_dump():
    global goldenRatio_json,GROrderpath,goldenlist
    jsonData = json.dumps(goldenRatio_json, indent = 2)

    with open(GROrderpath, 'a') as f :
        f.write(jsonData)
        f.write("\n")
        f.close()
    
    goldenlist.clear()
    goldenRatio_json.clear()

def masterLog_dump():
    global tradeLog_json,tradeLogpath
    jsonData = json.dumps(tradeLog_json, indent = 2)
    with open(tradeLogpath, 'a') as f :
        f.write(jsonData)
        f.write("\n")
        f.close()

    tradelogNF.clear()
    tradeLog_json.clear()

def goldenLog_dump():
    global goldenLog_json,goldenLogpath
    jsonData = json.dumps(goldenLog_json, indent = 2)
    with open(goldenLogpath, 'a') as f :
        f.write(jsonData)
        f.write("\n")
        f.close()

    grlogNF.clear()
    goldenLog_json.clear()


########################################## Telegram Support Functions  #################################


def sellorder(update, context):
    global strPrc,exePrc
    opIntra_NF_SELL('sell',strPrc,exePrc)

def buyorder(update, context):
    global strPrc,exePrc
    opIntra_NF_BUY('buy',strPrc,exePrc)

def allAccHedge(update, context):
    global strPrc
    placeHedge('allAccH',strPrc)

def sellallAccHedge(update, context):
    global strPrc
    remHedge('sellallAccH',strPrc,exePrc)

def cancelorders(update, context):
    cancelallorder('cancelorder')

# def main():
#     updater = Updater('807232387:AAF5OgaGJuUPV8xwDUxYFRHaOWJSU5pIAic',use_context=True)
#     updater.dispatcher.add_handler(CommandHandler('help',help))
#     updater.dispatcher.add_handler(CommandHandler('buyorder',buyorder))
#     updater.dispatcher.add_handler(CommandHandler('sellorder',sellorder))
#     updater.start_polling()
#     updater.idle()

# main()
