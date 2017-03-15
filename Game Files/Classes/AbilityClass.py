import math
import sys

import ascii_art
import battle
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


# Abilites are similar to magic, except they are tied to classes and are level-independent. They also
# cost Action Points to use instead of Mana, and tend to have much more specific functions.
class Ability:
    def __init__(self, name, desc, ap_cost):
        self.name = name
        self.desc = desc
        self.ap_cost = ap_cost

    def before_ability(self, user):
        # Used to set up variables for abilities
        pass

    def use_ability(self, user):
        pass


# 19 of 30 designed
# 3 of 30 implemented

# -- WARRIOR ABILITES, scales with Strength -- #
def before_parry(user):
    pass


def use_parry(user):
    pass


parry = Ability("Parry", f"""\
The user will move last this turn. If they are attacked, they will take no
damage and will reflect {ascii_art.colorize('[50 + Strength]', 'red')}% of the damage to the attacker.""", 5)
parry.before_ability = before_parry
parry.use_ability = use_parry


def before_roll_call(user):
    pass


def use_roll_call(user):
    pass


roll_call = Ability("Roll Call", f"""\
The user rally's their allies to fight, causing the physical defense of each
one to increase by {ascii_art.colorize('[(5 + Strength) x Number of allies]', 'red')}.""", 5)
roll_call.before_ability = before_roll_call
roll_call.use_ability = use_roll_call


# -- MONK ABILITIES, scales with Constitution -- #
def before_chakra_smash(user):
    pass


def use_chakra_smash(user):
    # A 2.5x crit that lowers the target's armor

    main.smart_sleep(0.75)
    dam_dealt = math.ceil(units.deal_damage(user, user.target, "physical")*2.5)
    user.target.hp -= dam_dealt

    print(f'The attack deals {dam_dealt} damage to the {user.target.name}!')

    user.target.dfns -= 5 + user.attributes['con']
    user.target.p_dfns -= 5 + user.attributes['con']
    user.target.m_dfns -= 5 + user.attributes['con']

    user.target.dfns = math.ceil(user.target.dfns)
    user.target.p_dfns = math.ceil(user.target.p_dfns)
    user.target.m_dfns = math.ceil(user.target.m_dfns)

    return True


chakra_smash = Ability("Chakra Smash", f"""\
Deals a 2.5x critical strike to the enemy, lowering their defensive stats
by {ascii_art.colorize('[5 + Constitution]', 'magenta')}. The armor reduction lasts indefinitely and stacks
with multiple uses.""", 5)
chakra_smash.before_ability = before_chakra_smash
chakra_smash.use_ability = use_chakra_smash


def before_pressure_point(user):
    pass


def use_pressure_point(user):
    pass


pressure_point = Ability("Pressure Point", f"""\
The user identifies the target's weak spots, causing all attacks on the
target enemy to be critical strikes for the next two turns. Also increases
max HP by {ascii_art.colorize('[1 + Constitution]', 'magenta')}%. Does not increase current HP. Stacks with
multiple uses.""", 5)
pressure_point.before_ability = before_pressure_point
pressure_point.use_ability = use_pressure_point


def before_aura_swap(user):
    pass


def use_aura_swap(user):
    pass


aura_swap = Ability("Aura Swap", f"""\
The user selects two targets and swaps their HP values. Can be used on both
allies and enemies, and can swap between both allies and enemies. For every
10% of maximum HP that this alters, the user's evasion goes up by
{ascii_art.colorize('[5 + Constitution]', 'magenta')}. Stacks with multiple uses. Evasion has a cap of 256.""", 5)
aura_swap.before_ability = before_aura_swap
aura_swap.use_ability = use_aura_swap


def before_berserkers_rage(user):
    pass


def use_berserkers_rage(user):
    pass


