#   This file is part of Peasants' Ascension.
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
import os
import random
import sys
import multiprocessing
from copy import copy as _c

import pygame

import ascii_art
import dialogue
import save_load
import sounds
import tiles
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

acquired_gems = []


class Item:
    # The basic item class. Items are stored in the "inventory" dictionary. All
    # item-subclasses inherit from this class.
    def __init__(self, name, desc, value, item_id, imp, ascart, cat):
        self.name = name
        self.desc = desc
        self.value = value
        self.imp = imp
        self.ascart = ascart
        self.cat = cat
        self.item_id = item_id

        try:
            assert self.ascart in ascii_art.item_sprites

        except AssertionError:
            raise Exception(f"{self.item_id} has invalid ascii art!")

    def use_item(self, user):
        print("You can't use this right now.")

        if main.party_info['gamestate'] != 'battle':
            main.s_input("\nPress enter/return ")


class Consumable(Item):
    # Items that are removed from your inventory after use. Includes Potions, Armor, Weapons, etc.
    # By definition these items are not considered "important", and can be freely sold and thrown away
    def __init__(self, name, desc, value, item_id, ascart, cat):
        super().__init__(name, desc, value, item_id, False, ascart, cat)


class NonConsumable(Item):
    # Items that remain in your inventory after use. Includes tools, ingredients
    def __init__(self, name, desc, value, item_id, imp, ascart, cat):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)


class HealthManaPotion(Consumable):
    # Items that restore your HP, MP, or both
    def __init__(self, name, desc, value, item_id, cat='consumables', heal=0, mana=0, ascart='Potion'):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.heal = heal
        self.mana = mana

    def use_item(self, user):
        print(f'{user.name} consumes the {self.name}...')

        main.smart_sleep(0.75)
        sounds.magic_healing.play()

        if self.heal > 0:
            user.hp += self.heal
            print(f"{user.name} restored {self.heal} HP with the {self.name}!")

        if self.mana > 0:
            user.mp += self.mana
            print(f"{user.name} restored {self.mana} MP with the {self.name}!")

        units.fix_stats()

        if main.party_info['gamestate'] != 'battle':
            main.s_input("\nPress enter/return ")

        remove_item(self.item_id)


class StatusPotion(Consumable):
    def __init__(self, name, desc, value, status, item_id, ascart='Status', cat='consumables'):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.status = status

    def use_item(self, user):
        if self.status in user.status_ail:
            sounds.buff_spell.play()
            user.status_ail = [x for x in user.status_ail if x != self.status]

            print(f'{user.name} consumes the {self.name}...')
            main.smart_sleep(0.75)
            sounds.magic_healing.play()

            print(f"{user.name} is no longer {self.status}!")

            if main.party_info['gamestate'] != 'battle':
                main.s_input("\nPress enter/return ")

            remove_item(self.item_id)

        else:
            print(f"Drinking this {self.name} probably wouldn't do anything.")
            main.s_input("\nPress enter/return ")


class AttractPotion(Consumable):
    def __init__(self, name, desc, value, num_steps, m_count, item_id, ascart="Alchemy", cat="consumables"):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.num_steps = num_steps
        self.m_count = m_count


class RepelPotion(Consumable):
    def __init__(self, name, desc, value, num_steps, item_id, ascart="Alchemy", cat="consumables"):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.num_steps = num_steps


class BombPotion(Consumable):
    def __init__(self, name, desc, value, multitarget, damage, item_id, ascart="Alchemy", cat="consumables"):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.multitarget = multitarget
        self.damage = damage


class XPGoldPotion(Consumable):
    def __init__(self, name, desc, value, gold_change, xp_change, item_id, ascart="Alchemy", cat="consumables"):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.gold_change = gold_change
        self.xp_change = xp_change


class GameCrashPotion(Consumable):
    def __init__(self, name, desc, value, item_id, ascart="Alchemy", cat="consumables"):
        super().__init__(name, desc, value, item_id, ascart, cat)

    def use_item(self, user):
        raise Exception("I told you this would crash the game.")


class Weapon(Consumable):
    # Items that increase your damage by a percentage.
    def __init__(self, name, desc, value, power, type_, class_, ascart, item_id, element='neutral', cat='weapons'):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.power = power
        self.type_ = type_
        self.class_ = class_
        self.element = element
        self.part = 'weapon'

        if self.class_:
            classes = ' and '.join([f"{x.title()}s" for x in self.class_])
            self.class_req = f"\nOnly equippable by {classes}."

        else:
            self.class_req = "\nEquippable by any class."

        self.desc = f"{desc} {self.class_req}"

    def use_item(self, user):
        if user.class_ in self.class_ or not self.class_:
            equip_item(self.item_id, user)

            print(f'{user.name} equips the {self.name}.')
            main.s_input("\nPress enter/return ")

        else:
            print(f"This {self.name} is f{self.class_req[3:]}.")

            main.s_input("\nPress enter/return ")


class Armor(Consumable):
    # Items that give the player a percent increase in defense when hit.
    def __init__(self, name, desc, value, defense, part, class_, ascart, item_id, cat='armor'):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.defense = defense
        self.part = part
        self.class_ = class_

        if self.class_:
            classes = ' and '.join([f"{x.title()}s" for x in self.class_])
            self.class_req = f"\nOnly equippable by {classes}."

        else:
            self.class_req = "\nEquippable by any class."

        self.desc = f"{desc} {self.class_req}"

    def use_item(self, user):
        if user.class_ in self.class_ or not self.class_:
            equip_item(self.item_id, user)
            print(f'{user.name} equips the {self.name}.')
            main.s_input("\nPress enter/return ")

        else:
            print(f"This {self.name} is f{self.class_req[3:]}.")

            main.s_input("\nPress enter/return ")


class Accessory(Consumable):
    def __init__(self, name, desc, value, item_id, ascart='Amulet', cat='access'):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.part = 'access'


class ElementAccessory(Accessory):
    # Gives the player an element used when taking damage
    def __init__(self, name, desc, value, def_element, item_id, ascart='Amulet', cat='access'):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.def_element = def_element

    def use_item(self, user):
        equip_item(self.item_id, user)
        user.def_element = self.def_element

        print(f'{user.name} equips the {self.name}. Their element is now set to {self.def_element}.')
        main.s_input("\nPress enter/return ")


class ActionAccessory(Consumable):
    def __init__(self, name, desc, value, class_, ap_gain, item_id, ascart='Amulet', cat='access'):
        super().__init__(name, desc, value, item_id, ascart, cat)
        self.class_ = class_
        self.ap_gain = ap_gain


class Shovel(NonConsumable):
    def __init__(self, name, desc, value, item_id, cat='tools', imp=True, ascart='Shovel'):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)

    def use_item(self, user):
        if main.party_info['gamestate'] == 'town':
            print("What, here? You can't just start digging up a town!")
            main.s_input("\nPress enter/return")
            return

        print("Digging...")
        sounds.foot_steps.play()
        main.smart_sleep(1)

        print("Digging...")
        sounds.foot_steps.play()
        main.smart_sleep(1)

        print("Still digging...")
        sounds.foot_steps.play()
        main.smart_sleep(1)

        try:
            c_gem = [x for x in main.party_info['current_tile'].gem_list if x.item_id not in acquired_gems][0]

        except IndexError:
            c_gem = None

        if c_gem:
            sounds.unlock_chest.play()
            print(f"Aha, your party found a {c_gem.name}! Might be a good idea to sell it.")
            main.s_input("\nPress enter/return ")

            acquired_gems.append(c_gem.item_id)
            add_item(c_gem.item_id)

        else:
            print("No luck, your party didn't find anything.")
            main.s_input("\nPress enter/return ")


class FastTravelAtlas(NonConsumable):
    def __init__(self, name, desc, value, item_id, cat='tools', imp=True, ascart='Map'):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)

    def use_item(self, user):
        if main.party_info['gamestate'] == 'town':
            print("Fast Travel Atlases can't be used in towns.")
            main.s_input("\nPress enter/return")
            return

        self.choose_prov()

    def choose_prov(self):
        avail_provs = tiles.all_provinces[:main.party_info['map_pow']]

        if len(avail_provs) == 1:
            self.choose_cell(avail_provs[0])

            return

        while True:
            print(f"Available Provinces [Pages: {main.party_info['map_pow']}]: ")
            for num, x in enumerate(avail_provs):
                print(f"      [{num + 1}] {x.name}")

            while True:
                chosen = main.s_input('Input [#] (or type "exit"): ')

                try:
                    chosen = avail_provs[int(chosen) - 1]

                except (IndexError, ValueError):
                    if chosen in ['e', 'x', 'exit', 'b', 'back']:
                        print('-'*save_load.divider_size)
                        return False

                    continue

                print('-' * save_load.divider_size)
                self.choose_cell(chosen)

                return

    @staticmethod
    def choose_cell(prov):
        while True:
            print(f"{prov.name} Province Locations: ")
            for num, x in enumerate(prov.cells):
                print(f"      [{num + 1}] {x.name}")

            do_loop = True
            while do_loop:
                chosen = main.s_input('Input [#] (or type "back"): ')

                try:
                    chosen = prov.cells[int(chosen) - 1]

                except (IndexError, ValueError):
                    if chosen in ['e', 'x', 'exit', 'b', 'back']:
                        print('-' * save_load.divider_size)
                        return

                    continue

                print("-"*save_load.divider_size)
                while True:
                    y_n = main.s_input(f"Warp to {chosen.name}? | Yes or No: ").lower()

                    if y_n.startswith('y'):
                        if 'has_teleported' not in main.party_info:
                            main.party_info['has_teleported'] = False

                        if main.party_info['has_teleported']:
                            print("-"*save_load.divider_size)
                            print("Your party peers into the Fast Travel Atlas and begins to phase out of reality")
                            print("Upon waking you're exactly where you wanted to be.")
                            main.s_input("\nPress enter/return ")

                        else:
                            print("-"*save_load.divider_size)
                            print("You begin to feel strange - your body feels light and all you hear is silence.")
                            print("Your vision starts going blank... All of your senses quickly turning off until")
                            print("you're left with nothing but your thoughts...")
                            main.s_input("\nPress enter/return ")
                            print("...")
                            main.smart_sleep(1)
                            print("...")
                            main.smart_sleep(1)
                            print("...")
                            main.smart_sleep(1)
                            sounds.enemy_hit.play()
                            print("CRASH! Your senses re-emerge you've landed on your back... Oh, you're exactly where")
                            print("you teleported to!")
                            main.s_input("\nPress enter/return ")
                            print("-"*save_load.divider_size)

                        main.party_info['has_teleported'] = True
                        main.party_info['prov'] = prov.name
                        main.party_info['biome'] = chosen.biome
                        main.party_info['current_tile'] = chosen.primary_tile
                        main.check_region()

                        return

                    if y_n.startswith('n'):
                        print('-'*save_load.divider_size)
                        do_loop = False

                        break


class LockpickKit(NonConsumable):
    def __init__(self, name, desc, value, power, item_id, imp=False, ascart='Lockpick', cat='tools'):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)
        self.power = power


