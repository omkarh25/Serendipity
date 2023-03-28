from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Nifty", callback_data='nifty'),
         InlineKeyboardButton("BankNifty", callback_data='banknifty')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Select the index:', reply_markup=reply_markup)

def index_callback(update, context):
    query = update.callback_query
    query.answer()

    index = query.data
    context.user_data['index'] = index
    context.bot.send_message(chat_id=query.message.chat_id, text="Enter the strike price:")

def strike_callback(update, context):
    strike_price = update.message.text
    context.user_data['strike_price'] = strike_price

    keyboard = [
        [InlineKeyboardButton("Call", callback_data='call'),
         InlineKeyboardButton("Put", callback_data='put')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Select the option type:', reply_markup=reply_markup)


def option_callback(update, context):
    query = update.callback_query
    query.answer()

    option_type = query.data
    context.user_data['option_type'] = option_type

    keyboard = [
        [InlineKeyboardButton("Buy", callback_data='buy'),
         InlineKeyboardButton("Sell", callback_data='sell')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text="Select the trade type:", reply_markup=reply_markup)


def trade_callback(update, context):
    query = update.callback_query
    query.answer()

    trade_type = query.data
    context.user_data['trade_type'] = trade_type

    index = context.user_data['index']
    strike_price = context.user_data['strike_price']
    option_type = context.user_data['option_type']
    trade_type = context.user_data['trade_type']
    reply_text = f"You selected:\nIndex: {index}\nStrike Price: {strike_price}\nOption Type: {option_type}\nTrade Type: {trade_type}"
    context.bot.send_message(chat_id=query.message.chat_id, text=reply_text)


def main():
    updater = Updater('5994380365:AAFv0GSI78IxP6nI7g_xJPoqY3zWSfDHndQ', use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(index_callback, pattern='^(nifty|banknifty)$'))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^[0-9]+$'), strike_callback))
    updater.dispatcher.add_handler(CallbackQueryHandler(option_callback, pattern='^(call|put)$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(trade_callback, pattern='^(buy|sell)$'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
