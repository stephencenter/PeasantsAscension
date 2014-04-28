import sys
import copy
import random
import inv_system

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]
inventory = ''
equipped = ''


class Item: # The basic item class. Items are stored in the "inventory" diction-
            # -ary. All item-subclasses inherit from this class.
    def __init__(self, name, desc, buy, sell, cat='', imp=False):
        self.name = name
        self.desc = desc
        self.buy = buy
        self.sell = sell # How much money you will get from selling it
        self.cat = cat # Ensures that items go into the correct inventory slot
        self.imp = imp
    def __str__(self):
        return self.name


class Consumable(Item): # Items that restore you HP, MP, or both. All items of
                        # this class stacks in the players inventory to increas-
                        # -e organization.
    def __init__(self, name, desc, buy, sell, cat='consum', imp=False, heal=0, mana=0):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.heal = heal
        self.mana = mana
    def __str__(self):
        return self.name
    def consume_item(self):
        print('-'*25)
        main.player.hp += self.heal
        if main.player.hp > main.static['hp_p']:
            main.player.hp -= (main.player.hp - main.static['hp_p'])
        main.player.mp += self.mana
        if main.player.mp > main.static['mp_p']:
            main.player.mp -= (main.player.mp - main.static['mp_p'])
        print('You consume the {0}'.format(self.name))
        inventory[self.cat].remove(self)
        print('-'*25)


