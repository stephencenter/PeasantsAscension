import sys
import copy
import math
import random
import time
import json
import re

import battle
import sounds

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

# A regular expression that replaces all non-NSEW characters with ''
only_nsew = lambda x: re.compile(r'[^n^s^e^w]').sub('', x)


class Companion:
    # A basic pet class
    def __init__(self, name, desc, cost, equip=False, level=1):
        self.name = name
        self.cost = cost
        self.desc = desc
        self.equip = equip
        self.level = level

    def __str__(self):
        return self.name


class Healer(Companion):
    # Healers have mana, and heal the player each turn if they have enough mana.
    def __init__(self, name, desc, cost, power, mana,
                 req_mana, mana_per_turn, equip=False, level=1):
        Companion.__init__(self, name, desc, cost, equip, level)
        self.power = power
        self.mana = mana
        self.rm = req_mana
        self.mpt = mana_per_turn
        self.max_m = copy.copy(mana)

    def __str__(self):
        return self.name

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

    def __init__(self, name, desc, cost, damage,
                 equip=False, level=1, incap_turns=2, incap_chance=25, rt=0):
        Companion.__init__(self, name, desc, cost, equip, level)
        self.damage = damage  # How much damage it deals per turn
        self.incap_turns = incap_turns  # How long the pet is incapacitated for
        self.incap_chance = incap_chance  # Chance of pet incapacitating itself
        self.rt = rt  # Amount of turns remaining until not-incapacitated

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


class Steed(Companion):
    def __init__(self, name, desc, cost, distance, equip=False, level=1):
        Companion.__init__(self, name, desc, cost, equip, level)
        self.distance = distance

    @staticmethod
    def out_of_bounds():
        print('-'*25)
        print('You see an ocean in front of you and decide to stop.')
        print('-'*25)

    def use_ability(self, direction):
        direction = only_nsew(direction)

        if len(direction) > self.distance:
            spam = self.distance
        else:
            spam = len(direction)

        for x in direction[:spam]:
            if x == 'n':
                if main.position['y'] < 125:
                    main.position['y'] += 1
                else:
                    Steed.out_of_bounds()
                    return

            elif x == 's':
                if main.position['y'] > -125:
                    main.position['y'] -= 1
                else:
                    Steed.out_of_bounds()
                    return

            elif x == 'w':
                if main.position['x'] > -125:
                    main.position['x'] -= 1
                else:
                    Steed.out_of_bounds()
                    return

            elif x == 'e':
                if main.position['x'] < 125:
                    main.position['x'] += 1
                else:
                    Steed.out_of_bounds()
                    return

        if len(direction) > self.distance:
            print("Your {0} got tired, so you had to stop part-way.".format(self.name))
            return

# --Healing Pets--
pet_cherub = Healer("Cherub",
                    "A sweet angel skilled in the way of weak-healing.", 150, 2, 10, 5, 2)
pet_sapling = Healer("Cherry Sapling",
                     "A small cherry tree which, due to a magical spell, is skilled as a healer.",
                     350, 5, 15, 6, 2)

# --Fighting Pets--
pet_wolf = Fighter("Wolf",
                   "A fearsome but tame canine capable of low-level fighting power.", 200, 2)
pet_viper = Fighter("Viper",
                    "Despite not being that big, this viper does pack quite a punch.",
                    400, 5, incap_chance=30)

# --Steed Pets--
pet_horse = Steed("Horse",
                  """A trusty horse. This horse allows you to enter up to 3 directions
at a time instead of 1.""", 350, 3)

all_pets = [pet_cherub, pet_sapling, pet_wolf, pet_viper, pet_horse]


def serialize_pets(path):
    j_all_pets = {}

    for pet in all_pets:
        j_all_pets[pet.name] = pet.__dict__

    with open(path, mode="w",  encoding='utf-8') as f:
        json.dump(j_all_pets, f, indent=4, separators=(', ', ': '))


def deserialize_pets(path):
    global all_pets

    with open(path, encoding='utf-8') as f:
        j_all_pets = json.load(f)

    for pet in all_pets:
        for key in j_all_pets:
            if pet.name == key:
                pet.__dict__ = j_all_pets[key]
