#   This file is part of Peasants' Ascension.
#
#	 Peasants' Ascension is free software: you can redistribute it and/or modify
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
import units


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
        print('-'*25)

        if is_battle:
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

        user.hp += self.heal
        user.mp += self.mana
        units.fix_stats()
        sounds.magic_healing.play()

        print(f'{user.name} consumes the {self.name}.')

        if not is_battle:
            input("\nPress enter/return ")

        for x, y in enumerate(inv_system.inventory[self.cat]):
            if y.name == self.name:
                inv_system.inventory[self.cat].remove(y)
                break


class StatusPotion(Item):
    def __init__(self, name, desc, buy, sell, status, cat='consum', imp=False, ascart='Potion'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.status = status

    def use_item(self, user, is_battle=False):
        print('-'*25)

        if is_battle:
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

        if user.status_ail == self.status:
            for x, y in enumerate(inv_system.inventory[self.cat]):
                if y.name == self.name:
                    inv_system.inventory[self.cat].remove(y)
                    break

            sounds.buff_spell.play()
            user.status_ail = 'none'

            print(f'{user.name} drinks the {self.name} and feels much better.')

            if not is_battle:
                input("\nPress enter/return ")

        else:
            print(f"Drinking this {self.name} probably wouldn't do anything.")
            input("\nPress enter/return ")


class Weapon(Item):
    # Items that increase your damage by a percentage.
    def __init__(self, name, desc, buy, sell, power, type_, class_, ascart, element='none', cat='weapons', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.power = power
        self.type_ = type_
        self.class_ = class_
        self.element = element

        if isinstance(self.class_, str):
            self.desc = ' '.join([desc, '|', self.class_.title(), 'ONLY'''])

        else:
            self.desc = ' '.join([desc, "[", ', '.join([x.title() for x in self.class_]), ']'])

    def use_item(self, user):
        if user.class_ in self.class_ or self.class_ == 'none':
            # Creating a copy of the weapon ensures that
            # only one weapon can be equipped at a time.
            spam = copy.copy(self)

            if isinstance(inv_system.equipped[user.name if user != units.player else 'player']['weapon'], Weapon):

                old = copy.copy(inv_system.equipped[user.name if user != units.player else 'player']['weapon'])
                inv_system.inventory['weapons'].remove(self)

                if old.name != 'Fists':
                    inv_system.inventory['weapons'].append(old)

                inv_system.equipped[user.name if user != units.player else 'player']['weapon'] = spam

            print('-'*25)
            print('{0} equips the {1}.'.format(user.name, str(self)))
            input("\nPress enter/return ")

        else:
            print('-'*25)

            if isinstance(self.class_, list):
                print(f"{user.name} must be a {self.class_[0].title()} or a {self.class_[1].title()} to equip this.")
                input("\nPress enter/return ")

            else:
                print("{0} must be a {1} to equip this.".format(user.name, self.class_.title()))
                input("\nPress enter/return ")


class Armor(Item):
    # Items that give the player a percent increase in defense when hit.
    def __init__(self, name, desc, buy, sell, defense, type_, part, class_, ascart, cat='armor', imp=False):
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

            if isinstance(inv_system.equipped[user.name if user != units.player else 'player'][self.part], Armor):

                old = copy.copy(inv_system.equipped[user.name if user != units.player else 'player'][self.part])

                inv_system.inventory['armor'].append(old)
                inv_system.inventory['armor'].remove(self)

            else:
                inv_system.equipped[user.name if user != units.player else 'player'][self.part] = fizz
                inv_system.inventory['armor'].remove(self)

            print('-'*25)
            print('{0} equips the {1}.'.format(user.name, str(self)))
            input("\nPress enter/return ")

        else:
            print('-'*25)

            if isinstance(self.class_, list):
                print("{0} must be a {1} or a {2} to equip.".format(
                    user.name, self.class_[0].title(), self.class_[1].title()))

                input("\nPress enter/return ")

            else:
                print("{0} must be a {1} to equip this.".format(user.name, self.class_.title()))
                input("\nPress enter/return ")


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
        if isinstance(inv_system.equipped[user.name if user != units.player else 'player']['access'], Accessory):

            old = copy.copy(inv_system.equipped[user.name if user != units.player else 'player']['access'])
            inv_system.inventory['access'].append(old)

        inv_system.inventory['access'].remove(self)
        inv_system.equipped[user.name if user != units.player else 'player']['access'] = spam
        user.element = self.element

        print('-'*25)
        print('{0} equips the {1}. Their element is now set to {2}.'.format(user.name, self.name, self.element))
        input("\nPress enter/return ")


# -- TOOLS -- #
class MagicCompass(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=True, ascart='Compass'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        if main.party_info['reg'] == 'Aethus':
            print('-'*25)
            print('Something about this place makes your compass needle spin wildly.')
            print('-'*25)
            return

        from towns import town_list, search_towns

        pos_towns = [tuple([town.name, round(math.hypot(town.x - main.party_info['x'],
                                                        town.y - main.party_info['y']))])
                     for town in town_list]
        distance = min(pos_towns, key=lambda x: x[1])

        print('-'*25)
        print(f'The closest town to your party is {distance[0]} at ~{distance[1]} degrees away.')

        if not towns.search_towns(enter=False):
            print('-'*25)


class DiviningRod(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=True, ascart='Div Rod'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        if main.party_info['reg'] == 'Aethus':
            print('-'*25)
            print("Your divining rod doesn't seem to be working properly up here.")
            print('-'*25)
            return

        from towns import search_towns
        pos_gems = [tuple([gem.name, round(math.hypot(gem.posx - main.party_info['x'],
                                                      gem.posy - main.party_info['y']))])
                    for gem in valuable_list if not gem.acquired]

        if not pos_gems:
            return print('Your party is unable to detect any gems.')

        distance = min(pos_gems, key=lambda x: x[1])

        print('-'*25)
        print('The closest gem to your party is {0} {1} at ~{2} degrees away.'.format(
            'an' if any([distance[0].startswith(x) for x in 'AEIOU'])
            else 'a', distance[0], distance[1]))

        if not search_towns(enter=False):
            print('-'*25)


class Shovel(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=True, ascart='Shovel'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        if main.party_info['reg'] == 'Aethus':
            print('-'*25)
            print('The soil up here is much too tough to be broken up using a shovel.')
            print('-'*25)
            return

        from towns import search_towns
        print('-'*25)
        print('Your party begins to search using your shovel...')
        main.smart_sleep(1)

        for gem in valuable_list:
            if (main.party_info['x'], main.party_info['y']) == (gem.posx, gem.posy) \
                    and not gem.acquired:

                gem.acquired = True
                print('Using your shovel, your party manages to uncover a {0}!'.format(gem.name))
                inv_system.inventory['misc'].append(gem)

                if not search_towns(enter=False):
                    print('-'*25)

                return

        print('Your party was unable to uncover anything.')
        if not search_towns(enter=False):
            print('-'*25)


class TownTeleporter(Item):
    def __init__(self, name, desc, buy, sell, cat='tools', imp=False, ascart='Map'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)

    @staticmethod
    def use_item(user):
        from towns import town_list, aethus_towns, search_towns

        print('-'*25)

        if not main.party_info['is_aethus']:
            town_list = town_list

        else:
            town_list = aethus_towns

        available = []

        for town in town_list:
            for visited in main.party_info['visited_towns']:
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
                    input('\nPress enter/return ')

                    main.party_info['x'] = chosen_town[1]
                    main.party_info['y'] = chosen_town[3]
                    main.party_info['h'] = chosen_town[2]
                    main.party_info['v'] = chosen_town[4]

                    world.check_region()
                    search_towns()
                    return

                elif y_n.lower().startswith('n'):
                    break


class LockpickKit(Item):
    def __init__(self, name, desc, buy, sell, power, cat='tools', imp=False, ascart='Lockpick'):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.power = power

    @staticmethod
    def use_item(user):
        print('-'*25)
        print("Your party could certainly make a quick buck lockpicking chests with this thing.")
        print("But that's illegal - you wouldn't break the law, would you?")
        input("\nPress enter/return ")


# -- OTHERS -- #
class Valuable(Item):
    def __init__(self, name, desc, buy, sell, ascart='Gem', acquired=False, cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp, ascart)
        self.acquired = acquired

    def use_item(self, user):
        print('-'*25)
        print(f'Your party admires the {self.name}. It looks very valuable.')
        input("\nPress enter/return ")


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
                            50, 25, 'asleep', ascart='Status')
silence_potion = StatusPotion('Potion of Allowing Speech',
                              "A potion designed to enable the usage of damaged vocal chords.",
                              50, 25, 'silenced', ascart='Status')
poison_potion = StatusPotion('Potion of Curing Disease',
                             'A potion designed to cure even the most deadly of illnesses.',
                             50, 25, 'poisoned', ascart='Status')
weakness_potion = StatusPotion('Potion of Regaining Strength',
                               'A potion designed to help regain lost muscle-mass and stamina.',
                               50, 25, 'weakened', ascart='Status')
blindness_potion = StatusPotion('Potion of Enabling Sight',
                                'A potion designed to help the blind regain their eyesight.',
                                50, 25, 'blinded', ascart='Status')
paralyzation_potion = StatusPotion('Potion of Inducing Motion',
                                   'A potion designed to cure minor paralysis in most of the body.',
                                   50, 25, 'paralyzed', ascart='Status')


# Fists exist to prevent bugs caused by not having any weapon equipped.
fists = Weapon('Fists',
               """Nothing beats good ol' fashioned hand-to-hand combat (No damage bonus)""",
               0, 0, 0, 'melee', 'none', 'Fists')

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
                  'A beautifully-crafted crossbow made from the wood of an ash tree. (+80% Damage)',
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
                     'A brass adornment for your knuckles providing extra punching power (+10% Damage)',
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
                    'An enhanced version of your typical Lead-Weighted Boxing Gloves (+100% Damage)',
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

# Accessories
# -- Elemental Accessories
water_amulet = ElementAccessory('Aquatic Amulet', 'An amulet that imbues its wearer with the power of WATER',
                                375, 175, 'Water')
fire_amulet = ElementAccessory('Infernal Amulet', 'An amulet that imbues its wearer with the power of FIRE',
                               375, 175, 'Fire')
earth_amulet = ElementAccessory('Ground Amulet', 'An amulet that imbues its wearer with the power of EARTH',
                                375, 175, 'Earth')
electric_amulet = ElementAccessory('Galvanic Amulet', 'An amulet that imbues its wearer with the power of ELECTRICITY',
                                   375, 175, 'Electric')
wind_amulet = ElementAccessory('Tempestuous Amulet', 'An amulet that imbues its wearer with the power of WIND',
                               375, 175, 'Wind')
grass_amulet = ElementAccessory('Verdant Amulet', 'An amulet that imbues its wearer with the power of GRASS',
                                375, 175, 'Grass')
ice_amulet = ElementAccessory('Glacial Amulet', 'An amulet that imbues its wearer with the power of ICE',
                              375, 175, 'Ice')
life_amulet = ElementAccessory('Living Amulet', 'An amulet that imbues its wearer with the power of LIFE',
                               375, 175, 'Life')
death_amulet = ElementAccessory('Necrotic Amulet', 'An amulet that imbues its wearer with the power of DEATH',
                                375, 175, 'Death')

# Quest items
message_joseph = Misc('Message from Joseph', 'A neatly written message addressed to Philliard.',
                      0, 0, cat='q_items', imp=True)

message_philliard = Misc('Message from Philliard', 'A neatly written message addressed to Joseph.',
                         0, 0, cat='q_items', imp=True)

iSound = Misc('iSound', "You can't even begin to imagine how one would go about using this.",
              250, 75, cat='q_items', imp=False)


# Gems & Valuables
pearl_gem = Valuable('Pearl', 'A valuable pearl. This could probably be sold for quite a bit.',
                     0, 175)

ruby_gem = Valuable('Ruby', 'A valuable ruby. This could be sold for quite a bit.',
                    0, 175)

sapphire_gem = Valuable('Sapphire', 'A valuable sapphire. This could probably be sold for quite a bit.',
                        0, 175)

emerald_gem = Valuable('Emerald', 'A valuable emerald. This could probably be sold for quite a bit.',
                       0, 175)

citrine_gem = Valuable('Citrine', 'A valuable citrine. This could probably be sold for quite a bit.',
                       0, 175)

jade_gem = Valuable('Jade', 'A valuable jade. This could probably be sold for quite a bit.',
                    0, 175)

opal_gem = Valuable('Opal', 'A valuable opal. This could probably be sold for quite a bit.',
                    0, 175)

onyx_gem = Valuable('Onyx', 'A valuable onyx. This could probably be sold for quite a bit.',
                    0, 175)

diamond_gem = Valuable('Diamond', 'A valuable diamond. This could probably be sold for quite a bit.',
                                  0, 175)

amethyst_gem = Valuable('Amethyst', 'A valuable amethyst. This could probably be sold for quite a bit.',
                                    0, 175)

topaz_gem = Valuable('Topaz', 'A valuable topaz. This could probably be sold for quite a bit.',
                              0, 175)

garnet_gem = Valuable('Garnet', 'A valuable garnet. This could probably be sold for quite a bit.',
                                0, 175)

quartz_gem = Valuable('Quartz', 'A valuable quartz. This could probably be sold for quite a bit.',
                                0, 175)

zircon_gem = Valuable('Zircon', 'A valuable zircon. This could probably be sold for quite a bit.',
                                0, 175)

agate_gem = Valuable('Agate', 'A valuable agate. This could probably be sold for quite a bit.',
                              0, 175)

aquamarine_gem = Valuable('Aquamarine', 'A valuable aquamarine. This could probably be sold for quite a bit.',
                          0, 175)

valuable_list = [pearl_gem, ruby_gem, sapphire_gem, emerald_gem, citrine_gem, jade_gem, opal_gem, onyx_gem, diamond_gem,
                 amethyst_gem, topaz_gem, garnet_gem, quartz_gem, zircon_gem, agate_gem, aquamarine_gem]

# Tools
magic_compass = MagicCompass('Magical Compass', 'A compass capable of detecting nearby towns.', 0, 0, imp=True)
divining_rod = DiviningRod('Divining Rod', 'A magical stick capable of detecting nearby ores and gems.', 300, 150)
shovel = Shovel('Shovel', 'A simple shovel used to excavate for hidden gems and minerals.', 200, 100)
map_of_fast_travel = TownTeleporter('Map of Fast Travel', 'Allows traveling to previously visited towns.', 2000, 100)

# Tools -- Lockpicks
wood_lckpck = LockpickKit('Wooden Lockpick Kit',
                          'A wooden lockpick kit with a 30% chance to open chests.', 30, 15, 30)
copper_lckpck = LockpickKit('Copper Lockpick Kit',
                            'A copper lockpick kit with a 45% chance to open chests.', 200, 100, 45)
iron_lckpck = LockpickKit('Iron Lockpick Kit',
                          'An iron lockpick kit with a 60% chance to open chests.', 300, 150, 60)
steel_lckpck = LockpickKit('Steel Lockpick Kit',
                           'A steel lockpick kit with a 75% chance to open chests.', 500, 250, 75)
mythril_lckpck = LockpickKit('Mythril Lockpick Kit',
                             'A mythril lockpick kit with a 90% chance to open chests.', 750, 375, 90)

# Monster Drops
shell_fragment = Misc('Shell Fragment', "A broken fragment of a once-beautiful sea-creature's shell [JUNK]", 0, 5)
crab_claw = Misc('Crab Claw', 'A reddish claw from a giant crab [JUNK]', 0, 5)
fairy_dust = Misc('Fairy Dust', 'Dust from a fairy. It has strange, magical properties [JUNK]', 0, 5)
serpent_scale = Misc('Serpent Scale', 'A rough scale from an unknown reptile [JUNK]', 0, 5)
ink_sack = Misc('Ink Sack', 'A small pouch full of an inky substance [JUNK]', 0, 5)
bone_bag = Misc('Bag of Bones', 'A bag full of various bones from a now deceased creature [JUNK]', 0, 5)
monster_skull = Misc('Monster Skull', 'A broken skull from a strange creature [JUNK]', 0, 5)
living_bark = Misc('Living Bark', 'This bark has a fleshy texture to it [JUNK]', 0, 5)
ripped_cloth = Misc('Ripped Cloth', 'A thick, torn cloth made out of an unknown fabric [JUNK]', 0, 5)
beetle_shell = Misc('Beetle Shell', 'A bluish shell from a large beetle [JUNK]', 0, 5)
wing_piece = Misc('Wing Piece', 'A piece of wing from a flying creature [JUNK]', 0, 5)
monster_fang = Misc('Monster Fang', 'The sharp fang of a frightening creature [JUNK]', 0, 5)
animal_fur = Misc('Animal Fur', 'A wet clump of fur from a strange animal [JUNK]', 0, 5)
golem_rock = Misc('Golem Rock', 'A small rock that seems to glow slightly [JUNK]', 0, 5)
burnt_ash = Misc('Burnt Ash', 'The ashy remains of a once-living creature [JUNK]', 0, 5)
antennae = Misc('Gooey Antennae', 'A pair of antennae from a massive, slimey insect [JUNK]', 0, 5)
ectoplasm = Misc('Ectoplasm', 'The gooey remains from a terrifying apparition [JUNK]', 0, 5)
chain_link = Misc('Chain links', 'A couple joined links of chain made from steel [JUNK]', 0, 5)
unicorn_horn = Misc('Unicorn Horn', 'A tough and shiny horn from a mythical creature [JUNK]', 0, 5)
demonic_essence = Misc('Demonic Essense', 'A strange orb that exudes a terrifying aura [JUNK]', 0, 5)
angelic_essence = Misc('Angelic Essence', 'A strange orb that radiates an incredible aura [JUNK]', 0, 5)
eye_balls = Misc('Eyeballs', 'The visual receptors of some disgusting creature [JUNK]', 0, 5)
mysterious_runes = Misc('Mysterious Runestone', 'Strange stones with even stranger symbols on it [JUNK]', 0, 5)
rodent_tail = Misc('Rodent Tail', 'The detatched tail of a hideous rodent [JUNK]', 0, 5)
serpent_tongue = Misc('Serpent Tongue', 'A dried-up tongue from a slithery serpent [JUNK]', 0, 5)
feathers = Misc('Feathers', 'A veiny feather from an unknown avian creature [JUNK]', 0, 5)
broken_crystal = Misc('Broken Crystal', 'A chunk of crystal too powdery to be of any value [JUNK]', 0, 5)
slime_vial = Misc('Vial of Slime', 'A small glass vial filled with gooey slime [JUNK]', 0, 5)
blood_vial = Misc('Vial of Blood', 'A small glass vial filled with the blood of an evil creature [JUNK]', 0, 5)
water_vial = Misc('Vial of Water', 'A small glass vial filled with enchanted water [JUNK]', 0, 5)

# Easter egg for my friend
calculus_homework = Misc('Calculus Homework', 'A load of random symbols and gibberish [FUNKY]', 0, 25)
graph_paper = Misc('Graph Paper', 'Useful paper for graphing points and lines [FUNKY]', 0, 25)
ruler = Misc('Ruler', 'A piece of wood with lines on it. Neat! [FUNKY]', 0, 25)
protractor = Misc('Protractor and Compass', 'Instruments used to make shapes and angles [FUNKY]', 0, 25)
textbook = Misc('AtW Textbook', 'More like Algebra that sucks amiright? [FUNKY)', 0, 25)

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
