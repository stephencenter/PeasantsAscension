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
import items

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

inventory = {'q_items': [], 'consum': [_c(items.s_potion), _c(items.s_elixir)], 'coord': [],
             'weapons': [], 'armor': [], 'tools': [], 'misc': [], 'access': []}

equipped = {
    'player': {
        'weapon': '',
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': '(None)'
    },

    'Solou': {
        'weapon': _c(items.mag_twg),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': '(None)'
    },

    'Xoann': {
        'weapon': _c(items.stn_dag),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': '(None)'
    },

    'Parsto': {
        'weapon': _c(items.slg_sht),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': '(None)'
    },

    'Adorine': {
        'weapon': _c(items.wdn_sht),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': '(None)'
    },

    'Chyme': {
        'weapon': _c(items.rbr_mlt),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': '(None)'
    },

    "Ran'Af": {
        'weapon': _c(items.fists),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': '(None)'
    },

}

# "gs_stock" is a list of all items in the General Store's stock. The GS's level determines
# what items are in its stock via: [category[self.gs_level - 1] for category in gs_stock]

gs_stock = {'Potions': [[items.s_potion, items.s_potion, items.m_potion,
                         items.l_potion, items.l_potion, items.x_potion],  # Health Potions

            [items.s_elixir, items.s_elixir, items.m_elixir,
             items.l_elixir, items.l_elixir, items.x_elixir],  # Mana Potions

            [items.s_rejuv, items.s_rejuv, items.m_rejuv,
             items.m_rejuv, items.l_rejuv, items.l_rejuv],  # HP + MP Potions

            [items.poison_potion, items.poison_potion, items.poison_potion,
             items.poison_potion, items.poison_potion, items.poison_potion],  # Poison Potion

            [items.sleep_potion, items.sleep_potion, items.sleep_potion,
             items.sleep_potion, items.sleep_potion, items.sleep_potion],  # Sleep Potion

            [items.silence_potion, items.silence_potion, items.silence_potion,
             items.silence_potion, items.silence_potion, items.silence_potion],  # Silence Potion

            [items.blindness_potion, items.blindness_potion, items.blindness_potion,
             items.blindness_potion, items.blindness_potion, items.blindness_potion],  # Blindness Potion

            [items.paralyzation_potion, items.paralyzation_potion, items.paralyzation_potion,
             items.paralyzation_potion, items.paralyzation_potion, items.paralyzation_potion],  # Para. Potion

            [items.weakness_potion, items.weakness_potion, items.weakness_potion,
             items.weakness_potion, items.weakness_potion, items.weakness_potion]],  # Weakness Potion

            'Weapons': [[items.bnz_swd, items.en_bnz_swd, items.stl_spr,
                         items.en_stl_spr, items.durs_axe, items.en_durs_axe],  # Warrior Weapons

            [items.oak_stf, items.en_oak_stf, items.arc_spb,
             items.en_arc_spb, items.rnc_stf, items.en_rnc_stf],  # Mage Weapons

            [items.ser_knf, items.en_ser_knf, items.stiletto,
             items.en_stiletto, items.myth_sb, items.en_myth_sb],  # Assassin Weapons

            [items.sht_bow, items.en_sht_bow, items.lng_bow,
             items.en_lng_bow, items.ash_cbow, items.en_ash_cbow],  # Ranger Weapons

            [items.holy_mace, items.en_holy_mace, items.hmr_of_mgt,
             items.en_hmr_of_mgt, items.ngt_bane, items.en_ngt_bane],  # Paladin Weapons

            [items.brass_kncls, items.en_brass_kncls, items.bladed_gloves,
             items.en_bladed_gloves, items.lead_bg, items.en_lead_bg]],  # Monk Weapons

            'Armor': [[items.bnz_hlm, items.en_bnz_hlm, items.stl_hlm,
                       items.en_stl_hlm, items.ori_hlm, items.ori_hlm],  # Warrior Armor -- Head

            [items.bnz_cst, items.en_bnz_cst, items.stl_cst,
             items.en_stl_cst, items.ori_cst, items.ori_cst],  # Warrior Armor -- Body

            [items.bnz_leg, items.en_bnz_leg, items.stl_leg,
             items.en_stl_leg, items.ori_leg, items.ori_leg],  # Warrior Armor -- Legs

            [items.wiz_hat, items.en_wiz_hat, items.myst_hat,
             items.en_myst_hat, items.elem_hat, items.elem_hat],  # Mage Armor -- Head

            [items.wiz_rob, items.en_wiz_rob, items.myst_rob,
             items.en_myst_rob, items.elem_rob, items.elem_rob],  # Mage Armor -- Body

            [items.wiz_gar, items.en_wiz_gar, items.myst_gar,
             items.en_myst_gar, items.elem_gar, items.elem_gar],  # Mage Armor -- Legs

            [items.lth_cap, items.en_lth_cap, items.std_cwl,
             items.en_std_cwl, items.drg_cwl, items.drg_cwl],  # Assassin + Ranged Armor -- Head

            [items.lth_bdy, items.en_lth_bdy, items.std_bdy,
             items.en_std_bdy, items.drg_bdy, items.drg_bdy],  # Assassin + Ranged Armor -- Body

            [items.lth_leg, items.en_lth_leg, items.std_leg,
             items.en_std_leg, items.drg_leg]],  # Assassin + Ranged Armor -- Legs

            'Accessories': [[items.water_amulet, items.water_amulet, items.water_amulet,
                             items.water_amulet, items.water_amulet, items.water_amulet],

                            [items.fire_amulet, items.fire_amulet, items.fire_amulet,
                             items.fire_amulet, items.fire_amulet, items.fire_amulet],

                            [items.earth_amulet, items.earth_amulet, items.earth_amulet,
                             items.earth_amulet, items.earth_amulet, items.earth_amulet],

                            [items.electric_amulet, items.electric_amulet, items.electric_amulet,
                             items.electric_amulet, items.electric_amulet, items.electric_amulet],

                            [items.wind_amulet, items.wind_amulet, items.wind_amulet,
                             items.wind_amulet, items.wind_amulet, items.wind_amulet],

                            [items.grass_amulet, items.grass_amulet, items.grass_amulet,
                             items.grass_amulet, items.grass_amulet, items.grass_amulet],

                            [items.ice_amulet, items.ice_amulet, items.ice_amulet,
                             items.ice_amulet, items.ice_amulet, items.ice_amulet],

                            [items.life_amulet, items.life_amulet, items.life_amulet,
                             items.life_amulet, items.life_amulet, items.life_amulet],

                            [items.death_amulet, items.death_amulet, items.death_amulet,
                             items.death_amulet, items.death_amulet, items.death_amulet]],

            'Tools': [[items.divining_rod, items.divining_rod, items.divining_rod,
                       items.divining_rod, items.divining_rod, items.divining_rod],

                      [items.shovel, items.shovel, items.shovel,
                       items.shovel, items.shovel, items.shovel],

                      [items.map_of_fast_travel, items.map_of_fast_travel, items.map_of_fast_travel,
                       items.map_of_fast_travel, items.map_of_fast_travel, items.map_of_fast_travel],

                      [items.boots_of_travel, items.boots_of_travel, items.boots_of_travel,
                       items.boots_of_travel, items.boots_of_travel, items.boots_of_travel],

                      [items.wood_lckpck, items.copper_lckpck, items.iron_lckpck, items.steel_lckpck,
                       items.mythril_lckpck, items.mythril_lckpck]]}


