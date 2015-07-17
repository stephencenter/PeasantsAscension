#   This file is part of PythoniusRPG.
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
import time
import copy
import random
import msvcrt

import pygame

import inv_system
import world
import npcs
import items
import pets
import text_scroll
import sounds
import ascii_art

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
    def __init__(self, name, desc, people, x, y, inn=True, inn_cost=0,
                 gen_store=True, gs_level=1, pet_shop=False, ps_level=1, wtrmelon_store=False):

        self.name = name  # The town's name (i.e. New York City)
        self.desc = desc  # A brief description of the town

        self.x = x  # X-coordinate on map
        self.y = y  # Y-coordinate on map

        self.people = people  # A list that contains the NPCs you can talk to

        self.inn = inn  # If True, the town contains an inn
        self.inn_cost = inn_cost  # How much money it costs to sleep at the inn

        self.gen_store = gen_store  # If True, the town contains a General Store
        self.gs_level = gs_level  # The higher this value is, the better the
                                  # items the store will sell.

        self.pet_shop = pet_shop  # If True, the town contains a Pet Shop
        self.ps_level = ps_level  # The higher this value, the better te pets the shop will
                                  # allow you to purchase.

        self.wtrmelon_store = wtrmelon_store  # Only used for one specific quest.
                                              # Definitely not a blatant ripoff of Apple Inc...

    def town_choice(self):
        print('-'*25)
        print('Welcome to {0}!\n{1}'.format(self.name, '-'*25))

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
                    if self.gen_store or self.inn or self.pet_shop or self.wtrmelon_store:
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
                    print('-'*25)
                    main.player.player_info()
                    print('-'*25)

                elif choice == '5':
                    print('-'*25)
                    inv_system.pick_category()
                    print('-'*25)

                elif choice.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    pygame.mixer.music.load(world.position['reg_music'])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(main.music_vol)
                    print('-'*25)
                    return

                else:
                    continue

                break

    def new_location(self, add=True):  # Translate the location of newly-found towns
        if self.y >= 0:  # into a string, then add to inventory.
            foo = "\u00b0N"
        else:
            foo = "\u00b0S"

        if self.x >= 0:
            bar = "\u00b0E"
        else:
            bar = "\u00b0W"

        spam = ''.join([self.name, ': ', str(self.y), foo, ', ', str(self.x), bar])
        if add:
            if spam not in inv_system.inventory['coord']:
                inv_system.inventory['coord'].append(spam)
                print('-'*25)
                print("{0}'s location has been added to your coordinates.".format(self.name))

                main.misc_vars['visited_towns'].append(self.name)
        else:
            return spam

    def inside_town(self):
        gen_words = ['g']
        inn_words = ['i']
        pet_words = ['p']
        watermelon_words = ['w']
        buildings = []
        while True:
            spam = False
            # (if anyone knows how to simplify this, please tell me!)
            if self.inn and not self.gen_store and not self.pet_shop:
                print('There is an [I]nn in this town.')
                buildings = inn_words

            elif self.gen_store and not self.inn and not self.pet_shop:
                print('There is a [G]eneral Store in this town.')
                buildings = gen_words

            elif self.pet_shop and not self.inn and not self.gen_store:
                print('There is a [P]et Shop in this town.')
                buildings = pet_words

            elif self.pet_shop and self.inn and not self.gen_store:
                print('There is an [I]nn and a [P]et Shop in this town.')
                buildings = inn_words[:]
                buildings.extend(pet_words)

            elif self.pet_shop and self.gen_store and not self.inn:
                print('There is a [G]eneral Store and a [P]et Shop in this town.')
                buildings = gen_words[:]
                buildings.extend(pet_words)

            elif self.gen_store and self.inn and not self.pet_shop:
                print('There is a [G]eneral Store and an [I]nn in this town.')
                buildings = gen_words[:]
                buildings.extend(inn_words)

            elif self.gen_store and self.inn and self.pet_shop:
                print('There is an [I]nn, a [P]et Shop, and a [G]eneral Store in this town.')
                buildings = inn_words[:]
                buildings.extend(gen_words)
                buildings.extend(pet_words)

            elif self.wtrmelon_store:
                print('There is a... [W]atermelon store? Why is there a store \
specifically for one fruit?')
                buildings = watermelon_words

            if buildings:
                while not spam:
                    selected = input(
                        'What building will you enter? | Input [Letter] (or type "exit"): ')

                    selected = selected.lower()

                    if any(map(selected.startswith, buildings)):
                        pygame.mixer.music.load('Music/Mayhem in the Village.ogg')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(main.music_vol)

                        if selected.startswith('g'):
                            self.town_gen()
                        elif selected.startswith('i'):
                            self.town_inn()
                        elif selected.startswith('w'):
                            self.watermelon()
                        else:
                            self.town_pet()

                        print('-'*25)

                        pygame.mixer.music.load('Music/Chickens (going peck peck peck).ogg')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(main.music_vol)

                        spam = True

                    elif selected in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return

    @staticmethod
    def watermelon():
        # Admittedly, this was just an excuse to be able to complain about how much I dislike
        # Apple Inc.
        print('-'*25)
        for sentence in [
            'Greetings, sir! Welcome to the Watermelon Inc. Store! We sell the latest',
            'Watermelon brand products, including the iSheet, the uPhone, and our most',
            'popular: the iSound! The latest one is our thinest yet, at slightly less',
            'than a micrometer thick! What purpose does that serve, you ask? No clue,',
            'I just sell the stuff. So, what will it be?'
        ]:  # They focus to much on the thickness and size of the phones, and not enough
            # on important things like battery life, reliability, and computing power.
            # I would personally pay quite a bit for an iPhone that has the same processing
            # power as the iPhone 6, but with 2-3 times the battery life.

            input(''.join(["Salesman: ", sentence, " | [ENTER] "]))
        print('-'*25)

        print('You understood absolutely none of what he said, but you get the feeling')
        input('that he wants you to buy something. | Press enter/return ')
        print('-'*25)

        while True:  # That's right, I used scientific notation. That's how serious I am.
            print('You have {0} GP'.format(main.misc_vars['gp']))
            print("""\
      [1] iSheet ---------> 6.5 x 10^96 GP
      [2] uPhone ---------> 6.4 x 10^93 GP
      [3] iSound ---------> 250 GP
      [4] wePad ----------> 7.8 x 10^93 GP
      [5] iListen --------> 6.2 x 10^94 GP
      [6] Watermelon TV --> 4.6 x 10^93 GP
      [7] iPrunes --------> 9.5 x 10^87 GP
      [8] Papaya Phone ---> 10 GP""")
            spam = True
            while spam:
                choice = input('Input [#] (or type "exit") ')

                try:
                    choice = int(choice)
                except ValueError:
                    if choice.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return

                if choice in range(1, 3) or choice in range(4, 8):  # They're expensive...
                    print('-'*25)
                    input('Salesman: \
Yeah right, as if you actually have that much money | [ENTER] ')
                    print('-'*25)
                    break

                elif choice == 8:
                    # ALL the apps have DRM, and it's difficult to bypass
                    # their rules and download apps from places
                    # other than the appstore

                    print('-'*25)
                    input("Salesman: Ha, that was a joke! Those phones don't have DRM, \
we'd never sell that! | [ENTER] ")
                    print('-'*25)

                    break

                elif choice == 3:
                    print('-'*25)
                    for sentence in [
                        "Are you sure you want to buy an iSound? It's expensive, and all",
                        "of the apps we make for it will be incompatible within a year."
                    ]:      # I bought an iPod 4th gen and pretty much every app was
                            # incompatible with it within a year. That's just stupid.
                        input(''.join(["Salesman: ", sentence, " | [ENTER] "]))

                    while True:
                        y_n = input("Do you want to buy an iSound for 250 GP? | Yes or No: ")

                        if y_n.lower().startswith("y") and main.misc_vars['gp'] >= 250:
                            print('-'*25)
                            input('*You exchange the 250 GP for the iSound thing* | [ENTER] ')
                            input('It has been added to the Quest Items page of your inventory | \
[ENTER] ')
                            print('-'*25)
                            input('Saleman: Thank you for your time, and especially for \
your money! | [ENTER] ')

                            main.misc_vars['gp'] -= 250
                            inv_system.inventory['q_items'].append(copy.copy(items.iSound))
                            spam = False
                            print('-'*25)

                            break

                        elif y_n.lower().startswith("y") and main.miscvars['gp'] < 250:
                            # The "cheap" iPhone 5C is still kinda stupidly expensive
                            print('-'*25)
                            input('Hey, you don\'t even have enough money for our "cheap" \
model! | [ENTER]')
                            print('-'*25)
                            break

                        elif y_n.lower().startswith("n"):
                            spam = False
                            print('-'*25)
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
                if main.misc_vars['gp'] >= self.inn_cost:

                    print('"Good night, Traveler."')
                    print('Sleeping...')

                    time.sleep(1)

                    while msvcrt.kbhit():
                        msvcrt.getwch()

                    main.misc_vars['gp'] -= self.inn_cost

                    main.player.hp = copy.copy(main.misc_vars['hp_p'])
                    main.player.mp = copy.copy(main.misc_vars['mp_p'])
                    print('Your HP and MP have been fully restored. ')

                    if main.player.status_ail != 'none':
                        main.player.status_ail = 'none'
                        print('You have been relieved of your status ailment. ')

                    print('-'*25)

                    main.save_game()

                else:
                    print('"...You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')

                return

            elif choice.startswith('n'):
                return

    def town_gen(self):  # Let the player purchase items from the General Store
        stock = {}  # A dictionary containing objects the player can purchase
        for category in inv_system.gs_stock:
            stock[category] = []
            for item_group in inv_system.gs_stock[category]:
                stock[category].append(item_group[self.gs_level - 1])

        stock['Other'] = [items.shovel, items.divining_rod]
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
      [1] Potions
      [2] Weapons
      [3] Armor
      [4] Accessories
      [5] Other
      [6] All""")
                while True:
                    spam = input('Input [#] (or type "back"): ')
                    if spam == '1':
                        item_category = 'Potions'

                    elif spam == '2':
                        item_category = 'Weapons'

                    elif spam == '3':
                        item_category = 'Armor'

                    elif spam == '4':
                        item_category = 'Accessories'

                    elif spam == '5':
                        item_category = 'Other'

                    elif spam == '6':
                        item_category = 'All'

                    elif spam in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
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

                    print('You have {0} GP'.format(main.misc_vars['gp']))
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
                            confirm = input(
                                "\"Ya want {0} {1}? It'll cost ya {2} GP.\" | Yes or No: ".format(
                                    'these' if str(i).endswith('s') else 'this', str(i), i.buy))

                            confirm = confirm.lower()

                            if confirm.startswith('y'):
                                if main.misc_vars['gp'] >= i.buy:
                                    inv_system.inventory[i.cat].append(i)
                                    main.misc_vars['gp'] -= i.buy

                                    print('-'*25)
                                    input('You purchase the {0} (-{1} \
GP). (Press enter/return).'.format(i, i.buy))
                                    print('-'*25)

                                else:
                                    input('"Hey, you don\'t even have enough GP for this \
{0}!" (Press enter/return) '.format(i))
                                    print()

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
      [5] Pets
      [6] Miscellaneous""")
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
                            cat = 'pets'
                            vis_cat = 'Pets'
                        elif cat == '6':
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

    def town_pet(self):
        pet_list = [[pets.pet_fox, pets.pet_cherub],
                    [pets.pet_sapling, pets.pet_viper],
                    [pets.pet_dove, pets.pet_wolf],
                    [pets.pet_dragon, pets.pet_doe]][self.ps_level - 1]

        padding = len(max([x.name for x in pet_list], key=len))

        print('-'*25)
        print('Welcome, adventurer!')
        print('-'*25)

        spam = True

        while spam:
            print("Here's what we have to offer:",
                  ''.join(["\n      [{0}] {1} {2}--> {3}".format(
                      num + 1, pet, ' '*(padding - len(pet.name)), pet.cost)
                      for num, pet in enumerate(pet_list)]))

            print("You have {0} GP.".format(main.misc_vars['gp']))

            while True:
                chosen = input('Input [#] (or type "exit"): ')

                try:
                    chosen = int(chosen) - 1
                    if chosen < 0:
                        continue

                except ValueError:
                    chosen = chosen.lower()

                    if chosen in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        spam = False
                        break

                    else:
                        continue

                try:
                    chosen_pet = pet_list[chosen]
                except IndexError:
                    continue

                print('-'*25)
                print('{0}: {1}'.format(chosen_pet, chosen_pet.desc))
                print('-'*25)

                while True:
                    y_n = input(
                        "You want this {0}? That would cost you {1} GP. | Yes or No: ".format(
                        chosen_pet, chosen_pet.cost))

                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        if main.misc_vars['gp'] >= chosen_pet.cost:
                            print('-'*25)
                            print("You received a {0} pet!".format(chosen_pet))
                            print('You give the shopkeeper {0} GP.'.format(chosen_pet.cost))
                            main.misc_vars['gp'] -= chosen_pet.cost

                            inv_system.inventory['pets'].append(copy.copy(chosen_pet))

                            print('-'*25)

                        else:
                            print('-'*25)
                            print("Hey, come on! You don't even have enough money for this!")
                            print('-'*25)

                        break

                    elif y_n.startswith('n'):
                        print('-'*25)
                        break

                break

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