class MonsterEncyclopedia(NonConsumable):
    def __init__(self, name, desc, value, item_id, cat='tools', imp=False, ascart='Book'):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)

    def use_item(self, user):
        if main.party_info['gamestate'] == 'battle':
            m_w = {'fire': 'water',
                   'water': 'electric',
                   'electric': 'earth',
                   'earth': 'wind',
                   'wind': 'grass',
                   'grass': 'ice',
                   'ice': 'fire',
                   'neutral': 'neutral',
                   'light': 'dark',
                   'dark': 'light'}[user.target.def_element]

            print(f"""{user.target.name.upper()}'s STATS:
Physical: {user.target.attk} Attack / {user.target.dfns} Defense
Magical: {user.target.m_attk} Attack / {user.target.m_dfns} Defense
Piercing: {user.target.p_attk} Attack / {user.target.p_dfns} Defense
Speed: {user.target.spd}
Evasion: {user.target.evad}
Elements: Attacks are {user.target.def_element.title()} / Defense is {user.target.off_element.title()} / \
Weak to {m_w.title()}""")

        else:
            print("This feature doesn't work yet, sorry :(")
            main.s_input("\nPress enter/return ")


class PocketAlchemyLab(NonConsumable):
    def __init__(self, name, desc, value, item_id, cat='tools', imp=False, ascart='alchemy_kit'):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)

    def use_item(self, user):
        chosen_ingredients = []
        available_flavors = {}

        for item in inventory['misc']:
            if isinstance(item, Ingredient):
                if item.flavor in available_flavors:
                    available_flavors[item.flavor].append(item)

                else:
                    available_flavors[item.flavor] = [item]

        if not (available_flavors and len([val for lst in available_flavors.values() for val in lst]) >= 3):
            print("You need at least three flavors to make a potion!")
            main.s_input("\nPress enter/return ")

            return

        while len(chosen_ingredients) != 3:
            available_flavors = {}

            for item in inventory['misc']:
                if isinstance(item, Ingredient):
                    if item.flavor in available_flavors:
                        available_flavors[item.flavor].append(item)

                    else:
                        available_flavors[item.flavor] = [item]

            print("Flavors in your inventory: ")

            list_flavors = sorted(list(available_flavors.keys()))

            for num, flavor in enumerate(list_flavors):
                print(f"      [{num + 1}] {flavor.title()}")

            while True:
                chosen = main.s_input('Input [#] (or type "exit"): ').lower()

                try:
                    chosen = available_flavors[list_flavors[int(chosen) - 1]]

                except (IndexError, ValueError):
                    if chosen in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    continue

                chosen_ingredient = self.choose_ingredients(chosen)
                chosen_ingredients.append(chosen_ingredient)

                print('-' * save_load.divider_size)
                print(f"Added a {chosen_ingredient.name} to the mix.")

                if len(chosen_ingredients) != 3:
                    print(f"{3 - len(chosen_ingredients)} ingredients remaining!")

                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                else:
                    print("All ingredients added! Time to start brewing!")
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                break

        self.make_potion(chosen_ingredients)

    @staticmethod
    def choose_ingredients(ingredients):
        print('-'*save_load.divider_size)
        print(f"'{ingredients[0].flavor.title()}' Ingredients: ")

        for num, ingredient in enumerate(ingredients):
            print(f"      [{num + 1}] {ingredient.name}")

        while True:
            chosen = main.s_input("Input [#]: ")

            try:
                chosen = ingredients[int(chosen) - 1]

            except (IndexError, ValueError):
                continue

            remove_item(chosen.item_id)

            return chosen

    @staticmethod
    def make_potion(ingredients):
        flavor_map = {
            "strange": [attract_potion_1, attract_potion_2, attract_potion_3],
            "mystic": [repel_potion_1, repel_potion_2, repel_potion_3],
            "rigid": [missile_potion_1, missile_potion_2, missile_potion_3],
            "flowing": [grenade_potion_1, grenade_potion_2, grenade_potion_3],
            "dark": [greed_potion_1, greed_potion_2, greed_potion_3],
            "natural": [temperance_potion_1, temperance_potion_2, temperance_potion_3],
            "mathematical": [gamecrash_potion, gamecrash_potion, gamecrash_potion]
        }

        added_flavors = [ing.flavor for ing in ingredients]
        chosen_flavor = random.choice(added_flavors)
        chosen_power = added_flavors.count(chosen_flavor)
        chosen_potion = flavor_map[chosen_flavor][chosen_power - 1]

        print("Brewing...")
        sounds.potion_brew.play()
        main.smart_sleep(1)
        print("Brewing...")
        sounds.potion_brew.play()
        main.smart_sleep(1)
        print("Brewing...")
        sounds.potion_brew.play()
        main.smart_sleep(1)

        sounds.unlock_chest.play()
        add_item(chosen_potion.item_id)
        print(f"Success! You brewed a {chosen_potion.name}!")
        main.s_input("\nPress enter/return ")


class MusicBox(NonConsumable):
    def __init__(self, name, desc, value, item_id, cat='tools', imp=False, ascart='Book'):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)

    def use_item(self, user):
        print(f"Musicbox is currently {'on' if main.party_info['musicbox_isplaying'] else 'off'}")
        print(f"Musicbox is set to {main.party_info['musicbox_mode']}")

        if main.party_info['musicbox_folder']:
            print(f"Musicbox is set to play music from {main.party_info['musicbox_folder']}/")

        else:
            print("Musicbox does not have a directory set")

        self.choose_option()

    def choose_option(self):
        print("-"*save_load.divider_size)
        while True:
            print("What should you do with the Musicbox?")
            print(f"      [1] Turn {'off' if main.party_info['musicbox_isplaying'] else 'on'}")
            print("      [2] Change play order")
            print("      [3] Set music directory")

            while True:
                chosen = main.s_input('Input [#] (or type "exit"): ')

                if chosen == '1':
                    if main.party_info['musicbox_folder']:
                        main.party_info['musicbox_isplaying'] = not main.party_info['musicbox_isplaying']

                        if main.party_info['musicbox_isplaying']:
                            pygame.mixer.music.stop()
                            self.create_process()
                            main.party_info['musicbox_process'].start()

                        else:
                            main.party_info['musicbox_process'].terminate()
                            pygame.mixer.music.play(-1)

                        print("-"*save_load.divider_size)
                        print(f"You turn {'on' if main.party_info['musicbox_isplaying'] else 'off'} the musicbox")
                        main.s_input("\nPress enter/return ")
                        print("-"*save_load.divider_size)

                        break

                    else:
                        print("-"*save_load.divider_size)
                        print("You need to set a music directory first!")
                        main.s_input("\nPress enter/return ")
                        print("-"*save_load.divider_size)

                        break

                elif chosen == '2':
                    print("-"*save_load.divider_size)
                    self.play_order()
                    print("-"*save_load.divider_size)

                    break

                elif chosen == '3':
                    print("-"*save_load.divider_size)
                    self.choose_directory()
                    print("-"*save_load.divider_size)

                    break

                elif chosen in ['e', 'x', 'exit', 'b', 'back']:
                    return

    def create_process(self):
        main.party_info['musicbox_process'] = multiprocessing.Process(target=self.playlist,
                                                                      args=(main.party_info['musicbox_folder'],
                                                                            main.party_info['musicbox_mode']))

    @staticmethod
    def play_order():
        print("Which setting do you want for the musicbox?")
        print("      [1] A->Z")
        print("      [2] Z->A")
        print("      [3] Shuffle")

        while True:
            chosen = main.s_input('Input [#] (or type "back"): ')

            if chosen in ['e', 'x', 'exit', 'b', 'back']:
                return

            elif chosen == '1':
                main.party_info['musicbox_mode'] = "A->Z"
                print("-"*save_load.divider_size)
                print("Musicbox set to play from A->Z.")

            elif chosen == '2':
                main.party_info['musicbox_mode'] = "Z->A"
                print("-"*save_load.divider_size)
                print("Musicbox set to play from Z->A.")

            elif chosen == '3':
                main.party_info['musicbox_mode'] = "shuffle"
                print("-"*save_load.divider_size)
                print("Musicbox set to shuffle.")

            else:
                continue

            if main.party_info['musicbox_isplaying']:
                print("You'll need to restart your musicbox to apply this change.")

            main.s_input("\nPress enter/return ")

            return

    def choose_directory(self):
        while True:
            folder = main.s_input("Type the directory path, type 'explore', or type 'back': ")

            if folder.lower() == "explore":
                print("-" * save_load.divider_size)
                folder = self.select_root()

                if not folder:
                    print("-" * save_load.divider_size)
                    continue

            elif folder.lower() in ['e', 'x', 'exit', 'b', 'back']:
                return

            else:
                if not os.path.isdir(folder):
                    print("-" * save_load.divider_size)
                    print(f"{folder} is not a valid directory")
                    main.s_input("\nPress enter/return ")
                    print("-" * save_load.divider_size)
                    continue

            print("-" * save_load.divider_size)
            for file in os.listdir(folder):
                if any(map(file.endswith, ['.ogg', 'flac', '.mp3', '.wav'])):

                    main.party_info['musicbox_folder'] = folder
                    print(f"Directory set to {folder}")

                    if main.party_info['musicbox_isplaying']:
                        print("You'll need to restart your musicbox to apply this change.")

                    main.s_input("\nPress enter/return ")

                    return

            else:
                print("Couldn't find any .ogg, .flac, .mp3, or .wav files in that directory.")
                while True:
                    y_n = main.s_input("Select a different directory? | Yes or No: ")

                    if y_n.startswith("y"):
                        print("-" * save_load.divider_size)
                        break

                    elif y_n.startswith("n"):
                        return

    def select_root(self):
        drive_list = []
        for drive in range(ord('A'), ord('N')):
            if os.path.exists(chr(drive) + ':'):
                drive_list.append(chr(drive))

        if len(drive_list) > 1:
            while True:
                print("Select a drive: ")

                for num, x in enumerate(drive_list):
                    print(f"      [{num + 1}] {x}:/")

                while True:
                    chosen = main.s_input("Input [#] (or type back): ")

                    try:
                        chosen = drive_list[int(chosen) - 1]

                    except (IndexError, ValueError):
                        if chosen in ['e', 'x', 'exit', 'b', 'back']:
                            return False

                        else:
                            continue

                    return self.file_explorer(f"{chosen}:")

        else:
            return self.file_explorer(f"{drive_list[0]}:")

    @staticmethod
    def file_explorer(root):
        current_path = [root]

        while True:
            print("-"*save_load.divider_size)
            available_dirs = []

            print(f"Current Path: {'/'.join(current_path)}/")
            for file in os.listdir(f"{'/'.join(current_path)}/"):
                if os.path.isdir('/'.join([x for x in current_path] + [file])):
                    available_dirs.append(file)
                    print(f"      [{len(available_dirs)}] {file}")

                else:
                    print(f"          {file}")

            while True:
                chosen = main.s_input('Input [#], type "choose" to choose this folder, or type "back": ').lower()

                try:
                    chosen = available_dirs[int(chosen) - 1]
                    current_path.append(chosen)

                    break

                except (IndexError, ValueError):
                    if chosen == "choose":
                        return '/'.join(current_path)

                    elif chosen in ['e', 'x', 'exit', 'b', 'back']:
                        if len(current_path) > 1:
                            current_path.pop()
                            break

                        else:
                            return False

    @staticmethod
    def playlist(folder, mode):
        import pygame

        pygame.mixer.pre_init()
        pygame.mixer.init()

        song_list = []

        for file in os.listdir(folder):
            if any(map(file.endswith, ['.ogg', 'flac', '.mp3', '.wav'])):
                song_list.append(file)

        if mode == 'A->Z':
            song_list = sorted(song_list)

        if mode == 'Z->A':
            song_list = sorted(song_list, reverse=True)

        if mode == 'shuffle':
            random.shuffle(song_list)

        for song in song_list:
            try:
                pygame.mixer.music.load(f"{folder}/{song}")
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pass

            except pygame.error:
                pass


