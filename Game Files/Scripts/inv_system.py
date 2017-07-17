# This file is part of Peasants' Ascension.
#
# Peasants' Ascension is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peasants' Ascension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

import json
import sys
from copy import copy as _c

import ascii_art
import dialogue
import items
import save_load
import units
import ItemClass

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

inventory = {'q_items': [],
             'consumables': [_c(items.s_potion), _c(items.s_elixir)],
             'coord': [],
             'weapons': [],
             'armor': [],
             'tools': [],
             'misc': [],
             'access': []}

equipped = {
    'player': {
        'weapon': _c(items.fists),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': _c(items.no_access)
    },

    'Solou': {
        'weapon': _c(items.mag_twg),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': _c(items.no_access)
    },

    'Xoann': {
        'weapon': _c(items.stn_dag),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': _c(items.no_access)
    },

    'Parsto': {
        'weapon': _c(items.slg_sht),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': _c(items.no_access)
    },

    'Adorine': {
        'weapon': _c(items.wdn_sht),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': _c(items.no_access)
    },

    'Chyme': {
        'weapon': _c(items.rbr_mlt),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': _c(items.no_access)
    },

    "Ran'Af": {
        'weapon': _c(items.fists),
        'head': _c(items.straw_hat),
        'body': _c(items.cotton_shirt),
        'legs': _c(items.sunday_trousers),
        'access': _c(items.no_access)
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
            cat = main.s_input('Input [#] or [L]etter (or type "exit"): ').lower()

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
                        print('Coordinates: ')

                        for item in inventory[cat]:
                            print(item)

                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)

                    else:
                        if [x for x in inventory[cat]]:
                            pick_item(cat, vis_cat)
                            print('-'*save_load.divider_size)

                        else:
                            print('-'*save_load.divider_size)
                            print(f'The {vis_cat} category is empty.')
                            main.s_input("\nPress enter/return ")
                            print('-'*save_load.divider_size)

                    break

                else:
                    print('-'*save_load.divider_size)
                    print(f'The {vis_cat} category is empty.')
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)
                    break

            elif cat == 'equipped_items':
                pick_item(cat, vis_cat)
                break

            if cat == 'quests' and [x for x in dialogue.all_dialogue if isinstance(x, dialogue.Quest) and x.started]:
                pick_item(cat, vis_cat)
                break

            else:
                print('-'*save_load.divider_size)
                print("Your party has no active or completed quests.")
                main.s_input("\nPress enter/return ")
                print('-'*save_load.divider_size)
                break


