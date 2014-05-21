import sys
import copy

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]


class Companion:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level


class Healer(Companion):
    def __init__(self, name, power, mana, req_mana, mana_per_turn, level=1):
        Companion.__init__(self, name, level)
        self.power = power
        self.mana = mana
        self.rm = req_mana
        self.mpt = mana_per_turn
        self.max_m = copy.copy(mana)

    def use_ability(self):
        if self.mana >= self.rm:
            heal = (self.level + self.power)*2
            main.player.hp += heal
            self.mana -= self.rm
            print("Your pet {0} is using its ability to heal you! (+{1} HP)".format(self.name, heal))
        else:
            print("Your pet {0} is out of mana, and is forced to rest! (+{1} Pet MP)".format(self.name, self.mpt))
            self.mana += self.mpt
            if self.mana >= self.max_m:
                self.max_m -= (self.mana - self.max_m)

# --Healing Pets--
pet_cherub = Healer("Cherub", 3, 10, 5, 2)

all_pets = [pet_cherub]