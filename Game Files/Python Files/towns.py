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
import logging
import sys
import time
import copy
import math
import random

import items
import units
import ascii_art
import npcs
import save_load
import tiles
import sounds

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Town:
    def __init__(self, name, desc, people, town_id):
        self.name = name  # The town's name (e.g. New York City)
        self.desc = desc  # A brief description of the town
        self.people = people  # A list that contains the NPCs you can talk to
        self.town_id = town_id  # A unique identifier for each town

        self.houses = []

    def town_choice(self):
        print('-'*save_load.divider_size)
        print(f'Welcome to {self.name}!')
        print('-'*save_load.divider_size)

        while True:
            main.party_info['gamestate'] = 'town'
            main.party_info['current_town'] = self.town_id
            print("""What do you wish to do?
      [1] Town Description
      [2] Buildings
      [3] People
      [4] Player Info
      [5] View Inventory""")

            while True:
                choice = main.s_input('Input [#] (or type "exit"): ')

                if choice == '1':
                    print('-'*save_load.divider_size)

                    for x in main.chop_by_79(self.desc):
                        print(x)

                    main.s_input('\nPress enter/return ')
                    print('-'*save_load.divider_size)

                elif choice == '2':
                    print('-'*save_load.divider_size)
                    self.inside_town()
                    print('-'*save_load.divider_size)

                elif choice == '3':
                    print('-'*save_load.divider_size)

                    if [x for x in self.people if any([y.active for y in x.convos[main.party_info['current_town']]])]:
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
                    items.pick_category()
                    print('-'*save_load.divider_size)

                elif choice.lower() in ['e', 'x', 'exit', 'b', 'back']:
                    sounds.play_music(main.party_info['music'])

                    print('-'*save_load.divider_size)
                    return

                else:
                    continue

                break

    def inside_town(self):
        while True:
            print('There is a [G]eneral Store, an [I]nn, and some [U]nlocked houses in this town.')
            buildings = ['i', 'g', 'u']

            while True:
                selected = main.s_input('Where do you want to go? | Input [L]etter (or type "exit"): ').lower()

                if any(map(selected.startswith, buildings)):
                    sounds.play_music('../Music/Mayhem in the Village.ogg')

                    if selected.startswith('u'):
                        self.town_houses()

                    if selected.startswith('g'):
                        self.town_gen()

                    if selected.startswith('i'):
                        self.town_inn()

                    print('-'*save_load.divider_size)

                    sounds.play_music('../Music/Chickens (going peck peck peck).ogg')

                    break

                elif selected in ['e', 'x', 'exit', 'b', 'back']:
                    return

    @staticmethod
    def town_inn():
        print('-'*save_load.divider_size)
        print('Inn Keeper: "Greetings, Traveler!"')

        while True:
            choice = main.s_input(f'"Would you like to stay at our inn? It\'s free, y\'know." | Y/N: ').lower()

            if choice.startswith('y'):

                print('\n"Goodnight, Traveler."')
                print('Sleeping', end='')

                sys.stdout.flush()

                main.text_scroll('...', spacing=0.75)
                print()

                for character in [
                    units.player,
                    units.solou,
                    units.chili,
                    units.chyme,
                    units.storm,
                    units.parsto,
                    units.adorine
                ]:

                    character.hp = copy.copy(character.max_hp)
                    character.mp = copy.copy(character.max_mp)
                    character.status_ail = ['alive']

                print("Your party's HP and MP have been fully restored.")
                print('Your party has been relieved of all status ailments.')
                main.s_input("\nPress enter/return ")
                print('-'*save_load.divider_size)

                save_load.save_game()

                return

            elif choice.startswith('n'):
                return

    def town_gen(self):
        # A dictionary containing objects the player can purchase. This list is populated based on the current
        # cell's store_level attribute
        stock = {'All': []}

        store_level = tiles.find_cell_with_tile_id(main.party_info['current_tile'].tile_id).store_level - 1

        for category in items.gs_stock:
            stock[category] = []

            for item_group in items.gs_stock[category]:
                stock[category].append(item_group[store_level])
                stock['All'].append(item_group[store_level])

        print('-'*save_load.divider_size)
        print('Merchant: "Welcome, Traveler!"')

        while True:
            chosen = main.s_input('Do you want to [b]uy or [s]ell items? | Input letter (or type "exit"): ').lower()

            if chosen.startswith('b'):
                print('-'*save_load.divider_size)
                self.buy_choose_cat(stock)

            elif chosen.startswith('s'):
                print('-'*save_load.divider_size)
                spam = True
                while spam:
                    print("""Sellable Categories:
      [1] Armor
      [2] Consumables
      [3] Weapons
      [4] Accessories
      [5] Tools
      [6] Misc. Items""")
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
                            cat = 'tools'
                            vis_cat = 'Tools'
                        elif cat == '6':
                            cat = 'misc'
                            vis_cat = 'Misc. Items'
                        else:
                            continue

                        if items.inventory[cat] and any([not i.imp for i in items.inventory[cat]]):
                            items.pick_item(cat, vis_cat, selling=True)
                            print('-'*save_load.divider_size)

                            break

                        else:
                            print('-'*save_load.divider_size)
                            print(f"You don't have any sellable items in the {vis_cat} category.")
                            main.s_input("\nPress enter/return")
                            print('-'*save_load.divider_size)

                            break

            elif chosen in ['e', 'x', 'exit', 'b', 'back']:
                return

    def buy_choose_cat(self, stock):
        while True:
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
                    print('-' * save_load.divider_size)

                    return

                else:
                    continue

                print('-' * save_load.divider_size)
                self.buy_choose_item(item_cat, stock)

                break

    def buy_choose_item(self, item_cat, stock):
        highest_charisma = max([pcu.attributes['cha'] for pcu in [units.player,
                                                                  units.solou,
                                                                  units.chili,
                                                                  units.chyme,
                                                                  units.adorine,
                                                                  units.parsto]]) - 1

        while True:
            padding = len(max([item.name for item in stock[item_cat]], key=len))
            print(f"{item_cat} (Your party has {main.party_info['gp']} GP): ")

            for num, item in enumerate(stock[item_cat]):
                modified_value = math.ceil(max([item.value/(1 + 0.01*highest_charisma), item.value*0.5]))
                print(f"      [{num + 1}] {item.name} {(padding - len(item.name))*'-'}--> {modified_value} GP")

            while True:
                chosen = main.s_input('Input [#] (or type "back"): ').lower()

                try:
                    chosen = stock[item_cat][int(chosen) - 1]

                except (IndexError, ValueError):
                    if chosen in ['e', 'x', 'exit', 'b', 'back']:
                        print('-'*save_load.divider_size)
                        return

                    continue

                print('-' * save_load.divider_size)
                print(f'-{chosen.name.upper()}-')
                print(ascii_art.item_sprites[chosen.ascart])
                print(f'"{chosen.desc}"')
                print('-' * save_load.divider_size)

                self.buy_yes_or_no(chosen)

                break

    @staticmethod
    def buy_yes_or_no(chosen):
        highest_charisma = max([pcu.attributes['cha'] for pcu in [units.player,
                                                                  units.solou,
                                                                  units.chili,
                                                                  units.chyme,
                                                                  units.adorine,
                                                                  units.parsto]]) - 1

        modified_value = math.ceil(max([chosen.value/(1 + 0.01*highest_charisma), chosen.value*0.5]))

        while True:
            y_n = main.s_input(f"Ya want this {chosen.name}? Will cost ya {modified_value} GP. | Y/N: ").lower()

            if y_n.startswith('y'):
                if main.party_info['gp'] >= modified_value:
                    main.party_info['gp'] -= modified_value
                    items.add_item(chosen.item_id)

                    print('-' * save_load.divider_size)
                    print(f'You purchase the {chosen.name} for {modified_value} GP.')
                    main.s_input("\nPress enter/return ")

                else:
                    print(f"Sorry, you don't have enough GP for that!")
                    main.s_input("\nPress enter/return ")

                print('-' * save_load.divider_size)

                return

            elif y_n.startswith('n'):
                print('-' * save_load.divider_size)

                return

    def speak_to_npcs(self):
        while True:
            print('NPCs: ')

            npc_list = [x for x in self.people if any([y.active for y in x.convos[main.party_info['current_town']]])]

            for x, character in enumerate(npc_list):
                print(f"      [{x + 1}] {character.name}")

            while True:
                character = main.s_input('Input [#] (or type "exit"): ').lower()

                try:
                    character = npc_list[int(character) - 1]

                except (IndexError, ValueError):
                    if character in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    continue

                sounds.play_music('../Music/Mayhem in the Village.ogg')

                print('-'*save_load.divider_size)

                character.speak()

                sounds.play_music('../Music/Chickens (going peck peck peck).ogg')

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

                sounds.play_music('../Music/Mayhem in the Village.ogg')

                break


