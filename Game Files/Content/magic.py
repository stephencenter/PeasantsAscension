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

import json
import math
import random
import sys

import pygame

import ascii_art
import battle
import sounds
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# This is the message that is printed if you attempt to use magic
# without the required amount of mana.
out_of_mana = "-------------------------\n{0} doesn't have enough mana to cast {1}."


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
        Spell.use_mana(self, user)
        target = user.target

        # Healing spells will always restore a minimum of user.hp*thresh.
        # e.g. A spell that heals 20 HP but has a 20% threshold will restore 20 HP for someone
        # with 45 max HP, but will restore 32 HP for someone with 160 max HP.
        # In addition to this, the user restores an additional 2*Wisdom, unless they are a
        # Paladin in which case it it 4*Wisdom.
        if self.health < target.hp*self.thresh:
            if user.class_ == 'paladin':
                total_heal = target.hp*self.thresh + 4*user.attributes['wis']

            else:
                total_heal = 2*user.attributes['wis']

        else:
            if user.class_ == 'paladin':
                total_heal = self.health + 4*user.attributes['wis']

            else:
                total_heal = self.health + 2*user.attributes['wis']

        target.hp += total_heal

        if target.hp > target.max_hp:
            target.hp -= (target.hp - target.max_hp)

        target.hp = math.ceil(target.hp)

        sounds.magic_healing.play()

        if is_battle:
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
            print(f'Using "{self.name}", {target.name} is healed by {total_heal} HP!')

        else:
            print('-'*25)
            print(f'Using "{self.name}", {target.name} is healed by {total_heal} HP!')
            input("\nPress enter/return ")
            print('-'*25)


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
        Spell.use_mana(self, user)
        target = user.target

        print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
        print(f'{user.name} attempts to summon a powerful spell...')

        sounds.magic_attack.play()
        main.smart_sleep(0.75)
        dam_dealt = units.deal_damage(user, target, "magical", spell_power=self.damage)

        # If the monster's evasion (with a max of 256) is higher than the user's accuracy roll, the spell will land
        if random.randint(1, 512) in range(target.evad, 512):
            sounds.enemy_hit.play()
            target.hp -= dam_dealt
            print(f'Using the power of {self.name}, {user.name} deals {dam_dealt} damage to the {target.monster_name}!')

        else:
            sounds.attack_miss.play()
            print(f"The {target.monster_name} narrowly dodges {user.name}'s spell!")


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
        Spell.use_mana(self, user)
        target = user.target

        print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

        if user == target:
            print(f"{user.name} raises their stats using the power of {self.name}!")

        else:
            print(f"{user.name} raises {target.name}'s stats using the power of {self.name}!")

        sounds.buff_spell.play()

        battle.temp_stats[target.name][self.stat] *= 1 + self.increase
        battle.temp_stats[target.name][self.stat] = math.ceil(battle.temp_stats[user.name][self.stat])
        units.fix_stats()


def pick_cat(user, is_battle=True):
    inv_name = user.name if user != units.player else 'player'

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

                    if is_battle:
                        user.c_spell = spell

                        if isinstance(spell, Healing) or isinstance(spell, Buff):
                            user.choose_target(f"Who should {user.name} cast {spell.name} on?", ally=True, enemy=False)

                            return True

                        else:
                            user.choose_target(f"Who should {user.name} cast {spell.name} on?")

                            break

                    else:
                        user.choose_target(f"Who should {user.name} cast {spell.name} on?", ally=True, enemy=False)
                        spell.use_magic(user, is_battle)

                        break

                else:
                    print('-'*25)
                    print(f'{user.name} has no previously used spells!')
                    input("\nPress enter/return ")
                    print('-'*25)

                    break

            else:
                if cat.lower() in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*25)
                    return False

                else:
                    continue

            if do_continue:
                continue

            if not spellbook[inv_name][cat]:
                print('-'*25)
                print(f'You do not yet have any spells in the {cat} category.')
                print('-'*25)
                continue

            if pick_spell(cat, user, is_battle):
                return True

            break


def pick_spell(cat, user, is_battle):
    inv_name = user.name if user != units.player else 'player'

    print('-'*25)
    while True:
        padding = len(max([spell.name for spell in spellbook[inv_name][cat]], key=len))
        print(f"{cat} Spells [{user.name} has {user.mp} mana remaining]:")

        for x, y in enumerate(spellbook[inv_name][cat]):
            print(f"      [{x + 1}] {y} --{'-'*(padding - len(y.name))}> {y.mana} MP")

        while True:
            spell = input('Input [#] (or type "back"): ').lower()

            try:
                spell = spellbook[inv_name][cat][int(spell) - 1]

            except (ValueError, IndexError):
                if spell in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*25)

                    return False

                continue

            if spell.mana > user.mp:
                print(out_of_mana.format(user.name, spell.name))

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

                input(f'{character.name} has learned "{spell}", a new {cat} spell! | Press enter/return ')

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
