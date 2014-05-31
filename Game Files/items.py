import sys
import copy
import random
import math
import inv_system

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

    def __str__(self):
        return self.name

    def consume_item(self):
        print('-' * 25)
        global inventory
        item_setup_vars()
        main.player.hp += self.heal
        if main.player.hp > main.static['hp_p']:
            main.player.hp -= (main.player.hp - main.static['hp_p'])
        main.player.mp += self.mana
        if main.player.mp > main.static['mp_p']:
            main.player.mp -= (main.player.mp - main.static['mp_p'])
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
                 element='None', equip=False, cat='weapons', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.power = power
        self.type_ = type_
        self.class_ = class_
        self.equip = equip
        self.element = element
        if self.equip:
            if self.type_ == 'melee':
                main.player.attk += self.power
                main.player.m_attk += int(math.ceil(self.power/3))
            elif self.type_ == 'magic':
                main.player.m_attk += self.power
                main.player.attk += int(math.ceil(self.power/3))

    def __str__(self):
        return self.name

    def equip_weapon(self):
        global equipped
        global inventory
        item_setup_vars()
        if main.player.class_ == self.class_ or self.class_ == 'none':
            spam = copy.copy(self)
            # Creating a copy of the weapon ensures that
            # only one weapon can be equipped at a time.
            if isinstance(equipped['weapon'], Weapon):
                old = copy.copy(equipped['weapon'])
                old.equip = False
                if old.type_ in ['melee', 'ranged']:
                    main.player.attk -= old.power
                elif old.type_ == 'magic':
                    main.player.m_attk -= old.power
            equipped['weapon'] = spam
            if self.type_ in ['melee', 'ranged']:
                main.player.attk += self.power
                main.player.m_attk += int(math.ceil(self.power/3))
            elif self.type_ == 'magic':
                main.player.m_attk += self.power
                main.player.attk += int(math.ceil(self.power/3))
            for x, y in enumerate(inventory[self.cat]):
                if self.name == y.name:
                    key = x
                    y.equip = True
                    break
            try:
                inventory[self.cat][key] = old
            except NameError:
                pass
            print('-'*25)
            print('You equip the {0}.'.format(str(self)))
        else:
            print('-' * 25)
            print("You must be a {0} to equip this.".format(self.class_.title()))


