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

import inv_system
import sounds

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam

# input = test_input

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

inventory = ''
equipped = ''


class Item:
    # The basic item class. Items are stored in the "inventory" dictionary. All
    # item-subclasses inherit from this class.
    def __init__(self, name, desc, buy, sell, cat='', imp=False):
        self.name = name
        self.desc = desc
        self.buy = buy
        self.sell = sell  # How much money you will get from selling it
        self.cat = cat  # Ensures that items go into the correct inventory slot
        self.imp = imp

    def __str__(self):
        return self.name


class Consumable(Item):
    # Items that restore you HP, MP, or both. All items of this class stacks
    # in the players inventory to increase organization.
    def __init__(self, name, desc, buy, sell,
                 cat='consum', imp=False, heal=0, mana=0):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.heal = heal
        self.mana = mana

    def use_item(self):
        global inventory

        item_setup_vars()

        print('-'*25)

        main.player.hp += self.heal

        sounds.magic_healing.play()

        if main.player.hp > main.misc_vars['hp_p']:
            main.player.hp -= (main.player.hp - main.misc_vars['hp_p'])
        main.player.mp += self.mana

        if main.player.mp > main.misc_vars['mp_p']:
            main.player.mp -= (main.player.mp - main.misc_vars['mp_p'])
        print('You consume the {0}'.format(self.name))

        for x, y in enumerate(inventory[self.cat]):
            if y.name == self.name:
                inventory[self.cat].remove(y)
                break


