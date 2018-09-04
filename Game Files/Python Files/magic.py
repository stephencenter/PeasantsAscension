# This file is part of Peasants' Ascension.
#
# Peasants' Ascension is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peasants' Ascension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

import copy
import json
import math
import random
import sys

import pygame

import ascii_art
import battle
import save_load
import sounds
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()


class Spell:
    def __init__(self, name, desc, mana, req_lvl, class_, spell_id):
        self.name = name
        self.desc = desc
        self.mana = mana
        self.req_lvl = req_lvl
        self.class_ = class_  # These are the classes that are able to obtain this spell
        self.spell_id = spell_id

    def use_mana(self, user):
        user.mp -= self.mana
        units.fix_stats()

    def use_magic(self, user, is_battle):
        pass


class Healing(Spell):
    # Healing spells are spells that restore your HP during battle
    def __init__(self, name, desc, mana, req_lvl, health, thresh, class_, spell_id):
        super().__init__(name, desc, mana, req_lvl, class_, spell_id)
        self.health = health
        self.thresh = thresh

    def use_magic(self, user, is_battle):
        Spell.use_mana(self, user)
        target = user.target

        # Healing spells will always restore a minimum of target.hp*thresh.
        # e.g. A spell that heals 20 HP but has a 20% threshold will restore 20 HP for someone
        # with 45 max HP, but will restore 32 HP for someone with 160 max HP.
        # In addition to this, the target restores an additional 1 HP for every point of wisdom the user has
        if self.health < target.hp*self.thresh:
            total_heal = target.hp*self.thresh + user.attributes['wis']

        else:
            total_heal = self.health + user.attributes['wis']

        target.hp += total_heal
        target.hp = math.ceil(target.hp)
        units.fix_stats()

        if is_battle:
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
            print(f"{user.name} is preparing to cast {self.name}...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            print(f'Using "{self.name}", {target.name} is healed by {total_heal} HP!')
            sounds.magic_healing.play()

        else:
            print('-'*save_load.divider_size)
            print(f'Using "{self.name}", {target.name} is healed by {total_heal} HP!')
            sounds.magic_healing.play()
            main.s_input("\nPress enter/return ")
            print('-'*save_load.divider_size)


class Damaging(Spell):
    # Damaging spells are spells that deal damage to the enemy during battle.
    # Just like normal attacks, they have a chance to miss based on
    # the enemy's evade stat.
    def __init__(self, name, desc, mana, req_lvl, damage, off_element, class_, spell_id):
        super().__init__(name, desc, mana, req_lvl, class_, spell_id)
        self.damage = damage
        self.off_element = off_element

    def use_magic(self, user, is_battle=True):
        Spell.use_mana(self, user)
        target = user.target

        print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
        print(f'{user.name} attempts to summon a powerful spell...')

        sounds.magic_attack.play()
        main.smart_sleep(0.75)
        dam_dealt = units.deal_damage(user, target, "magical", spell_power=self.damage)

        # If the monster's evasion is higher than the user's accuracy roll, the spell will land
        if random.randint(1, 512) in range(target.evad, 512):
            sounds.enemy_hit.play()
            target.hp -= dam_dealt
            print(f'Using the power of {self.name}, {user.name} deals {dam_dealt} damage to the {target.name}!')

        else:
            sounds.attack_miss.play()
            print(f"The {target.name} narrowly dodges {user.name}'s spell!")


class Buff(Spell):
    # Buffs are spells that temporarily raise the player's stats during battle. They last until the battle
    # is over, at which point the player's stats will return to normal.
    def __init__(self, name, desc, mana, req_lvl, increase, stat, class_, spell_id):
        super().__init__(name, desc, mana, req_lvl, class_, spell_id)
        self.increase = increase
        self.stat = stat

    def use_magic(self, user, is_battle=True):
        Spell.use_mana(self, user)
        target = user.target

        print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
        print(f"{user.name} is preparing to cast {self.name}...")
        sounds.ability_cast.play()
        main.smart_sleep(0.75)

        if user == target:
            print(f"{user.name} raises their stats using the power of {self.name}!")

        else:
            print(f"{user.name} raises {target.name}'s stats using the power of {self.name}!")

        sounds.buff_spell.play()

        # Temp stats is, as the name suggests, a temporary stat dictionary that is only used in-battle.
        # The dictionary is cleared after every battle and re-created when a new one begins, so that
        # buff spells and other stat increases can be made temporary instead of permanent.
        battle.temp_stats[target.name][self.stat] *= 1 + self.increase
        battle.temp_stats[target.name][self.stat] = math.ceil(battle.temp_stats[user.name][self.stat])
        units.fix_stats()


def pick_cat(user, is_battle=True):
    inv_name = user.name if user != units.player else 'player'

    while True:
        do_continue = False
        print(f"""{user.name}'s spellbook:
      [1] Damaging Spells
      [2] Buff Spells
      [3] Healing Spells""")

        if spellbook[inv_name]['Previous Spell']:
            print(f"      [4] Re-cast {spellbook[inv_name]['Previous Spell'][0].name}")

        spam = True
        while spam:
            cat = main.s_input('Input [#] (or type "exit"): ').lower()

            if cat == '1':
                cat = 'Damaging'

            elif cat == '2':
                cat = 'Buffs'

            elif cat == '3':
                cat = 'Healing'

            elif cat == '4' and spellbook[inv_name]['Previous Spell']:
                spell = spellbook[inv_name]['Previous Spell'][0]
                user.c_spell = spell

                if isinstance(spell, Healing) or isinstance(spell, Buff) or not is_battle:
                    user.choose_target(f"Who should {user.name} cast {spell.name} on?", ally=True, enemy=False)

                else:
                    user.choose_target(f"Who should {user.name} cast {spell.name} on?")

                return True

            else:
                if cat in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*save_load.divider_size)
                    return False

                else:
                    continue

            if do_continue:
                continue

            if not spellbook[inv_name][cat]:
                print('-'*save_load.divider_size)
                print(f'You do not yet have any spells in the {cat} category.')
                print('-'*save_load.divider_size)
                continue

            if pick_spell(cat, user, is_battle):
                return True

            break


