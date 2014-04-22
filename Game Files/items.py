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
        print('You consume the %s' % (self.name))
        inventory[self.cat].remove(self)
        print('-'*25)

class Weapon(Item): # Items that increase your attack, magic attack, or both wh-
                    # -en equipped. Certain weapons are planned to be infused w-
                    # -ith elements later on, which will deal more/less damage
                    # to certain enemies.
    def __init__(self, name, desc, buy, sell, power, type, element='None', req_lvl=1, equip=False,  cat='weapons', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.power = power
        self.type = type
        self.req_lvl = req_lvl
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
        if main.player.lvl >= self.req_lvl:
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
            inventory[self.cat][key] = fizz
            print('-'*25)
            print('You equip the %s.' % (str(self)))
        else:
            print('-'*25)
            print("You aren't a high enough to equip this yet. (Must be level %s to equip)" % (self.req_lvl))

class Armor(Item):
    def __init__(self, name, desc, buy, sell, defense, type, part, req_lvl=1, equip=False,  cat='armor', imp=False):
        Item.__init__(self, name, desc, buy, sell, cat, imp)
        self.defense = defense
        self.type = type
        self.part = part
        self.req_lvl = req_lvl
        self.equip = equip
    def __str__(self):
        return self.name
    def equip_armor(self):
        global equipped
        global inventory
        item_setup_vars()
        if main.player.lvl >= self.req_lvl:
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
            inventory[self.cat][key] = fizz
            print('-'*25)
            print('You equip the %s.' % (str(self)))
        else:
            print('-'*25)
            print("You aren't a high enough to equip this yet. (Must be level %s to equip)" % (self.req_lvl))

def sell_item():
    global inventory
    item_setup_vars()
    print('-'*25)
    while True:
        cat = input('Sell: Armor, Consum, Misc, Weapons | Input Category Name (or type "exit"): ')
        try:
            cat = cat.lower()
        except AttributeError:
            continue
        if cat == 'exit':
            return
        elif cat in ['coord', 'quest'] or cat not in ['armor', 'weapons', 'consum', 'misc']:
            continue
        elif cat in ['weapons', 'armor']:
            category = [item for item in inventory[cat] if not item.equip]
            if not category:
                print('-'*25)
                print('The "%s" category is empty...' % (cat))
                print('-'*25)
                continue
        else:
            if not inventory[cat]:
                print('-'*25)
                print('The "%s" category is empty...' % (cat))
                print('-'*25)
                continue
            category = copy.copy(inventory[cat])
        while True:
            if not category:
                break
            item = input(cat.title() + ': ' + str([str(x) for x in category]) + ' | Input Item Name (or type "back"): ')
            try:
                item = item.title()
            except AttributeError:
                continue
            if item == 'Back':
                break
            for i in category:
                if str(i) == item:
                    item = i
                    break
            if item.imp:
                print('-'*25)
                print('You cannot sell important items.')
                print('-'*25)
            else:
                continue
            while item in category:
                choice = input('"Ya want to sell this %s for %s GP?" | Yes or No: ' % (str(item), item.sell))
                try:
                    choice = choice.lower()
                except AttributeError:
                    continue
                if choice in ['yes', 'y']:
                    print('-'*25)
                    print('You hand the shopkeeper your %s and take %s GP in return.' % (str(item), item.sell))
                    print('-'*25)
                    main.static['gp'] += item.sell
                    inventory[cat].remove(item)
                    category.remove(item)
                elif choice in ['no', 'n']:
                    break

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
wdn_dag = Weapon('Wooden Dagger', 'A small dagger carved from an oak branch (+2 Attack).', 10, 5, 2, 'melee')
cpr_swd = Weapon('Copper Sword', 'A light yet sturdy sword smelted from copper ore (+5 Attack).', 45, 15, 5, 'melee', req_lvl=3)
bnz_spr = Weapon('Bronze Spear', 'A fair-sized spear smelted from a bronze alloy (+10 Attack).', 175, 60, 10, 'melee', req_lvl=10)
irn_axe = Weapon('Iron Battleaxe', 'A powerful battleaxe smelted from iron ore (+19 Attack).', 325, 110, 19, 'melee', req_lvl=23)

oak_stf = Weapon('Oak Staff', 'A wooden staff imbued with weak magical abilities (+5 Magic Attack).', 45, 15, 5, 'magic', req_lvl=3)
arc_spb = Weapon('Arcane Spellbook', 'An intermediate spellbook for combat purposes. (+10 Magic Attack).', 175, 60, 10, 'magic', req_lvl=10)
rnc_stf = Weapon('Runic Staff', 'A powerful staff enchanted with ancient magic. (+19 Magic Attack).', 325, 115, 19, 'magic', req_lvl=23)

# Armor
lthr_hlm = Armor('Leather Helmet', 'A simple helmet crafted from leather (+1 Defense).', 25, 8, 1, 'melee', 'head', req_lvl=3)
lthr_cst = Armor('Leather Chestpiece', 'Simple chest armor crafted from leather (+1 Defense).', 35, 12, 1, 'melee', 'body', req_lvl=3)
lthr_leg = Armor('Leather Leggings', 'Simple leg armor crafted from leather (+1 Defense).', 30, 10, 1, 'melee', 'legs', req_lvl=3)

wiz_hat = Armor('Wizard Hat', 'A silk hat woven with magic thread (+1 Magic Defense).', 25, 8, 1, 'magic', 'head', req_lvl=3)
wiz_rob = Armor('Wizard Robe', 'A silk robe woven with magic thread (+1 Magic Defense).', 35, 12, 1, 'magic', 'body', req_lvl=3)
wiz_gar = Armor('Wizard Garments', 'Silk garments woven with magic thread (+1 Magic Defense).', 30, 10, 1, 'magic', 'legs', req_lvl=3)

chn_hlm = Armor('Chainmail Helmet', 'A chain helmet created from a weak metal (+2 Defense).', 150, 50, 2, 'melee', 'head', req_lvl=10)
chn_cst = Armor('Chainmail Chestpiece', 'Chain body armor made from a weak metal (+3 Defense).', 175, 60, 3, 'melee', 'body', req_lvl=10)
chn_leg = Armor('Chainmail Leggings', 'Chain leggings made from a weak metal (+2 Defense).', 160, 55, 2, 'melee', 'legs', req_lvl=10)

myst_hat = Armor('Mystical Hood', 'A mysterious hood with strange symbols sewn into it (+2 Magic Defense).', 150, 50, 2, 'magic', 'head', req_lvl=10)
myst_rob = Armor('Mystical Robe', 'A mysterious robe with strange symbols sewn into it (+3 Magic Defense)', 175, 60, 3, 'magic', 'body', req_lvl=10)
myst_gar = Armor('Mystical Garmnets', 'Mysterious garments with strange symbols sewn into it (+2 Magic Defense).', 160, 55, 2, 'magic', 'legs', req_lvl=10)

stl_hlm = Armor('Steel Helmet', 'A strong helmet smelted from refined iron (+4 Defense).', 325, 110, 4, 'melee', 'head', req_lvl=23)
stl_cst = Armor('Steel Chestplate', 'Strong chest armor smelted from refined iron (+5 Defense).', 350, 120, 5, 'melee', 'body', req_lvl=23)
stl_leg = Armor('Steel Leggings', 'Strong leg armor smelted from refined iron (+4 Defense).', 335, 115, 4, 'melee', 'legs', req_lvl=23)

elem_hat = Armor('Elemental Hat', 'A leather hat enchanted with elemental power (+4 Magic Defense).', 325, 110, 4, 'magic', 'head', req_lvl=23)
elem_rob = Armor('Elemental Robe', 'A leather robe enchanted with elemental power (+5 Magic Defense).', 350, 120, 5, 'magic', 'body', req_lvl=23)
elem_gar = Armor('Elemental Garments', 'Leather garments enchanted with elemental power (+4 Magic Defense).', 335, 115, 4, 'magic', 'legs', req_lvl=23)

# Unique Drops
ice_blade = Weapon('Blade of Frost', 'A stunning blade enchanted with the power of ice (+16 Attack, ICE).', 0, 225, 16, 'melee', req_lvl=14, element='Ice')

unique_drops = {'Ice': [ice_blade], 'None':[lthr_leg]}

def monster_drop(level, element):
    if level in range(1, 13):
        drops = [s_elixr, s_potion, m_potion, wdn_dag, cpr_swd, wiz_hat, lthr_hlm]
    elif level in range(13, 26):
        drops = [s_elixr, m_potion, m_elixr, arc_spb, wiz_rob, myst_gar, chn_cst]
    else:
        drops = [m_potion, m_elixr, l_potion, l_elixr, stl_hlm, elem_rob, bnz_spr]
    if random.randint(0, 1) == 1:
        drops.append(random.choice(unique_drops[element]))
    return drops
