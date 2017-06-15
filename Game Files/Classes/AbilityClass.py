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


# -- WARRIOR ABILITES, scales with Strength -- #
def before_parry(user):
    pass


def use_parry(user):
    pass


parry = Ability("Parry", f"""\
The user readies themselves for an enemy attack. If they are attacked during
the next turn, they will take no damage  damage and will reflect
{ascii_art.colorize('[75 + Strength]', 'red')}% of the damage they would have taken to the attacker.""", 5)
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


def before_great_cleave(user):
    pass


def use_great_cleave(user):
    pass


great_cleave = Ability("Great Cleave", f"""\
The user deals a 1.25x critical strike to an enemy unit. If this attack
results in that unit's death, the user gets to target an random additional unit
for a second attack that deals {ascii_art.colorize('[150 + Strength]% damage', 'red')}.""", 2)
great_cleave.before_ability = before_great_cleave
great_cleave.use_ability = use_great_cleave


def before_berserkers_rage(user):
    pass


def use_berserkers_rage(user):
    pass


berserkers_rage = Ability("Berserker's Rage", f"""\
The user goes into a frenzy, discarding their defensive training and focusing
their might on destroying an target enemy. Increases speed, damage dealt, and
damage taken all by {ascii_art.colorize('[15 + Strength]', 'red')}% for 3 turns. Applies to damage from ALL
sources, including physical and magical damage. Does not stack with multiple
uses - repeat uses only refresh the buff duration.""", 2)
berserkers_rage.before_ability = before_berserkers_rage
berserkers_rage.use_ability = use_berserkers_rage


# -- MONK ABILITIES, scales with Constitution -- #
def before_chakra_smash(user):
    pass


def use_chakra_smash(user):
    # A 2x crit that lowers the target's armor

    main.smart_sleep(0.75)
    dam_dealt = math.ceil(units.deal_damage(user, user.target, "physical")*2)
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
Deals a 2x critical strike to a target enemy, lowering their defensive stats
by {ascii_art.colorize('[5 + Constitution]', 'magenta')}. The armor reduction lasts indefinitely and stacks
with multiple uses.""", 5)
chakra_smash.before_ability = before_chakra_smash
chakra_smash.use_ability = use_chakra_smash


def before_shared_experience(user):
    pass


def use_shared_experience(user):
    pass


shared_experience = Ability("Shared Experience", f"""\
The user disregards any sense of good judgement they had, throwing themself
wrecklessly at a target enemy. Deals {ascii_art.colorize('[25 + Constitution]', 'magenta')}% of the target's
current HP in magical damage, while also damaging the user for half the value.
The self-damage is non-lethal, meaning that the user cannot die from it.""", 5)
shared_experience.before_ability = before_shared_experience
shared_experience.use_ability = use_shared_experience


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


def before_breaking_vows(user):
    pass


def use_breaking_vows(user):
    pass


breaking_vows = Ability("Breaking Vows", f"""\
The user realigns their chakras, converting their own pain into an offensive
weapon. Deals 5 damage, with an additional 1% of the target's maximum HP added
for every 1% of HP the user is missing. If the user's current HP is below
25%, this ability will lifesteal for {ascii_art.colorize('[10 + Constitution]', 'magenta')}% of the damage
dealt.""", 5)
breaking_vows.before_ability = before_breaking_vows
breaking_vows.use_ability = use_breaking_vows


# -- ASSASSIN ABILITIES, scales with Dexterity -- #
def before_inject_poison(user):
    pass


def use_inject_poison(user):
    pass


inject_poison = Ability("Inject Poison", f"""\
Injects a poison into a target enemy that deals {ascii_art.colorize('[2 + Dexterity]', 'green')} magical
damage per turn. Stacks with multiple uses, with each stack increasing damage
dealt per turn by 2% of the target's maximum HP.""", 5)
inject_poison.before_ability = before_inject_poison
inject_poison.use_ability = use_inject_poison


def before_backstab(user):
    pass


def use_backstab(user):
    pass


backstab = Ability("Backstab", f"""\
The user sneaks up on their opponent and deals a {ascii_art.colorize('[125 + Dexterity]', 'green')}% critical
strike. If the target was previously affected by Inject Poison, the user's
weapon will become poisoned, causing it to apply one stack of Inject Poison on
every attack for the remainder of the battle. The weapon's poison cannot be
buffed through repeat uses.""", 2)
backstab.before_ability = before_backstab
backstab.use_ability = use_backstab


def before_knockout_gas(user):
    pass


def use_knockout_gas(user):
    pass


knockout_gas = Ability("Knockout Gas", f"""\
The user sneaks behind a target enemy and applies knockout gas to them,
putting them to sleep. The sleep lasts for {ascii_art.colorize('[Dexterity/25]', 'green')} turns, with
a minimum of 1 turn and a maximum of 8. The target has a 5% chance of randomly
waking up each turn, and is guaranteed to wake up when the timer runs out.
Does not stack with multiple uses - repeat uses only refresh the sleep duration.""", 2)
knockout_gas.before_ability = before_knockout_gas
knockout_gas.use_ability = use_knockout_gas


def before_disarming_blow(user):
    pass


def use_disarming_blow(user):
    pass