def pick_spell(cat, user, is_battle):
    inv_name = user.name if user != units.player else 'player'

    print('-'*save_load.divider_size)
    while True:
        padding = len(max([spell.name for spell in spellbook[inv_name][cat]], key=len))
        print(f"{user.name}'s {cat} Spells | {user.mp}/{user.max_mp} MP remaining")

        # Print the player's spell inventory
        for x, y in enumerate(spellbook[inv_name][cat]):
            print(f"      [{x + 1}] {y.name} --{'-'*(padding - len(y.name))}> {y.mana} MP")

        while True:
            spell = main.s_input('Input [#] (or type "back"): ').lower()

            try:
                spell = spellbook[inv_name][cat][int(spell) - 1]

            except (IndexError, ValueError):
                if spell in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*save_load.divider_size)

                    return False

                continue

            # Of course, you can't cast spells without the required amount of MP
            if spell.mana > user.mp:
                print('-'*save_load.divider_size)
                print(f"{user.name} doesn't have enough MP to cast {spell.name}!")
                main.s_input("\nPress enter/return ")

                break

            spellbook[inv_name]['Previous Spell'] = [spell]

            if is_battle:
                user.c_spell = spell

                if isinstance(spell, Healing) or isinstance(spell, Buff):
                    user.choose_target(f"Who should {user.name} cast {spell.name} on?", ally=True, enemy=False)

                    return True

                else:
                    user.choose_target(f"Who should {user.name} cast {spell.name} on?")

                    return True

            else:
                user.choose_target(f"Who should {user.name} cast {spell.name} on?", ally=True, enemy=False)
                spell.use_magic(user, is_battle)

                break


