# This file is part of Peasants' Ascension.
#
#	 Peasants' Ascension is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Peasants' Ascension is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

import sys
import json
import time
import math
import random
from copy import copy as _c

import npcs
import ascii_art
import towns
import units
import items as i

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

inventory = {'q_items': [], 'consum': [_c(i.s_potion), _c(i.s_elixir)], 'coord': [],
             'weapons': [], 'armor': [], 'misc': [], 'access': []}

equipped = {
    'player': {
        'weapon': '',
        'head': _c(i.straw_hat),
        'body': _c(i.cotton_shirt),
        'legs': _c(i.sunday_trousers),
        'access': '(None)'
    },

    'Solou': {
        'weapon': i.mag_twg,
        'head': _c(i.straw_hat),
        'body': _c(i.cotton_shirt),
        'legs': _c(i.sunday_trousers),
        'access': '(None)'
    },

    'Xoann': {
        'weapon': i.stn_dag,
        'head': _c(i.straw_hat),
        'body': _c(i.cotton_shirt),
        'legs': _c(i.sunday_trousers),
        'access': '(None)'
    },

    'Parsto': {
        'weapon': i.stn_dag,
        'head': _c(i.straw_hat),
        'body': _c(i.cotton_shirt),
        'legs': _c(i.sunday_trousers),
        'access': '(None)'
    },

    'Adorine': {
        'weapon': i.stn_dag,
        'head': _c(i.straw_hat),
        'body': _c(i.cotton_shirt),
        'legs': _c(i.sunday_trousers),
        'access': '(None)'
    },

    'Chyme': {
        'weapon': i.stn_dag,
        'head': _c(i.straw_hat),
        'body': _c(i.cotton_shirt),
        'legs': _c(i.sunday_trousers),
        'access': '(None)'
    },

    "Ran'Af": {
        'weapon': i.stn_dag,
        'head': _c(i.straw_hat),
        'body': _c(i.cotton_shirt),
        'legs': _c(i.sunday_trousers),
        'access': '(None)'
    },

}

# "gs_stock" is a list of all items in the General Store's stock. The GS's level determines
# what items are in its stock via: [category[self.gs_level - 1] for category in gs_stock]

