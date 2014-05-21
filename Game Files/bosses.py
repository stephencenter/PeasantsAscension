import monsters
import battle
import npcs
import sys
import copy
import json

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

static = ''


class Boss(monsters.Monster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, spd, evad,
                 lvl, pos_x, pos_y, item, gold, experience,
                 active=True, element='none'):
        monsters.Monster.__init__(self, name, hp, mp, attk, dfns, m_attk,
                                  m_dfns, spd, evad, lvl, element)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.item = item
        self.per_hp = copy.copy(self.hp)
        self.per_mp = copy.copy(self.mp)
        self.gold = gold
        self.experience = experience
        self.active = active

    def max_stats(self):
        global static
        setup_vars()
        static['hp_m'] = self.per_hp  # Make sure the bosses HP/MP regenerate
        static['mp_m'] = self.per_mp  # if the player runs away
        self.hp = copy.copy(static['hp_m'])
        self.mp = copy.copy(static['mp_m'])


def check_bosses(x, y):
    for boss in boss_list:
        if [boss.pos_x, boss.pos_y] == [x, y] and boss.name not in defeated_bosses and boss.active:
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


def serialize_bosses(path):
    json_bosslist = {}
    for boss in boss_list:
        json_bosslist[boss.name] = boss.active
    with open(path, encoding='utf-8', mode='w') as i:
        json.dump(json_bosslist, i)


def deserialize_bosses(path):
    global boss_list
    with open(path, encoding='utf-8') as i:
        json_bosslist = json.load(i)
    for key in json_bosslist:
        for boss in boss_list:
            if key == boss.name:
                boss.active = json_bosslist[key]


def setup_vars():
    global static
    static = main.static


# Boss: Master Slime -- Position: 0'N, 1'E
master_slime = Boss('Master Slime', 35, 4, 8, 3, 5, 0, 3, 3, 5, 1, 0, [], 35, 35, active=False)


def mastslim_ud():
    # Stands for "Master Slime -- Upon Defeating"
    npcs.alfred_quest_1.finished = True
    npcs.alfred_phrase_2.active = False


master_slime.upon_defeating = mastslim_ud

# Boss: Whispering Goblin -- Position: 4'N, -2'W
whisp_goblin = Boss('Whispering Goblin', 30, 10, 3, 6, 2, 5, 2, 2, 4, -2, 4, [], 25, 25)  # This is for you, Jacob!

# Boss: Menacing Phantom -- Position: 8'N, -12'W
menac_phantom = Boss('Menacing Phantom', 50, 25, 2, 4, 12, 8, 5, 6, 10, -12,  8, [], 100, 100)

boss_list = [whisp_goblin, master_slime, menac_phantom]
defeated_bosses = []  # Make sure you can only defeat the boss one time
