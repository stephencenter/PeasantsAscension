import sys
import json
import npcs
import items as i
from copy import copy as _c


if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

inventory = {'q_items': [], 'consum': [_c(i.s_potion), _c(i.s_elixir)], 'coord': [],
             'weapons': [], 'armor': [], 'misc': []}
equipped = {'weapon': '', 'head': _c(i.straw_hat),
            'body': _c(i.cotton_shirt),
            'legs': _c(i.sunday_trousers)}

gs_stock = [[i.s_potion, i.s_potion, i.m_potion, i.l_potion, i.l_potion, i.x_potion],
            [i.s_elixir, i.s_elixir, i.m_elixir, i.l_elixir, i.l_elixir, i.x_elixir],
            [i.s_rejuv, i.s_rejuv, i.m_rejuv, i.m_rejuv, i.l_rejuv, i.l_rejuv],
            [i.cpr_swd, i.en_cpr_swd, i.bnz_spr, i.en_bnz_spr, i.irn_axe, i.en_irn_axe],
            [i.oak_stf, i.en_oak_stf, i.arc_spb, i.en_arc_spb, i.rnc_stf, i.en_rnc_stf],
            [i.sht_bow, i.en_sht_bow, i.lng_bow, i.en_lng_bow, i.myth_sb, i.en_myth_sb],
            [i.bnz_hlm, i.en_bnz_hlm, i.stl_hlm, i.en_stl_hlm, i.ori_hlm],
            [i.bnz_cst, i.en_bnz_cst, i.stl_cst, i.en_stl_cst, i.ori_cst],
            [i.bnz_leg, i.en_bnz_leg, i.stl_leg, i.en_stl_leg, i.ori_leg],
            [i.wiz_hat, i.en_wiz_hat, i.myst_hat, i.en_myst_hat, i.elem_hat],
            [i.wiz_rob, i.en_wiz_rob, i.myst_rob, i.en_myst_rob, i.elem_rob],
            [i.wiz_gar, i.en_wiz_gar, i.myst_gar, i.en_myst_gar, i.elem_gar],
            [i.lth_cap, i.en_lth_cap, i.std_cwl, i.en_std_cwl],
            [i.lth_bdy, i.en_lth_bdy, i.std_bdy, i.en_std_bdy],
            [i.lth_leg, i.en_lth_leg, i.std_leg, i.en_std_leg]]

gs_stock = list(gs_stock)
i.item_setup_vars()


def pick_category():
    global inventory
    while True:
        print("""Categories:
      [1] Armor
      [2] Consumables
      [3] Weapons
      [4] Quest Items
      [5] Coordinates
      [6] Miscellaneous
      [7] Quests""")
        while True:
            cat = input('Input [#] (or type "exit"): ')
            try:
                cat = cat.lower()
            except AttributeError:
                pass
            if cat in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
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
                cat = 'q_items'
                vis_cat = 'Quest Items'
            elif cat == '5':
                cat = 'coord'
                vis_cat = 'Coordinates'
            elif cat == '6':
                cat = 'misc'
                vis_cat = 'Miscellaneous'
            elif cat == '7':
                cat = 'quests'
                vis_cat = 'Quests'
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
                            input('The "{0}" category is empty. (Press Enter/Return) '.format(
                                vis_cat))
                            print('-'*25)
                    break
                else:
                    print('-'*25)
                    input('The "{0}" category is empty. (Press Enter/Return) '.format(vis_cat))
                    print('-'*25)
                    break
            elif cat == 'quests' and [x for x in npcs.all_dialogue if isinstance(
                    x, npcs.Quest) and x.started]:
                pick_item(cat, vis_cat)
                break
            else:
                print('-'*25)
                print("You have no active or completed quests. (Press Enter/Return) ")
                print('-'*25)