class House:
    def __init__(self, owner, chests):
        self.owner = owner
        self.chests = chests

    def enter_house(self):
        sounds.play_music('../Music/song21_02.ogg')

        print('-'*save_load.divider_size)
        print(f"Your party enters the house of {self.owner}, completely undetected.")
        while True:
            available_chests = [c for c in self.chests if not (c.destroyed or c.opened)]

            lockpicks = []
            for item in items.inventory['tools']:
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
                main.s_input("\nPress enter/return ")

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
            if self.tries > 1:
                print(f'-{self.tries} ATTEMPTS REMAINING-')

            else:
                print('-ONLY ONE ATTEMPT REMAINING-')

            print(f'Your party attempts to unlock the chest using your {lockpick.name}...')
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

                    for item in self.contents:
                        sounds.item_pickup.play()

                        if isinstance(item, int):
                            main.party_info['gp'] += item
                            main.s_input(f"The chest had {item} gold in it! ")

                        else:
                            items.add_item(item.item_id)
                            main.s_input(f"The chest had a {item.name} in it! ")

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


# =========================== #
#       OVERSHIRE TOWNS       #
# =========================== #

# Nearton
class NeartonClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        nearton_h1_c1 = Chest([20], 1, "N-H1-C1")
        nearton_h1_c2 = Chest([10, items.s_rejuv], 1, "N-H1-C2")
        nearton_h1 = House("Philliard", [nearton_h1_c1, nearton_h1_c2])

        nearton_h2_c1 = Chest([5, items.bone_bag, items.fairy_dust, items.feathers], 1, "N-H2-C1")
        nearton_h2 = House("Alfred", [nearton_h2_c1])

        self.houses = [nearton_h1, nearton_h2]


