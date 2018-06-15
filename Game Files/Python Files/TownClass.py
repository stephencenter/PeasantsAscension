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
import items
import sounds
import units
import save_load
import text_scroll
import tiles

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()


class Town:
    def __init__(self, name, desc, people, houses, town_id):
        self.name = name  # The town's name (e.g. New York City)
        self.desc = desc  # A brief description of the town

        self.people = people  # A list that contains the NPCs you can talk to
        self.houses = houses  # A list that contains random buildings you can enter
        self.town_id = town_id

    def town_choice(self):
        print('-'*save_load.divider_size)
        print(f'Welcome to {self.name}!')
        print('-'*save_load.divider_size)

        while True:
            main.party_info['gamestate'] = 'town'
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

                text_scroll.text_scroll('...', spacing=0.75)
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
        while True:
            padding = len(max([item.name for item in stock[item_cat]], key=len))
            print(f"{item_cat} (Your party has {main.party_info['gp']} GP): ")

            for num, item in enumerate(stock[item_cat]):
                print(f"      [{num + 1}] {item.name} {(padding - len(item.name))*'-'}--> {item.value} GP")

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
        while True:
            y_n = main.s_input(f"Ya want this {chosen.name}? Will cost ya {chosen.value} GP. | Y/N: ").lower()

            if y_n.startswith('y'):
                if main.party_info['gp'] >= chosen.value:
                    main.party_info['gp'] -= chosen.value
                    items.add_item(chosen.item_id)

                    print('-' * save_load.divider_size)
                    print(f'You purchase the {chosen.name} for {chosen.value} GP.')
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

            npc_list = [x for x in self.people if any([y.active for y in x.conversations])]

            for x, npc in enumerate(npc_list):
                print(f"      [{x + 1}] {npc.name}")

            while True:
                npc = main.s_input('Input [#] (or type "exit"): ').lower()

                try:
                    npc = npc_list[int(npc) - 1]

                except (IndexError, ValueError):
                    if npc in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    continue

                sounds.play_music('../Music/Mayhem in the Village.ogg')

                print('-'*save_load.divider_size)

                npc.speak()

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
