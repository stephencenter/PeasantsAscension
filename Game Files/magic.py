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
import json
import random
import time

import pygame

import monsters
import battle
import inv_system
import sounds


if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# This is the message that is printed if you attempt to use magic
# without the required amount of mana.
out_of_mana = """-------------------------
You don't have enough mana to cast that spell!
-------------------------"""


class Spell:
    def __init__(self, name, desc, mana, req_lvl):
        self.name = name
        self.desc = desc
        self.mana = mana
        self.req_lvl = req_lvl

    def use_mana(self):
        main.player.mp -= self.mana
        if main.player.mp < 0:
            main.player.mp = 0


class Healing(Spell):
    # Healing spells are spells that restore your HP during battle
    def __init__(self, name, desc, mana, req_lvl, health):
        Spell.__init__(self, name, desc, mana, req_lvl)
        self.health = health

    def __str__(self):
        return self.name

    def use_magic_healing(self, is_battle):
        if main.player.mp >= self.mana:
            print()
            Spell.use_mana(self)
            main.player.hp += self.health + int(main.misc_vars['int']/4) + random.randint(-2, 2)

            if main.player.hp > main.misc_vars['hp_p']:
                main.player.hp -= (main.player.hp - main.misc_vars['hp_p'])
            sounds.magic_healing.play()

            if is_battle:
                print('-Player Turn-')

            print('Using "{0}", you are healed by {1} HP!'.format(self.name, self.health))
            return True

        else:
            print(out_of_mana)
            return False


class Damaging(Spell):
    # Damaging spells are spells that deal damage to the enemy during battle.
    # Just like normal attacks, they have a chance to miss based on
    # the enemy's evade stat.
    def __init__(self, name, desc, mana, req_lvl, damage, element):
        Spell.__init__(self, name, desc, mana, req_lvl)
        self.damage = damage
        self.element = element

    def __str__(self):
        return self.name

    def use_magic(self, var, dodge):
        if main.player.mp >= self.mana:
            print()
            Spell.use_mana(self)

            # Determine the power of the attack
            attk_pwr = int(self.damage + (battle.temp_stats['m_attk']/3) -
                           (battle.monster.m_dfns/2) + var)

            # Evaluate the element of the attack and the enemy
            attk_pwr = eval_element(
                p_elem=self.element,
                m_elem=monsters.monster.element,
                p_dmg=attk_pwr)[0]

            print('-Player Turn-')
            if inv_system.equipped['weapon'].class_ == 'magic':
                print('You begin to use your {0} to summon a powerful spell...'.format(
                    inv_system.equipped['weapon']))
            else:
                print('You attempt to summon a powerful spell...')

            sounds.magic_attack.play()
            time.sleep(0.75)

            if dodge in range(monsters.monster.evad, 250):
                sounds.enemy_hit.play()
                print('Using the power of "{0}", you deal {1} damage to the {2}!'.format(
                    self.name, attk_pwr, monsters.monster.name))
                monsters.monster.hp -= attk_pwr

            else:
                sounds.attack_miss.play()
                print('The {0} dodges your attack!'.format(monsters.monster.name))

            return True

        else:
            print(out_of_mana)
            return False


class Buff(Spell):
    # Buffs are spells that temporarily raise the player's stats
    # during battle. They last until the battle is over, at which
    # point the player's stats will return to normal.
    def __init__(self, name, desc, mana, req_lvl, incre, stat):
        Spell.__init__(self, name, desc, mana, req_lvl)
        self.incre = incre
        self.stat = stat

    def __str__(self):
        return self.name

    def use_magic(self):
        if main.player.mp >= self.mana:
            print()
            Spell.use_mana(self)
            print('-Player Turn-')
            print('Using the power of {0}, your {1} increases temporarily by {2}!'.format(
                self.name, self.stat, self.incre))

            if self.stat == 'Defense':
                battle.temp_stats['dfns'] += self.incre
            elif self.stat == 'Magic Defense':
                battle.temp_stats['m_dfns'] += self.incre
            elif self.stat == 'Speed':
                battle.temp_stats['spd'] += self.incre
            elif self.stat == 'Evasion':
                battle.temp_stats['evad'] += self.incre
            elif self.stat == 'Attack':
                battle.temp_stats['attk'] += self.incre
            elif self.stat == 'Magic Attack':
                battle.temp_stats['m_attk'] += self.incre

            return True

        else:
            print(out_of_mana)
            return False


