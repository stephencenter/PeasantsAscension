#   This file is part of Peasants' Ascension.
#
#	 Peasants' Ascension is free software: you can redistribute it and/or modify
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

import sys
import json
import random
import time
import math
import pygame

import units
import battle
import inv_system
import sounds
import ascii_art

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# This is the message that is printed if you attempt to use magic
# without the required amount of mana.
out_of_mana = """-------------------------
You don't have enough mana to cast that spell!"""


class Spell:
    def __init__(self, name, desc, mana, req_lvl, a_c=('mage',)):
        self.name = name
        self.desc = desc
        self.mana = mana
        self.req_lvl = req_lvl
        self.a_c = a_c  # These are the classes that are able to obtain this spell

    def __str__(self):
        return self.name

    def use_mana(self, user):
        user.mp -= self.mana
        if user.mp < 0:
            user.mp = 0


class Healing(Spell):
    # Healing spells are spells that restore your HP during battle
    def __init__(self, name, desc, mana, req_lvl, health, thresh, a_c=('mage', 'paladin')):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.health = health
        self.thresh = thresh

    def __str__(self):
        return self.name

    def use_magic(self, user, is_battle):
        if user.mp >= self.mana:
            print()
            Spell.use_mana(self, user)

            target_options = [x for x in [
                units.player,
                units.solou,
                units.xoann,
                units.adorine,
                units.ran_af,
                units.parsto,
                units.chyme] if x.enabled
            ]

            if len(target_options) == 1:
                target = user

            else:
                print("Select Target for {0}:".format(self.name))
                print("     ", "\n      ".join(["[{0}] {1}".format(int(num) + 1, character.name)
                                               for num, character in enumerate(target_options)]))

                while True:
                    target = input("Input [#]: ")
                    try:
                        target = int(target) - 1

                    except ValueError:
                        continue

                    try:
                        target = target_options[target]

                    except IndexError:
                        continue

                    break

            # Healing spells will always restore a minimum of user.hp*thresh.
            # e.g. A spell that heals 20 HP but has a 20% threshold will restore 20 HP for someone
            # with 45 max HP, but will restore 32 HP for someone with 160 max HP.
            # In addition to this, the user restores an additional 2*Wisdom, unless they are a
            # Paladin in which case it it 4*Wisdom.
            if self.health < target.hp*self.thresh:
                total_heal = target.hp*self.thresh + \
                    (4*user.attributes['wis'] if user.class_ == 'paladin' else 2*user.attributes['wis'])

                target.hp += total_heal
                target.hp = math.ceil(target.hp)

            else:
                total_heal = self.health + (2*user.attributes['wis'] if user.class_ !=
                                            'paladin' else 4*user.attributes['wis'])
                target.hp += total_heal

            # Handle HP higher than max due to overheal
            if target.hp > target.max_hp:
                target.hp -= (target.hp - target.max_hp)

            sounds.magic_healing.play()

            if is_battle:
                # Print the ASCII art and "User Turn" info if a battle is going on
                print("-{0}'s Turn-")
                print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

            print('Using "{0}", {1} is healed by {2} HP!'.format(self.name, target.name, total_heal))

            return True

        else:
            # Disallow the usage of spells if the player has insufficent MP
            print(out_of_mana)
            return False