gs_stock = {'Potions': [[i.s_potion, i.s_potion, i.m_potion,
            i.l_potion, i.l_potion, i.x_potion],  # Health Potions

            [i.s_elixir, i.s_elixir, i.m_elixir,
             i.l_elixir, i.l_elixir, i.x_elixir],  # Mana Potions

            [i.s_rejuv, i.s_rejuv, i.m_rejuv,
             i.m_rejuv, i.l_rejuv, i.l_rejuv],  # HP + MP Potions

            [i.poison_potion, i.poison_potion, i.poison_potion,
             i.poison_potion, i.poison_potion, i.poison_potion],  # Poison Potion

            [i.sleep_potion, i.sleep_potion, i.sleep_potion,
             i.sleep_potion, i.sleep_potion, i.sleep_potion],  # Sleep Potion

            [i.silence_potion, i.silence_potion, i.silence_potion,
             i.silence_potion, i.silence_potion, i.silence_potion],  # Silence Potion

            [i.blindness_potion, i.blindness_potion, i.blindness_potion,
             i.blindness_potion, i.blindness_potion, i.blindness_potion],  # Blindness Potion

            [i.paralyzation_potion, i.paralyzation_potion, i.paralyzation_potion,
             i.paralyzation_potion, i.paralyzation_potion, i.paralyzation_potion],  # Para. Potion

            [i.weakness_potion, i.weakness_potion, i.weakness_potion,
             i.weakness_potion, i.weakness_potion, i.weakness_potion]  # Weakness Potion
            ],

            'Weapons': [[i.bnz_swd, i.en_bnz_swd, i.stl_spr,
            i.en_stl_spr, i.durs_axe, i.en_durs_axe],  # Warrior Weapons

            [i.oak_stf, i.en_oak_stf, i.arc_spb,
             i.en_arc_spb, i.rnc_stf, i.en_rnc_stf],  # Mage Weapons

            [i.ser_knf, i.en_ser_knf, i.stiletto,
             i.en_stiletto, i.myth_sb, i.en_myth_sb],  # Assassin Weapons

            [i.sht_bow, i.en_sht_bow, i.lng_bow,
             i.en_lng_bow, i.ash_cbow, i.en_ash_cbow],  # Ranger Weapons

            [i.holy_mace, i.en_holy_mace, i.hmr_of_mgt,
             i.en_hmr_of_mgt, i.ngt_bane, i.en_ngt_bane],  # Paladin Weapons

            [i.brass_kncls, i.en_brass_kncls, i.bladed_gloves,
             i.en_bladed_gloves, i.lead_bg, i.en_lead_bg]],  # Monk Weapons

            'Armor': [[i.bnz_hlm, i.en_bnz_hlm, i.stl_hlm,
            i.en_stl_hlm, i.ori_hlm, i.ori_hlm],  # Warrior Armor -- Head

            [i.bnz_cst, i.en_bnz_cst, i.stl_cst,
             i.en_stl_cst, i.ori_cst, i.ori_cst],  # Warrior Armor -- Body

            [i.bnz_leg, i.en_bnz_leg, i.stl_leg,
             i.en_stl_leg, i.ori_leg, i.ori_leg],  # Warrior Armor -- Legs

            [i.wiz_hat, i.en_wiz_hat, i.myst_hat,
             i.en_myst_hat, i.elem_hat, i.elem_hat],  # Mage Armor -- Head

            [i.wiz_rob, i.en_wiz_rob, i.myst_rob,
             i.en_myst_rob, i.elem_rob, i.elem_rob],  # Mage Armor -- Body

            [i.wiz_gar, i.en_wiz_gar, i.myst_gar,
             i.en_myst_gar, i.elem_gar, i.elem_gar],  # Mage Armor -- Legs

            [i.lth_cap, i.en_lth_cap, i.std_cwl,
             i.en_std_cwl, i.drg_cwl, i.drg_cwl],  # Assassin + Ranged Armor -- Head

            [i.lth_bdy, i.en_lth_bdy, i.std_bdy,
             i.en_std_bdy, i.drg_bdy, i.drg_bdy],  # Assassin + Ranged Armor -- Body

            [i.lth_leg, i.en_lth_leg, i.std_leg,
             i.en_std_leg, i.drg_leg]],  # Assassin + Ranged Armor -- Legs

            'Accessories': [[i.water_amulet, i.water_amulet, i.water_amulet,
                             i.water_amulet, i.water_amulet, i.water_amulet],

                            [i.fire_amulet, i.fire_amulet, i.fire_amulet,
                             i.fire_amulet, i.fire_amulet, i.fire_amulet],

                            [i.earth_amulet, i.earth_amulet, i.earth_amulet,
                             i.earth_amulet, i.earth_amulet, i.earth_amulet],

                            [i.electric_amulet, i.electric_amulet, i.electric_amulet,
                             i.electric_amulet, i.electric_amulet, i.electric_amulet],

                            [i.wind_amulet, i.wind_amulet, i.wind_amulet,
                             i.wind_amulet, i.wind_amulet, i.wind_amulet],

                            [i.grass_amulet, i.grass_amulet, i.grass_amulet,
                             i.grass_amulet, i.grass_amulet, i.grass_amulet],

                            [i.ice_amulet, i.ice_amulet, i.ice_amulet,
                             i.ice_amulet, i.ice_amulet, i.ice_amulet],

                            [i.life_amulet, i.life_amulet, i.life_amulet,
                             i.life_amulet, i.life_amulet, i.life_amulet],

                            [i.death_amulet, i.death_amulet, i.death_amulet,
                             i.death_amulet, i.death_amulet, i.death_amulet]],

            'Other': [[i.divining_rod, i.divining_rod, i.divining_rod,
                       i.divining_rod, i.divining_rod, i.divining_rod],

                      [i.shovel, i.shovel, i.shovel,
                       i.shovel, i.shovel, i.shovel],

                      [i.map_of_fast_travel, i.map_of_fast_travel, i.map_of_fast_travel,
                       i.map_of_fast_travel, i.map_of_fast_travel, i.map_of_fast_travel],

                      [i.boots_of_travel, i.boots_of_travel, i.boots_of_travel,
                       i.boots_of_travel, i.boots_of_travel, i.boots_of_travel]]}


