import requests
import json
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import base64
import pyotp

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

userId = "KH364"
password = "K@nnada222"
twofa = 1990
totp_encrypt_key="FRKWJNNSORKSHQMIDMVBKKEFDKMPJGNM"
totp = pyotp.TOTP(totp_encrypt_key)

AB = "HTPUNQQVIOBDJAPSMRYSRHTEYDWGAZWA"
BY1424 = "JCOLSSUDFUCTMVKBLNZMCIBTUQSZLNEZ"  #Totp key
KH364 = "FRKWJNNSORKSHQMIDMVBKKEFDKMPJGNM"
HV = "SXHHDMKDCNPQUQPQMJQETIDJKUUYGFAZ"

def getEncryptionKey():

    url = BASE_URL+"/customer/getEncryptionKey"
    payload = json.dumps({
    "userId": userId
        })
    headers = {
    'Content-Type': 'application/json'
        }
    response = requests.post( url, headers=headers, data=payload)
    return response.json()['encKey']

getEncryptionKey = getEncryptionKey()
checksum = CryptoJsAES.encrypt(password.encode(), getEncryptionKey.encode()).decode('UTF-8')

def weblogin():
    url = BASE_URL+"/customer/webLogin"
    payload = json.dumps({
                        "userId": userId,
                        "userData": checksum
                        })
    headers = {
            'Content-Type': 'application/json'
            }
    response = requests.post( url, headers=headers, data=payload)
    return response.json()

weblogin = weblogin()
sCount = weblogin['sCount']
sIndex = weblogin['sIndex']

def twoFa(sCount, sIndex):
    url = BASE_URL+"/sso/2fa"
    payload = json.dumps({
                    "answer1": twofa,
                    "userId": userId,
                    "sCount": sCount,
                    "sIndex": sIndex
                    })
    headers = {
                'Content-Type': 'application/json'
                }
    response = requests.post( url, headers=headers, data=payload)
    return response.json()

twof = twoFa(sCount, sIndex)

def verifyTotp(twofa):
    if twofa["loPreference"] == "TOTP" and twofa["totpAvailable"]:
        url = BASE_URL+"/sso/verifyTotp"

        payload = json.dumps({
            "tOtp": totp.now(),
            "userId": userId
        })

        headers = {
            'Authorization': 'Bearer '+userId+' '+twofa['us'],
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload,verify=True)
    else:
        print("Try Again")

    if response.json()["userSessionID"]:
        print("Login Successfully")
    else:
        print("User is not enable TOTP! Please enable TOTP through mobile or web")

verifyTotp(twof)


# from pya3 import *
# alice = Aliceblue(user_id='AB068818',api_key='CBomUKElkhSmqOOIxSxeSMy49fANnfHmb5O85jkx9yTn6HhsPLlNBILrqqRQsrbaLTzK0MMFUHqOOOo2Ec5GllsLA3jdhkqHsjiEm0NqGFv7uRArn7r2gY5523Ur7M0y')
# print(alice.get_session_id()) # Get Session ID
