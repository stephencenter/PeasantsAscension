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

import pygame

import inv_system
import world
import npcs
import items
import pets

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100, buffer=1024)
pygame.mixer.init()


class Town:
    def __init__(self, name, desc, people, x, y, inn=True, inn_cost=0,
                 gen_store=True, gs_level=1, pet_shop=False, ps_level=1):

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
                    if self.gen_store or self.inn or self.pet_shop:
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
        else:
            return spam

    def inside_town(self):
        gen_words = ['g']
        inn_words = ['i']
        pet_words = ['p']
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
                        else:
                            self.town_pet()

                        print('-'*25)

                        pygame.mixer.music.load('Music/Chickens (going peck peck peck).ogg')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(main.music_vol)

                        spam = True

                    elif selected in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return

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

        stock['Others'] = [items.shovel, items.divining_rod]

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
      [4] Other""")
                while True:
                    spam = input('Input [#] (or type "back"): ')
                    if spam == '1':
                        item_category = 'Potions'

                    elif spam == '2':
                        item_category = 'Weapons'

                    elif spam == '3':
                        item_category = 'Armor'

                    elif spam == '4':
                        item_category = 'Other'

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
                    for num, item in enumerate(stock[item_category]):
                        print(''.join(
                            ['      [', str(num + 1), '] ', str(item), ' ',
                             '-'*(padding - len(item.name)), '--> ', str(item.buy),
                             ' GP']))

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
                        print(i.desc)
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
GP). (Press enter/return).'.format(str(i), i.buy))
                                    print('-'*25)

                                else:
                                    input('"Hey, you don\'t even have enough GP for this \
{0}!" (Press enter/return) '.format(str(i)))
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
      [4] Miscellaneous""")
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
                            cat = 'misc'
                            vis_cat = 'Miscellaneous'
                        else:
                            continue

                        if cat in inv_system.inventory:

                            if inv_system.inventory[cat]:

                                if cat not in ['weapons', 'armor']:
                                    inv_system.pick_item(cat, vis_cat, gs=True)
                                    print('-'*25)

                                else:
                                    if [x for x in inv_system.inventory[cat] if not x.equip]:
                                        inv_system.pick_item(cat, vis_cat, gs=True)
                                        print('-'*25)

                                    else:
                                        print('-'*25)
                                        print('The "{0}" category is empty...'.format(vis_cat))
                                        print('-'*25)

                                break

                            else:
                                print('-'*25)
                                print('The "{0}" category is empty...'.format(vis_cat))
                                print('-'*25)
                                break

            elif b_s in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                return

    def town_pet(self):
        pet_list = [[pets.pet_wolf],
                    [pets.pet_sapling, pets.pet_viper, pets.pet_horse]][self.ps_level - 1]

        print('-'*25)
        print('Welcome, adventurer!')
        print('-'*25)

        spam = True

        while spam:
            print("Here's what we have to offer:\n     ", "\n     ".join(
                ['[' + str(num + 1) + '] ' + str(pet) + ' --> ' + str(pet.cost)
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

                if chosen_pet in inv_system.inventory['pets']:
                    # Players can't have more than one of each pet. This is to prevent
                    # the player from getting confused as to which pet is which.

                    print('-'*25)
                    print("Hey, you already have a {0}! We aren't allowed to give you two.".format(
                        chosen_pet))
                    input("(Press Enter/Return to continue)")
                    print('-'*25)
                    break

                print('-'*25)
                print('{0}: {1}'.format(chosen_pet, chosen_pet.desc))
                print('-'*25)

                fizz = True
                while fizz:
                    y_n = input(
                        "You want this {0}? That would cost you {1} GP. | Yes or No: ".format(
                        chosen_pet, chosen_pet.cost))

                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        if main.misc_vars['gp'] >= chosen_pet.cost:
                            print('-'*25)
                            print("You received a {0} pet!".format(chosen_pet))
                            print('You give the shopkeeper {0} GP.'.format(chosen_pet.cost))

                            chosen_pet.equip = True
                            if main.player.current_pet:
                                main.player.current_pet.equip = False
                            inv_system.inventory['pets'].append(chosen_pet)
                            main.player.current_pet = chosen_pet
                            main.misc_vars['gp'] -= chosen_pet.cost

                            print('-'*25)

                        else:
                            print('-'*25)
                            print("Hey, come on! You don't even have enough money for this!")
                            print('-'*25)

                        fizz = False

                    elif y_n.startswith('n'):
                        print('-'*25)
                        fizz = False

                break

    def speak_to_npcs(self):
        while True:
            print('NPCs:\n     ', '\n      '.join(
                ["[" + str(x + 1) + "] " + npc.name for x, npc in enumerate(self.people)]))

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
town1 = Town('Nearton', """Nearton: a small village in the central region of t\
he Forest.
It is in this very town where numerous brave adventurers have begun
their journey. Nearton has a general store, an inn, and a few small houses.
An old man is standing near one of the houses, and appears to be very
troubled about something.""", [npcs.philliard, npcs.alfred], 0, 1)

town2 = Town('Southford', """Southford: A fair-size town in the central-southe\
rn region of the Forest.
This town is well-known for its wise inhabitants. Some of the elders here
are rumored to be masters of the arcane arts, and may be willing to train
your magical abilities for a reasonable price. There is a general store, an
inn, and several houses in this town.""", [npcs.wesley], -2, -6, inn_cost=2, pet_shop=True)

town3 = Town('Overshire', """Overshire: A city in the northwestern region of the Forest.
Overshire is the capital of Pythonia, and as such is very densely populated.
The city is separated into three sectors: the upper-class inner portion
consisting of castle surrounded by reinforced stone walls, a lower-class
outer portion comprised of smalls buildings and huts, and a middle-class
section situated in between. As an outsider, you are forbidden to enter the
upper two, but are welcome to do as you wish in the lower.""",
             [npcs.stewson, npcs.jeffery], -11, 13, inn_cost=5, gs_level=2)

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
             -12, -23, gs_level=2)

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

town10 = Town('Principalia', """Principalia: Principalia is the hometown of
King Pythonius II. He still lives in the same small, stone-and-wood house
that his father lived in before the war started, despite there being a
castle made for him in the nation's capital, Overshire. A few things about
the home have changed since Pythonius became king, however: There are now
a half-dozen highly-trained guards outside his house, as well as six
archer-towers arranged in a hexagonal shape around the building.""",
              [], -44, 20)

town11 = Town('Neo-Ekanmar', """Neo-Ekanmar: After Sugulat and his army overran
Flysconia  and declared the Empire of D\u00fC Haven, refugees from the
area escaped from the nation. Seeing as how most of the surrounding
states were allied against Flysconia, the refugees had no choice but
to run through Hillsbrad to Pythonia. They then established Neo-Ekanmar
as their safe-haven. Pythonia has established a non-aggression pact with
the refugees and gladly accept and protect them from danger. Seeing as
how the citizens are from Flysconia, approximately 90% of the population
are reptilian creatures.""",
              [], 3, 39, gs_level=3)

town12 = Town('Ravenstone', """Ravenstone: Ravenstone is a natural sanctuary,
home to dozens upon dozens of different animals and plantlife. Naturally,
the majority population of Ravenstone consists of Druids and
other nature-magicians. Ravenstone is also the home of the Druids'
section of the Sorcerers' Guild. Vegetation grows on almost
every building and statue in the town. When the population of
the town is calculated, animals are counted as people. More than
35% of the population are various species of animals.""",
              [], -30, -39, gs_level=3, pet_shop=True)

small_house1 = Town('Small Cottage', """Small Cottage: As the name would suggest,
this area only has a small cottage. An old man is tending to his
flock in a small pasture behind the building. There doesn't appear
be any other people near here.""", [npcs.alden],
                    -12, -26, inn=False, gen_store=False, pet_shop=True, ps_level=2)

town_list = [town1, town2, town3, town4, town5, town6,
             town7, town8, town9, town10, town11, town12, small_house1]


def search_towns(pos_x, pos_y, enter=True):
    # Check to see if there is a
    # town where the player is located
    for town in town_list:

        if town.x == pos_x and town.y == pos_y:

            if enter:
                print('-'*25)

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