def pick_category():
    global inventory
    while True:
        print("""Categories:
      [1] Armor
      [2] Weapons
      [3] Accessories
      [4] Equipped Items
      [5] Consumables
      [6] Coordinates
      [7] Quest Items
      [8] Quests
      [9] Miscellaneous""")
        while True:
            cat = input('Input [#] (or type "exit"): ')

            cat = cat.lower()

            if cat in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                return

            elif cat == '1':
                cat = 'armor'
                vis_cat = 'Armor'
            elif cat == '2':
                cat = 'weapons'
                vis_cat = 'Weapons'
            elif cat == '3':
                cat = 'access'
                vis_cat = 'Accessories'
            elif cat == '4':
                cat = 'equipped_items'
                vis_cat = 'Equipped Items'
            elif cat == '5':
                cat = 'consum'
                vis_cat = 'Consumables'
            elif cat == '6':
                cat = 'coord'
                vis_cat = 'Coordinates'
            elif cat == '7':
                cat = 'q_items'
                vis_cat = 'Quest Items'
            elif cat == '8':
                cat = 'quests'
                vis_cat = 'Quests'
            elif cat == '9':
                cat = 'misc'
                vis_cat = 'Miscellaneous'
            else:
                continue

            if cat in inventory:
                if inventory[cat]:

                    if cat not in ['coord', 'weapons', 'armor', 'access']:
                        pick_item(cat, vis_cat)
                        print('-'*25)

                    elif cat == 'coord':
                        print('-'*25)
                        print(' ', '\n  '.join(inventory[cat]))
                        input("\nPress enter/return ")
                        print('-'*25)

                    else:
                        if [x for x in inventory[cat]]:
                            pick_item(cat, vis_cat)
                            print('-'*25)

                        else:
                            print('-'*25)
                            print('The {0} category is empty.'.format(vis_cat))
                            input("\nPress enter/return ")
                            print('-'*25)

                    break

                else:
                    print('-'*25)
                    print('The {0} category is empty. (Press Enter/Return) '.format(vis_cat))
                    input("\nPress enter/return ")
                    print('-'*25)
                    break

            elif cat == 'equipped_items':
                pick_item(cat, vis_cat)
                break

            if cat == 'quests' and [x for x in npcs.all_dialogue if isinstance(
                    x, npcs.Quest) and x.started]:
                pick_item(cat, vis_cat)
                break

            else:
                print('-'*25)
                input("Your party has no active or completed quests. (Press Enter/Return) ")
                print('-'*25)
                break