town_nearton = NeartonClass("Nearton", """\
Nearton is a small village in in the Inner Forest. It is in this very town 
where numerous brave adventurers have begun their journey. Nearton is just 
your standard run-of-the-mill village: it has a general store, an inn, and 
a few small houses. An old man  is standing near one of the houses, and
appears to be very troubled about something.""", [npcs.philliard, npcs.alfred, npcs.saar, npcs.npc_solou], "nearton")


# Southford
class SouthfordClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        southford_h1_c1 = Chest([35], 2, "S-H1-C1")
        southford_h1 = House("Lazaro", [southford_h1_c1])

        self.houses = [southford_h1]


town_southford = SouthfordClass("Southford", """\
Southford is a fair-size town in the Southeast of the Inner Forest. The 
inhabitants of this town are known for being quite wise, and may provide you 
with helpful advice.""", [npcs.wesley, npcs.sondalar, npcs.lazaro], "southford")


# Overshire City
class OvershireCityClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        overshire_h1_c1 = Chest([items.lth_bdy, items.bnz_cst, items.wiz_rob], 2, "OC-H1-C1")
        overshire_h1 = House("Joseph", [overshire_h1_c1])

        overshire_h2_c1 = Chest([50], 2, "OC-H2-C1")
        overshite_h2 = House("Stewson", [overshire_h2_c1])

        self.houses = [overshire_h1, overshite_h2]


