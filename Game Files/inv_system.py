# This file is part of PythoniusRPG.
#
#	 PythoniusRPG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PythoniusRPG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PythoniusRPG.  If not, see <http://www.gnu.org/licenses/>.

import sys
import json
import time
import pets
from copy import copy as _c

import npcs
import towns
import items as i


if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

inventory = {'q_items': [], 'consum': [_c(i.s_potion), _c(i.s_elixir)], 'coord': [],
             'weapons': [], 'armor': [], 'pets': [], 'misc': []}
equipped = {'weapon': '', 'head': _c(i.straw_hat),
            'body': _c(i.cotton_shirt),
            'legs': _c(i.sunday_trousers)}

# "gs_stock" is a list of all items in the General Store's stock. The GS's level determines
# what items are in its stock via: [category[self.gs_level - 1] for category in gs_stock]

gs_stock = [[i.s_potion, i.s_potion, i.m_potion,
             i.l_potion, i.l_potion, i.x_potion],  # Health Potions

            [i.s_elixir, i.s_elixir, i.m_elixir,
             i.l_elixir, i.l_elixir, i.x_elixir],  # Mana Potions

            [i.s_rejuv, i.s_rejuv, i.m_rejuv,
             i.m_rejuv, i.l_rejuv, i.l_rejuv],  # HP + MP Potions

            [i.cpr_swd, i.en_cpr_swd, i.bnz_spr,
             i.en_bnz_spr, i.irn_axe, i.en_irn_axe],  # Warrior Weapons

            [i.oak_stf, i.en_oak_stf, i.arc_spb,
             i.en_arc_spb, i.rnc_stf, i.en_rnc_stf],  # Mage Weapons

            [i.ser_knf, i.en_ser_knf, i.stiletto,
             i.en_stiletto, i.myth_sb, i.en_myth_sb],  # Assassin Weapons

            [i.sht_bow, i.en_sht_bow, i.lng_bow,
             i.en_lng_bow, i.ash_cbow, i.en_ash_cbow],  # Ranger Weapons

            [i.bnz_hlm, i.en_bnz_hlm, i.stl_hlm,
             i.en_stl_hlm, i.ori_hlm],  # Warrior Armor -- Head

            [i.bnz_cst, i.en_bnz_cst, i.stl_cst,
             i.en_stl_cst, i.ori_cst],  # Warrior Armor -- Body

            [i.bnz_leg, i.en_bnz_leg, i.stl_leg,
             i.en_stl_leg, i.ori_leg],  # Warrior Armor -- Legs

            [i.wiz_hat, i.en_wiz_hat, i.myst_hat,
             i.en_myst_hat, i.elem_hat],  # Mage Armor -- Head

            [i.wiz_rob, i.en_wiz_rob, i.myst_rob,
             i.en_myst_rob, i.elem_rob],  # Mage Armor -- Body

            [i.wiz_gar, i.en_wiz_gar, i.myst_gar,
             i.en_myst_gar, i.elem_gar],  # Mage Armor -- Legs

            [i.lth_cap, i.en_lth_cap, i.std_cwl,
             i.en_std_cwl, i.drg_cwl],  # Assassin + Ranged Armor -- Head

            [i.lth_bdy, i.en_lth_bdy, i.std_bdy,
             i.en_std_bdy, i.drg_bdy],  # Assassin + Ranged Armor -- Body

            [i.lth_leg, i.en_lth_leg, i.std_leg,
             i.en_std_leg, i.drg_leg]]  # Assassin + Ranged Armor -- Legs

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
      [6] Pets
      [7] Miscellaneous
      [8] Quests""")
        while True:
            cat = input('Input [#] (or type "exit"): ')

            cat = cat.lower()

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
                cat = 'pets'
                vis_cat = 'Pets'
            elif cat == '7':
                cat = 'misc'
                vis_cat = 'Miscellaneous'
            elif cat == '8':
                cat = 'quests'
                vis_cat = 'Quests'
            else:
                continue
            if cat in inventory:

                if inventory[cat]:

                    if cat not in ['coord', 'weapons', 'armor', 'pets']:
                        pick_item(cat, vis_cat)
                        print('-'*25)

                    elif cat == 'coord':
                        print('-'*25)
                        print(' ', '\n  '.join(inventory[cat]))
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

            if cat == 'quests' and [x for x in npcs.all_dialogue if isinstance(
                    x, npcs.Quest) and x.started]:
                pick_item(cat, vis_cat)
                break

            else:
                print('-'*25)
                input("You have no active or completed quests. (Press Enter/Return) ")
                print('-'*25)
                break


def pick_item(cat, vis_cat, gs=False):  # Select an object to interact with in your inventory
    # If "gs == True" that means that items are being sold, and not used.
    while cat == 'quests' or inventory[cat]:
        if cat == 'quests':
            view_quests()
            return

        else:
            if cat in ['armor', 'weapons', 'pets']:
                if [x for x in inventory[cat] if not x.equip]:
                    print('-'*25)
                    if not gs:
                        print(vis_cat + ': \n      ' + '\n      '.join(
                            ['[' + str(x + 1) + '] ' + str(y) for x, y in enumerate(
                                inventory[cat]) if not y.equip]))

                    else:
                        print(vis_cat + ': \n      ' + '\n      '.join(
                            ['[' + str(x + 1) + '] ' + str(y) + ' --> ' + str(y.sell) + ' GP'
                             for x, y in enumerate(inventory[cat]) if not y.equip]))
                else:
                    return

            else:
                print('-'*25)
                if not gs:
                    print(''.join([vis_cat, ': \n      ', '\n      '.join(
                        ['[' + str(x + 1) + '] ' + str(y)
                         for x, y in enumerate(inventory[cat])])]))

                else:
                    print(''.join([vis_cat, ': \n      ', '\n      '.join(
                        ['[' + str(x + 1) + '] ' + str(y) + ' --> ' + str(y.sell) + ' GP'
                         for x, y in enumerate(inventory[cat]) if not y.imp])]))

            while True:
                item = input('Input [#] (or type "back"): ')
                try:
                    item = int(item) - 1
                    if item < 0:
                        continue

                except ValueError:
                    item = item.lower()

                    if item in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return
                    else:
                        continue

                try:
                    if cat in ['weapons', 'armor']:
                        if gs:
                            item = [x for x in inventory[cat] if not x.equip and not x.imp][item]
                        else:
                            item = [x for x in inventory[cat] if not x.equip][item]

                    else:
                        if gs:
                            item = [x for x in inventory[cat] if not x.imp][item]
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
        if (isinstance(item, i.Weapon)
            or isinstance(item, i.Armor)
                or isinstance(item, pets.Companion)):

            use_equip = 'Equip'

            if item.equip:
                break
        else:
            use_equip = 'Use'
        action = input("""What do you want to do with {0} {1}?'
      [1] {2}
      [2] Read Description
      [3] Drop