berserkers_rage = Ability("Berserker's Rage", f"""\
The user realigns their chakras, converting their own pain into an offensive
weapon. Deals 5 damage, with an additional 1% of the target's maximum HP added
for every 1% of HP the user is missing. If the user's current HP is below
[5 + 0.5*Constitution]%, this ability will lifesteal for 25% of the damage
dealt.""", 5)
berserkers_rage.before_ability = before_berserkers_rage
berserkers_rage.use_ability = use_berserkers_rage


# -- ASSASSIN ABILITIES, scales with Dexterity -- #
def before_inject_poison(user):
    pass


def use_inject_poison(user):
    pass


inject_poison = Ability("Inject Poison", f"""\
Injects a poison into the enemy target that deals {ascii_art.colorize('[2 + Dexterity]', 'green')} magical
damage per turn. Stacks with multiple uses, with each stack increasing damage
dealt per turn by 2.""", 5)
inject_poison.before_ability = before_inject_poison
inject_poison.use_ability = use_inject_poison


def before_backstab(user):
    pass


def use_backstab(user):
    pass


backstab = Ability("Backstab", f"""\
The user sneaks up on their opponent and deals a {ascii_art.colorize('[125 + Dexterity]', 'green')}% critical
strike. This move has increased priority and will always go first.""", 2)
backstab.before_ability = before_backstab
backstab.use_ability = use_backstab


# -- MAGE ABILITIES, scales with Intelligence -- #
def before_skill_shot(user):
    pass


def use_skill_shot(user):
    pass


skill_shot = Ability("Skill Shot", f"""\
The user launches a splash-damage attack at the enemy team equal to 50% of the
sum of their levels. If the user is higher level than the highest-levelled
opponent, Skill Shot does {ascii_art.colorize('[50 + Intelligence]', 'blue')}% more damage.""", 2)
skill_shot.before_ability = before_skill_shot
skill_shot.use_ability = use_skill_shot


def before_polymorph(user):
    pass


def use_polymorph(user):
    pass


polymorph = Ability("Polymorph", f"""\
Turns the enemy unit into a harmless frog for one turn, silencing them and
reducing their attack stats, speed, and evasion to 0. The user's magic attack
is also increased by {ascii_art.colorize('[5 + Intelligence]', 'blue')}. Stacks with multiple uses.""", 5)
polymorph.before_ability = before_polymorph
polymorph.use_ability = use_polymorph


def before_spell_shield(user):
    pass


def use_spell_shield(user):
    pass


spell_shield = Ability("Spell Shield", f"""\
Places a protective barrier around your party that lowers incoming magical
damage by {ascii_art.colorize('[20 + Intelligence]', 'blue')}% for 4 turns. Does not stack with multiple
uses - repeat uses only refresh the buff duration.""", 5)
spell_shield.before_ability = before_spell_shield
spell_shield.use_ability = use_spell_shield


def before_mana_drain(user):
    pass


def use_mana_drain(user):
    pass


mana_drain = Ability("Mana Drain", f"""\
Depletes the target's current mana by {ascii_art.colorize('[5 + Intelligence]', 'blue')}% of their maximum
mana pool, while restoring the same amount to the user.""", 5)
mana_drain.before_ability = before_mana_drain
mana_drain.use_ability = use_mana_drain


# -- RANGER ABILITIES, scales with Perception -- #
def before_roll(user):
    pass


def use_roll(user):
    pass


roll = Ability("Roll", f"""\
The user does a quick tuck-and-roll, disorienting the enemy and increasing
the user's evasion to 256 for one turn. Also increases their speed by
{ascii_art.colorize('[25 + Perception]', 'cyan')}. Stacks with multiple uses.""", 3)
roll.before_ability = before_roll
roll.use_ability = use_roll


def before_scout(user):
    monster_weakness = {'fire': 'Water',
                        'water': 'Electric',
                        'electric': 'Earth',
                        'earth': 'Wind',
                        'wind': 'Grass',
                        'grass': 'Ice',
                        'ice': 'Fire',
                        'none': 'None',
                        'light': 'Dark',
                        'dark': 'Light'}[user.target.element]

    print(f"""{user.target.name.upper()}'s STATS:
Attack: {user.target.attk} | M. Attack: {user.target.m_attk} | P. Attack: {user.target.p_attk}
Defense: {user.target.dfns} | M. Defense: {user.target.m_dfns} | P. Defense: {user.target.p_dfns}
Evasion: {user.target.evad} | Speed: {user.target.spd,}
Element: {user.target.element.title()} | Elemental Weakness: {monster_weakness}""")

    battle.temp_stats[user.name]['p_attack'] += (5 + user.attributes['per'])