# -- Attacks -- #

# Fire
w_flame = Damaging('Weak Flame',
                   "Summon a weak fireball to destroy your foes.",
                   3, 1, 6, "fire")
f_blaze = Damaging('Fierce Blaze',
                   "Summon a powerful flame to destroy your foes.",
                   10, 11, 13, "fire")
g_infer = Damaging('Grand Inferno',
                   "Unleash a monstrous blaze destroy your foes.",
                   18, 23, 23, "fire")

# Electricity
in_spark = Damaging('Inferior Spark',
                    "Summon a weak spark to destroy your foes.",
                    3, 2, 6, "electric")
pwr_jolt = Damaging('Powerful Jolt',
                    "Summon a powerful jolt of energy to destroy your foes.",
                    10, 10, 13, "electric")
sp_storm = Damaging('Superior Storm',
                    "Unleash a devastating lightning storm to destroy your foes.",
                    19, 22, 23, "electric")

# Grass
lef_blad = Damaging('Leaf Blade',
                    "Summon a weak blade of grass to destroy your foes.",
                    3, 1, 5, "grass")
gra_gren = Damaging('Grass Grenade',
                    "Summon a small explosion to destroy your foes.",
                    10, 12, 13, "grass")
vin_strm = Damaging('Vine Storm',
                    "Unleash a frenzy of powerful vines to destroy your foes.",
                    19, 24, 23, "grass")

# Water
bub_splsh = Damaging('Bubble Splash',
                     "Summon a small wave of bubbles to destroy your foes.",
                     3, 2, 5, "water")
wtr_blast = Damaging('Water Blast',
                     "Summon a large burst of water to destroy your foes.",
                     10, 12, 13, "water")
tsunami = Damaging('Tsunami',
                   "Unleash a terrifying barrage of waves upon your foes.",
                   19, 24, 23, "water")

# Earth
mud_toss = Damaging('Mud Toss',
                    "Summon a small ball of mud to throw at your foes.",
                    3, 4, 6, "earth")
rock_slam = Damaging('Rock Slam',
                     "Crush your enemies with a wall of solid rock.",
                     10, 14, 14, "earth")
earthquake = Damaging("Earthquake",
                      "Wreck havoc on your enemies with a powerful earthquake.",
                      19, 27, 24, "earth")

# -- Healing -- #
min_heal = Healing('Minor Healing',
                   "Restore a small amount of HP by using magic.",
                   3, 1, 20)
adv_heal = Healing('Advanced Healing',
                   "Restore a large amount of HP by using magic.",
                   10, 13, 60)
div_heal = Healing('Divine Healing',
                   "Call upon the arcane arts to greatly restore your HP.",
                   25, 25, 125)

# -- Buffs -- #
m_quick = Buff('Minor Quickness',
               "Temporarily raise your speed by a small amount.",
               2, 4, 2, "Speed")
m_evade = Buff('Minor Evade',
               "Temporarily raise your evasion by a small amount.",
               2, 4, 2, "Evasion")

m_defend = Buff('Minor Defend',
                "Temporarily raise your defense by a small amount.",
                2, 5, 2, "Defense")
m_shield = Buff('Minor Shield',
                "Temporarily raise your magic defense by a small amount.",
                2, 5, 2, "Magic Defense")

m_stren = Buff('Minor Strengthen',
               "Temporarily raise your attack by a small amount.",
               2, 6, 2, "Attack")