# List of Towns:

# Nearton is the player's hometown.
town1 = Town('Nearton', """Nearton: A small village in the central region of t\
he Forest.
It is in this very town where numerous brave adventurers have begun
their journey. Nearton has a general store, an inn, and a few small houses.
An old man is standing near one of the houses, and appears to be very
troubled about something.""", [npcs.philliard, npcs.alfred, npcs.sondalar, npcs.saar], 0, 1)

# Southford is essentially the tutorial town. It's easy to find, and there are three NPCs
# that all give helpful advice about the game.
town2 = Town('Southford', """Southford: A fair-size town in the central-southe\
rn region of the Forest.
Many of the residents of this town own pets, which can often be seen wandering the
street. Pets can be bought at the pet-shop located in the north-east part of the
town. The inhabitants of this town are known for being quite wise, and may
provide you with helpful advice.""",
             [npcs.wesley, npcs.elisha, npcs.lazaro], -2, -6, inn_cost=2, pet_shop=True)

town3 = Town('Overshire', """Overshire: A city in the northwestern region of the Forest.
Overshire is the capital of Pythonia, and as such is very densely populated.
The city is separated into three sectors: the upper-class inner portion
consisting of castle surrounded by reinforced stone walls, a lower-class
outer portion comprised of smalls buildings and huts, and a middle-class
section situated in between. As an outsider, you are forbidden to enter the
upper two, but are welcome to do as you wish in the lower.""",
             [npcs.stewson, npcs.jeffery, npcs.harthos, npcs.typhen],
             -11, 13, inn_cost=5, gs_level=2)