class Weapon(Item):
    # Items that increase your attack, magic attack, or both when equipped.
    # Certain weapons are planned to be infused with elements later on, which
    # will deal more/less damage to certain enemies.
    def __init__(self, name, desc, buy, sell, power, type_, class_,
                 element='none', equip=False, cat='weapons', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.power = power
        self.type_ = type_
        self.class_ = class_
        self.equip = equip
        self.element = element

        if isinstance(self.class_, str):
            self.desc = ' '.join([desc, '|', self.class_.title(), 'ONLY'''])

        else:
            self.desc = ' '.join([desc, '|', ' and '.join([
                x.title() for x in self.class_]), 'ONLY'])

        if self.equip:
            if self.type_ == 'melee':
                main.player.attk += self.power
                main.player.m_attk += int(math.ceil(self.power/3))
            elif self.type_ == 'magic':
                main.player.m_attk += self.power
                main.player.attk += int(math.ceil(self.power/3))

    def use_item(self):
        global equipped
        global inventory

        item_setup_vars()

        if main.player.class_ in self.class_ or self.class_ == 'none':
            # Creating a copy of the weapon ensures that
            # only one weapon can be equipped at a time.
            spam = copy.copy(self)

            if isinstance(equipped['weapon'], Weapon):
                old = copy.copy(equipped['weapon'])
                old.equip = False
                inventory['weapons'].remove(self)
                if old.name != 'Fists':
                    inventory['weapons'].append(old)

                if old.type_ == 'melee':
                    main.player.attk -= old.power
                    main.player.p_attk -= int(math.ceil(old.power/3))
                    main.player.m_attk -= int(math.ceil(old.power/3))

                elif old.type_ == 'magic':
                    main.player.m_attk -= old.power
                    main.player.p_attk -= int(math.ceil(old.power/3))
                    main.player.attk -= int(math.ceil(old.power/3))

                elif old.type_ == 'ranged':
                    main.player.p_attk -= old.power
                    main.player.m_attk -= int(math.ceil(old.power/3))
                    main.player.attk -= int(math.ceil(old.power/3))

            equipped['weapon'] = spam

            if self.type_ == 'melee':
                main.player.attk += self.power
                main.player.p_attk += int(math.ceil(self.power/3))
                main.player.m_attk += int(math.ceil(self.power/3))

            elif self.type_ == 'ranged':
                main.player.p_attk += self.power
                main.player.attk += int(math.ceil(self.power/3))
                main.player.m_attk += int(math.ceil(self.power/3))

            elif self.type_ == 'magic':
                main.player.m_attk += self.power
                main.player.p_attk += int(math.ceil(self.power/3))
                main.player.attk += int(math.ceil(self.power/3))

            self.equip = True

            print('-'*25)
            input('You equip the {0} | Press enter/return '.format(str(self)))

        else:
            print('-'*25)
            input("You must be a {0} to equip this | Press enter/return ".format(
                self.class_.title()))


class Armor(Item):
    def __init__(self, name, desc, buy, sell, defense, type_, part,
                 class_, equip=False, cat='armor', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.defense = defense
        self.type_ = type_
        self.part = part
        self.class_ = class_
        self.equip = equip
        if self.class_ != 'none':
            if isinstance(self.class_, str):
                self.desc = ' '.join([desc, '|', self.class_.title(), 'ONLY'''])
            else:
                self.desc = ' '.join([desc, '|', ' and '.join([
                    x.title() for x in self.class_]), 'ONLY'])

        else:
            self.desc = ' '.join([desc, '|', "ANY CLASS"])

    def use_item(self):
        global equipped
        global inventory

        item_setup_vars()

        if main.player.class_ in self.class_ or self.class_ == 'none':
            fizz = copy.copy(self)  # A copy of the armor is created for the same
                                    # reason as for weapons.

            if isinstance(equipped[self.part], Armor):
                old = copy.copy(equipped[self.part])
                old.equip = False
                inventory['armor'].remove(self)
                inventory['armor'].append(old)

                if old.type_ == 'melee':
                    main.player.dfns -= old.defense
                    main.player.m_dfns -= int(math.ceil(old.defense/2))
                    main.player.p_dfns -= int(math.ceil(old.defense/1.5))

                elif old.type_ == 'magic':
                    main.player.m_dfns -= old.defense
                    main.player.p_dfns -= int(math.ceil(old.defense/1.5))
                    main.player.dfns -= int(math.ceil(old.defense/2))

            equipped[self.part] = fizz

            if self.type_ == 'melee':
                main.player.dfns += self.defense
                main.player.m_dfns += int(math.ceil(self.defense/2))
                main.player.p_dfns += int(math.ceil(self.defense/1.5))

            elif self.type_ == 'magic':
                main.player.m_dfns += self.defense
                main.player.dfns += int(math.ceil(self.defense/2))
                main.player.p_dfns += int(math.ceil(self.defense/1.5))

            self.equip = True

            print('-'*25)
            input('You equip the {0} | Press enter/return '.format(str(self)))

        else:
            print('-'*25)
            input("You must be a {0} to equip this | Press enter/return ".format(
                self.class_.title()))
            print('-'*25)


class MagicCompass(Item):
    def __init__(self, name, desc, buy, sell, cat='misc', imp=True):
        Item.__init__(self, name, desc, buy, sell, cat, imp)

    def use_item(self):
        from towns import town_list, search_towns

        pos_towns = [tuple([town.name, round(math.hypot(town.x - main.position['x'],
                                                        town.y - main.position['y']))])
                     for town in town_list]
        distance = min(pos_towns, key=lambda x: x[1])

        print('-'*25)
        print('The closest town to you is {0} at ~{1} degrees away.'.format(
            distance[0], distance[1]))

        if not search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)


class DiviningRod(Item):
    def __init__(self, name, desc, buy, sell, cat='misc', imp=True):
        Item.__init__(self, name, desc, buy, sell, cat, imp)

    def use_item(self):
        pos_gems = [tuple([gem.name, round(math.hypot(gem.posx - main.position['x'],
                                                      gem.posy - main.position['y']))])
                    for gem in valuable_list if not gem.acquired]

        if not pos_gems:
            return print('You are unable to detect any gems.')

        distance = min(pos_gems, key=lambda x: x[1])

        print('-'*25)
        print('The closest gem to you is {0} {1} at ~{2} degrees away.'.format(
            'an' if any([distance[0].startswith(x) for x in 'AEIOU'])
            else 'a', distance[0], distance[1]))

        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)


