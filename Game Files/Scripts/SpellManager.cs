using System.Collections.Generic;
using System;

namespace Scripts
{
    public static class SpellManager
    {
        private static readonly List<AttackSpell> attack_spellbook = new List<AttackSpell>()
        {
            // Attack spells
            // Neutral spells - All 3 tiers can be learned by any class
            // Light spells - Tier 3 can be learned by Paladins and Mages
            // All other attack spells - Tier 3 can only be learned by mages

            // Neutral
            new AttackSpell("Magical Shot", "Hurl a small ball of magical energy at your enemies! (25% Spell Power)",
                3, 1, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.25, CEnums.Element.neutral, "no_elem_1"),

            new AttackSpell("Magical Burst", "Shatter your enemy with a wave of magical energy! (50% Spell Power)",
                9, 11, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.5, CEnums.Element.neutral, "no_elem_2"),

            new AttackSpell("Magical Blast", "Annihilate your enemies with a blast of magical energy! (100% Spell Power)",
                18, 23, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 1, CEnums.Element.neutral, "no_elem_3"),

            // Fire
            new AttackSpell("Flame Bolt", "Summon a small fireball to destroy your foes! (25% Spell Power)",
                3, 2, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.25, CEnums.Element.fire, "fire_elem_1"),

            new AttackSpell("Fierce Blaze", "Summon a powerful flame to destroy your foes! (50% Spell Power)",
                10, 12, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.5, CEnums.Element.fire, "fire_elem_2"),
            
            new AttackSpell("Grand Inferno", "Unleash a monstrous blaze destroy your foes! (100% Spell Power)",
                20, 24, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.fire, "fire_elem_3"),

            // Grass
            new AttackSpell("Leaf Blade", "Summon razor-sharp blades of grass to destroy your foes! (25% Spell Power)",
                3, 2, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.25, CEnums.Element.grass, "grass_elem_1"),

            new AttackSpell("Grass Grenade", "Summon a small explosion to destroy your foes! (50% Spell Power)",
                10, 12, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.5, CEnums.Element.grass, "grass_elem_2"),

            new AttackSpell("Vine Storm", "Unleash a frenzy of powerful vines to destroy your foes! (100% Spell Power)",
                20, 24, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.grass, "grass_elem_3"),

            // Electricity
            new AttackSpell("Spark", "Summon a small spark to destroy your foes! (25% Spell Power)",
                3, 3, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.25, CEnums.Element.electric, "elec_elem_1"),

            new AttackSpell("Powerful Jolt", "Summon a powerful jolt of energy to destroy your foes! (50% Spell Power)",
                10, 13, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.5, CEnums.Element.electric, "elec_elem_2"),

            new AttackSpell("Superior Storm", "Unleash a devastating lightning storm to destroy your foes! (100% Spell Power)",
                20, 25, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.electric, "elec_elem_3"),

            // Water
            new AttackSpell("Drizzle", "Summon a small to destroy your foes! (25% Spell Power)",
                3, 3, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.25, CEnums.Element.water, "water_elem_1"),

            new AttackSpell("Water Blast", "Summon a large burst of water to destroy your foes! (50% Spell Power)",
                10, 13, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.5, CEnums.Element.water, "water_elem_2"),

            new AttackSpell("Tsunami", "Unleash a terrifying barrage of waves upon your foes! (100% Spell Power)",
                20, 25, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.water, "water_elem_3"),

            // Earth
            new AttackSpell("Mud Toss", "Summon a small ball of mud to throw at your foes! (25% Spell Power)",
                3, 4, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.25, CEnums.Element.earth, "earth_elem_1"),

            new AttackSpell("Rock Slam", "Crush your enemies under a layer of solid rock! (50% Spell Power)",
                10, 13, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.5, CEnums.Element.earth, "earth_elem_2"),

            new AttackSpell("Earthquake", "Wreck havoc on your enemies with a powerful earthquake! (100% Spell Power)",
                20, 25, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.earth, "earth_elem_3"),

            // Ice
            new AttackSpell("Icicle Dagger", "Hurl a volley of supercooled icicles at your enemies! (25% Spell Power)",
                3, 4, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.25, CEnums.Element.ice, "ice_elem_1"),

            new AttackSpell("Hailstorm", "Rain ice upon your enemies with unrelenting force! (50% Spell Power)",
                11, 14, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any },0.5, CEnums.Element.ice, "ice_elem_2"),