def new_spells(character):
    # Teach the player new spells as they level up, or low-level spells not previously in the game.
    for spell in all_spells:
        if isinstance(spell, Damaging):
            cat = 'Damaging'
        elif isinstance(spell, Healing) or spell.name == 'Relieve Affliction':
            cat = 'Healing'
        elif isinstance(spell, Buff):
            cat = 'Buffs'
        else:
            continue

        # Only give the character spells that they are a high enough level for
        if character.lvl >= spell.req_lvl:
            for x in spellbook[character.name if character != units.player else 'player'][cat]:
                if x.name == spell.name:
                    break

            else:
                # Almost all spells can be learned by mages, but only a few can be learned by other classes
                if (character.class_ not in spell.class_) and spell.class_:
                    continue

                if not save_load.do_blip:
                    sounds.item_pickup.play()

                spellbook[character.name if character != units.player else 'player'][cat].append(spell)

                main.s_input(f'{character.name} has learned "{spell.name}", a new {cat} spell!')


# -- Damaging Spells -- #
# Neutral
magic_shot = Damaging('Magical Shot', "Hurl a small ball of magical energy at your enemies! (25% Spell Power)",
                      3, 1, 0.25, "neutral", [], "no_elem_1")

magic_burst = Damaging('Magical Burst', "Shatter your enemy with a wave of magical energy! (50% Spell Power)",
                       9, 11, 0.5, "neutral", [], "no_elem_2")

magic_blast = Damaging('Magical Blast', "Annihilate your enemies with a blast of magical energy! (100% Spell Power)",
                       18, 23, 1, "neutral", ['mage'], "no_elem_3")

# Fire
flame_bolt = Damaging('Flame Bolt', "Summon a small fireball to destroy your foes! (25% Spell Power)",
                      3, 2, 0.25, "fire", [], "fire_elem_1")

f_blaze = Damaging('Fierce Blaze', "Summon a powerful flame to destroy your foes! (50% Spell Power)",
                   10, 12, 0.5, "fire", [], "fire_elem_2")

g_infer = Damaging('Grand Inferno', "Unleash a monstrous blaze destroy your foes! (100% Spell Power)",
                   20, 24, 1, "fire", ['mage'], "fire_elem_3")

# Grass
lef_blad = Damaging('Leaf Blade', "Summon razor-sharp blades of grass to destroy your foes! (25% Spell Power)",
                    3, 2, 0.25, "grass", [], "grass_elem_1")

gra_gren = Damaging('Grass Grenade', "Summon a small explosion to destroy your foes! (50% Spell Power)",
                    10, 12, 0.5, "grass", [], "grass_elem_2")

vin_strm = Damaging('Vine Storm', "Unleash a frenzy of powerful vines to destroy your foes! (100% Spell Power)",
                    20, 24, 1, "grass", ['mage'], "grass_elem_3")

# Electricity
spark = Damaging('Spark', "Summon a small spark to destroy your foes! (25% Spell Power)",
                 3, 3, 0.25, "electric", [], "elec_elem_1")

pwr_jolt = Damaging('Powerful Jolt', "Summon a powerful jolt of energy to destroy your foes! (50% Spell Power)",
                    10, 13, 0.5, "electric", [], "elec_elem_2")

sp_storm = Damaging('Superior Storm', "Unleash a devastating lightning storm to destroy your foes! (100% Spell Power)",
                    20, 25, 1, "electric", ['mage'], "elec_elem_3")

# Water
drizzle = Damaging('Drizzle', "Summon a small to destroy your foes! (25% Spell Power)",
                   3, 3, 0.25, "water", [], "water_elem_1")

wtr_blast = Damaging('Water Blast', "Summon a large burst of water to destroy your foes! (50% Spell Power)",
                     10, 13, 0.5, "water", [], "water_elem_2")

tsunami = Damaging('Tsunami', "Unleash a terrifying barrage of waves upon your foes! (100% Spell Power)",
                   20, 25, 1, "water", ['mage'], "water_elem_3")