class Valuable(Item):
    def __init__(self, name, desc, buy, sell, posx, posy, acquired=False, cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.posx = posx
        self.posy = posy
        self.acquired = acquired

    def use_item(self):
        print('You admire the {0}. It looks very valuable.'.format(self.name))


class Shovel(Item):
    def __init__(self, name, desc, buy, sell, cat='misc', imp=True):
        Item.__init__(self, name, desc, buy, sell, cat, imp)

    def use_item(self):
        print('-'*25)
        print('You begin to search using your shovel...')
        time.sleep(1)

        for gem in valuable_list:
            if (main.position['x'], main.position['y']) == (gem.posx, gem.posy):
                gem.acquired = True
                print('Using your shovel, you manage to uncover a {0}!'.format(gem.name))
                inventory['misc'].append(gem)
                return

        print('You were unable to uncover anything.')
        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)


class StatusPotion(Item):
    def __init__(self, name, desc, buy, sell, status, cat='consum', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.status = status

    def use_item(self):
        global inventory

        item_setup_vars()

        print('-'*25)

        if main.player.status_ail == self.status:
            sounds.buff_spell.play()
            print('You drink the {0} and feel much better.'.format(self.name))
            main.player.status_ail = 'none'

            for x, y in enumerate(inventory[self.cat]):
                if y.name == self.name:
                    inventory[self.cat].remove(y)
                    break

        else:
            print("Drinking this potion probably wouldn't do anything.")
            print('-'*25)


class Misc(Item):
    def __init__(self, name, desc, buy, sell, cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)

    def use_item(self):
        if 'Message' in self.name:
            print("It would probably be best if you didn't read this.")
        else:
            print("You can't think of anything useful to do with this.")


def item_setup_vars():
    global inventory
    global equipped
    inventory = inv_system.inventory
    equipped = inv_system.equipped


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
                      10, 3, mana=10)
m_elixir = Consumable('Enhanced Elixir',
                      'A more potent elixir that restores 45 MP when consumed.',
                      25, 8, mana=35)
l_elixir = Consumable('Grand Elixir',
                      'A powerful elixir that restores 100 MP when consumed.',
                      50, 17, mana=75)
x_elixir = Consumable('Extreme Elixir',
                      'A super powerful elixir that restores 175 MP when consumed.',
                      100, 35, mana=175)

# Potions -- Both
s_rejuv = Consumable('Minor Rejuvenation Potion',
                     'A basic mixture that restores 15 HP and 15 MP when consumed.',
                     35, 12, heal=15, mana=15)

m_rejuv = Consumable('Refined Rejuvenation Potion',
                     'A higher quality mixture that restores 45 HP and 45 MP when consumed.',
                     65, 22, heal=45, mana=45)

l_rejuv = Consumable('Mighty Rejuvenation Potion',
                     'A super powerful mixture that restores 100 HP and 100 MP when consumed.',
                     225, 80, heal=100, mana=100)

# Potions - Status
sleep_potion = StatusPotion('Potion of Waking Up',
                            "Cures sleep. Don't ask how you're supposed to drink it while asleep.",
                            25, 10, 'asleep')
silence_potion = StatusPotion('Potion of Allowing Speech',
                              "Cures silence. One wonders how your supposed to talk to the seller.",
                              25, 10, 'silenced')
poison_potion = StatusPotion('Potion of Curing Disease',
                             'Cures poison. Testing this potion proved to be difficult.',
                             25, 10, 'poisoned')

# Fists
fists = Weapon('Fists',
               """Nothing beats good ol' fashioned hand-to-hand combat (+0 Attack)""",
               0, 0, 0, 'melee', 'none')  # Fists exist to prevent bugs caused by not having any
                                          # weapon equipped.

# Weapons -- Warrior
wdn_sht = Weapon('Wooden Shortsword',
                 'A small sword carved from an oak branch (+3 Attack)',
                 10, 5, 3, 'melee', 'warrior')

cpr_swd = Weapon('Copper Sword',
                 'A light yet sturdy sword smelted from copper ore (+5 Attack)',
                 45, 15, 5, 'melee', 'warrior')
