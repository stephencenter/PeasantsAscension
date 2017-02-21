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

from MagicClass import *
import json

# -- Damaging Spells -- #
# Neutral
magic_shot = Damaging('Magical Shot', "Hurl a small ball of magical energy at your enemies! (25% Spell Power)",
                      3, 1, 0.25, "none")

magic_burst = Damaging('Magical Burst', "Shatter your enemy with a wave of magical energy! (50% Spell Power)",
                       9, 11, 0.5, "none")

magic_blast = Damaging('Magical Blast', "Annihilate your enemies with a blast of magical energy! (100% Spell Power)",
                       18, 23, 1, "none", a_c=['mage'])

# Fire
flame_bolt = Damaging('Flame Bolt', "Summon a small fireball to destroy your foes! (25% Spell Power)",
                      3, 2, 0.25, "fire")

f_blaze = Damaging('Fierce Blaze', "Summon a powerful flame to destroy your foes! (50% Spell Power)",
                   10, 12, 0.5, "fire")

g_infer = Damaging('Grand Inferno', "Unleash a monstrous blaze destroy your foes! (100% Spell Power)",
                   20, 24, 1, "fire", a_c=['mage'])

# Grass
lef_blad = Damaging('Leaf Blade', "Summon razor-sharp blades of grass to destroy your foes! (25% Spell Power)",
                    3, 2, 0.25, "grass")

gra_gren = Damaging('Grass Grenade', "Summon a small explosion to destroy your foes! (50% Spell Power)",
                    10, 12, 0.5, "grass")

vin_strm = Damaging('Vine Storm', "Unleash a frenzy of powerful vines to destroy your foes! (100% Spell Power)",
                    20, 24, 1, "grass", a_c=['mage'])

# Electricity
spark = Damaging('Spark', "Summon a small spark to destroy your foes! (25% Spell Power)",
                 3, 3, 0.25, "electric")

pwr_jolt = Damaging('Powerful Jolt', "Summon a powerful jolt of energy to destroy your foes! (50% Spell Power)",
                    10, 13, 0.5, "electric")

sp_storm = Damaging('Superior Storm', "Unleash a devastating lightning storm to destroy your foes! (100% Spell Power)",
                    20, 25, 1, "electric", a_c=['mage'])

# Water
drizzle = Damaging('Drizzle', "Summon a small to destroy your foes! (25% Spell Power)",
                   3, 3, 0.25, "water")

wtr_blast = Damaging('Water Blast', "Summon a large burst of water to destroy your foes! (50% Spell Power)",
                     10, 13, 0.5, "water")

tsunami = Damaging('Tsunami', "Unleash a terrifying barrage of waves upon your foes! (100% Spell Power)",
                   20, 25, 1, "water", a_c=['mage'])

# Earth
mud_toss = Damaging('Mud Toss', "Summon a small ball of mud to throw at your foes! (25% Spell Power)",
                    3, 4, 0.25, "earth")

rock_slam = Damaging('Rock Slam', "Crush your enemies under a layer of solid rock! (50% Spell Power)",
                     10, 13, 0.5, "earth")

earthquake = Damaging("Earthquake", "Wreck havoc on your enemies with a powerful earthquake! (100% Spell Power)",
                      20, 25, 1, "earth", a_c=['mage'])

# Ice
icicle_dagger = Damaging('Icicle Dagger', "Hurl a volley of supercooled icicles at your enemies! (25% Spell Power)",
                         3, 4, 0.25, "ice")

hail_storm = Damaging('Hailstorm', "Rain ice upon your enemies with unrelenting force! (50% Spell Power)",
                      11, 14, 0.5, 'ice')

blizzard = Damaging('Blizzard', "Devastate your enemies with a terrifying flurry of ice and wind! (100% Spell Power)",
                    23, 26, 1, 'ice', a_c=['mage'])

# Wind
m_gust = Damaging('Minor Gust', "Batter your enemies with powerful gusts and winds! (25% Spell Power)",
                  3, 4, 0.25, "wind")

microburst = Damaging('Microburst',
                      "Decimate your foes with a powerful blast of wind! (50% Spell Power)",
                      11, 14, 0.5, "wind")
cyclone = Damaging('Cyclone',
                   "Demolish all that stand in your path with a terrifying tornado! (100% Spell Power)",
                   23, 26, 1, "wind", a_c=['mage'])

# Light
purify = Damaging('Purify', "Call upon His Divinity to cast out evil creatures! (25% Spell Power)!",
                  3, 5, 0.25, "light")
smite = Damaging('Holy Smite', "Strike down unholy beings using His Divinity's power! (50% Spell Power)",
                 11, 15, 0.5, "light")
moonbeam = Damaging('Moonbeam', "Utterly destroy evil creatures with holy rays from the moon! (100% Spell Power)",
                    23, 27, 1, "light", a_c=('paladin', 'mage'))


# Dark
curse = Damaging('Evil Curse', "Call upon His Wickedness to harm holy creatures! (25% Spell Power)",
                 3, 5, 0.25, "dark")
desecration = Damaging('Desecration', "Defile holy spirits with an evil aura! (50% Spell Power)",
                       11, 15, 0.5, "dark")
unholy_rend = Damaging('Unholy Rend', "Annihilate holy creatures with a sundering blow! (100% Spell Power)",
                       23, 27, 1, "dark", a_c=['mage'])