def pick_category():
    global inventory
    while True:
        print("""Categories:
      [1] Armor
      [2] Weapons
      [3] Accessories
      [4] Consumables
      [5] Tools
      [6] Quest Items
      [7] Miscellaneous
       |---->[I] Equipped Items
       |---->[C] Coordinates
       |---->[Q] Quests""")
        while True:
            cat = input('Input [#] or [L]etter (or type "exit"): ').lower()

            if cat in ['e', 'x', 'exit', 'b', 'back']:
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
                cat = 'consum'
                vis_cat = 'Consumables'
            elif cat == '5':
                cat = 'tools'
                vis_cat = 'Tools'
            elif cat == '6':
                cat = 'q_items'
                vis_cat = 'Quest Items'
            elif cat == '7':
                cat = 'misc'
                vis_cat = 'Miscellaneous'

            elif cat == 'i':
                cat = 'equipped_items'
                vis_cat = 'Equipped Items'
            elif cat == 'c':
                cat = 'coord'
                vis_cat = 'Coordinates'
            elif cat == 'q':
                cat = 'quests'
                vis_cat = 'Quests'

            else:
                continue

            if cat in inventory:
                if inventory[cat]:
                    if cat not in ['coord', 'weapons', 'armor', 'access']:
                        pick_item(cat, vis_cat)
                        print('-'*25)

                    elif cat == 'coord':
                        print('-'*25)
                        print('Coordinates:\n', '\n'.join(inventory[cat]))
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
                    print('The {0} category is empty.'.format(vis_cat))
                    input("\nPress enter/return ")
                    print('-'*25)
                    break

            elif cat == 'equipped_items':
                pick_item(cat, vis_cat)
                break

            if cat == 'quests' and [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest) and x.started]:
                pick_item(cat, vis_cat)
                break

            else:
                print('-'*25)
                print("Your party has no active or completed quests.")
                input("\nPress enter/return ")
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
                    print(f'{vis_cat}: \n      ', end='')
                    print('\n      '.join([f'[{x + 1}] {y}' for x, y in enumerate(inventory[cat])]))

                else:
                    try:
                        padding = len(max([it.name for it in inventory[cat] if not it.imp], key=len))

                    except ValueError:
                        padding = 1

                    extra_pad = len(str(len([it.name for it in inventory[cat] if not it.imp]) + 1))

                    print('{0}:'.format(vis_cat))

                    for x, y in enumerate([it for it in inventory[cat] if not it.imp]):
                        full_padding = '-'*(padding - len(y.name) + (extra_pad - len(str(x + 1))))
                        print('     ', '      '.join([f"[{x + 1}] {y} {full_padding}--> {y.sell} GP"]))

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

                    if item in ['e', 'x', 'exit', 'b', 'back']:
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
        if (isinstance(item, items.Weapon)
            or isinstance(item, items.Armor)
                or isinstance(item, items.Accessory)):

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
                isinstance(item, items.Accessory),
                isinstance(item, items.Armor),
                isinstance(item, items.Consumable),
                isinstance(item, items.Weapon),
                isinstance(item, items.StatusPotion)
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

                    item.use_item(target)

                    if item not in inventory[cat]:
                        return

                else:
                    print('-'*25)
                    print("Who should {0} the {1}?".format(use_equip.lower(), item.name))
                    print("     ", "\n      ".join([f"[{int(x) + 1}] {y.name}" for x, y in enumerate(target_options)]))

                    while True:
                        target = input('Input [#] (or type "back"): ').lower()

                        try:
                            target = target_options[int(target) - 1]

                        except (ValueError, IndexError):
                            if target in ['e', 'exit', 'x', 'b', 'back']:
                                break

                            continue

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
            print(f'-{str(item).upper()}-')

            if hasattr(item, "ascart"):
                print(ascii_art.item_sprites[item.ascart])

            print(f'"{item.desc}"')
            input("\nPress enter/return ")

        elif action == '3':
            print('-'*25)

            if item.imp:
                print('You cannot dispose of essential items.')
                input("\nPress enter/return ")

            else:
                while True:
                    y_n = input(f'Are you sure you want to get rid of this {str(item)}? | Yes or No: ').lower()

                    if y_n.startswith('y'):
                        input(f'Your party tosses the {str(item)} aside and continues on their journey.')

                        inventory[cat].remove(item)
                        return

                    elif y_n.startswith('n'):
                        print('-'*25)
                        print(f'Your party decide to keep the {str(item)} with them.')
                        input("\nPress enter/return ")

                        break

            print('-'*25)

        elif action in ['e', 'x', 'exit', 'b', 'back']:
            return