def pick_item(cat, vis_cat, gs=False):  # Select an object to interact with in your inventory
    # If "gs == True" that means that items are being sold, and not used.
    while cat in ['quests', 'equipped_items'] or inventory[cat]:
        if cat == 'quests':
            view_quests()
            return

        elif cat == 'equipped_items':
            manage_equipped()
            return

        else:
            if inventory[cat]:
                print('-'*25)
                if not gs:
                    print('{0}: \n      '.format(vis_cat), end='')
                    print('\n      '.join(
                        ['[{0}] {1}'.format(x + 1, y)
                         for x, y in enumerate(inventory[cat])]))

                else:
                    try:
                        padding = len(max([
                            it.name for it in inventory[cat] if not it.imp
                        ], key=len))
                    except ValueError:
                        padding = 1

                    ext_pad = len(str(len([it.name for it in inventory[cat] if not it.imp]) + 1))

                    print('{0}: \n      '.format(vis_cat), end='')
                    print('\n      '.join(
                        ['[{0}] {1} {2}--> {3} GP'.format(
                            x + 1, y, '-'*(padding - len(y.name) + (ext_pad - len(str(x + 1)))),
                            y.sell)
                         for x, y in enumerate([it for it in inventory[cat] if not it.imp])]))
            else:
                return

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

    # Loop while the item is in the inventory
    while item in inventory[cat]:
        if (isinstance(item, i.Weapon)
            or isinstance(item, i.Armor)
                or isinstance(item, i.Accessory)):

            # You equip weapons/armor/accessories
            use_equip = 'Equip'

        else:
            # You use other items
            use_equip = 'Use'

        print('-'*25)
        action = input("""What do you want to do with your {0}?
      [1] {1}
      [2] Read Description
      [3] Drop
Input [#] (or type "back"): """.format(str(item), use_equip))

        if action == '1':
            if any([
                isinstance(item, i.Accessory),
                isinstance(item, i.Armor),
                isinstance(item, i.Consumable),
                isinstance(item, i.Weapon),
                isinstance(item, i.StatusPotion)
            ]):
                target_options = [x for x in [
                    units.player,
                    units.solou,
                    units.xoann,
                    units.adorine,
                    units.ran_af,
                    units.parsto,
                    units.chyme] if x.enabled
                ]

                if len(target_options) == 1:
                    target = units.player

                else:
                    print("Who should {0} the {1}?".format(use_equip.lower(), item.name))
                    print("     ", "\n      ".join(
                        ["[{0}] {1}".format(int(num) + 1, character.name)
                         for num, character in enumerate(target_options)]))

                    while True:
                        target = input("Input [#]: ")
                        try:
                            target = int(target) - 1
                        except ValueError:
                            continue

                        try:
                            target = target_options[target]
                        except IndexError:
                            continue

                        break

                item.use_item(target)
                if item not in inventory[cat]:
                    return

            else:
                item.use_item(units.player)
                if item not in inventory[cat]:
                    return

        elif action == '2':
            # Display the item description
            print('-'*25)
            print('-{0}-'.format(str(item).upper()))

            if hasattr(item, "ascart"):
                print(ascii_art.item_sprites[item.ascart])

            input('"{0}" | [ENTER] '.format(item.desc))

        elif action == '3':
            print('-'*25)

            if item.imp:
                print('You cannot dispose of essential items.')

            else:
                while True:
                    y_n = input('Are you sure you want to get rid of this {0}\
? | Yes or No: '.format(str(item)))

                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        input('Your party tosses the {0} aside and continues on their \
journey.'.format(str(item)))

                        inventory[cat].remove(item)
                        return

                    elif y_n.startswith('n'):
                        print('Your party decide to keep the {0} with them.'.format(str(item)))
                        main.smart_sleep(1)

                        break

            print('-'*25)

        elif action in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
            return


