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

import copy
import random
import sys

import pygame

import ascii_art
import battle
import inv_system
import items
import sounds
import units
import save_load
import text_scroll

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()


class Town:
    def __init__(self, name, desc, people, houses, inn_cost, gs_level, town_id, has_watermelon=False):
        self.name = name  # The town's name (e.g. New York City)
        self.desc = desc  # A brief description of the town

        self.inn_cost = inn_cost  # How much money it costs to sleep at the inn
        self.gs_level = gs_level  # The higher this value is, the better the items the store will sell

        self.people = people  # A list that contains the NPCs you can talk to
        self.houses = houses  # A list that contains random buildings you can enter

        self.has_watermelon = has_watermelon  # Only used for one specific quest
        self.town_id = town_id

    def town_choice(self):
        print('-'*save_load.divider_size)
        print(ascii_art.locations['Town'])
        print(f'Welcome to {self.name}!')
        self.new_location()
        print('-'*save_load.divider_size)

        while True:
            print("""What do you wish to do?
      [1] --> Town Description
      [2] --> Buildings
      [3] --> People
      [4] --> Player Info
      [5] --> View Inventory""")

            while True:
                choice = main.s_input('Input [#] (or type "exit"): ')

                if choice == '1':
                    print('-'*save_load.divider_size)

                    for x in main.chop_by_79(self.desc):
                        print(x)

                    main.s_input('\nPress Enter/Return ')
                    print('-'*save_load.divider_size)

                elif choice == '2':
                    print('-'*save_load.divider_size)

                    if self.gs_level != -1 or self.inn_cost != -1 or self.has_watermelon:
                        self.inside_town()

                    else:
                        print("There don't appear to be any unlocked buildings to enter.")

                    print('-'*save_load.divider_size)

                elif choice == '3':
                    print('-'*save_load.divider_size)

                    if [x for x in self.people if any([y.active for y in x.conversations])]:
                        self.speak_to_npcs()

                    else:
                        print("There doesn't appear to be anyone to talk to.")

                    print('-'*save_load.divider_size)

                elif choice == '4':
                    units.player.choose_target("Select Party Member: ", ally=True, enemy=False)
                    print('-'*save_load.divider_size)
                    units.player.target.player_info()
                    print('-'*save_load.divider_size)

                elif choice == '5':
                    print('-'*save_load.divider_size)
                    inv_system.pick_category()
                    print('-'*save_load.divider_size)

                elif choice.lower() in ['e', 'x', 'exit', 'b', 'back']:
                    pygame.mixer.music.load(main.party_info['music'])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(save_load.music_vol)
                    print('-'*save_load.divider_size)
                    return

                else:
                    continue

                break

    def new_location(self, add=True):  # Translate the location of newly-found towns into a string
        mpi = main.party_info

        coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
        coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
        coord_z = f"""{mpi["z"] if mpi["z"] != 0 else ""}{"'UP" if mpi["z"] > 0 else "'DOWN" if mpi['z'] < 0 else ""}"""

        new_coords = f"{self.name}: {coord_y}, {coord_x}, {coord_z}"

        if add and new_coords not in inv_system.inventory['coord']:
            inv_system.inventory['coord'].append(new_coords)
            main.party_info['visited_towns'].append(self.name)

            print(f"{self.name}'s location has been added to the coordinates section of your inventory.")
            main.s_input("\nPress enter/return ")

        else:
            return new_coords

    def inside_town(self):
        town_words = ['i', 'g', 'u']
        watermelon_words = ['w', 'u']

        while True:
            if self.has_watermelon:
                print('There is a [W]atermelon store and some [U]nlocked houses in this town.')
                buildings = watermelon_words

            else:
                print('There is a [G]eneral Store, an [I]nn, and some [U]nlocked houses in this town.')
                buildings = town_words

            while True:
                selected = main.s_input('Where do you want to go? | Input [L]etter (or type "exit"): ').lower()

                if any(map(selected.startswith, buildings)):
                    pygame.mixer.music.load('Content/Music/Mayhem in the Village.ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(save_load.music_vol)

                    if selected.startswith('u'):
                        self.town_houses()

                    if selected.startswith('g'):
                        self.town_gen()

                    if selected.startswith('i'):
                        self.town_inn()

                    if selected.startswith('w'):
                        self.watermelon_store()

                    print('-'*save_load.divider_size)

                    pygame.mixer.music.load('Content/Music/Chickens (going peck peck peck).ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(save_load.music_vol)

                    break

                elif selected in ['e', 'x', 'exit', 'b', 'back']:
                    return

    def town_inn(self):
        print('-'*save_load.divider_size)
        print('Inn Keeper: "Greetings, Traveler!"')
        cost_string = f'"One Night is {self.inn_cost} GP."' if self.inn_cost else "It's free, y'know."

        while True:
            choice = main.s_input(f'"Would you like to stay at our inn? {cost_string}" | Y/N: ').lower()

            if choice.startswith('y'):
                print()
                if main.party_info['gp'] >= self.inn_cost:

                    print('"Goodnight, Traveler."')
                    print('Sleeping', end='')

                    sys.stdout.flush()

                    text_scroll.text_scroll('...', spacing=0.75)
                    print()

                    main.party_info['gp'] -= self.inn_cost

                    for character in [
                        units.player,
                        units.solou,
                        units.xoann,
                        units.chyme,
                        units.ran_af,
                        units.parsto,
                        units.adorine
                    ]:

                        character.hp = copy.copy(character.max_hp)
                        character.mp = copy.copy(character.max_mp)
                        character.status_ail = "none"

                    print("Your party's HP and MP have been fully restored.")
                    print('Your party has been relieved of all status ailments.')
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    save_load.save_game()

                else:
                    print('"...You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                return

            elif choice.startswith('n'):
                return

    def town_gen(self):
        # Let the player purchase items from the General Store
        # A dictionary containing objects the player can purchase

        stock = {}
        for category in items.gs_stock:
            stock[category] = []

            for item_group in items.gs_stock[category]:
                stock[category].append(item_group[self.gs_level - 1])

        stock['All'] = []

        for category in stock.keys():
            if category == 'All':
                continue

            for item in stock[category]:
                stock['All'].append(item)

        print('-'*save_load.divider_size)
        print('Merchant: "Welcome, Traveler!"')

        while True:
            eggs = False
            b_s = main.s_input('Do you want to [b]uy or [s]ell items? | Input letter (or type "exit"): ').lower()

            if b_s.startswith('b'):
                print('-'*save_load.divider_size)
                print("""Which category of items would you like to check out?
      [1] Armor
      [2] Weapons
      [3] Potions
      [4] Accessories
      [5] Tools
      [6] All""")
                while True:
                    chosen_cat = main.s_input('Input [#] (or type "back"): ')

                    if chosen_cat == '1':
                        item_cat = 'Armor'

                    elif chosen_cat == '2':
                        item_cat = 'Weapons'

                    elif chosen_cat == '3':
                        item_cat = 'Potions'

                    elif chosen_cat == '4':
                        item_cat = 'Accessories'

                    elif chosen_cat == '5':
                        item_cat = 'Tools'

                    elif chosen_cat == '6':
                        item_cat = 'All'

                    elif chosen_cat in ['e', 'x', 'exit', 'b', 'back']:
                        eggs = True
                        break

                    else:
                        continue

                    print('-'*save_load.divider_size)

                    break

                if eggs:
                    continue

                fizz = True

                while fizz:
                    padding = len(max([item.name for item in stock[item_cat]], key=len))
                    print(f"{item_cat} (Your party has {main.party_info['gp']} GP): ")

                    for num, item in enumerate(stock[item_cat]):
                        print(f"      [{num + 1}] {item} {(padding - len(item.name))*'-'}--> {item.buy} GP")

                    while True:
                        purchase = main.s_input('Input [#] (or type "back"): ').lower()

                        try:
                            i = stock[item_cat][int(purchase) - 1]

                        except (IndexError, ValueError):
                            if purchase in ['e', 'x', 'exit', 'b', 'back']:
                                print('-'*save_load.divider_size)
                                fizz = False
                                break

                            continue

                        print('-'*save_load.divider_size)
                        print(f'-{str(i).upper()}-')
                        print(ascii_art.item_sprites[i.ascart])
                        print(f'"{i.desc}"')
                        print('-'*save_load.divider_size)

                        while True:
                            spam = 'these' if str(i).endswith('s') else 'this'
                            confirm = main.s_input(f"\"Ya want {spam} {i}? It'll cost ya {i.buy} GP.\" | Y/N: ").lower()

                            if confirm.startswith('y'):
                                if main.party_info['gp'] >= i.buy:
                                    inv_system.inventory[i.cat].append(i)
                                    main.party_info['gp'] -= i.buy

                                    print('-'*save_load.divider_size)
                                    print(f'You purchase the {i} for {i.buy} GP.')
                                    main.s_input("\nPress enter/return ")
                                    print('-'*save_load.divider_size)

                                else:
                                    main.s_input(f'"Sorry, you don\'t have enough GP for that!" | Press enter/return ')

                                break

                            elif confirm.startswith('n'):
                                print()

                                break

                        break

            elif b_s.startswith('s'):
                print('-'*save_load.divider_size)
                spam = True
                while spam:
                    print("""Sellable Categories:
      [1] Armor
      [2] Consumables
      [3] Weapons
      [4] Accessories
      [5] Miscellaneous""")
                    while True:
                        cat = main.s_input('Input [#] (or type "back"): ').lower()

                        if cat in ['e', 'x', 'exit', 'b', 'back']:
                            print('-'*save_load.divider_size)
                            spam = False
                            break
                        elif cat == '1':
                            cat = 'armor'
                            vis_cat = 'Armor'
                        elif cat == '2':
                            cat = 'consumables'
                            vis_cat = 'Consumables'
                        elif cat == '3':
                            cat = 'weapons'
                            vis_cat = 'Weapons'
                        elif cat == '4':
                            cat = 'access'
                            vis_cat = 'Accessories'
                        elif cat == '5':
                            cat = 'misc'
                            vis_cat = 'Miscellaneous'
                        else:
                            continue

                        if cat in inv_system.inventory:

                            if inv_system.inventory[cat]:
                                inv_system.pick_item(cat, vis_cat, gs=True)
                                print('-'*save_load.divider_size)

                                break

                            else:
                                print('-'*save_load.divider_size)
                                print(f"You don't have any items in the {vis_cat} category.")
                                main.s_input("\nPress enter/return")
                                print('-'*save_load.divider_size)

                                break

            elif b_s in ['e', 'x', 'exit', 'b', 'back']:
                return

    def speak_to_npcs(self):
        while True:
            print('NPCs: ')

            npc_list = [x for x in self.people if any([y.active for y in x.conversations])]

            for x, npc in enumerate(npc_list):
                print(f"      [{x + 1}] {npc}")

            while True:
                npc = main.s_input('Input [#] (or type "exit"): ').lower()

                try:
                    npc = npc_list[int(npc) - 1]

                except (IndexError, ValueError):
                    if npc in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    continue

                pygame.mixer.music.load('Content/Music/Mayhem in the Village.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(save_load.music_vol)

                print('-'*save_load.divider_size)

                npc.speak()

                pygame.mixer.music.load('Content/Music/Chickens (going peck peck peck).ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(save_load.music_vol)

                break

    def town_houses(self):
        while True:
            print('-'*save_load.divider_size)
            print("Unlocked Houses:")

            for x, y in enumerate([house for house in self.houses]):
                print(f"      [{x + 1}] {y.owner}'s House")

            while True:
                chosen_house = main.s_input('Input [#] (or type "exit"): ').lower()

                try:
                    chosen_house = self.houses[int(chosen_house) - 1]

                except (IndexError, ValueError):
                    if chosen_house in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    continue

                chosen_house.enter_house()

                pygame.mixer.music.load('Content/Music/Mayhem in the Village.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(save_load.music_vol)

                break

    @staticmethod
    def watermelon_store():
        print('-'*save_load.divider_size)
        print("Salesman: ")
        for sentence in [
            'Greetings, sir! Welcome to the Watermelon Inc. Store! We sell the latest',
            'Watermelon brand products, including the iSheet, the uPhone, and our most',
            'popular: the iSound! The latest one is our thinnest yet, at slightly less',
            'than a micrometer thick! What purpose does that serve, you ask? No clue,',
            'I just sell the stuff. So, what will it be?'
        ]:

            main.s_input(sentence)

        print('-'*save_load.divider_size)
        print('Your party is very confused.')
        main.s_input("\nPress enter/return ")
        print('-'*save_load.divider_size)

        while True:
            print(f"""Shopkeeper Inventory | You have {main.party_info['gp']} GP
      [1] iSheet ---------> 1000000 GP
      [2] uPhone ---------> 1000000 GP
      [3] wePad ----------> 1000000 GP
      [4] iListen --------> 1000000 GP
      [5] Watermelon TV --> 1000000 GP
      [6] iSheet Mini ----> 1000000 GP
      [7] iSound ---------> 250 GP""")

            spam = True
            while spam:
                choice = main.s_input('Input [#] (or type "exit") ').lower()

                try:
                    choice = int(choice)

                except ValueError:
                    if choice in ['e', 'x', 'exit', 'b', 'back']:
                        return

                if choice in [1, 2, 3, 4, 5, 6]:
                    if main.party_info['gp'] >= 1000000:
                        print("Salesmen: ")
                        main.s_input("Oh wow, you actually have a million GP... Sorry these boxes are all empty,")
                        main.s_input("the only reason we have those on the item list is people don't find out")
                        print("that all we sell is the iSound.")
                        main.s_input("\nPress enter/return ")

                        break

                    print('-'*save_load.divider_size)
                    print('Salesman: Yeah right, as if you actually have that much money.')
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    break

                elif choice == 7:
                    print('-'*save_load.divider_size)

                    while True:
                        y_n = main.s_input("Do you want to buy an iSound for 250 GP? | Y/N: ").lower()

                        if y_n.startswith("y") and main.party_info['gp'] >= 250:
                            print('-'*save_load.divider_size)
                            print('*You exchange the 250 GP for the iSound thing*')
                            print('It has been added to the Quest Items page of your inventory.')
                            main.s_input("\nPress enter/return ")
                            print('-'*save_load.divider_size)

                            main.party_info['gp'] -= 250
                            inv_system.inventory['q_items'].append(copy.copy(items.iSound))
                            spam = False

                            break

                        elif y_n.startswith("y") and main.party_info['gp'] < 250:
                            print('-'*save_load.divider_size)
                            print("Salesman: Hey, you don't have enough money for that!")
                            main.s_input("\nPress enter/return ")
                            print('-'*save_load.divider_size)

                            break

                        elif y_n.startswith("n"):
                            print('-'*save_load.divider_size)
                            spam = False

                            break


class Tavern:
    def __init__(self, name, inn_cost):
        self.name = name
        self.inn_cost = inn_cost

    def get_coords(self, add=True):  # Translate the location of newly-found towns into a string
        mpi = main.party_info

        coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
        coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
        coord_z = f"""{mpi["z"] if mpi["z"] != 0 else ""}{"'UP" if mpi["z"] > 0 else "'DOWN" if mpi['z'] < 0 else ""}"""

        coords = f"{self.name}: {coord_y}, {coord_x}, {coord_z}"

        return coords

    def town_choice(self):
        print('-'*save_load.divider_size)
        print(f'Inn Keeper: "Hello, traveler! Welcome to the {self.name}!"')

        cost_string = f'"One Night is {self.inn_cost} GP."' if self.inn_cost else "It's free, y'know."

        while True:
            choice = main.s_input(f'"Would you like to stay at our inn? {cost_string}" | Y/N: ').lower()

            if choice.startswith('y'):
                print()
                if main.party_info['gp'] >= self.inn_cost:

                    print('"Goodnight, Traveler."')
                    print('Sleeping...')

                    main.smart_sleep(1)

                    main.party_info['gp'] -= self.inn_cost

                    for character in [units.player, units.solou, units.xoann,
                                      units.chyme, units.ran_af, units.parsto, units.adorine]:

                        character.hp = copy.copy(character.max_hp)
                        character.mp = copy.copy(character.max_mp)
                        character.status_ail = "none"

                    print("Your party's HP and MP have been fully restored.")
                    print('Your party has been relieved of its status ailments.')

                    print('-'*save_load.divider_size)

                    save_load.save_game()

                else:
                    print('"You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')

                pygame.mixer.music.load(main.party_info['music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(save_load.music_vol)
                print('-'*save_load.divider_size)

                return

            elif choice.startswith('n'):
                pygame.mixer.music.load(main.party_info['music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(save_load.music_vol)
                print('-'*save_load.divider_size)

                return


class House:
    def __init__(self, owner, chests):
        self.owner = owner
        self.chests = chests

    def enter_house(self):
        pygame.mixer.music.load('Content/Music/song21_02.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(save_load.music_vol)

        print('-'*save_load.divider_size)
        print(f"Your party enters the house of {self.owner}, completely undetected.")
        while True:
            available_chests = [c for c in self.chests if not (c.destroyed or c.opened)]

            lockpicks = []
            for item in inv_system.inventory['tools']:
                if 'Lockpick' in item.name:
                    lockpicks.append(item)

            print(f"Your party searches the room and stumbles upon ", end='')

            if not available_chests:
                print("nothing of interest. ")
                print(f"Your party discreetly exits {self.owner}'s house before anyone even")
                print("notices you've entered.")
                main.s_input("\nPress enter/return ")

                return

            elif len(available_chests) == 1:
                print(f"a single locked chest of Difficulty {available_chests[0].difficulty}.")
                print("The contents could be very valuable!\n")

                if not lockpicks:
                    print("Unfortunately, you do not own any lockpick kits and thus cannot attempt")
                    print(f"to open the chest. Your party discreetly exits {self.owner}'s house")
                    print("before anyone even notices you've entered.")
                    main.s_input("\nPress enter/return ")

                    return

                while True:
                    y_n = main.s_input("Attempt to unlock the chest? | Y/N: ").lower()

                    if y_n.startswith("y"):
                        target_chest = available_chests[0]
                        break

                    elif y_n.startswith("n"):
                        return

            else:
                print(f"{len(available_chests)} locked chests.")
                main.s_input("\nPress enter/return ")
                print('-'*save_load.divider_size)

                if not lockpicks:
                    print("Unfortunately, you do not own any lockpick kits and thus cannot attempt")
                    print(f"to open the chest. Your party discreetly exits {self.owner}'s house")
                    print("before anyone even notices you've entered.")
                    main.s_input("\nPress enter/return ")

                    return

                print("Which chest should your party attempt to unlock?")

                for num, chest in enumerate(available_chests):
                    print(f'      [{str(num + 1)}] Locked Chest #{str(num + 1)} --> Difficulty {chest.difficulty}')

                while True:
                    target_chest = main.s_input('Input [#] (or type "exit") ')

                    try:
                        target_chest = available_chests[int(target_chest) - 1]

                    except (IndexError, ValueError):
                        if target_chest in ['e', 'x', 'exit', 'b', 'back']:
                            return

                        continue

                    break

            target_chest.unlock_chest(max(lockpicks, key=lambda x: x.power))
            print('-'*save_load.divider_size)


class Chest:
    def __init__(self, contents, difficulty, chest_id, tries=5, destroyed=False, opened=False):
        self.contents = contents
        self.difficulty = difficulty
        self.chest_id = chest_id
        self.opened = opened
        self.destroyed = destroyed
        self.tries = tries

    def unlock_chest(self, lockpick):
        print('-'*save_load.divider_size)
        while True:
            print(f"-{self.tries if self.tries > 1 else 'ONLY ONE'} ATTEMPT{'S' if self.tries > 1 else ''} REMAINING-")
            print(f"Your party attempts to unlock the chest using your {lockpick.name}...")
            sounds.lockpicking.play()

            main.smart_sleep(2.5)

            # To unlock a chest, the player has to successfully make it through two RNG rolls.
            # The first roll is based on the chest's difficulty, and the second is based off the
            # player's lockpick quality.
            if random.randint(0, 100) < (100 - 10*self.difficulty):
                if random.randint(0, 100) < lockpick.power:
                    sounds.unlock_chest.play()
                    print('-'*save_load.divider_size)
                    print("Your party's lockpicking attempts were not in vain, as the lock")
                    print("gives way and the chest opens!")
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)

                    for n, item in enumerate(self.contents):
                        if isinstance(item, int):
                            main.party_info['gp'] += item
                            sounds.item_pickup.play()
                            main.s_input(f"Your party obtained {item} gold from the chest! | Press enter/return")

                        else:
                            inv_system.inventory[item.cat].append(item)
                            sounds.item_pickup.play()
                            an_a = 'an' if any(map(item.name.startswith, battle.vowels)) else 'a'
                            main.s_input(f"Your party obtained {an_a} {item.name} from the chest! | Press enter/return")

                    self.opened = True
                    return

            sounds.lockpick_break.play()
            print("Your party's lockpicking attempt fails.")
            main.s_input("\nPress enter/return ")

            self.tries -= 1

            if self.tries > 0:
                print('-'*save_load.divider_size)
                while True:
                    y_n = main.s_input("Attempt to open the chest again? | Y/N: ").lower()

                    if y_n.startswith('y'):
                        print('-'*save_load.divider_size)
                        break

                    elif y_n.startswith('n'):
                        return

            else:
                sounds.ally_death.play()
                print('-'*save_load.divider_size)
                print("Your party has run out of attempts, and the chest's lock breaks.")
                print("The chest is still locked, and the chest cannot be picked again.")
                main.s_input("\nPress enter/return ")

                self.destroyed = True

                return
