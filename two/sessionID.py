import json
import math
from pya3 import Aliceblue
import two.filepath as filepath

session = []
usernames = []
json_list = []
open_bal = []
qty = []
acc_name = []
alice_obj = []

# Load account configurations
with open(filepath.acc_config) as acc_config_file:
    acc_json = json.load(acc_config_file)

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
    global open_bal, qty
    bnf_qty_ratio = 0.75
    nf_qty_ratio = 1
    nf_lot_size = 50
    bnf_lot_size = 25
    draw_multiplier = 0.75
    up_multiplier = 1.33

    for i in range(len(acc_json)):
        summary = alice_obj[i].get_balance()
        open_bal.append(float(summary[0]['cashmarginavailable']))
        qty.append(math.floor(float(open_bal[i])/70000)*nf_lot_size)

accDetails()

for i in range(len(usernames)):
    json_list.append({
        "acc_name": acc_name[i], 
        "username": usernames[i], 
        "session_id": session[i], 
        "openingBal": open_bal[i],
        "qty": qty[i],
        "api_key": acc_json[i]["api_key"]
    })

with open(filepath.acc_config, 'w') as outfile:
    json.dump(json_list, outfile,indent=4)