class Damaging(Spell):
    # Damaging spells are spells that deal damage to the enemy during battle.
    # Just like normal attacks, they have a chance to miss based on
    # the enemy's evade stat.
    def __init__(self, name, desc, mana, req_lvl, damage, element, a_c=('mage',)):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.damage = damage
        self.element = element

    def __str__(self):
        return self.name

    def use_magic(self, user):
        inv_name = user.name if user != units.player else 'player'

        # Spells cannot be cast if the player does not have enough mana for it
        if user.mp >= self.mana:
            print()
            Spell.use_mana(self, user)

            # Determine the power of the attack
            dam_dealt = math.ceil(battle.temp_stats[user.name]['m_attk'] - units.monster.m_dfns/2)

            if user.class_ == 'mage':
                dam_dealt *= 1.5

            dam_dealt *= 1 + self.damage
            dam_dealt = math.ceil(dam_dealt)

            # Evaluate the element of the attack and the enemy
            dam_dealt = eval_element(
                p_elem=self.element,
                m_elem=units.monster.element,
                p_dmg=dam_dealt)[0]

            if dam_dealt < 1:
                dam_dealt = 1

            print("-{0}'s Turn-".format(user.name))
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

            if inv_system.equipped[inv_name]['weapon'].class_ == 'magic':
                print('{0} begins to use their {1} to summon a powerful spell...'.format(
                    user.name, inv_system.equipped[inv_name]['weapon']))

            else:
                print('{0} attempts to summon a powerful spell...'.format(user.name))

            sounds.magic_attack.play()
            main.smart_sleep(0.75)

            # If the monster's evasion (with a max of 256) is higher than the user's accuracy roll,
            # the spell will land
            if random.randint(1, 512) in range(units.monster.evad, 512):
                sounds.enemy_hit.play()

                # Mages have a 15% chance to get a critical hit, whereas other classes cannot
                if random.randint(0, 100) <= (15 if user.class_ == 'mage' else -1):
                    dam_dealt *= 1.5
                    print("It's a critical hit! 1.5x damage!")

                    sounds.critical_hit.play()
                    main.smart_sleep(0.5)

                print('Using the power of "{0}", {1} deals {2} damage to the {3}!'.format(
                    self.name, user.name, dam_dealt, units.monster.monster_name))

                units.monster.hp -= dam_dealt

            # Otherwise, the spell with miss and deal no damage
            else:
                sounds.attack_miss.play()
                print("The {0} narrowly dodges {1}'s spell!".format(units.monster.monster_name, user.name))

            return True

        else:
            print(out_of_mana)
            return False


class Buff(Spell):
    # Buffs are spells that temporarily raise the player's stats
    # during battle. They last until the battle is over, at which
    # point the player's stats will return to normal.
    def __init__(self, name, desc, mana, req_lvl, increase, stat, a_c=('mage', 'monk')):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.increase = increase
        self.stat = stat

    def __str__(self):
        return self.name

    def use_magic(self, user):
        if user.mp >= self.mana:
            Spell.use_mana(self, user)

            print("\n-{0}'s Turn-")
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
            print(f'{user.name} raises their stats using the power of {self.name}!')

            sounds.buff_spell.play()

            battle.temp_stats[user.name][self.stat] *= 1 + self.increase
            battle.temp_stats[user.name][self.stat] = math.ceil(battle.temp_stats[user.name][self.stat])

            return True

        else:
            print(out_of_mana)
            return False


# -- Attacks -- #

# Neutral (No element)
magic_shot = Damaging('Magical Shot',
                      "Hurl a small ball of magical energy at your enemies! (Weak)",
                      3, 1, 0.25, "none",
                      a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))
magic_burst = Damaging('Magical Burst',
                       "Shatter your enemy's defenses with a burst of magical energy! (Moderate)",
                       9, 11, 0.5, "none",
                       a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))
magic_blast = Damaging('Magical Blast',
                       "Bomb your enemies with a detonating ball of magical energy! (Strong)",
                       18, 23, 1, "none",
                       a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))

# Fire
w_flame = Damaging('Weak Flame',
                   "Summon a weak fireball to destroy your foes. (Weak)",
                   3, 2, 0.25, "fire")
f_blaze = Damaging('Fierce Blaze',
                   "Summon a powerful flame to destroy your foes. (Moderate)",
                   10, 12, 0.5, "fire")
g_infer = Damaging('Grand Inferno',
                   "Unleash a monstrous blaze destroy your foes. (Strong)",
                   20, 24, 1, "fire")

# Grass
lef_blad = Damaging('Leaf Blade',
                    "Summon a weak blade of grass to destroy your foes. (Weak)",
                    3, 2, 0.25, "grass")
gra_gren = Damaging('Grass Grenade',
                    "Summon a small explosion to destroy your foes. (Moderate)",
                    10, 12, 0.5, "grass")
vin_strm = Damaging('Vine Storm',
                    "Unleash a frenzy of powerful vines to destroy your foes. (Strong)",
                    20, 24, 1, "grass")

# Electricity
in_spark = Damaging('Inferior Spark',
                    "Summon a weak spark to destroy your foes. (Weak)",
                    3, 3, 0.25, "electric")
pwr_jolt = Damaging('Powerful Jolt',
                    "Summon a powerful jolt of energy to destroy your foes. (Moderate)",
                    10, 13, 0.5, "electric")
sp_storm = Damaging('Superior Storm',
                    "Unleash a devastating lightning storm to destroy your foes. (Strong)",
                    20, 25, 1, "electric")

