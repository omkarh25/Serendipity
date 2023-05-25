from telethon import TelegramClient, events
import re
from pya3 import *
import datetime

alice = Aliceblue(user_id='KH364',api_key='ejuSHTAmjA5SQvIRRdjx2rjQN6U0V7j80Ljp64L5tnsMN7PnQ1S5PGrebVo9peb13WLUtblSTbBmexCTFVHKgLu81UE3yrrsvKbkX4AQGbOpd08MPepMq4cMbCiOzKip')
alice_session = alice.get_session_id()


LTP = 0
socket_opened = False
subscribe_flag = False
subscribe_list = []
unsubscribe_list = []

def socket_open():  # Socket open callback function
    print("Connected")
    global socket_opened
    socket_opened = True
    if subscribe_flag:  # This is used to resubscribe the script when reconnect the socket.
        alice.subscribe(subscribe_list)

def socket_close():  # On Socket close this callback function will trigger
    global socket_opened, LTP
    socket_opened = False
    LTP = 0
    print("Closed")

def socket_error(message):  # Socket Error Message will receive in this callback function
    global LTP
    LTP = 0
    print("Error :", message)

def feed_data(message):  # Socket feed data will receive in this callback function
    global LTP, subscribe_flag
    feed_message = json.loads(message)
    if feed_message["t"] == "ck":
        print("Connection Acknowledgement status :%s (Websocket Connected)" % feed_message["s"])
        subscribe_flag = True
        print("subscribe_flag :", subscribe_flag)
        print("-------------------------------------------------------------------------------")
        pass
    elif feed_message["t"] == "tk":
        print("Token Acknowledgement status :%s " % feed_message)
        print("-------------------------------------------------------------------------------")
        pass
    else:
        print("Feed :", feed_message)
        LTP = feed_message[
            'lp'] if 'lp' in feed_message else LTP  # If LTP in the response it will store in LTP variable
        
        if 'lp' in feed_message:
            LTP = feed_message['lp']
            print('Latest LTP:', LTP)

# Socket Connection Request
alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                      socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True,market_depth=False)

while not socket_opened:
    pass

subscribe_list = [alice.get_instrument_by_symbol('INDICES','NIFTY 50'),alice.get_instrument_by_symbol('INDICES','NIFTY BANK')]
df = alice.subscribe(subscribe_list)
sleep(5)
alice.stop_websocket()


exp_yr = 2023
bnf_exp_mnth = 5     # for monthly series expiry, don't change to 0
bnf_exp_date = 25       # Use single digit for dates before 10th of a month / monthly expiry use expiry date
fnf_exp_mnth = 5
fnf_exp_date = 25

order_id = None

if datetime.datetime.today().weekday() == 4:
    nse_contract = alice.get_contract_master("NSE")
    nfo_contract = alice.get_contract_master("NFO")


api_id = '22353756'
api_hash = '351041b3c3951a0a116652896d55d9a2'
receiver_phone_number = '+918197137007' #Amol

def place_order(base_symbol,strike_prc,option_type):

    bnf_nf_expiry = f"{exp_yr}-{bnf_exp_mnth}-{bnf_exp_date}"
    fnf_expiry = f"{exp_yr}-{fnf_exp_mnth}-{fnf_exp_date}"

    if option_type == 'CE':
        option = True
    elif option_type == 'PE':
        option = False

    if base_symbol == 'NIFTY' or 'BANKNIFTY':
        order_symbol = alice.get_instrument_for_fno(exch="NFO",symbol=base_symbol, expiry_date=bnf_nf_expiry, is_fut=False, strike=int(strike_prc), is_CE=option)
    elif base_symbol == 'FINNIFTY':
        order_symbol = alice.get_instrument_for_fno(exch="NFO",symbol=base_symbol, expiry_date=fnf_expiry, is_fut=False, strike=int(strike_prc), is_CE=option)
    print("base symbol: ", base_symbol)
    print("expiry: ", bnf_nf_expiry)
    print("strike: ", strike_prc)
    print("option: ", option)

    order_id = alice.place_order(transaction_type = TransactionType.Buy,
                     instrument = order_symbol,
                     quantity = 20,
                     order_type = OrderType.Market,
                     product_type = ProductType.Intraday,
                     price = 0.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
    print(order_id)

client = TelegramClient(receiver_phone_number, api_id, api_hash)

@client.on(events.NewMessage(chats='https://t.me/+ibsPEy3QDxwyOGE1'))  #amol's group
# @client.on(events.NewMessage(chats='https://t.me/+cZixK-7oaCljZTE9')) #Siri Group
async def my_event_handler(event):
    global order_id
    message_text = event.message.text
    split_message = message_text.split()

    keywords = ['nifty', 'banknifty', 'finnifty']
    base_symbol = ', '.join([kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', message_text, flags=re.IGNORECASE)])
    strike_price = re.search(r'\d{5}', message_text)
    option_type = re.search(r'\b(ce|pe)\b', message_text, flags=re.IGNORECASE)

    if base_symbol and strike_price and option_type:
        base_symbol = base_symbol.upper()
        strike_price = strike_price.group()
        option_type = option_type.group().upper()
        
    place_order(base_symbol, strike_price, option_type)

    print("Base Symbol: ", base_symbol)
    print("Strike Price: ", strike_price)
    print("Option Type: ", option_type)
    await client.send_message(entity=902575766, message=f"{order_id}")


with client:
    print("Waiting for Orders...")
    client.run_until_disconnected()