en_cpr_swd = Weapon('Enhanced Copper Sword',
                    'An enhanced version of your typical Copper Sword (+7 Attack)',
                    65, 25, 7, 'melee', 'warrior')

bnz_spr = Weapon('Bronze Spear',
                 'A fair-sized spear smelted from a bronze alloy (+10 Attack)',
                 175, 60, 10, 'melee', 'warrior')
en_bnz_spr = Weapon('Enhanced Bronze Spear',
                    'An enhanced version of your typical Bronze Spear (+15 Attack)',
                    250, 75, 15, 'melee', 'warrior')

irn_axe = Weapon('Iron Battleaxe',
                 'A powerful battleaxe smelted from iron ore (+19 Attack)',
                 325, 110, 19, 'melee', 'warrior')
en_irn_axe = Weapon('Enhanced Iron Battleaxe',
                    'An enhanced version of your typical Iron Battleaxe (+25 Attack)',
                    420, 135, 25, 'melee', 'warrior')

# Weapons -- Assassin
stn_dag = Weapon('Stone Dagger',
                 'A crude yet effective knife carved from a light stone (+3 Attack)',
                 10, 5, 3, 'melee', 'assassin')

ser_knf = Weapon('Serated Knife',
                 'A durable knife made of iron, with one side made jagged (+5 Attack)',
                 45, 15, 5, 'melee', 'assassin')
en_ser_knf = Weapon('Enhanced Serated Knife',
                    'An enhanced version of your typical Serated Knife (+7 Attack)',
                    65, 25, 7, 'melee', 'assassin')

stiletto = Weapon('Stiletto',
                  'A long, cross-shaped knife perfect for "removing" your enemies (+10 Attack)',
                  175, 60, 10, 'melee', 'assassin')
en_stiletto = Weapon('Enhanced Stiletto',
                     'An enhanced version of your typical Stiletto (+15 Attack)',
                     250, 75, 15, 'melee', 'assassin')

myth_sb = Weapon('Mythril Shortblade',
                 'A knife made of a rare and powerful material (+19 Attack)',
                 325, 115, 19, 'melee', 'assassin')
en_myth_sb = Weapon('Enhanced Mythril Shortblade',
                    'An enhanced version of your typical Mythril Shortblade (+25 Attack)',
                    420, 135, 25, 'melee', 'assassin')

# Weapons -- Ranger
slg_sht = Weapon('Sling Shot',
                 'A weapon that could scare even the mightiest of tin-cans (+3 Pierce)',
                 10, 5, 3, 'ranged', 'ranger')

sht_bow = Weapon('Short Bow',
                 "A bow of great craftsmanship. It's kinda small, though (+5 Pierce)",
                 45, 15, 5, 'ranged', 'ranger')
en_sht_bow = Weapon('Enhanced Short Bow',
                    " An enhanced version of your typical Short Bow (+7 Pierce)",
                    65, 25, 7, 'ranged', 'ranger')

lng_bow = Weapon('Long Bow',
                 'A much more impressive bow capable of accuracy at long distances (+10 Pierce)',
                 175, 60, 10, 'ranged', 'ranger')
en_lng_bow = Weapon('Enhanced Long Bow',
                    'An enhanced version of your typical Long Bow (+15 Pierce)',
                    250, 75, 15, 'ranged', 'ranger')

ash_cbow = Weapon('Ashen Crossbow',
                  'A beautifully-crafted crossbow made fromt the wood of an ash tree. (+19 Pierce)',
                  325, 115, 19, 'ranged', 'ranger')
en_ash_cbow = Weapon('Enhanced Ashen Crossbow',
                     'An enhanced version of your typical Ashen Crossbow (+25 Pierce)',
                     325, 115, 19, 'ranged', 'ranger')

# Weapons -- Mage
mag_twg = Weapon('Magical Twig',
                 'A small stick with basic magical properties (+3 Magic Attack)',
                 10, 5, 3, 'magic', 'mage')

oak_stf = Weapon('Oak Staff',
                 'A wooden staff imbued with weak magical abilities (+5 Magic Attack)',
                 45, 15, 5, 'magic', 'mage')
