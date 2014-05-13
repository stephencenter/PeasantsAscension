import math
import random
import sys
import inv_system
import items
import battle

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

player = ''
monster = ''
static = ''
position = ''
inventory = ''


class Monster:  # All monsters use this class. Bosses use a sub-class called
                # "Boss" (located in bosses.py) which inherits from this.
    def __init__(self, name, hp, mp, attk, dfns, m_attk,
                 m_dfns, spd, evad, lvl, element='none'):
        self.name = name        # Name
        self.hp = hp            # Health
        self.mp = mp            # Mana
        self.attk = attk        # Attack
        self.dfns = dfns        # Defense
        self.m_attk = m_attk    # Magic Attack
        self.m_dfns = m_dfns    # Magic Defense
        self.spd = spd          # Speed
        self.evad = evad        # Evasion
        self.lvl = lvl          # Level
        self.element = element  # Element
        self.items = ''
        num = random.randint(0, 4)
        if num == 4:
            self.items = random.choice(items.monster_drop(self.lvl, self.element))

    def monst_damage(self, var):
        monst_dealt = int((self.attk/2) - (player.dfns/3) + (self.lvl/3) + var + 1)
        if monst_dealt < 1:
            monst_dealt = 1
        return monst_dealt

    def monst_magic(self, var):
        monst_dealt = int((self.m_attk/2) - (player.m_dfns/3) + (self.lvl/3) + var + 1)
        if monst_dealt < 1:
            monst_dealt = 1
        return monst_dealt

    def monst_level(self):
        global static
        self.lvl = int(1/2*abs(1.5*position['avg'] - 1)) + 1
        for x in range(1, self.lvl):
            self.hp += random.randint(4, 6)
            self.mp += random.randint(1, 2)
            self.attk = random.randint(1, 2)
            self.dfns += random.randint(0, 2)
            self.m_attk += random.randint(1, 2)
            self.m_dfns += random.randint(0, 2)
            self.spd += random.randint(1, 2)
            self.evad += random.randint(0, 2)
        static['hp_m'] = self.hp
        static['mp_m'] = self.mp

    def monst_attk(self, var, dodge):
        print('The {0} angrily begins to charge at you!'.format(self.name))
        if dodge in range(player.evad, 250):
            dealt = self.monst_damage(var)
            player.hp -= dealt
            print('The {0} hits you, dealing {1} damage!'.format(self.name, dealt))
        else:
            print("You narrowly avoid the {0}'s attack!".format(self.name))

    def monst_name(self):
        monster_type = {
                       'Beach': ['Minor Kraken', 'Mutant Crab', 'Land Shark'],
                       'Swamp': ['Moss Ogre', 'Bog Slime', 'Sludge Rat'],
                       'Forest': ['Imp', 'Skeleton', 'Goblin'],
                       'Desert': ['Sand Golem', 'Desert Python', 'Fire Ant'],
                       'Tundra': ['Frost Bat', 'Arctic Wolf', 'Minor Yeti'],
                       'Mountain': ['Rock Giant', 'Giant Worm', 'Troll']
                       }
        self.name = random.choice(monster_type[position['reg']])
        modifiers = [
                    'Slow', 'Fast',
                    'Powerful', 'Weak',
                    'Nimble', 'Clumsy',
                    'Armored', 'Broken',
                    'Mystic', 'Foolish'
                    ]
        modifier = random.choice(modifiers)
        if modifier == 'Slow':
            self.spd -= 3
            self.evad -= 1
        if modifier == 'Fast':
            self.spd += 3
            self.evad += 1
        if modifier == 'Powerful':
            self.attk += 2
            self.m_attk += 2
        if modifier == 'Weak':
            self.attk -= 2
            self.m_attk -= 2
        if modifier == 'Nimble':
            self.evad += 3
            self.spd += 1
        if modifier == 'Clumsy':
            self.evad -= 3
            self.spd -= 1
        if modifier == 'Armored':
            self.dfns += 2
            self.m_dfns += 2
        if modifier == 'Broken':
            self.dfns -= 2
            self.m_dfns -= 2
        if modifier == 'Mystic':
            self.m_attk += 2
            self.m_dfns += 2
            self.mp += 3
        if modifier == 'Foolish':
            self.m_attk -= 2
            self.m_dfns -= 2

        if position['reg'] == 'Tundra':
            self.element = 'ice'
        elif position['reg'] == 'Desert':
            self.element = 'fire'
        elif position['reg'] == 'Mountain':
            self.element = 'earth'
        elif position['reg'] == 'Beach':
            self.element = 'electric'
        elif position['reg'] == 'Forest':
            self.element = 'grass'
        elif position['reg'] == 'Swamp':
            self.element = 'water'
        self.name = ' '.join([modifier, self.name])


def spawn_monster():
    global monster
    setup_vars()
    monster = Monster('', random.randint(6, 8), random.randint(3, 4), 2, 1, 2, 1, 2, 1, 1)
    monster.monst_level()
    monster.monst_name()


def setup_vars():
    global player
    global static
    global position
    global inventory
    player = main.player
    static = main.static
    position = main.position
    inventory = inv_system.inventory
