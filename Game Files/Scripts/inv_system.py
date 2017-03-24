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

import json
import sys
from copy import copy as _c

import npcs
import ascii_art
import units
import items
import save_load
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


# noinspection PyUnboundLocalVariable
def pick_category():
    global inventory
    while True:
        print("""Inventory Categories:
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
                        print('-'*save_load.divider_size)

                    elif cat == 'coord':
                        print('-'*save_load.divider_size)
                        print('Coordinates:\n', '\n'.join(inventory[cat]))
                        input("\nPress enter/return ")
                        print('-'*save_load.divider_size)

                    else:
                        if [x for x in inventory[cat]]:
                            pick_item(cat, vis_cat)
                            print('-'*save_load.divider_size)

                        else:
                            print('-'*save_load.divider_size)
                            print(f'The {vis_cat} category is empty.')
                            input("\nPress enter/return ")
                            print('-'*save_load.divider_size)

                    break

                else:
                    print('-'*save_load.divider_size)
                    print(f'The {vis_cat} category is empty.')
                    input("\nPress enter/return ")
                    print('-'*save_load.divider_size)
                    break

            elif cat == 'equipped_items':
                pick_item(cat, vis_cat)
                break

            if cat == 'quests' and [x for x in npcs.all_dialogue if isinstance(x, npcs.Quest) and x.started]:
                pick_item(cat, vis_cat)
                break

            else:
                print('-'*save_load.divider_size)
                print("Your party has no active or completed quests.")
                input("\nPress enter/return ")
                print('-'*save_load.divider_size)
                break


def pick_item(cat, vis_cat, gs=False):  # Select an object to interact with in your inventory
    # If "gs == True" that means that items are being sold, and not used.
    while cat in ['quests', 'equipped_items'] or inventory[cat]:
        if cat == 'quests':
            view_quests()
            return

        if cat == 'equipped_items':
            manage_equipped()
            return

        if inventory[cat]:
            print('-'*save_load.divider_size)
            if not gs:
                print(f"{vis_cat}: ")
                for x, y in enumerate(inventory[cat]):
                    print(f'      [{x + 1}] {y}')

            else:
                try:
                    padding = len(max([it.name for it in inventory[cat] if not it.imp], key=len))

                except ValueError:
                    padding = 1

                extra_pad = len(str(len([it.name for it in inventory[cat] if not it.imp]) + 1))

                print(f'{vis_cat}:')

                for x, y in enumerate([it for it in inventory[cat] if not it.imp]):
                    full_padding = '-'*(padding - len(y.name) + (extra_pad - len(str(x + 1))))
                    print('     ', '      '.join([f"[{x + 1}] {y} {full_padding}--> {y.sell} GP"]))

        else:
            return

        while True:
            item = input('Input [#] (or type "back"): ').lower()

            try:
                if gs:
                    sell_item(cat, [x for x in inventory[cat] if not x.imp][int(item) - 1])

                else:
                    pick_action(cat, inventory[cat][int(item) - 1])

            except (IndexError, ValueError):
                if item in ['e', 'x', 'exit', 'b', 'back']:
                    return

                continue

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

        print('-'*save_load.divider_size)
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
            print('-'*save_load.divider_size)
            print(f'-{str(item).upper()}-')

            if hasattr(item, "ascart"):
                print(ascii_art.item_sprites[item.ascart])

            print(f'"{item.desc}"')
            input("\nPress enter/return ")

        elif action == '3':
            print('-'*save_load.divider_size)

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
                        print('-'*save_load.divider_size)
                        print(f'Your party decide to keep the {item} with them.')
                        input("\nPress enter/return ")

                        break

        elif action in ['e', 'x', 'exit', 'b', 'back']:
            return


def manage_equipped():
    units.player.choose_target("Choose party member to view equipment for:", ally=True, enemy=False)
    manage_equipped_2(units.player.target)


def manage_equipped_2(target):
    print('-'*save_load.divider_size)
    while True:
        p_equip = equipped[target.name if target != units.player else 'player']

        print(f"""{target.name}'s Equipped Items:
      [1] Weapon ----> {p_equip['weapon']}
      [2] Head ------> {p_equip['head']}
      [3] Body ------> {p_equip['body']}
      [4] Legs ------> {p_equip['legs']}
      [5] Accessory -> {p_equip['access']}""")

        while True:
            selected = input('Input [#] (or type "back"): ').lower()

            if selected in ['e', 'x', 'exit', 'b', 'back']:
                print('-'*save_load.divider_size)
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
                print('-'*save_load.divider_size)
                print(f"{target.name} doesn't have anything equipped in that slot.")
                input("\nPress enter/return ")

                break

            if isinstance(selected, ItemClass.Weapon):
                key = 'weapon'

            elif isinstance(selected, ItemClass.Accessory):
                key = 'access'

            elif isinstance(selected, ItemClass.Armor):
                key = selected.part

            else:
                continue

            print('-'*save_load.divider_size)
            manage_equipped_3(key, selected, p_equip, target)
            print('-'*save_load.divider_size)

            break


def manage_equipped_3(key, selected, p_equip, target):
    global equipped

    while True:
        print(f"""What should {target.name} do with their {selected}?
      [1] Unequip
      [2] Read Description""")

        while True:
            action = input('Input [#] (or type "back"): ').lower()

            if action == '1':
                if selected.name == 'Fists':
                    print('-'*save_load.divider_size)
                    print("Removing those would be difficult without causing damage.")
                    input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    break

                print('-'*save_load.divider_size)
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
                print('-'*save_load.divider_size)

                if hasattr(selected, "ascart"):
                    print(ascii_art.item_sprites[selected.ascart])

                print(selected.desc)
                input("\nPress enter/return ")
                print('-'*save_load.divider_size)

                break

            elif action in ['e', 'x', 'exit', 'b', 'back']:
                return


def view_quests():
    print('-'*save_load.divider_size)
    while True:
        fizz = True
        choice = input('View [f]inished or [a]ctive quests? | Input [Letter] (or type "back"): ').lower()

        print('-'*save_load.divider_size)
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
                if choice.startswith("f"):
                    print("Finished:")

                else:
                    print("Active:")

                for num, x in enumerate(dialogue):
                    print(f'      [{num + 1}] {x.name}')

                while True:
                    quest = input('Input [#] (or type "back"): ').lower()

                    try:
                        quest = dialogue[int(quest) - 1]

                    except (IndexError, ValueError):
                        if quest in ['e', 'x', 'exit', 'b', 'back']:
                            fizz = False  # Break the loop twice
                            break

                        continue

                    print('-'*save_load.divider_size)
                    print(f"QUEST NAME: {quest.name}")
                    print(f"GIVEN BY: {quest.q_giver}")

                    for x in quest.desc:
                        print(x)

                    input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    break

            print('-'*save_load.divider_size)

        else:
            print(f'Your party has no {"active" if choice.startswith("a") else "finished"} quests!')
            input('\nPress enter/return ')
            print('-'*save_load.divider_size)


def sell_item(cat, item):  # Trade player-owned objects for money (GP)
    print('-'*save_load.divider_size)

    if hasattr(item, "ascart"):
        print(ascii_art.item_sprites[item.ascart])

    print(item.desc)
    print('-'*save_load.divider_size)
    while True:
        y_n = input(f'Should your party sell the {item.name} for {item.sell} GP? | Yes or No: ').lower()

        if y_n.startswith('y'):
            for num, it in enumerate(inventory[cat]):
                if it.name == item.name:

                    inventory[cat].remove(it)
                    main.party_info['gp'] += item.sell

                    print(f'Your party hands the shopkeeper their {item.name} and receives {item.sell} GP.')
                    input('\nPress enter/return ')

                    return

        elif y_n.startswith('n'):
            return


def serialize_inv(path):
    j_inventory = {}

    for category in inventory:
        j_inventory[category] = []

        for item in inventory[category]:
            if category != 'coord':
                j_inventory[category].append(item.item_id)

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

        for item_id in j_inventory[category]:
            if category == 'coord':
                norm_inv[category].append(item_id)
                continue

            else:
                norm_inv[category].append(_c(items.find_item_with_id(item_id)))

    inventory = norm_inv


def serialize_equip(path):
    j_equipped = {}

    for user in equipped:
        j_equipped[user] = {}
        for category in equipped[user]:
            if equipped[user][category] != '(None)':
                j_equipped[user][category] = equipped[user][category].item_id

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

            else:
                norm_equip[user][category] = _c(items.find_item_with_id(j_equipped[user][category]))

    equipped = norm_equip