def manage_equipped():
    print('-'*25)

    while True:
        target_options = [x for x in [units.player,
                                      units.solou,
                                      units.xoann,
                                      units.adorine,
                                      units.ran_af,
                                      units.parsto,
                                      units.chyme] if x.enabled]

        if len(target_options) == 1:
            target = units.player

        else:
            print("Select Character: ")

            for num, character in enumerate(target_options):
                print("     ", "\n      ".join([f"[{int(num) + 1}] {character.name}"]))

            while True:
                target = input('Input [#] (or type "exit"): ')

                try:
                    target = target_options[int(target) - 1]

                except (IndexError, ValueError):
                    if target in ['e', 'x', 'exit', 'b', 'back']:
                        print('-'*25)

                        return

                    continue

                break

        manage_equipped_2(target)


def manage_equipped_2(target):
    while True:
        p_equip = equipped[target.name if target != units.player else 'player']

        print('-' * 25)
        print(f"""{target.name}'s Equipped Items:
      [1] Weapon ----> {p_equip['weapon']}
      [2] Head ------> {p_equip['head']}
      [3] Body ------> {p_equip['body']}
      [4] Legs ------> {p_equip['legs']}
      [5] Accessory -> {p_equip['access']}""")

        while True:
            selected = input('Input [#] (or type "back"): ')
            selected = selected.lower()

            if selected in ['e', 'x', 'exit', 'b', 'back']:
                print('-' * 25)

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
                print('-' * 25)
                print("You don't have anything equipped in that slot.")
                input("\nPress enter/return ")

                break

            if isinstance(selected, items.Weapon):
                key = 'weapon'

            elif isinstance(selected, items.Accessory):
                key = 'access'

            elif isinstance(selected, items.Armor):
                key = selected.part

            print('-' * 25)

            manage_equipped_3(key, selected, p_equip)


