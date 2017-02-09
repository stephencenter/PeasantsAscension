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

from UnitClass import *

player = ''
monster = ''

# Pronounced "So-low"
solou = PlayableCharacter('Solou', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='mage', enabled=False)

# Pronounced "Zo-ann"
xoann = PlayableCharacter('Xoann', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='assassin', enabled=False)

# Pronounced "Adore-een"
adorine = PlayableCharacter('Adorine', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='warrior', enabled=False)

# Pronounced "Rahn-ahf"
ran_af = PlayableCharacter("Ran'Af", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='monk', enabled=False)

# Pronounced "Parse-toe"
parsto = PlayableCharacter("Parsto", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='ranger', enabled=False)

# Rhymes with "Chime"
chyme = PlayableCharacter("Chyme", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='paladin', enabled=False)


def create_player():
    global player

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)

    # Set the player's max HP and MP
    player.max_hp = copy.copy(player.hp)
    player.max_mp = copy.copy(player.mp)

    player.name = player.choose_name()
    player.class_ = player.choose_class()
    main.set_adventure_name()

    if player.class_ == "warrior":
        player.max_hp += 5
        player.max_mp -= 1
        player.dfns += 3
        player.p_dfns += 2
        player.attk += 3
        player.spd -= 1
        player.evad -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.wdn_sht)

    elif player.class_ == "mage":
        player.max_hp += 1
        player.max_mp += 6
        player.m_attk += 4
        player.m_dfns += 3
        inv_system.equipped['player']['weapon'] = copy.copy(items.mag_twg)

    elif player.class_ == "assassin":
        player.max_hp += 2
        player.max_mp += 1
        player.attk += 3
        player.dfns += 2
        player.spd += 4
        player.evad += 2
        inv_system.equipped['player']['weapon'] = copy.copy(items.stn_dag)

    elif player.class_ == "ranger":
        player.max_mp += 2
        player.p_attk += 4
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        inv_system.equipped['player']['weapon'] = copy.copy(items.slg_sht)

    elif player.class_ == "monk":
        player.max_hp += 2
        player.max_mp += 2
        player.attk += 3
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        player.dfns -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.fists)

    elif player.class_ == "paladin":
        player.max_hp += 3
        player.max_mp += 4
        player.m_dfns += 3
        player.m_attk += 3
        player.dfns += 3
        player.p_dfns += 3
        player.attk += 3
        player.spd -= 1
        player.evad -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.rbr_mlt)

    player.hp = copy.copy(player.max_hp)
    player.mp = copy.copy(player.max_mp)
    print('-'*25)


def spawn_monster():
    global monster

    monster = Monster('', 10, 5, 3, 2, 3, 2, 3, 2, 3, 2)
    monster.monst_name()
    monster.monst_level()


