# This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
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
from copy import copy as _c

import npcs
import ascii_art
import units
import items
import ItemClass

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

inventory = {'q_items': [], 'consumables': [_c(items.s_potion), _c(items.s_elixir)], 'coord': [],
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
                cat = 'consumables'
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
        if any([isinstance(item, class_) for class_ in [ItemClass.Weapon, ItemClass.Armor, ItemClass.Accessory]]):
            # You equip weapons/armor/accessories
            use_equip = 'Equip'

        else:
            # You use other items
            use_equip = 'Use'

        print('-'*25)
        action = input(f"""What should your party do with the {item}?
      [1] {use_equip}
      [2] Read Description
      [3] Drop
Input [#] (or type "back"): """)

        if action == '1':
            if any([isinstance(item, class_) for class_ in [ItemClass.Accessory,
                                                            ItemClass.Armor,
                                                            ItemClass.Consumable,
                                                            ItemClass.Weapon,
                                                            ItemClass.StatusPotion]]):

                units.player.choose_target(f"Who should {use_equip} the {item.name}?", ally=True, enemy=False)
                item.use_item(units.player.target)

                if item not in inventory[cat]:
                    return

            else:
                item.use_item()
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
                print('Essential Items cannot be thrown away.')
                input("\nPress enter/return ")

            else:
                while True:
                    y_n = input(f'Are you sure your party should get rid of the {item}? | Yes or No: ').lower()

                    if y_n.startswith('y'):
                        print(f'Your party tosses the {item} aside and continues on their journey.')
                        input("\nPress enter/return ")

                        inventory[cat].remove(item)

                        return

                    elif y_n.startswith('n'):
                        print('-'*25)
                        print(f'Your party decide to keep the {item} with them.')
                        input("\nPress enter/return ")

                        break

        elif action in ['e', 'x', 'exit', 'b', 'back']:
            return


def manage_equipped():
    print('-'*25)

    units.player.choose_target("Choose party member to view equipment for:", ally=True, enemy=False)
    manage_equipped_2(units.player.target)


def manage_equipped_2(target):
    while True:
        p_equip = equipped[target.name if target != units.player else 'player']

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
                print(f"{target.name} doesn't have anything equipped in that slot.")
                input("\nPress enter/return ")

                break

            if isinstance(selected, ItemClass.Weapon):
                key = 'weapon'

            elif isinstance(selected, ItemClass.Accessory):
                key = 'access'

            elif isinstance(selected, ItemClass.Armor):
                key = selected.part

            print('-' * 25)
            manage_equipped_3(key, selected, p_equip, target)
            print('-' * 25)

            break


# NEEDS REWORDING
def manage_equipped_3(key, selected, p_equip, target):
    global equipped

    while True:
        print(f"""What should {target.name} do with their {selected}?
      [1] Unequip
      [2] Read Description""")

        while True:
            action = input('Input [#] (or type "back"): ')

            if action == '1':
                if selected.name == 'Fists':
                    print('-' * 25)
                    print("Removing those would be difficult without causing damage.")
                    input("\nPress enter/return ")
                    print('-' * 25)

                    break

                print('-' * 25)
                print(f'{target.name} unequips the {selected.name}.')
                input("\nPress enter/return ")

                if isinstance(selected, ItemClass.Weapon):
                    inventory[selected.cat].append(p_equip[key])

                    p_equip[key] = items.fists

                elif isinstance(selected, ItemClass.Armor):
                    inventory[selected.cat].append(p_equip[key])

                    p_equip[key] = '(None)'

                elif isinstance(selected, ItemClass.Accessory):
                    if isinstance(selected, ItemClass.ElementAccessory):
                        target.element = 'none'

                        print(f'{target.name} is no longer imbued with the {selected.element} element.')
                        input("\nPress enter/return ")

                    inventory[selected.cat].append(p_equip[key])
                    p_equip[key] = '(None)'

                return

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
        y_n = input('Should your party sell the {item.name} for {item.sell} GP? | Yes or No: ').lower()

        if y_n.startswith('y'):
            for num, it in enumerate(inventory[cat]):
                if it.name == item.name:

                    inventory[cat].remove(it)
                    main.party_info['gp'] += item.sell

                    print('Your party hands the shopkeeper their {item.name} and receives {item.sell} GP.')
                    input('\nPress enter/return ')

                    return

        elif y_n.startswith('n'):
            return


def tools_menu():  # Display a set of usable tools on the world map
    tool_names = ['Divining Rod', 'Shovel', 'Magical Compass', 'Map of Fast Travel', 'Boots of Insane Speed']
    available_tools = []

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
        print('-'*25)

        return

    while True:
        print('Tools: \n      ', end='')
        print('\n      '.join([f'[{x + 1}] {y}' for x, y in enumerate(available_tools)]))

        while True:
            tool = input('Input [#] (or type "exit"): ')

            try:
                tool = int(tool) - 1

            except ValueError:
                if tool.lower() in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*25)

                    return

                else:
                    continue

            if (tool < 0) or (tool > len(available_tools) - 1):
                continue

            tool = available_tools[tool]
            tool.use_item(units.player)

            print('-' * 25)

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
            if category == 'consumables':
                if 'Potion of ' in item['name']:
                    x = ItemClass.StatusPotion('', '', '', '', '')

                else:
                    x = ItemClass.Consumable('', '', '', '')

            elif category == 'weapons':
                x = ItemClass.Weapon('', '', '', '', '', '', '', '')

            elif category == 'armor':
                x = ItemClass.Armor('', '', '', '', '', '', '', '', '')

            elif category == 'access':
                if item['acc_type'] == 'elemental':
                    x = ItemClass.ElementAccessory('', '', '', '', '')

                else:
                    continue

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

                elif 'Lockpick' in item['name']:
                    if item['power'] == 30:
                        item = items.wood_lckpck

                    elif item['power'] == 45:
                        item = items.copper_lckpck

                    elif item['power'] == 60:
                        item = items.iron_lckpck

                    elif item['power'] == 75:
                        item = items.steel_lckpck

                    elif item['power'] == 90:
                        item = items.mythril_lckpck

                    norm_inv[category].append(item)
                    continue

                else:
                    x = items.Misc('', '', '', '')

            else:
                continue

            if not isinstance(x, ItemClass.Armor) and not isinstance(x, ItemClass.Weapon):

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
                x = ItemClass.Weapon('', '', '', '', '', '', '', '')

            elif category == 'access':
                if j_equipped[category]['acc_type'] == 'elemental':
                    x = ItemClass.ElementAccessory('', '', '', '', '')

            else:
                x = ItemClass.Armor('', '', '', '', '', '', '', '', '')

            x.__dict__ = j_equipped[user][category]
            norm_equip[user][category] = x

    equipped = norm_equip
