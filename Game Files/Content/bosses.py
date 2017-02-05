#   This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Peasants' Ascension is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

from BossClass import *

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


def check_bosses():
    for boss in main.party_info['current_tile'].boss_list:
        if boss.name not in defeated_bosses and boss.active:
            print('-'*25)

            sounds.item_pickup.play()

            if boss.new_location(add=False) not in inv_system.inventory['coord']:
                print('You feel the presence of an unknown entity...')

            else:
                print(f'You come across the lair of the {boss.name}.')

            while True:
                if boss.new_location(add=False) not in inv_system.inventory['coord']:
                    y_n = input('Do you wish to investigate? | Yes or No: ')

                else:
                    y_n = input(f'Do you wish to confront the {boss.name}? | Yes or No: ')

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    units.monster = boss
                    boss.max_stats()
                    boss.new_location()
                    print('-'*25)

                    battle.battle_system(is_boss=True)

                    return True

                elif y_n.startswith('n'):
                    return True

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


def unimportant_boss_ud():
    pass


# Boss: Master Slime -- Position: 0'N, 1'E
master_slime = Boss('Master Slime',
                    35, 5,   # 35 HP and 5 MP
                    12, 5,   # 12 Attack, 5 Defense
                    6, 5,    # 6 Pierce Attack, 5 Pierce Defense
                    8, 0,    # 8 Magic Attack, 0 Magic Defense
                    6, 6,    # 6 Speed, 6 Evasion
                    3,       # Level 3
                    1, 0,    # Located at 0'N, 1'W
                    None,    # Drops no items
                    25, 25,  # Drops 25 XP and 25 GP
                    "jiggles ferociously and begins to attack",
                    active=False)

master_slime.battle_turn = master_slime.melee_ai


def mastslim_ud():
    # Stands for "Master Slime -- Upon Defeating"
    npcs.alfred_quest_1.finished = True
    npcs.alfred_phrase_2.active = False


master_slime.upon_defeating = mastslim_ud

# Boss: Goblin Chieftain -- Position: 4'N, -2'W
whisp_goblin = Boss('Goblin Chieftain',
                    50, 10,  # 50 HP and 10 MP
                    20, 20,  # 20 Attack, 20 Defense
                    12, 15,  # 12 Pierce Attack, 15 Pierce Defense
                    8, 12,   # 8 Magic Attack, 12 Magic Defense
                    15, 7,   # 15 Speed, 7 Evasion
                    5,       # Level 5
                    -2, 4,   # Located at 4'N, -2'W
                    None,    # Drops no items
                    45, 45,  # Drops 45 XP and 45 GP
                    "readies his great spear and begins to stab")

whisp_goblin.battle_turn = whisp_goblin.melee_ai
whisp_goblin.upon_defeating = unimportant_boss_ud

# Boss: Menacing Phantom -- Position: 8'N, -12'W
menac_phantom = Boss('Menacing Phantom',
                     75, 50,  # 75 HP and 50 MP
                     10, 20,  # 10 Attack, 20 Defense
                     5, 20,   # 5 Pierce Attack, 20 Pierce Defense
                     35, 25,  # 35 Magic Attack, 25 Magic Defense
                     20, 15,  # 20 Speed, 15 Evasion
                     8,       # Level 8
                     -12, 8,  # Located at 8'N, -12'W
                     None,    # Drops no items
                     75, 75,  # Drops 75 XP and 75 GP
                     "calls upon its ethereal power and casts a hex on",
                     active=False, element='death')


def menacphan_ud():
    # Stands for "Menacing Phantom -- Upon Defeating"
    npcs.stewson_quest_1.finished = True
    npcs.stewson_phrase_2.active = False


menac_phantom.battle_turn = menac_phantom.magic_ai
menac_phantom.upon_defeating = menacphan_ud

# Boss: Terrible Tarantuloid -- Position: -23'S, -11'W  (Adventure in Pixels)
terr_tarant = Boss('Terrible Tarantuloid',
                   100, 25,   # 100 Health, 25 Mana
                   45, 30,    # 45 Attack, 30 Defense
                   25, 15,    # 25 Pierce Attack, 15 Pierce Defense
                   15, 25,    # 15 Magic Attack, 25 Magic Defense
                   35, 25,    # 35 Speed, 25 Evasion
                   12,        # Level 12
                   -11, -23,  # Located at -23'S, -11'W
                   None,      # Drops no items
                   150, 150,  # Drops 150 XP and 150 GP
                   "readies its venomous fangs and bites")


def terrtar_ud():
    npcs.krystal_phrase_2.active = False
    npcs.krystal_phrase_3.active = True
    npcs.kyle_phrase_2.active = False
    npcs.kyle_phrase_3.active = True
    npcs.alden_phrase_1.active = False
    npcs.alden_phrase_2.active = True


terr_tarant.battle_turn = terr_tarant.melee_ai
terr_tarant.upon_defeating = terrtar_ud

# Boss: Cursed Spectre -- Position 22'N, 3'E
cursed_spect = Boss('Cursed Spectre',
                    125, 75,             # 125 Health, 75 Mana
                    15, 30,              # 15 Attack, 30 Defense
                    20, 25,              # 20 Pierce Attack, 25 Pierce Defense
                    50, 35,              # 50 Magic Attack, 35 Magic Defense
                    25, 20,              # 25 Speed, 20 Evasion
                    15,                  # Level 15
                    3, 22,               # Located at 22'N, 3'E
                    i_items.spect_wand,  # Drops a spectre wand
                    250, 250,            # Drops 250 XP and 250 GP
                    "calls upon its ethereal power and casts a hex on",
                    element='death', active=False)


def cursspect_ud():
    npcs.rivesh_phrase_3.active = False
    npcs.rivesh_quest_1.finished = True


cursed_spect.battle_turn = cursed_spect.magic_ai
cursed_spect.upon_defeating = cursspect_ud

# Boss: Ent -- Position: 27'N, 15'E
giant_ent = Boss('Giant Ent',
                 125, 35,         # 125 Health, 75 Mana
                 35, 50,          # 35 Attack, 50 Defense
                 15, 50,          # 15 Pierce Attack, 50 Pierce Defense
                 20, 15,          # 20 Magic Attack, 15 Magic Defense
                 15, 5,           # 15 Speed, 5 Evasion
                 15,              # Level 15
                 15, 27,          # Located at 27'N, 15'E
                 i_items.enc_yw,  # Drops an enchanted yew wand
                 250, 250,        # Drops 250 XP and 250 GP
                 "calls upon the essence of the forest and attacks",
                 element='grass', active=True)

giant_ent.battle_turn = giant_ent.melee_ai
giant_ent.upon_defeating = unimportant_boss_ud

boss_list = [whisp_goblin, master_slime, menac_phantom, terr_tarant, cursed_spect, giant_ent]

defeated_bosses = []  # Make sure you can only defeat the boss one time