def use_scout(user):
    pass


scout = Ability("Scout", f"""\
Scouts the enemy, revealing their stats and elemental weakness. Also increases
Pierce attack by {ascii_art.colorize('[5 + Perception]', 'cyan')}%. Stacks with multiple uses.""", 1)
scout.before_ability = before_scout
scout.use_ability = use_scout


# -- PALADIN ABILITIES, scales with Wisdom -- #
def before_tip_the_scales(user):
    pass


def use_tip_the_scales(user):
    pass


tip_the_scales = Ability("Tip the Scales", f"""\
The user and their allies are healed for {ascii_art.colorize('[15 + Wisdom]', 'yellow')} HP each, while dealing
the same in magical damage to the enemy.""", 5)
tip_the_scales.before_ability = before_tip_the_scales
tip_the_scales.use_ability = use_tip_the_scales


def before_unholy_binds(user):
    user.target.element = "dark"
    user.mana += (5 + user.attributes['wis'])


def use_unholy_binds(user):
    pass


unholy_binds = Ability("Unholy Binds", f"""\
Sets the enemy's element to Darkness, causing Light spells to deal more
damage to it. Also restores {ascii_art.colorize('[5 + Wisdom]', 'yellow')} mana.""", 5)
unholy_binds.before_ability = before_unholy_binds
unholy_binds.use_ability = use_unholy_binds


def before_judgement(user):
    pass


def use_judgement(user):
    pass


judgement = Ability("Judgement", f"""\
Applies a DOOM to the target, guaranteeing their death in 7 turns. If the target
dies before the 7 turns is up, the one who dealt the killing blow restores
{ascii_art.colorize('[10 + Wisdom]', 'yellow')} HP.""", 5)
judgement.before_ability = before_judgement
judgement.use_ability = use_judgement


def before_canonize(user):
    pass


def use_canonize(user):
    pass


canonize = Ability("Canonize", f"""\
Declares the target ally a holy figure, converting their defensive element to
Light and causing all enemy light and dark magic casted on them to heal for
{ascii_art.colorize('[25 + Wisdom]', 'yellow')}% HP instead of damaging. Lasts 2 turns. Does not stack with
 multiple uses - repeat uses only refresh the buff duration.""", 5)
canonize.before_ability = before_canonize
canonize.use_ability = use_canonize


# --ULTIMATE ABILITIES-- Unique to each party member and do not scale with attributes
def before_ascend(user):
    pass


def use_ascend(user):
    pass

ascend = Ability("Ascend", """\
ULTIMATE ABILITY: The user ascends to a higher plane of being, raising their
main attribute by 25% + [10% per turn since the battle started]. Caps at 75%.
Can only be used once per battle, and therefore does not stack with multiple
uses.""", 0)
ascend.before_ability = before_ascend
ascend.use_ability = use_ascend

class_abilities = {
    'paladin': [tip_the_scales, unholy_binds, judgement, canonize],  # Designed
    'mage': [mana_drain, polymorph, spell_shield, skill_shot],       # Designed
    'warrior': [roll_call, parry],
    'assassin': [inject_poison, backstab],
    'ranger': [scout, roll],
    'monk': [chakra_smash, pressure_point, aura_swap, berserkers_rage],  # Designed

    'player': [ascend],  # Designed
    'solou': [],
    'ran_af': [],
    'chyme': [],
    'parsto': [],
    'xoann': [],
    'adorine': []

}

# print(sum(len(x) for x in class_abilities.values()))
# for x in class_abilities.values():
#     for y in x:
#         print(y.desc)
#         input()