def manage_equipped():
    global equipped

    spam = False

    print('-'*25)
    target_options = [x for x in [
        units.player,
        units.solou,
        units.xoann,
        units.adorine,
        units.ran_af,
        units.parsto,
        units.chyme] if x.enabled
    ]

    print("Select Character: ")
    print("     ", "\n      ".join(["[{0}] {1}".format(int(num) + 1, character.name)
                                   for num, character in enumerate(target_options)]))

    while True:
        target = input("Input [#]: ")

        try:
            target = int(target) - 1

        except ValueError:
            continue

        try:
            target = target_options[target]

        except IndexError:
            continue

        break

    while True:
        if not spam:
            p_equip = equipped[target.name if target != units.player else 'player']

        print('-'*25)
        print("""{0}'s Equipped Items:
      [1] Weapon ----> {1}
      [2] Head ------> {2}
      [3] Body ------> {3}
      [4] Legs ------> {4}
      [5] Accessory -> {5}""".format(target.name,
                                     p_equip['weapon'], p_equip['head'],
                                     p_equip['body'], p_equip['legs'],
                                     p_equip['access']))
        spam = True
        while spam:
            selected = input('Input [#] (or type "back"): ')
            selected = selected.lower()

            if selected in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                print('-'*25)

                return

            elif selected == '1':
                selected = p_equip['weapon']

            elif selected == '2':
                selected = p_equip['head']

            elif selected == '3':
                selected = p_equip['body']

            elif selected == '4':
                selected = p_equip['legs']

            elif selected == '5':
                selected = p_equip['access']

            else:
                continue

            if selected == '(None)':
                print('-'*25)
                print("You don't have anything equipped in that slot.")
                input("\nPress enter/return ")
                break

            if isinstance(selected, i.Weapon):
                key = 'weapon'

            elif isinstance(selected, i.Accessory):
                key = 'access'

            elif isinstance(selected, i.Armor):
                key = selected.part

            print('-'*25)
            while True:
                action = input("""What do you want to do with your {0}?
      [1] Unequip
      [2] Read Description
Input [#] (or type "back"): """.format(str(selected)))

                if action == '1':
                    if selected.name == 'Fists':
                        print('-'*25)
                        print("Removing those would be difficult without causing damage.")
                        input("\nPress enter/return ")
                        print('-'*25)

                        continue

                    print('-'*25)
                    print('You unequip the {0}.'.format(selected.name))
                    input("\nPress enter/return ")

                    if isinstance(selected, i.Weapon):
                        inventory[selected.cat].append(p_equip[key])

                        p_equip[key] = i.fists

                    elif isinstance(selected, i.Armor):
                        inventory[selected.cat].append(p_equip[key])

                        p_equip[key] = '(None)'

                    elif isinstance(selected, i.Accessory):
                        if isinstance(selected, i.ElementAccessory):
                            target.element = 'none'

                            print('You are no longer imbued with the {0} element.'.format(selected.element))
                            input("\nPress enter/return ")

                        inventory[selected.cat].append(p_equip[key])
                        p_equip[key] = '(None)'

                    spam = False
                    break

                elif action == '2':
                    print('-'*25)

                    if hasattr(selected, "ascart"):
                        print(ascii_art.item_sprites[selected.ascart])

                    print(selected.desc)
                    input("\nPress enter/return ")
                    print('-'*25)

                elif action.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    spam = False
                    break


def view_quests():
    print('-'*25)
    while True:
        fizz = True
        choice = input('View [f]inished or [a]ctive quests? | Input [Letter] (or type "back"): ')

        choice = choice.lower()

        if choice.startswith('f'):  # Finished Quests
            print('-'*25)
            dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest) and x.finished]

            if dialogue:
                while fizz:
                    print('Finished Quests:\n      ', end='')
                    print('\n      '.join(['[{0}] {1}'.format(num + 1, x.name)
                                           for num, x in enumerate([
                                           y for y in npcs.all_dialogue
                                           if isinstance(y, npcs.Quest) and y.finished])]))

                    while True:
                        number = input('Input [#] (or type "back"): ')

                        try:
                            number = int(number) - 1

                        except ValueError:
                            if number.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
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
                print('Your party has no finished quests!')
                input("\nPress enter/return")

            print('-'*25)

        elif choice.startswith('a'):  # Active Quest
            print('-'*25)

            dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest) and not x.finished and x.started]

            if dialogue:
                while fizz:
                    print('Active Quests: ')
                    print('     ', '\n     '.join(['[{0}] {1}'.format(num + 1, x)
                                                   for num, x in
                                                   enumerate([y for y in npcs.all_dialogue
                                                              if isinstance(y, npcs.Quest)
                                                              and not y.finished and y.started])]))

                    while True:
                        number = input('Input [#] (or type "back"): ')

                        try:
                            number = int(number) - 1

                        except ValueError:

                            if number.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:

                                fizz = False  # Break the loop twice
                                break

                            else:
                                continue

                        if (number < 0) or (number > len(dialogue) - 1):
                            continue

                        quest = dialogue[number]

                        print('-'*25)

                        print("""{0}:\n    "{1}"\nGiven by: {2}""".format(quest.name, '\n     '.join([
                                x for x in quest.desc]), quest.q_giver))

                        input("\nPress enter/return ")
                        print('-'*25)

                        break
            else:
                print('Your party has no active quests!')
                input('\nPress enter/return ')

            print('-'*25)

        elif choice in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
            return