class Ingredient(NonConsumable):
    def __init__(self, name, desc, value, flavor, item_id, ascart='misc', cat='misc', imp=False):
        super().__init__(name, desc, value, item_id, imp, ascart, cat)
        self.flavor = flavor


# --- ITEMS --- #
# Potions -- Health
s_potion = HealthManaPotion('Weak Potion',
                            'A small potion that restores 15 HP when consumed.',
                            15, "s_potion", heal=15)
m_potion = HealthManaPotion('Basic Potion',
                            'A regular potion that restores 45 HP when consumed.',
                            30, "m_potion", heal=45)
l_potion = HealthManaPotion('Strong Potion',
                            'A powerful potion that restores 100 HP when consumed.',
                            60, "l_potion", heal=100)
x_potion = HealthManaPotion('Super Potion',
                            'A super powerful potion that restores 200 HP when consumed.',
                            120, "x_potion", heal=200)

# Potions -- Mana
s_elixir = HealthManaPotion('Basic Elixir',
                            'A generic elixir that restores 15 MP when consumed.',
                            10, "s_elixir", mana=10, ascart='Elixir')
m_elixir = HealthManaPotion('Enhanced Elixir',
                            'A more potent elixir that restores 45 MP when consumed.',
                            20, "m_elixir", mana=35, ascart='Elixir')
l_elixir = HealthManaPotion('Grand Elixir',
                            'A powerful elixir that restores 100 MP when consumed.',
                            40, "l_elixir", mana=75, ascart='Elixir')
x_elixir = HealthManaPotion('Extreme Elixir',
                            'A super powerful elixir that restores 175 MP when consumed.',
                            80, "x_elixir", mana=175, ascart='Elixir')

# Potions -- Both
s_rejuv = HealthManaPotion('Minor Rejuvenation Potion',
                           'A basic mixture that restores 15 HP and 15 MP when consumed.',
                           30, "s_rejuv", heal=15, mana=15, ascart='Rejuv')

m_rejuv = HealthManaPotion('Refined Rejuvenation Potion',
                           'A higher quality mixture that restores 45 HP and 45 MP when consumed.',
                           60, 22, "m_rejuv", heal=45, mana=45, ascart='Rejuv')

l_rejuv = HealthManaPotion('Mighty Rejuvenation Potion',
                           'A super powerful mixture that restores 100 HP and 100 MP when consumed.',
                           120, 80, "l_rejuv", heal=100, mana=100, ascart='Rejuv')

# Potions - Status
silence_potion = StatusPotion('Potion of Allowing Speech', """\
A potion designed to enable the usage of damaged vocal chords. Relieves a party
member of the "Silenced" debuff.""", 50, 'silenced', "silence_pot")

poison_potion = StatusPotion('Potion of Curing Disease', """\
A potion designed to cure even the most deadly of illnesses.Relieves a party
member of the "Poisoned" debuff.""", 50, 'poisoned', "poison_pot")

weakness_potion = StatusPotion('Potion of Regaining Strength', """\
A potion designed to help regain lost muscle-mass and stamina. Relieves a party
member of the "Weakened" debuff.""", 50, 'weakened', "weakness_pot")

blindness_potion = StatusPotion('Potion of Enabling Sight', """\
A potion designed to help the blind regain their eyesight. Relieves a party
member of the "Blinded" debuff.""", 50, 'blinded', "blindness_pot")

paralyzation_potion = StatusPotion('Potion of Inducing Motion', """\
A potion designed to cure minor paralysis in most of the body. Relieves a party
member of the "Paralyzed" debuff.""", 50, 'paralyzed', "paralyze_pot")

# Potions - Alchemy
attract_potion_1 = AttractPotion("Attract Potion I", """\
A potion that can only be obtained through alchemy. Guarantees a one-monster
encounter for the next 3 steps on the overworld. Some areas don't
have monster spawns. Made using 'strange' ingredients.""", 100, 3, 1, "attractpot1")
attract_potion_2 = AttractPotion("Attract Potion II", """\
A potion that can only be obtained through alchemy. Guarantees a two-monster
encounter for the next 3 steps on the overworld. Some areas don't
have monster spawns. Made using 'strange' ingredients.""", 100, 3, 2, "attractpot2")
attract_potion_3 = AttractPotion("Attract Potion III", """\
A potion that can only be obtained through alchemy. Guarantees a three-monster
encounter for the next 3 steps on the overworld. Some areas don't
have monster spawns. Made using 'strange' ingredients.""", 100, 3, 3, "attractpot3")

repel_potion_1 = RepelPotion("Repel Potion I", """\
A potion that can only be obtained through alchemy. Prevents monster encounters
on the overworld for 10 steps. Bosses can still be fought while this potion is
active. Made using 'natural' ingredients.""", 100, 10, "repelpot1")
repel_potion_2 = RepelPotion("Repel Potion II", """\
A potion that can only be obtained through alchemy. Prevents monster encounters
on the overworld for 15 steps. Bosses can still be fought while this potion is
active. Made using 'natural' ingredients.""", 100, 15, "repelpot2")
repel_potion_3 = RepelPotion("Repel Potion III", """\
A potion that can only be obtained through alchemy. Prevents monster encounters
on the overworld for 20 steps. Bosses can still be fought while this potion is
active. Made using 'natural' ingredients.""", 100, 20, "repelpot3")

grenade_potion_1 = BombPotion("Grenade Potion I", """\
A potion that can only be obtained through alchemy. Deals 20 physical damage to
all enemies in the battle. Made using 'flowing' ingredients.""", 100, True, 20, "grenadepot1")
grenade_potion_2 = BombPotion("Grenade Potion II", """\
A potion that can only be obtained through alchemy. Deals 40 physical damage to
all enemies in the battle. Made using 'flowing' ingredients.""", 100, True, 40, "grenadepot2")
grenade_potion_3 = BombPotion("Grenade Potion III", """\
A potion that can only be obtained through alchemy. Deals 80 physical damage to
all enemies in the battle. Made using 'flowing' ingredients.""", 100, True, 80, "grenadepot3")

missile_potion_1 = BombPotion("Missile Potion I", """\
A potion that can only be obtained through alchemy. Deals 40 physical damage to
a single target enemy. Made using 'rigid' ingredients.""", 100, False, 40, "missilepot1")
missile_potion_2 = BombPotion("Missile Potion II", """\
A potion that can only be obtained through alchemy. Deals 80 physical damage to
a single target enemy. Made using 'rigid' ingredients.""", 100, False, 80, "missilepot2")
missile_potion_3 = BombPotion("Missile Potion III", """\
A potion that can only be obtained through alchemy. Deals 160 physical damage to
a single target enemy. Made using 'rigid' ingredients.""", 100, False, 160, "missilepot3")

greed_potion_1 = XPGoldPotion("Greed Potion I", """\
A potion that can only be obtained through alchemy. Used on an ally to convert 
50 XP into 50 GP. Made using 'dark' ingredients.""", 100, 50, -50, "greedpot1")
greed_potion_2 = XPGoldPotion("Greed Potion II", """\
A potion that can only be obtained through alchemy. Used on an ally to convert 
100 XP into 100 GP. Made using 'dark' ingredients.""", 100, 100, -100, "greedpot2")
greed_potion_3 = XPGoldPotion("Greed Potion III", """\
A potion that can only be obtained through alchemy. Used on an ally to convert 
200 XP into 200 GP. Made using 'dark' ingredients.""", 100, 200, -200, "greedpot3")

temperance_potion_1 = XPGoldPotion("Temperance Potion I", """\
A potion that can only be obtained through alchemy. Used on an ally to convert
50 GP into 50 XP. Made using 'mystic' ingredients.""", 100, -50, 50, "temppot1")
temperance_potion_2 = XPGoldPotion("Temperance Potion II", """\
A potion that can only be obtained through alchemy. Used on an ally to convert
100 GP into 100 XP. Made using 'mystic' ingredients.""", 100, -50, 50, "temppot2")
temperance_potion_3 = XPGoldPotion("Temperance Potion III", """\
A potion that can only be obtained through alchemy. Used on an ally to convert
200 GP into 200 XP. Made using 'mystic' ingredients.""", 100, -50, 50, "temppot3")

gamecrash_potion = GameCrashPotion("Game Crash Potion", """\
Instantly crashes the game when used. Speaking of which, why would drink this?
Maybe you think I'm lying. Maybe you think it will grant you an ultra-powerful
weapon, or maybe it will make you level 100, or maybe it will instantly defeat
an important boss coming up. Well you'd be wrong, it really does just crash the
game. That's all this potion does, you wasted those mathematical ingredients on
this useless potion. You could have sold those for money, unlike this potion 
which has no sale value. Instead you make a potion whose only purpose is to
crash the game. You probably don't believe me, do you? You think I'm lying and 
you're gonna drink this thing regardless of what I tell you. Well fine, but
at least save the game before you do, and don't yell at me if you didn't and
your progress is lost.""", 0, "gamecrashpot")

# Fists exist to prevent bugs caused by not having any weapon equipped. Also the starting
# weapon for the Monk. Cannot be unequipped, and therefore cannot be sold.
fists = Weapon('Fists', """\
The oldest weapon known to man [+0% Damage].""",
               0, 0, 'melee', [], 'Fists', "weapon_fist")

# These exist for the same reason as fists. They are only available when unequipping actual
# armor and accessories. Cannot be unequipped, and therefore cannot be sold.
no_head = Armor('None',
                "You should probably get some head armor [+0% Damage Resistance].",
                0, 0, 'head', [], 'misc', 'no_head')
no_body = Armor('None',
                "You should probably get some body armor [+0% Damage Resistance].",
                0, 0, 'body', [], 'misc', 'no_body')
no_legs = Armor('None',
                "You should probably get some leg armor [+0% Damage Resistance].",
                0, 0, 'legs', [], 'misc', 'no_legs')
no_access = Armor('None',
                  "You should probably get an accessory [No Effects].",
                  0, 0, 'access', [], 'misc', 'no_access')

# Weapons -- Warrior
iron_hoe = Weapon('Iron Hoe', """\
Not much of a weapon, unless you really hate dirt [+5% Damage].""",
                  10, 0.05, 'melee', ['warrior'], 'hoe', "wdn_sht")

bnz_swd = Weapon('Bronze Sword',
                 'A light yet sturdy sword smelted from bronze [+10% Damage].',
                 150, 0.1, 'melee', ['warrior'], 'Sword', "bnz_swd")
en_bnz_swd = Weapon('Enhanced Bronze Sword',
                    'Even better than your typical Bronze Sword [+25% Damage].',
                    300, 0.25, 'melee', ['warrior'], 'Sword', "en_bnz_swd")

stl_spr = Weapon('Steel Spear',
                 'A fair-sized spear crafted from well made steel [+40% Damage].',
                 600, 0.4, 'melee', ['warrior'], 'Spear', "stl_spr")
en_stl_spr = Weapon('Enhanced Steel Spear',
                    'Even better than your typical Steel Spear [+60% Damage].',
                    900, 0.6, 'melee', ['warrior'], 'Spear', "en_stl_spr")