town4 = Town('Charsulville', """Charsulville: A plain village in the south east
region of the Forest. It is home to nothing special, although it's cheap
inn service and higher-quality products it sells more than makes up for this.
There is a ragged beggar standing in the middle of the road.""", [npcs.ethos, npcs.joseph],
             19, -7, inn_cost=2, gs_level=2)

town5 = Town('Fort Sigil', """Fort Sigil: A small village in the northern region
of the Forest. The citizens of this town have worked tremendously hard to
convert the rarely-used fort into a hospitable village, and have done
fairly well. Despite it's rich backstory, Fort Sigil doesn't get many
visitors. Perhaps there's a reason...""", [npcs.seriph, npcs.rivesh],
             2, 22, gs_level=3)

town6 = Town('Tripton', """Tripton: When the town of Tripton was being built,
the people working on the project failed to notice that another town,
Fallville, just so happened to be located mere meters away from the
new town's borders. This has led to a bit of a rivalry between the
two towns, particularly between the village leaders.""", [npcs.kyle],
             -10, -24, inn_cost=3, gs_level=3)

town7 = Town('Fallville', """Fallville: When the town of Tripton was being built,
the people working on the project failed to notice that another town,
Fallville, just so happened to be located mere meters away from the
new town's borders. This has led to a bit of a rivalry between the
two towns, particularly between the village leaders.""", [npcs.krystal, npcs.frederick],
             -12, -23, gs_level=2, pet_shop=True)

