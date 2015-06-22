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
import math
import random
import time
import re
import msvcrt

import battle
import sounds
import ascii_art

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


class Companion:
    # A basic pet class
    def __init__(self, name, desc, cost, sell, cat='pets', level=1, imp=False):
        self.name = name
        self.cost = cost
        self.sell = sell
        self.desc = desc
        self.cat = cat
        self.level = level
        self.imp = imp

    def __str__(self):
        return self.name


class Healer(Companion):
    # Healers have mana, and heal the player each turn if they have enough mana.
    def __init__(self, name, desc, cost, sell, power, mana,
                 req_mana, mana_per_turn, cat='pets', level=1, imp=False, pet_type='healer'):
        Companion.__init__(self, name, desc, cost, sell, cat, level, imp)
        self.power = power
        self.mana = mana
        self.rm = req_mana
        self.mpt = mana_per_turn
        self.max_m = copy.copy(mana)
        self.pet_type = pet_type

    def __str__(self):
        return self.name

    def use_ability(self):
        # Heal!
        if self.mana >= self.rm and main.player.hp == main.misc_vars['hp_p']:
            print('Your pet {0} senses that you are healthy and waits patiently.'.format(self.name))

        elif self.mana >= self.rm:  # If the pet has enough mana...
            heal = int(math.ceil((self.level + self.power)*1.5))  # ...heal the player
            main.player.hp += heal
            self.mana -= self.rm

            print("Your pet {0} is using its ability to heal you! (+{1} HP)".format(
                self.name, heal))

            sounds.magic_healing.play()

        else:  # The pet rests and restores mana if it doesn't have enough mana
            print("Your pet {0} is out of mana, and is forced to rest! (+{1} Pet MP)".format(
                self.name, self.mpt))
            self.mana += self.mpt

            if self.mana >= self.max_m:
                self.max_m -= (self.mana - self.max_m)


class Fighter(Companion):
    # Fighters deal damage to the enemy but can sometimes mess up.

    def __init__(self, name, desc, cost, sell, damage, cat='pets',
                 level=1, incap_turns=2, incap_chance=25, rt=0, imp=False, pet_type='fighter'):
        Companion.__init__(self, name, desc, cost, sell, cat, level, imp)
        self.damage = damage  # How much damage it deals per turn
        self.incap_turns = incap_turns  # How long the pet is incapacitated for
        self.incap_chance = incap_chance  # Chance of pet incapacitating itself
        self.rt = rt  # Amount of turns remaining until not-incapacitated
        self.pet_type = pet_type

    def __str__(self):
        return self.name

    def use_ability(self):
        # Attack!
        if not self.rt:
            monster = battle.monster
            sounds.sword_slash.play()
            print('Your pet {0} begins to attack...'.format(self.name))
            success = random.randint(1, 100)
            time.sleep(0.75)

            while msvcrt.kbhit():
                msvcrt.getwch()

            sounds.enemy_hit.play()

            if success not in range(1, self.incap_chance + 1):
                damage = math.ceil(self.damage*2 - monster.dfns/2)

                if damage < 1:
                    damage = 1

                monster.hp -= damage
                print('The attack succeeded and dealt {0} damage to the {1}'.format(
                    damage, monster.name))

            else:
                print('Your pet {0} accidentally hit itself instead!'.format(self.name))
                self.rt += self.incap_turns

        else:
            print('Your pet {0} is incapacitated, and is forced to rest!'.format(self.name))
            self.rt -= 1


# --Healing Pets--
pet_cherub = Healer("Cherub",
                    "A sweet angel skilled in the way of weak-healing (T1)", 150, 35, 2, 10, 5, 3)
pet_sapling = Healer("Cherry Sapling",
                     "A small cherry tree that emits a soothing aroma with strange properties (T2)",
                     350, 75, 5, 15, 5, 4)
pet_dove = Healer("White Dove",
                  "A lovely dove that has powerful healing abilities (T3)",
                  750, 275, 10, 25, 4, 7)
pet_doe = Healer("Holy Doe",
                 "A beautiful deer that is enchanted with powerful healing magic (T4)",
                 2000, 750, 20, 40, 3, 6)

# --Fighting Pets--
pet_fox = Fighter("Fox",
                  "A fearsome but tame canine capable of low-level fighting power (T1)",
                  200, 50, 2)
pet_viper = Fighter("Viper",
                    "Despite not being that big, this viper does pack quite a punch (T2)",
                    400, 100, 5, incap_chance=30)
pet_wolf = Fighter("Wolf",
                   "A decently strong beast that will help you fight in battle (T3)",
                   750, 275, 12, incap_turns=3, incap_chance=15)
pet_dragon = Fighter("Dragon",
                     "A massive and powerful dragon that uses his flames to attack (T4)",
                     2000, 750, 25, incap_turns=4)
pet_ost = Fighter("Ostrich",
                  "A large and ferocious avian that kicks its prey with the force of an ox (T5)",
                  9001, 3500, 50, incap_turns=1, incap_chance=45)