disarming_blow = Ability("Disarming Blow", f"""\
The user knocks the weapon out of a target enemy's hands, taking it for
themselves. Deals 10 damage, and lowers enemy physical attack by
[5 + Dexterity]%. Has a 25% chance to add the target's weapon to the user's party
inventory. The weapon has attack stats equal to 75% the user's currently
equipped weapon, and has a resell value equal to the target's level. Can only
be used once per enemy per battle. Damage reduction is halved against bosses. """, 2)
disarming_blow.before_ability = before_disarming_blow
disarming_blow.use_ability = use_disarming_blow


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
Turns a target enemy into a harmless frog for one turn, silencing them and
reducing their attack stats, speed, and evasion to 0. If multiple enemies are
alive on the field, this spell has a {ascii_art.colorize('[25 + Intelligence]', 'blue')}% chance of affecting a
random second target, and a [5 + Intelligence]% chance of affecting a third.""", 5)
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
The user does a quick tuck-and-roll, disorienting the enemy team and dodging all
attacks for one turn. Also increases their speed by {ascii_art.colorize('[25 + Perception]', 'cyan')}.
Stacks with multiple uses.""", 3)
roll.before_ability = before_roll
roll.use_ability = use_roll


def before_scout(user):
    pass


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


scout = Ability("Scout", f"""\
Scouts a target enemy, revealing their stats and elemental weakness. In addition,
all attacks on this type of enemy - including in future battles - will have
an additional {ascii_art.colorize('[5 + Perception]', 'cyan')}% chance to be a critical strike, with a maximum
of 25%. Base critical strike chance is 15%. Casting this on an enemy that has
already been scouted in the past will not increase the critical strike bonus.""", 1)
scout.before_ability = before_scout
scout.use_ability = use_scout


def before_powershot(user):
    pass


def use_powershot(user):
    pass


powershot = Ability("Powershot", f"""\
The user channels the power of the wind, firing an single absurdly powerful
arrow. Deals {ascii_art.colorize('[175 + Perception]', 'cyan')}% attack damgage to the chosen target, as well
as all units next to them. The user is disabled for one turn after using this
ability, unable to use abilities, magic, or attacks.""", 2)
powershot.before_ability = before_powershot
powershot.use_ability = use_powershot


def before_unstable_footing(user):
    pass


def use_unstable_footing(user):
    pass


unstable_footing = Ability("Unstable Footing", f"""\
The user takes advantage of the uneven terrain and trips a target enemy.
Deals {ascii_art.colorize('[10 + Perception]', 'cyan')} damage. If the target has not yet moved this turn,
their turn is skipped. The target is also guaranteed to go last next turn.""", 2)
unstable_footing.before_ability = before_unstable_footing
unstable_footing.use_ability = use_unstable_footing


# -- PALADIN ABILITIES, scales with Wisdom -- #
def before_tip_the_scales(user):
    pass


def use_tip_the_scales(user):
    pass


tip_the_scales = Ability("Tip the Scales", f"""\
The user tips the scales in their favor, causing them and their allies to be
healed for {ascii_art.colorize('[5% of Maximum HP + Wisdom]', 'yellow')} HP each, while dealing the same in
magical damage to each member of the enemy team.""", 5)
tip_the_scales.before_ability = before_tip_the_scales
tip_the_scales.use_ability = use_tip_the_scales


def before_unholy_binds(user):
    pass


def use_unholy_binds(user):
    pass


unholy_binds = Ability("Unholy Binds", f"""\
Sets a target enemy's defensive element to Darkness, causing Light spells to
deal more damage to it. If the target already has Darkness as their element,
then Unholy Binds has a {ascii_art.colorize('[10 + Wisdom]', 'yellow')}% chance of instantly killing the target,
with a maximum of 50%. The instant-kill effect does not work on Bosses.""", 5)
unholy_binds.before_ability = before_unholy_binds
unholy_binds.use_ability = use_unholy_binds


def before_judgement(user):
    pass


def use_judgement(user):
    pass


judgement = Ability("Judgement", f"""\
Applies a DOOM to the target, guaranteeing their death in 7 turns. If the
chosen target was affected by Unholy Binds when this spell was cast, then
the 7 turns will be lowered by {ascii_art.colorize('[15 + Wisdom]', 'yellow')}%, with a minimum of 2 turns.
When cast on bosses, the turn count is always 10 turns. Re-casting this spell
has no effect, unless re-casting it would cause the timer to be lower.""", 5)
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
ULTIMATE ABILITY: The Hero ascends to a higher plane of being, raising their
main attribute by 25% + [10% per turn since the battle started]. Caps at 75%.
Can only be used once per battle, and therefore does not stack with multiple
uses.""", 5)
ascend.before_ability = before_ascend
ascend.use_ability = use_ascend


def before_infusion(user):
    pass


def use_infusion(user):
    pass


infusion = Ability("Infusion", """\
ULTIMATE ABILITY: Solou chooses a party member and enchants their weapon with
an element of her choice, while also causing it to deal an additional 10%
damage. Optionally, Solou can instead choose "random", causing a random element
to be selected and raising the damage buff to 20%. Can be re-casted to change
the chosen element, but the damage buff does not stack.""", 2)
infusion.before_ability = before_infusion
infusion.use_ability = use_infusion

class_abilities = {
    'paladin': [tip_the_scales, unholy_binds, judgement, canonize],
    'mage': [mana_drain, polymorph, spell_shield, skill_shot],
    'warrior': [roll_call, parry, great_cleave, berserkers_rage],
    'assassin': [inject_poison, backstab, knockout_gas, disarming_blow],
    'ranger': [scout, roll, powershot, unstable_footing],
    'monk': [chakra_smash, shared_experience, aura_swap, breaking_vows],

    'player': [ascend],
    'solou': [infusion],
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
#         main.s_input()