def pick_item(cat, vis_cat, gs=False):
    while cat == 'quests' or inventory[cat]:
        if cat == 'quests':
            print('-'*25)
            while True:
                fizz = True
                choice = input('View [f]inished or [a]ctive quests? |\
Input letter (or type "back"): ')
                try:
                    choice = choice.lower()
                except AttributeError:
                    continue

                if choice.startswith('f'):
                    print('-'*25)
                    dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest)
                                and x.finished]
                    if dialogue:
                        while fizz:
                            print('Finished Quests: ')
                            print('     ', '\n     '.join(['[' + str(num + 1) + '] ' + x.name
                                for num, x in enumerate([y for y in npcs.all_dialogue
                                if isinstance(y, npcs.Quest) and y.finished])]))

                            while True:
                                number = input('Input [#] (or type "back"): ')
                                try:
                                    number = int(number) - 1
                                except (TypeError, ValueError):
                                    try:
                                        if number.lower() in [
                                            'e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                            fizz = False
                                            break
                                        else:
                                            continue
                                    except AttributeError:
                                        continue
                                if (number < 0) or (number > len(dialogue) - 1):
                                    continue
                                quest = dialogue[number]
                                print('-'*25)
                                print("""{0}:\n    "{1}"\nGiven by: {2}""".format(
                                    quest.name, '\n     '.join([
                                        x for x in quest.desc]), quest.q_giver))
                                print('-'*25)
                                break
                    else:
                        input('You have no finished quests! (Press Enter/Return) ')
                    print('-'*25)

                elif choice.startswith('a'):
                    print('-'*25)
                    dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest)
                                and not x.finished and x.started]
                    if dialogue:
                        while fizz:
                            print('Active Quests: ')
                            print('     ', '\n     '.join(['[' + str(num + 1) + '] ' + x.name
                                for num, x in enumerate([y for y in npcs.all_dialogue
                                    if isinstance(y, npcs.Quest)
                                        and not y.finished and y.started])]))
                            while True:
                                number = input('Input [#] (or type "back"): ')
                                try:
                                    number = int(number) - 1
                                except (TypeError, ValueError):
                                    try:
                                        if number.lower() in [
                                            'e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                            fizz = False
                                            break
                                        else:
                                            continue
                                    except AttributeError:
                                        continue
                                if (number < 0) or (number > len(dialogue) - 1):
                                    continue
                                quest = dialogue[number]
                                print('-'*25)
                                print("""{0}:\n    "{1}"\nGiven by: {2}""".format(
                                    quest.name, '\n     '.join([
                                        x for x in quest.desc]), quest.q_giver))
                                print('-'*25)
                                break
                    else:
                        print('You have no active quests!')
                    print('-'*25)
                elif choice in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    return
        else:
            if cat in ['armor', 'weapons']:
                if [x for x in inventory[cat] if not x.equip]:
                    print('-'*25)
                    print(vis_cat + ': \n      ' + '\n      '.join(
                        ['[' + str(x + 1) + '] ' + str(y) for x, y in enumerate(
                            inventory[cat]) if not y.equip]))
                else:
                    return
            else:
                print('-'*25)
                print(''.join([vis_cat, ': \n      ', '\n      '.join(
                    ['[' + str(x + 1) + '] ' + str(y) for x, y in enumerate(inventory[cat])])]))
            while True:
                item = input('Input [#] (or type "back"): ')
                try:
                    item = int(item) - 1
                    if item < 0:
                        continue
                except (TypeError, ValueError):
                    try:
                        item = item.lower()
                    except AttributeError:
                        continue
                    if item in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return
                    else:
                        continue
                try:
                    if cat in ['weapons', 'armor']:
                        item = [x for x in inventory[cat] if not x.equip][item]
                    else:
                        item = inventory[cat][item]
                except IndexError:
                    continue
                if gs:
                    sell_item(cat, item)
                else:
                    pick_action(cat, item)
                break


def pick_action(cat, item):
    global inventory
    print('-'*25)
    while item in inventory[cat]:
        if isinstance(item, i.Weapon) or isinstance(item, i.Armor):
            use_equip = 'Equip'
            if item.equip:
                break
        else:
            use_equip = 'Use'
        action = input('{0} | 1: {1}, 2: Read Desc, 3: Drop, 4: Cancel | Input #(1-4): '.format(
            str(item), use_equip))
        if action == '1':
            item.use_item()
        elif action == '2':
            print('-'*25)
            print(str(item) + ': ' + item.desc)
            print('-'*25)
        elif action == '3':
            if item.imp:
                print('You cannot dispose of quest-related items.')
            else:
                while True:
                    y_n = input('Are you sure you want to get rid of this {0}\
? | Yes or No: '.format(str(item)))
                    try:
                        y_n = y_n.lower()
                    except AttributeError:
                        continue
                    if y_n.startswith('y'):
                        print('You toss the {0} aside and continue on your journey.'.format(
                            str(item)))
                        for x, y in enumerate(inventory[cat]):
                            if y.name == item.name:
                                inventory[cat].remove(y)
                                break
                        return
                    elif y_n.startswith('n'):
                        print('You decide to keep the {0} with you.'.format(str(item)))
                        break
        elif action == '4':
            return


def sell_item(cat, item):
    print('-'*25)
    print(item.desc)
    print('-'*25)
    while True:
        y_n = input('Do you wish to sell this {0} for {1} GP? | Yes or No: '.format(
            item.name, item.sell))
        try:
            y_n = y_n.lower()
        except AttributeError:
            continue
        if y_n.startswith('y'):
            for num, i in enumerate(inventory[cat]):
                if i.name == item.name:
                    inventory[cat].remove(inventory[cat][num])
                    main.static['gp'] += item.sell
                    print('You hand the shopkeep your {0} and recieve {1} GP.'.format(
                        item.name, item.sell))
                    return
        elif y_n.startswith('n'):
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
    with open(path, encoding='utf-8') as c:
        j_inventory = json.load(c)
    for category in j_inventory:
        norm_inv[category] = []
        for item in j_inventory[category]:
            if category == 'consum':
                x = i.Consumable('', '', '', '')
            elif category == 'weapon':
                x = i.Weapon('', '', '', '', '', '', '')
            elif category == 'armor':
                x = i.Armor('', '', '', '', '', '', '', '')
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
    with open(path, encoding='utf-8') as d:
        j_equipped = json.load(d)
    for category in j_equipped:
        if j_equipped[category] == '(None)':
            norm_equip[category] = '(None)'
            continue
        elif category == 'weapon':
            x = i.Weapon('', '', '', '', '', '', '')
        else:
            x = i.Armor('', '', '', '', '', '', '', '')
        x.__dict__ = j_equipped[category]
        norm_equip[category] = x
    equipped = norm_equip