# Earth
mud_toss = Damaging('Mud Toss', "Summon a small ball of mud to throw at your foes! (25% Spell Power)",
                    3, 4, 0.25, "earth", [], "earth_elem_1")

rock_slam = Damaging('Rock Slam', "Crush your enemies under a layer of solid rock! (50% Spell Power)",
                     10, 13, 0.5, "earth", [], "earth_elem_2")

earthquake = Damaging("Earthquake", "Wreck havoc on your enemies with a powerful earthquake! (100% Spell Power)",
                      20, 25, 1, "earth", ['mage'], "earth_elem_3")

# Ice
icicle_dagger = Damaging('Icicle Dagger', "Hurl a volley of supercooled icicles at your enemies! (25% Spell Power)",
                         3, 4, 0.25, "ice", [], "ice_elem_1")

hail_storm = Damaging('Hailstorm', "Rain ice upon your enemies with unrelenting force! (50% Spell Power)",
                      11, 14, 0.5, 'ice', [], "ice_elem_2")

blizzard = Damaging('Blizzard', "Devastate your enemies with a terrifying flurry of ice and wind! (100% Spell Power)",
                    23, 26, 1, 'ice', ['mage'], "ice_elem_3")

# Wind
m_gust = Damaging('Minor Gust', "Batter your enemies with powerful gusts and winds! (25% Spell Power)",
                  3, 4, 0.25, "wind", [], "wind_elem_1")

microburst = Damaging('Microburst',
                      "Decimate your foes with a powerful blast of wind! (50% Spell Power)",
                      11, 14, 0.5, "wind", [], "wind_elem_2")
cyclone = Damaging('Cyclone',
                   "Demolish all that stand in your path with a terrifying tornado! (100% Spell Power)",
                   23, 26, 1, "wind", ['mage'], "wind_elem_3")

# Light
purify = Damaging('Purify', "Call upon His Divinity to cast out evil creatures! (25% Spell Power)!",
                  3, 5, 0.25, "light", [], "light_elem_1")
smite = Damaging('Holy Smite', "Strike down unholy beings using His Divinity's power! (50% Spell Power)",
                 11, 15, 0.5, "light", [], "light_elem_2")
moonbeam = Damaging('Moonbeam', "Utterly destroy evil creatures with holy rays from the moon! (100% Spell Power)",
                    23, 27, 1, "light", ('paladin', 'mage'), "light_elem_3")


# Dark
curse = Damaging('Evil Curse', "Call upon His Wickedness to harm holy creatures! (25% Spell Power)",
                 3, 5, 0.25, "dark", [], "dark_elem_1")
desecration = Damaging('Desecration', "Defile holy spirits with an evil aura! (50% Spell Power)",
                       11, 15, 0.5, "dark", [], "dark_elem_2")
unholy_rend = Damaging('Unholy Rend', "Annihilate holy creatures with a sundering blow! (100% Spell Power)",
                       23, 27, 1, "dark", ['mage'], "dark_elem_3")

# -- Healing -- #
# Every character starts with this spell
pit_heal = Healing('Novice Healing', """\
Restore a small amount of an ally's HP using holy magic. Heals 10 HP or 5% of
the target's max HP, whichever is greater [5% Healing Power].""",
                   2, 1, 10, 0.05, [], "healing_1")

# The Paladin also starts with this spell
min_heal = Healing('Adept Healing', """\
Restore a moderate amount of an ally's HP using holy magic. Heals 25 HP or 20%
of the target's max HP, whichever is greater [20% Healing Power].""",
                   5, 3, 25, 0.2, [], "healing_2")

# This tier and up can only be learned by Paladins and Mages
adv_heal = Healing('Advanced Healing', """\
Restore a large amount of an ally's HP using holy magic. Heals 70 HP or 50%
of the target's max HP, whichever is greater [50% Healing Power].""",
                   10, 15, 70, 0.5, ('paladin', 'mage'), "healing_3")

