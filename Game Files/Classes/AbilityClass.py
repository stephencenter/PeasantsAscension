import math
# import sys

import ascii_art
# import battle
# import units

# if __name__ == "__main__":
#     sys.exit()
#
# else:
#     main = sys.modules["__main__"]


# Abilites are similar to magic, except they are tied to classes and are level-independent. They also
# cost Action Points to use instead of Mana, and tend to have much more specific functions.
class Ability:
    def __init__(self, name, desc, ap_cost, duration=0, priority=0):
        self.name = name
        self.desc = desc
        self.ap_cost = ap_cost
        self.duration = duration
        self.priortiy = priority

    def use_ability(self, user):
        pass

    def after_turn(self, user):
        pass


# 17 of 24 designed
# 3 of 24 implemented

# -- WARRIOR ABILITES, scales with Strength -- #
def use_parry(user):
    pass


def after_parry(user):
    pass


parry = Ability("Parry", f"""\
The user will move last this turn. If they are attacked, they will take no
damage and will reflect {ascii_art.colorize('[50 + Strength]', 'red')}% of the damage to the attacker.""", 5)
parry.use_ability = use_parry
parry.after_turn = after_parry


def use_roll_call(user):
    pass


def after_roll_call(user):
    pass


roll_call = Ability("Roll Call", f"""\
The user rally's their allies to fight, causing the physical defense of each
one to increase by {ascii_art.colorize('[(5 + Strength) x Number of allies]', 'red')}.""", 5)
roll_call.use_ability = use_roll_call
roll_call.after_turn = after_roll_call


# -- MONK ABILITIES, scales with Constitution -- #
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


def after_chakra_smash(user):
    pass


chakra_smash = Ability("Chakra Smash", f"""\
Deals a 2.5x critical strike to the enemy, lowering their defensive stats
by {ascii_art.colorize('[5 + Constitution]', 'magenta')}. The armor reduction lasts indefinitely and stacks
with multiple uses.""", 5)
chakra_smash.use_ability = use_chakra_smash
chakra_smash.after_turn = after_chakra_smash


def use_pressure_point(user):
    pass


def after_pressure_point(user):
    pass


pressure_point = Ability("Pressure Point", f"""\
The user identifies the target's weak spots, causing all attacks on the
target enemy to be critical strikes for the next two turns. Also increases
max HP by {ascii_art.colorize('[1 + Constitution]', 'magenta')}%. Does not increase current HP. Stacks with
multiple uses.""", 5)
pressure_point.use_ability = use_pressure_point
pressure_point.after_turn = after_pressure_point


def use_aura_swap(user):
    pass


def after_aura_swap(user):
    pass


aura_swap = Ability("Aura Swap", f"""\
The user selects two targets and swaps their HP values. Can be used on both
allies and enemies, and can swap between both allies and enemies. For every
10% of maximum HP that this alters, the user's evasion goes up by
{ascii_art.colorize('[5 + Constitution]', 'magenta')}. Stacks with multiple uses. Evasion has a cap of 256.""", 5)
aura_swap.use_ability = use_aura_swap
aura_swap.after_turn = after_aura_swap


# -- ASSASSIN ABILITIES, scales with Dexterity -- #
def use_inject_poison(user):
    pass


def after_inject_poison(user):
    pass


inject_poison = Ability("Inject Poison", f"""\
Injects a poison into the enemy target that deals {ascii_art.colorize('[2 + Dexterity]', 'green')} magical
damage per turn. Stacks with multiple uses, with each stack increasing damage
dealt per turn by 2.""", 5)
inject_poison.use_ability = use_inject_poison
inject_poison.after_turn = after_inject_poison


def use_backstab(user):
    pass


def after_backstab(user):
    pass


backstab = Ability("Backstab", f"""\
The user sneaks up on their opponent and deals a {ascii_art.colorize('[125 + Dexterity]', 'green')}% critical
strike. This move has increased priority and will always go first.""", 2)
backstab.use_ability = use_backstab
backstab.after_turn = after_backstab


# -- MAGE ABILITIES, scales with Intelligence -- #
def use_skill_shot(user):
    pass


def after_skill_shot(user):
    pass


skill_shot = Ability("Skill Shot", f"""\
The user launches a splash-damage attack at the enemy team equal to the sum of
their levels. If the user is higher level than the highest-levelled opponent,
Skill Shot does {ascii_art.colorize('[50 + Intelligence]', 'blue')}% more damage.""", 2)
skill_shot.use_ability = use_skill_shot
skill_shot.after_turn = after_skill_shot


def use_polymorph(user):
    pass


