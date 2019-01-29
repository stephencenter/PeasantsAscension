using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    public static class UnitManager
    {
        // Unit manager is responsible for storing PCUs and generating monsters, as well as 
        // performing basic methods with units such as calculating damage
        public static PlayableCharacter player = new PlayableCharacter("John", CEnums.CharacterClass.warrior, "_player", true);
        public static PlayableCharacter solou = new PlayableCharacter("Solou", CEnums.CharacterClass.mage, "_solou", true);
        public static PlayableCharacter chili = new PlayableCharacter("Chili", CEnums.CharacterClass.ranger, "_chili", true);
        public static PlayableCharacter chyme = new PlayableCharacter("Chyme", CEnums.CharacterClass.monk, "_chyme", false);
        public static PlayableCharacter storm = new PlayableCharacter("Storm", CEnums.CharacterClass.assassin, "_storm", false);
        public static PlayableCharacter parsto = new PlayableCharacter("Parsto", CEnums.CharacterClass.paladin, "_parsto", false);
        public static PlayableCharacter adorine = new PlayableCharacter("Adorine", CEnums.CharacterClass.warrior, "_adorine", false);
        public static PlayableCharacter kaltoh = new PlayableCharacter("Kaltoh", CEnums.CharacterClass.bard, "_kaltoh", false);

        public static Dictionary<CEnums.MonsterGroup, List<Monster>> MonsterGroups = new Dictionary<CEnums.MonsterGroup, List<Monster>>()
        {
            {
                CEnums.MonsterGroup.animal, new List<Monster>()
                {
                    new FireAnt(), new FrostBat(), new SparkBat(), new SludgeRat(), new GiantLandSquid(),
                    new GiantCrab(), new SnowWolf(), new Beetle(), new VineLizard(), new GirthWorm()
                }
            },

            {
                CEnums.MonsterGroup.monster, new List<Monster>()
                {
                    new Willothewisp(), new Alicorn(), new BogSlime(),
                    new SandGolem(), new Griffin(), new Harpy(), new SeaSerpent(), new NagaBowwoman()
                }
            },

            {
                CEnums.MonsterGroup.humanoid, new List<Monster>()
                {
                    new Troll(), new MossOgre(), new LesserYeti(), new RockGiant(), new GoblinArcher(),
                    new Oread(), new TenguRanger(), new Naiad(), new Imp(), new Spriggan()
                }
            },

            {
                CEnums.MonsterGroup.undead, new List<Monster>()
                {
                    new Zombie(), new UndeadCrossbowman(), new LightningGhost(), new Mummy(), new SkeletonBoneslinger(), new WindWraith()
                }
            },

            {
                CEnums.MonsterGroup.dungeon, new List<Monster>()
                {
                    new Necromancer(), new CorruptThaumaturge(), new IceSoldier(), new FallenKnight(), new DevoutProtector()
                }
            }
        };

        // Returns ALL PCUs, alive, dead, active, and inactive
        public static List<PlayableCharacter> GetAllPCUs()
        {
            return new List<PlayableCharacter>() { player, solou, chili, chyme, storm, parsto, adorine, kaltoh };
        }

        // Returns all PCUs that are alive, regardless of whether they're active or not
        public static List<PlayableCharacter> GetAlivePCUs()
        {
            return GetAllPCUs().Where(x => x.IsAlive()).ToList();
        }

        // Returns all PCUs that are active, regardless of whether they're alive or not
        public static List<PlayableCharacter> GetActivePCUs()
        {
            return GetAllPCUs().Where(x => x.Active).ToList();
        }

        // Returns all PCUs that are both alive and active
        public static List<PlayableCharacter> GetAliveActivePCUs()
        {
            return GetAllPCUs().Where(x => x.Active && x.IsAlive()).ToList();
        }

        public static Monster GenerateMonster()
        {
            // Get a list of all the monster groups that this cell has in its MonsterGroups property
            List<CEnums.MonsterGroup> cell_groups = TileManager.FindCellWithTileID(CInfo.CurrentTile).MonsterGroups;

            // Create a new empty list of monsters
            List<Monster> monsters = new List<Monster>() { };

            // Add all the monsters from the cell_groups to the monster list
            cell_groups.ForEach(x => monsters = monsters.Concat(MonsterGroups[x]).ToList());

            // Choose a random monster type from the list and create a new monster out of it
            Type type = CMethods.GetRandomFromIterable(monsters).GetType();
            Monster new_monster = Activator.CreateInstance(type) as Monster;

            // Level-up the monster to increase its stats to the level of the cell that the player is in
            new_monster.MonsterLevelUp();

            // Apply multipliers to the monster based on its species, class, and party difficulty
            new_monster.MonsterApplyMultipliers();

            // The new monster has been generated - we now return it
            return new_monster;
        }

        public static int CalculateDamage(Unit attacker, Unit target, CEnums.DamageType damage_type, double spell_power = 0, bool do_criticals = true)
        {
            // Attacker - the Unit that is attacking
            // Target - the Unit that is being attacked
            // Damage Type - the type of damage being dealt (magical, physical, or piercing)
            Random rng = new Random();

            int attack;
            int p_attack;
            int m_attack;

            int defense;
            int p_defense;
            int m_defense;

            double weapon_power;
            double armor_resist;

            int final_damage;

            if (attacker is PlayableCharacter)
            {
                weapon_power = InventoryManager.GetEquipment(attacker.UnitID)[CEnums.EquipmentType.weapon].Power;

                attack = attacker.TempStats["attack"];
                p_attack = attacker.TempStats["p_attack"];
                m_attack = attacker.TempStats["m_attack"];
            }

            else
            {
                attack = attacker.Attack;
                p_attack = attacker.PAttack;
                m_attack = attacker.MAttack;

                weapon_power = 0;
            }

            if (target is PlayableCharacter)
            {
                double a = InventoryManager.GetEquipment(target.UnitID)[CEnums.EquipmentType.head].Resist;
                double b = InventoryManager.GetEquipment(target.UnitID)[CEnums.EquipmentType.body].Resist;
                double c = InventoryManager.GetEquipment(target.UnitID)[CEnums.EquipmentType.legs].Resist;
                armor_resist = a + b + c;

                defense = target.TempStats["defense"];
                p_defense = target.TempStats["p_defense"];
                m_defense = target.TempStats["m_defense"];
            }

            else
            {
                defense = target.Defense;
                p_defense = target.PDefense;
                m_defense = target.PAttack;

                armor_resist = 0;
            }

            if (damage_type == CEnums.DamageType.physical)
            {
                final_damage = (int)((attack - defense / 2) * (1 + armor_resist) * (1 + weapon_power));

                // Weakeness reduces physical damage by 1/2
                if (attacker.HasStatus(CEnums.Status.weakness))
                {
                    final_damage /= 2;
                    Console.WriteLine($"{attacker.Name}'s weakness reduces their attack damage by half!");
                }
            }

            else if (damage_type == CEnums.DamageType.physical)
            {
                final_damage = (int)((p_attack - p_defense / 2) * (1 + armor_resist) * (1 + weapon_power));

                // Blindness reduces piercing damage by 1/2
                if (attacker.HasStatus(CEnums.Status.blindness))
                {
                    final_damage /= 2;
                    Console.WriteLine($"{attacker.Name}'s blindness reduces their attack damage by half!");
                }
            }

            else
            {
                // Spell damage is affected by Spell Power (which is specific to the spell) rather than weapon power
                final_damage = (int)((m_attack - m_defense / 2) * (1 + armor_resist) * (1 + spell_power));
            }

            if (rng.Next(0, 100) < 15 && do_criticals)
            {
                final_damage = (int)(final_damage * 1.5);
                SoundManager.critical_hit.Play();
                Console.WriteLine("It's a critical hit! 1.5x damage!");

                CMethods.SmartSleep(500);
            }

            final_damage = ApplyElementalChart(attacker, target, final_damage);
            final_damage = (int)CMethods.Clamp(final_damage, 1, 999);

            return final_damage;
        }

        public static int ApplyElementalChart(Unit attacker, Unit target, int damage)
        {
            // Fire > Ice > Grass > Wind > Electricity > Earth > Water > Fire
            // Light > Dark and Dark > Light, Dark and Light resist themselves
            // Neutral element is neutral both offensively and defensively
            // All other interactions are neutral

            CEnums.Element attacker_element = attacker.OffensiveElement;
            CEnums.Element target_element = target.DefensiveElement;

            // If either the attacker or the target is neutral element, then damage will not be modified
            if (attacker_element == CEnums.Element.neutral || target_element == CEnums.Element.neutral)
            {
                return damage;
            }

            // If the target is weak to the attackers element, then the attack will deal 1.5x damage
            if (CEnums.ElementChart[attacker_element][1] == target_element)
            {
                return (int)(damage * 1.5);
            }

            else if (CEnums.ElementChart[attacker_element][0] == target_element)
            {
                return (int)(damage / 1.5);
            }

            return damage;
        }

        public static void HealAllPCUs(double heal_percentage, bool restore_hp, bool restore_mp, bool restore_ap)
        {
            foreach (PlayableCharacter pcu in GetAllPCUs())
            {
                if (restore_hp)
                {
                    pcu.HP = (int)(pcu.MaxHP * heal_percentage);
                }

                if (restore_mp)
                {
                    pcu.MP = (int)(pcu.MaxMP * heal_percentage);
                }

                if (restore_ap)
                {
                    pcu.AP = (int)(pcu.MaxAP * heal_percentage);
                }

                pcu.FixAllStats();
            }
        }
    }

    public abstract class Unit
    {
        /* =========================== *
         *      GENERAL PROPERTIES     *
         * =========================== */
        public string UnitID { get; set; }
        public CEnums.Element OffensiveElement = CEnums.Element.neutral;
        public CEnums.Element DefensiveElement = CEnums.Element.neutral;
        public List<CEnums.Status> Statuses = new List<CEnums.Status> { CEnums.Status.alive };

        public string Name { get; set; }
        public int HP { get; set; }
        public int MaxHP { get; set; }
        public int MP { get; set; }
        public int MaxMP { get; set; }
        public int AP { get; set; }
        public int MaxAP { get; set; }
        public int Attack { get; set; }
        public int Defense { get; set; }
        public int PAttack { get; set; }
        public int PDefense { get; set; }
        public int MAttack { get; set; }
        public int MDefense { get; set; }
        public int Speed { get; set; }
        public int Evasion { get; set; }
        public int Level { get; set; }

        public Dictionary<string, int> TempStats = new Dictionary<string, int>()
        {
            { "attack", 0 },
            { "defense", 0 },
            { "p_attack", 0 },
            { "p_defense", 0 },
            { "m_attack", 0 },
            { "m_defense", 0 },
            { "speed", 0 },
            { "evasion", 0 }
        };

        /* =========================== *
         *           METHODS           *
         * =========================== */
        public bool IsAlive()
        {
            return HasStatus(CEnums.Status.alive);
        }

        public bool IsDead()
        {
            return HasStatus(CEnums.Status.dead);
        }

        public void SetTempStats()
        {
            TempStats["attack"] = Attack;
            TempStats["defense"] = Defense;
            TempStats["p_attack"] = PAttack;
            TempStats["p_defense"] = PDefense;
            TempStats["m_attack"] = MAttack;
            TempStats["m_defense"] = MDefense;
            TempStats["speed"] = Speed;
            TempStats["evasion"] = Evasion;
        }

        public bool HasStatus(CEnums.Status status)
        {
            return Statuses.Contains(status);
        }

        public void FixAllStats()
        {
            // Makes sure that that no-one ever has stats that would cause the game to malfunction.
            // e.g. no negative HP/MP/AP, no HP/MP/AP above max, etc.
            // This function also acts as a hard-cap for evasion, which is limited to a max of 256
            // (50% dodge chance). This is to prevent people from min-maxing their evasion to cheese
            // their way through the game, and also prevents monsters from being invincible.

            // Initialize the Common Methods manager

            HP = (int)CMethods.Clamp(HP, 0, MaxHP);
            MP = (int)CMethods.Clamp(MP, 0, MaxMP);
            AP = (int)CMethods.Clamp(AP, 0, MaxAP);

            Attack = Math.Max(1, Attack);
            PAttack = Math.Max(1, PAttack);
            MAttack = Math.Max(1, MAttack);

            Defense = Math.Max(1, Defense);
            PDefense = Math.Max(1, PDefense);
            MDefense = Math.Max(1, MDefense);

            Speed = Math.Max(1, Speed);
            Evasion = (int)CMethods.Clamp(Evasion, 1, 256);

            Statuses = Statuses.Distinct().ToList();

            if (HP > 0 && !IsAlive())
            {
                Statuses = new List<CEnums.Status>() { CEnums.Status.alive };
            }

            if (HP == 0 && !IsDead())
            {
                Statuses = new List<CEnums.Status>() { CEnums.Status.dead };
            }
        }
    }

    public class PlayableCharacter : Unit
    {
        public CEnums.CharacterClass PClass { get; set; }
        public bool Active { get; set; }
        public int CurrentXP { get; set; }
        public int RequiredXP { get; set; }
        public char CurrentMove { get; set; }
        public Unit CurrentTarget { get; set; }
        public Ability CurrentAbility { get; set; }
        public Spell CurrentSpell { get; set; }

        public Dictionary<string, int> Attributes = new Dictionary<string, int>()
        {
            { "int", 1 },
            { "wis", 1 },
            { "str", 1 },
            { "con", 1 },
            { "dex", 1 },
            { "per", 1 },
            { "cha", 1 },
            { "fte", 1 }
        };

        public Dictionary<string, dynamic> PlayerAbilityFlags = new Dictionary<string, dynamic>()
        {
            {"ascend_used", false },
            {"berserk", false },
            {"rolling", false }
        };

        /* =========================== *
         *        PLAYER METHODS       *
         * =========================== */
        public void PlayerChooseName()
        {
            /*
            while True:
                // Ask the player for their name, and remove any non alphanumeric/dash characters from it
                // Also remove beginning/ending whitespace, and repeated spaces
                choice1 = main.s_input('What is your name, young adventurer? | Input Name: ')
                choice2 = ' '.join(re.sub('[^\w\-_ ]', '', choice1).split())

                // If your original choice contained characters, but the filtered version didn't,
                // this message will pop up.
                if choice1 and not choice2:
                    Console.WriteLine("I'm sorry, I didn't quite catch that.")
                    main.s_input('\nPress enter/return ')
                    Console.WriteLine('-'*save_load.divider_size)
                    continue

                // You can't name yourself nothing. Sorry but that's the rules.
                if not(choice1 or choice2) :
                    continue

                self.name = choice2

                while True:
                    if self.name.lower() == 'y':
                        Console.WriteLine("""Your name's "y", eh? Must be in a hurry.""")
                        main.s_input('\nPress enter/return ')
                        Console.WriteLine('-' * save_load.divider_size)

                    elif self.name.lower() in main.friend_names:
                        Console.WriteLine($"Ah, {self.name}! My dear friend, it is great to see you again!")
                        main.s_input('\nPress enter/return ')
                        Console.WriteLine('-' * save_load.divider_size)

                    elif self.name.lower() == "frisk":
                        Console.WriteLine("Frisk? Sorry, no hard mode for you in this game.")
                        main.s_input('\nPress enter/return ')
                        Console.WriteLine('-' * save_load.divider_size)

                    else:
                        y_n = main.s_input($"So, your name is "{self.name}?" | Y/N: ').lower()

                        if y_n.startswith('n'):
                            Console.WriteLine('-'*save_load.divider_size)
                            self.name = ''
                            break

                        elif not y_n.startswith('y'):
                            continue

                        Console.WriteLine('-'*save_load.divider_size)

                    return */
        }

        public void PlayerChooseClass()
        {
            /*
            while True:
                class_ = main.s_input($"""{self.name}, which class would you like to train as?
          [1] Mage: Master of the arcane arts
          [2] Assassin: Proficient in both stealth and murder
          [3] Ranger: Fast and evasive, good with a bow
          [4] Paladin: Holy knight whose healing prowess is unmatched
          [5] Monk: Fighter whose fists are a worthy oppenent to any blade
          [6] Warrior: Excellent soldier, good balance of offense and defense
          [7] Bard: True team-player and master musician
    Input[#]: """)

                try:
                    class_ = {'1': "mage",
                              '2': "assassin",
                              '3': "ranger",
                              '4': "paladin",
                              '5': "monk",
                              '6': "warrior",
                              '7': "bard"}
        [class_]

        class_desc = {'mage': """\
        -Can use abilities that scale off Intelligence
        -Capable of learning every spell
        -Deals Pierce Damage with Standard Attacks
        -Deals 50% damage with Standard Attacks
        -High Magical Attack/Defense and MP
        -Average HP, Speed, and Evasion
        -Low Pierce Attack and Pierce/Physical Defense""",

                                  'assassin': """\
        -Can use abilities that scale off Dexterity
        -Deals Physical Damage with Standard Attacks
        -Deals 75% damage with Magical Spells
        -High Speed, Physical Attack, and Evasion
        -Average HP, Pierce Defense, and Physical Defense
        -Low Magical Attack/Defense and MP""",

                                  'ranger': """\
        -Can use abilities that scale off Perception
        -Deals Pierce Damage with Standard Attacks
        -Deals 75% damage with Magical Spells
        -High Pierce Attack, Speed, and Evasion
        -Average MP, HP, and Pierce Defense
        -Low HP, Pierce/Physcial Defense, and Magical Attack""",

                                  'paladin': """\
        -Can use abilities that scale off Wisdom
        -Can learn all Healing spells and offensive Light spells
        -Deals Physical Damage with Standard Attacks
        -High Magical/Physical Defense
        -Average MP, HP, and Pierce Defense
        -Low Physical/Magical Attack, Speed, and Evasion""",

                                  'monk': """\
        -Can use abilities that scale off Constitution
        -Capable of learning all Buff spells
        -Deals Physical damage with Standard Attacks
        -Deals 75% damage with Magical Spells
        -High Physical Attack, Speed, and Evasion
        -Average MP and Magical Attack
        -Low Pierce/Physical Defense and HP""",

                                  'warrior': """\
        -Can use abilities that scale off Strength
        -Deals Physical Damage with Standard Attacks
        -Deals 75% damage with Magical Spells
        -High Pierce/Physical Defense and Physical Attack
        -Average HP
        -Low Magical Attack/Defense, Speed, Evasion, and MP""",

                                  'bard': """\
        -Can use abilities that scale of Charisma
        -Deals Magical Damage with Standard Attacks
        -Deals 75% damage with Magical Spells
        -Has 6 Abilities instead of 4
        -High Evasion
        -Average MP, Speed, and Magical Defense
        -Low HP, Magical Attack, and Physical/Pierce Defense"""}[class_]

                except KeyError:
                    continue

                Console.WriteLine('-'*save_load.divider_size)
                Console.WriteLine($"Information about {class_.title()}s: ")
                Console.WriteLine(class_desc)
                Console.WriteLine('-'*save_load.divider_size)

                while True:
                    y_n = main.s_input($"You wish to be of the {class_.title()} class? | Y/N: ').lower()

                    if y_n.startswith('y'):
                        Console.WriteLine('-'*save_load.divider_size)
                        self.class_ = class_

                        return

                    elif y_n.startswith('n'):
                        Console.WriteLine()
                        break */
        }

        public void PlayerLevelUp()
        {
            if (CurrentXP >= RequiredXP)
            {
                // sounds.play_music('../Music/Adventures in Pixels.ogg')
                int remaining_skillpoints = 0;

                while (CurrentXP >= RequiredXP)
                {
                    Level++;
                    remaining_skillpoints += 3;

                    CMethods.PrintDivider();
                    Console.WriteLine($"{Name} has advanced to level {Level}!");

                    // Get a list of all the spells in the game
                    List<Spell> new_spells = SpellManager.GetSpellbook(CEnums.SpellCategory.all);

                    // Filter this list to only include the spells that the player was not previously able to use, and 
                    // that are usable by the player's class
                    new_spells = new_spells.Where(x => x.RequiredLevel == Level && 
                        (x.AllowedClasses.Contains(PClass) || x.AllowedClasses.Contains(CEnums.CharacterClass.any))).ToList();
                    
                    // Prompt the player of their new spells.
                    foreach (Spell spell in new_spells)
                    {
                        SoundManager.item_pickup.Play();
                        CMethods.Input($"{Name} has learned a new spell: {spell.SpellName}!");
                    }

                    if (PClass == CEnums.CharacterClass.warrior)
                    {
                        Attack += 3;
                        Defense += 3;
                        MAttack += 1;
                        MDefense += 1;
                        PAttack += 1;
                        PDefense += 3;
                        Speed += 1;
                        Evasion += 1;
                        MaxHP += 2;
                        MaxMP += 1;
                    }

                    else if (PClass == CEnums.CharacterClass.mage)
                    {
                        Attack += 1;
                        Defense += 1;
                        MAttack += 3;
                        MDefense += 1;
                        PAttack += 2;
                        PDefense += 3;
                        Speed += 1;
                        Evasion += 1;
                        MaxHP += 1;
                        MaxMP += 3;
                    }

                    else if (PClass == CEnums.CharacterClass.assassin)
                    {
                        Attack += 3;
                        Defense += 1;
                        MAttack += 1;
                        MDefense += 1;
                        PAttack += 1;
                        PDefense += 2;
                        Speed += 3;
                        Evasion += 3;
                        MaxHP += 1;
                        MaxMP += 1;
                    }

                    else if (PClass == CEnums.CharacterClass.ranger)
                    {
                        Attack += 1;
                        Defense += 1;
                        MAttack += 1;
                        MDefense += 1;
                        PAttack += 3;
                        PDefense += 1;
                        Speed += 3;
                        Evasion += 3;
                        MaxHP += 1;
                        MaxMP += 2;
                    }

                    else if (PClass == CEnums.CharacterClass.monk)
                    {
                        Attack += 3;
                        Defense += 1;
                        MAttack += 1;
                        MDefense += 1;
                        PAttack += 1;
                        PDefense += 1;
                        Speed += 3;
                        Evasion += 3;
                        MaxHP += 1;
                        MaxMP += 2;
                    }

                    else if (PClass == CEnums.CharacterClass.paladin)
                    {
                        Attack += 1;
                        Defense += 3;
                        MAttack += 1;
                        MDefense += 3;
                        PAttack += 1;
                        PDefense += 2;
                        Speed += 1;
                        Evasion += 1;
                        MaxHP += 2;
                        MaxMP += 2;
                    }

                    else if (PClass == CEnums.CharacterClass.bard)
                    {
                        Attack += 1;
                        Defense += 1;
                        MAttack += 1;
                        MDefense += 2;
                        PAttack += 1;
                        PDefense += 1;
                        Speed += 2;
                        Evasion += 3;
                        MaxHP += 1;
                        MaxMP += 2;
                    }

                    CurrentXP -= RequiredXP;
                    RequiredXP = (int)(Math.Pow(Level * 2, 2) - Level);
                    FixAllStats();
                }
            // The player restores all their health and mana when they level up
            HP = MaxHP;
            MP = MaxMP;
            Statuses = new List<CEnums.Status>() { CEnums.Status.alive };

            CMethods.PrintDivider();
            PlayerAllocateSkillPoints();
            CMethods.PrintDivider();
            SavefileManager.SaveTheGame();
            }
        }

        public void PlayerAllocateSkillPoints()
        {
            /*
            while rem_points > 0:
            Console.WriteLine($"{self.name} has {rem_points} skill point{'s' if rem_points > 1 else ''} left to spend.")

            skill = main.s_input("""Choose a skill to increase:
        [1] INTELLIGENCE, The attribute of MAGES
        [2] WIDSOM, the attribute of PALADINS
        [3] STRENGTH, The attribute of WARRIORS
        [4] CONSTITUTION, the attribute of MONKS
        [5] DEXTERITY, the attribute of ASSASSINS
        [6] PERCEPTION, the attribute of RANGERS
        [7] CHARISMA, the attribute of BARDS
        [8] FATE, the forgotten attribute
        [9] DIFFICULTY, the forbidden attribute
Input[#]: """).lower()

            if skill and skill[0] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                if skill[0] == '1':
                    act_skill = 'int'
                    vis_skill = 'INTELLIGENCE'
                    message = """\
Increasing INTELLIGENCE will provide:
    +1 Magical Attack
    +1 Magical Defense
    +1 MP
    +Mage Ability Power"""

                elif skill[0] == '2':
                    act_skill = 'wis'
                    vis_skill = 'WISDOM'
                    message = """\
Increasing WISDOM will provide:
    +1 Heal from healing spells(Non-paladins)
    +2 MP
    +Paladin Ability Power"""

                elif skill[0] == '3':
                    act_skill = 'str'
                    vis_skill = 'STRENGTH'
                    message = """\
Increasing STRENGTH will provide:
    +1 Physical Attack
    +1 Physical Defense
    +1 Pierce Defense
    +Warrior Ability Power"""

                elif skill[0] == '4':
                    act_skill = 'con'
                    vis_skill = 'CONSTITUTION'
                    message = """\
Increasing CONSTITUTION will provide:
    +1 HP
    +1 Physical Defense
    +1 Pierce Defense
    +1 Magical Defense
    +Monk Ability Power"""

                elif skill[0] == '5':
                    act_skill = 'dex'
                    vis_skill = 'DEXTERITY'
                    message = """\
Increasing DEXTERITY will provide:
    +1 Physical Attack
    +1 Speed
    +1 Evasion
    +Assassin Ability Power"""

                elif skill[0] == '6':
                    act_skill = 'per'
                    vis_skill = 'PERCEPTION'
                    message = """\
Increasing PERCEPTION will provide:
    +1 Pierce Attack
    +1 Pierce Defense
    +1 Evasion
    +Ranger Ability Power"""

                elif skill[0] == '7':
                    act_skill = 'cha'
                    vis_skill = 'CHARISMA'
                    message = """\
Increasing CHARISMA will provide:
    +Items cost 1% less(caps at 50% original cost)
    +Items sell for 1% more(caps at 200% original sell value)
    +Only the highest CHARISMA in party contributes to these
    +Bard Ability Power"""

                elif skill[0] == '8':
                    act_skill = 'fte'
                    vis_skill = 'FATE'
                    message = """\
Increasing FATE will provide:
    +1 to a random attribute(won't choose DIFFICULTY or FATE)
    +1 to a second random attribute (won't choose DIFFICULTY or FATE)
    +Knowledge that your destiny is predetermined and nothing matters"""

                elif skill[0] == '9':
                    act_skill = "dif"
                    vis_skill = "DIFFICULTY"
                    message = """\
Increasing DIFFICULTY will provide:
    +0.5% Enemy Physical Attack (Applies to entire party)
    +0.5% Enemy Pierce Attack(Applies to entire party)
    +0.5% Enemy Magical Attack(Applies to entire party)
    +More challenging experience"""

                else:
                    continue

                Console.WriteLine('-'*save_load.divider_size)

                if act_skill == "dif":
                    Console.WriteLine($"Current {vis_skill}: {main.party_info["dif"]}")

                else:
                    Console.WriteLine($"Current {vis_skill}: {self.attributes[act_skill]}")

                Console.WriteLine(message)
                Console.WriteLine('-'*save_load.divider_size)

                while True:
                    y_n = main.s_input($"Increase {self.name}'s {vis_skill}? | Y/N: ").lower()

                    if y_n.startswith('n'):
                        Console.WriteLine('-'*save_load.divider_size)
                        break

                    elif y_n.startswith('y'):
                        self.increase_attribute(act_skill)

                    else:
                        continue

                    if act_skill == "dif":
                        Console.WriteLine('-'*save_load.divider_size)
                        Console.WriteLine("Difficulty increased!")
                        Console.WriteLine("The enemies of your world have grown in power!")

                    if act_skill != 'fte':
                        Console.WriteLine('-'*save_load.divider_size)
                        Console.WriteLine($"{self.name}'s {vis_skill} has increased!")

                    // Decrement remaining points
    rem_points -= 1

                    Console.WriteLine('-'*save_load.divider_size) if rem_points else ''

                    break

        Console.WriteLine($"\n{self.name} is out of skill points.') */
        }

        public void PlayerViewStats()
        {
            /*
            fix_stats()

            m_w = { 'fire': 'water',
                    'water': 'electric',
                    'electric': 'earth',
                    'earth': 'wind',
                    'wind': 'grass',
                    'grass': 'ice',
                    'ice': 'fire',
                    'neutral': 'neutral',
                    'light': 'dark',
                    'dark': 'light'}
    [self.def_element]

            Console.WriteLine($"""-{self.name}'s Stats-
    Level { self.lvl} {self.class_.title()
        }
        Statuses: {', '.join([x.title() for x in self.status_ail])}
    XP: {self.exp}/{self.req_xp} / GP: {main.party_info['gp']}

    HP: {self.hp}/{self.max_hp} / MP: {self.mp}/{self.max_mp} / AP: {self.ap}/{self.max_ap}
    Physical: {self.attk} Attack / {self.dfns} Defense
    Magical: {self.m_attk} Attack / {self.m_dfns} Defense
    Piercing: {self.p_attk} Attack / {self.p_dfns} Defense
    Speed: {self.spd}
    Evasion: {self.evad}
    Elements: Attacks are { self.off_element.title()} / Defense is {self.def_element.title()} / \
    Weak to { m_w.title()}

    Intelligence: {self.attributes['int']} 
    Wisdom: {self.attributes['wis']}
    Strength: {self.attributes['str']}
    Constitution: {self.attributes['con']}
    Dexterity: {self.attributes['dex']}
    Perception: {self.attributes['per']}
    Charisma: {self.attributes['cha']}
    Difficulty: {main.party_info["dif"]}""") 
            main.s_input('\nPress enter/return ')*/
        }

        public void PrintBattleOptions()
        {
            Console.WriteLine($"Pick {Name}'s Move:");
            Console.WriteLine("      [1] Standard Attack");
            Console.WriteLine("      [2] Use Magic");
            Console.WriteLine("      [3] Use Abilities");
            Console.WriteLine("      [4] Use Items");
            Console.WriteLine("      [5] Run");
        }

        public void PlayerChoice(List<Monster> monster_list)
        {
            PrintBattleOptions();

            while (true)
            {
                string c_move = CMethods.Input("Input [#]: ");

                try
                {
                    CurrentMove = c_move[0];
                }

                catch (IndexOutOfRangeException)
                {
                    continue;
                }

                // Attack
                if (CurrentMove == '1')
                {
                    if (!PlayerGetTarget(monster_list, $"Who should {Name} attack?", false, true, false, false))
                    {
                        PrintBattleOptions();
                        continue;
                    }

                    return;
                }

                // Magic
                else if (CurrentMove == '2')
                {
                    CMethods.PrintDivider();

                    // Silence is a status ailment that prevents using spells
                    if (HasStatus(CEnums.Status.silence))
                    {
                        SoundManager.debuff.Play();
                        Console.WriteLine($"{Name} can't use spells when silenced!");
                        CMethods.PressEnterReturn();
                        PrintBattleOptions();

                        continue;
                    }

                    if (!SpellManager.PickSpellCategory(this, monster_list, true))
                    {
                        PrintBattleOptions();
                        continue;
                    }

                    return;
                }

                // Ability
                else if (CurrentMove == '3')
                {
                    if (PlayerChooseAbility())
                    {
                        return;
                    }
                }

                // Use Items
                else if (CurrentMove == '4')
                {
                    CMethods.PrintDivider();

                    var x = new List<int>();
                    if (!InventoryManager.GetInventory()["consumables"].Any())
                    {
                        SoundManager.debuff.Play();
                        Console.WriteLine("Your party has no consumables!");

                        CMethods.PressEnterReturn();
                        CMethods.PrintDivider();
                        PrintBattleOptions();

                        continue;
                    }

                    if (HasStatus(CEnums.Status.muted))
                    {
                        SoundManager.debuff.Play();
                        Console.WriteLine($"{Name} can't use items when muted!");

                        CMethods.PressEnterReturn();
                        CMethods.PrintDivider();
                        PrintBattleOptions();

                        continue;
                    }

                    if (!BattleManager.BattleInventory(this))
                    {
                        PrintBattleOptions();

                        continue;
                    }

                    CMethods.PressEnterReturn();
                    return;
                }

                // Run
                else if (CurrentMove == '5')
                {
                    return;
                }
            }
        }

        public string PlayerExecuteMove(List<Monster> monster_list)
        {
            Random rng = new Random();

            SoundManager.item_pickup.Stop();

            // If the player's target is an enemy, and the target died before the player's turn began,
            // then the attack automatically redirects to a random living enemy.
            if (CurrentTarget is Monster && !CurrentTarget.IsAlive())
            {
                CurrentTarget = CMethods.GetRandomFromIterable(monster_list.Where(x => x.IsAlive()));
            }

            Weapon player_weapon = InventoryManager.GetEquipment(UnitID)[CEnums.EquipmentType.weapon];

            Console.WriteLine($"-{Name}'s Turn-");

            // PCUs regenerate 1 Action Point per turn, unless they used an ability that turn
            if (CurrentMove != '3')
            {
                AP++;
            }

            if (HasStatus(CEnums.Status.poison))
            {
                CMethods.SmartSleep(750);

                SoundManager.poison_damage.Play();

                int poison_damage = HP / 5;
                HP -= poison_damage;

                Console.WriteLine($"{Name} took {poison_damage} damage from poison!");

                if (HP <= 0)
                {
                    return "";
                }
            }

            foreach (CEnums.Status status in Statuses)
            {
                // There is a 12.5% chance each turn per status ailment to be relived of that status ailment
                // Only one status can be cleared per turn
                if (status != CEnums.Status.alive && rng.Next(0, 8) == 0)
                {
                    SoundManager.buff_spell.Play();
                    Statuses.Remove(status);
                    Console.WriteLine($"{Name} is no longer {CEnums.EnumToString(status)}!");
                    CMethods.SmartSleep(500);

                    break;
                }
            }

            // Basic Attack
            if (CurrentMove == '1')
            {
                // TO-DO: Ascii art
                Console.WriteLine($"{Name} is making a move!\n");

                if (player_weapon.WeaponType == CEnums.WeaponType.melee)
                {
                    SoundManager.sword_slash.Play();
                    Console.WriteLine($"{Name} fiercely attacks the {CurrentTarget.Name} using their {player_weapon.Name}...");
                }

                else if (player_weapon.WeaponType == CEnums.WeaponType.instrument)
                {
                    SoundManager.bard_sounds[player_weapon.ItemID].Play();
                    Console.WriteLine($"{Name} starts playing their {player_weapon.Name} at the {CurrentTarget.Name}...");
                }

                else
                {
                    SoundManager.aim_weapon.Play();
                    Console.WriteLine($"{Name} aims carefully at the {CurrentTarget.Name} using their {player_weapon.Name}...");
                }

                CMethods.SmartSleep(750);

                int attack_damage;
                if (CEnums.CharacterClassToDamageType(PClass) == CEnums.DamageType.physical)
                {
                    attack_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.physical);
                }

                else if (CEnums.CharacterClassToDamageType(PClass) == CEnums.DamageType.piercing)
                {
                    attack_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.piercing);
                }

                else
                {
                    attack_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.magical);
                }

                if (CurrentTarget.Evasion < rng.Next(0, 512))
                {
                    Console.WriteLine($"{Name}'s attack connects with the {CurrentTarget.Name}, dealing {attack_damage} damage!");
                    SoundManager.enemy_hit.Play();
                    CurrentTarget.HP -= attack_damage;
                }

                else
                {
                    Console.WriteLine($"The {CurrentTarget.Name} narrowly avoids {Name}'s attack!");
                    SoundManager.attack_miss.Play();
                }
            }

            // Use Magic
            else if (CurrentMove == '2')
            {
                CurrentSpell.UseMagic(this, true);
            }

            // Use Ability
            else if (CurrentMove == '3')
            {
                // TO-DO: Ascii art
                Console.WriteLine($"{Name} is making a move!\n");
                CurrentAbility.UseAbility(this);
            }

            // Run away
            else if (CurrentMove == '5' && BattleManager.RunAway(this, monster_list))
            {
                // sounds.play_music(main.party_info['music'])
                return "ran";
            }

            return "";
        }

        public bool PlayerGetTarget(List<Monster> monster_list, string action_desc, bool target_allies, bool target_enemies, bool allow_dead, bool allow_inactive)
        {
            // A list of PCUs that are valid for targetting (could be unused if target_allies is false)
            List<PlayableCharacter> pcu_list;

            if (allow_inactive)
            {
                if (allow_dead)
                {
                    // YES to dead PCUs, YES to inactive PCUs
                    pcu_list = UnitManager.GetAllPCUs();
                }

                else
                {
                    // NO to dead PCUs, YES to inactive PCUs
                    pcu_list = UnitManager.GetAlivePCUs();
                }
            }

            else
            {
                if (allow_dead)
                {
                    // YES to dead PCUs, NO to inactive PCUs
                    pcu_list = UnitManager.GetActivePCUs();
                }

                else
                {
                    // NO to dead PCUs, NO to inactive PCUs
                    pcu_list = UnitManager.GetAliveActivePCUs();
                }
            }

            // The full list of valid targets, including both monsters and allies if applicable
            List<dynamic> valid_targets = new List<dynamic>();

            // Do this if both allies and enemies are valid targets (e.g. some abilities and spells)
            if (target_allies && target_enemies)
            {
                pcu_list.ForEach(x => valid_targets.Add(x));
                monster_list.ForEach(x => x.FixAllStats());
                monster_list.Where(x => x.IsAlive()).ToList().ForEach(x => valid_targets.Add(x));
            }

            // Do this if the player is allowed to target allies but not enemies (e.g. items, some spells/abilities)
            else if (target_allies && !target_enemies)
            {
                if (pcu_list.Count == 1)
                {
                    CurrentTarget = pcu_list[0];
                    return true;
                }

                pcu_list.ForEach(x => valid_targets.Add(x));
            }

            // Do this if the player is allowed to target enemies but not allies (e.g. attacks, some spells/abilities)
            else if (!target_allies && target_enemies)
            {
                if (monster_list.Where(x => x.IsAlive()).Count() == 1)
                {
                    CurrentTarget = monster_list.Where(x => x.IsAlive()).ToList()[0];
                    return true;
                }

                monster_list.Where(x => x.IsAlive()).ToList().ForEach(x => valid_targets.Add(x));
            }

            else
            {
                throw new Exception("Exception in 'choose_target': at least one of 'target_allies' or 'target_enemies' must be true");
            }

            CMethods.PrintDivider();
            Console.WriteLine(action_desc);

            int counter = 0;
            foreach (Unit unit in valid_targets)
            {
                Console.WriteLine($"      [{counter + 1}] {unit.Name}");
                counter++;
            }

            while (true)
            {
                string chosen = CMethods.Input("Input [#] (or type 'back'): ");

                try
                {
                    CurrentTarget = valid_targets[int.Parse(chosen) - 1];
                }

                catch (Exception ex)
                {
                    if (ex is FormatException || ex is ArgumentOutOfRangeException)
                    {
                        if (CMethods.IsExitString(chosen))
                        {
                            CMethods.PrintDivider();
                            return false;
                        }

                        continue;
                    }

                    else
                    {
                        throw ex;
                    }
                }

                return true;
            }
        }

        public bool PlayerChooseAbility()
        {
            while (true)
            {
                CMethods.PrintDivider();
                Console.WriteLine($"{Name}'s Abilities | {AP}/{MaxAP} AP remaining");

                // List of all abilities usable by the PCU's class
                List<dynamic> a_list = AbilityManager.GetAbilityList()[PClass];

                // This is used to make sure that the AP costs of each ability line up. Purely asthetic.
                int padding = a_list.Select(x => x.AbilityName.Length).Max();

                int counter = 0;
                foreach (Ability ability in a_list)
                {
                    int true_pad = padding - ability.AbilityName.Length;
                    Console.WriteLine($"      [{counter + 1}] {ability.AbilityName} {new string('-', true_pad)}--> {ability.APCost} AP");
                    counter++;
                }

                while (true)
                {
                    string chosen_ability = CMethods.Input("Input [#] or type 'back'): ");

                    try
                    {
                        CurrentAbility = a_list[int.Parse(chosen_ability) - 1];
                    }

                    catch (Exception ex)
                    {
                        if (ex is FormatException || ex is ArgumentOutOfRangeException)
                        {
                            if (CMethods.IsExitString(chosen_ability))
                            {
                                CMethods.PrintDivider();
                                PrintBattleOptions();

                                return false;
                            }

                            continue;
                        }

                        else
                        {
                            throw ex;
                        }
                    }

                    // Abilities cost AP to cast, just like spells cost MP.
                    if (AP < CurrentAbility.APCost)
                    {
                        CMethods.PrintDivider();
                        Console.WriteLine($"{Name} doesn't have enough AP to cast {CurrentAbility.AbilityName}!");
                        CMethods.PressEnterReturn();

                        break;
                    }

                    AP -= CurrentAbility.APCost;
                    CurrentAbility.BeforeAbility(this);

                    return true;
                }
            }
        }

        /* =========================== *
         *          CONSTRUCTOR        *
         * =========================== */
        public PlayableCharacter(string name, CEnums.CharacterClass p_class, string unit_id, bool active) : base()
        {
            Name = name;
            HP = 20;
            MaxHP = 20;
            MP = 5;
            MaxMP = 5;
            AP = 10;
            MaxAP = 10;
            Attack = 8;
            Defense = 5;
            PAttack = 8;
            PDefense = 5;
            MAttack = 8;
            MDefense = 5;
            Speed = 6;
            Evasion = 3;
            Level = 1;

            CurrentXP = 0;
            RequiredXP = 3;
            PClass = p_class;
            UnitID = unit_id;
            Active = active;
        }
    }

    public abstract class Monster : Unit
    {
        public CEnums.MonsterClass MClass { get; set; }
        public string AttackMessage { get; set; }
        public string AsciiArt { get; set; }
        public Dictionary<string, double> ClassMultipliers { get; set; }
        public Dictionary<string, double> SpeciesMultipliers { get; set; }
        public List<string> DropList { get; set; }

        public string DroppedItem { get; set; }
        public int DroppedGold { get; set; }
        public int DroppedXP { get; set; }

        public Dictionary<string, dynamic> MonsterAbilityFlags = new Dictionary<string, dynamic>()
        {
            {"poison_pow", 0},
            {"poison_dex", 0},
            {"knockout_turns", 0},
            {"judgment_day", 0},
            {"taunted_turn", 0},
            {"taunted_user", null},
            {"drained", false},
            {"disarmed", false}
        };

        public bool IsDefending { get; set; }
        public Unit CurrentTarget { get; set; }

        /* =========================== *
         *        MONSTER METHODS      *
         * =========================== */
        public void GiveStatus(int status_mp_cost)
        {
            Random rng = new Random();
            Array StatusArray = Enum.GetValues(typeof(CEnums.Status));
            CEnums.Status chosen_status = (CEnums.Status)StatusArray.GetValue(rng.Next(StatusArray.Length));

            Console.WriteLine($"The {Name} is attempting to make {CurrentTarget.Name} {CEnums.EnumToString(chosen_status)}!");
            CMethods.SmartSleep(750);

            if (rng.Next(0, 2) == 0)
            {
                if (CurrentTarget.HasStatus(chosen_status))
                {
                    SoundManager.debuff.Play();
                    Console.WriteLine($"...But {CurrentTarget.Name} is already {CEnums.EnumToString(chosen_status)}!");
                }

                else
                {
                    CurrentTarget.Statuses.Add(chosen_status);
                    SoundManager.buff_spell.Play();
                    Console.WriteLine($"{CurrentTarget.Name} is now {CEnums.EnumToString(chosen_status)}!");
                }
            }

            else
            {
                SoundManager.debuff.Play();
                Console.WriteLine($"...But {Name}'s attempt failed!");
            }

            MP -= status_mp_cost;
        }

        public bool GetDrops()
        {
            Random rng = new Random();

            if (rng.Next(0, 4) == 0)
            {
                DroppedItem = CMethods.GetRandomFromIterable(DropList);
                return true;
            }

            return false;
        }

        public void MonsterLevelUp()
        {
            Random rng = new Random();
            int minlvl = TileManager.FindCellWithTileID(CInfo.CurrentTile).MinMonsterLevel;
            int maxlvl = TileManager.FindCellWithTileID(CInfo.CurrentTile).MaxMonsterLevel;

            Level = rng.Next(minlvl, maxlvl);

            for (int i = 0; i < Level; i++)
            {
                HP += 5;
                MP += 3;
                Attack += 3;
                Defense += 3;
                PAttack += 3;
                PDefense += 3;
                MAttack += 3;
                MDefense += 3;
                Speed += 3;
                Evasion += 2;
            }

            MaxHP = HP;
            MaxMP = MP;
        }

        public void MonsterApplyMultipliers()
        {
            HP = (int)(HP * ClassMultipliers["hp"] * SpeciesMultipliers["hp"]);
            MP = (int)(MP * ClassMultipliers["mp"] * SpeciesMultipliers["mp"]);
            Attack = (int)(Attack * ClassMultipliers["attack"] * SpeciesMultipliers["attack"]);
            Defense = (int)(Defense * ClassMultipliers["defense"] * SpeciesMultipliers["defense"]);
            PAttack = (int)(PAttack * ClassMultipliers["p_attack"] * SpeciesMultipliers["p_attack"]);
            PDefense = (int)(PDefense * ClassMultipliers["p_defense"] * SpeciesMultipliers["p_defense"]);
            MAttack = (int)(MAttack * ClassMultipliers["m_attack"] * SpeciesMultipliers["m_attack"]);
            MDefense = (int)(MDefense * ClassMultipliers["m_defense"] * SpeciesMultipliers["m_defense"]);
            Speed = (int)(Speed * ClassMultipliers["speed"] * SpeciesMultipliers["speed"]);
            Evasion = (int)(Evasion * ClassMultipliers["evasion"] * SpeciesMultipliers["evasion"]);

            Attack += (int)(Attack * 0.0005 * CInfo.Difficulty);
            MAttack += (int)(MAttack * 0.0005 * CInfo.Difficulty);
            PAttack += (int)(PAttack * 0.0005 * CInfo.Difficulty);
        }

        public void MonsterExecuteMove()
        {
            // Base Turn
            SoundManager.item_pickup.Stop();
            MonsterGetTarget();

            Console.WriteLine($"-{Name}'s Turn-");

            if (!(MonsterAbilityFlags["knockout_turns"] > 0))
            {
                Console.WriteLine($"The {Name} is making a move!\n");

                MonsterBattleAI();
            }

            else
            {
                Console.WriteLine($"The {Name} is asleep!");
            }

            MonsterDoAbilities();
        }

        public void MonsterGetTarget()
        {
            Random rng = new Random();

            CurrentTarget = CMethods.GetRandomFromIterable(UnitManager.GetAliveActivePCUs());

            if (MonsterAbilityFlags["taunted_turn"] == BattleManager.GetTurnCounter())
            {
                CurrentTarget = MonsterAbilityFlags["taunted_user"];
            }
        }

        public void MonsterDoAbilities()
        {
            Random rng = new Random();

            // Sleep prevents the unit from acting
            if (MonsterAbilityFlags["knockout_turns"] > 0)
            {
                // Number of turns remaining for knockout gas goes down by 1 each turn
                MonsterAbilityFlags["knockout_turns"]--;

                // If decrementing knockout_turns caused it to equal 0, then wake up
                if (MonsterAbilityFlags["knockout_turns"] == 0)
                {
                    CMethods.SmartSleep(500);
                    SoundManager.buff_spell.Play();
                    Statuses.Remove(CEnums.Status.sleep);
                    Console.WriteLine($"The {Name} woke up!");
                }

                else
                {
                    int chance = 10;

                    if (rng.Next(0, 100) < chance)
                    {
                        CMethods.SmartSleep(500);
                        SoundManager.buff_spell.Play();
                        Statuses.Remove(CEnums.Status.sleep);
                        Console.WriteLine($"The {Name} woke up early!");
                    }
                }
            }

            // Poison deals damage per turn
            if (HasStatus(CEnums.Status.poison))
            {
                int poison_damage = MonsterAbilityFlags["poison_pow"] * MaxHP + MonsterAbilityFlags["poison_dex"];
                HP -= poison_damage;
                SoundManager.poison_damage.Play();
                Console.WriteLine($"The {Name} took {poison_damage} from poison!");
            }

            // Judgment day instantly kills the unit if the wait timer expires
            if (MonsterAbilityFlags["judgment_day"] == BattleManager.GetTurnCounter())
            {
                CMethods.SmartSleep(500);
                Console.WriteLine($"{Name}'s judgment day has arrived. The darkness devours it...");
                HP = 0;
            }


        }

        public abstract void UponDefeating();

        public abstract void MonsterBattleAI();

        /* =========================== *
         *          CONSTRUCTOR        *
         * =========================== */
        protected Monster() : base()
        {
            HP = 10;
            MaxHP = 10;
            MP = 5;
            MaxMP = 5;
            AP = 10;
            MaxAP = 10;
            Attack = 8;
            Defense = 5;
            PAttack = 8;
            PDefense = 5;
            MAttack = 8;
            MDefense = 5;
            Speed = 6;
            Evasion = 3;
            Level = 1;

            UnitID = Guid.NewGuid().ToString();
            IsDefending = false;
        }
    }

    // =========================== #
    //       MELEE MONSTERS        #
    // =========================== #
    #region
    internal abstract class MeleeMonster : Monster
    {
        public override void MonsterBattleAI()
        {
            Random rng = new Random();

            // Melee monsters have a 1 in 6 (16.667%) chance to defend
            if (rng.Next(0, 5) == 0 && !IsDefending && !(MonsterAbilityFlags["taunted_turn"] == BattleManager.GetTurnCounter()))
            {
                IsDefending = true;
                Console.WriteLine($"The {Name} is preparing itself for enemy attacks...");
                CMethods.SmartSleep(750);

                Defense *= 2;
                MDefense *= 2;
                PDefense *= 2;

                Console.WriteLine($"The {Name}'s defense stats increased by 2x for one turn!");
                SoundManager.buff_spell.Play();
                return;
            }

            else if (IsDefending)
            {
                Console.WriteLine($"The {Name} stops defending, returning its defense stats to normal.");
                IsDefending = false;
                Defense /= 2;
                MDefense /= 2;
                PDefense /= 2;
            }

            SoundManager.sword_slash.Play();
            Console.WriteLine($"The {Name} {AttackMessage} {CurrentTarget.Name}...");
            CMethods.SmartSleep(750);

            int attack_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.physical);

            if (CurrentTarget.TempStats["evasion"] < rng.Next(0, 512))
            {
                SoundManager.enemy_hit.Play();
                Console.WriteLine($"The {Name}'s attack deals {attack_damage} damage to {CurrentTarget.Name}!");
                CurrentTarget.HP -= attack_damage;
            }

            else
            {
                SoundManager.attack_miss.Play();
                Console.WriteLine($"The {Name}'s attack narrowly misses {CurrentTarget.Name}!");
            }
        }

        protected MeleeMonster() : base()
        {
            MClass = CEnums.MonsterClass.melee;

            ClassMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1.2 },            // HP
                { "mp", 1 },          // MP
                { "attack", 1.5 },      // Physical Attack
                { "defense", 1.5 },    // Physical Defense
                { "p_attack", 0.5 },    // Pierce Attack
                { "p_defense", 1.5 },  // Pierce Defense
                { "m_attack", 0.5 },    // Magical Attack
                { "m_defense", 0.5 },   // Magical Defense
                { "speed", -0.65 },         // Speed
                { "evasion", 1 }        // Evasion
            };
        }
    }

    internal class GiantCrab : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public GiantCrab() : base()
        {
            Name = "Giant Crab";
            OffensiveElement = CEnums.Element.water;
            DefensiveElement = CEnums.Element.water;
            AttackMessage = "snaps its massive claws at";
            DropList = new List<string>() { "crab_claw", "shell_fragment" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class BogSlime : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public BogSlime() : base()
        {
            Name = "Bog Slime";
            OffensiveElement = CEnums.Element.grass;
            DefensiveElement = CEnums.Element.grass;
            AttackMessage = "jiggles menacingly at";
            DropList = new List<string>() { "slime_vial", "water_vial" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Mummy : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public Mummy() : base()
        {
            Name = "Mummy";
            OffensiveElement = CEnums.Element.fire;
            DefensiveElement = CEnums.Element.dark;
            AttackMessage = "meanders over and grabs";
            DropList = new List<string>() { "burnt_ash", "ripped_cloth" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class SandGolem : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public SandGolem() : base()
        {
            Name = "Sand Golem";
            OffensiveElement = CEnums.Element.earth;
            DefensiveElement = CEnums.Element.earth;
            AttackMessage = "begins to pile sand on";
            DropList = new List<string>() { "golem_rock", "broken_crystal" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class MossOgre : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public MossOgre() : base()
        {
            Name = "Moss Ogre";
            OffensiveElement = CEnums.Element.grass;
            DefensiveElement = CEnums.Element.grass;
            AttackMessage = "swings a tree trunk like a club at";
            DropList = new List<string>() { "bone_bag", "monster_skull" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Troll : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public Troll() : base()
        {
            Name = "Troll";
            OffensiveElement = CEnums.Element.neutral;
            DefensiveElement = CEnums.Element.neutral;
            AttackMessage = "swings its mighty battleaxe at";
            DropList = new List<string>() { "monster_skull", "eye_balls" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Griffin : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public Griffin() : base()
        {
            Name = "Griffin";
            OffensiveElement = CEnums.Element.wind;
            DefensiveElement = CEnums.Element.wind;
            AttackMessage = "swipes with its ferocious claws at";
            DropList = new List<string>() { "animal_fur", "wing_piece" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class GirthWorm : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public GirthWorm() : base()
        {
            Name = "Girth Worm";
            OffensiveElement = CEnums.Element.earth;
            DefensiveElement = CEnums.Element.earth;
            AttackMessage = "burrows into the ground and starts charging towards";
            DropList = new List<string>() { "monster_fang", "slime_vial" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Zombie : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public Zombie() : base()
        {
            Name = "Giant Crab";
            OffensiveElement = CEnums.Element.dark;
            DefensiveElement = CEnums.Element.dark;
            AttackMessage = "charges and tries to bite";
            DropList = new List<string>() { "monster_skull", "blood_vial" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class SnowWolf : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public SnowWolf() : base()
        {
            Name = "Snow Wol$";
            OffensiveElement = CEnums.Element.ice;
            DefensiveElement = CEnums.Element.ice;
            AttackMessage = "claws and bites at";
            DropList = new List<string>() { "animal_fur", "monster_fang" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class LesserYeti : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public LesserYeti() : base()
        {
            Name = "Lesser Yeti";
            OffensiveElement = CEnums.Element.ice;
            DefensiveElement = CEnums.Element.ice;
            AttackMessage = "begins to maul";
            DropList = new List<string>() { "animal_fur", "monster_fang" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class SludgeRat : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public SludgeRat() : base()
        {
            Name = "Sludge Rat";
            OffensiveElement = CEnums.Element.neutral;
            DefensiveElement = CEnums.Element.neutral;
            AttackMessage = "ferociously chomps at";
            DropList = new List<string>() { "monster_skull", "rodent_tail" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class SeaSerpent : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public SeaSerpent() : base()
        {
            Name = "Sea Serpent";
            OffensiveElement = CEnums.Element.water;
            DefensiveElement = CEnums.Element.water;
            AttackMessage = "charges head-first into";
            DropList = new List<string>() { "serpent_scale", "serpent_tongue" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Beetle : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public Beetle() : base()
        {
            Name = "Beetle";
            OffensiveElement = CEnums.Element.earth;
            DefensiveElement = CEnums.Element.grass;
            AttackMessage = "charges horn-first into";
            DropList = new List<string>() { "beetle_shell", "antennae" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Harpy : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public Harpy() : base()
        {
            Name = "Harpy";
            OffensiveElement = CEnums.Element.wind;
            DefensiveElement = CEnums.Element.wind;
            AttackMessage = "dives claws-first towards";
            DropList = new List<string>() { "wing_piece", "feathers" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class FallenKnight : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public FallenKnight() : base()
        {
            Name = "Fallen Knight";
            OffensiveElement = CEnums.Element.light;
            DefensiveElement = CEnums.Element.dark;
            AttackMessage = "thrusts its heavenly spear towards";
            DropList = new List<string>() { "chain_link", "blood_vial" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class DevoutProtector : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public DevoutProtector() : base()
        {
            Name = "Devout Protector";
            OffensiveElement = CEnums.Element.light;
            DefensiveElement = CEnums.Element.light;
            AttackMessage = "swings its holy hammer towards";
            DropList = new List<string>() { "angelic_essence", "mysterious_runes" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Calculator : MeleeMonster
    {
        public override void UponDefeating()
        {

        }

        public Calculator() : base()
        {
            Name = "Calculator";
            OffensiveElement = CEnums.Element.neutral;
            DefensiveElement = CEnums.Element.water;
            AttackMessage = "casts its mathemagical spell on";
            DropList = new List<string>() { "calculus_homework", "graph_paper", "protractor", "ruler", "textbook" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }
    #endregion

    // =========================== #
    //       RANGED MONSTERS       #
    // =========================== #
    #region
    internal abstract class RangedMonster : Monster
    {
        public override void MonsterBattleAI()
        {
            Random rng = new Random();
            Console.WriteLine($"The {Name} {AttackMessage} {CurrentTarget.Name}...");
            SoundManager.aim_weapon.Play();

            CMethods.SmartSleep(750);

            int attack_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.piercing);

            if (CurrentTarget.TempStats["evasion"] < rng.Next(0, 512))
            {
                SoundManager.enemy_hit.Play();
                Console.WriteLine($"The {Name}'s attack deals {attack_damage} damage to {CurrentTarget.Name}!");
                CurrentTarget.HP -= attack_damage;
            }

            else
            {
                SoundManager.attack_miss.Play();
                Console.WriteLine($"The {Name}'s attack narrowly misses {CurrentTarget.Name}!");
            }
        }

        protected RangedMonster() : base()
        {
            MClass = CEnums.MonsterClass.ranged;

            ClassMultipliers = new Dictionary<string, double>()
            {
                { "hp", 0.9 },            // HP
                { "mp", 1 },          // MP
                { "attack", 0.8 },      // Physical Attack
                { "defense", 0.8 },    // Physical Defense
                { "p_attack", 1.5 },    // Pierce Attack
                { "p_defense", 1.2 },  // Pierce Defense
                { "m_attack", 0.8 },    // Magical Attack
                { "m_defense", 1 },   // Magical Defense
                { "speed", 1.5 },         // Speed
                { "evasion", 1.5 }        // Evasion
            };
        }
    }

    internal class FireAnt : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public FireAnt() : base()
        {
            Name = "Fire Ant";
            OffensiveElement = CEnums.Element.fire;
            DefensiveElement = CEnums.Element.fire;
            AttackMessage = "spits a firey glob of acid at";
            DropList = new List<string>() { "antennae", "burnt_ash" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class NagaBowwoman : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public NagaBowwoman() : base()
        {
            Name = "Naga Bow-woman";
            OffensiveElement = CEnums.Element.neutral;
            DefensiveElement = CEnums.Element.water;
            AttackMessage = "fires a volley of arrows at";
            DropList = new List<string>() { "serpent_scale", "serpent_tongue" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class IceSoldier : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public IceSoldier() : base()
        {
            Name = "Ice Soldier";
            OffensiveElement = CEnums.Element.ice;
            DefensiveElement = CEnums.Element.ice;
            AttackMessage = "fires a single hyper-cooled arrow at";
            DropList = new List<string>() { "chain_link", "blood_vial" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class FrostBat : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public FrostBat() : base()
        {
            Name = "Frost Bat";
            OffensiveElement = CEnums.Element.ice;
            DefensiveElement = CEnums.Element.ice;
            AttackMessage = "spits a frozen glob of acid at";
            DropList = new List<string>() { "monster_fang", "wing_piece" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class SparkBat : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public SparkBat() : base()
        {
            Name = "Spark Bat";
            OffensiveElement = CEnums.Element.electric;
            DefensiveElement = CEnums.Element.electric;
            AttackMessage = "spits an electrified glob of acid at";
            DropList = new List<string>() { "monster_fang", "wing_piece" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class SkeletonBoneslinger : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public SkeletonBoneslinger() : base()
        {
            Name = "Skeleton Boneslinger";
            OffensiveElement = CEnums.Element.dark;
            DefensiveElement = CEnums.Element.dark;
            AttackMessage = "grabs a nearby bone and slings it at";
            DropList = new List<string>() { "bone_bag", "demonic_essence" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class UndeadCrossbowman : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public UndeadCrossbowman() : base()
        {
            Name = "Undead Crossbowman";
            OffensiveElement = CEnums.Element.dark;
            DefensiveElement = CEnums.Element.dark;
            AttackMessage = "fires a bone-tipped crossbow bolt at";
            DropList = new List<string>() { "chain_link", "bone_bag" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class RockGiant : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public RockGiant() : base()
        {
            Name = "Rock Giant";
            OffensiveElement = CEnums.Element.earth;
            DefensiveElement = CEnums.Element.earth;
            AttackMessage = "hurls a giant boulder at";
            DropList = new List<string>() { "golem_rock", "broken_crystal" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class GoblinArcher : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public GoblinArcher() : base()
        {
            Name = "Goblin Archer";
            OffensiveElement = CEnums.Element.neutral;
            DefensiveElement = CEnums.Element.neutral;
            AttackMessage = "fires an arrow at";
            DropList = new List<string>() { "ripped_cloth", "eye_balls" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class GiantLandSquid : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public GiantLandSquid() : base()
        {
            Name = "Giant Land-Squid";
            OffensiveElement = CEnums.Element.water;
            DefensiveElement = CEnums.Element.water;
            AttackMessage = "shoots a black, inky substance at";
            DropList = new List<string>() { "ink_sack", "slime_vial" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class VineLizard : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public VineLizard() : base()
        {
            Name = "Vine Lizard";
            OffensiveElement = CEnums.Element.grass;
            DefensiveElement = CEnums.Element.grass;
            AttackMessage = "spits an acidic string of vines at";
            DropList = new List<string>() { "serpent_scale", "living_bark" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class TenguRanger : RangedMonster
    {
        public override void UponDefeating()
        {

        }

        public TenguRanger() : base()
        {
            Name = "Tengu Ranger";
            OffensiveElement = CEnums.Element.earth;
            DefensiveElement = CEnums.Element.earth;
            AttackMessage = "catapults a stone javelin towards";
            DropList = new List<string>() { "wing_piece", "feathers" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }
    #endregion

    // =========================== //
    //       MAGIC MONSTERS        //
    // =========================== //
    #region
    internal abstract class MagicMonster : Monster
    {
        public override void MonsterBattleAI()
        {
            Random rng = new Random();
            int status_mp_cost = MaxMP / 10;
            int heal_mp_cost = MaxMP / 5;
            int attack_mp_cost = MaxHP / 7;

            // If the monster is neither taunted nor silenced, it will use a spell
            if (!(MonsterAbilityFlags["taunted_turn"] == BattleManager.GetTurnCounter()) || HasStatus(CEnums.Status.silence))
            {
                if (rng.Next(0, 7) == 0 && MP >= status_mp_cost)
                {
                    GiveStatus(status_mp_cost);

                    return;
                }

                // Magic heal
                else if (HP <= MaxHP / 5 && MP >= heal_mp_cost)
                {
                    Console.WriteLine($"The {Name} is casting a healing spell on itself...");
                    CMethods.SmartSleep(750);

                    int total_heal = Math.Max(HP / 5, 5);
                    HP += total_heal;
                    MP -= heal_mp_cost;

                    Console.WriteLine($"The {Name} heals itself for {total_heal} HP!");
                    SoundManager.magic_healing.Play();

                    return;
                }

                // Magical Attack
                else if (MP >= attack_mp_cost)
                {
                    SoundManager.magic_attack.Play();

                    Console.WriteLine($"The {Name} {AttackMessage} {CurrentTarget.Name}...");
                    CMethods.SmartSleep(750);

                    // Spell Power is equal to Level/105 + 0.05, with a maximum value of 1
                    // This formula means that spell power increases linearly from 0.06 at level 1, to 1 at level 100
                    // All monsters from level 100 onwards have exactly 1 spell power
                    double m_spell_power = Math.Min((double)Level / 105 + 0.05, 1);
                    int spell_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.magical, spell_power: m_spell_power);

                    if (CurrentTarget.TempStats["evasion"] < rng.Next(0, 512))
                    {
                        SoundManager.enemy_hit.Play();
                        Console.WriteLine($"The {Name}'s spell deals {spell_damage} damage to {CurrentTarget.Name}!");

                        CurrentTarget.HP -= spell_damage;
                    }

                    else
                    {
                        SoundManager.attack_miss.Play();
                        Console.WriteLine($"The {Name}'s spell narrowly misses {CurrentTarget.Name}!");
                    };

                    MP -= attack_mp_cost;

                    return;
                }
            }

            // Non-magical Attack (Pierce Damage). Only happens if taunted, silenced, or if out of mana.           
            Console.WriteLine($"The {Name} attacks {CurrentTarget.Name}...");
            SoundManager.aim_weapon.Play();

            CMethods.SmartSleep(750);
            int attack_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.piercing);

            if (CurrentTarget.TempStats["evasion"] < rng.Next(0, 512))
            {
                SoundManager.enemy_hit.Play();
                Console.WriteLine($"The {Name}'s attack deals {attack_damage} damage to {CurrentTarget.Name}!");
                CurrentTarget.HP -= attack_damage;
            }

            else
            {
                SoundManager.attack_miss.Play();
                Console.WriteLine($"The {Name}'s attack narrowly misses {CurrentTarget.Name}!");
            }
        }

        protected MagicMonster() : base()
        {
            MClass = CEnums.MonsterClass.magic;

            ClassMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },            // HP
                { "mp", 1.5 },          // MP
                { "attack", 0.5 },      // Physical Attack
                { "defense", 0.65 },    // Physical Defense
                { "p_attack", 0.5 },    // Pierce Attack
                { "p_defense", 0.65 },  // Pierce Defense
                { "m_attack", 1.5 },    // Magical Attack
                { "m_defense", 1.5 },   // Magical Defense
                { "speed", 1 },         // Speed
                { "evasion", 1 }        // Evasion
            };
        }
    }

    internal class Oread : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public Oread() : base()
        {
            Name = "Oread";
            OffensiveElement = CEnums.Element.earth;
            DefensiveElement = CEnums.Element.earth;
            AttackMessage = "casts a basic earth spell on";
            DropList = new List<string>() { "fairy_dust", "eye_balls" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Willothewisp : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public Willothewisp() : base()
        {
            Name = "Will-o'-the-wisp";
            OffensiveElement = CEnums.Element.fire;
            DefensiveElement = CEnums.Element.fire;
            AttackMessage = "casts a basic fire spell on";
            DropList = new List<string>() { "fairy_dust", "burnt_ash" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Naiad : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public Naiad() : base()
        {
            Name = "Naiad";
            OffensiveElement = CEnums.Element.water;
            DefensiveElement = CEnums.Element.water;
            AttackMessage = "casts a basic water spell on";
            DropList = new List<string>() { "fairy_dust", "water_vial" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Necromancer : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public Necromancer() : base()
        {
            Name = "Necromancer";
            OffensiveElement = CEnums.Element.dark;
            DefensiveElement = CEnums.Element.dark;
            AttackMessage = "casts a basic dark spell on";
            DropList = new List<string>() { "ripped_cloth", "demonic_essence" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class CorruptThaumaturge : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public CorruptThaumaturge() : base()
        {
            Name = "Corrupt Thaumaturge";
            OffensiveElement = CEnums.Element.ice;
            DefensiveElement = CEnums.Element.ice;
            AttackMessage = "casts a basic ice spell on";
            DropList = new List<string>() { "ripped_cloth", "mysterious_runes" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Imp : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public Imp() : base()
        {
            Name = "Imp";
            OffensiveElement = CEnums.Element.fire;
            DefensiveElement = CEnums.Element.neutral;
            AttackMessage = "casts a basic fire spell on";
            DropList = new List<string>() { "wing_piece", "fairy_dust" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Spriggan : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public Spriggan() : base()
        {
            Name = "Spriggan";
            OffensiveElement = CEnums.Element.grass;
            DefensiveElement = CEnums.Element.grass;
            AttackMessage = "casts a basic grass spell on";
            DropList = new List<string>() { "fairy_dust", "fairy_dust" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class Alicorn : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public Alicorn() : base()
        {
            Name = "Alicorn";
            OffensiveElement = CEnums.Element.light;
            DefensiveElement = CEnums.Element.light;
            AttackMessage = "casts a basic light spell on";
            DropList = new List<string>() { "unicorn_horn", "angelic_essence" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class WindWraith : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public WindWraith() : base()
        {
            Name = "Wind Wraith";
            OffensiveElement = CEnums.Element.wind;
            DefensiveElement = CEnums.Element.wind;
            AttackMessage = "casts a basic wind spell on";
            DropList = new List<string>() { "ectoplasm", "demonic_essence" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }

    internal class LightningGhost : MagicMonster
    {
        public override void UponDefeating()
        {

        }

        public LightningGhost() : base()
        {
            Name = "Lightning Ghost";
            OffensiveElement = CEnums.Element.electric;
            DefensiveElement = CEnums.Element.electric;
            AttackMessage = "casts a basic electric spell on";
            DropList = new List<string>() { "ectoplasm", "demonic_essence" };

            SpeciesMultipliers = new Dictionary<string, double>()
            {
                { "hp", 1 },         // HP
                { "mp", 1 },         // MP
                { "attack", 1 },     // Physical Attack
                { "defense", 1 },    // Physical Defense
                { "p_attack", 1 },   // Pierce Attack
                { "p_defense", 1 },  // Pierce Defense
                { "m_attack", 1 },   // Magical Attack
                { "m_defense", 1 },  // Magical Defense
                { "speed", 1 },      // Speed
                { "evasion", 1 }     // Evasion
            };
        }
    }
    #endregion
}