            new AttackSpell("Blizzard", "Devastate your enemies with a terrifying flurry of ice and wind! (100% Spell Power)",
                23, 26, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.ice, "ice_elem_3"),

            // Wind
            new AttackSpell("Minor Gust", "Batter your enemies with powerful gusts and winds! (25% Spell Power)",
                3, 4, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.25, CEnums.Element.wind, "wind_elem_1"),

            new AttackSpell("Microburst", "Decimate your foes with a powerful blast of wind! (50% Spell Power)",
                11, 14, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.5, CEnums.Element.wind, "wind_elem_2"),

            new AttackSpell("Cyclone", "Demolish all that stand in your path with a terrifying tornado! (100% Spell Power)",
                23, 26, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.wind, "wind_elem_3"),

            // Light
            new AttackSpell("Purify", "Call upon His Divinity to cast out evil creatures! (25% Spell Power)!",
                 3, 5, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.25, CEnums.Element.light, "light_elem_1"),

            new AttackSpell("Holy Smite", "Strike down unholy beings using His Divinity's power! (50% Spell Power)",
                 11, 15, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.5, CEnums.Element.light, "light_elem_2"),

            new AttackSpell("Moonbeam", "Utterly destroy evil creatures with holy rays from the moon! (100% Spell Power)",
                 23, 27, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.paladin }, 1, CEnums.Element.light, "light_elem_3"),

            // Dark
            new AttackSpell("Evil Curse", "Call upon His Wickedness to harm holy creatures! (25% Spell Power)",
                 3, 5, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.25, CEnums.Element.dark, "dark_elem_1"),

            new AttackSpell("Desecration", "Defile holy spirits with an evil aura! (50% Spell Power)",
                 11, 15, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.5, CEnums.Element.dark, "dark_elem_2"),