def after_polymorph(user):
    pass


polymorph = Ability("Polymorph", f"""\
Turns the enemy unit into a harmless frog for one turn, silencing them and
reducing their attack stats, speed, and evasion to 0. The user's magic attack
is also increased by {ascii_art.colorize('[5 + Intelligence]', 'blue')}. Stacks with multiple uses.""", 5)
polymorph.use_ability = use_polymorph
polymorph.after_turn = after_polymorph


def use_spell_shield(user):
    pass


def after_spell_shield(user):
    pass


spell_shield = Ability("Spell Shield", f"""\
Places a protective barrier around your party that lowers incoming magical
damage by {ascii_art.colorize('[20 + Intelligence]', 'blue')}% for 5 turns.""", 5)
spell_shield.use_ability = use_spell_shield
spell_shield.after_turn = after_spell_shield


def use_mana_drain(user):
    pass


def after_mana_drain(user):
    pass


mana_drain = Ability("Mana Drain", f"""\
Depletes the target's current mana by {ascii_art.colorize('[5 + Intelligence]', 'blue')}% of their maximum
mana pool, while restoring the same amount to the user.""", 5)
mana_drain.use_ability = use_mana_drain
mana_drain.after_turn = after_mana_drain


# -- RANGER ABILITIES, scales with Perception -- #
def use_roll(user):
    pass


def after_roll(user):
    pass


roll = Ability("Roll", f"""\
The user does a quick tuck-and-roll, disorienting the enemy and increasing
the user's evasion to 256 for one turn. Also increases their speed by
{ascii_art.colorize('[25 + Perception]', 'cyan')}. Stacks with multiple uses.""", 3)
roll.use_ability = use_roll
roll.after_Turn = after_roll


def use_scout(user):
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


def after_scout(user):
    pass


scout = Ability("Scout", f"""\
Scouts the enemy, revealing their stats and elemental weakness. Also increases
Pierce attack by {ascii_art.colorize('[5 + Perception]', 'cyan')}%. Stacks with multiple uses.""", 1)
scout.use_ability = use_scout
scout.after_turn = after_scout


# -- PALADIN ABILITIES, scales with Wisdom -- #
def use_tip_the_scales(user):
    pass


def after_tip_the_scales(user):
    pass


tip_the_scales = Ability("Tip the Scales", f"""\
The user and their allies are healed for {ascii_art.colorize('[15 + Wisdom]', 'yellow')} HP each, while dealing
the same in magical damage to the enemy.""", 5)
tip_the_scales.use_ability = use_tip_the_scales
tip_the_scales.after_turn = after_tip_the_scales


def use_unholy_binds(user):
    user.target.element = "dark"
    user.mana += (5 + user.attributes['wis'])


def after_unholy_binds(user):
    pass


unholy_binds = Ability("Unholy Binds", f"""\
Sets the enemy's element to Darkness, causing Light spells to deal more
damage to it. Also restores {ascii_art.colorize('[5 + Wisdom]', 'yellow')} mana.""", 5)
unholy_binds.use_ability = use_unholy_binds
unholy_binds.after_turn = after_unholy_binds


def use_judgement(user):
    pass


def after_judgement(user):
    pass


judgement = Ability("Judgement", f"""\
Applies a DOOM to the target, guaranteeing their death in 7 turns. If the target
dies before the 7 turns is up, the one who dealt the killing blow restores
{ascii_art.colorize('[10 + Wisdom]', 'yellow')} HP.""", 5)
judgement.use_ability = use_judgement
judgement.after_turn = after_judgement


def use_canonize(user):
    pass


def after_canonize(user):
    pass


canonize = Ability("Canonize", f"""\
Declares the target ally a holy figure, rendering them immune to physical
damage, converting their element to Light, and causing all offensive light
and dark magic casted on them to heal for {ascii_art.colorize('[50 + Wisdom]', 'yellow')}% HP instead of
damaging. Lasts 2 turns. Does not stack with multiple uses.""", 5)
canonize.use_ability = use_canonize
canonize.after_turn = after_canonize

class_abilities = {
    'paladin': [tip_the_scales, unholy_binds, judgement, canonize],  # Done
    'mage': [mana_drain, polymorph, spell_shield, skill_shot],       # Done
    'warrior': [roll_call, parry],
    'assassin': [inject_poison, backstab],
    'ranger': [scout, roll],
    'monk': [chakra_smash, pressure_point, aura_swap]

}

# print(sum(len(x) for x in class_abilities.values()))
for x in class_abilities.values():
    for y in x:
        print(y.desc)
        input()