town8 = Town('Parceon', """Parceon: A highly populated town renown for it's rich
magical background. Parceon is home to the famous Sorcerers' Guild,
a group of unbelievably skilled and wise mages. The head of the guild,
Azura, lives in a large tower in the southwest side of the town.""",
             [npcs.azura], 28, 24, gs_level=3)

town9 = Town('Sardooth', """Sardooth: A ghost town. There has not been a single
permanant inhabitant of this town for more than 75 years. It is completely
run down, with most of the buildings having been destroyed in the Pythonian
Revolution. While this town may seem interesting and historic, there is nothing
of value here.""",
             [], -25, 29, inn=False, gen_store=False)

town10 = Town('Principalia', """Principalia: Principalia is the home of
King Pythonius II. The main attraction here is the Pytheror Building, a
medium-large cottage that the original King Pythonius I had lived in
centuries ago. Every Monarch to date has decided to instead live in
the Overshire Castle, with the exception of the current monarch,
Pythonius. Pythonius II has changed several things since his ancestor
lived here, however. The cottage now has access to running water,
and the cottage is surrounded by a ring of 12 archer towers, each with
2 crossbowmen and one archer at the top. Each tower is about
100 yards from the cottage. In addition, there are numerous guards
standing watch all around the building. One guard happens to catch
your attention - probably because she just screamed "HALT!" at you.""",
              [npcs.sakura], -44, 20, gen_store=False, inn=False)

