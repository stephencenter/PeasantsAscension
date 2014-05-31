import random
import sys
import inv_system
import items
import battle
import pygame
import sounds
import time

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

player = ''
monster = ''
static = ''
position = ''
inventory = ''


class Monster:
    # All monsters use this class. Bosses use a sub-class called
    # "Boss" (located in bosses.py) which inherits from this.
    def __init__(self, name, hp, mp, attk, dfns, m_attk,
                 m_dfns, spd, evad, lvl, element='none'):
        self.name = name  # Name
        self.hp = hp  # Health
        self.mp = mp  # Mana
        self.attk = attk  # Attack
        self.dfns = dfns  # Defense
        self.m_attk = m_attk  # Magic Attack
        self.m_dfns = m_dfns  # Magic Defense
        self.spd = spd  # Speed
        self.evad = evad  # Evasion
        self.lvl = lvl  # Level
        self.element = element  # Element
        self.items = ''
        num = random.randint(0, 5)
        if num == 4:
            self.items = random.choice(items.monster_drop(self.lvl, self.element))

    def monst_damage(self, var):
        monst_dealt = int((self.attk/2) - (battle.temp_stats['dfns']/3) + (self.lvl/3) + var + 1)
        if monst_dealt < 1:
            monst_dealt = 1
        return monst_dealt

    def monst_magic(self, var):
        monst_dealt = int((self.m_attk/2)
                          - (battle.temp_stats['m_dfns']/3)
                          + (self.lvl/3) + var + 1)
        if monst_dealt < 1:
            monst_dealt = 1
        return monst_dealt

    def monst_level(self):
        global static
        self.lvl = int((1/3)*abs(1.4*position['avg'] - 1)) + 1
        for x in range(1, self.lvl):
            self.hp += random.randint(4, 6)
            self.mp += random.randint(1, 2)
            self.attk = random.randint(1, 3)
            self.dfns += random.randint(1, 2)
            self.m_attk += random.randint(1, 3)
            self.m_dfns += random.randint(1, 2)
            self.spd += random.randint(1, 2)
            self.evad += random.randint(0, 2)
        static['hp_m'] = self.hp
        static['mp_m'] = self.mp

    def monst_attk(self, var, dodge):
        sounds.sword_slash.play()
        print('The {0} angrily begins to charge at you!'.format(self.name))
        time.sleep(0.75)
        if dodge in range(player.evad, 250):
            dealt = self.monst_damage(var)
            player.hp -= dealt
            sounds.enemy_hit.play()
            print('The {0} hits you, dealing {1} damage!'.format(self.name, dealt))
        else:
            print("You narrowly avoid the {0}'s attack!".format(self.name))

    def monst_name(self):
        monster_type = {'Beach': ['Minor Kraken', 'Mutant Crab', 'Land Shark'],
                        'Swamp': ['Moss Ogre', 'Bog Slime', 'Sludge Rat'],
                        'Forest': ['Imp', 'Sprite', 'Goblin'],
                        'Desert': ['Sand Golem', 'Mummy', 'Fire Ant'],
                        'Tundra': ['Frost Bat', 'Arctic Wolf', 'Minor Yeti'],
                        'Mountain': ['Rock Giant', 'Giant Worm', 'Troll'],
                        'Graveyard': ['Ghoul', 'Zombie', 'Skeleton']
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
        if modifier == 'Slow':  # Very-low speed, below-average speed
            self.spd -= 3
            self.evad -= 1
        if modifier == 'Fast':  # Very-high speed, above-average speed
            self.spd += 3
            self.evad += 1
        if modifier == 'Powerful':  # High attack stats
            self.attk += 2
            self.m_attk += 2
        if modifier == 'Weak':  # Low attack stats
            self.attk -= 2
            self.m_attk -= 2
        if modifier == 'Nimble':  # Very-high evasion, above-average speed
            self.evad += 3
            self.spd += 1
        if modifier == 'Clumsy':  # Very-low evasion, below-average speed
            self.evad -= 3
            self.spd -= 1
        if modifier == 'Armored':  # High defense stats
            self.dfns += 2
            self.m_dfns += 2
        if modifier == 'Broken':  # Low defense stats
            self.dfns -= 2
            self.m_dfns -= 2
        if modifier == 'Mystic':  # High magic stats
            self.m_attk += 2
            self.m_dfns += 2
            self.mp += 3
        if modifier == 'Foolish':  # Low magic stats
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
        elif position['reg'] == 'Graveyard':
            self.element = 'death'
        else:
            self.element = 'none'
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