titan_axe = Weapon('Titanium Battleaxe',
                   'A heavy and powerful axe made of high quality Titanium [+80% Damage].',
                   1200, 0.8, 'melee', ['warrior'], 'Axe', "titan_axe")
en_titan_axe = Weapon('Enhanced Titanium Battleaxe',
                      'Even better than your typical Titanium Battleaxe [+100% Damage].',
                      2400, 1, 'melee', ['warrior'], 'Axe', "en_titan_axe")

# Weapons -- Assassin
stn_dag = Weapon('Stone Dagger', """\
A stone knife that you made yourself! Used to shear sheep and cut meat [+5% Damage]""",
                 10, 0.05, 'melee', ['assassin'], 'Dagger', "stn_dag")

ser_knf = Weapon('Serrated Knife',
                 'A durable knife made of iron, with one side made jagged [+10% Damage]',
                 150, 0.1, 'melee', ['assassin'], 'Dagger', "ser_knf")
en_ser_knf = Weapon('Enhanced Serrated Knife',
                    'Even better than your typical Serrated Knife [+25% Damage].',
                    300, 0.25, 'melee', ['assassin'], 'Dagger', "en_ser_knf")

stiletto = Weapon('Stiletto',
                  'A long, cross-shaped knife perfect for "removing" your enemies [+40% Damage].',
                  600, 0.4, 'melee', ['assassin'], 'Stiletto', "stiletto")
en_stiletto = Weapon('Enhanced Stiletto',
                     'Even better than your typical Stiletto [+60% Damage].',
                     900, 0.6, 'melee', ['assassin'], 'Stiletto', "en_stiletto")

myth_sb = Weapon('Mythril Shortblade',
                 'A knife made of a rare and powerful material [+80% Damage].',
                 1200, 0.8, 'melee', ['assassin'], 'Short Sword', "myth_sb")
en_myth_sb = Weapon('Enhanced Mythril Shortblade',
                    'Even better than your typical Mythril Shortblade [+100% Damage].',
                    2400, 1, 'melee', ['assassin'], 'Short Sword', "en_myth_sb")

# Weapons -- Ranger
slg_sht = Weapon('Sling Shot', """\
A weapon that could scare even the mightiest of tin-cans [+5% Damage].""",
                 10, 0.05, 'ranged', ['ranger'], 'Sling Shot', "slg_sht")

sht_bow = Weapon('Short Bow',
                 "A bow of great craftsmanship. It's kinda small, though [+10% Damage].",
                 150, 0.10, 'ranged', ['ranger'], 'Bow', "sht_bow")
en_sht_bow = Weapon('Enhanced Short Bow',
                    "Even better than your typical Short Bow [+25% Damage].",
                    300, 0.25, 'ranged', ['ranger'], 'Bow', "en_sht_bow")

lng_bow = Weapon('Long Bow',
                 'A much more impressive bow capable of accuracy at long distances [+40% Damage].',
                 600, 0.4, 'ranged', ['ranger'], 'Bow', "lng_bow")
en_lng_bow = Weapon('Enhanced Long Bow',
                    'Even better than your typical Long Bow [+60% Damage].',
                    900, 0.6, 'ranged', ['ranger'], 'Bow', "en_lng_bow")

ash_cbow = Weapon('Ashen Crossbow',
                  'A beautifully-crafted crossbow made from the wood of an ash tree. [+80% Damage].',
                  1200, 0.8, 'ranged', ['ranger'], 'Crossbow', "ash_cbow")
en_ash_cbow = Weapon('Enhanced Ashen Crossbow',
                     'Even better than your typical Ashen Crossbow [+100% Damage].',
                     2400, 1, 'ranged', ['ranger'], 'Crossbow', "en_ash_cbow")

# Weapons -- Mage
mag_twg = Weapon('Magical Twig', """\
Not actually magical but it makes you feel cooler when you use it [+5% Damage].""",
                 10, 0.05, 'ranged', ['mage'], 'Twig', "mag_twg")

oak_stf = Weapon('Oak Staff',
                 'A wooden staff imbued with weak magical abilities [+10% Damage].',
                 150, 0.1, 'ranged', ['mage'], 'Staff', "oak_stf")
en_oak_stf = Weapon('Enhanced Oak Staff',
                    'Even better than your typical Oak Staff [+15% Damage].',
                    300, 0.15, 'ranged', ['mage'], 'Staff', "en_oak_stf")

arc_spb = Weapon('Arcane Spellbook',
                 'An intermediate spellbook for combat purposes [+20% Damage].',
                 600, 0.2, 'ranged', ['mage'], 'Book', "arc_spb")
en_arc_spb = Weapon('Enhanced Arcane Spellbook',
                    'Even better than your typical Arcane Spellbook [+30% Damage].',
                    900, 0.3, 'ranged', ['mage'], 'Book', "en_arc_spb")

rnc_stf = Weapon('Runic Staff',
                 'A powerful staff enchanted with ancient magic [+40% Damage].',
                 1200, 0.4, 'ranged', ['mage'], 'Staff', "rnc_stf")
en_rnc_stf = Weapon('Enhanced Runic Staff',
                    'Even better than your typical Runic Staff [+50% Damage].',
                    2400, 0.5, 'ranged', ['mage'], 'Staff', "en_rnc_stf")

# Weapons -- Paladin
rbr_mlt = Weapon('Rubber Mallet', """\
This can barely hammer nails, what do you expect to kill with it? [+5% Damage].""",
                 10, 0.05, 'melee', ['paladin'], 'Hammer', "rbr_mlt")

holy_mace = Weapon('Holy Mace',
                   'An well-made iron mace imbued with the power of the heavens [+10% Damage].',
                   150, 0.1, 'melee', ['paladin'], 'Mace', "holy_mace")
en_holy_mace = Weapon('Enhanced Holy Mace',
                      'Even better than your typical Holy Mace [+25% Damage].',
                      300, 0.25, 'melee', ['paladin'], 'Mace', "en_holy_mace")

hmr_of_mgt = Weapon('Hammer of Might',
                    'A hammer often used by holy warriors to smash their foes [+40% Damage].',
                    600, 0.4, 'melee', ['paladin'], 'Hammer', "hmr_of_mgt")
en_hmr_of_mgt = Weapon('Enhanced Hammer of Might',
                       'Even better than your typical Hammer of Might [+60% Damage].',
                       900, 0.6, 'melee', ['paladin'], 'Hammer', "en_hmr_of_mgt")

ngt_bane = Weapon("Night's Bane",
                  'A forbidden hammer used throughout history to crush unholy creatures [+80% Damage].',
                  1200, 0.8, 'melee', ['paladin'], 'Hammer', "ngt_bane")
en_ngt_bane = Weapon("Enhanced Night's Bane",
                     "Even better than your typical Night's Bane [+100% Damage].",
                     2400, 1, 'melee', ['paladin'], 'Hammer', "en_ngt_bane")

# Weapons -- Monk
garden_gloves = Weapon("Gardening Gloves", """\
Used to prevent getting cut on thorns or the teeth of your enemies [+5% Damage].""",
                       10, 0.05, 'melee', ['monk'], 'Gloves', "gardening_gloves")

brass_kncls = Weapon('Brass Knuckles',
                     'A brass adornment for your knuckles providing extra punching power [+10% Damage].',
                     150, 0.1, 'melee', ['monk'], 'Knuckles', "brass_kncls")
en_brass_kncls = Weapon('Enhanced Brass Knuckles',
                        'Even better than your typical Brass Knuckles [+25% Damage].',
                        300, 0.25, 'melee', ['monk'], 'Knuckles', "en_brass_kncls")

bladed_gloves = Weapon('Bladed Gloves',
                       'Leather gloves with sturdy steel blades protruding from them [+40% Damage].',
                       600, 0.4, 'melee', ['monk'], 'Gloves', "bladed_gloves")
en_bladed_gloves = Weapon('Enhanced Bladed Gloves',
                          'Even better than your typical Bladed Gloves [+60% Damage].',
                          900, 0.6, 'melee', ['monk'], 'Gloves', "en_bladed_gloves")

lead_bg = Weapon('Lead-Weighted Mitts',
                 'Weighted with 5 pounds of lead and tipped with steel blades [+80% Damage].',
                 1200, 0.8, 'melee', ['monk'], 'Gloves', "lead_bg")
en_lead_bg = Weapon('Enhanced Lead Mitts',
                    'Even better than your typical Lead-Weighted Mitts [+100% Damage].',
                    2400, 1, 'melee', ['monk'], 'Gloves', "en_lead_bg")

# Weapons -- Bard
kazoo = Weapon("Kazoo", """\
A wooden kazoo that does more to annoy your enemies than damage them [+5% Damage].""",
               10, 0.05, 'magic', ['bard'], 'kazoo', "kazoo")

flute = Weapon("Flute", """\
A good-quality flute made out of wood and silver [+10% Damage].""",
               150, 0.1, 'magic', ['bard'], 'flute', "flute")

snare_drum = Weapon("Snare Drum", """\
A marching drum used to inspire courage in the hearts of your allies [+30% Damage].""",
                    300, 0.3, 'magic', ['bard'], 'drum', "snare_drum")

trumpet = Weapon("Trumpet", """\
A mighty brass trumpet that can be heard blaring from miles away [+50% Damage].""",
                 600, 0.5, 'magic', ['bard'], 'trumpet', "trumpet")

violin = Weapon("Violin", """\
A beautiful violin that could make even the most stone-cold weep [+70% Damage].""",
                1200, 0.7, 'magic', ['bard'], 'violin', "violin")

bagpipes = Weapon("Bagpipes", """\
A ridiculously loud and extravagent bagpipe made from plaid fabric. Your
allies will probably hate you if you use this [+90% Damage].""",
                  2400, 0.9, 'magic', ['bard'], 'bagpipes', "bagpipes")

# Starting Armor (All classes)
straw_hat = Armor('Straw Hat', """\
Useful for keeping the sun out of your eyes and not much else [+0% Resistance].""",
                  10, 0, 'head', [], 'Hat', "straw_hat")

cotton_shirt = Armor('Cotton Shirt', """\
This shirt is all torn up and stained from years of use [+0% Resistance].""",
                     10, 0, 'body', [], 'Shirt', "cotton_shirt")

sunday_trousers = Armor('Sunday Trousers', """\
Unfortuantely you have to wear these uncomfortable pants on more than just
sundays [+0% Resistance].""",
                        10, 0, 'legs', [], 'Pants', "sunday_trousers")

# Armor -- Warrior + Paladin -- Weak
# 30% Resistance
bnz_hlm = Armor('Bronze Helmet',
                'A simple helmet crafted from bronze [+10% Resistance].',
                100, 0.1, 'head', ['warrior', 'paladin'], 'Helmet', "bnz_hlm")
bnz_cst = Armor('Bronze Chestpiece',
                'Simple chest armor crafted from bronze [+10% Resistance].',
                100, 0.1, 'body', ['warrior', 'paladin'], 'Shirt', "bnz_cst")
bnz_leg = Armor('Bronze Greaves',
                'Simple leg armor crafted from bronze [+10% Resistance].',
                100, 0.1, 'legs', ['warrior', 'paladin'], 'Pants', "bnz_leg")

# Armor -- Warrior + Paladin -- Mid
# 45% Resistance
stl_hlm = Armor('Steel Helmet',
                'A decent helmet created from a solid metal [+15% Resistance].',
                600, 0.15, 'head', ['warrior', 'paladin'], 'Helmet', "stl_hlm")