town11 = Town('New Ekanmar', """New Ekanmar: The home of the Flyscorian Embassy in
Pythonia. Prior to the Pythonian Revolution, this town was the location of
a large portion of Flyscoria's troops in Pythonia. The Pythonians drove much of
them out, but a large number of them defected to the Pythonian side and stayed.
After the war, the citizens gave up their weapons and became a peaceful town.
The vast majority of the inhabitants of this town are, naturally, Flyscors.
It seems that the Flyscorian Royal Family is visiting here - perhaps you can
talk with them for a bit.""",
              [npcs.f_jones, npcs.stravi, npcs.caesar], 3, 39, gs_level=3)

town12 = Town('Ravenstone', """Ravenstone: Ravenstone is a natural sanctuary,
home to dozens upon dozens of different animals and plantlife. Naturally,
the majority population of Ravenstone consists of Druids and
other nature-magicians. Ravenstone is also the home of the Druids'
section of the Sorcerers' Guild. Vegetation grows on almost
every building and statue in the town. When the population of
the town is calculated, animals are counted as people. More than
35% of the population are various species of animals.""",
              [npcs.strathius], -30, -39, gs_level=3, pet_shop=True, ps_level=2)

town13 = Town('Ambercreek', """Ambercreek: Ambercreek is a large mining town
located in the Terrius Mt. Range. The Chin'toric embassy can be found
in the middle of this town surrounded by large stone walls and a few
guard-towers. Sugulat, the King of Chin'tor, can often be found mining
on the outskirts of town. A very troubled-looking old man is in
the southwest portion of the town near a few smaller houses.""",
              [npcs.raidon, npcs.sugulat], -51, 7, gs_level=4, inn_cost=15)

