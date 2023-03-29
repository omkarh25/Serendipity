import requests
import json
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import base64
import pyotp
from pya3 import *
import math



# import two.filepath as filepath
from babel.numbers import format_currency
import telegram
import calendar
from datetime import date, timedelta

class CryptoJsAES:
	@staticmethod
	def __pad(data):
		BLOCK_SIZE = 16
		length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
		return data + (chr(length) * length).encode()

	@staticmethod
	def __unpad(data):
		return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

	def __bytes_to_key(data, salt, output=48):
		assert len(salt) == 8, len(salt)
		data += salt
		key = hashlib.md5(data).digest()
		final_key = key
		while len(final_key) < output:
			key = hashlib.md5(key + data).digest()
			final_key += key
		return final_key[:output]

	@staticmethod
	def encrypt(message, passphrase):
		salt = Random.new().read(8)
		key_iv = CryptoJsAES.__bytes_to_key(passphrase, salt, 32 + 16)
		key = key_iv[:32]
		iv = key_iv[32:]
		aes = AES.new(key, AES.MODE_CBC, iv)
		return base64.b64encode(b"Salted__" + salt + aes.encrypt(CryptoJsAES.__pad(message)))

	@staticmethod
	def decrypt(encrypted, passphrase):
		encrypted = base64.b64decode(encrypted)
		assert encrypted[0:8] == b"Salted__"
		salt = encrypted[8:16]
		key_iv = CryptoJsAES.__bytes_to_key(passphrase, salt, 32 + 16)
		key = key_iv[:32]
		iv = key_iv[32:]
		aes = AES.new(key, AES.MODE_CBC, iv)
		return CryptoJsAES.__unpad(aes.decrypt(encrypted[16:]))

BASE_URL="https://ant.aliceblueonline.com/rest/AliceBlueAPIService"

with open("acc_config.json", "r") as read_file:
	acc_json = json.load(read_file)

for i in range(len(acc_json)):
	totp = pyotp.TOTP(acc_json[i]["totp_access"])

	def getEncryptionKey():
		url = BASE_URL+"/customer/getEncryptionKey"
		payload = json.dumps({"userId": acc_json[i]["username"]})
		headers = {'Content-Type': 'application/json'}
		response = requests.post( url, headers=headers, data=payload)
		return response.json()['encKey']

	getEncryptionKey = getEncryptionKey()
	checksum = CryptoJsAES.encrypt(acc_json[i]["password"].encode(), getEncryptionKey.encode()).decode('UTF-8')

	def weblogin():
		url = BASE_URL+"/customer/webLogin"
		payload = json.dumps({"userId": acc_json[i]["username"],
                          "userData": checksum})                    
		headers = {'Content-Type': 'application/json'}
		response = requests.post( url, headers=headers, data=payload)
		return response.json()

	weblogin = weblogin()
	sCount = weblogin['sCount']
	sIndex = weblogin['sIndex']

	def twoFa(sCount, sIndex):
		url = BASE_URL+"/sso/2fa"
		payload = json.dumps({"answer1": acc_json[i]["twoFA"],
                    "userId": acc_json[i]["username"],
                    "sCount": sCount,
                    "sIndex": sIndex})
		headers = {'Content-Type': 'application/json'}
		response = requests.post( url, headers=headers, data=payload)
		return response.json()

	twof = twoFa(sCount, sIndex)

	def verifyTotp(twofa):
		if twofa["loPreference"] == "TOTP" and twofa["totpAvailable"]:
			url = BASE_URL+"/sso/verifyTotp"

			payload = json.dumps({"tOtp": totp.now(),
                      "userId": acc_json[i]["username"] })
			headers = {
            	'Authorization': 'Bearer '+acc_json[i]["username"]+' '+twofa['us'],
            	'Content-Type': 'application/json'}
			response = requests.request("POST", url, headers=headers, data=payload,verify=True)
		else:
			print("Try Again")
		if response.json()["userSessionID"]:
			print("Login Successfully")
		else:
			print("User is not enable TOTP! Please enable TOTP through mobile or web")

	verifyTotp(twof) 

acc_names = []
session = []
usernames = []
json_list = []
qty = []
acc_name = []
alice_obj = []
bal = []

def sessionID():
    global session, usernames, acc_name, alice_obj
    for i in range(len(acc_json)):
        alice = Aliceblue(user_id=acc_json[i]["username"], api_key=acc_json[i]["api_key"])
        usernames.append(acc_json[i]["username"])
        acc_name.append(acc_json[i]["acc_name"])
        session.append(alice.get_session_id()["sessionID"])
        alice_obj.append(alice)

sessionID()

def accDetails():
    global bal, qty
    nf_lot_size = 50
    for i in range(len(acc_json)):
        summary = alice_obj[i].get_balance()
        openingBal = ((summary[0]['cashmarginavailable']))
        bal.append(openingBal)
        qty.append(math.floor(float(bal[i])/70000)*nf_lot_size)

accDetails()

for i in range(len(usernames)):
    json_list.append({
        "acc_name": acc_name[i], 
        "username": usernames[i], 
        "session_id": session[i], 
        "openingBal": bal[i],
        "qty": qty[i],
        "api_key": acc_json[i]["api_key"],
        "totp_access": acc_json[i]["totp_access"],
    })

with open("acc_config_qty.json", 'w') as outfile:
    json.dump(json_list, outfile,indent=4)
