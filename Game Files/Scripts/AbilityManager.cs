using System.Collections.Generic;

namespace Scripts
{
    public static class AbilityManager
    {
        public static Dictionary<CEnums.CharacterClass, List<dynamic>> ability_list = new Dictionary<CEnums.CharacterClass, List<dynamic>>()
        {
            { // 1 2 4 finished
                CEnums.CharacterClass.warrior, new List<dynamic>()
                {
                    // Warrior abilities - Text should not pass this line --> |
                    new TauntAbility("Taunt", @"\
The user taunts the enemy team, forcing all enemies to attack him for 1 turn.
The enemies can only use standard attacks while taunted, and cannot cast
spells or defend. Does not go into effect until the current turn is finished.
Provides a bonus [10 + Strength] Physical Defense during this turn, and half
values for Magical and Pierce Defense.", 2),

                    new RollCallAbility("Roll Call", @"\
The user rallies their allies to fight, causing the physical defense of each
one to increase by [(5 + Strength) / Number of allies]. Always increases defense
by at least 5. Stacks with multiple uses.", 3),

                    new GreatCleaveAbility("Great Cleave", @"\
The user deals a 1.25x critical strike to an enemy unit. If this attack
results in that unit's death, the user gets to target a random additional unit
for a second attack that deals [150 + Strength]% damage.", 2),

                    new BerserkersRageAbility("Berserker's Rage", @"\
The user goes into a frenzy, discarding their defensive training and focusing
their might on destroying a target enemy. Increases speed and physical attack
by [15 + Strength]%, and reduces all three armor stats by the half the value.
Repeat casts only affect these stats by 10/5% each, with no attribute bonus.", 2),
                }
            },

            { // 1 2 3 4 finished
                CEnums.CharacterClass.monk, new List<dynamic>()
                {
                    // Monk abilities - Text should not pass this line -----> |
                    new ChakraSmashAbility("Chakra Smash", @"\
Deals a 2x critical strike to a target enemy, lowering their defensive stats
by [5 + Constitution]. This attack can also crit, which would result in a total
of 3x damage. The armor reduction lasts indefinitely and stacks with multiple
uses.", 3),

                    new SharedExperienceAbility("Shared Experience", @"\
The user disregards any sense of good judgment they had, throwing themself
wrecklessly at a target enemy. Deals [25 + Constitution]% of the target's
current HP in magical damage, while also damaging the user for half the value.
The self-damage is non-lethal, meaning that the user cannot die from it.", 3),

                    new AuraSwapAbility("Aura Swap", @"\
The user swaps the HP values of the highest-hp enemy and the lowest-hp ally.
For every 5 HP that this alters, the user's evasion goes up by 
[5 + Constitution]. Always increases evasion by at least 5. This spell does
nothing if it would result in the ally losing HP. Cannot be casted on dead
units. When cast on bosses, the boss's HP is not altered, but the ally's HP 
is. The evasion bonus stacks with multiple uses. Evasion has a cap of 256.", 3),

                    new BreakingVowsAbility("Breaking Vows", @"\
The user realigns their chakras, converting their own pain into an offensive
weapon. Deals 5 damage, with an additional 1% of the target's maximum HP added
for every 1% of HP the user is missing. If the user's current HP is below
25%, this ability will lifesteal for [10 + Constitution]% of the damage
dealt.", 5)
                }
            },

            { // 1 2 3 4 finished
                CEnums.CharacterClass.assassin, new List<dynamic>()
                {
                    // Assassin abilities - Text should not pass this line -> |
                    new InjectPoisonAbility("Inject Poison", @"\
Injects a poison into a target enemy that deals [2 + Dexterity] magical
damage per turn, capped at 10% the target's maximum HP. Stacks with multiple 
uses, with each stack increasing damage dealt per turn by 2% of the target's 
maximum HP.", 2),

                    new KnockoutGasAbility("Knockout Gas", @"\
The user sneaks behind a target enemy and applies knockout gas to them,
putting them to sleep. The sleep lasts for [4% of Dexterity] turns, with
a minimum of 2 turns and a maximum of 8. The target has a 10% chance of 
randomly waking up each turn. Does not stack with multiple uses - repeat uses 
only refresh the sleep duration.", 2),

                    new DisarmingBlowAbility("Disarming Blow", @"\
The user knocks the weapon out of a target enemy's hands, taking it for
themselves. Deals 10 physical damage, and lowers the target's physical attack 
by[5 + Dexterity]%. The attack-reduction has half the effect on bosses. The
user has a 25% chance to steal the weapon, immediately trading it in for an
amount of GP equal to the target's level, with a minimum of 5 GP.", 2),

                    new BackstabAbility("Backstab", @"\
The user sneaks up on their opponent and deals a [125 + Dexterity]% critical
strike. If the target is poisoned, Backstab will deal 1.5x base damage. If the
target is asleep, Backstab will lifesteal for 10% of the damage dealt. If the
target is disarmed, Backstab will lower the target's physical defense by 10%.
All three effects can happen with a single Backstab.", 2)
                }
            },

            { // 1 2 finished
                CEnums.CharacterClass.mage, new List<dynamic>()
                {
                    // Mage abilities - Text should not pass this line -----> |
                    new SkillSyphonAbility("Skill Syphon", @"\
The user channels their power to literally drain the skill from a target enemy.
Reduces the target's 3 Attack Stats, 3 Armor Stats, Speed and Evasion by 
[1 + Intelligence] each, and increases the respective stat by the same
for the user. Stat loss/gain is capped at 20% the target's original stat value.
Will always drain at least 1 of each stat. Will only affect the user's stats if
casted on bosses. Can only be used once per enemy per battle.", 5),

                    new PolymorphAbility("Polymorph", @"\
The user turns a target enemy into a harmless frog for 1 turn, silencing them
and reducing their attack stats, speed, and evasion to 0. If multiple enemies
are alive on the field, this spell has a [25 + Intelligence]% chance of
affecting a random second target, and a [5 + Intelligence]% chance of
affecting a third.", 3),

                    new SpellShieldAbility("Spell Shield", @"\
Places a protective barrier around your party that increases magical defense by
[20 + Intelligence] for 3 turns. Does not stack with multiple uses - repeat uses
only refresh the buff duration.", 5),

                    new ManaDrainAbility("Mana Drain", @"\
Depletes the target's current MP by [5 + Intelligence]% of their maximum
MP, while restoring the same amount to the user. Always drains/restores a
minimum of 5 MP.", 2)
                }
            },

            { // None finished
                CEnums.CharacterClass.ranger, new List<dynamic>()
                {
                    // Ranger abilities - Text should not pass this line ---> |
                    new RollAbility("Roll", @"\
The user does a quick tuck-and-roll, disorienting the enemy team and dodging all
attacks for one turn. Also increases their speed by [25 + Perception].
The speed bonus stacks with multiple uses.", 3),

                    new ScoutAbility("Scout", @"\
Scouts a target enemy, identifying its weak point. For 1 turn, all pierce
attacks (Mages and Rangers) on the target will be critical strikes,
dealing [150 + Perception]% damage. Also prevents the attacks from missing.", 1),

                    new PowershotAbility("Powershot", @"\
The user channels the power of the wind, firing an single absurdly powerful
arrow. Deals [175 + Perception]% attack damage to the chosen target, and
[50 + Perception]% attack damage to all other enemy targets. The user is
completely disabled for 1 turn after using this ability.", 2),

                    new NaturesCallAbility("Nature's Call", @"\
The user calls upon nature, requesting help from the most powerful of animal
allies. Deals a base damage dependent on what animal arrives, plus
[100 + Perception]% additional damage.", 2)
                }
            },

            { // 1 2 3 finished
                CEnums.CharacterClass.paladin, new List<dynamic>()
                {
                    // Paladin abilities - Text should not pass this line --> |
                    new TipTheScalesAbility("Tip the Scales", @"\
The user tips the scales in their favor, healing allies and damaging enemies.
Has a 'power value' of [5% Max HP + Wisdom]. If casted on an ally, this will
deal the power value in magical damage to all enemy units, while healing the
ally for the total damage dealt.If casted on an enemy, this will restore HP
equal to the power value for each ally unit, while damaging the enemy for the
total healing done in magical damage.", 3),

                    new UnholyBindsAbility("Unholy Binds", @"\
Sets a target's defensive element to Darkness, causing Light and Dark spells
to do more/less damage, respectively. If the target is an enemy, and already
has Darkness as their element, then Unholy Binds has a [10 + Wisdom]% chance
of instantly killing the target, with a maximum of 50%. The instant-kill
effect does not work on Bosses.", 2),

                    new JudgmentAbility("Judgment", @"\
Applies a DOOM to the target, guaranteeing their death in 7 turns. If the
target's defensive element is Darkness, then the 7 turns will be lowered by
[15 + Wisdom]%, with a minimum of 2 turns. When cast on bosses, the turn count
is always 10 turns. Re-casting this spell has no effect, unless re-casting 
it would cause the timer to be lower.", 4),

                    new CanonizeAbility("Canonize", @"\
Declares the target ally a holy figure, converting their defensive element to
Light and causing all healing spells casted on them to heal for an additional
[15 + Wisdom]%. Lasts 2 turns. Does not stack with multiple uses - repeat
uses only refresh the buff duration.", 3)
                }
            },

            { // None finished
                CEnums.CharacterClass.bard, new List<dynamic>()
                {
                    // Bard abilities - Text should not pass this line -----> |
                    new WaywardFellowAbility("The Wayward Fellow", @"\
Summons the elusive Wayward Fellow to assist your party. The Wayward Fellow
lasts for the entire duration of the battle and cannot be targetted by any
spell, attack, or ability. He has no spells or abilities and can only attack
using his Bow. The Fellow has [10 + 0.10*Charisma] Speed and Pierce Attack.
Replaying this song increases the Speed and Pierce Attack of the fellow by
[5 + 0.10*Charisma], with no cap. The Wayward Fellow does not need to be
controlled, he will automatically attack a random target each turn.", 0),

                    new FallenComradeAbility("Ode to a Fallen Comrade", @"\
1 A X
2 B Y
3 C Z", 0),

                    new StubbornBoarAbility("Tale of the Stubborn Boar", @"\
Sets the target's defense stats to 0 for one turn, then increases them to
[115 + Charisma]% of their original. Can be used on both enemies and allies.", 0),

                    new UnlikelyHeroAbility("An Unlikely Hero", @"\
1 A X
2 B Y
3 C Z", 0),

                    new TournamentAbility("The Tournament of Thieves", @"\
1 A X
2 B Y
3 C Z", 0),

                    new GrandFinaleAbility("Grand Finale", @"\
A satisfying and exciting closer to a bard performance! Deals 
[(5 + Charisma)*Songs Played] magical damgage to a single target, and
heals the user for the same amount. Only up to three songs are counted, and
they must have been played during the current battle. The order of the songs 
do not matter, and they do not haven to be three different songs. Does
nothing if no songs have been played yet.", 3)
                }
            }
        };

        public static Dictionary<CEnums.CharacterClass, List<dynamic>> GetAbilityList()
        {
            return ability_list;
        }
    }

    public class Ability
    {
        // Abilites are similar to magic, except they are tied to classes and are level-independent. They also
        // cost Action Points to use instead of Mana, and tend to have much more specific functions.

        public string AbilityName { get; set; }
        public string AbilityDesc { get; set; }
        public int APCost { get; set; }

        public void BeforeAbility(Unit user)
        {

        }

        public void UseAbility(Unit user)
        {

        }

        public Ability(string name, string desc, int ap_cost)
        {
            AbilityName = name;
            AbilityDesc = desc;
            APCost = ap_cost;
        }
    }

    /* =========================== *
     *      WARRIOR ABILITIES      *
     * =========================== */

    class TauntAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            for x in battle.m_list:
                x.ability_vars['taunted'] = [battle.turn_counter + 1, user]
                x.status_ail.append("Taunted")

            print(f"{user.name} is preparing to cast Taunt...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            phys = 10 + user.attributes['str']
            other = math.ceil(phys / 2)

            battle.temp_stats[user.name]['dfns'] += phys
            battle.temp_stats[user.name]['p_dfns'] += other
            battle.temp_stats[user.name]['m_dfns'] += other

            print(f"{user.name} taunts the enemy team!")
            print(f"{user.name} gains {phys}/{other}/{other} physical/magical/pierce defense!") */

        public TauntAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class RollCallAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            sounds.ability_cast.play()
            print(f"{user.name} begins to motivate their allies with a Roll Call...")
            main.smart_sleep(0.75)

            for pcu in battle.enabled_pcus:
                increase = (battle.temp_stats[user.name]['attributes']['str'] + 5)/len(battle.enabled_pcus)
                increase = max(math.ceil(increase), 5)
                battle.temp_stats[pcu.name]['dfns'] += increase

            print(f"All allies physical defense increased by {increase}!")
            sounds.buff_spell.play() */

        public RollCallAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class GreatCleaveAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Great Cleave on?")

        def use_ability(self, user):
            pass */

        public GreatCleaveAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class BerserkersRageAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            if user.ability_vars['berserk']:
                values = 0.10

            else:
                values = 0.15 + user.attributes['str']/100

            print(f"{user.name} is preparing to cast Berserker's Rage...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            print(f"Speed and Physical Attack increased by {math.ceil(values*100)}%!")
            print(f"Armor Stats decreased by {math.ceil(values*50)}%!")

            battle.temp_stats[user.name]['spd'] += math.ceil(battle.temp_stats[user.name]['spd']* values)
            battle.temp_stats[user.name]['attk'] += math.ceil(battle.temp_stats[user.name]['spd']* values)
            battle.temp_stats[user.name]['dfns'] -= math.ceil(battle.temp_stats[user.name]['spd']* values/2)
            battle.temp_stats[user.name]['m_dfns'] -= math.ceil(battle.temp_stats[user.name]['spd']* values/2)
            battle.temp_stats[user.name]['p_dfns'] -= math.ceil(battle.temp_stats[user.name]['spd']* values/2)
            user.ability_vars['berserk'] = True */

        public BerserkersRageAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    /* =========================== *
     *        MONK ABILITIES       *
     * =========================== */


    class ChakraSmashAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Chakra Smash on?")

        def use_ability(self, user):
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

            return True */

        public ChakraSmashAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class SharedExperienceAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public SharedExperienceAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class AuraSwapAbility : Ability
    {
        /* 
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            c_enemy = max(battle.m_list, key= lambda x: x.hp)
            c_ally = min([x for x in battle.enabled_pcus if 'dead' not in x.status_ail], key= lambda x: x.hp)

            sounds.ability_cast.play()
            print(f"{user.name} is beginning to cast Aura Swap...")
            main.smart_sleep(0.75)

            if c_enemy.hp <= c_ally.hp:
                print("...But it failed!")
                sounds.debuff.play()

            else:
                sounds.buff_spell.play()
                beginning = [c_enemy.hp, c_ally.hp]

                if isinstance(c_enemy, units.Boss) :
                    c_ally.hp = c_enemy.hp

                else:
                    c_enemy.hp, c_ally.hp = c_ally.hp, c_enemy.hp

                units.fix_stats()

                evad = max(math.floor((c_ally.hp - c_enemy.hp)/5)* (5 + battle.temp_stats[user.name]['attributes']['str']),
                           5)
                battle.temp_stats[user.name]['evad'] += evad

                print(f"{c_ally.name}'s HP rose from {beginning[1]} to {c_ally.hp}!")

                if isinstance(c_enemy, units.Boss) :
                    print(f"{c_enemy.name}'s boss aura protected them!")

                else:
                    print(f"{c_enemy.name}'s HP dropped from {beginning[0]} to {c_enemy.hp}!")

                print(f"{user.name}'s evasion increased by {evad}!") */

        public AuraSwapAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class BreakingVowsAbility : Ability
    {
        /* 
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Breaking Vows on?")

        def use_ability(self, user):
            hp_missing = (user.max_hp - user.hp)/(user.max_hp*100)
            damage = 5 + math.ceil(hp_missing* user.target.max_hp)
            lifesteal = 0 if hp_missing <= 75 else max((0.1 + user.attributes['con']/100)* damage, 1)

            print(f"{user.name} is preparing to cast Breaking Vows...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            user.target.hp -= damage
            user.hp += lifesteal

            print(f"{user.name}'s Breaking Vows deals {damage} damage to the {user.target.name}!")

            if lifesteal:
                print(f"{user.target.name} lifesteals for {lifesteal} HP!") */

        public BreakingVowsAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    /* =========================== *
     *      ASSASSIN ABILITIES     *
     * =========================== */

    class InjectPoisonAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} inject poison into?")

        def use_ability(self, user):
            user.target.status_ail.append('poisoned')
            user.target.ability_vars['poison_pow'] += 0.02
            user.target.ability_vars['poison_dex'] = 2 + battle.temp_stats[user.name]['attributes']['dex']

            poison_power = math.ceil(100 * user.target.ability_vars['poison_pow'] + user.target.ability_vars['poison_dex'])

            print(f"{user.name} is preparing a poison with power {poison_power}...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            print(f"{user.name} injects the poison into the {user.target.name}!")
            sounds.poison_damage.play() */

        public InjectPoisonAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class KnockoutGasAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Knockout Gas on?")

        def use_ability(self, user):
            print(f"{user.name} is preparing some Knockout Gas for {user.target.name}...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            k_dur = math.ceil(battle.temp_stats[user.name]['attributes']['dex']/25)
            k_dur = min(max(k_dur, 2), 8)
            user.target.ability_vars['knockout_turns'] = k_dur
            user.target.status_ail.append("asleep")

            print(f"{user.target.name} was put to sleep for {k_dur} turns!")
            sounds.poison_damage.play() */

        public KnockoutGasAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class DisarmingBlowAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} disarm?")

        def use_ability(self, user):
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

            if isinstance(user.target, units.Boss) :
                base_ar = (5 + battle.temp_stats[user.name]['attributes']['dex'])/2

            else:
                base_ar = 5 + battle.temp_stats[user.name]['attributes']['dex']

            actual_ar = max(0, 100 - base_ar) / 100
            user.target.attk *= actual_ar

            user.target.hp -= max(10 - user.target.dfns/2, 1)

            if random.randint(0, 3) == 3:
                main.smart_sleep(0.75)
                sounds.unlock_chest.play()
                print(f"{user.name} stealthily retrieves the weapon and pawns it off for {max(user.target.lvl, 5)} GP!")
                main.party_info['gp'] += max(user.target.lvl, 5) */

        public DisarmingBlowAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class BackstabAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} Backstab?")

        def use_ability(self, user):
            print(f"{user.name} is preparing to Backstab {user.target.name}...")
            sounds.sword_slash.play()
            main.smart_sleep(0.75)

            damage_multiplier = (125 + battle.temp_stats[user.name]['attributes']['dex'])/100
            base_damage = damage_multiplier* units.deal_damage(user, user.target, "physical", do_criticals= False)

            if user.target.ability_vars['poison_pow']:
                print("Inject Poison increases Backstab damage by 1.5x!")

            base_damage = math.ceil(base_damage)

            if user.target.ability_vars['knockout_turns']:
                user.hp += math.ceil(0.1* base_damage)
                units.fix_stats()
                print(f"Knockout Gas causes Backstab to lifesteal for {math.ceil(0.1*base_damage)} HP!")

            if user.target.ability_vars['disarmed']:
                user.target.dfns = math.ceil(user.target.dfns*0.9)
                print(f"Disarming Blow lowers {user.target.name}'s defense by {math.floor(user.target.dfns*0.1)}!")

            sounds.enemy_hit.play()
            user.target.hp -= base_damage
            print(f"{user.name}'s Backstab deals {base_damage} to the {user.target.name}!") */

        public BackstabAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    /* =========================== *
     *        MAGE ABILITIES       *
     * =========================== */

    class SkillSyphonAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Skill Syphon on?")

        def use_ability(self, user):
            print(f"{user.name} is preparing to cast Skill Syphon...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            if user.target.ability_vars['drained']:
                print(f"...But the {user.target.name} has already been drained!")
                sounds.debuff.play()

            else:
                sounds.buff_spell.play()
                user.target.ability_vars['drained'] = True
                user.target.status_ail.append('Drained')

                total = 0

                # I don't know of any better way to do this than like this so here we go
                for x in ['attk', 'm_attk', 'p_attk', 'dfns', 'dfns', 'dfns', 'spd', 'evad']:
                    value = eval(f"max(1, min(math.ceil(0.2*user.target.{x}), 1 + user.attributes['int']))")
                    total += value

                    if not isinstance(user.target, units.Boss):
                        exec(f"user.target.{x} -= value")

                    exec(f"battle.temp_stats[user.name]['{x}'] += value")

                print(f"{user.name} stats increased by {total}!")

                if isinstance(user.target, units.Boss) :
                    print(f"{user.target.name}'s boss aura protected them!")

                else:
                    print(f"{user.target.name} stats decreased by {total}!") */

        public SkillSyphonAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class PolymorphAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public PolymorphAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class SpellShieldAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public SpellShieldAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class ManaDrainAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Mana Drain on?")

        def use_ability(self, user):
            print(f"{user.name} is preparing to cast Mana Drain...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            drain = max(((5 + battle.temp_stats[user.name]['attributes']['int'])/100)* user.target.max_mp, 5)

            user.mp += drain
            user.target.mp -= drain

            units.fix_stats()

            sounds.buff_spell.play()
            print(f"The {user.target.name} lost {drain} MP!")
            print(f"{user.name} gained {drain} MP!") */

        public ManaDrainAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    /* =========================== *
     *       RANGER ABILITIES      *
     * =========================== */

    class RollAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public RollAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class ScoutAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} scout?")

        def use_ability(self, user):
            pass */

        public ScoutAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class PowershotAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public PowershotAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class NaturesCallAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            animal_dict = {
                "Mouse": 1,
                "Chipmunk": 5,
                "Weasel": 10,
                "Snake": 15,
                "Mongoose": 20,
                "Fox": 25,
                "Badger": 30,
                "Eagle": 35,
                "Coyote": 40,
                "Moose": 45,
                "Bear": 50,
                "Goose": 75,
                "Pack of Wolves": 100
            } */

        public NaturesCallAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    /* =========================== *
     *      PALADIN ABILITIES      *
     * =========================== */

    class TipTheScalesAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Tip the Scales on?", ally=True)

        def use_ability(self, user):
            print(f"{user.name} is preparing to cast Tip the Scales...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            power_value = math.ceil(user.max_hp*0.05 + user.attributes['wis'])
            total = 0

            if isinstance(user.target, units.PlayableCharacter) :
                for enemy in [x for x in battle.m_list if x.hp > 0]:
                    damage = math.ceil(power_value - enemy.m_dfns/2)
                    total += damage
                    enemy.hp -= damage
                    print(f"Tip the Scales deals {damage} damage to the {enemy.name}!")

                sounds.enemy_hit.play()
                main.smart_sleep(0.5)
                sounds.enemy_hit.stop()

                user.target.hp += total
                print(f"Tip the scales heals {user.target.name} by {total} HP!")
                sounds.magic_healing.play()

            else:
                for ally in [x for x in battle.enabled_pcus if x.hp > 0]:
                    total += power_value
                    ally.hp += power_value
                    print(f"Tip the Scales heals {user.name} by {power_value} HP! ")

                sounds.magic_healing.play()
                main.smart_sleep(0.5)
                sounds.magic_healing.stop()

                user.target.hp -= total
                print(f"Tip the Scales deals {total} damage to the {user.target.name}!")
                sounds.enemy_hit.play() */

        public TipTheScalesAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class UnholyBindsAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Unholy Binds on?", ally=True, enemy=True)

        def use_ability(self, user):
            if isinstance(user.target, units.PlayableCharacter) :
                print(f"{user.name} is preparing to cast Unholy Binds on {user.target.name}...")

            else:
                print(f"{user.name} is preparing to cast Unholy Binds on the {user.target.name}...")

            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            chance = min(10 + battle.temp_stats[user.name]['attributes']['wis'], 50)/10

            if all([user.target.def_element == 'dark',
                    random.randint(1, 10) < chance,
                    not isinstance(user.target, units.Boss),
                    not isinstance(user.target, units.PlayableCharacter)]) :
                user.target.status_ail = ['dead']
        user.target.hp = 0

                sounds.enemy_death.play()

                print(f"The {user.target.name} succumed to the darkness!")

                return

            user.target.def_element = 'dark'

            sounds.poison_damage.play()
            if isinstance(user.target, units.PlayableCharacter) :
                print(f"{user.target.name} had their defensive element set to Darkness!")

            else:
                print(f"The {user.target.name} had their defensive element set to Darkness!") */

        public UnholyBindsAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class JudgmentAbility : Ability
    {
        /*
        def before_ability(self, user):
            user.choose_target(f"Who should {user.name} cast Judgment on?")

        def use_ability(self, user):
            if isinstance(user.target, units.Boss) :
                rem_turns = 10

            elif user.target.def_element == 'dark':
                rem_turns = max(math.ceil(7 * (1 - (15 + user.attributes['wis']) / 100)), 2)

            else:
                rem_turns = 7

            judgment_day = battle.turn_counter + rem_turns

            print(f"{user.name} is preparing to cast Judgment...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            if user.target.ability_vars['judgment_day'] and user.target.ability_vars['judgment_day'] <= judgment_day:
                print(f"...But {user.target.name}'s jugdement day is already on its way!")
                sounds.debuff.play()

            else:
                print(f"{user.target.name} is doomed. They will die in {rem_turns} turns.")
                user.target.ability_vars['judgment_day'] = judgment_day
                user.target.status_ail.append("Doomed")
                sounds.poison_damage.play() */

        public JudgmentAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class CanonizeAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public CanonizeAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    /* =========================== *
     *        BARD ABILITIES       *
     * =========================== */

    class WaywardFellowAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public WaywardFellowAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class FallenComradeAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public FallenComradeAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class StubbornBoarAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public StubbornBoarAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class UnlikelyHeroAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public UnlikelyHeroAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class TournamentAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public TournamentAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    class GrandFinaleAbility : Ability
    {
        /*
        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass */

        public GrandFinaleAbility(string name, string desc, int ap_cost) : base(name, desc, ap_cost)
        {

        }
    }

    /* =========================== *
     *     ULTIMATE ABILITIES      *
     * =========================== */
    // Unique to each party member and do not scale with attributes

    /*
    class AscendAbility : Ability {
        def __init__(self, name, desc, ap_cost):
            super().__init__(name, desc, ap_cost)

        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            print(f"{user.name} is casting Ascend...")
            sounds.ability_cast.play()
            main.smart_sleep(0.75)

            primary_attr = {"ranger": ["per", "Perception"],
                            "warrior": ["str", "Strength"],
                            "paladin": ["wis", "Wisdom"],
                            "assassin": ["dex", "Dexterity"],
                            "monk": ["con", "Constitution"],
                            "mage": ["int", "Intelligence"],
                            "bard": ["cha", "Charisma"]}[user.class_]

            increase = min((0.25 + 0.1*battle.turn_counter), 0.75)
                    increase *= battle.temp_stats[user.name]['attributes'][primary_attr[0]]
                    increase = math.ceil(increase)
                    battle.temp_stats[user.name]['attributes'][primary_attr[0]] += increase

                    sounds.buff_spell.play()
                    user.ability_vars['ascend_used'] = True
                    print(f"{user.name}'s {primary_attr[1]} increased by {increase}!")

    ascend = Ascend("Ascend", @"\
    ULTIMATE ABILITY: The Hero ascends to a higher plane of being, raising their
    main attribute by 25% + [10% per turn since the battle started]. Caps at 75%.
    Can only be used once per battle, and therefore does not stack with multiple
    uses.", 2)

    class InfusionAbility : Ability {
        def __init__(self, name, desc, ap_cost):
            super().__init__(name, desc, ap_cost)

        def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass

    infusion = Infusion("Infusion", @"\
    ULTIMATE ABILITY: Solou chooses a party member and enchants their weapon with
    an element of her choice, while also causing it to deal an additional 10 %
    damage.Optionally, Solou can instead choose "random", causing a random element
    to be selected and raising the damage buff to 20 %.Can be re - casted to change
    the chosen element, but the damage buff does not stack.", 1)

    class TuneInstrumentAbility : Ability {
        def __init__(self, name, desc, ap_cost):
            super().__init__(name, desc, ap_cost)

            # Normal    -> 1.00x Charisma
            # Good      -> 1.25x Charisma
            # Great     -> 1.50x Charisma
            # Excellent -> 1.75x Charisma
            # Perfect   -> 2.00x Charisma

    def before_ability(self, user):
            pass

        def use_ability(self, user) :
            pass

    tune_instrument = TuneInstrument("Tune Instrument", @"\
    ULTIMATE ABILITY: Flaard has perfect pitch, allowing him to effortlessly tune
    his instruments while in battle.Instruments have 5 tuning levels: Normal,
    Good, Great, Excellent, and Perfect.Using this ability will set the tuning
    level to Perfect, and playing any song will lower the tuning level by one.
    The higher the tuning level, the higher Flaard's Charisma multiplier will be 
    when casting abilities, up to 2x.Flaard's tuning level is not reset after 
    battle.", 0) */
}