town_overshire_city = OvershireCityClass("Overshire City", """\
Overshire City is a city just outside the Inner Forest. Overshire is the 
capital of The Province of Overshire, and therefore the capital of the entire
Kingdom of Harconia. As such, the city is very densely populated. The city is
separated into three sectors: the upper-class inner portion consisting of a 
castle surrounded by reinforced stone walls, a lower-class outer portion
comprised of smalls buildings and huts, and a middle-class section situated in
between. As an outsider, you are forbidden to enter the upper two, but are
welcome to do as you wish in the lower.""", [npcs.joseph, npcs.stewson, npcs.jeffery, npcs.harthos], "overshire_city")


# Principalia
class PrincipaliaClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_principalia = PrincipaliaClass("Principalia", """\
Principalia is an unbelievably large town, rivaling the likes of Overshire 
and Valice. More interestingly, this is also the current home of 
King Harconius II. The main attraction here is the Hytherior Building, a 
medium-large cottage that the original King Harconius I had lived in centuries 
ago. Every Monarch to date has decided to instead live in the Overshire Castle,
with the exception of the current monarch, Harconius. Harconius II has changed 
several things since his ancestor lived here, however. The cottage now has 
access to running water,and the cottage is surrounded by a ring of 12 archer 
towers, each with 2 crossbowmen and one archer at the top. Each tower is about
100 yards from the cottage. In addition, there are numerous guards standing 
watch all around the building.""", [npcs.sakura], "principalia")


# Sardooth
class SardoothClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_sardooth = SardoothClass("Sardooth", """\
Sardooth is a ghost town, without a single permanent inhabitant. This town
was hit the hardest by the latest wave of monsters, causing it to turn from
the bustling hub of commerce and culture to a barren wasteland within just 
six months. Everyone who lived here was either killed or driven out by the 
monsters, and the King's troops were powerless to stop it. The only thing of
note here is the small camp on the outskirts that has a temporary merchant 
stand and sleeping quarters. That, and "The Undershire", a massive cemetery
to the northeast, which is rumored to be even more dangerous than here.""", [], "sardooth")


# =========================== #
#        DOWNPOUR TOWNS       #
# =========================== #
# Tripton
class TriptonClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_tripton = TriptonClass("Tripton", """\
When the town of Tripton was being built, the people working on the
project failed to notice that another town, Fallville, just so happened to be
located mere meters away from the new town's borders. Merchants in Tripton
became very successful, as their superior bartering tactics allowed them to
easily steal business from Fallvillian merchants. This has led to a bitter,
and sometimes violent, rivalry between the two towns, particularly between the
village leaders.""", [npcs.kyle, npcs.alden], "tripton")


# Fallville
class FallvilleClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_fallville = FallvilleClass("Fallville", """\
When the town of Tripton was being built, the people working on the
project failed to notice that another town, Fallville, just so happened to be
located mere meters away from the new town's borders. Merchants in Tripton
became very successful, as their superior bartering tactics allowed them to
easily steal business from Fallvillian merchants. This has led to a bitter,
and sometimes violent, rivalry between the two towns, particularly between the
village leaders.""", [npcs.krystin, npcs.frederick], "fallville")


# =========================== #
#          FLUTE TOWNS        #
# =========================== #
# Valice
class ValiceClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_valice = ValiceClass("Valice", """\
Valice is a massive town in the Province of Overshire. Despite its immense 
size, comparable to that of Overshire City, Valice has little to offer. Back 
during the Harconian Gem Rush, when thousands of tons of gems and ore were 
discovered to be lying beneath the surface of Valice, the town grew 
tremendously in both size and wealth. This wealth did not last, as the gems 
quickly became rarer and rarer and are now nowhere to be seen. This, 
unfortunately, means that Valice is both one of the biggest towns in Overshire,
and also one of the poorest.""", [npcs.ethos, npcs.typhen], "valice")