class Armor(Item):
    def __init__(self, name, desc, buy, sell, defense, type_, part,
                 class_, equip=False, cat='armor', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.defense = defense
        self.type_ = type_
        self.part = part
        self.class_ = class_
        self.equip = equip

    def equip_armor(self):
        global equipped
        global inventory
        item_setup_vars()
        if main.player.class_ == self.class_ or self.class_ == 'none':
            fizz = copy.copy(self)  # A copy of the armor is created for the same
                                    # reason as for weapons.
            if isinstance(equipped[self.part], Armor):
                old = copy.copy(equipped[self.part])
                old.equip = False
                if old.type_ == 'melee':
                    main.player.dfns -= old.defense
                    main.player.m_dfns -= int(math.ceil(self.defense/3))
                elif old.type_ == 'magic':
                    main.player.m_dfns -= old.defense
                    main.player.dfns -= int(math.ceil(self.defense/3))
            equipped[self.part] = fizz
            if self.type_ == 'melee':
                main.player.dfns += self.defense
                main.player.m_dfns += int(math.ceil(self.defense/3))
            elif self.type_ == 'magic':
                main.player.m_dfns += self.defense
                main.player.dfns += int(math.ceil(self.defense/3))
            for x, y in enumerate(inventory[self.cat]):
                if self.name == y.name:
                    key = x
                    y.equip = True
                    break
            try:
                inventory[self.cat][key] = old
            except NameError:
                pass
            print('-'*25)
            print('You equip the {0}.'.format(str(self)))
        else:
            print('-'*25)
            print("You must be a {0} to equip this.".format(self.class_.title()))


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

# Weapons -- Warrior
wdn_sht = Weapon('Wooden Shortsword',
                 'A small sword carved from an oak branch (+3 Attack).',
                 10, 5, 3, 'melee', 'warrior')

cpr_swd = Weapon('Copper Sword',
                 'A light yet sturdy sword smelted from copper ore (+5 Attack).',
                 45, 15, 5, 'melee', 'warrior')
en_cpr_swd = Weapon('Enhanced Copper Sword',
                    'An enhanced version of your typical Copper Sword (+7 Attack).',
                    65, 25, 7, 'melee', 'warrior')

bnz_spr = Weapon('Bronze Spear',
                 'A fair-sized spear smelted from a bronze alloy (+10 Attack).',
                 175, 60, 10, 'melee', 'warrior')
en_bnz_spr = Weapon('Enhanced Bronze Spear',
                    'An enhanced version of your typical Bronze Spear (+15 Attack).',
                    250, 75, 15, 'melee', 'warrior')

irn_axe = Weapon('Iron Battleaxe',
                 'A powerful battleaxe smelted from iron ore (+19 Attack).',
                 325, 110, 19, 'melee', 'warrior')
en_irn_axe = Weapon('Enhanced Iron Battleaxe',
                    'An enhanced version of your typical Iron Battleaxe (+25 Attack).',
                    420, 135, 25, 'melee', 'warrior')

# Weapons -- Rogue
stn_dag = Weapon('Stone Dagger',
                 'A crude yet effective knife carved from a light stone (+3 Attack).',
                 10, 5, 3, 'melee', 'rogue')

sht_bow = Weapon('Short Bow',
                 "A bow of great craftsmanship. It's kinda small, though (+5 Attack).",
                 45, 15, 5, 'ranged', 'rogue')
en_sht_bow = Weapon('Enhanced Short Bow',
                    " An enhanced version of your typical Short Bow (+7 Attack).",
                    65, 25, 7, 'ranged', 'rogue')

lng_bow = Weapon('Long Bow',
                 'A much more impressive bow capable of accuracy at long distances (+10 Attack).',
                 175, 60, 10, 'ranged', 'rogue')
en_lng_bow = Weapon('Enhanced Long Bow',
                    'An enhanced version of your typical Long Bow (+15 Attack).',
                    250, 75, 15, 'ranged', 'rogue')

myth_sb = Weapon('Mythril Shortblade',
                 'A knife made of a rare and powerful material (+19 Attack).',
                 325, 115, 19, 'melee', 'rogue')
en_myth_sb = Weapon('Enhanced Mythril Shortblade',
                    'An enhanced version of your typical Mythril Shortblade (+25 Attack).',
                    420, 135, 25, 'melee', 'rogue')

# Weapons -- Mage
mag_twg = Weapon('Magical Twig',
                 'A small stick with basic magical properties (+3 Magic Attack).',
                 10, 5, 3, 'magic', 'mage')

oak_stf = Weapon('Oak Staff',
                 'A wooden staff imbued with weak magical abilities (+5 Magic Attack).',
                 45, 15, 5, 'magic', 'mage')
en_oak_stf = Weapon('Enhanced Oak Staff',
                    'An enhanced version of your typical Oak Staff (+7 Magic Attack).',
                    65, 25, 7, 'magic', 'mage')

arc_spb = Weapon('Arcane Spellbook',
                 'An intermediate spellbook for combat purposes (+10 Magic Attack).',
                 175, 60, 10, 'magic', 'mage')
en_arc_spb = Weapon('Enhanced Arcane Spellbook',
                    'An enhanced version of your typical Arcane Spellbook (+15 Magic Attack).',
                    250, 75, 15, 'magic', 'mage')

rnc_stf = Weapon('Runic Staff',
                 'A powerful staff enchanted with ancient magic (+19 Magic Attack).',
                 325, 115, 19, 'magic', 'mage')
en_rnc_stf = Weapon('Enhanced Runic Staff',
                    'An enhanced version of your typical Runic Staff (+25 Magic Attack',
                    420, 135, 25, 'magic', 'mage')

# Armor -- Warrior -- Weak
bnz_hlm = Armor('Bronze Helmet',
                'A simple helmet crafted from bronze (+1 Defense).',
                20, 8, 1, 'melee', 'head', 'warrior')
bnz_cst = Armor('Bronze Chestpiece',
                'Simple chest armor crafted from bronze (+2 Defense).',
                30, 12, 2, 'melee', 'body', 'warrior')
bnz_leg = Armor('Bronze Leggings',
                'Simple leg armor crafted from bronze (+1 Defense).',
                25, 10, 1, 'melee', 'legs', 'warrior')

en_bnz_hlm = Armor('Enhanced Bronze Helmet',
                   'An enhanced version of your typical bronze helmet (+3 Defense).',
                   60, 25, 3, 'melee', 'head', 'warrior')
en_bnz_cst = Armor('Enhanced Bronze Chestpiece',
                   'An enhanced version of your typical bronze chestpiece (+4 Defense).',
                   70, 35, 4, 'melee', 'body', 'warrior')
en_bnz_leg = Armor('Enhanced Bronze Leggings',
                   'An enhanced version of your typical bronze leggings (+3 Defense).',
                   65, 30, 3, 'melee', 'legs', 'warrior')

# Armor -- Mage -- Weak
wiz_hat = Armor('Wizard Hat',
                'A silk hat woven with magic thread (+1 Magic Defense).',
                20, 8, 1, 'magic', 'head', 'mage')
wiz_rob = Armor('Wizard Robe',
                'A silk robe woven with magic thread (+2 Magic Defense).',
                30, 12, 2, 'magic', 'body', 'mage')
wiz_gar = Armor('Wizard Garments',
                'Silk garments woven with magic thread (+1 Magic Defense).',
                25, 10, 1, 'magic', 'legs', 'mage')

en_wiz_hat = Armor('Enhanced Wizard Hat',
                   'An enhanced version of your typical wizard hat (+3 Magic Defense).',
                   60, 25, 3, 'magic', 'head', 'mage')
en_wiz_rob = Armor('Enhanced Wizard Robe',
                   'An enhanced version of your typical wizard robe (+4 Magic Defense).',
                   70, 35, 4, 'magic', 'body', 'mage')
en_wiz_gar = Armor('Enhanced Wizard Garments',
                   'An enhanced version of your typical wizard garments (+3 Magic Defense).',
                   65, 30, 3, 'magic', 'legs', 'mage')

# Armor -- Rogue -- Weak
lth_cap = Armor('Leather Cap',
                'A simple leather cap providing equally simple protection (+1 Defense).',
                20, 8, 1, 'melee', 'head', 'rogue')
lth_bdy = Armor('Leather Bodyarmor',
                'Simple body armor providing equally simple protection (+1 Defense).',
                30, 12, 1, 'melee', 'body', 'rogue')
lth_leg = Armor('Leather Leggings',
                'Simple leggings providing equally simple protection (+1 Defense).',
                25, 10, 1, 'melee', 'legs', 'rogue')

en_lth_cap = Armor('Enhanced Leather Cap',
                   'An enhanced version of your typical leather cap (+3 Defense).',
                   60, 25, 3, 'melee', 'head', 'rogue')
en_lth_bdy = Armor('Enhanced Leather Bodyarmor',
                   'An enhanced version of your typical leather bodyarmor (+3 Defense).',
                   70, 35, 3, 'melee', 'body', 'rogue')
en_lth_leg = Armor('Enhanced Leather Leggings',
                   'An enhanced version of your typical leather leggings (+3 Defense).',
                   65, 30, 3, 'melee', 'legs', 'rogue')

# Armor -- Warrior -- Mid
irn_hlm = Armor('Iron Helmet',
                'A decent helmet created from a solid metal (+6 Defense).',
                145, 50, 6, 'melee', 'head', 'warrior')
irn_cst = Armor('Iron Chestpiece',
                'Decent body armor made from a solid metal (+7 Defense).',
                165, 60, 7, 'melee', 'body', 'warrior')
irn_leg = Armor('Iron Leggings',
                'Decent leggings made from a solid metal (+6 Defense).',
                155 , 55, 6, 'melee', 'legs', 'warrior')

# Armor -- Mage -- Mid
myst_hat = Armor('Mystical Hood',
                 'A mysterious hood with strange symbols sewn into it (+6 Magic Defense).',
                 145, 50, 6, 'magic', 'head', 'mage')
myst_rob = Armor('Mystical Robe',
                 'A mysterious robe with strange symbols sewn into it (+7 Magic Defense)',
                 165, 60, 7, 'magic', 'body', 'mage')
myst_gar = Armor('Mystical Garments',
                 'Mysterious garments with strange symbols sewn into it (+6 Magic Defense).',
                 155, 55, 6, 'magic', 'legs', 'mage')

# Armor -- Rogue -- Mid
std_cwl = Armor('Studded Cowl',
                'A soft leather cap studded with steel pieces (+6 Defense).',
                145, 50, 6, 'melee', 'head', 'rogue')
std_bdy = Armor('Studded Bodyarmor',
                'Soft leather body armor studded with steel pieces (+6 Defense).',
                165, 60, 6, 'melee', 'body', 'rogue')
std_leg = Armor('Studded Leggings',
                'Soft leather leggings studded with steel pieces (+6 Defense).',
                155, 55, 6, 'melee', 'body', 'rogue')

# Armor -- Warrior -- Pow
stl_hlm = Armor('Steel Helmet',
                'A strong helmet smelted from refined iron (+14 Defense).',
                320, 110, 4, 'melee', 'head', 'warrior')
stl_cst = Armor('Steel Chestplate',
                'Strong chest armor smelted from refined iron (+15 Defense).',
                340, 120, 5, 'melee', 'body', 'warrior')
stl_leg = Armor('Steel Leggings',
                'Strong leg armor smelted from refined iron (+14 Defense).',
                330, 115, 4, 'melee', 'legs', 'warrior')

# Armor -- Mage -- Pow
elem_hat = Armor('Elemental Hat',
                 'A leather hat enchanted with elemental power (+14 Magic Defense).',
                 320, 110, 14, 'magic', 'head', 'mage')
elem_rob = Armor('Elemental Robe',
                 'A leather robe enchanted with elemental power (+15 Magic Defense).',
                 340, 120, 15, 'magic', 'body', 'mage')
elem_gar = Armor('Elemental Garments',
                 'Leather garments enchanted with elemental power (+14 Magic Defense).',
                 330, 115, 14, 'magic', 'legs', 'mage')

# Unique Drops -- Weapons
ice_blade = Weapon('Blade of Frost',
                   'A stunning blade enchanted with the power of ice (+16 Attack, ICE).',
                   0, 225, 16, 'melee', 'warrior', element='ice')
enc_yw = Weapon('Enchanted Yew Wand',
                'A yewen wand of remarkable craftsmanship (+16 Magic Attack, GRASS).',
                0, 225, 16, 'magic', 'mage', element='grass')
spect_wand = Weapon('Spectre Wand',
                    'A ghastly wand made of an indescribable material (+15 Magic Attack, DEATH).',
                    0, 225, 15, 'magic', 'mage', element='death')

unique_drops = {'ice': [ice_blade], 'grass': [enc_yw], 'none': [bnz_leg]}


def monster_drop(level, element):
    if level in range(1, 13):
        drops = [s_elixir, s_potion, m_potion, wdn_sht, cpr_swd, wiz_hat, bnz_hlm]
    elif level in range(13, 26):
        drops = [s_elixir, m_potion, m_elixir, arc_spb, wiz_rob, myst_gar, irn_cst]
    else:
        drops = [l_potion, l_elixir, x_potion, x_elixir, stl_hlm, elem_rob, bnz_spr]
    try:
        return [drops.append(random.choice(unique_drops[element]))] if random.randint(0, 1) else drops
    except (KeyError, IndexError):
        return drops
