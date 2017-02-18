import math
import sys
import copy

import units
import UnitClass

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


# 8 of 24 designed
# 3 of 24 implemented

# -- WARRIOR ABILITES, scales with Strength -- #
def use_parry(user):
    pass

parry = Ability("Parry", """The user will move last this turn. If they are attacked, they will
take no damage and will reflect [50 + Strength]% damage to the attacker.""", 5)
parry.use_ability = use_parry

warrior_abilities = [parry]


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
by [5 + Constitution]%. The armor reduction lasts indefinitely and stacks
with multiple uses.""", 5)
chakra_smash.use_ability = use_chakra_smash

monk_abilities = [chakra_smash]


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

assassin_abilities = [inject_poison, backstab]

# -- MAGE ABILITIES, scales with Intelligence -- #
mage_abilities = []


# -- RANGER ABILITIES, scales with Perception -- #
def use_roll(user):
    pass


roll = Ability("Roll", """The user does a quick tuck-and-roll, disorienting the enemy and increasing their evasion
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
                        'life': 'Death',
                        'death': 'Life'}[units.monster.element]

    print(f"""{units.monster.name.upper()}'s STATS:
Attack: {units.monster.attk} | M. Attack: {units.monster.m_attk} | P. Attack: {units.monster.p_attk}
Defense: {units.monster.dfns} | M. Defense: {units.monster.m_dfns} | P. Defense: {units.monster.p_dfns}
Evasion: {units.monster.evad} | Speed: {units.monster.spd,}
Element: {units.monster.element.title()} | Elemental Weakness: {monster_weakness}""")


scout = Ability("Scout", """Scouts the enemy, revealing their stats and elemental weakness. Also increases Pierce
attack by [5 + Perception]%. Stacks with multiple uses.""", 1)
scout.use_ability = use_scout

ranger_abilities = [roll, scout]


# -- PALADIN ABILITIES, scales with Wisdom -- #
def use_tip_the_scales(user):
    pass


tip_the_scales = Ability("Tip the Scales", """The user and their allies are healed for [15 + Wisdom] HP each, while
dealing the same in magical damage to the enemy.""", 5)
tip_the_scales.use_ability = use_tip_the_scales


def use_unholy_binds(user):
    units.monster.element = "death"
    user.mana += (5 + user.attributes['wis'])


unholy_binds = Ability("Unholy Binds", """Sets the enemy's element to Death, causing your holy spells to
do more damage. Also restores [5 + Wisdom] mana.""", 5)
unholy_binds.use_ability = use_unholy_binds

paladin_abilities = [tip_the_scales, unholy_binds]