# Valenfall
class ValenfallClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_valenfall = ValenfallClass("Valenfall", """\
Valenfall is a city in the Aether. Not much is known about this ancient city. 
It's inhabitants claim that it was lifted up from the mainland several millenia ago
by his Divinity. The gods supposedly used Valenfall as the cornerstone,
constructing all of the surrounding land of Aethus around it. Valenfall is
deeply intertwined with nature, and monuments depicting the nature deities can
be seen on every corner.
""", [npcs.fitzgerald], "valenfall")

# =========================== #
#        DELTORA TOWNS        #
# =========================== #


# =========================== #
#        PARRIWEY TOWNS       #
# =========================== #
# Parceon
class ParceonClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_parceon = ParceonClass("Parceon", """\
Parceon is a highly populated town renown for it's rich magical background.
Parceon is home to the famous Sorcerers' Guild, a group of unbelievably
skilled and wise mages who work together to establish and enforce magical law.
The head of the guild, Azura, lives in a large tower in the southwest side of
the town.""", [npcs.azura], "parceon")


# =========================== #
#        CHIN'TOR TOWNS       #
# =========================== #
# Rymn Outpost
class RymnOutpostClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_rymn_outpost = RymnOutpostClass("Rymn Outpost", """\
Rymn Outpost is one of the several small villages established
after the Thexian Incursion. All of the residents of this town are soldiers or
family members of soldiers, with the exception a few merchants. Rymn Outpost
is named after Rymnes, the Divinic gods of defense.""", [], "rymn_outpost")


# Fort Sigil
class FortSigilClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_fort_sigil = FortSigilClass("Fort Sigil", """\
Fort Sigil small village in the Barrier Forest. As the name suggests, the
town was built around an old fort, named Fort Sigil. Originally comprised of
just a few tents meant to house soldiers, many of these soldiers eventually
put down their arms and settled. Despite it's rich backstory and pleasant
scenery, Fort Sigil doesn't get many visitors. Perhaps there's a reason why...""",
                       [npcs.seriph, npcs.rivesh], "fort_sigil")


# Mardovian Caverns
class MardovianCavernsClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_mardoviancaverns = MardovianCavernsClass("Mardovian Caverns", """\
""", [], "mardoviancaverns")


# Mt. Falenkarth
class MtFalenkarthClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_mtfalenkarth = MtFalenkarthClass("Dewfrost", """\
""", [], "mtfalenkarth")


# Coran Outpost
class CoranOutpostClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_coran_outpost = CoranOutpostClass("Coran Outpost", """\
""", [], "coran_outpost")


# =========================== #
#       CAMBERLITE TOWNS      #
# =========================== #
# Dewfrost
class DewfrostClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_dewfrost = DewfrostClass("Dewfrost", """\
""", [], "dewfrost")


# Clayroost
class ClayroostClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_clayroost = ClayroostClass("Clayroost", """\
""", [], "clayroost")


# Ravenstone
class RavenstoneClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_ravenstone = RavenstoneClass("Ravenstone", """\
Ravenstone is a natural sanctuary, home to dozens upon dozens of different 
flora and fauna. Naturally, the majority population of Ravenstone consists of
Druids and other nature-magicians. Ravenstone is also the home of the Druids'
section of the Sorcerers' Guild. Vegetation grows on almost every building and 
statue in the town. When the population of the town is calculated, animals are 
counted as people. More than 35% of the population are various species of 
animals.""", [npcs.strathius], "ravenstone")


# Ambercreek
class AmbercreekClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_ambercreek = AmbercreekClass("Ambercreek", """\
Ambercreek is a large mining town located in the Chin'tor. The Chin'toric
embassy can be found in the middle of this town surrounded by large stone walls
and a few guard-towers. Sugulat, the Lord of Chin'tor, can often be found mining
on the outskirts of town. A very troubled-looking old man is in the southwest 
portion of the town near a few smaller houses.""", [npcs.raidon, npcs.sugulat], "ambercreek")


