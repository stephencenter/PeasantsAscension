import monsters
import battle
import sys
import copy

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

position = ''


class Boss(monsters.Monster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, spd, evad,
                 lvl, pos_x, pos_y, item, gold, experience, element='none'):
        monsters.Monster.__init__(self, name, hp, mp, attk, dfns, m_attk,
                                  m_dfns, spd, evad, lvl, element)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.item = item
        self.per_hp = copy.copy(self.hp)
        self.per_mp = copy.copy(self.mp)
        self.gold = gold
        self.experience = experience


    def max_stats(self):
        global static
        setup_vars()
        static['hp_m'] = self.per_hp  # Make sure the bosses HP/MP regen
        static['mp_m'] = self.per_mp  # if the player runs away
        self.hp = copy.copy(static['hp_m'])
        self.mp = copy.copy(static['mp_m'])


def check_bosses(x, y):
    for boss in boss_list:
        if boss.pos_x == x and boss.pos_y == y and boss.name not in defeated_bosses:
            print('-'*25)
            print('You feel the presence of an unknown entity...')
            while True:
                y_n = input('Do you wish to investigate? | Yes or No: ')
                try:
                    y_n = y_n.lower()
                except AttributeError:
                    continue
                if y_n in ['yes', 'y']:
                    monsters.monster = boss
                    monsters.setup_vars()
                    battle.setup_vars()
                    boss.max_stats()
                    battle.battle_system(is_boss=True)
                    return True
                elif y_n in ['no', 'n']:
                    return True
                else:
                    continue
    else:
        return False


def setup_vars():
    global static
    static = main.static


master_slime = Boss('Master Slime', 35, 4, 8, 3, 5, 0, 3, 3, 5, 1, 0, [], 50, 50)
whisp_goblin = Boss('Whispering Goblin', 30, 10, 3, 6, 2, 5, 2, 2, 4, -2, 4, [], 40, 30) # This is for you, Jacob!

boss_list = [whisp_goblin, master_slime]
defeated_bosses = []  # Make sure you can only defeat the boss one time