en_oak_stf = Weapon('Enhanced Oak Staff',
                    'An enhanced version of your typical Oak Staff (+7 Magic Attack)',
                    65, 25, 7, 'magic', 'mage')

arc_spb = Weapon('Arcane Spellbook',
                 'An intermediate spellbook for combat purposes (+10 Magic Attack)',
                 175, 60, 10, 'magic', 'mage')
en_arc_spb = Weapon('Enhanced Arcane Spellbook',
                    'An enhanced version of your typical Arcane Spellbook (+15 Magic Attack)',
                    250, 75, 15, 'magic', 'mage')

rnc_stf = Weapon('Runic Staff',
                 'A powerful staff enchanted with ancient magic (+19 Magic Attack)',
                 325, 115, 19, 'magic', 'mage')
en_rnc_stf = Weapon('Enhanced Runic Staff',
                    'An enhanced version of your typical Runic Staff (+25 Magic Attack',
                    420, 135, 25, 'magic', 'mage')

# Starting Armor (Useless)
straw_hat = Armor('Straw Hat',
                  "Other than keep the sun out of your eyes, this doesn't do much.",
                  0, 2, 0, 'melee', 'head', 'none')
cotton_shirt = Armor('Cotton Shirt',
                     "It's barely even worth the material it's made of.",
                     0, 2, 0, 'melee', 'body', 'none')
sunday_trousers = Armor('Sunday Trousers',
                        "At least they look nice... Wait, isn't it Thursday?",
                        0, 2, 0, 'melee', 'legs', 'none')

# Armor -- Warrior -- Weak
bnz_hlm = Armor('Bronze Helmet',
                'A simple helmet crafted from bronze (+1 Defense)',
                20, 8, 1, 'melee', 'head', 'warrior')
bnz_cst = Armor('Bronze Chestpiece',
                'Simple chest armor crafted from bronze (+2 Defense)',
                30, 12, 2, 'melee', 'body', 'warrior')
bnz_leg = Armor('Bronze Leggings',
                'Simple leg armor crafted from bronze (+1 Defense)',
                25, 10, 1, 'melee', 'legs', 'warrior')

en_bnz_hlm = Armor('Enhanced Bronze Helmet',
                   'An enhanced version of your typical Bronze Helmet (+3 Defense)',
                   60, 25, 3, 'melee', 'head', 'warrior')
en_bnz_cst = Armor('Enhanced Bronze Chestpiece',
                   'An enhanced version of your typical Bronze Chestpiece (+4 Defense)',
                   70, 35, 4, 'melee', 'body', 'warrior')
en_bnz_leg = Armor('Enhanced Bronze Leggings',
                   'An enhanced version of your typical Bronze Leggings (+3 Defense)',
                   65, 30, 3, 'melee', 'legs', 'warrior')

# Armor -- Mage -- Weak
wiz_hat = Armor('Wizard Hat',
                'A silk hat woven with magic thread (+1 Magic Defense)',
                20, 8, 1, 'magic', 'head', 'mage')
wiz_rob = Armor('Wizard Robe',
                'A silk robe woven with magic thread (+2 Magic Defense)',
                30, 12, 2, 'magic', 'body', 'mage')
wiz_gar = Armor('Wizard Garments',
                'Silk garments woven with magic thread (+1 Magic Defense)',
                25, 10, 1, 'magic', 'legs', 'mage')

en_wiz_hat = Armor('Enhanced Wizard Hat',
                   'An enhanced version of your typical Wizard Hat (+3 Magic Defense)',
                   60, 25, 3, 'magic', 'head', 'mage')
en_wiz_rob = Armor('Enhanced Wizard Robe',
                   'An enhanced version of your typical Wizard Robe (+4 Magic Defense)',
                   70, 35, 4, 'magic', 'body', 'mage')
en_wiz_gar = Armor('Enhanced Wizard Garments',
                   'An enhanced version of your typical Wizard Garments (+3 Magic Defense)',
                   65, 30, 3, 'magic', 'legs', 'mage')

