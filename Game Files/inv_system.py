import sys
import towns
import json
from items import *

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

inventory = {'quest': [], 'consum': [s_potion, s_elixr], 'coord': [],
             'weapons': [], 'armor': [], 'misc': []}
equipped = {'weapon': '', 'head': '(None)', 'body': '(None)', 'legs': '(None)'}

gs_stock = [[s_potion, m_potion, l_potion],
            [s_elixr, m_elixr, l_elixr],
            ['\n       ', '\n       ', '\n       '],
            [cpr_swd, bnz_spr, irn_axe],
            [oak_stf, arc_spb, rnc_stf],
            ['\n       ', '\n       ', '\n       '],
            [bnz_hlm, irn_hlm, stl_hlm],
            [bnz_cst, irn_cst, stl_cst],
            [bnz_leg, irn_leg, stl_leg],
            ['\n       ', '\n       ', '\n       '],
            [wiz_hat, myst_hat, elem_hat],
            [wiz_rob, myst_rob, elem_rob],
            [wiz_gar, myst_gar, elem_gar]]

item_setup_vars()

def pick_category():
    global inventory
    while True:
        print('Categories: ' + ', '.join(sorted([x.title() for x in inventory], key=str.lower)))
        while True:
            cat = input('Input the name of the category you want to view (or type "exit"): ')
            try:
                cat = cat.lower()
            except AttributeError:
                continue
            if cat in inventory:
                if inventory[cat]:
                    if cat not in ['coord', 'weapons', 'armor']:
                        print('-'*25)
                        pick_item(cat)
                        print('-'*25)
                    elif cat == 'coord':
                        print('-'*25)
                        print(inventory[cat])
                        input("Press enter/return when you are finished viewing these coordinates.")
                        print('-'*25)
                    else:
                        if [x for x in inventory[cat] if not x.equip]:
                            pick_item(cat)
                            print('-'*25)
                        else:
                            print('-'*25)
                            print('The "%s" category is empty...' % (cat))
                            print('-'*25)
                    break
                else:
                    print('-'*25)
                    print('The "%s" category is empty...' % (cat))
                    print('-'*25)
                    break
            elif cat == 'exit':
                return

def pick_item(cat):
    while inventory[cat]:
        if cat == 'armor' or cat == 'weapons':
            if [x for x in inventory[cat] if not x.equip]:
                print('-'*25)
                print(cat.title() + ': ' + ', '.join(sorted([str(x) for x in inventory[cat] if not x.equip], key=str.lower)))
            else:
                return
        else:
            print('-'*25)
            print(cat.title() + ': ' + ', '.join(sorted([str(x) + ' x' + str(inventory[cat].count(x)) for x in set(inventory[cat])], key=str.lower)))
        while True:
            item = input('Input the name of the item you want to interact with (or type "back"): ')
            try:
                item = item.title()
            except AttributeError:
                continue
            try:
                for i in [x for x in inventory[cat] if not x.equip]:
                    if str(i) == item:
                        item = i
                        break
                    elif item == 'Back':
                        return
                else:
                    continue
            except AttributeError:
                for i in inventory[cat]:
                    if str(i) == item:
                        item = i
                        break
                    elif item == 'Back':
                        return
                else:
                    continue
            if isinstance(item, Armor) or isinstance(item, Weapon):
                if item.equip:
                    continue
            pick_action(cat, item)
            break

def pick_action(cat, item):
    global inventory
    print('-'*25)
    while item in inventory[cat]:
        if isinstance(item, Weapon) or isinstance(item, Armor):
            if item.equip:
               break
        action = input('%s | 1: %s, 2: Read Desc, 3: Drop, 4: Cancel | Input #(1-4): ' % (
        str(item), 'Equip' if isinstance(item, (Armor or Weapon)) else 'Use'))
        try:
            action = int(action)
        except TypeError:
            continue
        if action == 1:
            if isinstance(item, Weapon):
                 item.equip_weapon()
            elif isinstance(item, Armor):
                 item.equip_armor()
                 return
            elif isinstance(item, Consumable):
                 item.consume_item()
        elif action == 2:
            print('-'*25)
            print(str(item) + ': ' + item.desc)
            print('-'*25)
        elif action == 3:
            if item.imp:
                 print('You cannot dispose of quest-related items.')
            else:
                 while True:
                     y_n = input('Are you sure you want to get rid of this %s? | Yes or No: ' % (str(item)))
                     try:
                         y_n = y_n.lower()
                     except AttributeError:
                         continue
                     if y_n in ['yes', 'y']:
                         print('You toss the %s aside and continue on your journey.' % (str(item)))
                         inventory[cat].remove(item)
                         break
                     elif y_n in ['no', 'n']:
                         print('You decide to keep the %s with you.' % (str(item)))
                         break
        elif action == 4:
            print('-'*25)
            return

def add_item(item):
    global inventory
    inventory[item.cat].append(item)

def serialize_inv(path):
    j_inventory = {}
    for category in inventory:
        j_inventory[category] = []
        for item in inventory[category]:
            if category != 'coord':
                j_inventory[category].append(item.__dict__)
            else:
                j_inventory[category].append(item)
    with open(path, mode='w', encoding='utf-8') as c:
        json.dump(j_inventory, c, indent=4, separators=(', ', ': '))

def deserialize_inv(path):
    global inventory
    norm_inv = {}
    with open(path, mode='r', encoding='utf-8') as c:
       j_inventory = json.load(c)
    for category in j_inventory:
        norm_inv[category] = []
        for item in j_inventory[category]:
            if category == 'consum':
                x = Consumable('', '', '', '')
            elif category == 'weapon':
                x = Weapon('', '', '', '', '', '', '')
            elif category == 'armor':
                x = Armor('', '', '', '', '', '', '', '')
            elif category == 'coord':
                norm_inv[category].append(item)
                continue
            else:
                continue
            x.__dict__ = item
            norm_inv[category].append(x)
    inventory = norm_inv

def serialize_equip(path):
    j_equipped = {}
    for category in equipped:
        if equipped[category] != '(None)':
            j_equipped[category] = equipped[category].__dict__
        else:
            j_equipped[category] = '(None)'
    with open(path, mode='w', encoding='utf-8') as d:
        json.dump(j_equipped, d, indent=4, separators=(', ', ': '))

def deserialize_equip(path):
    global equipped
    norm_equip = {}
    with open(path, mode='r', encoding='utf-8') as d:
        j_equipped = json.load(d)
    for category in j_equipped:
        if j_equipped[category] == '(None)':
            norm_equip[category] = '(None)'
            continue
        elif category == 'weapon':
            x = Weapon('', '', '', '', '', '', '')
        else:
            x = Armor('', '', '', '', '', '', '', '')
        x.__dict__ = j_equipped[category]
        norm_equip[category] = x
    equipped = norm_equip