town14 = Town('Whistumn', """Whistumn: An ancient city situated on the border
between the Arcadian Desert and the Central Forest. The inhabitants of this town
are known for their skepticism and reasoning. Many of them are scientists and are
skilled mathematicians and engineers. This town has an ongoing rivalry with
the town of Parceon because of their magical background, but this appears
to be mostly one-sided. A saddened-looking woman and her husband are sitting
on the steps of the general store.""",
              [npcs.polmor, npcs.serena], 52, 12, gs_level=4,
              inn_cost=13, pet_shop=True, ps_level=3)

town15 = Town("Hatchnuk", """Hatchnuk: Hatchnuk is the only remaining town in Pythonia
that still has cases of "Hatchnuk's Blight", a plauge-like disease that
killed hundreds of thousands of people during the 10th and 11th centuries.
Something about the strand that infects Hatchnuk seems to make it completely
incurable, as the disease has been running rampant for the past four centuries.
The economy of Hatchnuk has entirely collapsed, as the risk of spreading disease
is far too great for people to be walking out in the open doing business together.
As a result, there are no buildings that you are able to enter, and no people to talk
to. The only people who are around to speak to are the guards, but their plague-doctor-esque
apparel and stern looks make it clear that they are not in the mood for chit-chat.""",
              [], 63, 17, gen_store=False, inn=False)

town16 = Town("Cesura", """Cesura: A town of great historical significance.
This town was named after King Cesura I, the war general during the Pythonian Civil War
who helped to reunite the nation's six regions. Cesura was built on top of the site
of the Battle of Parchak, the definitive battle in the Civil War that Cesura used
to help the Central Forest win. There is a large monument to the King in the middle of
town, with the words "Here's to prosperity" written on a plaque at its feet.
An interesting thing to note is that Cesura is the only town that has a train
station. Construction of the town of Cesura was outsourced to Elysium, who is
the most technologically advanced civilization on the planet by far, having
developed and perfected the Steam Engine and later the Train before the year
1300 A.D.""",
              [npcs.bamdeliit], 58, 123, gen_store=False, inn=False, wtrmelon_store=True)

town17 = Town("Sanguion", """Sanguion: Sanguion is a save-haven for vampires. Vampires
are feared throughout Pythonia, so this fairly unknown town is the only place they
can go without being persecuted. The vampires in this town are peacful, and
actually refuse to drink the blood of intelligent lifeforms. As a matter of fact,
non-vampires who are afraid of vampires are actually more of a threat to civilization
than the actual vampires are! They look very friendly, although a few of them do look
quite scared for some reason. Perhaps you should investigate.""",
              [npcs.pime, npcs.ariver], -96, -67, gs_level=5, inn_cost=18,
              pet_shop=True, ps_level=2)

town18 = Town("Lamtonum", """"Lantonum: Lantonum is a small town that has the best
forge in all of Arcadia. Nearly 2/3s of all citizens of this town are
experienced blacksmiths, and 90% of all ores and minerals mined
in Chin'tor or Ambercreek are brought here. It is one of the wealthiest
cities in all of the desert region due to its Mythril, Magestite, and
Necrite exports.""", [npcs.matthew],
              72, 69, gs_level=4, pet_shop=True, ps_level=3)

small_house1 = Town('Small Cottage', """Small Cottage: As the name would suggest,
this area only has a small cottage. An old man is tending to his
flock in a small pasture behind the building. There doesn't appear
be any other people near here.""", [npcs.alden],
                    -12, -26, inn=False, gen_store=False, pet_shop=True, ps_level=2)