Input [#] (or type "back"): """.format('these' if str(item).endswith('s') else 'this',
                                       str(item), use_equip))

        if action == '1':
            if isinstance(item, pets.Companion):
                item.equip = True
                main.player.current_pet.equip = False
                main.player.current_pet = item

            else:
                item.use_item()

        elif action == '2':
            print('-'*25)
            print(str(item) + ': ' + item.desc)
            time.sleep(1)
            print('-'*25)

        elif action == '3':
            print('-'*25)

            if item.imp:
                print('You cannot dispose of quest-related items.')

            else:
                while True:
                    y_n = input('Are you sure you want to get rid of this {0}\
? | Yes or No: '.format(str(item)))

                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        print('You toss the {0} aside and continue on your journey.'.format(
                            str(item)))

                        for x, y in enumerate(inventory[cat]):
                            if y.name == item.name:
                                inventory[cat].remove(y)
                                break

                        time.sleep(1)
                        return

                    elif y_n.startswith('n'):
                        print('You decide to keep the {0} with you.'.format(str(item)))
                        time.sleep(1)
                        break

            print('-'*25)

        elif action in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
            return


def view_quests():
    print('-'*25)
    while True:
        fizz = True
        choice = input('View [f]inished or [a]ctive quests? | Input [Letter] (or type "back"): ')

        choice = choice.lower()

        if choice.startswith('f'):  # Finished Quests
            print('-'*25)
            dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest)
                        and x.finished]
            if dialogue:
                while fizz:
                    print('Finished Quests: ')
                    print('     ', '\n     '.join(['[' + str(num + 1) + '] ' + x.name
                                                   for num, x in
                                                   enumerate([y for y in npcs.all_dialogue
                                                              if isinstance(y, npcs.Quest)
                                                              and y.finished])]))

                    while True:
                        number = input('Input [#] (or type "back"): ')

                        try:
                            number = int(number) - 1

                        except ValueError:
                            if number.lower() in [
                                'e', 'x', 'exit', 'c', 'cancel', 'b', 'back'
                            ]:
                                fizz = False  # Break the loop twice
                                break

                            else:
                                continue

                        if (number < 0) or (number > len(dialogue) - 1):
                            continue

                        quest = dialogue[number]

                        print('-'*25)
                        print("""{0}:\n    "{1}"\nGiven by: {2}""".format(
                            quest.name, '\n     '.join([x for x in quest.desc]), quest.q_giver))
                        print('-'*25)

                        break
            else:
                input('You have no finished quests! (Press Enter/Return) ')
            print('-'*25)

        elif choice.startswith('a'):  # Active Quest
            print('-'*25)

            dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest)
                        and not x.finished and x.started]

            if dialogue:
                while fizz:
                    print('Active Quests: ')
                    print('     ', '\n     '.join(['[' + str(num + 1) + '] ' + x.name
                                                   for num, x in
                                                   enumerate([y for y in npcs.all_dialogue
                                                              if isinstance(y, npcs.Quest)
                                                              and not y.finished and y.started])]))

                    while True:
                        number = input('Input [#] (or type "back"): ')

                        try:
                            number = int(number) - 1
                        except ValueError:

                            if number.lower() in [
                                'e', 'x', 'exit', 'c', 'cancel', 'b', 'back'
                            ]:

                                fizz = False  # Break the loop twice
                                break

                            else:
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