def fix_stats():
    # Makes sure that that no-one ever has 1) stats that are above their maximum, 2) stats that are negative,
    # and 3) stats that are not integers.

    global player
    global solou
    global xoann
    global chyme
    global parsto
    global ran_af
    global adorine
    global monster

    if player.hp < 0:
        player.hp = 0
    if solou.hp < 0:
        solou.hp = 0
    if xoann.hp < 0:
        xoann.hp = 0
    if chyme.hp < 0:
        chyme.hp = 0
    if parsto.hp < 0:
        parsto.hp = 0
    if ran_af.hp < 0:
        ran_af.hp = 0
    if adorine.hp < 0:
        adorine.hp = 0

    if player.mp < 0:
        player.mp = 0
    if solou.mp < 0:
        solou.mp = 0
    if xoann.mp < 0:
        xoann.mp = 0
    if chyme.mp < 0:
        chyme.mp = 0
    if parsto.mp < 0:
        parsto.mp = 0
    if ran_af.mp < 0:
        ran_af.mp = 0
    if adorine.mp < 0:
        adorine.mp = 0

    if player.hp > player.max_hp:
        player.hp -= (player.hp - player.max_hp)
    if solou.hp > solou.max_hp:
        solou.hp -= (solou.hp - solou.max_hp)
    if xoann.hp > xoann.max_hp:
        xoann.hp -= (xoann.hp - xoann.max_hp)
    if chyme.hp > chyme.max_hp:
        chyme.hp -= (chyme.hp - chyme.max_hp)
    if parsto.hp > parsto.max_hp:
        parsto.hp -= (parsto.hp - parsto.max_hp)
    if ran_af.hp > ran_af.max_hp:
        ran_af.hp -= (ran_af.hp - ran_af.max_hp)
    if adorine.hp > adorine.max_hp:
        adorine.hp -= (adorine.hp - adorine.max_hp)

    if player.mp > player.max_mp:
        player.mp -= (player.mp - player.max_mp)
    if solou.mp > solou.max_mp:
        solou.mp -= (solou.mp - solou.max_mp)
    if xoann.mp > xoann.max_mp:
        xoann.mp -= (xoann.mp - xoann.max_mp)
    if chyme.mp > chyme.max_mp:
        chyme.mp -= (chyme.mp - chyme.max_mp)
    if parsto.mp > parsto.max_mp:
        parsto.mp -= (parsto.mp - parsto.max_mp)
    if ran_af.mp > ran_af.max_mp:
        ran_af.mp -= (ran_af.mp - ran_af.max_mp)
    if adorine.mp > adorine.max_mp:
        adorine.mp -= (adorine.mp - adorine.max_mp)

    player.hp = math.ceil(player.hp)
    player.mp = math.ceil(player.mp)
    parsto.hp = math.ceil(parsto.hp)
    parsto.mp = math.ceil(parsto.mp)
    adorine.hp = math.ceil(adorine.hp)
    adorine.mp = math.ceil(adorine.mp)
    ran_af.hp = math.ceil(ran_af.hp)
    ran_af.mp = math.ceil(ran_af.mp)
    xoann.hp = math.ceil(xoann.hp)
    xoann.mp = math.ceil(xoann.mp)
    solou.hp = math.ceil(solou.hp)
    solou.mp = math.ceil(solou.mp)
    chyme.hp = math.ceil(chyme.hp)
    chyme.mp = math.ceil(chyme.mp)

    if adorine.evad > 256:
        adorine.evad = 256
    if ran_af.evad > 256:
        ran_af.evad = 256
    if solou.evad > 256:
        solou.evad = 256
    if xoann.evad > 256:
        xoann.evad = 256
    if chyme.evad > 256:
        chyme.evad = 256
    if parsto.evad > 256:
        parsto.evad = 256

    if player.hp > 0 and player.status_ail == 'dead':
        player.status_ail = 'none'
    if solou.hp > 0 and solou.status_ail == 'dead':
        solou.status_ail = 'none'
    if xoann.hp > 0 and xoann.status_ail == 'dead':
        xoann.status_ail = 'none'
    if chyme.hp > 0 and chyme.status_ail == 'dead':
        chyme.status_ail = 'none'
    if parsto.hp > 0 and parsto.status_ail == 'dead':
        parsto.status_ail = 'none'
    if ran_af.hp > 0 and ran_af.status_ail == 'dead':
        ran_af.status_ail = 'none'
    if adorine.hp > 0 and adorine.status_ail == 'dead':
        adorine.status_ail = 'none'

    try:
        monster.hp = math.ceil(monster.hp)
        monster.mp = math.ceil(monster.mp)

        if monster.hp < 0:
            monster.hp = 0
        if monster.mp < 0:
            monster.mp = 0

        if monster.hp > monster.max_hp:
            monster.hp -= (monster.hp - monster.max_hp)
        if monster.mp > monster.max_mp:
            monster.mp -= (monster.mp - monster.max_mp)

        if monster.evad > 256:
            monster.evad = 256

    except AttributeError:
        if not isinstance(monster, str):
            raise


def serialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Save the "PlayableCharacter" objects as JSON files

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(player.__dict__, f, indent=4, separators=(', ', ': '))
    with open(s_path, mode='w', encoding='utf-8') as f:
        json.dump(solou.__dict__, f, indent=4, separators=(', ', ': '))
    with open(x_path, mode='w', encoding='utf-8') as f:
        json.dump(xoann.__dict__, f, indent=4, separators=(', ', ': '))
    with open(a_path, mode='w', encoding='utf-8') as f:
        json.dump(adorine.__dict__, f, indent=4, separators=(', ', ': '))
    with open(r_path, mode='w', encoding='utf-8') as f:
        json.dump(chyme.__dict__, f, indent=4, separators=(', ', ': '))
    with open(f_path, mode='w', encoding='utf-8') as f:
        json.dump(ran_af.__dict__, f, indent=4, separators=(', ', ': '))
    with open(p_path, mode='w', encoding='utf-8') as f:
        json.dump(parsto.__dict__, f, indent=4, separators=(', ', ': '))


def deserialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Load the JSON files and translate them into "PlayableCharacter" objects
    global player
    global solou
    global xoann
    global adorine
    global chyme
    global ran_af
    global parsto

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    solou = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    xoann = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    adorine = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    chyme = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    ran_af = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    parsto = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)

    with open(path, encoding='utf-8') as f:
        player.__dict__ = json.load(f)
    with open(s_path, encoding='utf-8') as f:
        solou.__dict__ = json.load(f)
    with open(x_path, encoding='utf-8') as f:
        xoann.__dict__ = json.load(f)
    with open(a_path, encoding='utf-8') as f:
        adorine.__dict__ = json.load(f)
    with open(r_path, encoding='utf-8') as f:
        chyme.__dict__ = json.load(f)
    with open(f_path, encoding='utf-8') as f:
        ran_af.__dict__ = json.load(f)
    with open(p_path, encoding='utf-8') as f:
        parsto.__dict__ = json.load(f)