stl_cst = Armor('Steel Chestpiece',
                'Decent body armor made from a solid metal [+15% Resistance].',
                600, 0.15, 'body', ['warrior', 'paladin'], 'Shirt', "stl_cst")
stl_leg = Armor('Steel Greaves',
                'Decent greaves made from a solid metal [+15% Resistance].',
                600, 0.15, 'legs', ['warrior', 'paladin'], 'Pants', "stl_leg")

# Armor -- Warrior + Paladin -- Pow
# 60% Resistance
ori_hlm = Armor('Orichalcum Helmet',
                'A strong helmet smelted from rare mountain copper  [+20% Resistance].',
                1200, 0.2, 'head', ['warrior', 'paladin'], 'Helmet', "ori_hlm")
ori_cst = Armor('Orichalcum Chestplate',
                'Strong chest armor smelted from rare mountain copper  [+20% Resistance].',
                1200, 0.2, 'body', ['warrior', 'paladin'], 'Shirt', "ori_cst")
ori_leg = Armor('Orichalcum Greaves',
                'Strong leg armor smelted from rare mountain copper [+20% Resistance].',
                1200, 0.2, 'legs', ['warrior', 'paladin'], 'Pants', "ori_leg")

# Armor -- Mage + Monk -- Weak
# 18% Resistance
wiz_hat = Armor('Silk Hat',
                'A silk hat woven with magic thread [+5% Resistance].',
                100, 0.05, 'head', ['mage', 'monk'], 'Wizard Hat', "wiz_hat")
wiz_rob = Armor('Silk Robe',
                'A silk robe woven with magic thread [+5% Resistance].',
                100, 0.05, 'body', ['mage', 'monk'], 'Robe', "wiz_rob")
wiz_gar = Armor('Silk Garments',
                'Silk garments woven with magic thread [+5% Resistance].',
                100, 0.05, 'legs', ['mage', 'monk'], 'Robe Pants', "wiz_gar")

# Armor -- Mage + Monk -- Mid
# 27% Resistance
myst_hat = Armor('Mystical Hood',
                 'A mysterious hood with strange symbols sewn into it [+9% Resistance].',
                 600, 0.09, 'head', ['mage', 'monk'], 'Wizard Hat', "myst_hat")
myst_rob = Armor('Mystical Robe',
                 'A mysterious robe with strange symbols sewn into it [+9% Resistance].',
                 600, 0.09, 'body', ['mage', 'monk'], 'Robe', "myst_rob")
myst_gar = Armor('Mystical Garments',
                 'Mysterious garments with strange symbols sewn into it [+9% Resistance].',
                 600, 0.09, 'legs', ['mage', 'monk'], 'Robe Pants', "myst_gar")

# Armor -- Mage + Monk -- Pow
# 36% Resistance
elem_hat = Armor('Armored Cloth Hat',
                 'A silk hat lined with chainmail in important parts [+12% Resistance].',
                 1200, 0.12, 'head', ['mage', 'monk'], 'Wizard Hat', "elem_hat")
elem_rob = Armor('Armored Cloth Robe',
                 'A silk robe lined with chainmail in important parts [+12% Resistance].',
                 1200, 0.12, 'body', ['mage', 'monk'], 'Robe', "elem_rob")
elem_gar = Armor('Armored Cloth Garments',
                 'Silk garments lined with chainmail in important parts [+12% Resistance].',
                 1200, 0.12, 'legs', ['mage', 'monk'], 'Robe Pants', "elem_gar")

# Armor -- Assassin + Ranger -- Weak
# 24% Resistance
lth_cap = Armor('Leather Cap',
                'A simple leather cap providing equally simple protection [+8% Resistance].',
                100, 0.08, 'head', ['assassin', 'ranger'], 'Cap', "lth_cap")
lth_bdy = Armor('Leather Bodyarmor',
                'Simple body armor providing equally simple protection [+8% Resistance].',
                100, 0.08, 'body', ['assassin', 'ranger'], 'Shirt', "lth_bdy")
lth_leg = Armor('Leather Leggings',
                'Simple leggings providing equally simple protection [+8% Resistance].',
                100, 0.08, 'legs', ['assassin', 'ranger'], 'Pants', "lth_leg")

# Armor -- Assassin + Ranger -- Mid
# 36% Resistance
std_cwl = Armor('Studded Cowl',
                'A soft leather cap studded with steel pieces [+12% Resistance].',
                600, 0.12, 'head', ['assassin', 'ranger'], 'Cap', "std_cwl")
std_bdy = Armor('Studded Body-armor',
                'Soft leather body armor studded with steel pieces [+12% Resistance].',
                600, 0.12, 'body', ['assassin', 'ranger'], 'Shirt', "std_bdy")
std_leg = Armor('Studded Leggings',
                'Soft leather leggings studded with steel pieces [+12% Resistance].',
                600, 0.12, 'legs', ['assassin', 'ranger'], 'Pants', "std_leg")

# Armor -- Assassin + Ranger -- Pow
# 48% Resistance
drg_cwl = Armor('Dragonhide Cowl',
                'A tough hood crafted from high-quality dragonskin [+16% Resistance].',
                1200, 0.16, 'head', ['assassin', 'ranger'], 'Cap', "drg_cwl")
drg_bdy = Armor('Dragonhide Bodyarmor',
                'Tough bodyarmor crafted from high-quality dragonskin [+16% Resistance].',
                1200, 0.16, 'body', ['assassin', 'ranger'], 'Shirt', "drg_bdy")
drg_leg = Armor('Dragonhide Leggings',
                'Tough leggings crafted from high-quality dragonskin [+16% Resistance].',
                1200, 0.16, 'legs', ['assassin', 'ranger'], 'Pants', "drg_leg")

# Armor -- Bard -- Weak
# 15% Resistance
linen_beret = Armor('Linen Beret', """\
A stylish hat made of linen. Looks great, doesn't do much to protect your head [+5% Resistance].""",
                    100, 0.05, 'head', ['bard'], 'Hat', "linen_beret")
linen_shirt = Armor('Linen Shirt', """\
A classic shirt made of linen. Not really intended to be worn in battle [+5% Resistance].""",
                    100, 0.05, 'body', ['bard'], 'Shirt', "linen_shirt")
linen_trousers = Armor('Linen Trousers', """\
Some good-looking pants made of linen. You're not gonna be deflecting many attacks 
with these [+5% Resistance].""",
                       100, 0.05, 'legs', ['bard'], 'Pants', "linen_trousers")

# Armor -- Bard -- Mid
# 21% Resistance
wool_roundlet = Armor('Wool Roundlet', """\
The perfect hat for someone who considers fanciness a priority [+7% Resistance].""",
                      600, 0.07, 'head', ['bard'], "Hat", "wool_roundlet")
wool_tunic = Armor('Wool Tunic', """\
A more durable shirt complete with a fancy leather belt [+7% Resistance].""",
                   600, 0.07, 'body', ['bard'], "Shirt", "wool_tunic")
wool_britches = Armor('Wool Britches', """\
Wool pants that balance classiness and comfort [+7% Resistance].""",
                      600, 0.07, 'legs', ['bard'], "Pants", "wool_britches")

# Armor -- Bard -- Pow
# 27% Resistance
velvet_cavalier = Armor('Velvet Cavalier', """\
A hat fit for nobility. Complete with a large red pheasant feather [+9% Resistance].""",
                        1200, 0.09, 'head', ['bard'], 'Hat', "velvet_cavalier")
velvet_doublet = Armor('Velvet Doublet', """\
A ludicrously-fancy shirt with red and gold trimmings, worn by only the rich 
and powerful. And you. [+9% Resistance].""",
                       1200, 0.09, 'body', ['bard'], 'Shirt', "velvet_doublet")
velvet_kilt = Armor('Velvet Kilt', """\
A fancy skirt that allows for a more full range of movement. Try not to use in
gusty weather [+9% Resistance].""",
                    1200, 0.09, 'body', ['bard'], 'kilt', "velvet_kilt")


# Accessories
# -- Elemental Accessories
water_amulet = ElementAccessory('Aquatic Amulet', 'An amulet that imbues its wearer with the power of WATER',
                                375, 'water', "aquatic_amulet")
fire_amulet = ElementAccessory('Infernal Amulet', 'An amulet that imbues its wearer with the power of FIRE',
                               375, 'fire', "fire_amulet")
earth_amulet = ElementAccessory('Ground Amulet', 'An amulet that imbues its wearer with the power of EARTH',
                                375, 'earth', "earth_amulet")
electric_amulet = ElementAccessory('Galvanic Amulet', 'An amulet that imbues its wearer with the power of ELECTRICITY',
                                   375, 'electric', "electric_amulet")
wind_amulet = ElementAccessory('Tempestuous Amulet', 'An amulet that imbues its wearer with the power of WIND',
                               375, 'wind', "wind_amulet")
grass_amulet = ElementAccessory('Verdant Amulet', 'An amulet that imbues its wearer with the power of GRASS',
                                375, 'grass', "grass_amulet")
ice_amulet = ElementAccessory('Glacial Amulet', 'An amulet that imbues its wearer with the power of ICE',
                              375, 'ice', "ice_amulet")
light_amulet = ElementAccessory('Divine Amulet', 'An amulet that imbues its wearer with the power of LIGHT',
                                375, 'light', "light_amulet")
dark_amulet = ElementAccessory('Umbral Amulet', 'An amulet that imbues its wearer with the power of DARKNESS',
                               375, 'dark', "dark_amulet")

# Quest items
message_joseph = Item('Message from Joseph', 'A neatly written message addressed to Philliard.',
                      0, "message_joseph", True, "misc", 'q_items')

message_philliard = Item('Message from Philliard', 'A neatly written message addressed to Joseph.',
                         0, "message_philliard", True, "misc", 'q_items')

# Gems & Valuables
pearl_gem = Item('Pearl', 'A valuable pearl. This could probably be sold for quite a bit.',
                 875, "pearl_gem", False, "Gem", "misc")

ruby_gem = Item('Ruby', 'A valuable ruby. This could be sold for quite a bit.',
                875, "ruby_gem", False, "Gem", "misc")

sapphire_gem = Item('Sapphire', 'A valuable sapphire. This could probably be sold for quite a bit.',
                    875, "sapphire_gem", False, "Gem", "misc")

emerald_gem = Item('Emerald', 'A valuable emerald. This could probably be sold for quite a bit.',
                   875, "emerald_gem", False, "Gem", "misc")

citrine_gem = Item('Citrine', 'A valuable citrine. This could probably be sold for quite a bit.',
                   875, "citrine_gem", False, "Gem", "misc")

jade_gem = Item('Jade', 'A valuable jade. This could probably be sold for quite a bit.',
                875, "jade_gem", False, "Gem", "misc")

opal_gem = Item('Opal', 'A valuable opal. This could probably be sold for quite a bit.',
                875, "opal_gem", False, "Gem", "misc")

onyx_gem = Item('Onyx', 'A valuable onyx. This could probably be sold for quite a bit.',
                875, "onyx_gem", False, "Gem", "misc")

diamond_gem = Item('Diamond', 'A valuable diamond. This could probably be sold for quite a bit.',
                   875, "diamond_gem", False, "Gem", "misc")

amethyst_gem = Item('Amethyst', 'A valuable amethyst. This could probably be sold for quite a bit.',
                    875, "amethyst_gem", False, "Gem", "misc")

