import math
import sys
import copy

import units
import UnitClass
import battle

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

    def use_ability(self, user):
        pass

    def after_turn(self, user):
        pass


# 13 of 24 designed
# 3 of 24 implemented

# -- WARRIOR ABILITES, scales with Strength -- #
def use_parry(user):
    pass

parry = Ability("Parry", """The user will move last this turn. If they are attacked, they will
take no damage and will reflect [50 + Strength]% of the damage to the attacker.""", 5)
parry.use_ability = use_parry


def use_roll_call(user):
    pass


roll_call = Ability("Roll Call", """Each of the user's allies have their physical defense increased by "
[(5 + Strength) x Number of allies]""", 5)
roll_call.use_ability = use_roll_call


# -- MONK ABILITIES, scales with Constitution -- #
def use_chakra_smash(user):
    # A 2.5x crit that lowers the target's armor

    main.smart_sleep(0.75)
    dam_dealt = math.ceil(deal_damage(user, units.monster, "physical")*2.5)
    units.monster.hp -= dam_dealt

    print(f'The attack deals {dam_dealt} damage to the {monster.name}!')

    monster.dfns *= 0.9
    monster.p_dfns *= 0.9
    monster.m_dfns *= 0.9

    monster.dfns = math.ceil(monster.dfns)
    monster.p_dfns = math.ceil(monster.p_dfns)
    monster.m_dfns = math.ceil(monster.m_dfns)

    return True


chakra_smash = Ability("Chakra Smash", """Deals a 2.5x critical strike to the enemy, lowering their defensive stats
by [5 + Constitution]. The armor reduction lasts indefinitely and stacks
with multiple uses.""", 5)
chakra_smash.use_ability = use_chakra_smash


# -- ASSASSIN ABILITIES, scales with Dexterity -- #
def use_inject_poison(user):
    pass


inject_poison = Ability("Inject Poison", """Injects a poison into the enemy target that deals [2 + Dexterity] magical
damage per turn. Stacks with multiple uses, with each stack increasing damage
dealt per turn by 2.""", 5)
inject_poison.use_ability = use_inject_poison


def use_backstab(user):
    pass


backstab = Ability("Backstab", """The user will move first and deal a [125 + Dexterity]% critical strike.""", 2)
backstab.use_ability = use_backstab


# -- MAGE ABILITIES, scales with Intelligence -- #
def use_skill_shot(user):
    pass


skill_shot = Ability("Skill Shot", """Deals damage to the target equal to [User's Level + Target's level].
If the user's level is lower than the enemy's level, the user's mana is restored by [5 + Intelligence].""", 2)
skill_shot.use_ability = use_skill_shot


def use_polymorph(user):
    pass


polymorph = Ability("Polymorph", """Turns the enemy unit into a frog for one turn, reducing their attack
stats, speed, and evasion to 0. The user's magic attack is also increased by
[5 + Intelligence]. Stacks with multiple uses.""", 5)
polymorph.use_ability = use_polymorph


def use_spell_shield(user):
    pass


spell_shield = Ability("Spell Shield", """Places a protective barrier around your party that lowers incoming
magical damage by [20 + Intelligence]% for 5 turns.""", 5)
spell_shield.use_ability = use_spell_shield


# -- RANGER ABILITIES, scales with Perception -- #
def use_roll(user):
    pass


roll = Ability("Roll", """The user does a quick tuck-and-roll, disorienting the enemy and increasing the user's evasion
to 256 for one turn. Also increases their speed by [25 + Perception]. Stacks
with multiple uses.""", 3)
roll.use_ability = use_roll


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
                        'dark': 'Light'}[units.monster.element]

    print(f"""{units.monster.name.upper()}'s STATS:
Attack: {units.monster.attk} | M. Attack: {units.monster.m_attk} | P. Attack: {units.monster.p_attk}
Defense: {units.monster.dfns} | M. Defense: {units.monster.m_dfns} | P. Defense: {units.monster.p_dfns}
Evasion: {units.monster.evad} | Speed: {units.monster.spd,}
Element: {units.monster.element.title()} | Elemental Weakness: {monster_weakness}""")

    battle.temp_stats[user.name]['p_attack'] += (5 + user.attributes['per'])


scout = Ability("Scout", """Scouts the enemy, revealing their stats and elemental weakness. Also increases Pierce
attack by [5 + Perception]%. Stacks with multiple uses.""", 1)
scout.use_ability = use_scout


# -- PALADIN ABILITIES, scales with Wisdom -- #
def use_tip_the_scales(user):
    pass


tip_the_scales = Ability("Tip the Scales", """The user and their allies are healed for [15 + Wisdom] HP each, while
dealing the same in magical damage to the enemy.""", 5)
tip_the_scales.use_ability = use_tip_the_scales


def use_unholy_binds(user):
    units.monster.element = "death"
    user.mana += (5 + user.attributes['wis'])


unholy_binds = Ability("Unholy Binds", """Sets the enemy's element to Darkness, causing your Light spells to
do more damage. Also restores [5 + Wisdom] mana.""", 5)
unholy_binds.use_ability = use_unholy_binds


def use_judgement(user):
    pass


judgement = Ability("Judgement", """Applies DOOM to the target, guaranteeing their death in 7 turns. If the target
dies before the 7 turns is up, the user restores [5 + Wisdom] HP.""", 5)
judgement.use_ability = use_judgement

class_abilities = {
    'paladin': [tip_the_scales, unholy_binds, judgement],
    'mage': [skill_shot, polymorph, spell_shield],
    'warrior': [roll_call, parry],
    'assassin': [inject_poison, backstab],
    'ranger': [scout, roll],
    'monk': [chakra_smash]

}

print(sum(len(x) for x in class_abilities.values()))