            new AttackSpell("Unholy Rend", "Annihilate holy creatures with a sundering blow! (100% Spell Power)",
                 23, 27, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage }, 1, CEnums.Element.dark, "dark_elem_3")
        };

        private static readonly List<HealingSpell> healing_spellbook = new List<HealingSpell>()
        {
            new HealingSpell("Novice Healing", @"\
Restore a small amount of an ally's HP using holy magic. Heals 10 HP or 5% of
the target's max HP, whichever is greater [5% Healing Power].",
                2, 1, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 10, 0.05, "healing_1"),
            
            new HealingSpell("Adept Healing", @"\
Restore a moderate amount of an ally's HP using holy magic. Heals 25 HP or 20%
of the target's max HP, whichever is greater [20% Healing Power].",
                5, 3, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 25, 0.2, "healing_2"),

            new HealingSpell("Advanced Healing", @"\
Restore a large amount of an ally's HP using holy magic. Heals 70 HP or 50%
of the target's max HP, whichever is greater [50% Healing Power].",
                10, 15, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 70, 0.5, "healing_3"),
                
            // This tier can only be learned by Paladins and Mages
            new HealingSpell("Divine Healing", @"\
Restore a very large amount of an ally's HP using holy magic. Heals 125 HP or
75% of the target's max HP, whichever is greater [75% Healing Power].", 
                25, 28, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.paladin, CEnums.CharacterClass.mage }, 125, 0.75, "healing_4")
        };

        private static readonly List<BuffSpell> buff_spellbook = new List<BuffSpell>()
        {
            new BuffSpell("Minor Quickness", @"\
Raise an ally's speed by 15%. Stacks with multiple uses. Lasts until the end
of battle.", 
                3, 1, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "speed", "speed_1"),

            new BuffSpell("Minor Evade", @"\
Raise an ally's evasion by 15%. Stacks with multiple uses. Lasts until the end
of battle. Note: Evasion has a cap of 256 (50 % chance to dodge).", 
                3, 1, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "evasion", "evad_1"),

            new BuffSpell("Adept Quickness", @"\
Raise an ally's speed by 30%. Stacks with multiple uses. Lasts until the end
of battle.", 
                6, 10, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.3, "speed", "speed_2"),

            new BuffSpell("Adept Evade", @"\
Raise an ally's evasion by 30%. Stacks with multiple uses. Lasts until the end
of battle.Note: Evasion has a cap of 256(50 % chance to dodge).", 
                6, 10, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, 0.3, "evad", "evad_2"),

// Defense Buffs
            new BuffSpell("Minor Defend", @"\
Raise an ally's Physical Defense by 15%. Stacks with multiple uses. Lasts until the end
of battle.", 
                3, 3, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "dfns", "defend_1"),

            new BuffSpell("Minor Shield", @"\
Raise an ally's Magical Defense by 15%. Stacks with multiple uses. Lasts until the end
of battle.", 
                3, 5, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "m_dfns", "shield_1"),

            new BuffSpell("Minor Block", @"\
Raise an ally's Pierce Defense by 15%. Stacks with multiple uses. Lasts until
the end of battle.", 
    3, 7, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "p_dfns", "block_1"),

            new BuffSpell("Adept Defend", @"\
Raise an ally's Physical Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.", 
    6, 14, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, 0.3, "dfns", "defend_2"),

            new BuffSpell("Adept Shield", @"\
Raise an ally's Magical Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.", 
    6, 16, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, 0.3, "m_dfns", "shield_2"),

            new BuffSpell("Adept Block", @"\
Raise an ally's Pierce Defense by 30%. Stacks with multiple uses. Lasts until the end
of battle.", 
    6, 18, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, 0.3, "p_dfns", "block_2"),

// Attack Buffs
            new BuffSpell("Minor Strengthen", @"\
Raise an ally's Physical Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.", 
    3, 2, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "attk", "strength_1"),

            new BuffSpell("Minor Empower", @"\
Raise an ally's Magical Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.", 
    3, 4, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "m_attk", "power_1"),

            new BuffSpell("Minor Aim", @"\
Raise an ally's Pierce Attack by 15%. Stacks with multiple uses. Lasts until the end
of battle.", 
    3, 6, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.any }, 0.15, "p_attk", "aim_1"),

            new BuffSpell("Adept Strengthen", @"\
Raise an ally's Physical Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.", 
    6, 13, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, 0.3, "attk", "strength_2"),

            new BuffSpell("Adept Empower", @"\
Raise an ally's Magical Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.", 
    6, 15, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, 0.3, "m_attk", "power_2"),

            new BuffSpell("Adept Aim", @"\
Raise an ally's Pierce Attack by 30%. Stacks with multiple uses. Lasts until the end
of battle.", 
    6, 17, new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, 0.3, "p_attk", "aim_2"),
        };

        public static bool PickSpellCategory(PlayableCharacter user, bool is_battle)
        {
            /*
            inv_name = user.name if user != units.player else 'player'

            while True:
                do_continue = False
                print(f"{user.name}'s spellbook:
              [1] Damaging Spells
              [2] Buff Spells
              [3] Healing Spells")

                if spellbook[inv_name]['Previous Spell']:
                    print(f"      [4] Re-cast {spellbook[inv_name]['Previous Spell'][0].name}")

                spam = True
                while spam:
                    cat = main.s_input('Input [#] (or type "exit"): ).lower()

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
                            user.choose_target(f"Who should {user.name} cast {spell.name} on?", ally= True, enemy= False)

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
                        print(f'You do not yet have any spells in the {cat} category.)
                        print('-'*save_load.divider_size)
                        continue

                    if pick_spell(cat, user, is_battle) :
                        return True

                    break */
        }

        public static bool PickSpell(CEnums.SpellCategory category, PlayableCharacter user, bool is_battle)
        {
            /*
            inv_name = user.name if user != units.player else 'player'

            print("-'*save_load.divider_size)
            while True:
                padding = len(max([spell.name for spell in spellbook[inv_name][cat]], key= len))
                print(f"{user.name}'s {cat} Spells | {user.mp}/{user.max_mp} MP remaining")

                // Print the player's spell inventory
                for x, y in enumerate(spellbook[inv_name][cat]) :
                    print(f"      [{x + 1}] {y.name} --{'-'*(padding - len(y.name))}> {y.mana} MP")

                while True:
                    spell = main.s_input("Input [#] (or type "back"): ).lower()

                    try:
                        spell = spellbook[inv_name][cat][int(spell) - 1]

                    except(IndexError, ValueError):
                        if spell in ['e', 'x', 'exit', 'b', 'back']:
                            print("-'*save_load.divider_size)

                            return False

                        continue

                    // Of course, you can't cast spells without the required amount of MP
                    if spell.mana > user.mp:
                        print("-'*save_load.divider_size)
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

                        break */
        }

        public static void GiveCharacterNewSpells(PlayableCharacter pcu)
        {
            /*
            // Teach the player new spells as they level up, or low-level spells not previously in the game.
            for spell in all_spells:
                if isinstance(spell, Damaging) :
                    cat = 'Damaging'
                elif isinstance(spell, Healing) or spell.name == 'Relieve Affliction':
                    cat = 'Healing'
                elif isinstance(spell, Buff):
                    cat = 'Buffs'
                else:
                    continue

                // Only give the character spells that they are a high enough level for
                if character.lvl >= spell.req_lvl:
                    for x in spellbook[character.name if character != units.player else 'player'][cat]:
                        if x.name == spell.name:
                            break

                    else:
                        // Almost all spells can be learned by mages, but only a few can be learned by other classes
                        if (character.class_ not in spell.class_) and spell.class_:
                            continue

                        if not save_load.do_blip:
                            sounds.item_pickup.play()

                        spellbook[character.name if character != units.player else 'player'][cat].append(spell)

                        main.s_input(f'{character.name} has learned "{spell.name}", a new {cat} spell!) */

        }
    }

    public abstract class Spell
    {
        public string SpellName { get; set; }
        public string Description { get; set; }
        public int ManaCost { get; set; }
        public int RequiredLevel { get; set; }
        public List<CEnums.CharacterClass> AllowedClasses { get; set; }
        public string SpellID { get; set; }

        public abstract void UseMagic(PlayableCharacter user, bool is_battle);

        public void SpendMana(PlayableCharacter user)
        {
            user.MP -= ManaCost;
            user.FixAllStats();
        }
    }

    public class HealingSpell : Spell
    {
        // Healing spells will always restore a minimum of target.HP*HealthIncreasePercent.
        // e.g. A spell that heals 20 HP but has a 20% HIP will restore 20 HP for someone
        // with 45 max HP, but will restore 32 HP for someone with 160 max HP.
        // In addition to this, the target restores an additional 1 HP for every point of wisdom the user has
        public int HealthIncreaseFlat { get; set; }
        public double HealthIncreasePercent { get; set; }

        public override void UseMagic(PlayableCharacter user, bool is_battle)
        {
            SpendMana(user);
            Unit target = user.CurrentTarget;

            int total_heal;

            if (HealthIncreaseFlat < target.MaxHP * HealthIncreasePercent)
            {
                total_heal = (int)(target.MaxHP * HealthIncreasePercent + user.Attributes["wis"]);
            }

            else
            {
                total_heal = HealthIncreaseFlat + user.Attributes["wis"];
            }

            target.HP += total_heal;
            target.FixAllStats();

            if (is_battle)
            {
                Console.WriteLine($"{user.Name} is making a move!\n");
                Console.WriteLine($"{user.Name} is preparing to cast {SpellName}...");

                SoundManager.ability_cast.Play();
                CMethods.SmartSleep(750);

                Console.WriteLine($"Using {SpellName}, {target.Name} is healed by {total_heal} HP!");
                SoundManager.magic_healing.Play();
            }

            else
            {
                CMethods.PrintDivider();

                Console.WriteLine($"Using {SpellName}, {target.Name} is healed by {total_heal} HP!");
                SoundManager.magic_healing.Play();
                CMethods.PressEnterReturn();

                CMethods.PrintDivider();
            }
        }

        public HealingSpell(string spell_name, string desc, int mana, int req_lvl, List<CEnums.CharacterClass> classes,
            int hp_flat, double hp_perc, string spell_id) : base()
        {
            SpellName = spell_name;
            Description = desc;
            ManaCost = mana;
            RequiredLevel = req_lvl;
            AllowedClasses = classes;
            HealthIncreaseFlat = hp_flat;
            HealthIncreasePercent = hp_perc;
            SpellID = spell_id;
        }
    }

    public class AttackSpell : Spell
    {
        // Damaging spells are spells that deal damage to the enemy during battle.
        // Just like normal attacks, they have a chance to miss based on
        // the enemy's evasion stat.
        public double SpellPower { get; set; }
        public CEnums.Element OffensiveElement { get; set; }

        public override void UseMagic(PlayableCharacter user, bool is_battle)
        {
            SpendMana(user);
            Unit target = user.CurrentTarget;
            Random rng = new Random();

            Console.WriteLine($"{user.Name} is making a move!\n");
            Console.WriteLine($"{user.Name} attempts to summon a powerful spell...");

            SoundManager.magic_attack.Play();
            CMethods.SmartSleep(750);

            int attack_damage = UnitManager.CalculateDamage(user, target, CEnums.DamageType.magical, spell_power: SpellPower);

            if (target.Evasion < rng.Next(0, 512))
            {
                SoundManager.enemy_hit.Play();
                target.HP -= attack_damage;
                Console.WriteLine($"{user.Name}'s attack connects with the {target.Name}, dealing {attack_damage} damage!");
            }

            else
            {
                SoundManager.attack_miss.Play();
                Console.WriteLine($"The {target.Name} narrowly dodges {user.Name}'s spell!");
            }
        }

        public AttackSpell(string spell_name, string desc, int mana, int req_lvl, List<CEnums.CharacterClass> classes,
            double spell_power, CEnums.Element element, string spell_id) : base()
        {
            SpellName = spell_name;
            Description = desc;
            ManaCost = mana;
            RequiredLevel = req_lvl;
            AllowedClasses = classes;
            SpellPower = spell_power;
            OffensiveElement = element;
            SpellID = spell_id;
        }
    }

    public class BuffSpell : Spell
    {
        // Buffs are spells that temporarily raise the player's stats during battle. They last until the battle
        // is over, at which point the player's stats will return to normal.
        public double IncreaseAmount { get; set; }
        public string Stat { get; set; }

        public override void UseMagic(PlayableCharacter user, bool is_battle)
        {
            SpendMana(user);
            Unit target = user.CurrentTarget;

            Console.WriteLine($"{user.Name} is making a move!\n");
            Console.WriteLine($"{user.Name} is preparing to cast {SpellName}...");
            SoundManager.ability_cast.Play();
            CMethods.SmartSleep(750);

            if (target == user)
            {
                Console.WriteLine($"{user.Name} raises their stats using the power of {SpellName}!");
            }

            else
            {
                Console.WriteLine($"{user.Name} raises {target.Name}'s stats using the power of {SpellName}!");
            }

            SoundManager.buff_spell.Play();

            // We write to TempStats instead of the player's actual stats so that the changes will
            // not persist after battle
            target.TempStats[Stat] = (int)(target.TempStats[Stat] * (1 + IncreaseAmount));
        }

        public BuffSpell(string spell_name, string desc, int mana, int req_lvl, List<CEnums.CharacterClass> classes,
            double increase, string stat, string spell_id) : base()
        {
            SpellName = spell_name;
            Description = desc;
            ManaCost = mana;
            RequiredLevel = req_lvl;
            AllowedClasses = classes;
            IncreaseAmount = increase;
            Stat = stat;
            SpellID = spell_id;
        }
    }
}