# Water
bub_splsh = Damaging('Bubble Splash',
                     "Summon a small wave of bubbles to destroy your foes. (Weak)",
                     3, 3, 0.25, "water")
wtr_blast = Damaging('Water Blast',
                     "Summon a large burst of water to destroy your foes. (Moderate)",
                     10, 13, 0.5, "water")
tsunami = Damaging('Tsunami',
                   "Unleash a terrifying barrage of waves upon your foes. (Strong)",
                   20, 25, 1, "water")

# Earth
mud_toss = Damaging('Mud Toss',
                    "Summon a small ball of mud to throw at your foes. (Weak)",
                    3, 4, 0.25, "earth")
rock_slam = Damaging('Rock Slam',
                     "Crush your enemies with a wall of solid rock. (Moderate)",
                     10, 13, 0.5, "earth")
earthquake = Damaging("Earthquake",
                      "Wreck havoc on your enemies with a powerful earthquake. (Strong)",
                      20, 25, 1, "earth")

# Ice
icicle_dagger = Damaging('Icicle Dagger',
                         "Hurl a volley of supercooled icicles at your enemies. (Weak)",
                         3, 4, 0.25, "ice")
hail_storm = Damaging('Hailstorm',
                      "Rain ice upon your enemies with unrelenting force! (Moderate)",
                      11, 14, 0.5, 'ice')
blizzard = Damaging('Blizzard',
                    "Devastate your enemies with a terrifying flurry of ice and wind. (Strong)",
                    23, 26, 1, 'ice')

# Wind
m_gust = Damaging('Minor Gust',
                  "Batter your enemies with powerful gusts and winds! (Weak)",
                  3, 4, 0.25, "wind")
microburst = Damaging('Microburst',
                      "Decimate your foes with a powerful blast of wind! (Moderate)",
                      11, 14, 0.5, "wind")
cyclone = Damaging('Cyclone',
                   "Demolish all that stand in your path with a terrifying tornado! (Strong)",
                   23, 26, 1, "wind")

# Life
purify = Damaging('Purify',  # Paladins start with this spell
                  "Call upon His Divinity to cast out evil creatures! (Weak)",
                  3, 5, 0.25, "life", a_c=('paladin', 'mage'))
smite = Damaging('Holy Smite',
                 "Strike down unholy beings using His Divinity's power! (Moderate)",
                 11, 15, 0.5, "life", a_c=('paladin', 'mage'))
moonbeam = Damaging('Moonbeam',
                    "Utterly destroy evil creatures with holy rays from the moon! (Strong)",
                    23, 27, 1, "life", a_c=('paladin', 'mage'))


# Death
curse = Damaging('Evil Curse',
                 "Call upon His Wickedness to harm holy creatures! (Weak)",
                 3, 5, 0.25, "death")
desecration = Damaging('Desecration',
                       "Defile holy spirits with an evil aura! (Moderate)",
                       11, 15, 0.5, "death")
unholy_rend = Damaging('Unholy Rend',
                       "Annihilate holy creatures with a searing blow! (Strong)",
                       23, 27, 1, "death")

# -- Healing -- #
pit_heal = Healing('Pitiful Healing',  # Every character starts with this spell
                   """Restore a downright pitiful amount of HP by using magic.
Heals 10 HP or 5% of the target's max HP, whichever is more (Tier 1: Pitiful)""",
                   1, 1, 10, 0.05)

min_heal = Healing('Minor Healing',  # The Paladin also starts with this spell
                   """Restore a small amount of HP by using magic.
Heals 25 HP or 20% of the target's max HP, whichever is more (Tier 2: Weak)""",
                   3, 3, 25, 0.2, a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))

adv_heal = Healing('Advanced Healing',  # This tier and up can only be learned by Paladins and Mages
                   """Restore a large amount of HP by using magic.
Heals 70 HP, or 50% of the target's max HP, whichever is more (Tier 3: Moderate)""",
                   10, 15, 70, 0.5, a_c=('paladin', 'mage'))

div_heal = Healing('Divine Healing',
                   """Call upon the arcane arts to greatly restore your HP.
Heals 100% of the target's HP (Tier 4: Strong)""",
                   25, 28, 0, 1, a_c=('paladin', 'mage'))

# -- Buffs -- #