# Armor -- Assassin + Ranger -- Weak
lth_cap = Armor('Leather Cap',
                'A simple leather cap providing equally simple protection (+1 Defense)',
                20, 8, 1, 'melee', 'head', ['assassin', 'ranger'])
lth_bdy = Armor('Leather Bodyarmor',
                'Simple body armor providing equally simple protection (+1 Defense)',
                30, 12, 1, 'melee', 'body', ['assassin', 'ranger'])
lth_leg = Armor('Leather Leggings',
                'Simple leggings providing equally simple protection (+1 Defense)',
                25, 10, 1, 'melee', 'legs', ['assassin', 'ranger'])

en_lth_cap = Armor('Enhanced Leather Cap',
                   'An enhanced version of your typical Leather Cap (+3 Defense)',
                   60, 25, 3, 'melee', 'head', ['assassin', 'ranger'])
en_lth_bdy = Armor('Enhanced Leather Bodyarmor',
                   'An enhanced version of your typical Leather Bodyarmor (+3 Defense)',
                   70, 35, 3, 'melee', 'body', ['assassin', 'ranger'])
en_lth_leg = Armor('Enhanced Leather Leggings',
                   'An enhanced version of your typical Leather Leggings (+3 Defense)',
                   65, 30, 3, 'melee', 'legs', ['assassin', 'ranger'])

# Armor -- Warrior -- Mid
stl_hlm = Armor('Steel Helmet',
                'A decent helmet created from a solid metal (+6 Defense)',
                145, 50, 6, 'melee', 'head', 'warrior')
stl_cst = Armor('Steel Chestpiece',
                'Decent body armor made from a solid metal (+7 Defense)',
                165, 60, 7, 'melee', 'body', 'warrior')
stl_leg = Armor('Steel Leggings',
                'Decent leggings made from a solid metal (+6 Defense)',
                155, 55, 6, 'melee', 'legs', 'warrior')

en_stl_hlm = Armor('Enhanced Steel Helmet',
                   'An enhanced version of your typical Steel Helmet (+10 Defense)',
                   260, 75, 10, 'melee', 'head', 'warrior')
en_stl_cst = Armor('Enhanced Steel Chestpiece',
                   'An enhanced version of your typical Steel Chestpiece (+11 Defense)',
                   280, 85, 11, 'melee', 'body', 'warrior')
en_stl_leg = Armor('Enhanced Steel Leggings',
                   'An enhanced version of your typical Steel Leggings (+10 Defense)',
                   270, 80, 10, 'melee', 'legs', 'warrior')


# Armor -- Mage -- Mid
myst_hat = Armor('Mystical Hood',
                 'A mysterious hood with strange symbols sewn into it (+6 Magic Defense)',
                 145, 50, 6, 'magic', 'head', 'mage')
myst_rob = Armor('Mystical Robe',
                 'A mysterious robe with strange symbols sewn into it (+7 Magic Defense)',
                 165, 60, 7, 'magic', 'body', 'mage')
myst_gar = Armor('Mystical Garments',
                 'Mysterious garments with strange symbols sewn into it (+6 Magic Defense)',
                 155, 55, 6, 'magic', 'legs', 'mage')

en_myst_hat = Armor('Enhanced Mystical Hood',
                    'An enhanced version of your typical Mystical Hood (+10 Magic Defense)',
                    260, 75, 10, 'magic', 'head', 'mage')
en_myst_rob = Armor('Enhanced Mystical Robe',
                    'An enhanced version of your typical Mystical Robe (+11 Magic Defense)',
                    280, 85, 11, 'magic', 'body', 'mage')
en_myst_gar = Armor('Enhanced Mystical Garments',
                    'An enhanced version of your typical Mystical Garments (+10 Magic Defense)',
                    270, 80, 10, 'magic', 'legs', 'mage')

# Armor -- Assassin + Ranger -- Mid
std_cwl = Armor('Studded Cowl',
                'A soft leather cap studded with steel pieces (+6 Defense)',
                145, 50, 6, 'melee', 'head', ['assassin', 'ranger'])
