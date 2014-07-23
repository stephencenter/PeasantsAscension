import sys
import copy
import math
import random
import time

import battle
import sounds

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]


class Companion:
    # A basic pet class
    def __init__(self, name, level=1):
        self.name = name
        self.level = level


class Healer(Companion):
    # Healers have mana, and heal the player each turn if they have enough mana.
    def __init__(self, name, power, mana, req_mana, mana_per_turn, level=1):
        Companion.__init__(self, name, level)
        self.power = power
        self.mana = mana
        self.rm = req_mana
        self.mpt = mana_per_turn
        self.max_m = copy.copy(mana)

    def use_ability(self):
        # Heal!
        if self.mana >= self.rm:  # If the pet has enough mana...
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

    def __init__(self, name, damage, level=1, incap_turns=2, incap_chance=25, rt=0):
        Companion.__init__(self, name, level)
        self.damage = damage  # How much damage it deals per turn
        self.incap_turns = incap_turns  # How long the pet is incapacitated for
        self.incap_chance = incap_chance  # Chance of pet incapacitating itself
        self.rt = rt  # Amount of turns remaining until not-incapacitated

    def use_ability(self):
        # Attack!
        if not self.rt:
            monster = battle.monster
            sounds.sword_slash.play()
            print('Your pet {0} begins to attack...'.format(self.name))
            success = random.randint(1, 100)
            time.sleep(0.75)
            sounds.enemy_hit.play()
            if success not in range(1, self.incap_chance + 1):
                damage = int(self.damage + self.level*1.5)
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
pet_cherub = Healer("Cherub", 2, 10, 5, 2)

# --Fighting Pets--
pet_wolf = Fighter("Wolf", 2)

all_pets = [pet_cherub, pet_wolf]