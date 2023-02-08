import json
from json import JSONEncoder

import numpy as np

import AmiPy

orderpathNF = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\signalsNF.json"

def short(strikePrc,shortPrice):
    signalJSONData = {  "tradeType": "short",  "strikePrc": str(strikePrc),"shortPrice": str(shortPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc

def shortcover(strikePrc,coverPrice):
    signalJSONData = {  "tradeType": "shortcover",  "strikePrc": str(strikePrc),"coverPrice": str(coverPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc

def long(strikePrc,buyPrice):
    signalJSONData = {  "tradeType": "long",  "strikePrc": str(strikePrc),"buyPrice": str(buyPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc

def longcover(strikePrc,sellPrice):
    signalJSONData = {  "tradeType": "longcover",  "strikePrc": str(strikePrc),"sellPrice": str(sellPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc

def sarshort(strikePrc,sellPrice):
    signalJSONData = {  "tradeType": "sarshort",  "strikePrc": str(strikePrc),"sellPrice": str(sellPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc
    
def sarlong(strikePrc,coverPrice):
    signalJSONData = {  "tradeType": "sarlong",  "strikePrc": str(strikePrc),"buyPrice": str(coverPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc
    
def manualbuy(strikePrc,buyPrice):
    signalJSONData = {  "tradeType": "buy",  "strikePrc": str(strikePrc),"buyPrice": str(buyPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc

def manualsell(strikePrc,shortPrice):
    signalJSONData = {  "tradeType": "sell",  "strikePrc": str(strikePrc),"shortPrice": str(shortPrice)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return strikePrc  

def goldenlong(futPrc):
    signalJSONData = {  "tradeType": "goldenlong",  "spot": str(futPrc)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return futPrc

def goldenlongcover(futPrc):
    signalJSONData = {  "tradeType": "goldenlongcover",  "spot": str(futPrc)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return futPrc
    
def goldenshort(futPrc):
    signalJSONData = {  "tradeType": "goldenshort",  "spot": str(futPrc)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return futPrc
    
def goldenshortcover(futPrc):
    signalJSONData = {  "tradeType": "goldenshortcover",  "spot": str(futPrc)}
    jsonData = json.dumps(signalJSONData)
    with open(orderpathNF ,'a') as f:
        f.write(jsonData)
        f.write("\n")
        f.close()
    return futPrc