m_power = Buff('Minor Empower',
               "Temporarily raise your magic attack by a small amount.",
               2, 6, 2, "Magic Attack")

a_defend = Buff('Adept Defend',
                "Temporarily raise your defense by a large amount.",
                7, 12, 5, "Defense")
a_shield = Buff('Adept Shield',
                "Temporarily raise your magic defense by a large amount.",
                7, 12, 5, "Magic Defense")

a_stren = Buff('Adept Strengthen',
               "Temporarily raise your attack by a large amount.",
               7, 10, 5, "Attack")
a_power = Buff('Adept Empower',
               "Temporarily raise your magic attack by a large amount.",
               7, 10, 5, "Magic Attack")

a_quick = Buff('Adept Quickness',
               "Temporarily raise your speed by a large amount.",
               7, 11, 5, "Speed")
a_evade = Buff('Adept Evade',
               "Temporarily raise your evasion by a large amount.",
               7, 11, 5, "Evasion")

spells = [
    w_flame, lef_blad, in_spark, bub_splsh, mud_toss, min_heal,
    m_quick, m_evade, m_defend, m_shield, m_stren, m_power,
    f_blaze, gra_gren, pwr_jolt, wtr_blast, rock_slam, adv_heal,
    a_stren, a_power, a_defend, a_shield, a_quick, a_evade,
    g_infer, vin_strm, sp_storm, tsunami, earthquake, div_heal
]


def eval_element(p_elem='none', m_elem='none', m_dmg=0, p_dmg=0):
    # Fire < Water < Electricity < Earth < Grass < Wind < Ice < Fire
    # Life < Death and Death < Life
    # "None" element is neutral to all elements.
    element_list = ['fire', 'water', 'electric', 'earth',
                    'grass', 'wind', 'ice']

    if (p_elem == 'death' and m_elem == 'life') or (p_elem == 'life' and m_elem == 'death'):
        p_dmg *= 1.5
        m_dmg *= 1.5
        return [p_dmg, m_dmg]

    elif (p_elem == 'death' and m_elem == 'death') or (p_elem == 'life' and m_elem == 'life'):
        p_dmg /= 1.5
        m_dmg /= 1.5
        return [p_dmg, m_dmg]

    for x, y in enumerate(element_list):
        if p_elem == y:
            player = x
        if m_elem == y:
            monster = x

    try:
        if p_elem == element_list[monster + 1]:
            m_dmg /= 1.5
        elif p_elem == element_list[monster - 1]:
            m_dmg *= 1.5
    except (IndexError, NameError):
        if p_elem != 'none':
            if m_elem == 'ice':
                m_dmg /= 1.5
            elif m_elem == 'water':
                m_dmg *= 1.5
    finally:
        try:
            if m_elem == element_list[player + 1]:
                p_dmg /= 1.5
            elif m_elem == element_list[player - 1]:
                p_dmg *= 1.5
        except (IndexError, NameError):
            if m_elem != 'none':
                if p_elem == 'ice':
                    p_dmg /= 1.5
                elif p_elem == 'water':
                    p_dmg *= 1.5

    return [int(p_dmg), int(m_dmg)]


spellbook = {'Healing': [min_heal], 'Damaging': [w_flame, lef_blad], 'Buffs': []}


