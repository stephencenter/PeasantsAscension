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
import copy
import random
import math
import json
import time
import re

import inv_system
import sounds
import ascii_art
import world


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


class Item:
    # The basic item class. Items are stored in the "inventory" dictionary. All
    # item-subclasses inherit from this class.
    def __init__(self, name, desc, buy, sell, cat='', imp=False, ascart='Misc'):
        self.name = name
        self.desc = desc
        self.buy = buy
        self.sell = sell  # How much money you will get from selling it
        self.cat = cat  # Ensures that items go into the correct inventory slot
        self.imp = imp
        self.ascart = ascart

    def __str__(self):
        return self.name


class Consumable(Item):
    # Items that restore your HP, MP, or both
    def __init__(self, name, desc, buy, sell,
                 cat='consum', imp=False, heal=0, mana=0, ascart='Potion'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.heal = heal
        self.mana = mana

    def use_item(self, user, is_battle=False):
        if is_battle:
            print(ascii_art.player_art[user.class_.title()] %
                  "{0} is making a move!\n".format(user.name))

        else:
            print('-'*25)

        user.hp += self.heal

        sounds.magic_healing.play()

        if user.hp > user.max_hp:
            user.hp -= (user.hp - user.max_hp)
        user.mp += self.mana

        if user.mp > user.max_mp:
            user.mp -= (user.mp - user.max_mp)
        print('{0} consumes the {1}'.format(user.name, self.name))

        for x, y in enumerate(inv_system.inventory[self.cat]):
            if y.name == self.name:
                inv_system.inventory[self.cat].remove(y)
                break


class StatusPotion(Item):
    def __init__(self, name, desc, buy, sell, status, cat='consum', imp=False, ascart='Potion'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.status = status

    def use_item(self, user):
        if is_battle:
            print(ascii_art.player_art[user.class_.title()] %
                  "{0} is making a move!\n".format(user.name))

        else:
            print('-'*25)

        if user.status_ail == self.status:
            sounds.buff_spell.play()
            print('{0} drinks the {1} and feels much better.'.format(user.name, self.name))
            user.status_ail = 'none'

            for x, y in enumerate(inv_system.inventory[self.cat]):
                if y.name == self.name:
                    inv_system.inventory[self.cat].remove(y)
                    break

        else:
            print("Drinking this potion probably wouldn't do anything.")
            print('-'*25)


class Weapon(Item):
    # Items that increase your damage by a percentage.
    def __init__(self, name, desc, buy, sell, power, type_, class_, ascart,
                 element='none', cat='weapons', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.power = power
        self.type_ = type_
        self.class_ = class_
        self.element = element

        if isinstance(self.class_, str):
            self.desc = ' '.join([desc, '|', self.class_.title(), 'ONLY'''])

        else:
            self.desc = ' '.join([desc, '|', ' and '.join([
                x.title() for x in self.class_]), 'ONLY'])

    def use_item(self, user):
        if user.class_ in self.class_ or self.class_ == 'none':
            # Creating a copy of the weapon ensures that
            # only one weapon can be equipped at a time.
            spam = copy.copy(self)

            if isinstance(
                    inv_system.equipped[user.name if user != main.player else 'player']['weapon'], Weapon
            ):

                old = copy.copy(inv_system.equipped[user.name if user != main.player else 'player']['weapon'])
                inv_system.inventory['weapons'].remove(self)
                if old.name != 'Fists':
                    inv_system.inventory['weapons'].append(old)

                    inv_system.equipped[user.name if user != main.player else 'player']['weapon'] = spam

            print('-'*25)
            input('{0} equips the {1} | Press enter/return '.format(user.name, str(self)))

        else:
            print('-'*25)

            if isinstance(self.class_, list):
                input("{0} must be a {1} or a {2} to equip this | Press enter/return ".format(
                    user.name,
                    self.class_[0].title(),
                    self.class_[1].title()))

            else:
                input("{0} must be a {1} to equip this | Press enter/return ".format(
                    user.name,
                    self.class_.title()))


class Armor(Item):
    # Items that give the player a percent increase in defense when hit.
    def __init__(self, name, desc, buy, sell, defense, type_, part,
                 class_, ascart, cat='armor', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.defense = defense
        self.type_ = type_
        self.part = part
        self.class_ = class_

        if self.class_ != 'none':
            if isinstance(self.class_, str):
                self.desc = ' '.join([desc, '|', self.class_.title(), 'ONLY'''])
            else:
                self.desc = ' '.join([desc, '|', ' and '.join([
                    x.title() for x in self.class_]), 'ONLY'])

        else:
            self.desc = ' '.join([desc, '|', "ANY CLASS"])

    def use_item(self, user):
        if user.class_ in self.class_ or self.class_ == 'none':
            # A copy of the armor is created for the same
            # reason as for weapons.
            fizz = copy.copy(self)

            if isinstance(
                    inv_system.equipped[user.name if user != main.player else 'player'][self.part], Armor
            ):

                old = copy.copy(inv_system.equipped[user.name if user != main.player else 'player'][self.part])
                inv_system.inventory['armor'].append(old)
                inv_system.inventory['armor'].remove(self)
            else:
                inv_system.equipped[user.name if user != main.player else 'player'][self.part] = fizz
                inv_system.inventory['armor'].remove(self)

            print('-'*25)
            input('{0} equip the {1} | Press enter/return '.format(user.name, str(self)))

        else:
            print('-'*25)

            if isinstance(self.class_, list):
                input("{0} must be a {1} or a {2} to equip this | Press enter/return ".format(
                    user.name,
                    self.class_[0].title(),
                    self.class_[1].title()))

            else:
                input("{0} must be a {1} to equip this | Press enter/return ".format(
                    user.name,
                    self.class_.title()))


# -- ACCESSORIES -- #
class Accessory(Item):
    def __init__(self, name, desc, buy, sell, ascart, cat='access', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)


class ElementAccessory(Accessory):
    # Gives the player an element used when taking damage
    def __init__(self, name, desc, buy, sell, element, ascart='Amulet', acc_type='elemental',
                 cat='access', imp=False):
        Accessory.__init__(self, name, desc, buy, sell, ascart, cat, imp)
        self.element = element
        self.acc_type = acc_type

    def __str__(self):
        return self.name

    def use_item(self, user):
        spam = copy.copy(self)
        if isinstance(
                inv_system.equipped[user.name if user != main.player else 'player']['access'], Accessory
        ):

            old = copy.copy(inv_system.equipped[user.name if user != main.player else 'player']['access'])
            inv_system.inventory['access'].append(old)

        inv_system.inventory['access'].remove(self)
        inv_system.equipped[user.name if user != main.player else 'player']['access'] = spam
        user.element = self.element

        print('-'*25)
        input('{0} equips the {1}. Their element is now set to {2} | Press enter/return '.format(
            user.name, self.name, self.element))


class ImmunityAccessory(Accessory):
    # Grants the player immunity to a certain status ailment
    pass


class TradeOffAccessory(Accessory):
    # Doubles one stat, but halves another
    pass


# -- TOOLS -- #
class MagicCompass(Item):
    def __init__(self, name, desc, buy, sell, ascart='Compass', cat='misc', imp=True):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        if main.position['reg'] == 'Aethus':
            print('-'*25)
            print('Something about this place makes your compass needle spin wildly.')
            print('-'*25)
            return

        from towns import town_list, search_towns

        pos_towns = [tuple([town.name, round(math.hypot(town.x - main.position['x'],
                                                        town.y - main.position['y']))])
                     for town in town_list]
        distance = min(pos_towns, key=lambda x: x[1])

        print('-'*25)
        print('The closest town to your party is {0} at ~{1} degrees away.'.format(
            distance[0], distance[1]))

        if not search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)


class DiviningRod(Item):
    def __init__(self, name, desc, buy, sell, ascart='Div Rod', cat='misc', imp=True):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        if main.position['reg'] == 'Aethus':
            print('-'*25)
            print("Your divining rod doesn't seem to be working properly up here.")
            print('-'*25)
            return

        from towns import search_towns
        pos_gems = [tuple([gem.name, round(math.hypot(gem.posx - main.position['x'],
                                                      gem.posy - main.position['y']))])
                    for gem in valuable_list if not gem.acquired]

        if not pos_gems:
            return print('Your party is unable to detect any gems.')

        distance = min(pos_gems, key=lambda x: x[1])

        print('-'*25)
        print('The closest gem to your party is {0} {1} at ~{2} degrees away.'.format(
            'an' if any([distance[0].startswith(x) for x in 'AEIOU'])
            else 'a', distance[0], distance[1]))

        if not search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)


class Shovel(Item):
    def __init__(self, name, desc, buy, sell, ascart='Shovel', cat='misc', imp=True):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        if main.position['reg'] == 'Aethus':
            print('-'*25)
            print('The soil up here is much too tough to be broken up using a shovel.')
            print('-'*25)
            return

        from towns import search_towns
        print('-'*25)
        print('Your party begins to search using your shovel...')
        main.smart_sleep(1)

        for gem in valuable_list:
            if (main.position['x'], main.position['y']) == (gem.posx, gem.posy) \
                    and not gem.acquired:

                gem.acquired = True
                print('Using your shovel, your party manages to uncover a {0}!'.format(gem.name))
                inv_system.inventory['misc'].append(gem)

                if not search_towns(main.position['x'], main.position['y'], enter=False):
                    print('-'*25)

                return

        print('Your party was unable to uncover anything.')
        if not search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)


class InsaneSpeedBoots(Item):
    def __init__(self, name, desc, buy, sell, cat='misc', imp=False, ascart='Boots'):
        # This item is the most expensive purchasable object in the game.
        # It allows immediate travelling to any location on the map.
        # It's basically an insanely OP version of the Map of Fast Travelling.

        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        from towns import search_towns

        letters = 'abcdefghijklmnopqrstuvwxyz'
        numbers = '1234567890'

        print('-'*25)
        print('-Fast Travel Menu-')
        while True:
            direction = input("Enter a direction (N, S, E, W) followed by a number: ")
            direction = direction.lower()

            direction = only_nsew(direction)

            chosen_list = []

            if len(direction) > 1:
                curstring = direction[0]

                for char in direction[1:]:
                    if any(map(curstring.startswith, ''.join([letters, letters.upper()]))):
                        if char.isalpha():
                            curstring = ''.join([curstring, char])

                        else:
                            chosen_list.append(curstring)
                            curstring = char

                    elif any(map(curstring.startswith, numbers)):
                        if char.isnumeric():
                            curstring = ''.join([curstring, char])

                        else:
                            chosen_list.append(curstring)
                            curstring = char

                chosen_list.append(curstring)

                if chosen_list[0].isalpha():
                    all_directions = chosen_list[::2]
                    all_magnitudes = chosen_list[1::2]
                    while len(all_directions) > len(all_magnitudes):
                        all_magnitudes.append('1')

                elif chosen_list[0].isnumeric():
                    all_magnitudes = chosen_list[::2]
                    all_directions = chosen_list[1::2]
                    if len(all_magnitudes) > len(all_directions):
                        all_magnitudes.remove(all_magnitudes[-1])

                all_directions = [spam[0] for spam in all_directions]
                all_magnitudes = [int(spam) for spam in all_magnitudes]

                all_vectors = list(zip(all_directions, all_magnitudes))

                new_position = [main.position['x'], main.position['y']]

                for vector in all_vectors:
                    if vector[0] == 'n':
                        new_position[1] += vector[1]

                        if new_position[1] > 125:
                            new_position[1] = 125

                    if vector[0] == 's':
                        new_position[1] -= vector[1]

                        if new_position[1] < -125:
                            new_position[1] = -125

                    if vector[0] == 'w':
                        new_position[0] -= vector[1]

                        if new_position[0] < -125:
                            new_position[0] = -125

                    if vector[0] == 'e':
                        new_position[0] += vector[1]

                        if new_position[0] > 125:
                            new_position[0] = 125

                dt_vertical = str(new_position[1] - main.position['y'])
                dt_horizontal = str(new_position[0] - main.position['x'])

                if int(dt_vertical) > 0:
                    vert_message = ''.join([str(abs(int(dt_vertical))), "\u00b0 North"])
                    dir_ = 'north'
                elif int(dt_vertical) < 0:
                    vert_message = ''.join([str(abs(int(dt_vertical))), "\u00b0 South"])
                    dir_ = 'south'
                else:
                    vert_message = ''

                if int(dt_horizontal) > 0:
                    horiz_message = ''.join([str(abs(int(dt_horizontal))), "\u00b0 East"])
                    dir_ = 'east'
                elif int(dt_horizontal) < 0:
                    horiz_message = ''.join([str(abs(int(dt_horizontal))), "\u00b0 West"])
                    dir_ = 'west'
                else:
                    horiz_message = ''

                if new_position[1] >= 0:
                    verdir = '\u00b0N'
                else:
                    verdir = '\u00b0S'

                if new_position[0] >= 0:
                    hordir = '\u00b0E'
                else:
                    hordir = '\u00b0W'

                if horiz_message and vert_message:
                    vert_message = ''.join([vert_message, ", "])

                if not (horiz_message or vert_message):
                    print("\nYour party walk quickly in a small circle, arriving precisely where \
they started.")
                    input('Press enter/return ')

                    return

                elif ((abs(int(dt_horizontal)) == 1 and abs(int(dt_vertical)) == 0)
                        or (abs(int(dt_horizontal)) == 0 and abs(int(dt_vertical)) == 1)):

                    print('\nUsing the nearly unlimited magical power of these expensive and rare')
                    print('boots, your party heroically and valiantly takes a single step \
{0}ward.'.format(dir_))
                    input('Press enter/return ')

                    main.position['x'] = new_position[0]
                    main.position['y'] = new_position[1]
                    main.position['v'] = verdir
                    main.position['h'] = hordir

                    if not world.check_region():
                        print('-'*25)

                    return

                print('-'*25)
                print('Your input has been interpreted as {0}{1}.'.format(vert_message,
                                                                          horiz_message))
                print('Travelling in that direction will take your party to {0}{1}, {2}{3}.'.format(
                    new_position[1], verdir, new_position[0], hordir
                ))
                while True:
                    y_n = input('Confirm fast travel? | Yes or No: ')
                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        print('-'*25)
                        print('Fast travelling in...')
                        print('3')
                        main.smart_sleep(1)
                        print('2')
                        main.smart_sleep(1)
                        print('1')
                        main.smart_sleep(1)
                        print('Your party arrives at their destination in one piece.')
                        input('Press enter/return ')

                        main.position['x'] = new_position[0]
                        main.position['y'] = new_position[1]
                        main.position['v'] = verdir
                        main.position['h'] = hordir

                        if not world.check_region():
                            print('-'*25)

                        search_towns(main.position['x'], main.position['y'])

                        return

                    elif y_n.startswith('n'):
                        return


class TownTeleporter(Item):
    def __init__(self, name, desc, buy, sell, imp=False, cat='misc', ascart='Map'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        from towns import town_list, aethus_towns, search_towns

        print('-'*25)

        if not main.position['is_aethus']:
            town_list = town_list
        else:
            town_list = aethus_towns

        available = []

        for town in town_list:
            for visited in main.misc_vars['visited_towns']:
                if town.name == visited:
                    available.append((town.name,
                                      town.x, "\u00b0E" if town.x >= 0 else "\u00b0W",
                                      town.y, "\u00b0N" if town.y >= 1 else "\u00b0S"))

        if not available:
            print('Your party has not visited any towns yet, thus the map fails to respond.')
            return

        available = sorted(available, key=lambda x: x[0])

        print("Available Towns:\n      ", sep='', end='')
        print("\n      ".join(["[{0}] {1}: {2}, {3}".format(num + 1, town[0],
                                                            ''.join([str(town[3]), town[4]]),
                                                            ''.join([str(town[1]), town[2]]))
                              for num, town in enumerate(available)]))
        while True:
            chosen = input('Input [#] (or type "exit"): ')

            try:
                chosen = int(chosen) - 1

            except ValueError:
                if chosen.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    return

            try:
                chosen_town = available[chosen]
            except IndexError:
                continue

            while True:
                y_n = input('Fast travel to {0}, located at {1}{2}, {3}{4}? | Yes or No: '.format(
                    chosen_town[0], chosen_town[3], chosen_town[4], chosen_town[1], chosen_town[2]
                ))

                if y_n.lower().startswith('y'):
                    print('You wave your hand over the map and then blow into it, and you suddenly')
                    print('feel a rush of air around you. You go unconscious for a few seconds and')
                    print('upon waking find yourself exactly where you intended to go.')
                    input('Press enter/return ')

                    main.position['x'] = chosen_town[1]
                    main.position['y'] = chosen_town[3]
                    main.position['h'] = chosen_town[2]
                    main.position['v'] = chosen_town[4]

                    world.check_region()
                    search_towns(main.position['x'], main.position['y'])
                    return

                elif y_n.lower().startswith('n'):
                    break


class Valuable(Item):
    def __init__(self, name, desc, buy, sell, posx, posy, ascart='Gem',
                 acquired=False, cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.posx = posx
        self.posy = posy
        self.acquired = acquired

    def use_item(self, user):
        print('Your party admires the {0}. It looks very valuable.'.format(self.name))


class Misc(Item):
    def __init__(self, name, desc, buy, sell, ascart='Misc', cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    def use_item(self, user):
        print('-'*25)
        if 'Message' in self.name:
            input("""The envelop is designed in a way that makes tampering easily noticeable.
It's probably best not to try to open it and read the letter. | [ENTER] """)

        else:
            input("Your party cannot think of anything useful to do with this. | [ENTER] ")


# A regular expression that replaces all non-NSEW characters with ''
def only_nsew(string):
    return re.compile(r'[^n^s^e^w^1^2^3^4^5^6^7^8^9^0]').sub('', string)


# Potions -- Health
s_potion = Consumable('Weak Potion',
                      'A small potion that restores 15 HP when consumed.',
                      15, 5, heal=15)
m_potion = Consumable('Basic Potion',
                      'A regular potion that restores 45 HP when consumed.',
                      30, 10, heal=45)
l_potion = Consumable('Strong Potion',
                      'A powerful potion that restores 100 HP when consumed.',
                      60, 20, heal=100)
x_potion = Consumable('Super Potion',
                      'A super powerful potion that restores 200 HP when consumed.',
                      120, 40, heal=200)

# Potions -- Mana
s_elixir = Consumable('Basic Elixir',
                      'A generic elixir that restores 15 MP when consumed.',
                      10, 3, mana=10, ascart='Elixir')
m_elixir = Consumable('Enhanced Elixir',
                      'A more potent elixir that restores 45 MP when consumed.',
                      25, 8, mana=35, ascart='Elixir')
l_elixir = Consumable('Grand Elixir',
                      'A powerful elixir that restores 100 MP when consumed.',
                      50, 17, mana=75, ascart='Elixir')
x_elixir = Consumable('Extreme Elixir',
                      'A super powerful elixir that restores 175 MP when consumed.',
                      100, 35, mana=175, ascart='Elixir')

# Potions -- Both
s_rejuv = Consumable('Minor Rejuvenation Potion',
                     'A basic mixture that restores 15 HP and 15 MP when consumed.',
                     35, 12, heal=15, mana=15, ascart='Rejuv')

m_rejuv = Consumable('Refined Rejuvenation Potion',
                     'A higher quality mixture that restores 45 HP and 45 MP when consumed.',
                     65, 22, heal=45, mana=45, ascart='Rejuv')

l_rejuv = Consumable('Mighty Rejuvenation Potion',
                     'A super powerful mixture that restores 100 HP and 100 MP when consumed.',
                     225, 80, heal=100, mana=100, ascart='Rejuv')

# Potions - Status
sleep_potion = StatusPotion('Potion of Waking Up',
                            "A potion designed to wake its partaker from a deep sleep.",
                            25, 10, 'asleep', ascart='Status')
silence_potion = StatusPotion('Potion of Allowing Speech',
                              "A potion designed to enable the usage of damaged vocal chords.",
                              25, 10, 'silenced', ascart='Status')
poison_potion = StatusPotion('Potion of Curing Disease',
                             'A potion designed to cure even the most deadly of illnesses.',
                             25, 10, 'poisoned', ascart='Status')
weakness_potion = StatusPotion('Potion of Regaining Strength',
                               'A potion designed to help regain lost muscle-mass and stamina.',
                               25, 10, 'weakened', ascart='Status')
blindness_potion = StatusPotion('Potion of Enabling Sight',
                                'A potion designed to help the blind regain their eyesight.',
                                25, 10, 'blinded', ascart='Status')
paralyzation_potion = StatusPotion('Potion of Inducing Motion',
                                   'A potion designed to cure minor paralysis in most of the body.',
                                   25, 10, 'paralyzed', ascart='Status')

# Fists
fists = Weapon('Fists',
               """Nothing beats good ol' fashioned hand-to-hand combat (+0 Attack)""",
               0, 0, 0, 'melee', 'none', 'Fists')
               # Fists exist to prevent bugs caused by not having any
               # weapon equipped.

# Weapons -- Warrior
wdn_sht = Weapon('Wooden Shortsword',
                 'A small sword carved from an oak branch (+5% Damage)',
                 10, 5, 0.05, 'melee', 'warrior', 'Short Sword')

bnz_swd = Weapon('Bronze Sword',
                 'A light yet sturdy sword smelted from a bronze alloy (+10% Damage)',
                 50, 15, 0.1, 'melee', 'warrior', 'Sword')
en_bnz_swd = Weapon('Enhanced Bronze Sword',
                    'An enhanced version of your typical Bronze Sword (+25% Damage)',
                    100, 25, 0.25, 'melee', 'warrior', 'Sword')

stl_spr = Weapon('Steel Spear',
                 'A fair-sized spear crafted from well made steel (+40% Damage)',
                 225, 75, 0.4, 'melee', 'warrior', 'Spear')
en_stl_spr = Weapon('Enhanced Steel Spear',
                    'An enhanced version of your typical Steel Spear (+60% Damage)',
                    350, 125, 0.6, 'melee', 'warrior', 'Spear')

durs_axe = Weapon('Durasteel Battleaxe',
                  'A heavy and powerful axe made with high quality durasteel ore (+80% Damage)',
                  500, 225, 0.8, 'melee', 'warrior', 'Axe')
en_durs_axe = Weapon('Enhanced Durasteel Battleaxe',
                     'An enhanced version of your typical Durasteel Battleaxe (+100% Damage)',
                     750, 325, 1, 'melee', 'warrior', 'Axe')

# Weapons -- Assassin
stn_dag = Weapon('Stone Dagger',
                 'A crude yet effective knife carved from a light stone (+5% Damage)',
                 10, 5, 0.05, 'melee', 'assassin', 'Dagger')

ser_knf = Weapon('Serrated Knife',
                 'A durable knife made of iron, with one side made jagged (+10% Damage)',
                 50, 15, 0.1, 'melee', 'assassin', 'Dagger')
en_ser_knf = Weapon('Enhanced Serrated Knife',
                    'An enhanced version of your typical Serrated Knife (+25% Damage)',
                    100, 25, 0.25, 'melee', 'assassin', 'Dagger')

stiletto = Weapon('Stiletto',
                  'A long, cross-shaped knife perfect for "removing" your enemies (+40% Damage)',
                  225, 75, 0.4, 'melee', 'assassin', 'Stiletto')
en_stiletto = Weapon('Enhanced Stiletto',
                     'An enhanced version of your typical Stiletto (+60% Damage)',
                     350, 125, 0.6, 'melee', 'assassin', 'Stiletto')

myth_sb = Weapon('Mythril Shortblade',
                 'A knife made of a rare and powerful material (+80% Damage)',
                 500, 225, 0.8, 'melee', 'assassin', 'Short Sword')
en_myth_sb = Weapon('Enhanced Mythril Shortblade',
                    'An enhanced version of your typical Mythril Shortblade (+100% Damage)',
                    750, 325, 1, 'melee', 'assassin', 'Short Sword')

# Weapons -- Ranger
slg_sht = Weapon('Sling Shot',
                 'A weapon that could scare even the mightiest of tin-cans (+5% Damage)',
                 10, 5, 0.05, 'ranged', 'ranger', 'Sling Shot')

sht_bow = Weapon('Short Bow',
                 "A bow of great craftsmanship. It's kinda small, though (+10% Damage)",
                 50, 15, 0.10, 'ranged', 'ranger', 'Bow')
en_sht_bow = Weapon('Enhanced Short Bow',
                    " An enhanced version of your typical Short Bow (+25% Damage)",
                    100, 25, 0.25, 'ranged', 'ranger', 'Bow')

lng_bow = Weapon('Long Bow',
                 'A much more impressive bow capable of accuracy at long distances (+40% Damage)',
                 225, 75, 0.4, 'ranged', 'ranger', 'Bow')
en_lng_bow = Weapon('Enhanced Long Bow',
                    'An enhanced version of your typical Long Bow (+60% Damage)',
                    350, 125, 0.6, 'ranged', 'ranger', 'Bow')

ash_cbow = Weapon('Ashen Crossbow',
                  'A beautifully-crafted crossbow made from the wood\
of an ash tree. (+80% Damage)',
                  500, 225, 0.8, 'ranged', 'ranger', 'Crossbow')
en_ash_cbow = Weapon('Enhanced Ashen Crossbow',
                     'An enhanced version of your typical Ashen Crossbow (+100% Damage)',
                     750, 325, 1, 'ranged', 'ranger', 'Crossbow')

# Weapons -- Mage
# Mage weapons deal around half that of other weapons, but their magic deals 2x damage so it
# for the most part balances it out
mag_twg = Weapon('Magical Twig',
                 'A small stick with basic magical properties (+5% Damage)',
                 10, 5, 0.05, 'magic', 'mage', 'Twig')

oak_stf = Weapon('Oak Staff',
                 'A wooden staff imbued with weak magical abilities (+10% Damage)',
                 50, 15, 0.1, 'magic', 'mage', 'Staff')
en_oak_stf = Weapon('Enhanced Oak Staff',
                    'An enhanced version of your typical Oak Staff (+15% Damage)',
                    100, 25, 0.15, 'magic', 'mage', 'Staff')

arc_spb = Weapon('Arcane Spellbook',
                 'An intermediate spellbook for combat purposes (+20% Damage)',
                 225, 75, 0.2, 'magic', 'mage', 'Book')
en_arc_spb = Weapon('Enhanced Arcane Spellbook',
                    'An enhanced version of your typical Arcane Spellbook (+30% Damage)',
                    350, 125, 0.3, 'magic', 'mage', 'Book')

rnc_stf = Weapon('Runic Staff',
                 'A powerful staff enchanted with ancient magic (+40% Damage)',
                 500, 225, 0.4, 'magic', 'mage', 'Staff')
en_rnc_stf = Weapon('Enhanced Runic Staff',
                    'An enhanced version of your typical Runic Staff (+50% Damage)',
                    750, 325, 0.5, 'magic', 'mage', 'Staff')

# Weapons -- Paladin
rbr_mlt = Weapon('Rubber Mallet',
                 'This can barely hammer nails, what do you expect to kill with it? (+5% Damage)',
                 10, 5, 0.05, 'melee', 'paladin', 'Hammer')

holy_mace = Weapon('Holy Mace',
                   'An well-made iron mace imbued with the power of the heavens (+10% Damage)',
                   50, 15, 0.1, 'melee', 'paladin', 'Mace')
en_holy_mace = Weapon('Enhanced Holy Mace',
                      'An enhanced version of your typical Holy Mace (+25% Damage)',
                      100, 25, 0.25, 'melee', 'paladin', 'Mace')

hmr_of_mgt = Weapon('Hammer of Might',
                    'A hammer often used by holy warriors to smash their foes (+40% Damage)',
                    225, 75, 0.4, 'melee', 'paladin', 'Hammer')
en_hmr_of_mgt = Weapon('Enhanced Hammer of Might',
                       'An enhanced version of your typical Hammer of Might (+60% Damage)',
                       350, 125, 0.6, 'melee', 'paladin', 'Hammer')

ngt_bane = Weapon("Night's Bane",  # Reference to Terraria's "Light's Bane"
                  'A hammer used by countless paladins to stamp out unholy creatures (+80% Damage)',
                  500, 225, 0.8, 'melee', 'paladin', 'Hammer')
en_ngt_bane = Weapon("Enhanced Night's Bane",
                     "An enhanced version of your typical Night's Bane (+100% Damage)",
                     750, 325, 1, 'melee', 'paladin', 'Hammer')

# Weapon -- Monk
brass_kncls = Weapon('Brass Knuckles',
                     'A brass adornment for your knuckles providing \
extra punching power (+10% Damage)',
                     50, 15, 0.1, 'melee', 'monk', 'Knuckles')
en_brass_kncls = Weapon('Enhanced Brass Knuckles',
                        'An enhanced version of your typical Brass Knuckles (+25% Damage)',
                        100, 25, 0.25, 'melee', 'monk', 'Knuckles')

bladed_gloves = Weapon('Bladed Gloves',
                       'Leather gloves with sturdy steel blades protruding from them (+40% Damage)',
                       225, 75, 0.4, 'melee', 'monk', 'Gloves')
en_bladed_gloves = Weapon('Enhanced Bladed Gloves',
                          'An enhanced version of your typical Bladed Gloves (+60% Damage)',
                          350, 125, 0.6, 'melee', 'monk', 'Gloves')

lead_bg = Weapon('Lead-Weighted Boxing Gloves',
                 'Weighted with 5 pounds of lead and tipped with steel blades. Probably \n\
not allowed in standard matches (+80% Damage)',
                 500, 225, 0.8, 'melee', 'monk', 'Gloves')
en_lead_bg = Weapon('Enhanced Lead Gloves',
                    'An enhanced version of your typical \
Lead-Weighted Boxing Gloves (+100% Damage)',
                    750, 325, 1, 'melee', 'monk', 'Gloves')

# Starting Armor (Useless)
straw_hat = Armor('Straw Hat',
                  "Other than keep the sun out of your eyes, this doesn't do much.",
                  0, 2, 0, 'melee', 'head', 'none', 'Hat')
cotton_shirt = Armor('Cotton Shirt',
                     "It's barely even worth the material it's made of.",
                     0, 2, 0, 'melee', 'body', 'none', 'Shirt')
sunday_trousers = Armor('Sunday Trousers',
                        "At least they look nice... Wait, isn't it Thursday?",
                        0, 2, 0, 'melee', 'legs', 'none', 'Pants')

# Armor -- Warrior + Paladin -- Weak
bnz_hlm = Armor('Bronze Helmet',
                'A simple helmet crafted from bronze (+5% ARMOR)',
                20, 8, 0.05, 'melee', 'head', ['warrior', 'paladin'], 'Helmet')
bnz_cst = Armor('Bronze Chestpiece',
                'Simple chest armor crafted from bronze (+10% ARMOR)',
                30, 12, 0.1, 'melee', 'body', ['warrior', 'paladin'], 'Shirt')
bnz_leg = Armor('Bronze Greaves',
                'Simple leg armor crafted from bronze (+5% ARMOR)',
                25, 10, 0.05, 'melee', 'legs', ['warrior', 'paladin'], 'Pants')

en_bnz_hlm = Armor('Enhanced Bronze Helmet',
                   'An enhanced version of your typical Bronze Helmet (+10% ARMOR)',
                   60, 25, 0.1, 'melee', 'head', ['warrior', 'paladin'], 'Helmet')
en_bnz_cst = Armor('Enhanced Bronze Chestpiece',
                   'An enhanced version of your typical Bronze Chestpiece (+15% ARMOR)',
                   70, 35, 0.15, 'melee', 'body', ['warrior', 'paladin'], 'Shirt')
en_bnz_leg = Armor('Enhanced Bronze Greaves',
                   'An enhanced version of your typical Bronze Greaves (+10% ARMOR)',
                   65, 30, 0.1, 'melee', 'legs', ['warrior', 'paladin'], 'Pants')

# Armor -- Mage + Monk -- Weak
wiz_hat = Armor('Silk Hat',
                'A silk hat woven with magic thread (+3% ARMOR)',
                20, 8, 0.03, 'magic', 'head', ['mage', 'monk'], 'Wizard Hat')
wiz_rob = Armor('Silk Robe',
                'A silk robe woven with magic thread (+5% ARMOR)',
                30, 12, 0.05, 'magic', 'body', ['mage', 'monk'], 'Robe')
wiz_gar = Armor('Silk Garments',
                'Silk garments woven with magic thread (+3% ARMOR)',
                25, 10, 0.03, 'magic', 'legs', ['mage', 'monk'], 'Robe Pants')

en_wiz_hat = Armor('Enhanced Silk Hat',
                   'An enhanced version of your typical Wizard Hat (+5% ARMOR)',
                   60, 25, 0.05, 'magic', 'head', ['mage', 'monk'], 'Wizard Hat')
en_wiz_rob = Armor('Enhanced Silk Robe',
                   'An enhanced version of your typical Wizard Robe (+10% ARMOR)',
                   70, 35, 0.1, 'magic', 'body', ['mage', 'monk'], 'Robe')
en_wiz_gar = Armor('Enhanced Silk Garments',
                   'An enhanced version of your typical Wizard Garments (+5% ARMOR)',
                   65, 30, 0.05, 'magic', 'legs', ['mage', 'monk'], 'Robe Pants')

# Armor -- Assassin + Ranger -- Weak
lth_cap = Armor('Leather Cap',
                'A simple leather cap providing equally simple protection (+2% ARMOR)',
                20, 8, 0.02, 'melee', 'head', ['assassin', 'ranger'], 'Cap')
lth_bdy = Armor('Leather Bodyarmor',
                'Simple body armor providing equally simple protection (+4% ARMOR)',
                30, 12, 0.04, 'melee', 'body', ['assassin', 'ranger'], 'Shirt')
lth_leg = Armor('Leather Leggings',
                'Simple leggings providing equally simple protection (+2% ARMOR)',
                25, 10, 0.02, 'melee', 'legs', ['assassin', 'ranger'], 'Pants')

en_lth_cap = Armor('Enhanced Leather Cap',
                   'An enhanced version of your typical Leather Cap (+7% ARMOR)',
                   60, 25, 0.07, 'melee', 'head', ['assassin', 'ranger'], 'Cap')
en_lth_bdy = Armor('Enhanced Leather Bodyarmor',
                   'An enhanced version of your typical Leather Bodyarmor (+12% ARMOR)',
                   70, 35, 0.12, 'melee', 'body', ['assassin', 'ranger'], 'Shirt')
en_lth_leg = Armor('Enhanced Leather Leggings',
                   'An enhanced version of your typical Leather Leggings (+7% ARMOR)',
                   65, 30, 0.07, 'melee', 'legs', ['assassin', 'ranger'], 'Pants')

# Armor -- Warrior + Paladin -- Mid
stl_hlm = Armor('Steel Helmet',
                'A decent helmet created from a solid metal (+15% ARMOR)',
                145, 50, 0.15, 'melee', 'head', ['warrior', 'paladin'], 'Helmet')
stl_cst = Armor('Steel Chestpiece',
                'Decent body armor made from a solid metal (+20% ARMOR)',
                165, 60, 0.20, 'melee', 'body', ['warrior', 'paladin'], 'Shirt')
stl_leg = Armor('Steel Greaves',
                'Decent greaves made from a solid metal (+15% ARMOR)',
                155, 55, 0.15, 'melee', 'legs', ['warrior', 'paladin'], 'Pants')

en_stl_hlm = Armor('Enhanced Steel Helmet',
                   'An enhanced version of your typical Steel Helmet (+20% ARMOR)',
                   260, 75, 0.20, 'melee', 'head', ['warrior', 'paladin'], 'Helmet')
en_stl_cst = Armor('Enhanced Steel Chestpiece',
                   'An enhanced version of your typical Steel Chestpiece (+25% ARMOR)',
                   280, 85, 0.25, 'melee', 'body', ['warrior', 'paladin'], 'Shirt')
en_stl_leg = Armor('Enhanced Steel Leggings',
                   'An enhanced version of your typical Steel Greaves (+20% ARMOR)',
                   270, 80, 0.20, 'melee', 'legs', ['warrior', 'paladin'], 'Pants')


# Armor -- Mage + Monk -- Mid
myst_hat = Armor('Mystical Hood',
                 'A mysterious hood with strange symbols sewn into it (+8% ARMOR)',
                 145, 50, 0.08, 'magic', 'head', ['mage', 'monk'], 'Wizard Hat')
myst_rob = Armor('Mystical Robe',
                 'A mysterious robe with strange symbols sewn into it (+12% ARMOR)',
                 165, 60, 0.12, 'magic', 'body', ['mage', 'monk'], 'Robe')
myst_gar = Armor('Mystical Garments',
                 'Mysterious garments with strange symbols sewn into it (+8% ARMOR)',
                 155, 55, 0.08, 'magic', 'legs', ['mage', 'monk'], 'Robe Pants')

en_myst_hat = Armor('Enhanced Mystical Hood',
                    'An enhanced version of your typical Mystical Hood (+15% ARMOR)',
                    260, 75, 0.15, 'magic', 'head', ['mage', 'monk'], 'Wizard Hat')
en_myst_rob = Armor('Enhanced Mystical Robe',
                    'An enhanced version of your typical Mystical Robe (+20% ARMOR)',
                    280, 85, 0.2, 'magic', 'body', ['mage', 'monk'], 'Robe')
en_myst_gar = Armor('Enhanced Mystical Garments',
                    'An enhanced version of your typical Mystical Garments (+15% ARMOR)',
                    270, 80, 0.15, 'magic', 'legs', ['mage', 'monk'], 'Robe Pants')

# Armor -- Assassin + Ranger -- Mid
std_cwl = Armor('Studded Cowl',
                'A soft leather cap studded with steel pieces (+12% ARMOR)',
                145, 50, 0.12, 'melee', 'head', ['assassin', 'ranger'], 'Cap')
std_bdy = Armor('Studded Body-armor',
                'Soft leather body armor studded with steel pieces (+18% ARMOR)',
                165, 60, 0.18, 'melee', 'body', ['assassin', 'ranger'], 'Shirt')
std_leg = Armor('Studded Leggings',
                'Soft leather leggings studded with steel pieces (+12% ARMOR)',
                155, 55, 0.12, 'melee', 'legs', ['assassin', 'ranger'], 'Pants')

en_std_cwl = Armor('Enhanced Studded Cowl',
                   'An enhanced version of your typical Studded Hood (+17% ARMOR)',
                   260, 75, 0.17, 'melee', 'head', ['assassin', 'ranger'], 'Cap')
en_std_bdy = Armor('Enhanced Studded Body-armor',
                   'An enhanced version of your typical Studded Bodyarmor (+22% ARMOR)',
                   280, 85, 0.22, 'melee', 'body', ['assassin', 'ranger'], 'Shirt')
en_std_leg = Armor('Enhanced Studded Leggings',
                   'An enhanced version of your typical Studded Leggings (+17% ARMOR)',
                   270, 80, 0.17, 'melee', 'legs', ['assassin', 'ranger'], 'Pants')


# Armor -- Warrior + Paladin -- Pow
# 90% ARMOR
ori_hlm = Armor('Orichalcum Helmet',
                'A strong helmet smelted from rare mountain copper  (+25% ARMOR)',
                320, 110, 0.25, 'melee', 'head', ['warrior', 'paladin'], 'Helmet')
ori_cst = Armor('Orichalcum Chestplate',
                'Strong chest armor smelted from rare mountain copper  (+35% ARMOR)',
                340, 120, 0.35, 'melee', 'body', ['warrior', 'paladin'], 'Shirt')
ori_leg = Armor('Orichalcum Greaves',
                'Strong leg armor smelted from rare mountain copper (+25% ARMOR)',
                330, 115, 0.25, 'melee', 'legs', ['warrior', 'paladin'], 'Pants')

# Armor -- Mage + Monk -- Pow
# 65% ARMOR
elem_hat = Armor('Armored Cloth Hat',
                 'A silk hat lined with chainmail in important parts (+20% ARMOR)',
                 320, 110, 0.20, 'magic', 'head', ['mage', 'monk'], 'Wizard Hat')
elem_rob = Armor('Armored Cloth Robe',
                 'A silk robe lined with chainmail in important parts (+25% ARMOR)',
                 340, 120, 0.25, 'magic', 'body', ['mage', 'monk'], 'Robe')
elem_gar = Armor('Armored Cloth Garments',
                 'Silk garments lined with chainmail in important parts (+20% ARMOR)',
                 330, 115, 0.20, 'magic', 'legs', ['mage', 'monk'], 'Robe Pants')

# Armor -- Assassin + Ranger -- Pow
# 80% ARMOR
drg_cwl = Armor('Dragonhide Cowl',
                'A tough hood crafted from high-quality dragonskin (+25% ARMOR)',
                320, 110, 0.25, 'melee', 'head', ['assassin', 'ranger'], 'Cap')
drg_bdy = Armor('Dragonhide Bodyarmor',
                'Tough bodyarmor crafted from high-quality dragonskin (+30% ARMOR)',
                340, 120, 0.3, 'melee', 'body', ['assassin', 'ranger'], 'Shirt')
drg_leg = Armor('Dragonhide Leggings',
                'Tough leggings crafted from high-quality dragonskin (+25% ARMOR)',
                330, 115, 0.25, 'melee', 'legs', ['assassin', 'ranger'], 'Pants')

# Unique Drops -- Weapons
ice_blade = Weapon('Blade of Frost',
                   'A stunning blade enchanted with the power of ice (+50% Damage, ICE)',
                   0, 225, 0.5, 'melee', 'warrior', 'Sword', element='ice')

enc_yw = Weapon('Enchanted Yew Wand',
                'A yewen wand of remarkable craftsmanship (+25% Damage, GRASS)',
                0, 225, 0.5, 'magic', 'mage', 'Twig', element='grass')

spect_wand = Weapon('Spectre Wand',
                    'A ghastly wand made of an indescribable material (+25% Damage, DEATH)',
                    0, 225, 0.5, 'magic', 'mage', 'Wand', element='death')

muramasa = Weapon('Blade of Muramasa',
                  'A blade crafted by the great Muramasa (+60% Damage, DEATH)',
                  0, 500, 0.6, 'melee', ['warrior', 'assassin'], 'Sword', element='death')

masamune = Weapon('Blade of Masamune',
                  'A blade crafted by the great Masamune (+60% Damage, LIFE)',
                  0, 500, 0.6, 'melee', ['warrior', 'assassin'], 'Sword', element='life')

wind_bow = Weapon('Bow of Echoes',
                  'A finely made bow that harnesses the power of wind (+60% Damage, WIND)',
                  0, 450, 0.6, 'ranged', 'ranger', 'Bow', element='wind')

lightning_dagger = Weapon('Lightning Dagger',
                          'A blade in the shape of a lightning bolt. A powerful current \n\
flows through the edge (+60% Damage, ELECTRIC)',
                          0, 450, 0.6, 'melee', 'assassin', 'Dagger', element='electric')

# forksbane = Weapon('Forksbane')

# Accessories
# -- Elemental Accessories
water_amulet = ElementAccessory('Aquatic Amulet',
                                'An amulet that imbues its wearer with the power of WATER',
                                250, 75, 'Water')
fire_amulet = ElementAccessory('Infernal Amulet',
                               'An amulet that imbues its wearer with the power of FIRE',
                               250, 75, 'Fire')
earth_amulet = ElementAccessory('Ground Amulet',
                                'An amulet that imbues its wearer with the power of EARTH',
                                250, 75, 'Earth')
electric_amulet = ElementAccessory('Galvanic Amulet',
                                   'An amulet that imbues its wearer with the power of ELECTRICITY',
                                   250, 75, 'Electric')
wind_amulet = ElementAccessory('Tempestuous Amulet',
                               'An amulet that imbues its wearer with the power of WIND',
                               250, 75, 'Wind')
grass_amulet = ElementAccessory('Verdant Amulet',
                                'An amulet that imbues its wearer with the power of GRASS',
                                250, 75, 'Grass')
ice_amulet = ElementAccessory('Glacial Amulet',
                              'An amulet that imbues its wearer with the power of ICE',
                              250, 75, 'Ice')
life_amulet = ElementAccessory('Living Amulet',
                               'An amulet that imbues its wearer with the power of LIFE',
                               250, 75, 'Life')
death_amulet = ElementAccessory('Necrotic Amulet',
                                'An amulet that imbues its wearer with the power of DEATH',
                                250, 75, 'Death')

# Quest items
message_joseph = Misc('Message from Joseph',
                      'A neatly written message addressed to Philliard.',
                      0, 0, cat='q_items', imp=True)
message_philliard = Misc('Message from Philliard',
                         'A neatly written message addressed to Joseph.',
                         0, 0, cat='q_items', imp=True)

iSound = Misc('iSound',
              "You can't even begin to imagine how one would go about using this.",
              250, 75, cat='q_items', imp=False)
    # Alternate description: Pythonia has no internet access, no electricity, and no radio.
    # What's the point of having this again?


# Gems & Valuables
pearl_gem = Valuable('Pearl', 'A valuable pearl. This could probably be sold for quite a bit.',
                     0, 175, 119, -121)
    # Alternate Description: Impossible to read, but will sell for money nonetheless

ruby_gem = Valuable('Ruby', 'A valuable ruby. This could be sold for quite a bit.',
                    0, 175, -62, -84)  # better_than_perl=True

sapphire_gem = Valuable('Sapphire',
                        'A valuable sapphire. This could probably be sold for quite a bit.',
                        0, 175, -78, 102)

emerald_gem = Valuable('Emerald',
                       'A valuable emerald. This could probably be sold for quite a bit.',
                       0, 175, 26, -13)

citrine_gem = Valuable('Citrine',
                       'A valuable citrine. This could probably be sold for quite a bit.',
                       0, 175, 53, 92)

jade_gem = Valuable('Jade', 'A valuable jade. This could probably be sold for quite a bit.',
                    0, 175, 81, -103)

opal_gem = Valuable('Opal', 'A valuable opal. This could probably be sold for quite a bit.',
                    0, 175, 25, 67)

onyx_gem = Valuable('Onyx', 'A valuable onyx. This could probably be sold for quite a bit.',
                    0, 175, 121, -56)

diamond_gem = Valuable('Diamond', 'A valuable diamond. This could probably be sold for quite a \
bit.',
                                  0, 175, -12, 124)

amethyst_gem = Valuable('Amethyst', 'A valuable amethyst. This could probably be sold for quite a \
bit.',
                                    0, 175, -12, -5)

topaz_gem = Valuable('Topaz', 'A valuable topaz. This could probably be sold for quite a bit.',
                              0, 175, 0, 0)

garnet_gem = Valuable('Garnet', 'A valuable garnet. This could probably be sold for quite a bit.',
                                0, 175, 11, -101)

quartz_gem = Valuable('Quartz', 'A valuable quartz. This could probably be sold for quite a bit.',
                                0, 175, 114, 52)

zircon_gem = Valuable('Zircon', 'A valuable zircon. This could probably be sold for quite a bit.',
                                0, 175, -108, 100)

agate_gem = Valuable('Agate', 'A valuable agate. This could probably be sold for quite a bit.',
                              0, 175, 0, -114)

aquamarine_gem = Valuable('Aquamarine', 'A valuable aquamarine. This could probably be sold \
for quite a bit.',
                          0, 175, 109, -13)

valuable_list = [pearl_gem, ruby_gem, sapphire_gem, emerald_gem, citrine_gem, jade_gem,
                 opal_gem, onyx_gem, diamond_gem, amethyst_gem, topaz_gem, garnet_gem,
                 quartz_gem, zircon_gem, agate_gem, aquamarine_gem]

# Tools
magic_compass = MagicCompass(
    'Magical Compass',
    'A compass infused with the power of magic capable of detecting nearby towns.',
    0, 0, imp=True)

divining_rod = DiviningRod('Divining Rod',
                           'A supposedly magical stick capable of detecting nearby ores and gems.',
                           325, 107)

shovel = Shovel('Shovel', 'A simple shovel used to excavate for hidden gems and minerals.',
                175, 56)

map_of_fast_travel = TownTeleporter('Map of Fast Travel',
                                    'Allows quick travelling to previously visited towns.',
                                    575, 190)

boots_of_travel = InsaneSpeedBoots('Boots of Travel',  # Made with Boots of Speed and a 2000 gold recipe
                                   'Allows insanely fast travel to any point on the map.',
                                   7500, 3750)

# Monster Drops
shell_fragment = Misc('Shell Fragment', 'A broken fragment of a remarkable sea-shell.', 0, 5)
crab_claw = Misc('Crab Claw', 'A reddish claw from a giant crab.', 0, 5)
fairy_dust = Misc('Fairy Dust', 'Dust from a fairy. It has strange, magical properties.', 0, 5)
serpent_scale = Misc('Serpent Scale', 'A rough scale from an unknown reptile.', 0, 5)
slimey_residue = Misc('Slimy Residue', 'The slimy remains of a slimy monster.', 0, 5)
ink_sack = Misc('Ink Sack', 'A small pouch full of an inky substance.', 0, 5)
skeleton_bone = Misc('Skeleton Bone', 'The leg bone of a now-deceased creature.', 0, 5)
monster_skull = Misc('Monster Skull', 'A broken skull from a strange creature.', 0, 5)
living_bark = Misc('Living Bark', 'This bark has a fleshy texture to it.', 0, 5)
shirt_cloth = Misc('Cloth', 'A thick, torn cloth made out of an unknown fabric.', 0, 5)
beetle_shell = Misc('Beetle Shell', 'A bluish shell from a large beetle.', 0, 5)
wing_piece = Misc('Wing Piece', 'A piece of wing from a flying creature.', 0, 5)
bat_fang = Misc('Fang', 'The sharp fang of a frightening creature.', 0, 5)
animal_fur = Misc('Animal Fur', 'A furry clump of hair from a strange animal.', 0, 5)
golem_rock = Misc('Rock', 'A small rock that seems to glow slightly.', 0, 5)
burnt_ash = Misc('Ash', 'The ashy remains of a once-living creature.', 0, 5)
antennae = Misc('Antennae', 'A pair of antennae from a massive insect.', 0, 5)
ectoplasm = Misc('Ectoplasm', 'The gooey remains from a terrifying apparition.', 0, 5)
chain_link = Misc('Chain links', 'A couple joined links of chain made from steel.', 0, 5)
unicorn_horn = Misc('Unicorn Horn', 'A tough and shiny horn from a mythical creature.', 0, 5)
calculus_homework = Misc('Calculus Homework', 'A load of random symbols and gibberish', 0, 25)


def monster_drop(level, name):
    monster_drop_list = {'Shell Mimic': [shell_fragment],
                         'Giant Crab': [crab_claw],
                         'Naiad': [fairy_dust],
                         'Sea Serpent': [serpent_scale],
                         'Squid': [ink_sack],
                         'Bog Slime': [slimey_residue],
                         'Moss Ogre': [skeleton_bone],
                         'Sludge Rat': [monster_skull],
                         'Spriggan': [living_bark],
                         'Vine Lizard': [serpent_scale],
                         'Goblin Archer': [shirt_cloth],
                         'Beetle': [beetle_shell],
                         "Will-o'-the-wisp": [fairy_dust],
                         'Imp': [wing_piece],
                         'Bat': [bat_fang],
                         'Mummy': [burnt_ash],
                         'Sand Golem': [golem_rock],
                         'Minubis': [animal_fur],
                         'Fire Ant': [antennae],
                         'Naga': [serpent_scale],
                         'Ice Soldier': [chain_link],
                         'Minor Yeti': [animal_fur],
                         'Corrupt Thaumaturge': [shirt_cloth],
                         'Arctic Wolf': [animal_fur],
                         'Frost Bat': [bat_fang],
                         'Troll': [monster_skull],
                         'Rock Giant': [golem_rock],
                         'Oread': [fairy_dust],
                         'Tengu': [wing_piece],
                         'Giant Worm': [bat_fang],
                         'Zombie': [monster_skull],
                         'Undead Archer': [chain_link],
                         'Necromancer': [shirt_cloth],
                         'Skeleton': [skeleton_bone],
                         'Ghoul': [ectoplasm],
                         'Alicorn': [unicorn_horn],
                         'Wraith': [ectoplasm],
                         'Griffin': [animal_fur],
                         'Flying Serpent': [serpent_scale],
                         'Harpy': [wing_piece],
                         'Calculator': [calculus_homework]}

    if level in range(1, 16):
        drops = [s_elixir, s_potion, bnz_swd, wiz_hat, lth_bdy]

    elif level in range(16, 27):
        drops = [m_elixir, m_potion, lng_bow, myst_gar, stl_leg]

    elif level in range(27, 38):
        drops = [l_elixir, l_potion, rnc_stf, drg_leg, ori_hlm]

    elif level > 37:
        drops = [x_elixir, x_potion, en_myth_sb, ori_leg, elem_gar]

    for x in range(4):
        drops.extend(monster_drop_list[name])

    return drops


def serialize_gems(path):
    with open(path, mode='w') as j:
        json.dump([gem.name for gem in valuable_list if gem.acquired],
                  j, indent=4, separators=(', ', ': '))


def deserialize_gems(path):
    global valuable_list

    with open(path) as j:
        gems = json.load(j)

    for name in gems:
        for gem in valuable_list:
            if gem.name == name:
                gem.acquired = True


# These are bits of code used to get information about various items

# total = 0
# for x in copy.copy(globals()):
#     if isinstance(globals()[x], Item):
#         total += 1
#         print(globals()[x].desc)
# print(total)
#
# for gem in valuable_list:
#     for other in valuable_list:
#         if gem == other:
#             continue
#         if bool(gem.posx > 0) == bool(other.posx > 0):
#             if bool(gem.posy > 0) == bool(other.posy > 0):
#                 print(gem.name,
#                       other.name,
#                       round(math.hypot(gem.posx - other.posx, gem.posy - other.posy)))

# for gem in valuable_list:
#     print(''.join([gem.name, ": ", str((abs(gem.posx) + abs(gem.posy))/2)]))