# Movement Buffs
m_quick = Buff('Minor Quickness',
               "Temporarily raise your speed by a small amount. (Weak)",
               3, 1, 0.25, "spd", a_c=('mage', 'monk', 'ranger', 'assassin'))
m_evade = Buff('Minor Evade',
               "Temporarily raise your evasion by a small amount. (Weak)",
               3, 1, 0.25, "evad", a_c=('mage', 'monk', 'ranger', 'assassin'))

a_quick = Buff('Adept Quickness',
               "Temporarily raise your speed by a large amount. (Moderate)",
               6, 10, 0.5, "spd", a_c=('mage', 'monk', 'ranger', 'assassin'))
a_evade = Buff('Adept Evade',
               "Temporarily raise your evasion by a large amount. (Moderate)",
               6, 10, 0.5, "evad", a_c=('mage', 'monk', 'ranger', 'assassin'))

# Defense Buffs
m_defend = Buff('Minor Defend',
                "Temporarily raise your defense by a small amount. (Weak)",
                3, 3, 0.25, "dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
m_shield = Buff('Minor Shield',
                "Temporarily raise your magic defense by a small amount. (Weak)",
                3, 3, 0.25, "m_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
m_block = Buff('Minor Block',
               "Temporarily raise your pierce defense by a small amount. (Weak)",
               3, 7, 0.25, "p_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

a_defend = Buff('Adept Defend',
                "Temporarily raise your defense by a large amount. (Moderate)",
                6, 13, 0.5, "dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
a_shield = Buff('Adept Shield',
                "Temporarily raise your magic defense by a large amount. (Moderate)",
                6, 13, 0.5, "m_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
a_block = Buff('Adept Block',
               "Temporarily raise your pierce defense by a large amount. (Moderate)",
               6, 17, 0.5, "p_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

# Attack Buffs
m_stren = Buff('Minor Strengthen',
               "Temporarily raise your attack by a small amount. (Weak)",
               3, 6, 0.25, "attk", a_c=('mage', 'paladin', 'warrior', 'assassin', 'monk'))
m_power = Buff('Minor Empower',
               "Temporarily raise your magic attack by a small amount. (Weak)",
               3, 6, 0.25, "m_attk")
m_aim = Buff('Minor Aim',
             "Temporarily raise your pierce attack by a small amount. (Weak)",
             3, 7, 0.25, "p_attk", a_c=('ranger', 'mage', 'monk'))

a_stren = Buff('Adept Strengthen',
               "Temporarily raise your attack by a large amount. (Moderate)",
               6, 16, 0.5, "attk", a_c=('mage', 'paladin', 'warrior', 'assassin', 'monk'))
a_power = Buff('Adept Empower',
               "Temporarily raise your magic attack by a large amount. (Moderate)",
               6, 16, 0.5, "m_attk")
a_aim = Buff('Adept Aim',
             "Temporarily raise your pierce attack by a large amount. (Moderate)",
             6, 17, 0.5, "p_attk", a_c=('ranger', 'mage', 'monk'))

# -- Other Spells -- #
r_affliction = Spell('Relieve Affliction', 'Cure yourself of all status ailments, such as poison or weakness.', 4, 5)


def relieve_affliction(user, is_battle):
    if user.mp >= r_affliction.mana:
        if user.status_ail != 'none':

            Spell.use_mana(r_affliction, user)

            if is_battle:
                print(f"\n-{user.name}'s Turn-")
                print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

            print(f'Using the power of {r_affliction.name}, {user.name} is cured of their afflictions!')

            user.status_ail = 'none'
            sounds.buff_spell.play()

            return True

        else:
            print('-'*25)
            print("{0} doesn't have any status ailments.".format(user.name))
            print('-'*25)
            return False

    else:
        print(out_of_mana)
        return False


r_affliction.use_magic = relieve_affliction

spells = [
    pit_heal, min_heal, adv_heal, div_heal,  # Healing Spells (Level 1, 3, 15, 28)
    magic_shot, magic_burst, magic_blast,    # Neutral-typed Spells (Level 1, 11, 23)
    w_flame, f_blaze, g_infer,               # Fire Spells (Level 2, 12, 24)
    lef_blad, gra_gren, vin_strm,            # Grass Spells (Level 2, 12, 24)
    in_spark, pwr_jolt, sp_storm,            # Electric Spells (Level 3, 13, 25)
    bub_splsh, wtr_blast, tsunami,           # Water Spells (Level 3, 13, 25)
    mud_toss, rock_slam, earthquake,         # Earth Spells (Level 4, 14, 26)
    icicle_dagger, hail_storm, blizzard,     # Ice Spells (Level 4, 14, 26)
    m_gust, microburst, cyclone,             # Wind Spells (Level 4, 14, 26)
    purify, smite, moonbeam,                 # Life Spells (Level 5, 15, 27)
    curse, desecration, unholy_rend,         # Death Spells (Level 5, 15, 27)

    m_quick, m_evade, a_quick, a_evade,       # Movement Spells (Level 1, 10)
    m_defend, m_shield, a_defend, a_shield,   # Defense Spells (Level 3, 13)
    m_stren, m_power, a_stren, a_power,       # Attack Spells (Level 6, 16)
    m_aim, m_block, a_aim, a_block,           # Pierce Spells (Level 7, 17)

    r_affliction  # Relieve Affliction (Level 5)
]


def eval_element(p_elem, m_elem, m_dmg=0, p_dmg=0):
    # Fire < Water < Electricity < Earth < Grass < Wind < Ice < Fire
    # Life < Death and Death < Life
    # "None" element is neutral to all elements.

    # Set everything to be lowercase, just incase
    p_elem = p_elem.lower()
    m_elem = m_elem.lower()

    element_matchup = {  # element_matchup[key][0] is the element that key is weak to
                         # element_matchup[key][1] is the element that key is resistant to
        'fire': ['water', 'ice'],
        'water': ['electric', 'fire'],
        'electric': ['earth', 'water'],
        'earth': ['grass', 'electric'],
        'grass': ['wind', 'earth'],
        'wind': ['ice', 'grass'],
        'ice': ['fire', 'wind'],
        'life': ['death', 'life'],
        'death': ['life', 'death']
    }

    if p_elem == 'none' or m_elem == 'none':
        return [p_dmg, m_dmg]

    if element_matchup[p_elem][1] == m_elem:
        if p_elem == 'life' or p_elem == 'death':
            spam = [int(p_dmg/1.5), int(m_dmg/1.5)]
        else:
            spam = [int(p_dmg*1.5), int(m_dmg/1.5)]

        if spam[0] <= 1:
            spam[0] = 2

        return spam

    elif element_matchup[p_elem][0] == m_elem or p_elem == m_elem:
        if p_elem == 'life' or p_elem == 'death':
            return [int(p_dmg*1.5), int(m_dmg*1.5)]
        else:
            return [int(p_dmg/1.5), int(m_dmg*1.5)]

    return [p_dmg, m_dmg]

spellbook = {
    'player': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Solou': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Xoann': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Parsto': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    "Ran'af": {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Adorine': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Chyme': {
        'Healing': [pit_heal, min_heal],
        'Damaging': [magic_shot, purify],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    }
}


def pick_cat(user, is_battle=True):
    inv_name = user.name if user != units.player else 'player'

    if user.status_ail == 'silenced':
        sounds.debuff.play()
        print(f"{user.name} is silenced and cannot use spells!")
        input("\nPress enter/return ")

        return False

    while True:
        do_continue = False
        print("""{0}'s spellbook:
      [1] Damaging Spells
      [2] Buff Spells
      [3] Healing Spells
      [4] Use Most Recent Spell""".format(user.name))
        spam = True
        while spam:
            cat = input('Input [#] (or type "exit"): ')

            if cat == '1':
                cat = 'Damaging'

            elif cat == '2':
                cat = 'Buffs'

            elif cat == '3':
                cat = 'Healing'

            elif cat == '4':
                spell = spellbook[inv_name]['Previous Spell']
                if spell:
                    spell = spell[0]

                    if isinstance(spell, Healing) or spell.name == 'Relieve Affliction':
                        if spell.use_magic(user, is_battle):
                            return True

                        else:
                            break

                    if spell.use_magic(user):
                        return True

                    else:
                        break

                else:
                    print('-'*25)
                    print('{0} has no previously used spells!'.format(user.name))
                    print('-'*25)
                    break

                while True:
                    y_n = input('Use {spell}? | Yes or No: ')

                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        if isinstance(spell, Damaging):
                            return spell.use_magic(user)

                        else:
                            if isinstance(spell, Healing) or spell.name == 'Relieve Affliction':
                                return spell.use_magic(user, is_battle)

                            return spell.use_magic(user)

                    elif y_n.startswith('n'):
                        spam = False
                        do_continue = True
                        break

            else:
                if cat.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    print('-'*25)
                    return False

                else:
                    continue

            if do_continue:
                continue

            if not spellbook[inv_name][cat]:
                print('-'*25)
                print('You do not yet have any spells in the {0} category.'.format(cat))
                print('-'*25)
                continue

            if pick_spell(cat, user, is_battle):
                return True

            break


def pick_spell(cat, user, is_battle):
    global spellbook
    inv_name = user.name if user != units.player else 'player'

    print('-'*25)
    while True:
        padding = len(max([spell.name for spell in spellbook[inv_name][cat]], key=len))
        print(''.join([cat, ' Spells: \n      ']), end='')
        print('\n      '.join(f"[{num + 1}] {spell} --{'-'*(padding - len(spell.name))}> {spell.mana} MP")
              for num, spell in enumerate(spellbook[inv_name][cat]))

        fizz = True
        while fizz:
            spell = input('Input [#] (or type "back"): ').lower()

            try:
                spell = spellbook[inv_name][cat][int(spell) - 1]
            except (ValueError, IndexError):
                if spell in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*25)

                    return False

                continue

            print('-'*25)
            print(''.join([str(spell), ': ', spell.desc, ' | ', str(spell.mana), ' MP']))
            print('-'*25)

            while True:
                y_n = input(f'Use {spell}? | Yes or No: ').lower()

                if y_n.startswith('y'):
                    spellbook[inv_name]['Previous Spell'] = [spell]

                    if isinstance(spell, Damaging):
                        return spell.use_magic(user)

                    else:
                        if isinstance(spell, Healing) or spell.name == 'Relieve Affliction':
                            return spell.use_magic(user, is_battle)

                        return spell.use_magic(user)

                elif y_n.startswith('n'):
                    print('-'*25)
                    fizz = False
                    break


def new_spells(character):
    # Teach the player new spells as they level up, or low-level spells not
    # previously in the game.
    global spellbook

    for spell in spells:
        if isinstance(spell, Damaging):
            cat = 'Damaging'
        elif isinstance(spell, Healing) or spell.name == 'Relieve Affliction':
            cat = 'Healing'
        elif isinstance(spell, Buff):
            cat = 'Buffs'

        # Only give the character spells that they are a high enough level for
        if character.lvl >= spell.req_lvl:
            for x in spellbook[character.name if character != units.player else 'player'][cat]:
                if x.name == spell.name:
                    break

            else:
                # Almost all spells can be learned by mages, but only a few can be learned by other classes
                if character.class_ not in spell.a_c:
                    continue

                sounds.item_pickup.play()
                spellbook[character.name if character != units.player else 'player'][cat].append(spell)

                print(f'{character.name} has learned "{spell}", a new {cat} spell!')
                input('\nPress enter/return ')


def serialize_sb(path):
    j_spellbook = {}
    for user in spellbook:
        j_spellbook[user] = {}

        for cat in spellbook[user]:
            j_spellbook[user][cat] = []

            for spell in spellbook[user][cat]:
                spell_dict = {key: spell.__dict__[key] for key in spell.__dict__ if key != 'use_magic'}
                j_spellbook[user][cat].append(spell_dict)

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_spellbook, f, indent=4, separators=(', ', ': '))


def deserialize_sb(path):
    global spellbook
    norm_sb = {}

    with open(path, encoding='utf-8') as f:
        j_spellbook = json.load(f)

    for user in j_spellbook:
        norm_sb[user] = {}

        for category in j_spellbook[user]:
            norm_sb[user][category] = []

            for spell in j_spellbook[user][category]:

                if category == 'Damaging':
                    x = Damaging('', '', '', '', '', '')

                elif category == 'Healing':
                    if spell['name'] == 'Relieve Affliction':
                        x = Spell('', '', '', '')
                        x.__dict__ = spell
                        x.use_magic = relieve_affliction
                        norm_sb[user][category].append(x)

                        continue

                    x = Healing('', '', '', '', '', '')

                elif category == 'Buffs':
                    x = Buff('', '', '', '', '', '')

                elif category == 'Previous Spell':
                    continue

                x.__dict__ = spell
                norm_sb[user][category].append(x)

    spellbook = norm_sb
