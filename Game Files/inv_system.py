import sys
import towns
import json
from copy import copy as _c
from items import *

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

inventory = {'quest': [], 'consum': [_c(s_potion), _c(s_elixr)], 'coord': [],
             'weapons': [], 'armor': [], 'misc': []}
equipped = {'weapon': '', 'head': '(None)', 'body': '(None)', 'legs': '(None)'}

gs_stock = [[s_potion, m_potion, l_potion, l_potion, l_potion, l_potion],
            [s_elixr, m_elixr, l_elixr, l_elixr, l_elixr, l_elixr],
            ['\n       ' for x in range(6)],
            [cpr_swd, en_cpr_swd, bnz_spr, en_bnz_spr, irn_axe, en_irn_axe],
            [oak_stf, en_oak_stf, arc_spb, en_arc_spb, rnc_stf, en_irn_axe],
            ['\n       ' for x in range(6)],
            [bnz_hlm, irn_hlm, stl_hlm],
            [bnz_cst, irn_cst, stl_cst],
            [bnz_leg, irn_leg, stl_leg],
            ['\n       ' for x in range(6)],
            [wiz_hat, myst_hat, elem_hat],
            [wiz_rob, myst_rob, elem_rob],
            [wiz_gar, myst_gar, elem_gar]]
gs_stock = list(gs_stock)
item_setup_vars()


def pick_category():
    global inventory
    while True:
        print('Categories: 1: Armor; 2: Consumables; 3: Weapons; 4: Quest Items; 5: Misc.')
        while True:
            cat = input('Input the number of the category you want to view (or type "exit"): ')
            try:
                cat = cat.lower()
            except AttributeError:
                pass
            if cat == 'exit':
                return
            elif cat == '1':
                cat = 'armor'
                vis_cat = 'Armor'
            elif cat == '2':
                cat = 'consum'
                vis_cat = 'Consumables'
            elif cat == '3':
                cat = 'weapons'
                vis_cat = 'Weapons'
            elif cat == '4':
                cat = 'quest'
                vis_cat = 'Quest Items'
            elif cat == '5':
                cat = 'misc'
                vis_cat = 'Misc.'
            else:
                continue
            if cat in inventory:
                if inventory[cat]:
                    if cat not in ['coord', 'weapons', 'armor']:
                        pick_item(cat, vis_cat)
                        print('-'*25)
                    elif cat == 'coord':
                        print('-'*25)
                        print(inventory[cat])
                        input("Press enter/return when you are finished viewing these coordinates.")
                        print('-'*25)
                    else:
                        if [x for x in inventory[cat] if not x.equip]:
                            pick_item(cat, vis_cat)
                            print('-'*25)
                        else:
                            print('-'*25)
                            print('The "{0}" category is empty...'.format(vis_cat))
                            print('-'*25)
                    break
                else:
                    print('-'*25)
                    print('The "{0}" category is empty...'.format(vis_cat))
                    print('-'*25)
                    break


def pick_item(cat, vis_cat):
    while inventory[cat]:
        if cat == 'armor' or cat == 'weapons':
            if [x for x in inventory[cat] if not x.equip]:
                print('-'*25)
                print(vis_cat + ': \n      ' + '\n      '.join(
                      ['[' + str(x + 1) + '] ' + str(y) for x, y in enumerate(
                      inventory[cat]) if not y.equip]))
            else:
                return
        else:
            print('-'*25)
            print(vis_cat + ': \n      ' + '\n      '.join(
                  ['[' + str(x + 1) + '] ' + str(y)
                  for x, y in enumerate(inventory[cat])]))
        while True:
            item = input('Input [#] (or type "back"): ')
            try:
                item = int(item) - 1
            except (TypeError, ValueError):
                try:
                    item = item.lower()
                except AttributeError:
                    continue
                if item == 'back':
                    return
            if item < 0:
                continue
            try:
                if cat in ['weapons', 'armor']:
                    item = [x for x in inventory[cat] if not x.equip][item]
                else:
                    item = inventory[cat][item]
            except IndexError:
                continue
            pick_action(cat, item)
            break


def pick_action(cat, item):
    global inventory
    print('-'*25)
    while item in inventory[cat]:
        if isinstance(item, Weapon) or isinstance(item, Armor):
            use_equip = 'Equip'
            if item.equip:
               break
        else:
            use_equip = 'Use'
        action = input('{0} | 1: {1}, 2: Read Desc, 3: Drop, 4: Cancel | Input #(1-4): '.format(
        str(item), use_equip))
        try:
            action = int(action)
        except TypeError:
            continue
        if action == 1:
            if isinstance(item, Weapon):
                 item.equip_weapon()
            elif isinstance(item, Armor):
                 item.equip_armor()
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
                     y_n = input('Are you sure you want to get rid of this {0}? | Yes or No: '.format(str(item)))
                     try:
                         y_n = y_n.lower()
                     except AttributeError:
                         continue
                     if y_n in ['yes', 'y']:
                         print('You toss the {0} aside and continue on your journey.'.format(str(item)))
                         for x, y in enumerate(inventory[cat]):
                             if y.name == item.name:
                                 inventory[cat].remove(y)
                                 break
                         return
                     elif y_n in ['no', 'n']:
                         print('You decide to keep the {0} with you.'.format(str(item)))
                         break
        elif action == 4:
            return


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