class Weapon(Item): # Items that increase your attack, magic attack, or both wh-
                    # -en equipped. Certain weapons are planned to be infused w-
                    # -ith elements later on, which will deal more/less damage
                    # to certain enemies.
    def __init__(self, name, desc, buy, sell, power, type, _class,
                 element='None', equip=False,  cat='weapons', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.power = power
        self.type = type
        self._class = _class
        self.equip = equip
        self.element = element
        if self.equip:
            if self.type == 'melee':
                main.player.attk += self.power
            elif self.type == 'magic':
                main.player.m_attk += self.power
    def __str__(self):
        return self.name
    def equip_weapon(self):
        global equipped
        global inventory
        item_setup_vars()
        if main.player._class == self._class:
            spam = copy.copy(self) # Creating a copy of the weapon ensures that
                                   # only one weapon can be equipped at a time.
            spam.equip = True # If a copy of the weapon wasn't created, setting
                              # equip to "true" would break the game by setting
                              # every weapon with the same name as equipped, al-
                              # -so. This would obviously not be ideal.
            if isinstance(equipped['weapon'], Weapon):
                old = copy.copy(equipped['weapon'])
                old.equip = False
                if old.type == 'melee':
                    main.player.attk -= old.power
                elif old.type == 'magic':
                    main.player.m_attk -= old.power
            equipped['weapon'] = spam
            if self.type == 'melee':
                main.player.attk += self.power
            elif self.type == 'magic':
                main.player.m_attk += self.power
            for x, y in enumerate(inventory[self.cat]):
                if self.name == y.name:
                    key = x
                    break
            try:
                inventory[self.cat][key] = old
            except NameError:
                pass
            print('-'*25)
            print('You equip the {0}.'.format(str(self)))
        else:
            print('-'*25)
            print("You must be a {0} to equip this.".format(self._class.title()))


class Armor(Item):
    def __init__(self, name, desc, buy, sell, defense, type, part,
                 _class, equip=False,  cat='armor', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.defense = defense
        self.type = type
        self.part = part
        self._class = _class
        self.equip = equip
    def __str__(self):
        return self.name
    def equip_armor(self):
        global equipped
        global inventory
        item_setup_vars()
        if main.player._class == self._class:
            fizz = copy.copy(self) # A copy of the armor is created for the same
                                   # reason as for weapons.
            fizz.equip = True
            if isinstance(equipped[self.part], Armor):
                old = copy.copy(equipped[self.part])
                old.equip = False
                if old.type == 'melee':
                    main.player.dfns -= old.defense
                elif old.type == 'magic':
                    main.player.m_dfns -= old.defense
            equipped[self.part] = fizz
            if self.type == 'melee':
                main.player.dfns += self.defense
            elif self.type == 'magic':
                main.player.m_dfns += self.defense
            for x, y in enumerate(inventory[self.cat]):
                if self.name == y.name:
                    key = x
                    break
            try:
                inventory[self.cat][key] = old
            except NameError:
                pass
            print('-'*25)
            print('You equip the {0}.'.format(str(self)))
        else:
            print('-'*25)
            print("You must be a {0} to equip this.".format(self._class.title()))


def item_setup_vars():
    global inventory
    global equipped
    inventory = inv_system.inventory
    equipped = inv_system.equipped


# Potions
s_potion = Consumable('Weak Potion', 'A small potion that restores 15 HP when consumed.', 15, 5, heal=15)
m_potion = Consumable('Basic Potion', 'A regular potion that restores 45 HP when consumed.', 45, 15, heal=45)
l_potion = Consumable('Strong Potion', 'A powerful potion that restores 100 HP when consumed.', 100, 35, heal=100)

s_elixr = Consumable('Basic Elixr', 'A generic elixr that restores 15 MP when consumed.', 15, 5, mana=15)
m_elixr = Consumable('Enhanced Elixr', 'A more potent elixr that restores 45 MP when consumed.', 45, 15, mana=45)
l_elixr = Consumable('Grand Elixr', 'A powerful elixr that restores 100 MP when consumed.', 100, 35, mana=100)

# Weapons
wdn_sht = Weapon('Wooden Shortsword', 'A small sword carved from an oak branch (+2 Attack).', 10, 5, 2, 'melee', 'warrior')
cpr_swd = Weapon('Copper Sword', 'A light yet sturdy sword smelted from copper ore (+5 Attack).', 45, 15, 5, 'melee', 'warrior')
bnz_spr = Weapon('Bronze Spear', 'A fair-sized spear smelted from a bronze alloy (+10 Attack).', 175, 60, 10, 'melee', 'warrior')
irn_axe = Weapon('Iron Battleaxe', 'A powerful battleaxe smelted from iron ore (+19 Attack).', 325, 110, 19, 'melee', 'warrior')

mag_twg = Weapon('Magical Twig', 'A small stick with basic magical properties. (+2 Magic Attack).', 10, 5, 2, 'magic', 'mage')
oak_stf = Weapon('Oak Staff', 'A wooden staff imbued with weak magical abilities (+5 Magic Attack).', 45, 15, 5, 'magic', 'mage')
arc_spb = Weapon('Arcane Spellbook', 'An intermediate spellbook for combat purposes. (+10 Magic Attack).', 175, 60, 10, 'magic', 'mage')
rnc_stf = Weapon('Runic Staff', 'A powerful staff enchanted with ancient magic. (+19 Magic Attack).', 325, 115, 19, 'magic', 'mage')

# Armor
bnz_hlm = Armor('Bronze Helmet', 'A simple helmet crafted from bronze (+1 Defense).', 25, 8, 1, 'melee', 'head', 'warrior')
bnz_cst = Armor('Bronze Chestpiece', 'Simple chest armor crafted from bronze (+1 Defense).', 35, 12, 1, 'melee', 'body', 'warrior')
bnz_leg = Armor('Bronze Leggings', 'Simple leg armor crafted from bronze (+1 Defense).', 30, 10, 1, 'melee', 'legs', 'warrior')

wiz_hat = Armor('Wizard Hat', 'A silk hat woven with magic thread (+1 Magic Defense).', 25, 8, 1, 'magic', 'head', 'mage')
wiz_rob = Armor('Wizard Robe', 'A silk robe woven with magic thread (+1 Magic Defense).', 35, 12, 1, 'magic', 'body', 'mage')
wiz_gar = Armor('Wizard Garments', 'Silk garments woven with magic thread (+1 Magic Defense).', 30, 10, 1, 'magic', 'legs', 'mage')

irn_hlm = Armor('Iron Helmet', 'A decent helmet created from a solid metal (+2 Defense).', 150, 50, 2, 'melee', 'head', 'warrior')
irn_cst = Armor('Iron Chestpiece', 'Decent body armor made from a solid metal (+3 Defense).', 175, 60, 3, 'melee', 'body', 'warrior')
irn_leg = Armor('Iron Leggings', 'Decent leggings made from a solid metal (+2 Defense).', 160, 55, 2, 'melee', 'legs', 'warrior')

myst_hat = Armor('Mystical Hood', 'A mysterious hood with strange symbols sewn into it (+2 Magic Defense).', 150, 50, 2, 'magic', 'head', 'mage')
myst_rob = Armor('Mystical Robe', 'A mysterious robe with strange symbols sewn into it (+3 Magic Defense)', 175, 60, 3, 'magic', 'body', 'mage')
myst_gar = Armor('Mystical Garmnets', 'Mysterious garments with strange symbols sewn into it (+2 Magic Defense).', 160, 55, 2, 'magic', 'legs', 'mage')

stl_hlm = Armor('Steel Helmet', 'A strong helmet smelted from refined iron (+4 Defense).', 325, 110, 4, 'melee', 'head', 'warrior')
stl_cst = Armor('Steel Chestplate', 'Strong chest armor smelted from refined iron (+5 Defense).', 350, 120, 5, 'melee', 'body', 'warrior')
stl_leg = Armor('Steel Leggings', 'Strong leg armor smelted from refined iron (+4 Defense).', 335, 115, 4, 'melee', 'legs', 'warrior')

elem_hat = Armor('Elemental Hat', 'A leather hat enchanted with elemental power (+4 Magic Defense).', 325, 110, 4, 'magic', 'head', 'mage')
elem_rob = Armor('Elemental Robe', 'A leather robe enchanted with elemental power (+5 Magic Defense).', 350, 120, 5, 'magic', 'body', 'mage')
elem_gar = Armor('Elemental Garments', 'Leather garments enchanted with elemental power (+4 Magic Defense).', 335, 115, 4, 'magic', 'legs', 'mage')

# Unique Drops
ice_blade = Weapon('Blade of Frost', 'A stunning blade enchanted with the power of ice (+16 Attack, ICE).', 0, 225, 16, 'melee', 'warrior', element='Ice')
enc_yw = Weapon('Enchanted Yew Wand', 'A yewen wand of remarkable craftsmanship (+16 Magic Attack, GRASS).', 0, 225, 16, 'magic', 'mage', element='Grass')

unique_drops = {'Ice': [ice_blade], 'Grass': [enc_yw], 'None': [bnz_leg]}


def monster_drop(level, element):
    if level in range(1, 13):
        drops = [s_elixr, s_potion, m_potion, wdn_sht, cpr_swd, wiz_hat, bnz_hlm]
    elif level in range(13, 26):
        drops = [s_elixr, m_potion, m_elixr, arc_spb, wiz_rob, myst_gar, irn_cst]
    else:
        drops = [m_potion, m_elixr, l_potion, l_elixr, stl_hlm, elem_rob, bnz_spr]
    if random.randint(0, 1) == 1:
        drops.append(random.choice(unique_drops[element]))
    return drops
