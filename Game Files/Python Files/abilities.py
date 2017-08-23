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

import math
import sys

import units
import sounds
import random
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

    def before_ability(self, user):
        # Used to set up variables for abilities
        pass

    def use_ability(self, user):
        pass


# -- WARRIOR ABILITES, scales with Strength -- #
def before_taunt(user):
    pass


def use_taunt(user):
    for x in battle.m_list:
        x.ability_vars['taunted'] = [battle.turn_counter + 1, user]
        x.status_ail.append("Taunted")

    print(f"{user.name} is preparing to cast Taunt...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    phys = 10 + user.attributes['str']
    other = math.ceil(phys/2)

    battle.temp_stats[user.name]['dfns'] += phys
    battle.temp_stats[user.name]['p_dfns'] += other
    battle.temp_stats[user.name]['m_dfns'] += other

    print(f"{user.name} taunts the enemy team!")
    print(f"{user.name} gains {phys}/{other}/{other} physical/magical/pierce defense!")

taunt = Ability("Taunt", f"""\
The user taunts the enemy team, forcing all enemies to attack him for 1 turn.
The enemies can only use standard attacks while taunted, and cannot cast
spells or defend. Does not go into effect until the current turn is finished.
Provides a bonus [10 + Strength] Physical Defense during this turn, and half 
values for Magical and Pierce Defense.""", 2)
taunt.before_ability = before_taunt
taunt.use_ability = use_taunt


def before_roll_call(user):
    pass


def use_roll_call(user):
    sounds.ability_cast.play()
    print(f"{user.name} begins to motivate their allies with a Roll Call...")
    main.smart_sleep(0.75)

    for pcu in battle.enabled_pcus:
        increase = (battle.temp_stats[user.name]['attributes']['str'] + 5)/len(battle.enabled_pcus)
        increase = max(math.ceil(increase), 5)
        battle.temp_stats[pcu.name]['dfns'] += increase

    print(f"All allies physical defense increased by {increase}!")
    sounds.buff_spell.play()


roll_call = Ability("Roll Call", f"""\
The user rally's their allies to fight, causing the physical defense of each
one to increase by [(5 + Strength)/Number of allies]. Always increases defense
by at least 5. Stacks with multiple uses.""", 3)
roll_call.before_ability = before_roll_call
roll_call.use_ability = use_roll_call


def before_great_cleave(user):
    pass


def use_great_cleave(user):
    pass


great_cleave = Ability("Great Cleave", f"""\
The user deals a 1.25x critical strike to an enemy unit. If this attack
results in that unit's death, the user gets to target an random additional unit
for a second attack that deals [150 + Strength]% damage.""", 2)
great_cleave.before_ability = before_great_cleave
great_cleave.use_ability = use_great_cleave


def before_berserkers_rage(user):
    pass


def use_berserkers_rage(user):
    if user.ability_vars['berserk']:
        values = 0.10

    else:
        values = 0.15 + user.attributes['str']/100

    print(f"{user.name} is preparing to cast Berserker's Rage...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    print(f"Speed and Physical Attack increased by {math.ceil(values*100)}%!")
    print(f"Armor Stats decreased by {math.ceil(values*50)}%!")

    battle.temp_stats[user.name]['spd'] += math.ceil(battle.temp_stats[user.name]['spd']*values)
    battle.temp_stats[user.name]['attk'] += math.ceil(battle.temp_stats[user.name]['spd']*values)
    battle.temp_stats[user.name]['dfns'] -= math.ceil(battle.temp_stats[user.name]['spd']*values/2)
    battle.temp_stats[user.name]['m_dfns'] -= math.ceil(battle.temp_stats[user.name]['spd']*values/2)
    battle.temp_stats[user.name]['p_dfns'] -= math.ceil(battle.temp_stats[user.name]['spd']*values/2)
    user.ability_vars['berserk'] = True


berserkers_rage = Ability("Berserker's Rage", f"""\
The user goes into a frenzy, discarding their defensive training and focusing
their might on destroying a target enemy. Increases speed and physical attack
by [15 + Strength]%, and reduces all three armor stats by the half the value. 
Repeat casts only affect these stats by 10/5% each, with no attribute bonus.""", 2)
berserkers_rage.before_ability = before_berserkers_rage
berserkers_rage.use_ability = use_berserkers_rage


# -- MONK ABILITIES, scales with Constitution -- #
def before_chakra_smash(user):
    user.choose_target(f"Who should {user.name} cast Chakra Smash on?")


def use_chakra_smash(user):
    # A 2x crit that lowers the target's armor
    print(f"{user.name} is preparing a Chakra Smash...")
    sounds.sword_slash.play()
    main.smart_sleep(0.75)

    dam_dealt = math.ceil(units.deal_damage(user, user.target, "physical")*2)
    user.target.hp -= dam_dealt

    armor_lower = 5 + battle.temp_stats[user.name]['attributes']['con']
    user.target.dfns -= armor_lower
    user.target.p_dfns -= armor_lower
    user.target.m_dfns -= armor_lower

    print(f'The attack deals {dam_dealt} damage to the {user.target.name}!')
    print(f"All of {user.target.name}'s defense stats reduced by {armor_lower}!")
    sounds.enemy_hit.play()

    return True


chakra_smash = Ability("Chakra Smash", f"""\
Deals a 2x critical strike to a target enemy, lowering their defensive stats
by [5 + Constitution]. This attack can also crit, which would result in a total
of 3x damage. The armor reduction lasts indefinitely and stacks with multiple 
uses.""", 3)
chakra_smash.before_ability = before_chakra_smash
chakra_smash.use_ability = use_chakra_smash


def before_shared_experience(user):
    pass


def use_shared_experience(user):
    pass


shared_experience = Ability("Shared Experience", f"""\
The user disregards any sense of good judgement they had, throwing themself
wrecklessly at a target enemy. Deals [25 + Constitution]% of the target's
current HP in magical damage, while also damaging the user for half the value.
The self-damage is non-lethal, meaning that the user cannot die from it.""", 3)
shared_experience.before_ability = before_shared_experience
shared_experience.use_ability = use_shared_experience


def before_aura_swap(user):
    pass


def use_aura_swap(user):
    c_enemy = max(battle.m_list, key=lambda x: x.hp)
    c_ally = min([x for x in battle.enabled_pcus if 'dead' not in x.status_ail], key=lambda x: x.hp)

    sounds.ability_cast.play()
    print(f"{user.name} is beginning to cast Aura Swap...")
    main.smart_sleep(0.75)

    if c_enemy.hp <= c_ally.hp:
        print("...But it failed!")
        sounds.debuff.play()

    else:
        sounds.buff_spell.play()
        beginning = [c_enemy.hp, c_ally.hp]

        if isinstance(c_enemy, units.Boss):
            c_ally.hp = c_enemy.hp

        else:
            c_enemy.hp, c_ally.hp = c_ally.hp, c_enemy.hp

        units.fix_stats()

        evad = max(math.floor((c_ally.hp - c_enemy.hp)/5)*(5 + battle.temp_stats[user.name]['attributes']['str']), 5)
        battle.temp_stats[user.name]['evad'] += evad

        print(f"{c_ally.name}'s HP rose from {beginning[1]} to {c_ally.hp}!")

        if isinstance(c_enemy, units.Boss):
            print(f"{c_enemy.name}'s boss aura protected them!")

        else:
            print(f"{c_enemy.name}'s HP dropped from {beginning[0]} to {c_enemy.hp}!")

        print(f"{user.name}'s evasion increased by {evad}!")


aura_swap = Ability("Aura Swap", f"""\
The user swaps the HP values of the highest-hp enemy and the lowest-hp ally.
For every 5 HP that this alters, the user's evasion goes up by 
[5 + Constitution]. Always increases evasion by at least 5. This spell does 
nothing if it would result in the ally losing HP. Cannot be casted on dead 
units. When cast on bosses, the boss's HP is not altered, but the ally's HP 
is. The evasion bonus stacks with multiple uses. Evasion has a cap of 256.""", 3)
aura_swap.before_ability = before_aura_swap
aura_swap.use_ability = use_aura_swap


def before_breaking_vows(user):
    user.choose_target(f"Who should {user.name} cast Breaking Vows on?")


def use_breaking_vows(user):
    hp_missing = (user.max_hp - user.hp)/(user.max_hp*100)
    damage = 5 + math.ceil(hp_missing*user.target.max_hp)
    lifesteal = 0 if hp_missing <= 75 else max((0.1 + user.attributes['con']/100)*damage, 1)

    print(f"{user.name} is preparing to cast Breaking Vows...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    user.target.hp -= damage
    user.hp += lifesteal

    print(f"{user.name}'s Breaking Vows deals {damage} damage to the {user.target.name}!")

    if lifesteal:
        print(f"{user.target.name} lifesteals for {lifesteal} HP!")

breaking_vows = Ability("Breaking Vows", f"""\
The user realigns their chakras, converting their own pain into an offensive
weapon. Deals 5 damage, with an additional 1% of the target's maximum HP added
for every 1% of HP the user is missing. If the user's current HP is below
25%, this ability will lifesteal for [10 + Constitution]% of the damage
dealt.""", 5)
breaking_vows.before_ability = before_breaking_vows
breaking_vows.use_ability = use_breaking_vows


# -- ASSASSIN ABILITIES, scales with Dex terity -- #
def before_inject_poison(user):
    user.choose_target(f"Who should {user.name} inject poison into?")


def use_inject_poison(user):
    user.target.status_ail.append('poisoned')
    user.target.ability_vars['poison_pow'] += 0.02
    user.target.ability_vars['poison_dex'] = 2 + battle.temp_stats[user.name]['attributes']['dex']

    poison_power = math.ceil(100*user.target.ability_vars['poison_pow'] + user.target.ability_vars['poison_dex'])

    print(f"{user.name} is preparing a poison with power {poison_power}...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    print(f"{user.name} injects the poison into the {user.target.name}!")
    sounds.poison_damage.play()
    pass


inject_poison = Ability("Inject Poison", f"""\
Injects a poison into a target enemy that deals [2 + Dexterity] magical
damage per turn. Stacks with multiple uses, with each stack increasing damage
dealt per turn by 2% of the target's maximum HP.""", 2)
inject_poison.before_ability = before_inject_poison
inject_poison.use_ability = use_inject_poison


def before_knockout_gas(user):
    user.choose_target(f"Who should {user.name} cast Knockout Gas on?")


def use_knockout_gas(user):
    print(f"{user.name} is preparing some Knockout Gas for {user.target.name}...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    k_dur = math.ceil(battle.temp_stats[user.name]['attributes']['dex']/25)
    k_dur = min(max(k_dur, 2), 8)
    user.target.ability_vars['knockout_turns'] = k_dur
    user.target.status_ail.append("asleep")

    print(f"{user.target.name} was put to sleep for {k_dur} turns!")
    sounds.poison_damage.play()


knockout_gas = Ability("Knockout Gas", f"""\
The user sneaks behind a target enemy and applies knockout gas to them,
putting them to sleep. The sleep lasts for [Dexterity/25] turns, with
a minimum of 2 turns and a maximum of 8. The target has a 10% chance of randomly
waking up each turn. Bosses have a 25% chance. Does not stack with multiple 
uses - repeat uses only refresh the sleep duration.""", 2)
knockout_gas.before_ability = before_knockout_gas
knockout_gas.use_ability = use_knockout_gas


def before_disarming_blow(user):
    user.choose_target(f"Who should {user.name} disarm?", ally=False, enemy=True)


def use_disarming_blow(user):
    sounds.ability_cast.play()
    print(f"{user.name} is preparing to disarm the {user.target.name}")
    main.smart_sleep(0.75)

    if user.target.ability_vars['disarmed']:
        sounds.debuff.play()
        print(f"But the {user.target.name} is already disarmed!")
        return

    print(f"The {user.target.name} drops their weapon, lowering their attack!")
    sounds.buff_spell.play()

    user.target.ability_vars['disarmed'] = True
    user.target.status_ail.append('disarmed')

    if isinstance(user.target, units.Boss):
        base_ar = (5 + battle.temp_stats[user.name]['attributes']['dex'])/2

    else:
        base_ar = 5 + battle.temp_stats[user.name]['attributes']['dex']

    actual_ar = max(0, 100 - base_ar)/100
    user.target.attk *= actual_ar

    user.target.hp -= max(10 - user.target.dfns/2, 1)

    if random.randint(0, 3) == 3:
        main.smart_sleep(0.75)
        sounds.unlock_chest.play()
        print(f"{user.name} stealthily retrieves the weapon and pawns it off for {max(user.target.lvl, 5)} GP!")
        main.party_info['gp'] += max(user.target.lvl, 5)


disarming_blow = Ability("Disarming Blow", f"""\
The user knocks the weapon out of a target enemy's hands, taking it for
themselves. Deals 10 physical damage, and lowers the target's physical attack 
by [5 + Dexterity]%. The attack-reduction has half the effect on bosses. The 
user has a 25% chance to steal the weapon, immediately trading it in for an 
amount of GP equal to the target's level, with a minimum of 5 GP.""", 2)
disarming_blow.before_ability = before_disarming_blow
disarming_blow.use_ability = use_disarming_blow


def before_backstab(user):
    user.choose_target(f"Who should {user.name} Backstab?")


def use_backstab(user):
    print(f"{user.name} is preparing to Backstab {user.target.name}...")
    sounds.sword_slash.play()
    main.smart_sleep(0.75)

    damage_multiplier = (125 + battle.temp_stats[user.name]['attributes']['dex'])/100
    base_damage = damage_multiplier*units.deal_damage(user, user.target, "physical", do_criticals=False)

    if user.target.ability_vars['poison_pow']:
        print("Inject Poison increases Backstab damage by 1.5x!")

    base_damage = math.ceil(base_damage)

    if user.target.ability_vars['knockout_turns']:
        user.hp += math.ceil(0.1*base_damage)
        units.fix_stats()
        print(f"Knockout Gas causes Backstab to lifesteal for {math.ceil(0.1*base_damage)} HP!")

    if user.target.ability_vars['disarmed']:
        user.target.dfns = math.ceil(user.target.dfns*0.9)
        print(f"Disarming Blow lowers {user.target.name}'s defense by {math.floor(user.target.dfns*0.1)}!")

    sounds.enemy_hit.play()
    user.target.hp -= base_damage
    print(f"{user.name}'s Backstab deals {base_damage} to the {user.target.name}!")


backstab = Ability("Backstab", f"""\
The user sneaks up on their opponent and deals a [125 + Dexterity]% critical
strike. If the target is poisoned, Backstab will deal 1.5x damage. If the 
target is asleep, Backstab will lifesteal for 10% of the damage dealt. If the
target is disarmed, Backstab will lower the target's physical defense by 10%.
All three effects can happen with a single Backstab.""", 2)
backstab.before_ability = before_backstab
backstab.use_ability = use_backstab


# -- MAGE ABILITIES, scales with Intelligence -- #
def before_skill_shot(user):
    pass


def use_skill_shot(user):
    if user.lvl > max(battle.m_list, key=lambda x: x.lvl).lvl:
        multiplier = (1 + (user.attributes['int'] + 50)/100)

    else:
        multiplier = 1

    base_damage = math.ceil(0.5*sum([x.lvl for x in battle.m_list])*multiplier)

    print(f"{user.name} is preparing to cast Skill Shot...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    for enemy in battle.m_list:
        actual_damage = max(math.ceil((base_damage - enemy.m_dfns/2)), 5)
        enemy.hp -= actual_damage
        print(f"{user.name}'s Skill Shot deals {actual_damage} damage to the {enemy.name}")

    sounds.enemy_hit.play()

skill_shot = Ability("Skill Shot", f"""\
The user launches a magic damage attack at the enemy team, damaging each
target equal to 50% of the sum of their levels. If the user is higher level
than the highest-levelled opponent, Skill Shot does [50 + Intelligence]% more 
damage. Always deals a minimum of 5 damage.""", 4)
skill_shot.before_ability = before_skill_shot
skill_shot.use_ability = use_skill_shot


def before_polymorph(user):
    pass


def use_polymorph(user):
    pass


polymorph = Ability("Polymorph", f"""\
Turns a target enemy into a harmless frog for 1 turn, silencing them and
reducing their attack stats, speed, and evasion to 0. If multiple enemies are
alive on the field, this spell has a [25 + Intelligence]% chance of affecting a
random second target, and a [5 + Intelligence]% chance of affecting a third.""", 3)
polymorph.before_ability = before_polymorph
polymorph.use_ability = use_polymorph


def before_spell_shield(user):
    pass


def use_spell_shield(user):
    pass


spell_shield = Ability("Spell Shield", f"""\
Places a protective barrier around your party that increases magical defense by
[20 + Intelligence] for 3 turns. Does not stack with multiple uses - repeat uses
only refresh the buff duration.""", 5)
spell_shield.before_ability = before_spell_shield
spell_shield.use_ability = use_spell_shield


def before_mana_drain(user):
    user.choose_target(f"Who should {user.name} cast Mana Drain on?")


def use_mana_drain(user):
    print(f"{user.name} is preparing to cast Mana Drain on the {user.target.name}...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    drain = max(((5 + battle.temp_stats[user.name]['attributes']['int'])/100)*user.target.max_mp, 5)

    user.mp += drain
    user.target.mp -= drain

    units.fix_stats()

    sounds.buff_spell.play()
    print(f"The {user.target.name} lost {drain} MP!")
    print(f"{user.name} gained {drain} MP!")


mana_drain = Ability("Mana Drain", f"""\
Depletes the target's current MP by [5 + Intelligence]% of their maximum
MP, while restoring the same amount to the user. Always drains/restores a
minimum of 5 MP.""", 2)
mana_drain.before_ability = before_mana_drain
mana_drain.use_ability = use_mana_drain


# -- RANGER ABILITIES, scales with Perception -- #
def before_roll(user):
    pass


def use_roll(user):
    pass


roll = Ability("Roll", f"""\
The user does a quick tuck-and-roll, disorienting the enemy team and dodging all
attacks for one turn. Also increases their speed by [25 + Perception].
The speed bonus stacks with multiple uses.""", 3)
roll.before_ability = before_roll
roll.use_ability = use_roll


def before_scout(user):
    user.choose_target(f"Who should {user.name} scout?")


def use_scout(user):
    pass


scout = Ability("Scout", f"""\
Scouts a target enemy, identifying its weak point. For 1 turn, all pierce
attacks (Mages and Rangers) on the target will be critical strikes,
dealing [125 + Perception]% damage. Also prevents the attacks from missing.""", 1)
scout.before_ability = before_scout
scout.use_ability = use_scout


def before_powershot(user):
    pass


def use_powershot(user):
    pass


powershot = Ability("Powershot", f"""\
The user channels the power of the wind, firing an single absurdly powerful
arrow. Deals [175 + Perception]% attack damgage to the chosen target, as well
as all units next to them. The user is disabled for 1 turn after using this
ability, unable to use abilities, magic, or attacks.""", 2)
powershot.before_ability = before_powershot
powershot.use_ability = use_powershot


def before_unstable_footing(user):
    pass


def use_unstable_footing(user):
    pass


unstable_footing = Ability("Unstable Footing", f"""\
The user takes advantage of the uneven terrain and trips a target enemy.
Deals [10 + Perception] damage. If the target has not yet moved this turn,
their turn is skipped. The target is also guaranteed to go last next turn.""", 2)
unstable_footing.before_ability = before_unstable_footing
unstable_footing.use_ability = use_unstable_footing


# -- PALADIN ABILITIES, scales with Wisdom -- #
def before_tip_the_scales(user):
    pass


def use_tip_the_scales(user):
    # heal_value = user.max_hp*0.05 +
    pass


tip_the_scales = Ability("Tip the Scales", f"""\
The user tips the scales in their favor, causing them and their allies to be
healed for [5% of User's Max HP + Wisdom] HP each, while dealing the same in
magical damage to a single enemy unit.""", 3)
tip_the_scales.before_ability = before_tip_the_scales
tip_the_scales.use_ability = use_tip_the_scales


def before_unholy_binds(user):
    user.choose_target(f"Who should {user.name} cast Unholy Binds on?", ally=True, enemy=True)


def use_unholy_binds(user):
    if isinstance(user.target, units.PlayableCharacter):
        print(f"{user.target.name} is preparing to cast Unholy Binds on {user.target.name}!")

    else:
        print(f"{user.target.name} is preparing to cast Unholy Binds on the {user.target.name}!")

    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    chance = min(10 + battle.temp_stats[user.name]['attributes']['wis'], 50)/10

    if all([user.target.def_element == 'dark',
            random.randint(1, 10) < chance,
            not isinstance(user.target, units.Boss),
            not isinstance(user.target, units.PlayableCharacter)]):
        user.target.status_ail = ['dead']
        user.target.hp = 0

        sounds.enemy_death.play()

        print(f"The {user.target.name} succumed to the darkness!")

        return

    user.target.def_element = 'dark'

    sounds.poison_damage.play()
    if isinstance(user.target, units.PlayableCharacter):
        print(f"{user.target.name} had their defensive element set to Darkness!")

    else:
        print(f"The {user.target.name} had their defensive element set to Darkness!")

unholy_binds = Ability("Unholy Binds", f"""\
Sets a target's defensive element to Darkness, causing Light and Dark spells
to do more/less damage, respectively. If the target is an enemy, and already
has Darkness as their element, then Unholy Binds has a [10 + Wisdom]% chance
of instantly killing the target, with a maximum of 50%. The instant-kill
effect does not work on Bosses.""", 2)
unholy_binds.before_ability = before_unholy_binds
unholy_binds.use_ability = use_unholy_binds


def before_judgement(user):
    user.choose_target(f"Who should {user.name} cast Judgement on?")


def use_judgement(user):
    if isinstance(user.target, units.Boss):
        rem_turns = 10

    elif user.target.def_element == 'dark':
        rem_turns = max(math.ceil(7*(1 - (15 + user.attributes['wis'])/100)), 2)

    else:
        rem_turns = 7

    judgement_day = battle.turn_counter + rem_turns

    print(f"{user.name} is preparing to cast Judgement on {user.target.name}...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    if user.target.ability_vars['judgement_day'] and user.target.ability_vars['judgement_day'] <= judgement_day:
        print(f"...But {user.target.name}'s jugdement day is already on its way!")
        sounds.debuff.play()

    else:
        print(f"{user.target.name} is doomed. They will die in {rem_turns} turns.")
        user.target.ability_vars['judgement_day'] = judgement_day
        user.target.status_ail.append("Doomed")
        sounds.poison_damage.play()

judgement = Ability("Judgement", f"""\
Applies a DOOM to the target, guaranteeing their death in 7 turns. If the
target's defensive element is Darkness, then the 7 turns will be lowered by
[15 + Wisdom]%, with a minimum of 2 turns. When cast on bosses, the turn count
is always 10 turns. Re-casting this spell has no effect, unless re-casting it 
would cause the timer to be lower.""", 4)
judgement.before_ability = before_judgement
judgement.use_ability = use_judgement


def before_canonize(user):
    pass


def use_canonize(user):
    pass


canonize = Ability("Canonize", f"""\
Declares the target ally a holy figure, converting their defensive element to
Light and causing all healing spells casted on them to heal for an additional
[25 + Wisdom]% HP. Lasts 2 turns. Does not stack with multiple uses - repeat
uses only refresh the buff duration.""", 3)
canonize.before_ability = before_canonize
canonize.use_ability = use_canonize


# --ULTIMATE ABILITIES-- Unique to each party member and do not scale with attributes
def before_ascend(user):
    pass


def use_ascend(user):
    print(f"{user.name} is casting Ascend...")
    sounds.ability_cast.play()
    main.smart_sleep(0.75)

    primary_attr = {"ranger": ["per", "Perception"],
                    "warrior": ["str", "Strength"],
                    "paladin": ["wis", "Wisdom"],
                    "assassin": ["dex", "Dexterity"],
                    "monk": ["con", "Constitution"],
                    "mage": ["int", "Intelligence"]}[user.class_]

    increase = min((0.25 + 0.1*battle.turn_counter), 0.75)
    increase *= battle.temp_stats[user.name]['attributes'][primary_attr[0]]
    increase = math.ceil(increase)
    battle.temp_stats[user.name]['attributes'][primary_attr[0]] += increase

    sounds.buff_spell.play()
    user.ability_vars['ascend_used'] = True
    print(f"{user.name}'s {primary_attr[1]} increased by {increase}!")


ascend = Ability("Ascend", """\
ULTIMATE ABILITY: The Hero ascends to a higher plane of being, raising their
main attribute by 25% + [10% per turn since the battle started]. Caps at 75%.
Can only be used once per battle, and therefore does not stack with multiple
uses.""", 0)
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
the chosen element, but the damage buff does not stack.""", 1)
infusion.before_ability = before_infusion
infusion.use_ability = use_infusion

a_abilities = {
    'paladin': [tip_the_scales, unholy_binds, judgement, canonize],  # 2 3
    'mage': [mana_drain, polymorph, spell_shield, skill_shot],  # 1 4
    'warrior': [roll_call, taunt, great_cleave, berserkers_rage],  # 1 2 4
    'assassin': [inject_poison, knockout_gas, disarming_blow, backstab],  # 1 2 3 4
    'ranger': [scout, roll, powershot, unstable_footing],
    'monk': [chakra_smash, shared_experience, aura_swap, breaking_vows],  # 1 2 3 4

    'player': [ascend],
    'Solou': [infusion],
    'Ran_af': [],
    'Chyme': [],
    'Parsto': [],
    'Xoann': [],
    'Adorine': []

}