# Capwild
class CapwildClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_capwild = CapwildClass("Capwild", """\
Capwild is a medium sized town situated in the Terrius Mt. Range.
Capwild is a supplier of grains and herbs for the entire region, and makes
extensive use of terrace farming to make up for the lack of arable land.
Further investigation reveals that water mages have created self-sustaining
irrigation systems as well, further enhancing Capwild's farming capabilities.""", [], "capwild")


# =========================== #
#        WHITLOCK TOWNS       #
# =========================== #
# Simphet
class SimphetClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_simphet = SimphetClass("Simphet", """""", [], "simphet")


# Whistumn
class WhistumnClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_whistumn = WhistumnClass("Whistumn", """\
Whistumn ancient city situated on the border
between the Arcadian Desert and the Barrier Forest. The inhabitants of this town
are known for their skepticism and reasoning. Many of them are scientists and are
skilled mathematicians and engineers. This town has an ongoing rivalry with
the town of Parceon because of their magical background, but this appears
to be mostly one-sided. A saddened-looking woman and her husband are sitting
on the steps of the general store.""", [npcs.polmor, npcs.serena], "whistumn")


# Hatchnuk
class HatchnukClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_hatchnuk = HatchnukClass("Hatchnuk", """\
Hatchnuk is the only remaining town in Harconia that still has cases of 
"Hatchnuk's Blight", a plague-like disease that killed hundreds of thousands of
people during the 10th and 11th centuries. Something about the strand that 
infects Hatchnuk seems to make it completely incurable, as the disease has been 
running rampant for the past four centuries. The economy of Hatchnuk has 
entirely collapsed, as the risk of spreading disease is far too great for people
to be walking out in the open doing business together. As a result, there are no
buildings that you are able to enter, and no people to talk to. The only people 
who are around to speak to are the guards, but their plague-doctor-esque
apparel and stern looks make it clear that they are not in the mood for 
chit-chat.""", [], "hatchnuk")


# =========================== #
#         KOHRIN TOWNS        #
# =========================== #
# Cesura
class CesuraClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_cesura = CesuraClass("Cesura", """""", [npcs.morrison], "cesura")


# Trintooli
class TrintooliClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_trintooli = TrintooliClass("Trintooli", """""", [], "trintooli")


# Fogwhite
class FogwhiteClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_fogwhite = FogwhiteClass("Foqwhitte", """""", [], "fogwhite")


# Don'kohrin
class DonkohrinClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_don_kohrin = DonkohrinClass("Don'kohrin", """""", [], "donkohrin")


# =========================== #
#        PELAMORA TOWNS       #
# =========================== #
# Sanguion
class SanguionClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_sanguion = SanguionClass("Sanguion", """\
Sanguion is a safe-haven for vampires. Vampires are feared throughout
Harconia, so this fairly unknown town is the only place they can go without
being persecuted. The vampires in this town are peaceful, and actually refuse
to drink the blood of intelligent lifeforms. Beware, though, as not all
vampires are as friendly as the ones who inhabit Sanguion.""", [npcs.pime, npcs.ariver], "sanguion")


# Lamtonum
class LamtonumClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_lantonum = LamtonumClass("Lamtonum", """\
Lantonum is a small town that has the best forge in all of Arcadia.
Nearly 2/3s of all citizens of this town are experienced blacksmiths, and 90%
of all ores and minerals mined in Pelamora are brought here. It is one of the 
wealthiest cities in Pelamora due to its Mythril, Magestite, and Necrite bar 
exports.""", [npcs.matthew], "lantonum")


# =========================== #
#        CELEMIA TOWNS        #
# =========================== #
# New Ekanmar
class NewEkanmarClass(Town):
    def __init__(self, name, desc, people, town_id):
        super().__init__(name, desc, people, town_id)

        self.houses = []


town_new_ekanmar = NewEkanmarClass("New Ekanmar", """\
New Ekanmar is the capital of Celemia, one of the Harconian provinces. Prior
to the Harconian Revolution, this town was the location of a large portion of
Flyscoria's troops in Harconia. The Harconians drove much of them out, but
a large number of them defected to the Harconian side and stayed. After the
war, the citizens gave up their weapons and became a peaceful town. The vast
majority of the inhabitants of this town are, naturally, Flyscors. It seems
that the Flyscorian Royal Family is visiting here - perhaps you can talk with
them for a bit.""", [npcs.fly, npcs.stravi, npcs.caesar], "new_ekanmar")

