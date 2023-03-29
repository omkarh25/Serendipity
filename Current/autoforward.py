from telethon.sync import TelegramClient
from telethon import events

api_id = '22353756'
api_hash = '351041b3c3951a0a116652896d55d9a2'
phone_number = '+919902106162'  # your phone number
# username = 'Amol Kittur'
client = TelegramClient(phone_number, api_id, api_hash)
client.start()

@client.on(events.NewMessage(from_users='+918147039490'))
async def handle_message(event):
    message_text = event.message.text
    print(message_text)
    await client.send_message(entity=902575766, message=f"You received a message from the number +1234567890: {message_text}")

client.start()
client.run_until_disconnected()




# api_id = '28308447'
# api_hash = '63b0228d40d21350751400088775536a'
# phone_number = '+918197137007'  # your phone number
# username = 'Amol Kittur'