def pick_cat(var, dodge, is_battle=True):
    if battle.temp_stats['status_effect'] == 'silenced':
        print("You are silenced -- you can't use magic right now.")
        return False

    while True:
        do_continue = False
        cat = input("""Spellbook:
      [1] Damaging Spells
      [2] Buff Spells
      [3] Healing Spells
      [4] Use Most Recent Spell
Input [#] (or type "exit"): """)

        if cat == '1':
            cat = 'Damaging'

        elif cat == '2':
            cat = 'Buffs'

        elif cat == '3':
            cat = 'Healing'

        elif cat == '4':
            spell = ''

            try:
                for cat in spellbook:
                    for x in spellbook[cat]:
                        if x.name == main.misc_vars['prev_spell']:
                            spell = x
            except KeyError:
                main.misc_vars['prev_spell'] = ""

            if not spell:
                print('-'*25)
                print('You have no previously used spells!')
                print('-'*25)
                continue

            while True:
                y_n = input('Use {0}? | Yes or No: '.format(str(spell)))
                if not y_n:
                    continue

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    if isinstance(spell, Damaging):

                        if spell.use_magic(var, dodge):
                            return True
                        else:
                            return False

                    else:
                        if isinstance(spell, Healing):
                            if spell.use_magic_healing(is_battle):
                                return True

                        elif spell.use_magic():
                            return True

                        else:
                            return False

                elif y_n.startswith('n'):
                    print('-'*25)
                    do_continue = True
                    break

        else:
            if cat.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                return False

            else:
                continue

        if do_continue:
            continue

        if not spellbook[cat]:
            print('-'*25)
            print('You do not yet have any spells in the {0} category.'.format(cat))
            print('-'*25)
            continue

        if pick_spell(cat, var, dodge, is_battle):
            return True


def pick_spell(cat, var, dodge, is_battle):
    print('-'*25)

    while True:

        print(cat + ' Spells: \n      ' + '\n      '.join(
            ['[' + str((num + 1)) + '] ' + spell.name + ' --> ' + str(
                spell.mana) + ' MP' for num, spell in enumerate(
                    spellbook[cat])]))

        while True:
            spell = input('Input [#] (or type "back"): ')

            try:
                spell = int(spell) - 1
            except ValueError:

                spell = spell.lower()

                if spell in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    return False
                else:
                    continue

            try:
                spell = spellbook[cat][spell]
            except IndexError:
                continue

            print('-'*25)
            print(''.join([str(spell), ': ', spell.desc, ' | ', str(spell.mana), ' MP']))
            print('-'*25)

            while True:
                y_n = input('Use {0}? | Yes or No: '.format(str(spell)))
                if y_n == '':
                    continue

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    main.misc_vars['prev_spell'] = spell.name

                    if isinstance(spell, Damaging):

                        if spell.use_magic(var, dodge):
                            return True
                        else:
                            return False

                    else:
                        if isinstance(spell, Healing):
                            if spell.use_magic_healing(is_battle):
                                return True

                        elif spell.use_magic():
                            return True

                        else:
                            return False

                elif y_n.startswith('n'):
                    break


def new_spells():
    # Teach the player new spells as they level up, or low-level spells not
    # previously in the game.
    global spellbook
    for spell in spells:
        if isinstance(spell, Damaging):
            cat = 'Damaging'
        elif isinstance(spell, Healing):
            cat = 'Healing'
        elif isinstance(spell, Buff):
            cat = 'Buffs'
        if main.player.lvl >= spell.req_lvl:
            for x in spellbook[cat]:
                if x.name == spell.name:
                    break
            else:
                spellbook[cat].append(spell)
                print('You have learned "{0}", a new {1} spell!'.format(
                    str(spell), cat if not cat.endswith('s') else cat[0:len(cat) - 1]))


def serialize_sb(path):
    j_spellbook = {}
    for cat in spellbook:
        j_spellbook[cat] = []

        for spell in spellbook[cat]:
            j_spellbook[cat].append(spell.__dict__)

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_spellbook, f, indent=4, separators=(', ', ': '))


def deserialize_sb(path):
    global spellbook
    norm_sb = {}
    with open(path, encoding='utf-8') as f:
        j_spellbook = json.load(f)
    for category in j_spellbook:
        norm_sb[category] = []
        for spell in j_spellbook[category]:
            if category == 'Damaging':
                x = Damaging('', '', '', '', '', '')
            elif category == 'Healing':
                x = Healing('', '', '', '', '')
            elif category == 'Buffs':
                x = Buff('', '', '', '', '', '')
            x.__dict__ = spell
            norm_sb[category].append(x)
    spellbook = norm_sb