std_bdy = Armor('Studded Body-armor',
                'Soft leather body armor studded with steel pieces (+6 Defense)',
                165, 60, 6, 'melee', 'body', ['assassin', 'ranger'])
std_leg = Armor('Studded Leggings',
                'Soft leather leggings studded with steel pieces (+6 Defense)',
                155, 55, 6, 'melee', 'legs', ['assassin', 'ranger'])

en_std_cwl = Armor('Enhanced Studded Cowl',
                   'An enhanced version of your typical Studded Hood (+10 Defense)',
                   260, 75, 10, 'melee', 'head', ['assassin', 'ranger'])
en_std_bdy = Armor('Enhanced Studded Body-armor',
                   'An enhanced version of your typical Studded Bodyarmor (+10 Defense)',
                   280, 85, 10, 'melee', 'body', ['assassin', 'ranger'])
en_std_leg = Armor('Enhanced Studded Leggings',
                   'An enhanced version of your typical Studded Leggings (+10 Defense)',
                   270, 80, 10, 'melee', 'legs', ['assassin', 'ranger'])


# Armor -- Warrior -- Pow
ori_hlm = Armor('Orichalcum Helmet',
                'A strong helmet smelted from rare mountain copper  (+14 Defense)',
                320, 110, 14, 'melee', 'head', 'warrior')
ori_cst = Armor('Orichalcum Chestplate',
                'Strong chest armor smelted from rare mountain copper  (+15 Defense)',
                340, 120, 15, 'melee', 'body', 'warrior')
ori_leg = Armor('Orichalcum Leggings',
                'Strong leg armor smelted from rare mountain copper (+14 Defense)',
                330, 115, 14, 'melee', 'legs', 'warrior')

# Armor -- Mage -- Pow
elem_hat = Armor('Elemental Hat',
                 'A leather hat enchanted with elemental power (+14 Magic Defense)',
                 320, 110, 14, 'magic', 'head', 'mage')
elem_rob = Armor('Elemental Robe',
                 'A leather robe enchanted with elemental power (+15 Magic Defense)',
                 340, 120, 15, 'magic', 'body', 'mage')
elem_gar = Armor('Elemental Garments',
                 'Leather garments enchanted with elemental power (+14 Magic Defense).',
                 330, 115, 14, 'magic', 'legs', 'mage')

# Armor -- Assassin + Ranger -- Pow
drg_cwl = Armor('Dragonhide Cowl',
                'A tough hood crafted from high-quality dragonskin (+14 Defense)',
                320, 110, 14, 'melee', 'head', ['assassin', 'ranger'])
drg_bdy = Armor('Dragonhide Bodyarmor',
                'Tough bodyarmor crafted from high-quality dragonskin (+14 Defense)',
                340, 120, 14, 'melee', 'body', ['assassin', 'ranger'])
drg_leg = Armor('Dragonhide Leggings',
                'Tough leggings crafted from high-quality dragonskin (+14 Defense)',
                330, 115, 14, 'melee', 'legs', ['assassin', 'ranger'])

# Unique Drops -- Weapons
ice_blade = Weapon('Blade of Frost',
                   'A stunning blade enchanted with the power of ice (+16 Attack, ICE)',
                   0, 225, 16, 'melee', 'warrior', element='ice')
enc_yw = Weapon('Enchanted Yew Wand',
                'A yewen wand of remarkable craftsmanship (+16 Magic Attack, GRASS)',
                0, 225, 16, 'magic', 'mage', element='grass')
spect_wand = Weapon('Spectre Wand',
                    'A ghastly wand made of an indescribable material (+15 Magic Attack, DEATH)',
                    0, 225, 15, 'magic', 'mage', element='death')

# Quest items
message_joseph = Misc('Message from Joseph',
                      'A neatly written message addressed from Joseph to Philliard.',
                      0, 0, cat='q_items', imp=True)
message_philliard = Misc('Message from Philliard',
                         'A neatly written message addressed from Philliard to Joseph.',
                         0, 0, cat='q_items', imp=True)