# Select an object to interact with in your inventory
# If "gs == True" that means that items are being sold, and not used.
def pick_item(cat, vis_cat, gs=False):
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
                    print(f'      [{x + 1}] {y.name}')

            else:
                try:
                    padding = len(max([it.name for it in inventory[cat] if not it.imp], key=len))

                except ValueError:
                    padding = 1

                extra_pad = len(str(len([it.name for it in inventory[cat] if not it.imp]) + 1))

                print(f'{vis_cat}:')

                for x, y in enumerate([it for it in inventory[cat] if not it.imp]):
                    full_padding = '-'*(padding - len(y.name) + (extra_pad - len(str(x + 1))))
                    print(f"      [{x + 1}] {y.name} {full_padding}--> {y.sell} GP")

        else:
            return

        while True:
            item = main.s_input('Input [#] (or type "back"): ').lower()

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
        action = main.s_input(f"""What should your party do with the {item.name}?
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
            print(f'-{str(item.name).upper()}-')

            if hasattr(item, "ascart"):
                print(ascii_art.item_sprites[item.ascart])

            print(f'"{item.desc}"')
            main.s_input("\nPress enter/return ")

        elif action == '3':
            print('-'*save_load.divider_size)

            if item.imp:
                print('Essential Items cannot be thrown away.')
                main.s_input("\nPress enter/return ")

            else:
                while True:
                    y_n = main.s_input(f'Are you sure your party should get rid of the {item.name}? | Y/N: ').lower()

                    if y_n.startswith('y'):
                        print(f'Your party tosses the {item.name} aside and continues on their journey.')
                        main.s_input("\nPress enter/return ")

                        inventory[cat].remove(item)

                        return

                    elif y_n.startswith('n'):
                        print('-'*save_load.divider_size)
                        print(f'Your party decide to keep the {item.name} with them.')
                        main.s_input("\nPress enter/return ")

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
      [1] Weapon ----> {p_equip['weapon'].name}
      [2] Head ------> {p_equip['head'].name}
      [3] Body ------> {p_equip['body'].name}
      [4] Legs ------> {p_equip['legs'].name}
      [5] Accessory -> {p_equip['access'].name}""")

        while True:
            selected = main.s_input('Input [#] (or type "back"): ').lower()

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

            if selected.item_id in ["no_head",
                                    "no_body",
                                    "no_legs",
                                    "no_access"]:

                print('-'*save_load.divider_size)
                print(f"{target.name} doesn't have anything equipped in that slot.")
                main.s_input("\nPress enter/return ")

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
        print(f"""What should {target.name} do with their {selected.name}?
      [1] Unequip
      [2] Read Description""")

        while True:
            action = main.s_input('Input [#] (or type "back"): ').lower()

            if action == '1':
                if selected.item_id == "weapon_fists":
                    print('-'*save_load.divider_size)
                    print("Removing those would be difficult without causing damage.")
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    break

                else:
                    unequip_item(selected.item_id, target)
                    print('-'*save_load.divider_size)
                    print(f'{target.name} unequips the {selected.name}.')
                    main.s_input("\nPress enter/return ")

                return

            elif action == '2':
                print('-'*save_load.divider_size)

                if hasattr(selected, "ascart"):
                    print(ascii_art.item_sprites[selected.ascart])

                print(selected.desc)
                main.s_input("\nPress enter/return ")
                print('-'*save_load.divider_size)

                break

            elif action in ['e', 'x', 'exit', 'b', 'back']:
                return


def view_quests():
    print('-'*save_load.divider_size)
    while True:
        fizz = True
        choice = main.s_input('View [f]inished or [a]ctive quests? | Input [Letter] (or type "back"): ').lower()

        print('-'*save_load.divider_size)
        if choice.startswith('f'):  # Finished Quests
            dia_ = [x for x in dialogue.all_dialogue if isinstance(x, dialogue.Quest) and x.finished]

        elif choice.startswith('a'):
            dia_ = [x for x in dialogue.all_dialogue if isinstance(x, dialogue.Quest) and not x.finished and x.started]

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
                    quest = main.s_input('Input [#] (or type "back"): ').lower()

                    try:
                        quest = dia_[int(quest) - 1]

                    except (IndexError, ValueError):
                        if quest in ['e', 'x', 'exit', 'b', 'back']:
                            fizz = False  # Break the loop twice
                            break

                        continue

                    print('-'*save_load.divider_size)
                    print(f"QUEST NAME: {quest.name}")
                    print(f"GIVEN BY: {quest.q_giver}")

                    for x in main.chop_by_79(quest.dialogue):
                        print(x)

                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    break

            print('-'*save_load.divider_size)

        else:
            print(f'Your party has no {"active" if choice.startswith("a") else "finished"} quests!')
            main.s_input('\nPress enter/return ')
            print('-'*save_load.divider_size)


# Trade player-owned objects for money (GP)
def sell_item(cat, item):
    print('-'*save_load.divider_size)

    if hasattr(item, "ascart"):
        print(ascii_art.item_sprites[item.ascart])

    print(item.desc)
    print('-'*save_load.divider_size)

    while True:
        y_n = main.s_input(f'Should your party sell the {item.name} for {item.sell} GP? | Y/N: ').lower()

        if y_n.startswith('y'):
            for num, it in enumerate(inventory[cat]):
                if it.name == item.name:

                    inventory[cat].remove(it)
                    main.party_info['gp'] += item.sell

                    print(f'Your party hands the shopkeeper their {item.name} and receives {item.sell} GP.')
                    main.s_input('\nPress enter/return ')

                    return

        elif y_n.startswith('n'):
            return