def sell_item(cat, item):  # Trade player-owned objects for money (GP)
    print('-'*25)
    print(item.desc)
    print('-'*25)
    while True:
        y_n = input('Do you wish to sell this {0} for {1} GP? | Yes or No: '.format(
            item.name, item.sell))

        y_n = y_n.lower()

        if y_n.startswith('y'):
            for num, i in enumerate(inventory[cat]):
                if i.name == item.name:

                    inventory[cat].remove(inventory[cat][num])
                    main.misc_vars['gp'] += item.sell

                    print('You hand the shopkeep your {0} and recieve {1} GP.'.format(
                        item.name, item.sell))

                    return

        elif y_n.startswith('n'):
            return


def tools_menu():  # Display a set of usable tools on the world map
    tool_names = ['Divining Rod', 'Shovel', 'Magical Compass']
    available_tools = []
    spam = True

    for cat in inventory:
        if cat in ['coord', 'quests']:
            continue

        for item in set(inventory[cat]):
            if item.name in tool_names:
                available_tools.append(item)

    print('-'*25)

    if not available_tools:
        print('You have no available tools to use...')
        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)
        return

    while spam:
        print(''.join(['Tools', ': \n      ', '\n      '.join(
            ['[' + str(x + 1) + '] ' + str(y)
             for x, y in enumerate(available_tools)])]))

        while True:
            tool = input('Input [#] (or type "exit"): ')

            try:
                tool = int(tool) - 1
            except ValueError:
                if tool.lower() in [
                    'e', 'x', 'exit', 'c', 'cancel', 'b', 'back'
                ]:
                    spam = False  # Essentially breaks the loop twice
                    if not towns.search_towns(
                            main.position['x'],
                            main.position['y'], enter=False
                    ):
                        print('-'*25)
                    break

                else:
                    continue

            if (tool < 0) or (tool > len(available_tools) - 1):
                continue

            tool = available_tools[tool]
            tool.use_item()

            break


def serialize_inv(path):
    j_inventory = {}

    for category in inventory:
        j_inventory[category] = []

        for item in inventory[category]:
            if category != 'coord':
                j_inventory[category].append(item.__dict__)

            else:
                j_inventory[category].append(item)

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_inventory, f, indent=4, separators=(', ', ': '))


def deserialize_inv(path):
    global inventory
    norm_inv = {}

    with open(path, encoding='utf-8') as f:
        j_inventory = json.load(f)

    for category in j_inventory:
        norm_inv[category] = []

        for item in j_inventory[category]:
            if category == 'consum':
                if 'Potion of ' in item['name']:
                    x = i.StatusPotion('', '', '', '')

                else:
                    x = i.Consumable('', '', '', '')

            elif category == 'weapon':
                x = i.Weapon('', '', '', '', '', '', '')

            elif category == 'armor':
                x = i.Armor('', '', '', '', '', '', '', '')

            elif category == 'coord':
                norm_inv[category].append(item)
                continue

            elif category == 'pets':
                for j in pets.all_pets:
                    for key in j_inventory['pets']:
                        if j.name == key:
                            norm_inventory['pets'].append(j)
                continue

            elif category in ['misc', 'q_items']:
                if item['name'] == 'Magical Compass':
                    item = i.magic_compass
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Dowsing Rod':
                    item = i.dowsing_rod
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Shovel':
                    item = i.shovel
                    norm_inv[category].append(item)
                    continue

                else:
                    x = i.Item('', '', '', '')
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

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_equipped, f, indent=4, separators=(', ', ': '))


def deserialize_equip(path):
    global equipped
    norm_equip = {}

    with open(path, encoding='utf-8') as f:
        j_equipped = json.load(f)

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