div_heal = Healing('Divine Healing', """\
Restore a very large amount of an ally's HP using holy magic. Heals 125 HP or
75% of the target's max HP, whichever is greater [75% Healing Power].""",
                   25, 28, 125, 0.75, ('paladin', 'mage'), "healing_4")

# -- Buffs -- #

# Movement Buffs
m_quick = Buff('Minor Quickness', """\
Raise an ally's speed by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 1, 0.15, "spd", [], "speed_1")

m_evade = Buff('Minor Evade', """\
Raise an ally's evasion by 15%. Stacks with multiple uses. Lasts until the end
of battle. Note: Evasion has a cap of 256 (50% chance to dodge).""",
               3, 1, 0.15, "evad", [], "evad_1")

a_quick = Buff('Adept Quickness', """\
Raise an ally's speed by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 10, 0.3, "spd", ('mage', 'monk'), "speed_2")

a_evade = Buff('Adept Evade', """\
Raise an ally's evasion by 30%. Stacks with multiple uses. Lasts until the end
of battle. Note: Evasion has a cap of 256 (50% chance to dodge).""",
               6, 10, 0.3, "evad", ('mage', 'monk'), "evad_2")

# Defense Buffs
m_defend = Buff('Minor Defend', """\
Raise an ally's Physical Defense by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 3, 0.15, "dfns", [], "defend_1")

m_shield = Buff('Minor Shield', """\
Raise an ally's Magical Defense by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 5, 0.15, "m_dfns", [], "shield_1")

m_block = Buff('Minor Block', """\
Raise an ally's Pierce Defense by 15%. Stacks with multiple uses. Lasts until
the end of battle.""", 3, 7, 0.15, "p_dfns", [], "block_1")

a_defend = Buff('Adept Defend', """\
Raise an ally's Physical Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 14, 0.3, "dfns", ('mage', 'monk'), "defend_2")

a_shield = Buff('Adept Shield', """\
Raise an ally's Magical Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 16, 0.3, "m_dfns", ('mage', 'monk'), "shield_2")

a_block = Buff('Adept Block', """\
Raise an ally's Pierce Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 18, 0.3, "p_dfns", ('mage', 'monk'), "block_2")

# Attack Buffs
m_stren = Buff('Minor Strengthen', """\
Raise an ally's Physical Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 2, 0.15, "attk", [], "strength_1")

m_power = Buff('Minor Empower', """\
Raise an ally's Magical Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 4, 0.15, "m_attk", [], "power_1")

m_aim = Buff('Minor Aim', """\
Raise an ally's Pierce Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.""", 3, 6, 0.15, "p_attk", [], "aim_1")

a_stren = Buff('Adept Strengthen', """\
Raise an ally's Physical Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 13, 0.3, "attk", ('mage', 'monk'), "strength_2")

a_power = Buff('Adept Empower', """\
Raise an ally's Magical Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 15, 0.3, "m_attk", ('mage', 'monk'), "power_2")

a_aim = Buff('Adept Aim', """\
Raise an ally's Pierce Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.""", 6, 17, 0.3, "p_attk", ('mage', 'monk'), "aim_2")

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

    'Chili': {
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
    },

    "Storm": {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
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
                j_spellbook[user][cat].append(spell.spell_id)

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

            for spell_id in j_spellbook[user][category]:
                norm_sb[user][category].append(find_spell_with_id(spell_id))

    spellbook = norm_sb


def find_spell_with_id(spell_id):
    for x in all_spells:
        if x.spell_id == spell_id:
            return x

    return False


for item1 in copy.copy(globals()):
    if isinstance(globals()[item1], Spell) and globals()[item1] not in all_spells:
        print(f"{globals()[item1].spell_id} not in all_spells!")

for item2 in all_spells:
    if find_spell_with_id(item2.spell_id) != item2:
        print(f"{item2.spell_id} doesn't have a unique spell_id!")