# -- Healing -- #
# Every character starts with this spell
pit_heal = Healing('Novice Healing', """\
Restore a small amount of an ally's HP using holy magic. Heals 10 HP or 5% of
the target's max HP, whichever is greater (5% Healing Power)""", 2, 1, 10, 0.05)

# The Paladin also starts with this spell
min_heal = Healing('Adept Healing', """\
Restore a moderate amount of an ally's HP using holy magic. Heals 25 HP or 20%
of the target's max HP, whichever is greater (20% Healing Power)""",
                   5, 3, 25, 0.2, a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))

# This tier and up can only be learned by Paladins and Mages
adv_heal = Healing('Advanced Healing', """\
Restore a large amount of an ally's HP using holy magic. Heals 70 HP or 50%
of the target's max HP, whichever is greater (50% Healing Power)""",
                   10, 15, 70, 0.5, a_c=('paladin', 'mage'))

div_heal = Healing('Divine Healing', """\
Restore a very large amount of an ally's HP using holy magic. Heals 125 HP or
75% of the target's max HP, whichever is greater (75% Healing Power)""",
                   25, 28, 125, 0.75, a_c=('paladin', 'mage'))

# -- Buffs -- #

# Movement Buffs
m_quick = Buff('Minor Quickness', """\
Raise an ally's speed by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 1, 0.15, "spd", a_c=('mage', 'monk', 'ranger', 'assassin'))

m_evade = Buff('Minor Evade', """\
Raise an ally's evasion by 15%. Stacks with multiple uses. Lasts until the end
of battle. Note: Evasion has a cap of 256 (50% chance to dodge).""",
               3, 1, 0.15, "evad", a_c=('mage', 'monk', 'ranger', 'assassin'))

a_quick = Buff('Adept Quickness', """\
Raise an ally's speed by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 10, 0.3, "spd", a_c=('mage', 'monk', 'ranger', 'assassin'))

a_evade = Buff('Adept Evade', """\
Raise an ally's evasion by 30%. Stacks with multiple uses. Lasts until the end
of battle. Note: Evasion has a cap of 256.""",
               6, 10, 0.3, "evad", a_c=('mage', 'monk', 'ranger', 'assassin'))

# Defense Buffs
m_defend = Buff('Minor Defend', """\
Raise an ally's Physical Defense by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 3, 0.15, "dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

m_shield = Buff('Minor Shield', """\
Raise an ally's Magical Defense by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 5, 0.15, "m_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

m_block = Buff('Minor Block', """\
Raise an ally's Pierce Defense by 15%. Stacks with multiple uses. Lasts until
the end of battle.""", 3, 7, 0.15, "p_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

a_defend = Buff('Adept Defend', """\
Raise an ally's Physical Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 14, 0.3, "dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

a_shield = Buff('Adept Shield', """\
Raise an ally's Magical Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 16, 0.3, "m_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

a_block = Buff('Adept Block', """\
Raise an ally's Pierce Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 18, 0.3, "p_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

# Attack Buffs
m_stren = Buff('Minor Strengthen', """\
Raise an ally's Physical Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 2, 0.15, "attk", a_c=('mage', 'paladin', 'warrior', 'assassin', 'monk'))

m_power = Buff('Minor Empower', """\
Raise an ally's Magical Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 4, 0.15, "m_attk", a_c=('mage', 'paladin', 'monk'))

m_aim = Buff('Minor Aim', """\
Raise an ally's Pierce Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 6, 0.15, "p_attk", a_c=('ranger', 'mage', 'monk'))

a_stren = Buff('Adept Strengthen', """\
Raise an ally's Physical Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 13, 0.3, "attk", a_c=('mage', 'paladin', 'warrior', 'assassin', 'monk'))

a_power = Buff('Adept Empower', """\
Raise an ally's Magical Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 15, 0.3, "m_attk", a_c=('mage', 'paladin', 'monk'))

a_aim = Buff('Adept Aim', """\
Raise an ally's Pierce Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 17, 0.3, "p_attk", a_c=('mage', 'ranger', 'monk'))

all_spells = [
    pit_heal, min_heal, adv_heal, div_heal,  # Healing Spells
    magic_shot, magic_burst, magic_blast,    # Neutral-element Spells
    flame_bolt, f_blaze, g_infer,            # Fire Spells
    lef_blad, gra_gren, vin_strm,            # Grass Spells
    spark, pwr_jolt, sp_storm,               # Electric Spells
    drizzle, wtr_blast, tsunami,             # Water Spells
    mud_toss, rock_slam, earthquake,         # Earth Spells
    icicle_dagger, hail_storm, blizzard,     # Ice Spells
    m_gust, microburst, cyclone,             # Wind Spells
    purify, smite, moonbeam,                 # Light Spells
    curse, desecration, unholy_rend,         # Dark Spells

    m_quick, m_evade, a_quick, a_evade,       # Movement Spells
    m_defend, m_shield, a_defend, a_shield,   # Defense Spells
    m_stren, m_power, a_stren, a_power,       # Attack Spells
    m_aim, m_block, a_aim, a_block]           # Pierce Spells

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
                    x = Healing('', '', '', '', '', '')

                elif category == 'Buffs':
                    x = Buff('', '', '', '', '', '')

                elif category == 'Previous Spell':
                    continue

                x.__dict__ = spell
                norm_sb[user][category].append(x)

    spellbook = norm_sb