def sell_item(cat, item):  # Trade player-owned objects for money (GP)
    print('-'*25)

    if hasattr(item, "ascart"):
        print(ascii_art.item_sprites[item.ascart])

    print(item.desc)
    print('-'*25)
    while True:
        y_n = input('Do you wish to sell this {0} for {1} GP? | Yes or No: '.format(item.name, item.sell))
        y_n = y_n.lower()

        if y_n.startswith('y'):
            for num, it in enumerate(inventory[cat]):
                if it.name == item.name:

                    inventory[cat].remove(it)
                    main.party_info['gp'] += item.sell

                    print('Your party hands the shopkeeper their {0} and receives {1} GP.'.format(item.name, item.sell))
                    input('\nPress enter/return ')
                    return

        elif y_n.startswith('n'):
            return


def tools_menu():  # Display a set of usable tools on the world map
    tool_names = ['Divining Rod', 'Shovel', 'Magical Compass', 'Map of Fast Travel', 'Boots of Insane Speed']
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
        print('Your party has no available tools to use.')
        input('\nPress enter/return ')

        if not towns.search_towns(main.party_info['x'], main.party_info['y'], enter=False):
            print('-'*25)

        return

    while spam:
        print('Tools: \n      ', end='')
        print('\n      '.join(['[{0}] {1}'.format(x + 1, y) for x, y in enumerate(available_tools)]))

        while True:
            tool = input('Input [#] (or type "exit"): ')

            try:
                tool = int(tool) - 1

            except ValueError:
                if tool.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    spam = False

                    if not towns.search_towns(main.party_info['x'], main.party_info['y'], enter=False):
                        print('-'*25)

                    break

                else:
                    continue

            if (tool < 0) or (tool > len(available_tools) - 1):
                continue

            tool = available_tools[tool]
            tool.use_item(units.player)

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
                    x = i.StatusPotion('', '', '', '', '')

                else:
                    x = i.Consumable('', '', '', '')

            elif category == 'weapons':
                x = i.Weapon('', '', '', '', '', '', '', '')

            elif category == 'armor':
                x = i.Armor('', '', '', '', '', '', '', '', '')

            elif category == 'access':
                if item['acc_type'] == 'elemental':
                    x = i.ElementAccessory('', '', '', '', '')

            elif category == 'coord':
                norm_inv[category].append(item)
                continue

            elif category in ['misc', 'q_items']:
                if item['name'] == 'Magical Compass':
                    item = i.magic_compass
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Divining Rod':
                    item = i.divining_rod
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Shovel':
                    item = i.shovel
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Map of Fast Travel':
                    item = i.map_of_fast_travel
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Boots of Travel':
                    item = i.boots_of_travel
                    norm_inv[category].append(item)
                    continue

                else:
                    x = i.Misc('', '', '', '')
            else:
                continue

            if (not isinstance(x, i.Armor)
                    and not isinstance(x, i.Weapon)):

                item_art = x.ascart
                x.__dict__ = item
                x.ascart = item_art

            else:
                x.__dict__ = item

            norm_inv[category].append(x)

    inventory = norm_inv


def serialize_equip(path):
    j_equipped = {}

    for user in equipped:
        j_equipped[user] = {}
        for category in equipped[user]:
            if equipped[user][category] != '(None)':
                j_equipped[user][category] = equipped[user][category].__dict__
            else:
                j_equipped[user][category] = '(None)'

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_equipped, f, indent=4, separators=(', ', ': '))


def deserialize_equip(path):
    global equipped
    norm_equip = {}

    with open(path, encoding='utf-8') as f:
        j_equipped = json.load(f)

    for user in j_equipped:
        norm_equip[user] = {}
        for category in j_equipped[user]:
            if j_equipped[user][category] == '(None)':
                norm_equip[user][category] = '(None)'
                continue

            elif category == 'weapon':
                x = i.Weapon('', '', '', '', '', '', '', '')

            elif category == 'access':
                if j_equipped[category]['acc_type'] == 'elemental':
                    x = i.ElementAccessory('', '', '', '', '')

            else:
                x = i.Armor('', '', '', '', '', '', '', '', '')

            x.__dict__ = j_equipped[user][category]
            norm_equip[user][category] = x

    equipped = norm_equip