class StairwayToAethus(Town):
    def __init__(self, name, desc, people, x, y, inn=False, inn_cost=0,
                 gen_store=False, gs_level=1, pet_shop=False, ps_level=1):
        Town.__init__(self, name, desc, people, x, y, inn, inn_cost,
                      gen_store, gs_level, pet_shop, ps_level)

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
                time.sleep(1)
                sounds.foot_steps.play()
                print('Climbing...')
                time.sleep(1)
                sounds.foot_steps.play()
                print('Climbing...')
                time.sleep(1)
                sounds.foot_steps.play()
                print('Still climbing...')
                time.sleep(1)

                input("After several hours of climbing the staircase, \
you finally arrive at the top | Press enter/return ")

                main.position['x'] = 0
                main.position['y'] = 0
                main.position['is_aethus'] = True
                main.position['reg'] = 'Aethus'
                main.position['avg'] = 0

                main.position['reg_music'] = 'Music/Island of Peace.ogg'
                world.save_coords(0, 0)

                print('-'*25)
                print('You have left the Glacian Plains region and are now entering the Aethus.')
                print('-'*25)

                pygame.mixer.music.load(main.position['reg_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                return

            elif choice.lower().startswith('n'):
                return

to_aethus = StairwayToAethus("New Babylon", None, None, -84, -84)


class StairwayFromAethus(Town):
    def __init__(self, name, desc, people, x, y, inn=False, inn_cost=0,
                 gen_store=False, gs_level=1, pet_shop=False, ps_level=1):
        Town.__init__(self, name, desc, people, x, y, inn, inn_cost,
                      gen_store, gs_level, pet_shop, ps_level)

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
                time.sleep(1)
                sounds.foot_steps.play()
                print('Zipping...')
                time.sleep(1)
                input("Amazing, that was much faster! | Press enter/return ")

                main.position['x'] = -84
                main.position['y'] = -84
                main.position['is_aethus'] = False
                main.position['reg'] = 'Tundra'
                main.position['avg'] = -84

                main.position['reg_music'] = 'Music/Arpanauts.ogg'
                world.save_coords(-84, -84)

                print('-'*25)
                print('You have left the Aethus and are now entering the Tundra region.')
                print('-'*25)

                pygame.mixer.music.load(main.position['reg_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                return

            elif choice.lower().startswith('n'):
                return

town_list = [town1, town2, town3, town4, town5, town6, town7,
             town8, town9, town10, town11, town12, town13, town14,
             town15, town16, town17, town18,
             small_house1, to_aethus]

town19 = Town("Valenfall", """Not much is known about the ancient city of Valenfall.
It's inhabitants claim that it was lifted up from the mainland several millenia ago
by his Divinity. The gods supposedly used Valenfall as the cornerstone, constructing
all of the surrounding land of Aethus around it. Valenfall is deeply intertwined with
nature, and houses a petshop that sells rather... "unusual" pets.
""", [npcs.fitzgerald], 5, 12, inn_cost=2, gs_level=4, pet_shop=True, ps_level=4)

to_mainland = StairwayFromAethus("Old Babylon", None, None, 0, 0)


aethus_towns = [to_mainland, town19]


def search_towns(pos_x, pos_y, enter=True):
    # Check to see if there is a
    # town where the player is located

    available_towns = town_list if not main.position['is_aethus'] else aethus_towns
    for town in available_towns:

        if town.x == pos_x and town.y == pos_y:

            if enter:
                print('-'*25)

                sounds.item_pickup.play()

                while True:

                    if town.new_location(add=False) not in inv_system.inventory['coord']:
                        y_n = input('There is a town nearby. \
Do you wish to investigate? | Yes or No: ')

                    else:
                        y_n = input('The town of {0} is nearby. \
Do you want to visit it? | Yes or No: '.format(town.name))

                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        pygame.mixer.music.load('Music/Chickens (going peck peck peck).ogg')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(main.music_vol)
                        world.save_coords(town.x, town.y)
                        town.new_location()
                        town.town_choice()

                        return

                    elif y_n.startswith('n'):
                        print('-'*25)
                        return

            else:
                return True

    else:
        return False

# import math
#
# for x_town in town_list:
#     x = abs(x_town.x)
#     y = abs(x_town.y)
#     pos = (x + y)/2
#     print(x_town.name, math.ceil(pos/(125/8)), x_town.gs_level)