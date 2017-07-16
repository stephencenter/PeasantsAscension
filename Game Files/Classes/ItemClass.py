#   This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
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
import inv_system
import save_load
import sounds
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Item:
    # The basic item class. Items are stored in the "inventory" dictionary. All
    # item-subclasses inherit from this class.
    def __init__(self, name, desc, buy, sell, item_id, imp, ascart, cat):
        self.name = name
        self.desc = desc
        self.buy = buy
        self.sell = sell
        self.imp = imp
        self.ascart = ascart
        self.cat = cat
        self.item_id = item_id

    def __str__(self):
        return self.name


class Consumable(Item):
    # Items that restore your HP, MP, or both
    def __init__(self, name, desc, buy, sell, item_id, cat='consumables', imp=False, heal=0, mana=0, ascart='Potion'):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)
        self.heal = heal
        self.mana = mana

    def use_item(self, user, is_battle=False):
        print('-'*save_load.divider_size)
        print(f'{user.name} consumes the {self.name}...')

        main.smart_sleep(0.75)
        sounds.magic_healing.play()

        if self.heal > 0:
            user.hp += self.heal
            print(f"{user.name} restored {self.heal} HP with the {self.name}!")

        if self.mana > 0:
            user.mp += self.mana
            print(f"{user.name} restored {self.mana} MP with the {self.name}!")

        units.fix_stats()

        if not is_battle:
            main.s_input("\nPress enter/return ")

        inv_system.remove_item(self.item_id)


class StatusPotion(Item):
    def __init__(self, name, desc, buy, sell, status, item_id, cat='consumables', imp=False, ascart='Potion'):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)
        self.status = status

    def use_item(self, user, is_battle=False):
        print('-'*save_load.divider_size)

        if user.status_ail == self.status:
            sounds.buff_spell.play()
            user.status_ail = 'none'

            print(f'{user.name} consumes the {self.name}...')
            main.smart_sleep(0.75)
            sounds.magic_healing.play()

            print(f"{user.name} is no longer {self.status}!")

            if not is_battle:
                main.s_input("\nPress enter/return ")

            inv_system.remove_item(self.item_id)

        else:
            print(f"Drinking this {self.name} probably wouldn't do anything.")
            main.s_input("\nPress enter/return ")


class Weapon(Item):
    # Items that increase your damage by a percentage.
    def __init__(self, name, desc, buy, sell, power, type_, class_, ascart, item_id, off_element='none', cat='weapons',
                 imp=False):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)
        self.power = power
        self.type_ = type_
        self.class_ = class_
        self.off_element = off_element
        self.part = 'weapon'

        if self.class_:
            classes = ' and '.join([f"{x.title()}s" for x in self.class_])
            self.class_req = f"| For {classes}s only"

        else:
            self.class_req = "| For any class"

        self.desc = f"{desc} {self.class_req}"

    def use_item(self, user):
        if user.class_ in self.class_ or not self.class_:
            inv_system.equip_item(self.item_id, user)

            print('-'*save_load.divider_size)
            print(f'{user.name} equips the {self.name}.')
            main.s_input("\nPress enter/return ")

        else:
            print('-'*save_load.divider_size)
            print(f"This {self.name} is f{self.class_req[3:]}.")

            main.s_input("\nPress enter/return ")


class Armor(Item):
    # Items that give the player a percent increase in defense when hit.
    def __init__(self, name, desc, buy, sell, defense, part, class_, ascart, item_id, cat='armor', imp=False):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)
        self.defense = defense
        self.part = part
        self.class_ = class_

        if self.class_:
            classes = ' and '.join([f"{x.title()}s" for x in self.class_])
            self.class_req = f"| For {classes}s only"

        else:
            self.class_req = "| For any class"

        self.desc = f"{desc} {self.class_req}"

    def use_item(self, user):
        if user.class_ in self.class_ or not self.class_:
            inv_system.equip_item(self.item_id, user)

            print('-'*save_load.divider_size)
            print(f'{user.name} equips the {self.name}.')
            main.s_input("\nPress enter/return ")

        else:
            print('-'*save_load.divider_size)
            print(f"This {self.name} is f{self.class_req[3:]}.")

            main.s_input("\nPress enter/return ")


# -- ACCESSORIES -- #
class Accessory(Item):
    def __init__(self, name, desc, buy, sell, item_id, ascart='a', cat='access', imp=False):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)


class ElementAccessory(Accessory):
    # Gives the player an element used when taking damage
    def __init__(self, name, desc, buy, sell, def_element, item_id, ascart='Amulet', acc_type='elemental',
                 cat='access', imp=False):
        Accessory.__init__(self, name, desc, buy, sell, item_id, ascart, cat, imp)
        self.def_element = def_element
        self.acc_type = acc_type

    def __str__(self):
        return self.name

    def use_item(self, user):
        inv_system.equip_item(self.item_id, user)
        user.def_element = self.def_element

        print('-'*save_load.divider_size)
        print(f'{user.name} equips the {self.name}. Their element is now set to {self.def_element}.')
        main.s_input("\nPress enter/return ")


# -- TOOLS -- #
class MagicCompass(Item):
    def __init__(self, name, desc, buy, sell, item_id, cat='tools', imp=True, ascart='Compass'):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)

    def use_item(self):
        pass


class DiviningRod(Item):
    def __init__(self, name, desc, buy, sell, item_id, cat='tools', imp=True, ascart='Div Rod'):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)

    def use_item(self):
        pass


class Shovel(Item):
    def __init__(self, name, desc, buy, sell, item_id, cat='tools', imp=True, ascart='Shovel'):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)

    def use_item(self):
        pass


class TownTeleporter(Item):
    def __init__(self, name, desc, buy, sell, item_id, cat='tools', imp=False, ascart='Map'):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)

    def use_item(self):
        pass


class LockpickKit(Item):
    def __init__(self, name, desc, buy, sell, power, item_id, cat='tools', imp=False, ascart='Lockpick'):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)
        self.power = power

    @staticmethod
    def use_item():
        print('-'*save_load.divider_size)
        print("Your party could certainly make a quick buck lockpicking chests with this thing.")
        print("But that's illegal - you wouldn't break the law, would you?")
        main.s_input("\nPress enter/return ")


# -- OTHERS -- #
class Valuable(Item):
    def __init__(self, name, desc, buy, sell, item_id, ascart='Gem', acquired=False, cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)
        self.acquired = acquired

    # noinspection PyMethodMayBeStatic
    def use_item(self):
        print('-'*save_load.divider_size)
        print(f'Your party admires the {self.name}. It looks very valuable.')
        main.s_input("\nPress enter/return ")


class Misc(Item):
    def __init__(self, name, desc, buy, sell, item_id, ascart='Misc', cat='misc', imp=False):
        Item.__init__(self, name, desc, buy, sell, item_id, imp, ascart, cat)

    def use_item(self):
        print('-'*save_load.divider_size)
        print(self.desc)
        main.s_input("\nPress enter/return ")
