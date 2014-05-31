import sys
import copy
import math

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]


class Companion:
    # A basic pet class
    def __init__(self, name, level=1):
        self.name = name
        self.level = level


class Healer(Companion):  # A subclass of Companion
    # Healers have mana, and heal the player each turn if they have enough mana.
    def __init__(self, name, power, mana, req_mana, mana_per_turn, level=1):
        Companion.__init__(self, name, level)
        self.power = power
        self.mana = mana
        self.rm = req_mana
        self.mpt = mana_per_turn
        self.max_m = copy.copy(mana)

    def use_ability(self):
        # Heal
        input('\nPress Enter/Return')
        if self.mana >= self.rm:  # If the pet has enough mana...
            heal = int(math.ceil((self.level + self.power)*1.5))  # ...heal the player
            main.player.hp += heal
            self.mana -= self.rm
            print(
                "Your pet {0} is using its ability to heal you! (+{1} HP)".format(self.name, heal))
        else:  # The pet rests and restores mana if it doesn't have enough mana
            print("Your pet {0} is out of mana, and is forced to rest! (+{1} Pet MP)".format(
                self.name, self.mpt))
            self.mana += self.mpt
            if self.mana >= self.max_m:
                self.max_m -= (self.mana - self.max_m)

# --Healing Pets--
pet_cherub = Healer("Cherub", 2, 10, 5, 2)

all_pets = [pet_cherub]