# Gems & Valuables
pearl_gem = Valuable('Pearl', 'A valuable pearl. This could probably be sold for quite a bit.',
                     0, 150, 119, -121)
    # Alternate Description: Impossible to read, but will sell for money nonetheless

ruby_gem = Valuable('Ruby', 'A valuable ruby. Could be sold for quite a bit.',
                    0, 150, -62, -84)  # better_than_perl=True

sapphire_gem = Valuable('Sapphire',
                        'A valuable sapphire. This could probably be sold for quite a bit.',
                        0, 150, -78, 102)

emerald_gem = Valuable('Emerald',
                       'A valuable emerald. This could probably be sold for quite a bit.',
                       0, 150, 26, -13)

citrine_gem = Valuable('Citrine',
                       'A valuable citrine. This could probably be sold for quite a bit.',
                       0, 150, 53, 92)

jade_gem = Valuable('Jade', 'A valuable jade. This could probably be sold for quite a bit.',
                    0, 150, 99, -107)

valuable_list = [pearl_gem, ruby_gem, sapphire_gem, emerald_gem, citrine_gem, jade_gem]

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


# Monster Drops
shell_fragment = Misc('Shell Fragment', 'A broken fragment of a remarkable sea-shell.', 0, 5)
crab_claw = Misc('Crab Claw', 'A reddish claw from a giant crab.', 0, 5)
fairy_dust = Misc('Fairy Dust', 'Dust from a fairy. It has strange, magical properties.', 0, 5)
serpent_scale = Misc('Serpent Scale', 'A rough scale from an unknown reptile.', 0, 5)
slimey_residue = Misc('Slimey Residue', 'The slimey remains of a slimey monster.', 0, 5)
ink_sack = Misc('Ink Sack', 'A small pouch full of an inky substance.', 0, 5)
skeleton_bone = Misc('Skeleton Bone', 'The leg bone of a now-deceased creature.', 0, 5)
monster_skull = Misc('Monster Skull', 'A broken skull from a strange creature.', 0, 5)
plant_stalk = Misc('Plant Stalk', 'The decaying stalk of a large plant.', 0, 5)
shirt_cloth = Misc('Cloth', 'A thick, torn cloth made out of an unknown fabric.', 0, 5)
beetle_shell = Misc('Beetle Shell', 'A bluish shell from a large beetle.', 0, 5)
wing_piece = Misc('Wing Piece', 'A piece of wing from a flying creature.', 0, 5)
bat_fang = Misc('Fang', 'The sharp fang of a frightening creature.', 0, 5)
animal_fur = Misc('Animal Fur', 'A furry clump of hair from a strange animal.', 0, 5)
golem_rock = Misc('Rock', 'A small rock that seems to glow slightly.', 0, 5)
burnt_ash = Misc('Ash', 'The ashy remains of a once-living creature.', 0, 5)
antennae = Misc('Antennae', 'A pair of antennae from a massive insect.', 0, 5)
ectoplasm = Misc('Ectoplasm', 'The gooey remains from a terrifying apparition.', 0, 5)
chain_link = Misc('Chain links', 'A couple jointed link of chain made from steel.', 0, 5)


def monster_drop(level, name):
    monster_drop_list = {'Shell Mimic': [shell_fragment],
                         'Giant Crab': [crab_claw],
                         'Naiad': [fairy_dust],
                         'Sea Serpent': [serpent_scale],
                         'Squid': [ink_sack],
                         'Bog Slime': [slimey_residue],
                         'Moss Ogre': [skeleton_bone],
                         'Sludge Rat': [monster_skull],
                         'Walking Venus': [plant_stalk],
                         'Vine Lizard': [serpent_scale],
                         'Goblin': [shirt_cloth],
                         'Beetle': [beetle_shell],
                         'Sprite': [fairy_dust],
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
                         'Undead Warrior': [chain_link],
                         'Necromancer': [shirt_cloth],
                         'Skeleton': [skeleton_bone],
                         'Ghoul': [ectoplasm]}

    if level in range(1, 16):
        drops = [s_elixir, s_potion, cpr_swd, wiz_hat, lth_bdy]

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