# =========================== #
#          THEX TOWNS         #
# =========================== #

# These three lists are used to serialize chest data. It's easier than having to constantly add chests to lists
all_towns = [town_nearton, town_southford, town_ambercreek, town_capwild, town_valice,
             town_fallville, town_hatchnuk, town_rymn_outpost, town_lantonum, town_fort_sigil, town_sanguion,
             town_ravenstone, town_principalia, town_whistumn, town_new_ekanmar, town_overshire_city, town_sardooth,
             town_tripton, town_valenfall, town_parceon, town_mardoviancaverns, town_mtfalenkarth, town_dewfrost,
             town_clayroost, town_simphet, town_cesura, town_trintooli, town_fogwhite, town_don_kohrin,
             town_coran_outpost]
all_houses = [house for sublist in [town.houses for town in all_towns] for house in sublist]
all_chests = [chest for sublist in [house.chests for house in all_houses] for chest in sublist]

# TAVERN NAMES
# "The Traveling Merchant Inn"
# "The Drunken Moon Tavern"
# "The Wandering Falcon Inn"
# "The Dancing Knight Tavern"
# "The Golden Watchman Tavern"
# "The Smiling Rapier Inn"
# "The Howling Warrior Inn"
# "The Vanishing Skull Inn"
# "The Brave Foal Tavern"
# "The Cowardly Dagger Inn"
# "The Thirsty Wizard Tavern"
# "The Painted Bard Inn"


# Check to see if there is a town where the player is located
def search_towns(enter=True):
    if not isinstance(main.party_info['current_tile'], tiles.Tile):
        # If the player's current tile position is broken, relocate them to the main tile
        logging.exception(f"""Error gathering tile data on {time.strftime('%m/%d/%Y at %H:%M:%S')}: """)

        main.party_info['current_tile'] = tiles.nearton_tile
        print("Error gathering tile data - relocated to nearton_tile.")
        main.s_input("\nPress enter/return ")

    for town in main.party_info['current_tile'].town_list:
        if enter:
            print('-'*save_load.divider_size)

            while True:
                y_n = main.s_input(f'The town of {town.name} is nearby. Give it a visit? | Y/N: ').lower()

                if y_n.startswith('y'):
                    sounds.play_music('../Music/Chickens (going peck peck peck).ogg')

                    main.party_info['prev_town'] = main.party_info['current_tile']

                    town.town_choice()

                    return True

                elif y_n.startswith('n'):
                    print('-'*save_load.divider_size)
                    return True

        else:
            return bool(len(main.party_info['current_tile'].town_list))


def find_chest_with_id(chest_id):
    # A very simple function that scans through a list of all existing Chest objects and returns the first
    # one it finds with the inputted chest_id

    for chest in all_chests:
        if chest.chest_id == chest_id:
            return chest

    return False


def serialize_chests(path):
    with open(path, mode='w') as j:
        json.dump([(c.chest_id, c.destroyed, c.opened) for c in all_chests], j, indent=4, separators=(', ', ': '))


def deserialize_chests(path):
    with open(path, encoding='utf-8') as j:
        json_chests = json.load(j)

    for j_chest in json_chests:
        find_chest_with_id(j_chest[0]).destroyed = j_chest[1]
        find_chest_with_id(j_chest[0]).opened = j_chest[2]


for item1 in copy.copy(globals()):
    if isinstance(globals()[item1], Town) and globals()[item1] not in all_towns:
        print(f'{item1} not in all_towns!')

for item2 in all_chests:
    if find_chest_with_id(item2.chest_id) != item2:
        print(f"{item1.chest_id} doesn't have a unique chest_id!")


for item3 in all_towns:
    for person in item3.people:
        if item3.town_id not in person.convos:
            print(f"{npc.npc_id} does not have any dialogue for {item3.town_id}!")