topaz_gem = Item('Topaz', 'A valuable topaz. This could probably be sold for quite a bit.',
                 875, "topaz_gem", False, "Gem", "misc")

garnet_gem = Item('Garnet', 'A valuable garnet. This could probably be sold for quite a bit.',
                  875, "garnet_gem", False, "Gem", "misc")

quartz_gem = Item('Quartz', 'A valuable quartz. This could probably be sold for quite a bit.',
                  875, "quartz_gem", False, "Gem", "misc")

zircon_gem = Item('Zircon', 'A valuable zircon. This could probably be sold for quite a bit.',
                  875, "zircon_gem", False, "Gem", "misc")

agate_gem = Item('Agate', 'A valuable agate. This could probably be sold for quite a bit.',
                 875, "agate_gem", False, "Gem", "misc")

aquamarine_gem = Item('Aquamarine', 'A valuable aquamarine. This could probably be sold for quite a bit.',
                      875, "aquamarine_gem", False, "Gem", "misc")

# Tools
shovel = Shovel('Expert Mining Tool', """\
A tool used to excavate for hidden gems and minerals. Comines the functions
of a pickaxe, shovel, and hammer all into one device! Use while on the
overworld to dig for gems. Gems have pre-determined locations and do not
respawn - there is no luck involved with this tool.""", 150, "shovel")

fast_travel_atlas = FastTravelAtlas('Fast Travel Atlas', """\
A convenient tome that allows teleportation between towns. These aren't
being made anymore, after having been banned by the King due to its use in
many recent abductions and murders. Most of the pages appear to be missing.""", 0, "fast_map")

monster_book = MonsterEncyclopedia('Monster Encyclopedia', """\
A book containing information on monsters. When used in battle, this will 
identify the stats and weaknesses of an enemy. When used outside of battle,
this will let you check what biome monsters are found in, what items they drop,
and how many of them you've killed. Out-of-battle use only works for enemies
you've encountered.""", 200, "monster_book")

pocket_lab = PocketAlchemyLab('Pocket Alchemy Lab', """\
A nifty little Pocket Alchemy Lab! Somehow all of the necessary tools to
convert everyday ingredients into useful potions can fit in your pocket.
There are six flavors of ingredients, and each flavor corresponds to a specific
potion. Combine three ingredients to make a potion. The ratio of flavors used
determines the probability of getting each flavor potion. The quantity of the
prevailing ingredient determines the potion strength.""", 200, "pocket_lab")

musicbox = MusicBox('Portable Musicbox', """\
Somehow this small device has the ability to play music without need for a 
bard or instruments. Select a folder full of music on your computer and this
device will replace the in-game music with your tunes!""", 250, "musicbox")


# Tools -- Lockpicks
wood_lckpck = LockpickKit('Wooden Lockpick Kit', """\
A wooden lockpick kit with a 30% chance to open chests. Chests can be found
by sneaking into houses in towns.""", 30, 30, "wood_lckpck")

copper_lckpck = LockpickKit('Copper Lockpick Kit', """\
A copper lockpick kit with a 45% chance to open chests. Chests can be found
by sneaking into houses in towns.""", 200, 45, "copper_lckpck")

iron_lckpck = LockpickKit('Iron Lockpick Kit', """\
An iron lockpick kit with a 60% chance to open chests. Chests can be found
by sneaking into houses in towns.""", 300, 60, "iron_lckpck")

steel_lckpck = LockpickKit('Steel Lockpick Kit', """\
A steel lockpick kit with a 75% chance to open chests. Chests can be found
by sneaking into houses in towns.""", 500, 75, "steel_lckpck")

mythril_lckpck = LockpickKit('Mythril Lockpick Kit', """\
A mythril lockpick kit with a 90% chance to open chests. Chests can be found
by sneaking into houses in towns.""", 700, 90, "mythril_lckpck")

# ALCHEMY INGREDIENTS - Dropped by monsters, used to make potions
# Strange
broken_crystal = Ingredient('Broken Crystal', """\
A chunk of crystal too powdery to be of any value. Could have useful alchemical
applications. Has a "Strange" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "strange", "b_crystal")

chain_link = Ingredient('Chain links', """\
A couple joined links of chain made from steel. Could have useful alchemical
applications. Has a "Strange" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "strange", "chain_link")

bone_bag = Ingredient('Bag of Bones', """\
A bag full of various bones from a now deceased creature. Could have useful 
alchemical applications. Has a "Strange" alchemical flavor. Combine with two 
other ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "strange", "bone_bag")

ripped_cloth = Ingredient('Ripped Cloth', """\
A thick, torn cloth made out of an unknown fabric. Could have useful alchemical
applications. Has a "Strange" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "strange", "ripped_cloth")

