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
import json

import npcs
import monsters
import battle
import items


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
        self.max_stats()
        self.hp = copy.copy(static['hp_m'])
        self.mp = copy.copy(static['mp_m'])

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
                if y_n.startswith('y'):
                    monsters.monster = boss
                    monsters.setup_vars()
                    battle.setup_vars()
                    boss.max_stats()
                    print('-'*25)
                    battle.battle_system(is_boss=True)
                    return True
                elif y_n.startswith('n'):
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
master_slime = Boss('Master Slime', 45, 4, 8, 3, 5, 0, 3, 3, 5, 1, 0, [], 35, 35, active=False)


def mastslim_ud():
    # Stands for "Master Slime -- Upon Defeating"
    npcs.alfred_quest_1.finished = True
    npcs.alfred_phrase_2.active = False


master_slime.upon_defeating = mastslim_ud

# Boss: Whispering Goblin -- Position: 4'N, -2'W  (This is for you, Jacob!)
whisp_goblin = Boss('Whispering Goblin', 35, 10, 3, 6, 2, 5, 2, 2, 4, -2, 4, [], 25, 25)

# Boss: Menacing Phantom -- Position: 8'N, -12'W
menac_phantom = Boss('Menacing Phantom', 60, 25, 2, 4, 12, 8, 5, 6, 9, -12,  8, [
    items.spect_wand], 75, 75, active=False, element='death')


def menacphan_ud():
    # Stands for "Menacing Phantom -- Upon Defeating"
    npcs.stewson_quest_1.finished = True
    npcs.stewson_phrase_2.active = False


menac_phantom.upon_defeating = menacphan_ud

# Boss: Terrible Tarrantuloid -- Position: -23'S, -11'W  (Adventure in Pixels)
terr_tarrant = Boss('Terrible Tarrantuloid', 100, 20, 15, 15, 5, 5, 18, 6, 11, -11, -23, [],
                    100, 100)


def terrtarr_ud():
    npcs.krystal_phrase_2.active = False
    npcs.krystal_phrase_3.active = True
    npcs.kyle_phrase_2.active = False
    npcs.kyle_phrase_3.active = True
    npcs.alden_phrase_1.active = False
    npcs.alden_phrase_2.active = True


terr_tarrant.upon_defeating = terrtarr_ud

# Boss: Cursed Spectre -- Position 22'N, 3'E
cursed_spect = Boss('Cursed Spectre', 85, 30, 10, 10, 20, 20, 14, 10, 12, 3, 22, [], 100, 100,
                    element='death')


def cursspect_ud():
    npcs.polmor_phrase_3.active = False
    npcs.polmor_quest_1.finished = True


cursed_spect.upon_defeating = cursspect_ud

# Boss: Ent -- Position: 27'N, 15'E
giant_ent = Boss('Giant Ent', 125, 35, 17, 12, 20, 20, 12, 3, 13, 15, 27, [items.enc_yw],
                 120, 120, active=True, element='grass')

boss_list = [whisp_goblin, master_slime, menac_phantom, terr_tarrant, cursed_spect, giant_ent]

defeated_bosses = []  # Make sure you can only defeat the boss one time