def manage_equipped_3(key, selected, p_equip):
    global equipped

    while True:
        print(f"""What do you want to do with your {str(selected)}?
      [1] Unequip
      [2] Read Description""")

        while True:
            action = input('Input [#] (or type "back"')

            if action == '1':
                if selected.name == 'Fists':
                    print('-' * 25)
                    print("Removing those would be difficult without causing damage.")
                    input("\nPress enter/return ")
                    print('-' * 25)

                    break

                print('-' * 25)
                print(f'You unequip the {selected.name}.')
                input("\nPress enter/return ")

                if isinstance(selected, items.Weapon):
                    inventory[selected.cat].append(p_equip[key])

                    p_equip[key] = items.fists

                elif isinstance(selected, items.Armor):
                    inventory[selected.cat].append(p_equip[key])

                    p_equip[key] = '(None)'

                elif isinstance(selected, items.Accessory):
                    if isinstance(selected, items.ElementAccessory):
                        target.element = 'none'

                        print('You are no longer imbued with the {0} element.'.format(selected.element))
                        input("\nPress enter/return ")

                    inventory[selected.cat].append(p_equip[key])
                    p_equip[key] = '(None)'

                break

            elif action == '2':
                print('-' * 25)

                if hasattr(selected, "ascart"):
                    print(ascii_art.item_sprites[selected.ascart])

                print(selected.desc)
                input("\nPress enter/return ")
                print('-' * 25)

                break

            elif action.lower() in ['e', 'x', 'exit', 'b', 'back']:
                return