living_bark = Ingredient('Living Bark', """\
This bark has a fleshy texture to it. Could have useful alchemical
applications. Has a "Strange" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "strange", "living_bark")

# Mystic
demonic_essence = Ingredient('Demonic Essence', """\
A strange orb that exudes a terrifying aura. Could have useful alchemical
applications. Has a "Mystic" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mystic", "d_essence")

angelic_essence = Ingredient('Angelic Essence', """\
A strange orb that radiates an incredible aura. Could have useful alchemical
applications. Has a "Mystic" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mystic", "a_essence")

mysterious_runes = Ingredient('Strange Runestone', """\
Strange stones with even stranger symbols on it. Could have useful alchemical
applications. Has a "Mystic" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mystic", "runestone")

unicorn_horn = Ingredient('Unicorn Horn', """\
A tough and shiny horn from a mythical creature. Could have useful alchemical
applications. Has a "Mystic" alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mystic", "unicorn_horn")

fairy_dust = Ingredient('Fairy Dust', """\
Dust from a fairy. It has strange, magical properties. Could have useful 
alchemical applications. Has a "Mystic" alchemical flavor. Combine with two 
other ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mystic", "fairy_dust")

# Rigid
crab_claw = Ingredient('Crab Claw', """\
A reddish claw from a giant crab. Could have useful alchemical applications.
Has a "Rigid" alchemical flavor. Combine with two other ingredients in a 
Pocket Alchemy Lab to make a potion.""", 25, "rigid", "crab_claw")

shell_fragment = Ingredient('Shell Fragment', """\
A broken fragment of a once-beautiful shell. Could have useful alchemical 
applications. Has a "Rigid" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "rigid", "shell_fragment")

golem_rock = Ingredient('Golem Rock', """\
A small rock that seems to glow slightly. Could have useful alchemical 
applications. Has a "Rigid" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "rigid", "golem_rcok")

beetle_shell = Ingredient('Beetle Shell', """\
A bluish shell from a large beetle. Could have useful alchemical applications.
Has a "Rigid" alchemical flavor. Combine with two other ingredients in a 
Pocket Alchemy Lab to make a potion.""", 25, "rigid", "beetle_shell")

monster_skull = Ingredient('Monster Skull', """\
A broken skull from a strange creature. Could have useful alchemical 
applications. Has a "Rigid" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "rigid", "m_skull")

# Flowing
slime_vial = Ingredient('Vial of Slime', """\
A small glass vial filled with gooey slime. Could have useful alchemical 
applications. Has a "Flowing" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "flowing", "s_vial")

blood_vial = Ingredient('Vial of Blood', """\
A small glass vial filled with the blood of some creature. Could have useful 
alchemical applications. Has a "Flowing" alchemical flavor. Combine with two 
other ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "flowing", "b_vial")

water_vial = Ingredient('Vial of Water', """\
A small glass vial filled with enchanted water. Could have useful alchemical 
applications. Has a "Flowing" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "flowing", "w_vial")

ink_sack = Ingredient('Ink Sack', """\
A small pouch full of an inky substance. Could have useful alchemical 
applications. Has a "Flowing" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "flowing", "ink_sack")

ectoplasm = Ingredient('Ectoplasm', """\
The gooey remains from a terrifying apparition. Could have useful alchemical 
applications. Has a "Flowing" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "flowing", "ectoplasm")

# Dark
burnt_ash = Ingredient('Burnt Ash', """\
The ashy remains of a once-living creature. Could have useful alchemical 
applications. Has a "Dark" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "dark", "burnt_ash")

monster_fang = Ingredient('Monster Fang', """\
The sharp fang of a frightening creature. Could have useful alchemical 
applications. Has a "Dark" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "dark", "monster_fang")

antennae = Ingredient('Gooey Antennae', """\
A pair of antennae from a massive, slimy insect. Could have useful alchemical 
applications. Has a "Dark" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "dark", "antennae")

eye_balls = Ingredient('Eyeballs', """\
The visual receptors of some disgusting creature. Could have useful alchemical 
applications. Has a "Dark" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "dark", "eyeballs")

serpent_scale = Ingredient('Serpent Scale', """\
A rough scale from an unknown reptile. Could have useful alchemical 
applications. Has a "Dark" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "dark", "s_scale")

# Natural
wing_piece = Ingredient('Wing Piece', """\
A piece of wing from a flying creature. Could have useful alchemical 
applications. Has a "Natural" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "natural", "wing_piece")

animal_fur = Ingredient('Animal Fur', """\
A wet clump of fur from a strange animal. Could have useful alchemical 
applications. Has a "Natural" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "natural", "animal_fur")

rodent_tail = Ingredient('Rodent Tail', """\
The detached tail of a hideous rodent. Could have useful alchemical 
applications. Has a "Natural" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "natural", "rodent_tail")

serpent_tongue = Ingredient('Serpent Tongue', """\
A dried-up tongue from a slithery serpent. Could have useful alchemical 
applications. Has a "Natural" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "natural", "s_tongue")

feathers = Ingredient('Feathers', """\
A veiny feather from an unknown avian creature. Could have useful alchemical 
applications. Has a "Natural" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "natural", "feathers")

# Mathematical
calculus_homework = Ingredient('Calculus Homework', """\
A load of random symbols and gibberish. Could have useful alchemical 
applications. Has a "Mathematical" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mathematical", "c_homework")

graph_paper = Ingredient('Graph Paper', """\
Useful paper for graphing points and lines. Could have useful alchemical 
applications. Has a "Mathematical" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mathematical", "g_paper")

ruler = Ingredient('Ruler', """\
A piece of wood with lines on it. Neat! Could have useful alchemical 
applications. Has a "Mathematical" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mathematical", "ruler")

protractor = Ingredient('Protractor and Compass', """\
Instruments used to make shapes and angles. Could have useful alchemical 
applications. Has a "Mathematical" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mathematical", "protractor")

textbook = Ingredient('AtW Textbook', """\
More like Algebra that sucks amiright? Could have useful alchemical 
applications. Has a "Mathematical" alchemical flavor. Combine with two other 
ingredients in a Pocket Alchemy Lab to make a potion.""", 25, "mathematical", "textbook")

# Each monster can drop two different items, with the exception of the Calculator which is an easter egg monster
monster_drop_list = {'Shell Mimic': [shell_fragment, water_vial],
                     'Giant Crab': [crab_claw, shell_fragment],
                     'Naiad': [fairy_dust, water_vial],
                     'Squid': [ink_sack, slime_vial],
                     'Bog Slime': [slime_vial, water_vial],
                     'Moss Ogre': [bone_bag, ripped_cloth],
                     'Sludge Rat': [monster_skull, rodent_tail],
                     'Spriggan': [living_bark, fairy_dust],
                     'Vine Lizard': [serpent_scale, living_bark],
                     'Goblin Archer': [ripped_cloth, eye_balls],
                     'Beetle': [beetle_shell, antennae],
                     'Corrupt Thaumaturge': [ripped_cloth, mysterious_runes],
                     'Minor Yeti': [animal_fur, monster_fang],
                     'Fire Ant': [antennae, burnt_ash],
                     'Necromancer': [ripped_cloth, demonic_essence],
                     'Wraith': [ectoplasm, demonic_essence],
                     'Ghoul': [ectoplasm, demonic_essence],
                     "Will-o'-the-wisp": [fairy_dust, burnt_ash],
                     'Imp': [wing_piece, fairy_dust],
                     'Bat': [monster_fang, wing_piece],
                     'Skeleton': [bone_bag, demonic_essence],
                     'Undead Archer': [chain_link, bone_bag],
                     'Frost Bat': [monster_fang, wing_piece],
                     'Alicorn': [unicorn_horn, angelic_essence],
                     'Mummy': [burnt_ash, ripped_cloth],
                     'Giant Worm': [monster_fang, slime_vial],
                     'Griffin': [animal_fur, wing_piece],
                     'Anubis': [animal_fur, burnt_ash],
                     'Sea Serpent': [serpent_scale, serpent_tongue],
                     'Flying Serpent': [serpent_scale, serpent_tongue],
                     'Harpy': [wing_piece, feathers],
                     'Troll': [monster_skull, eye_balls],
                     'Sand Golem': [golem_rock, broken_crystal],
                     'Naga': [serpent_scale, eye_balls],
                     'Rock Giant': [golem_rock, broken_crystal],
                     'Ice Soldier': [chain_link, blood_vial],
                     'Arctic Wolf': [animal_fur, monster_fang],
                     'Oread': [fairy_dust, eye_balls],
                     'Tengu': [wing_piece, feathers],
                     'Zombie': [monster_skull, blood_vial],
                     'Calculator': [calculus_homework, graph_paper, protractor, ruler, textbook]
                     }

# A list of all ingredients, used to power the ingredient_bomb() cheat. Doesn't include the Mathematical potions.
ingredient_list = [
    shell_fragment, crab_claw, fairy_dust, serpent_scale, ink_sack, bone_bag, monster_skull, living_bark,
    ripped_cloth, beetle_shell, wing_piece, monster_fang, animal_fur, golem_rock, burnt_ash, antennae,
    ectoplasm, chain_link, unicorn_horn, demonic_essence, angelic_essence, eye_balls, mysterious_runes,
    rodent_tail, serpent_tongue, feathers, broken_crystal, slime_vial, blood_vial, water_vial
]


# "gs_stock" is a list of all items in the General Store's stock. The quality of the items
# sold is determined by the cell, store_stock[category][cell.store_level - 1]

gs_stock = {'Potions': [[s_potion, s_potion, m_potion,
                         l_potion, l_potion, x_potion],  # Health Potions

                        [s_elixir, s_elixir, m_elixir,
                         l_elixir, l_elixir, x_elixir],  # Mana Potions

                        [s_rejuv, s_rejuv, m_rejuv,
                         m_rejuv, l_rejuv, l_rejuv],  # HP + MP Potions

                        [poison_potion, poison_potion, poison_potion,
                         poison_potion, poison_potion, poison_potion],  # Poison Potion

                        [silence_potion, silence_potion, silence_potion,
                         silence_potion, silence_potion, silence_potion],  # Silence Potion

                        [blindness_potion, blindness_potion, blindness_potion,
                         blindness_potion, blindness_potion, blindness_potion],  # Blindness Potion

                        [paralyzation_potion, paralyzation_potion, paralyzation_potion,
                         paralyzation_potion, paralyzation_potion, paralyzation_potion],  # Para. Potion

                        [weakness_potion, weakness_potion, weakness_potion,
                         weakness_potion, weakness_potion, weakness_potion]],  # Weakness Potion

            'Weapons': [[bnz_swd, en_bnz_swd, stl_spr,
                         en_stl_spr, titan_axe, en_titan_axe],  # Warrior Weapons

                        [oak_stf, en_oak_stf, arc_spb,
                         en_arc_spb, rnc_stf, en_rnc_stf],  # Mage Weapons

                        [ser_knf, en_ser_knf, stiletto,
                         en_stiletto, myth_sb, en_myth_sb],  # Assassin Weapons

                        [sht_bow, en_sht_bow, lng_bow,
                         en_lng_bow, ash_cbow, en_ash_cbow],  # Ranger Weapons

                        [holy_mace, en_holy_mace, hmr_of_mgt,
                         en_hmr_of_mgt, ngt_bane, en_ngt_bane],  # Paladin Weapons

                        [brass_kncls, en_brass_kncls, bladed_gloves,
                         en_bladed_gloves, lead_bg, en_lead_bg],  # Monk Weapons

                        [kazoo, flute, snare_drum,
                         trumpet, violin, bagpipes]],  # Bard Weapons

            'Armor': [[bnz_hlm, bnz_hlm, stl_hlm,
                       stl_hlm, ori_hlm, ori_hlm],  # Warrior + Paladin Armor -- Head

                      [bnz_cst, bnz_cst, stl_cst,
                       stl_cst, ori_cst, ori_cst],  # Warrior + Paladin Armor -- Body

                      [bnz_leg, bnz_leg, stl_leg,
                       stl_leg, ori_leg, ori_leg],  # Warrior + Paladin Armor -- Legs

                      [wiz_hat, wiz_hat, myst_hat,
                       myst_hat, elem_hat, elem_hat],  # Mage + Monk Armor -- Head

                      [wiz_rob, wiz_rob, myst_rob,
                       myst_rob, elem_rob, elem_rob],  # Mage + Monk Armor -- Body

                      [wiz_gar, wiz_gar, myst_gar,
                       myst_gar, elem_gar, elem_gar],  # Mage + Monk Armor -- Legs

                      [lth_cap, lth_cap, std_cwl,
                       std_cwl, drg_cwl, drg_cwl],  # Assassin + Ranger Armor -- Head

                      [lth_bdy, lth_bdy, std_bdy,
                       std_bdy, drg_bdy, drg_bdy],  # Assassin + Ranger Armor -- Body

                      [lth_leg, lth_leg, std_leg,
                       std_leg, drg_leg],  # Assassin + Ranger Armor -- Legs

                      [linen_beret, linen_beret, wool_roundlet,
                       wool_roundlet, velvet_cavalier, velvet_cavalier],  # Bard Armor -- Head

                      [linen_shirt, linen_shirt, wool_tunic,
                       wool_tunic, velvet_doublet, velvet_doublet],  # Bard Armor -- Body

                      [linen_trousers, linen_trousers, wool_britches,
                       wool_britches, velvet_kilt, velvet_kilt]],  # Bard Armor -- Legs


            'Accessories': [[water_amulet, water_amulet, water_amulet,
                             water_amulet, water_amulet, water_amulet],

                            [fire_amulet, fire_amulet, fire_amulet,
                             fire_amulet, fire_amulet, fire_amulet],

                            [earth_amulet, earth_amulet, earth_amulet,
                             earth_amulet, earth_amulet, earth_amulet],

                            [electric_amulet, electric_amulet, electric_amulet,
                             electric_amulet, electric_amulet, electric_amulet],

                            [wind_amulet, wind_amulet, wind_amulet,
                             wind_amulet, wind_amulet, wind_amulet],

                            [grass_amulet, grass_amulet, grass_amulet,
                             grass_amulet, grass_amulet, grass_amulet],

                            [ice_amulet, ice_amulet, ice_amulet,
                             ice_amulet, ice_amulet, ice_amulet],

                            [light_amulet, light_amulet, light_amulet,
                             light_amulet, light_amulet, light_amulet],

                            [dark_amulet, dark_amulet, dark_amulet,
                             dark_amulet, dark_amulet, dark_amulet]],

            'Tools': [[shovel, shovel, shovel,
                       shovel, shovel, shovel],

                      [monster_book, monster_book, monster_book,
                       monster_book, monster_book, monster_book],

                      [musicbox, musicbox, musicbox,
                       musicbox, musicbox, musicbox],

                      [wood_lckpck, copper_lckpck, iron_lckpck,
                       steel_lckpck, mythril_lckpck, mythril_lckpck],

                      [pocket_lab, pocket_lab, pocket_lab,
                       pocket_lab, pocket_lab, pocket_lab]]}


# As the name suggests, this is a list of every item in the entire game.
# This is used for functions like find_item_with_id(), remove_item(), and add_item()
all_items = [shell_fragment, crab_claw, fairy_dust, serpent_scale, ink_sack, bone_bag, monster_skull, living_bark,
             ripped_cloth, beetle_shell, wing_piece, monster_fang, animal_fur, golem_rock, burnt_ash, antennae,
             ectoplasm, chain_link, unicorn_horn, demonic_essence, angelic_essence, eye_balls, mysterious_runes,
             rodent_tail, serpent_tongue, feathers, broken_crystal, slime_vial, blood_vial, water_vial,
             calculus_homework, graph_paper, ruler, protractor, textbook, message_joseph, message_philliard, musicbox,
             pearl_gem, ruby_gem, sapphire_gem, emerald_gem, citrine_gem, jade_gem, opal_gem, onyx_gem, diamond_gem,
             amethyst_gem, topaz_gem, garnet_gem, quartz_gem, zircon_gem, agate_gem, aquamarine_gem, wood_lckpck,
             copper_lckpck, iron_lckpck, steel_lckpck, mythril_lckpck, shovel, pocket_lab, monster_book,
             fast_travel_atlas, s_potion, m_potion, l_potion, x_potion, s_elixir, m_elixir, l_elixir, x_elixir,
             s_rejuv, m_rejuv, l_rejuv, silence_potion, poison_potion, weakness_potion, blindness_potion,
             paralyzation_potion, fists, iron_hoe, bnz_swd, en_bnz_swd, stl_spr, en_stl_spr, titan_axe, en_titan_axe,
             stn_dag, ser_knf, en_ser_knf, stiletto, en_stiletto, myth_sb, en_myth_sb, slg_sht, sht_bow, en_sht_bow,
             lng_bow, en_lng_bow, ash_cbow, en_ash_cbow, mag_twg, oak_stf, en_oak_stf, arc_spb, en_arc_spb, rnc_stf,
             en_rnc_stf, rbr_mlt, holy_mace, en_holy_mace, hmr_of_mgt, en_hmr_of_mgt, ngt_bane, en_ngt_bane,
             brass_kncls, en_brass_kncls, bladed_gloves, en_bladed_gloves, lead_bg, en_lead_bg, straw_hat, cotton_shirt,
             sunday_trousers, bnz_hlm, bnz_cst, bnz_leg, wiz_hat, wiz_rob, wiz_gar,  lth_cap, lth_bdy, lth_leg, stl_hlm,
             stl_cst, stl_leg, myst_hat, myst_rob, myst_gar, std_cwl, std_bdy, std_leg, ori_hlm, ori_cst, ori_leg,
             elem_hat, elem_rob, elem_gar, drg_cwl, drg_bdy, drg_leg, water_amulet, fire_amulet, earth_amulet,
             electric_amulet, wind_amulet, grass_amulet, ice_amulet, light_amulet, dark_amulet, no_head, no_body,
             no_legs, no_access, attract_potion_1, attract_potion_2, attract_potion_3, repel_potion_1, repel_potion_2,
             repel_potion_3, grenade_potion_1, grenade_potion_2, grenade_potion_3, missile_potion_1, missile_potion_2,
             missile_potion_3, greed_potion_1, greed_potion_2, greed_potion_3, temperance_potion_1, temperance_potion_2,
             temperance_potion_3, gamecrash_potion, garden_gloves, kazoo, flute, snare_drum, trumpet, violin, bagpipes,
             linen_beret, linen_shirt, linen_trousers, wool_roundlet, wool_tunic, wool_britches, velvet_cavalier,
             velvet_doublet, velvet_kilt]


# Writes a list of all collected gems to a .json file. Used when saving the game.
def serialize_gems(path):
    with open(path, mode='w') as j:
        json.dump(acquired_gems, j, indent=4, separators=(', ', ': '))


# Deserializes the above list. Used when loading the game.
def deserialize_gems(path):
    global acquired_gems

    with open(path) as j:
        acquired_gems = json.load(j)


# Checks to make sure there aren't any major errors with the items (may become more robust in the future)
for item1 in _c(globals()):
    if isinstance(globals()[item1], Item) and globals()[item1] not in all_items:
        print(f"{globals()[item1].item_id} not in all_items!")

for item2 in all_items:
    try:
        if not isinstance(item2.class_, list):
            print(f"{item2.item_id} has an invalid class_!")

    except AttributeError:
        pass


# ---INVENTORY SYSTEM --- #

inventory = {'q_items': [],
             'consumables': [_c(s_potion), _c(s_elixir)],
             'weapons': [],
             'armor': [],
             'tools': [_c(fast_travel_atlas), _c(musicbox)],
             'access': [],
             'misc': []}

equipped = {
    'player': {
        'weapon': _c(fists),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)
    },

    'Solou': {
        'weapon': _c(mag_twg),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)
    },

    'Chili': {
        'weapon': _c(garden_gloves),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)
    },

    'Parsto': {
        'weapon': _c(slg_sht),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)
    },

    'Adorine': {
        'weapon': _c(iron_hoe),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)
    },
    'Ravioli': {
        'weapon': _c(iron_hoe),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)

    },
    'Chyme': {
        'weapon': _c(rbr_mlt),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)
    },

    "Storm": {
        'weapon': _c(stn_dag),
        'head': _c(straw_hat),
        'body': _c(cotton_shirt),
        'legs': _c(sunday_trousers),
        'access': _c(no_access)
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
      [7] Misc. Items
       |---->[I] Equipped Items
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
                vis_cat = 'Misc. Items'

            elif cat == 'i':
                cat = 'equipped_items'
                vis_cat = 'Equipped Items'
            elif cat == 'q':
                cat = 'quests'
                vis_cat = 'Quests'

            else:
                continue

            if cat in inventory:
                if inventory[cat]:
                    if cat not in ['weapons', 'armor', 'access']:
                        pick_item(cat, vis_cat)
                        print('-'*save_load.divider_size)

                    else:
                        if [x for x in inventory[cat]]:
                            pick_item(cat, vis_cat)
                            print('-'*save_load.divider_size)

                        else:
                            print('-'*save_load.divider_size)
                            print(f'Your party has no {vis_cat}.')
                            main.s_input("\nPress enter/return ")
                            print('-'*save_load.divider_size)

                    break

                else:
                    print('-'*save_load.divider_size)
                    print(f'Your party has no {vis_cat}.')
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
# If "selling == True" that means that items are being sold, and not used.
def pick_item(cat, vis_cat, selling=False):
    while True:
        # Quests have their own function, because they aren't actually instances of the Item class
        if cat == 'quests':
            view_quests()
            return

        # Equipped items aren't actually stored in the inventory, so they need their own function to handle them
        if cat == 'equipped_items':
            manage_equipped()
            return

        # The code that prints the inventory is kind of complicated so it's located in another function
        print('-'*save_load.divider_size)
        item_ids = print_inventory(cat, vis_cat, selling)

        while True:
            chosen = main.s_input('Input [#] (or type "back"): ').lower()
            try:
                item_id = item_ids[int(chosen) - 1]

            except (IndexError, ValueError):
                if chosen in ['e', 'x', 'exit', 'b', 'back']:
                    return

                continue

            # If you're selling items at a general store, you have to call a different function
            if selling:
                sell_item(item_id)

                if not any([not i.imp for i in inventory[cat]]):
                    return

            else:
                pick_action(item_id)

                if not inventory[cat]:
                    return

            break


# Count the number of each item in the player's inventory, and display it alongside one copy of each item
def print_inventory(cat, vis_cat, selling):
    quantity_inv = []

    temp_inv = []
    for item_x in inventory[cat]:
        if item_x.item_id not in temp_inv:
            temp_inv.append(item_x.item_id)

    for item_y in temp_inv:
        quantity_inv.append((find_item_with_id(item_y).name,
                             item_y,
                             sum(i.item_id == item_y for i in inventory[cat])))

    if not selling:
        print(f"{vis_cat}: ")
        for x, y in enumerate(quantity_inv):
            print(f'      [{x + 1}] {y[0]} x {y[2]}')

        return [x[1] for x in quantity_inv]

    else:
        sellable_inv = [it for it in quantity_inv if not find_item_with_id(it[1]).imp]

        try:
            padding = len(max([it2[0] + f" x {it2[2]}" for it2 in sellable_inv], key=len))

        except ValueError:
            padding = 1

        extra_pad = len(str(len([it3[0] for it3 in sellable_inv]) + 1))

        print(f'{vis_cat}:')

        for num, b in enumerate(sellable_inv):
            fp = '-'*(padding - (len(b[0]) + len(f" x {b[2]}")) + (extra_pad - len(str(num + 1))))
            sell_value = find_item_with_id(b[1]).value//5
            print(f"      [{num + 1}] {b[0]} x {b[2]} {fp}--> {sell_value} GP each")

        return [x[1] for x in sellable_inv]


def pick_action(item_id):
    global inventory

    item = find_item_with_id(item_id)

    # Loop while the item is in the inventory
    while True:
        if any([isinstance(item, class_) for class_ in [Weapon, Armor, Accessory]]):
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
            # Items of these classes require a target to be used, so we have to acquire a target first
            if any([isinstance(item, class_) for class_ in [Accessory, Armor, HealthManaPotion, Weapon, StatusPotion]]):
                units.player.choose_target(f"Who should {use_equip} the {item.name}?", ally=True, enemy=False)

                print('-'*save_load.divider_size)
                item.use_item(units.player.target)

                return

            # Other items can just be used normally
            else:
                print('-'*save_load.divider_size)
                item.use_item(units.player)

                return

        elif action == '2':
            # Display the item description
            print('-'*save_load.divider_size)
            print(f'-{str(item.name).upper()}-')

            if hasattr(item, "ascart"):
                print(ascii_art.item_sprites[item.ascart])

            for x in main.chop_by_79(item.desc):
                print(x)

            main.s_input("\nPress enter/return ")

        elif action == '3':
            print('-'*save_load.divider_size)

            # You can't throw away important/essential items, such as one-of-a-kind tools and quest items.
            # This is to prevent the game from becoming unwinnable.
            if item.imp:
                print('Essential Items cannot be thrown away.')
                main.s_input("\nPress enter/return ")

            else:
                while True:
                    y_n = main.s_input(f'Should you really get rid of the {item.name}? | Y/N: ').lower()

                    if y_n.startswith('y'):
                        remove_item(item.item_id)

                        print(f'You toss the {item.name} aside and continues on your journey.')
                        main.s_input("\nPress enter/return ")

                        return

                    elif y_n.startswith('n'):
                        print(f'Your party decides to keep the {item.name} with them.')
                        main.s_input("\nPress enter/return ")

                        break

        elif action in ['e', 'x', 'exit', 'b', 'back']:
            return


# Trade player-owned objects for money (GP)
def sell_item(item_id):
    item = find_item_with_id(item_id)

    print('-'*save_load.divider_size)

    if hasattr(item, "ascart"):
        print(ascii_art.item_sprites[item.ascart])

    for x in main.chop_by_79(item.desc):
        print(x)

    print('-'*save_load.divider_size)

    while True:
        sell_value = item.value//5
        y_n = main.s_input(f'Sell the {item.name} for {sell_value} GP? | Y/N: ').lower()

        if y_n.startswith('y'):
            remove_item(item.item_id)
            main.party_info['gp'] += sell_value
            print(f'The shopkeeper takes the {item.name} and gives you {sell_value} GP.')
            main.s_input('\nPress enter/return ')

            return

        elif y_n.startswith('n'):
            return


def manage_equipped():
    units.player.choose_target("Choose party member to view equipment for:", ally=True, enemy=False)

    print('-'*save_load.divider_size)
    while True:
        p_equip = equipped[units.player.target.name if units.player.target != units.player else 'player']

        print(f"""{units.player.target.name}'s Equipped Items:
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
                print(f"{units.player.target.name} doesn't have anything equipped in that slot.")
                main.s_input("\nPress enter/return ")
                print('-'*save_load.divider_size)

                break

            print('-'*save_load.divider_size)
            manage_equipped_2(selected)
            print('-'*save_load.divider_size)

            break


def manage_equipped_2(selected):
    global equipped

    while True:
        print(f"""What should {units.player.target.name} do with their {selected.name}?
      [1] Unequip
      [2] Read Description""")

        while True:
            action = main.s_input('Input [#] (or type "back"): ').lower()

            if action == '1':
                if selected.item_id == "weapon_fist":
                    print('-'*save_load.divider_size)
                    print("Removing those would be difficult without causing damage.")
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    break

                else:
                    unequip_item(selected.item_id, units.player.target)
                    print('-'*save_load.divider_size)
                    print(f'{units.player.target.name} unequips the {selected.name}.')
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

        if dia_:
            while fizz:
                if choice.startswith("f"):
                    print("Finished:")

                else:
                    print("Active:")

                for num, x in enumerate(dia_):
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


# Cheat used for testing the alchemy kit. Adds 'num' random ingredients to the player's inventory.
def ingredient_bomb(num):
    for ingredient in random.sample(ingredient_list, num):
        add_item(ingredient.item_id)


# Searches the all_items list, and returns the item that has the given item_id.
# If it can't find anything, it returns False (this shouldn't ever happen in this game, but could be
# useful if someone else is making something with this engine)
def find_item_with_id(item_id):
    for x in all_items:
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

    if item_id == 'musicbox' and main.party_info['musicbox_process']:
        main.party_info['musicbox_process'].terminate()
        main.party_info['musicbox_process'] = None
        sounds.play_music(main.party_info['music'])

    this_item = _c(find_item_with_id(item_id))

    for z in inventory[this_item.cat]:
        if z.item_id == this_item.item_id:
            inventory[this_item.cat].remove(z)
            return True

    return False


# Utilizes add_item() and remove_item() to equip/unequip items, and remove/add them to the inventory
def equip_item(item_id, equipper):
    global equipped

    this_item = _c(find_item_with_id(item_id))
    inv_name = equipper.name if equipper != units.player else 'player'

    if isinstance(equipped[inv_name][this_item.part], Item):
        if equipped[inv_name][this_item.part].item_id not in ["weapon_fist",
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
            j_inventory[category].append(item.item_id)

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
            if find_item_with_id(item_id):
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
for item1 in all_items:
    if find_item_with_id(item1.item_id) != item1:
        print(f"{item1.item_id} doesn't have a unique item_id!")
