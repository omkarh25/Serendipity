from pya3 import *
import json
import math

session = []
usernames = []
jsonList = []
bal = []
qty = []
acc_name = []
aliceobj = []

####### sessionID ##########
with open('acc_config.json') as acc_config_file: 
    acc_json = json.load(acc_config_file)


def sessionID():
  global session,usernames,jsonList,aliceobj
  for i in range(len(acc_json)):
    alice_obj = Aliceblue(user_id=acc_json[i]["username"], api_key = acc_json[i]["api_key"])
    usernames.append(acc_json[i]["username"])
    acc_name.append(acc_json[i]["acc_name"])
    acc_json[i]["alice_obj"] = alice_obj
    aliceobj.append(alice_obj)
    session_id = acc_json[i]["alice_obj"].get_session_id()
    session.append(session_id["sessionID"])
    
sessionID()

####### autoQTY ##########

bnf_qty_ratio = 0.75
nf_qty_ratio = 1
nf_lot_size = 50
bnf_lot_size = 25
draw_multiplier = 0.75
up_multiplier = 1.33

def draw_multi_func(curr_cap,opening_bal):
  draw_ratio = (curr_cap - opening_bal)/curr_cap
  if(draw_ratio < 0.75):
    return True
  else:
    return False

def up_multi_func(curr_cap,opening_bal):
  up_ratio = (opening_bal-curr_cap)/opening_bal
  if(up_ratio > 1.33):
    return True
  else:
    return False

def accDetails():
    global bal,qty
    for i in range(len(acc_json)):
      summary = acc_json[i]["alice_obj"].get_balance()
      openingBal = summary[0]['cashmarginavailable']
      acc_json[i]['open_bal'] = float(openingBal)
      acc_json[i]['qty'] = math.floor(float(openingBal)/70000)*nf_lot_size      
      bal.append(openingBal)
      quantity = acc_json[i]['qty']
      qty.append(quantity)
      acc_json[i].pop('alice_obj')

accDetails()

for i in range(0,len(usernames)):
        jsonList.append({"acc_name":acc_name[i], "username":usernames[i], "session_id":session[i], "openingBal": bal[i],"qty":qty[i],"api_key":acc_json[i]["api_key"]})


with open('acc_config_qty.json', 'w') as outfile:
  # json_dumper = json.dumps(acc_json, indent=4)
  json.dump(jsonList, outfile)

