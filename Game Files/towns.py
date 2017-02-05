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

import sys
import time
import copy
import random
import pygame
import math

import inv_system
import world
import npcs
import items
import text_scroll
import sounds
import ascii_art
import units
import battle

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

pygame.mixer.pre_init(frequency=44100, buffer=1024)
pygame.mixer.init()


class Town:
    def __init__(self, name, desc, people, houses, inn_cost=0, gs_level=1, wtrmelon_store=False):
        self.name = name  # The town's name (i.e. New York City)
        self.desc = desc  # A brief description of the town

        self.inn_cost = inn_cost  # How much money it costs to sleep at the inn
        self.gs_level = gs_level  # The higher this value is, the better the items the store will sell

        self.people = people  # A list that contains the NPCs you can talk to
        self.houses = houses  # A list that contains random buildings you can enter

        self.wtrmelon_store = wtrmelon_store  # Only used for one specific quest

    def town_choice(self):
        print('-'*25)
        print(ascii_art.locations['Town'])
        print(f'Welcome to {self.name}!')
        self.new_location()
        print('-'*25)

        while True:
            print("""What do you wish to do?
      [1] --> Town Description
      [2] --> Buildings
      [3] --> People
      [4] --> Player Info
      [5] --> View Inventory""")

            while True:
                choice = input('Input [#] (or type "exit"): ')

                if choice == '1':
                    print('-'*25)
                    input(''.join([self.desc, '\n\nPress Enter/Return ']))
                    print('-'*25)

                elif choice == '2':
                    print('-'*25)
                    if self.gs_level != -1 or self.inn_cost != -1 or self.wtrmelon_store:
                        self.inside_town()

                    else:
                        print("There don't appear to be any unlocked buildings to enter.")

                    print('-'*25)

                elif choice == '3':
                    print('-'*25)

                    if self.people:
                        self.speak_to_npcs()

                    else:
                        print("There doesn't appear to be anyone to talk to.")

                    print('-'*25)

                elif choice == '4':
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
                        print('-'*25)
                        print("Select Party Member:")
                        print("     ", "\n      ".join(["[{0}] {1}".format(int(num) + 1, character.name)
                                                        for num, character in enumerate(target_options)]))

                        while True:
                            target = input('Input [#] (or type "exit"): ')

                            if target.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                print('-'*25)
                                break

                            try:
                                target = int(target) - 1
                            except ValueError:
                                continue

                            try:
                                target = target_options[target]
                            except IndexError:
                                continue

                            break

                    if isinstance(target, units.PlayableCharacter):
                        print('-' * 25)
                        target.player_info()
                        print('-' * 25)

                elif choice == '5':
                    print('-'*25)
                    inv_system.pick_category()
                    print('-'*25)

                elif choice.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    pygame.mixer.music.load(main.party_info['reg_music'])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(main.music_vol)
                    print('-'*25)
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
            input("\nPress enter/return ")

        else:
            return new_coords

    def inside_town(self):
        town_words = ['i', 'g', 'u']
        watermelon_words = ['w', 'u']

        while True:
            if self.wtrmelon_store:
                print('There is a [W]atermelon store and some [U]nlocked houses in this town.')
                buildings = watermelon_words

            else:
                print('There is a [G]eneral Store, an [I]nn, and some [U]nlocked houses in this town.')
                buildings = town_words

            while True:
                selected = input('Where do you want to go? | Input [L]etter (or type "exit"): ').lower()

                if any(map(selected.startswith, buildings)):
                    pygame.mixer.music.load('Music/Mayhem in the Village.ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(main.music_vol)

                    if selected.startswith('u'):
                        self.town_houses()

                    if selected.startswith('g'):
                        self.town_gen()

                    if selected.startswith('i'):
                        self.town_inn()

                    if selected.startswith('w'):
                        self.watermelon()

                    print('-'*25)

                    pygame.mixer.music.load('Music/Chickens (going peck peck peck).ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(main.music_vol)

                    break

                elif selected in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    return

    @staticmethod
    def watermelon():
        print('-'*25)
        for sentence in [
            'Greetings, sir! Welcome to the Watermelon Inc. Store! We sell the latest',
            'Watermelon brand products, including the iSheet, the uPhone, and our most',
            'popular: the iSound! The latest one is our thinnest yet, at slightly less',
            'than a micrometer thick! What purpose does that serve, you ask? No clue,',
            'I just sell the stuff. So, what will it be?'
        ]:

            input(''.join(["Salesman: ", sentence, " | [ENTER] "]))

        print('-'*25)
        print('You understood absolutely none of what he said, but you get the feeling')
        input('that he wants you to buy something. | Press enter/return ')
        print('-'*25)

        while True:
            print('You have {0} GP'.format(main.party_info['gp']))
            print("""
      [1] iSheet ---------> 1000000 GP
      [2] uPhone ---------> 1000000 GP
      [3] wePad ----------> 1000000 GP
      [4] iListen --------> 1000000 GP
      [5] Watermelon TV --> 1000000 GP
      [6] iSheet Mini ----> 1000000 GP
      [7] iSound ---------> 250 GP""")

            spam = True
            while spam:
                choice = input('Input [#] (or type "exit") ')

                try:
                    choice = int(choice)

                except ValueError:
                    if choice.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return

                if choice in [1, 2, 3, 4, 5, 6]:
                    print('-'*25)
                    input('Salesman: Yeah right, as if you actually have that much money | [ENTER] ')
                    print('-'*25)

                    break

                elif choice == 7:
                    print('-'*25)

                    while True:
                        y_n = input("Do you want to buy an iSound for 250 GP? | Yes or No: ")

                        if y_n.lower().startswith("y") and main.party_info['gp'] >= 250:
                            print('-'*25)
                            input('*You exchange the 250 GP for the iSound thing* | [ENTER] ')
                            input('It has been added to the Quest Items page of your inventory | [ENTER] ')
                            print('-'*25)
                            input('Salesman: Thank you, come back again!" | [ENTER] ')
                            print('-'*25)

                            main.party_info['gp'] -= 250
                            inv_system.inventory['q_items'].append(copy.copy(items.iSound))
                            spam = False

                            break

                        elif y_n.lower().startswith("y") and main.party_info['gp'] < 250:
                            print('-'*25)
                            input('Salesman: "Hey, you don\'t have enough money for that!" | [ENTER]')
                            print('-'*25)

                            break

                        elif y_n.lower().startswith("n"):
                            print('-'*25)
                            spam = False

                            break

    def town_inn(self):
        print('-'*25)
        print('Inn Keeper: "Greetings, Traveler!"')

        while True:
            choice = input('"Would you like to stay at our inn? {0}" | Yes or No: '.format(
                "It's free, y'know." if not self.inn_cost else ' '.join(
                    ["One Night is", str(self.inn_cost), "GP."])))

            choice = choice.lower()

            if choice.startswith('y'):
                print()
                if main.party_info['gp'] >= self.inn_cost:

                    print('"Good night, Traveler."')
                    print('Sleeping...')

                    main.smart_sleep(1)

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
                    print('Your party has been relieved of their status ailments.')
                    print('-'*25)

                    main.save_game()

                else:
                    print('"...You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')

                return

            elif choice.startswith('n'):
                return

    def town_gen(self):
        # Let the player purchase items from the General Store
        # A dictionary containing objects the player can purchase

        stock = {}
        for category in inv_system.gs_stock:
            stock[category] = []
            for item_group in inv_system.gs_stock[category]:
                stock[category].append(item_group[self.gs_level - 1])

        stock['All'] = []

        for category in stock.keys():
            if category == 'All':
                continue

            for item in stock[category]:
                stock['All'].append(item)

        print('-'*25)
        print('Merchant: "Welcome, Traveler!"')

        while True:
            eggs = False
            b_s = input('Do you want to [b]uy or [s]ell items? | Input letter (or type "exit"): ')

            b_s = b_s.lower()

            if b_s.startswith('b'):
                print('-'*25)
                print("""Which category of items would you like to check out?
      [1] Armor
      [2] Weapons
      [3] Potions
      [4] Accessories
      [5] Tools
      [6] All""")
                while True:
                    spam = input('Input [#] (or type "back"): ')

                    if spam == '1':
                        item_category = 'Armor'

                    elif spam == '2':
                        item_category = 'Weapons'

                    elif spam == '3':
                        item_category = 'Potions'

                    elif spam == '4':
                        item_category = 'Accessories'

                    elif spam == '5':
                        item_category = 'Tools'

                    elif spam == '6':
                        item_category = 'All'

                    elif spam in ['e', 'x', 'exit', 'b', 'back']:
                        eggs = True
                        break

                    else:
                        continue

                    print('-'*25)

                    break

                if eggs:
                    continue

                fizz = True

                while fizz:

                    print('You have {0} GP'.format(main.party_info['gp']))
                    print('"Well, here\'s what I have in my stock for that category: "')

                    padding = len(max([item.name for item in stock[item_category]], key=len))
                    print('-'*25, '\n', item_category, ':\n      ', end='', sep='')
                    print('\n      '.join(['[{0}] {1} {2}--> {3} GP'.format(
                        num + 1, item, '-'*(padding - len(item.name)), item.buy)
                        for num, item in enumerate(stock[item_category])]))

                    while True:
                        purchase = input('Input [#] (or type "back"): ')
                        try:
                            purchase = int(purchase) - 1
                            if purchase < 0:
                                continue

                        except ValueError:
                            purchase = purchase.lower()

                            if purchase in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                print('-'*25)
                                fizz = False
                                break

                            else:
                                continue

                        try:
                            i = stock[item_category][purchase]
                        except IndexError:
                            continue

                        print('-'*25)
                        print('-{0}-'.format(str(i).upper()))
                        print(ascii_art.item_sprites[i.ascart])
                        print('"{0}"'.format(i.desc))
                        print('-'*25)

                        while True:
                            confirm = input("\"Ya want {0} {1}? It'll cost ya {2} GP.\" | Yes or No: ".format(
                                'these' if str(i).endswith('s') else 'this', str(i), i.buy)).lower()

                            if confirm.startswith('y'):
                                if main.party_info['gp'] >= i.buy:
                                    inv_system.inventory[i.cat].append(i)
                                    main.party_info['gp'] -= i.buy

                                    print('-'*25)
                                    print(f'You purchase the {i} for {i.buy} GP.')
                                    input("\nPress enter/return ")
                                    print('-'*25)

                                else:
                                    print(f'"Hey, you don\'t even have enough GP for this {i}!"')
                                    input("\nPress enter/return ")

                                break

                            elif confirm.startswith('n'):
                                print()

                                break

                        break

            elif b_s.startswith('s'):
                print('-'*25)
                spam = True
                while spam:
                    print("""Categories:
      [1] Armor
      [2] Consumables
      [3] Weapons
      [4] Accessories
      [5] Miscellaneous""")
                    while True:
                        cat = input('Input [#] (or type "back"): ')

                        cat = cat.lower()

                        if cat in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                            print('-'*25)
                            spam = False
                            break
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
                                print('-'*25)

                                break

                            else:
                                print('-'*25)
                                input("You don't have any items in the \"{0}\" category | \
Press enter/return ".format(vis_cat))
                                print('-'*25)

                                break

            elif b_s in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                return

    def speak_to_npcs(self):
        while True:
            print('NPCs:\n     ', '\n      '.join(
                ['[{0}] {1}'.format(x + 1, npc) for x, npc in enumerate(self.people)]))

            while True:
                npc = input('Input [#] (or type "exit"): ')

                try:
                    npc = int(npc) - 1
                    if npc < 0:
                        continue
                except ValueError:

                    npc = npc.lower()

                    if npc in ['e', 'x', 'exit', 'b', 'back', 'c', 'cancel']:
                        return
                    else:
                        continue

                try:
                    npc = self.people[npc]
                except IndexError:
                    continue

                pygame.mixer.music.load('Music/Mayhem in the Village.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                print('-'*25)

                npc.speak()

                print('-'*25)

                pygame.mixer.music.load('Music/Chickens (going peck peck peck).ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                break

    def town_houses(self):
        while True:
            print("-"*25)
            print("Unlocked Houses:")

            for x, y in enumerate([house for house in self.houses]):
                print('     ', '      '.join([f"[{x + 1}] {y.owner}'s House"]))

            while True:
                chosen_house = input('Input [#] (or type "exit"): ').lower()

                try:
                    chosen_house = self.houses[int(chosen_house) - 1]

                except (IndexError, ValueError):
                    if chosen_house in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    continue

                chosen_house.enter_house()

                pygame.mixer.music.load('Music/Mayhem in the Village.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                break


class StairwayToAethus(Town):
    def __init__(self, name, desc, people, x, y):
        Town.__init__(self, name, desc, people, x, y, [])

    def town_choice(self):
        pygame.mixer.music.load('Music/CopperNickel.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print('-'*25)

        function = text_scroll.text_scroll if main.do_text_scroll else print

        function("""\
As you enter the town of New Babylon, you notice something rather odd. Not
a single door in this town is open or unlocked, including those of the shops
and other businesses. No sign of life can be seen for miles. The entire city
seems almost... frozen. Something near the center of the town catches your
eye - a large, golden staircase with a sign on it that reads "Stairway to Aethus".
The staircase seems to go on for quite a while, but you can faintly see a large
island floating up in the sky. Perhaps something is up there!""")
        print('-'*25)
        while True:
            choice = input("Climb the stairs? | Yes or No: ")
            if choice.lower().startswith('y'):
                print('-'*25)
                input('You begin to climb the staircase | Press enter/return ')
                sounds.foot_steps.play()
                print('Climbing...')
                main.smart_sleep(1)
                sounds.foot_steps.play()
                print('Climbing...')
                main.smart_sleep(1)
                sounds.foot_steps.play()
                print('Climbing...')
                main.smart_sleep(1)
                sounds.foot_steps.play()
                print('Still climbing...')
                main.smart_sleep(1)

                print("After several hours of climbing the staircase, you finally arrive at the top.")

                input("\nPress enter/return ")

                main.party_info['x'] = 0
                main.party_info['y'] = 0
                main.party_info['avg'] = 0
                main.party_info['reg'] = 'Aethus'
                main.party_info['prev_town'][0] = 0
                main.party_info['prev_town'][1] = 0
                main.party_info['is_aethus'] = True
                main.party_info['reg_music'] = 'Music/Island of Peace.ogg'

                print('-'*25)
                print('You have left the Glacian Plains region and are now entering the Aethus.')
                print('-'*25)

                pygame.mixer.music.load(main.party_info['reg_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                return

            elif choice.lower().startswith('n'):
                return


class StairwayFromAethus(Town):
    def __init__(self, name, desc, people, x, y):
        Town.__init__(self, name, desc, people, x, y, [])

    def town_choice(self):
        pygame.mixer.music.load('Music/CopperNickel.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print('-'*25)

        function = text_scroll.text_scroll if main.do_text_scroll else print

        function("""You come across the place that you entered Aethus from. It looks remarkably
similar to the town of New Babylon from the mainland. Everything is frozen in place,
and no people are anywhere to be seen. The staircase you came up in is in the middle of town,
and seeing it evokes bad memories of walking up five miles of stairs. Luckily for you,
you notice a zipline-like structure that would be much easier and faster to use.""")
        while True:
            choice = input("Go down the zipline? | Yes or No: ")

            if choice.lower().startswith('y'):
                print('-'*25)
                input('You strap yourself to the zipline using a harness | Press enter/return ')
                sounds.foot_steps.play()
                print('Zipping...')
                main.smart_sleep(1)
                sounds.foot_steps.play()
                print('Zipping...')
                main.smart_sleep(1)
                input("Amazing, that was much faster! | Press enter/return ")

                main.party_info['x'] = -84
                main.party_info['y'] = -84
                main.party_info['avg'] = -84
                main.party_info['reg'] = 'Tundra'
                main.party_info['prev_town'][0] = -84
                main.party_info['prev_town'][1] = -84
                main.party_info['is_aethus'] = False
                main.party_info['reg_music'] = 'Music/Arpanauts.ogg'

                print('-'*25)
                print('You have left the Aethus and are now entering the Tundra region.')
                print('-'*25)

                pygame.mixer.music.load(main.party_info['reg_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                return

            elif choice.lower().startswith('n'):
                return


class Tavern:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def new_location(self):
        pass

    def town_choice(self):
        print('-'*25)
        print(f'Inn Keeper: "Hello, traveler! Welcome to the {self.name}!"')

        while True:
            choice = input('"Would you like to stay at our inn? {0}" | Yes or No: '.format(
                "It's free, y'know." if not self.cost else ' '.join(["One Night is", str(self.cost), "GP."])))
            choice = choice.lower()

            if choice.startswith('y'):
                print()
                if main.party_info['gp'] >= self.cost:

                    print('"Good night, traveler."')
                    print('Sleeping...')

                    main.smart_sleep(1)

                    main.party_info['gp'] -= self.cost

                    for character in [units.player, units.solou, units.xoann,
                                      units.chyme, units.ran_af, units.parsto, units.adorine]:

                        character.hp = copy.copy(character.max_hp)
                        character.mp = copy.copy(character.max_mp)
                        character.status_ail = "none"

                    print("Your party's HP and MP have been fully restored.")
                    print('Your party has been relieved of its status ailments.')

                    print('-'*25)

                    main.save_game()

                else:
                    print('"You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')

                pygame.mixer.music.load(main.party_info['reg_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)
                print('-'*25)

                return

            elif choice.startswith('n'):
                pygame.mixer.music.load(main.party_info['reg_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)
                print('-'*25)

                return


class House:
    def __init__(self, owner, chests):
        self.owner = owner
        self.chests = chests

    def enter_house(self):
        pygame.mixer.music.load('Music/Somewhere I Went Wrong.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print('-' * 25)
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
                input("\nPress enter/return ")

                return

            elif len(available_chests) == 1:
                print(f"a single locked chest of Difficulty {available_chests[0].difficulty}.")
                print("The contents could be very valuable!\n")

                if not lockpicks:
                    print("Unfortunately, you do not own any lockpick kits and thus cannot attempt")
                    print(f"to open the chest. Your party discreetly exits {self.owner}'s house")
                    print("before anyone even notices you've entered.")
                    input("\nPress enter/return ")

                    return

                while True:
                    y_n = input("Attempt to unlock the chest? | Yes or No: ").lower()

                    if y_n.startswith("y"):
                        target_chest = available_chests[0]
                        break

                    elif y_n.startswith("n"):
                        return

            else:
                print(f"{len(available_chests)} locked chests.")
                input("\nPress enter/return ")
                print('-'*25)

                if not lockpicks:
                    print("Unfortunately, you do not own any lockpick kits and thus cannot attempt")
                    print(f"to open the chest. Your party discreetly exits {self.owner}'s house")
                    print("before anyone even notices you've entered.")
                    input("\nPress enter/return ")

                    return

                print("Which chest should your party attempt to unlock?")

                for num, chest in enumerate(available_chests):
                    print(f'      [{str(num + 1)}] Locked Chest #{str(num + 1)} --> Difficulty {chest.difficulty}')

                while True:
                    target_chest = input('Input [#] (or type "exit") ')

                    try:
                        target_chest = available_chests[int(target_chest) - 1]

                    except (IndexError, ValueError):
                        if target_chest in ['e', 'x', 'exit', 'b', 'back']:
                            return

                        continue

                    break

            target_chest.unlock_chest(max(lockpicks, key=lambda x: x.power))
            print('-'*25)


class Chest:
    def __init__(self, contents, difficulty, chest_id, tries=5, destroyed=False, opened=False):
        self.contents = contents
        self.difficulty = difficulty
        self.chest_id = chest_id
        self.opened = opened
        self.destroyed = destroyed
        self.tries = tries

    def unlock_chest(self, lockpick):
        print('-'*25)
        while True:
            print(f"-{self.tries if self.tries > 1 else 'ONLY ONE'} ATTEMPT{'S' if self.tries > 1 else ''} REMAINING-")
            print(f"Your party attempts to unlock the chest using your {lockpick.name}...")
            sounds.lockpicking.play()

            main.smart_sleep(2.5)

            # To unlock a chest, the player has to successfully make it through two RNG rolls.
            # The first roll is based on the chest's difficulty, and the second is based off the
            # player's lockpick quality.
            if random.randint(0, 100) < (100 - 10*(self.difficulty)):
                if random.randint(0, 100) < lockpick.power:
                    sounds.unlock_chest.play()
                    print('-'*25)
                    print("Your party's lockpicking attempts were not in vain, as the lock")
                    print("gives way and the chest opens!")
                    input("\nPress enter/return ")
                    print('-'*25)

                    for n, item in enumerate(self.contents):
                        if isinstance(item, int):
                            main.party_info['gp'] += item
                            sounds.item_pickup.play()
                            input(f"Your party obtained {item} gold from the chest! | Press enter/return")

                        else:
                            inv_system.inventory[item.cat].append(item)
                            sounds.item_pickup.play()
                            an_a = 'an' if any(map(item.name.startswith, battle.vowels)) else 'a'
                            input(f"""Your party obtained {an_a} {item.name} from the chest! | Press enter/return""")

                    self.opened = True
                    return

            sounds.lockpick_break.play()
            print("Your party's lockpicking attempt fails.")
            input("\nPress enter/return ")

            self.tries -= 1

            if self.tries > 0:
                print('-'*25)
                while True:
                    y_n = input("Attempt to open the chest again? | Yes or No: ").lower()

                    if y_n.startswith('y'):
                        print('-'*25)
                        break

                    elif y_n.startswith('n'):
                        return

            else:
                sounds.ally_death.play()
                print('-'*25)
                print("Your party has run out of attempts, and the chest's lock breaks.")
                print("The chest is still locked, and the chest cannot be picked again.")
                input("\nPress enter/return ")

                self.destroyed = True
                return


# AETHUS TRANSPORTS
to_mainland = StairwayFromAethus("Old Babylon", None, None, 0, 0)
to_aethus = StairwayToAethus("New Babylon", None, None, -84, -84)

# OVERWORLD TOWNS
nearton_h1_c1 = Chest([20], 1, "N-H1-C1")
nearton_h1_c2 = Chest([10, items.s_rejuv], 1, "N-H1-C2")
nearton_h1 = House("Philliard", [nearton_h1_c1, nearton_h1_c2])

nearton_h2_c1 = Chest([5, items.bone_bag, items.fairy_dust, items.feathers], 1, "N-H2-C1")
nearton_h2 = House("Alfred", [nearton_h2_c1])

town_nearton = Town('Nearton', """Nearton: A small village in the central region of the Forest.
It is in this very town where numerous brave adventurers have begun their
journey. Nearton is just your standard run-of-the-mill village: it has a
general store, an inn, and a few small houses. An old man  is standing
near one of the houses, and appears to be very troubled about something.""",
             [npcs.philliard, npcs.alfred, npcs.sondalar, npcs.saar, npcs.npc_solou],
             [nearton_h1, nearton_h2])

town_southford = Town('Southford', """Southford: A fair-size town in the central-southern region of the Forest.
The inhabitants of this town are known for being quite wise, and may
provide you with helpful advice.""",
                      [npcs.wesley, npcs.lazaro], [], inn_cost=2)

town_overshire = Town('Overshire', """Overshire: A city in the northwestern region of the Forest.
Overshire is the capital of Harconia, and as such is very densely populated.
The city is separated into three sectors: the upper-class inner portion
consisting of castle surrounded by reinforced stone walls, a lower-class
outer portion comprised of smalls buildings and huts, and a middle-class
section situated in between. As an outsider, you are forbidden to enter the
upper two, but are welcome to do as you wish in the lower.""",
             [npcs.joseph, npcs.stewson, npcs.jeffery, npcs.harthos],
             [], inn_cost=5, gs_level=2)

town_charsulville = Town('Charsulville', """Charsulville: A plain village in the south east
region of the Forest. It is home to nothing special, although it's cheap
inn service and higher-quality products it sells more than makes up for this.
There is a ragged beggar standing in the middle of the road.""", [npcs.ethos, npcs.typhen],
             [], inn_cost=2, gs_level=2)

town_fort_sigil = Town('Fort Sigil', """Fort Sigil: A small village in the northern region
of the Forest. The citizens of this town have worked tremendously hard to
convert the rarely-used fort into a hospitable village, and have done
fairly well. Despite it's rich backstory, Fort Sigil doesn't get many
visitors. Perhaps there's a reason...""",
             [npcs.seriph, npcs.rivesh], [], gs_level=3)

town_tripton = Town('Tripton', """Tripton: When the town of Tripton was being built,
the people working on the project failed to notice that another town,
Fallville, just so happened to be located mere meters away from the
new town's borders. This has led to a bit of a rivalry between the
two towns, particularly between the village leaders.""",
             [npcs.kyle], [], inn_cost=3, gs_level=3)

town_fallville = Town('Fallville', """Fallville: When the town of Tripton was being built,
the people working on the project failed to notice that another town,
Fallville, just so happened to be located mere meters away from the
new town's borders. This has led to a bit of a rivalry between the
two towns, particularly between the village leaders.""",
             [npcs.krystin, npcs.frederick], [], gs_level=2)

town_parceon = Town('Parceon', """Parceon: A highly populated town renown for it's rich
magical background. Parceon is home to the famous Sorcerers' Guild,
a group of unbelievably skilled and wise mages. The head of the guild,
Azura, lives in a large tower in the southwest side of the town.""",
             [npcs.azura], [], gs_level=3)

town_sardooth = Town('Sardooth', """Sardooth: A ghost town. There has not been a single
permanent inhabitant of this town for more than 75 years. It is completely
run down, with most of the buildings having been destroyed in the Harconian
Revolution. While this town may seem interesting and historic, there is nothing
of value here.""",
             [], [])

town_principalia = Town('Principalia', """Principalia: Principalia is the home of
King Harconius II. The main attraction here is the Pytheror Building, a
medium-large cottage that the original King Harconius I had lived in
centuries ago. Every Monarch to date has decided to instead live in
the Overshire Castle, with the exception of the current monarch,
Harconius. Harconius II has changed several things since his ancestor
lived here, however. The cottage now has access to running water,
and the cottage is surrounded by a ring of 12 archer towers, each with
2 crossbowmen and one archer at the top. Each tower is about
100 yards from the cottage. In addition, there are numerous guards
standing watch all around the building. One guard happens to catch
your attention - probably because she just screamed "HALT!" at you.""",
              [npcs.sakura], [])

town_new_ekanmar = Town('New Ekanmar', """New Ekanmar: The home of the Flyscorian Embassy in
Harconia. Prior to the Harconian Revolution, this town was the location of
a large portion of Flyscoria's troops in Harconia. The Harconians drove much of
them out, but a large number of them defected to the Harconian side and stayed.
After the war, the citizens gave up their weapons and became a peaceful town.
The vast majority of the inhabitants of this town are, naturally, Flyscors.
It seems that the Flyscorian Royal Family is visiting here - perhaps you can
talk with them for a bit.""", [npcs.f_jones, npcs.stravi, npcs.caesar], [], gs_level=3)

town_ravenstone = Town('Ravenstone', """Ravenstone: Ravenstone is a natural sanctuary,
home to dozens upon dozens of different flora and fauna. Naturally,
the majority population of Ravenstone consists of Druids and
other nature-magicians. Ravenstone is also the home of the Druids'
section of the Sorcerers' Guild. Vegetation grows on almost
every building and statue in the town. When the population of
the town is calculated, animals are counted as people. More than
35% of the population are various species of animals.""",
              [npcs.strathius], [], gs_level=3)

town_ambercreek = Town('Ambercreek', """Ambercreek: Ambercreek is a large mining town
located in the Terrius Mt. Range. The Chin'toric embassy can be found
in the middle of this town surrounded by large stone walls and a few
guard-towers. Sugulat, the King of Chin'tor, can often be found mining
on the outskirts of town. A very troubled-looking old man is in
the southwest portion of the town near a few smaller houses.""",
              [npcs.raidon, npcs.sugulat], [], gs_level=4, inn_cost=15)

town_whistumn = Town('Whistumn', """Whistumn: An ancient city situated on the border
between the Arcadian Desert and the Central Forest. The inhabitants of this town
are known for their skepticism and reasoning. Many of them are scientists and are
skilled mathematicians and engineers. This town has an ongoing rivalry with
the town of Parceon because of their magical background, but this appears
to be mostly one-sided. A saddened-looking woman and her husband are sitting
on the steps of the general store.""",
              [npcs.polmor, npcs.serena], [], gs_level=4, inn_cost=13)

town_hatchnuk = Town("Hatchnuk", """Hatchnuk: Hatchnuk is the only remaining town in Harconia
that still has cases of "Hatchnuk's Blight", a plague-like disease that
killed hundreds of thousands of people during the 10th and 11th centuries.
Something about the strand that infects Hatchnuk seems to make it completely
incurable, as the disease has been running rampant for the past four centuries.
The economy of Hatchnuk has entirely collapsed, as the risk of spreading disease
is far too great for people to be walking out in the open doing business together.
As a result, there are no buildings that you are able to enter, and no people to talk
to. The only people who are around to speak to are the guards, but their plague-doctor-esque
apparel and stern looks make it clear that they are not in the mood for chit-chat.""",
              [], [])

town_cesura = Town("Cesura", """Cesura: A town of great historical significance.
This town was named after King Cesura I, the war general during the Harconian Civil War
who helped to reunite the nation's six regions. Cesura was built on top of the site
of the Battle of Parchak, the definitive battle in the Civil War that Cesura used
to help the Central Forest win. There is a large monument to the King in the middle of
town, with the words "Here's to prosperity" written on a plaque at its feet.
An interesting thing to note is that Cesura is the only town that has a train
station. Construction of the town of Cesura was outsourced to Elysium, who is
the most technologically advanced civilization on the planet by far, having
developed and perfected the Steam Engine and later the Train before the year
1300 A.D.""",
              [npcs.bamdeliit], [], wtrmelon_store=True)

town_sanguion = Town("Sanguion", """Sanguion: Sanguion is a save-haven for vampires. Vampires
are feared throughout Harconia, so this fairly unknown town is the only place they
can go without being persecuted. The vampires in this town are peaceful, and
actually refuse to drink the blood of intelligent lifeforms. As a matter of fact,
non-vampires who are afraid of vampires are actually more of a threat to civilization
than the actual vampires are! They look very friendly, although a few of them do look
quite scared for some reason. Perhaps you should investigate.""",
              [npcs.pime, npcs.ariver], [], gs_level=5, inn_cost=18)

town_lantonum = Town("Lamtonum", """Lantonum: Lantonum is a small town that has the best
forge in all of Arcadia. Nearly 2/3s of all citizens of this town are
experienced blacksmiths, and 90% of all ores and minerals mined
in Chin'tor or Ambercreek are brought here. It is one of the wealthiest
cities in all of the desert region due to its Mythril, Magestite, and
Necrite bar exports.""",
              [npcs.matthew], [], gs_level=4)

town_capwild = Town("Capwild", """Capwild: Capwild is a medium sized town situated in the
Terrius Mt. Range. Capwild is a supplier of grains and herbs for the entire region,
and makes extensive use of terrace farming to make up for the lack of arable land.""",
              [], [], gs_level=5, inn_cost=15)

town_rymn_outpost = Town("Rymn Outpost", """Rymn Outpost: Rymn Outpost is one of the several
small villages established after the Thexian Incursion. All of the residents of this town
are soldiers or family members of soldiers, with the exception a few merchants. Rymn Outpost
is named after Rymnes, the Divinic gods of defense.""",
              [], [], gs_level=5, inn_cost=17)

cottage1 = Town('Small Cottage', """Small Cottage: As the name would suggest,
this area only has a small cottage. An old man is tending to his
flock in a small pasture behind the building. There doesn't appear
be any other people near here.""",
                [npcs.alden], [], gs_level=-1, inn_cost=-1)

# AETHUS TOWNS
a_town_valenfall = Town("Valenfall", """Not much is known about the ancient city of Valenfall.
It's inhabitants claim that it was lifted up from the mainland several millenia ago
by his Divinity. The gods supposedly used Valenfall as the cornerstone, constructing
all of the surrounding land of Aethus around it. Valenfall is deeply intertwined with
nature, and monuments depicting the nature deities can be seen on every corner.
""", [npcs.fitzgerald], [], inn_cost=2, gs_level=4)

# OVERWORLD TAVERNS
tavern1 = Tavern("The Traveling Merchant Inn", 0)
tavern2 = Tavern("The Drunken Moon Tavern ", 5)
tavern3 = Tavern("The Wandering Falcon Inn", 5)
tavern4 = Tavern("The Dancing Knight Tavern", 5)
tavern5 = Tavern("The Golden Watchman Tavern", 5)
tavern6 = Tavern("The Smiling Rapier Inn", 5)
tavern7 = Tavern("The Howling Warrior Inn", 10)
tavern8 = Tavern("The Vanishing Skull Inn", 10)
tavern9 = Tavern("The Brave Foal Tavern", 10)
tavern10 = Tavern("The Cowardly Dagger Inn", 10)
tavern11 = Tavern("The Thirsty Wizard Tavern", 15)
tavern12 = Tavern("The Painted Bard Inn", 15)

town_list = [town_nearton, town_southford, town_overshire, town_charsulville, town_fort_sigil, town_tripton,
             town_fallville, town_parceon, town_sardooth, town_principalia, town_new_ekanmar, town_ravenstone,
             town_ambercreek, town_whistumn, town_hatchnuk, town_cesura, town_sanguion, town_lantonum, town_capwild,
             town_rymn_outpost, cottage1, to_aethus]

tavern_list = [tavern1, tavern2, tavern3, tavern4, tavern5, tavern6,
               tavern7, tavern8, tavern9, tavern10, tavern11, tavern12]

aethus_towns = [to_mainland, a_town_valenfall]

aethus_taverns = []


def search_towns(enter=True):
    # Check to see if there is a
    # town where the player is located

    for town in main.party_info['current_tile'].town_list:
        if enter:
            print('-'*25)

            sounds.item_pickup.play()

            while True:
                if isinstance(town, Tavern):
                    if town.new_location(add=False) not in inv_system.inventory['coord']:
                        y_n = input("How convenient, a tavern is nearby! Do you wish to investigate? | Yes or No: ")

                    else:
                        y_n = input(f'{town.name} is nearby. Do you want to visit it? | Yes or No: ')
                else:
                    if town.new_location(add=False) not in inv_system.inventory['coord']:
                        y_n = input('There is a town nearby. Do you wish to investigate? | Yes or No: ')

                    else:
                        y_n = input(f'The town of {town.name} is nearby. Do you want to visit it? | Yes or No: ')

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    pygame.mixer.music.load('Music/Chickens (going peck peck peck).ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(main.music_vol)

                    main.party_info['prev_town'] = main.party_info['current_tile']

                    town.town_choice()

                    return

                elif y_n.startswith('n'):
                    print('-'*25)
                    return

            else:
                return True