# Searches the all_items list, and returns the item that has the given item_id.
# If it can't find anything, it returns False (this shouldn't ever happen in this game, but could be
# useful if someone else is making something with this engine)
def find_item_with_id(item_id):
    for x in items.all_items:
        if x.item_id == item_id:
            return x

    return False


# Utilizes find_item_with_id() to add a specific item to the player's inventory
def add_item(item_id):
    global inventory

    this_item = _c(find_item_with_id(item_id))
    inventory[this_item.cat].append(this_item)


# Same as add_item(), but removes the item from the inventory instead.
# Returns True if the item in question is actually in the player's inventory, otherwise it returns False.
def remove_item(item_id):
    global inventory

    this_item = _c(find_item_with_id(item_id))

    for z in inventory[this_item.cat]:
        if z.item_id == z.item_id:
            inventory[this_item.cat].remove(z)
            return True

    return False


# Utilizes add_item() and remove_item() to equip/unequip items, and remove/add them to the inventory
def equip_item(item_id, equipper):
    global equipped

    this_item = _c(find_item_with_id(item_id))
    inv_name = equipper.name if equipper != units.player else 'player'

    if isinstance(equipped[inv_name][this_item.part], ItemClass.Item):
        if equipped[inv_name][this_item.part].item_id not in ["weapon_fist"
                                                              "no_head",
                                                              "no_body",
                                                              "no_legs",
                                                              "no_access"]:

            add_item(equipped[inv_name][this_item.part].item_id)

    remove_item(item_id)
    equipped[inv_name][this_item.part] = this_item


def unequip_item(item_id, unequipper):
    global equipped

    this_item = _c(find_item_with_id(item_id))
    inv_name = unequipper.name if unequipper != units.player else 'player'
    add_item(this_item.item_id)

    if this_item.part == 'weapon':
        equip_item("weapon_fist", unequipper)
    if this_item.part == 'head':
        equip_item("no_head", unequipper)
    if this_item.part == 'body':
        equip_item("no_body", unequipper)
    if this_item.part == 'legs':
        equip_item("no_legs", unequipper)
    if this_item.part == 'access':
        equip_item("no_access", unequipper)


# Makes a dictionary with the item_id's of all items in their respective categories,
# then saves it to a .json file. Used when saving the game.
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


# Converts the above dictionary into the actual inventory, by swapping out each item_id for the
# items they belong to. Used when loading the game.
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
                norm_inv[category].append(_c(find_item_with_id(item_id)))

    inventory = norm_inv


# Identical to serialize_inv(), but specifically for the player's equipped items
# which are not stored in the inventory.
def serialize_equip(path):
    j_equipped = {}

    for user in equipped:
        j_equipped[user] = {}
        for category in equipped[user]:
            j_equipped[user][category] = equipped[user][category].item_id

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_equipped, f, indent=4, separators=(', ', ': '))


# Identical to deserialize_inv(), but specifically for the player's equipped items
# which are not stored in the inventory.
def deserialize_equip(path):
    global equipped
    norm_equip = {}

    with open(path, encoding='utf-8') as f:
        j_equipped = json.load(f)

    for user in j_equipped:
        norm_equip[user] = {}

        for category in j_equipped[user]:
            norm_equip[user][category] = _c(find_item_with_id(j_equipped[user][category]))

    equipped = norm_equip


# Checks to make sure all items in items.all_items have a unique item_id
for item1 in items.all_items:
    if find_item_with_id(item1.item_id) != item1:
        print(f"{item1.item_id} doesn't have a unique item_id!")