def view_quests():
    print('-'*25)
    while True:
        fizz = True
        choice = input('View [f]inished or [a]ctive quests? | Input [Letter] (or type "back"): ').lower()

        print('-' * 25)
        if choice.startswith('f'):  # Finished Quests
            dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest) and x.finished]

        elif choice.startswith('a'):
            dialogue = [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest) and not x.finished and x.started]

        elif choice in ['e', 'x', 'exit', 'b', 'back']:
            return

        else:
            continue

        if dialogue:
            while fizz:
                print(f'{"Finished" if choice.startswith("f") else "Active"}:\n      ', end='')
                print('\n      '.join([f'[{num + 1}] {x.name}' for num, x in enumerate(dialogue)]))

                while True:
                    number = input('Input [#] (or type "back"): ')

                    try:
                        number = int(number) - 1

                    except ValueError:
                        if number.lower() in ['e', 'x', 'exit', 'b', 'back']:
                            fizz = False  # Break the loop twice
                            break

                        else:
                            continue

                    if (number < 0) or (number > len(dialogue) - 1):
                        continue

                    quest = dialogue[number]

                    print('-'*25)
                    print(f"""QUEST NAME: {quest.name}\nGIVEN BY: {quest.q_giver}\n""")
                    print('\n'.join([x for x in quest.desc]))
                    input("\nPress enter/return ")
                    print('-'*25)

                    break

            print('-'*25)

        else:
            print(f'Your party has no {"active" if choice.startswith("a") else "finished"} quests!')
            input('\nPress enter/return ')
            print('-'*25)


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
        print('\n      '.join([f'[{x + 1}] {y}' for x, y in enumerate(available_tools)]))

        while True:
            tool = input('Input [#] (or type "exit"): ')

            try:
                tool = int(tool) - 1

            except ValueError:
                if tool.lower() in ['e', 'x', 'exit', 'b', 'back']:
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
                    x = items.StatusPotion('', '', '', '', '')

                else:
                    x = items.Consumable('', '', '', '')

            elif category == 'weapons':
                x = items.Weapon('', '', '', '', '', '', '', '')

            elif category == 'armor':
                x = items.Armor('', '', '', '', '', '', '', '', '')

            elif category == 'access':
                if item['acc_type'] == 'elemental':
                    x = items.ElementAccessory('', '', '', '', '')

            elif category == 'coord':
                norm_inv[category].append(item)
                continue

            elif category in ['misc', 'tools', 'q_items']:
                if item['name'] == 'Magical Compass':
                    item = items.magic_compass
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Divining Rod':
                    item = items.divining_rod
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Shovel':
                    item = items.shovel
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Map of Fast Travel':
                    item = items.map_of_fast_travel
                    norm_inv[category].append(item)
                    continue

                elif item['name'] == 'Boots of Travel':
                    item = items.boots_of_travel
                    norm_inv[category].append(item)
                    continue

                elif 'Lockpick' in item['name']:
                    if item['power'] == 10:
                        item = items.wood_lckpck

                    elif item['power'] == 30:
                        item = items.copper_lckpck

                    elif item['power'] == 50:
                        item = items.iron_lckpck

                    elif item['power'] == 70:
                        item = items.steel_lckpck

                    elif item['power'] == 90:
                        item = items.mythril_lckpck

                    norm_inv[category].append(item)
                    continue

                else:
                    x = items.Misc('', '', '', '')

            else:
                continue

            if (not isinstance(x, items.Armor) and not isinstance(x, items.Weapon)):

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
                x = items.Weapon('', '', '', '', '', '', '', '')

            elif category == 'access':
                if j_equipped[category]['acc_type'] == 'elemental':
                    x = items.ElementAccessory('', '', '', '', '')

            else:
                x = items.Armor('', '', '', '', '', '', '', '', '')

            x.__dict__ = j_equipped[user][category]
            norm_equip[user][category] = x

    equipped = norm_equip
