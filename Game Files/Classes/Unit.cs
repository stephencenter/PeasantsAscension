using System;
using System.Collections.Generic;
using System.Linq;
using Scripts.Items;

namespace Scripts
{
    public class Unit
    {
        // Method 
        readonly Common c_methods = new Common();
        readonly AbilityManager ability_manager = new AbilityManager();
        readonly PCUStorage pcu_storage = new PCUStorage();
        protected SpellManager spell_manager = new SpellManager();

        // General Unit Properties
        public enum Element { fire, water, electric, earth, wind, grass, ice, light, dark, none }
        public Dictionary<Element, List<Element>> ElementChart = new Dictionary<Element, List<Element>>
        {
            {Element.fire, new List<Element> {Element.water, Element.ice } },
            {Element.water, new List<Element> {Element.electric, Element.fire } },
            {Element.electric, new List<Element> {Element.earth, Element.water } },
            {Element.earth, new List<Element> {Element.wind, Element.electric } },
            {Element.wind, new List<Element> {Element.grass, Element.earth } },
            {Element.grass, new List<Element> {Element.ice, Element.wind } },
            {Element.ice, new List<Element> {Element.fire, Element.grass } },
            {Element.light, new List<Element> {Element.light, Element.dark } },
            {Element.dark, new List<Element> {Element.dark, Element.light } }
        };
        public Element off_element = Element.none;
        public Element def_element = Element.none;

        public enum Status { silence, poison, weakness, blindness, paralyzation, alive, dead }
        public List<Status> Statuses = new List<Status> { Status.alive };

        public enum UnitType { player, monster, boss }
        public UnitType Type { get; set; }

        public string Name { get; set; }
        public int HP { get; set; }
        public int MaxHP { get; set; }
        public int MP { get; set; }
        public int MaxMP { get; set; }
        public int Attack { get; set; }
        public int Defense { get; set; }
        public int PAttack { get; set; }
        public int PDefense { get; set; }
        public int MAttack { get; set; }
        public int MDefense { get; set; }
        public int Speed { get; set; }
        public int Evasion { get; set; }
        public int Level { get; set; }

        // Player Attributes
        public enum CharacterClass { warrior, ranger, mage, assassin, paladin, monk, bard }
        public CharacterClass PClass { get; set; }

        public bool Active { get; set; }
        public int CurrentXP { get; set; }
        public int RequiredXP { get; set; }
        public int AP { get; set; }
        public int MaxAP { get; set; }
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


        // Monster Attributes
        public enum MonsterClass { melee, ranged, magic }
        public MonsterClass MClass { get; set; }

        public Status StatusOnAttack { get; set; }
        public bool IsDefending { get; set; }
        public int DroppedGold { get; set; }
        public int DroppedXP { get; set; }
        public List<Item> DroppedItems { get; set; }
        public string AttackMessage { get; set; }
        public string AsciiArt { get; set; }


        public Dictionary<string, dynamic> MonsterAbilityFlags = new Dictionary<string, dynamic>()
        {
            {"poison_pow", 0},
            {"poison_dex", 0},
            {"knockout_turns", 0},
            {"judgement_day", 0},
            {"taunted_turn", 0},
            {"taunted_user", null},
            {"drained", false},
            {"disarmed", false}
        };

       
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

        public bool IsAlive()
        {
            return !Statuses.Contains(Unit.Status.dead);
        }

        public bool IsPCU()
        {
            return Type == UnitType.player;
        }

        public bool IsMonster()
        {
            return Type == UnitType.monster;
        }

        public void FixAllStats()
        {
            // Makes sure that that no-one ever has stats that would cause the game to malfunction.
            // e.g. no negative HP/MP/AP, no HP/MP/AP above max, etc.
            // This function also acts as a hard-cap for evasion, which is limited to a max of 256
            // (50% dodge chance). This is to prevent people from min-maxing their evasion to cheese
            // their way through the game, and also prevents monsters from being invincible.

            HP = c_methods.Clamp(HP, MaxHP, 0);
            MP = c_methods.Clamp(MP, MaxMP, 0);
            AP = c_methods.Clamp(AP, MaxAP, 0);

            Evasion = Math.Min(256, Evasion);
            Statuses = Statuses.Distinct().ToList();

            TempStats["evasion"] = Math.Min(PlayerAbilityFlags["rolling"] ? 512 : 256, TempStats["evasion"]);

            if (HP > 0 && !IsAlive())
            {
                Statuses = new List<Unit.Status>() { Unit.Status.alive };
            }

            if (!IsAlive())
            {
                Statuses = new List<Unit.Status>() { Unit.Status.dead };
            }
        }

        public string GetStatusName(Status status)
        {
            Dictionary<Status, string> StatusNameMap = new Dictionary<Status, string>()
            {
                {Status.silence, "Silence"},
                {Status.poison, "Poison"},
                {Status.weakness, "Weakness"},
                {Status.blindness, "Blindness"},
                {Status.paralyzation, "Paralyzation" },
                {Status.alive, "Alive"},
                {Status.dead, "Dead"},
            };

            return StatusNameMap[status];
        }

        public void PlayerChoice(List<Unit> monster_list)
        {
            PrintBattleOptions();

            while (true)
            {
                string c_move = c_methods.Input("Input [#]: ");

                try
                {
                    CurrentMove = String.Join("", c_move.Where(x => char.IsDigit(x)))[0];
                }

                catch (IndexOutOfRangeException)
                {
                    continue;
                }

                // Attack
                if (CurrentMove == '1')
                {
                    if (!ChooseTarget(monster_list, $"Who should {Name} attack?", false, true, false, false))
                    {
                        PrintBattleOptions();
                        continue;
                    }

                    return;
                }

                // Magic
                else if (CurrentMove == '2')
                {
                    c_methods.PrintDivider();

                    // Silence is a status ailment that prevents using spells
                    if (Statuses.Contains(Status.silence))
                    {
                        // sounds.debuff.play()
                        Console.WriteLine($"{Name} can't use spells when silenced!");
                        c_methods.PressEnterReturn();
                        PrintBattleOptions();

                        continue;
                    }

                    if (!spell_manager.PickSpellCategory())
                    {
                        PrintBattleOptions();
                        continue;
                    }

                    return;
                }

                // Ability
                else if (CurrentMove == '3')
                {
                    while (true)
                    {
                        c_methods.PrintDivider();
                        Console.WriteLine($"{Name}'s Abilities | {AP}/{MaxAP} AP remaining");

                        // List of all abilities usable by the PCU's class
                        List<dynamic> a_list = ability_manager.GetAbilityList()[PClass];

                        // This is used to make sure that the AP costs of each ability line up. Purely asthetic.
                        int padding = a_list.Select(x => x.Name.Length).Max();

                        int counter = 0;
                        foreach (Ability ability in a_list)
                        {
                            int true_pad = padding - ability.AbilityName.Length;
                            Console.WriteLine($"      [{counter + 1}] {ability.AbilityName} {new String('-', true_pad)}--> {ability.APCost} AP");
                        }

                        while (true)
                        {
                            string chosen_ability = c_methods.Input("Input [#] or type 'back'): ");

                            try
                            {
                                CurrentAbility = a_list[int.Parse(chosen_ability) - 1];
                            }

                            catch (Exception ex)
                            {
                                if (ex is ArgumentException || ex is IndexOutOfRangeException)
                                {
                                    if (c_methods.IsExitString(chosen_ability)) {
                                        c_methods.PrintDivider();
                                        PrintBattleOptions();

                                        return;
                                    }

                                    continue;
                                }
                            }

                            // Abilities cost AP to cast, just like spells cost MP.
                            if (AP < CurrentAbility.APCost)
                            {
                                c_methods.PrintDivider();
                                Console.WriteLine($"{Name} doesn't have enough AP to cast {CurrentAbility.AbilityName}!");
                                c_methods.PressEnterReturn();

                                break;
                            }

                            AP -= CurrentAbility.APCost;
                            CurrentAbility.BeforeAbility();

                            return;
                        }
                    }
                }

                // Use Items
                else if (CurrentMove == '4')
                {
                    /*
                    print('-'*save_load.divider_size)

                    # You can only use consumable items during battle
                    if not items.inventory['consumables']:
                        print('Your party has no consumables!')
                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)
                        print(battle_options.format(self.name))

                        continue

                    # Mute is a status ailment that prevents using items
                    if 'muted' in self.status_ail:
                        sounds.debuff.play()
                        print(f"{self.name} can't use items when muted!")
                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)
                        print(battle_options.format(self.name))

                        continue

                    if not battle.battle_inventory(self):
                        print(battle_options.format(self.name))

                        continue

                    main.s_input('\nPress enter/return ')
                    return */
                }

                // Run
                else if (CurrentMove == '5')
                {
                    return;
                }
            }
        }

        public void PrintBattleOptions()
        {
            Console.WriteLine("Pick {0}'s Move:\n      [1]Standard Attack\n      [2] Use Magic\n      [3] Use Abilities\n      [4] Use Items\n      [5] Run");
        }

        public string PCUExecuteMove()
        {
            return "run";
        }

        public string MonsterExecuteMove()
        {
            return "run";
        }

        public bool ChooseTarget(List<Unit> monster_list, string action_desc, bool target_allies, bool target_enemies, bool allow_dead, bool allow_inactive)
        {
            // A list of PCUs that are valid for targetting (could be unused if target_allies is false)
            List<Unit> pcu_list;

            if (allow_inactive)
            {
                if (allow_dead)
                {
                    // YES to dead PCUs, YES to inactive PCUs
                    pcu_list = pcu_storage.GetAllPCUs();
                }

                else
                {
                    // NO to dead PCUs, YES to inactive PCUs
                    pcu_list = pcu_storage.GetAlivePCUs();
                }
            }

            else
            {
                if (allow_dead)
                {
                    // YES to dead PCUs, NO to inactive PCUs
                    pcu_list = pcu_storage.GetActivePCUs();
                }

                else
                {
                    // NO to dead PCUs, NO to inactive PCUs
                    pcu_list = pcu_storage.GetAliveActivePCUs();
                }
            }

            // The full list of valid targets, including both monsters and allies if applicable
            List<Unit> valid_targets;

            // Do this if both allies and enemies are valid targets (e.g. some abilities and spells)
            if (target_allies && target_enemies)
            {
                valid_targets = pcu_list.Concat(monster_list.Where(x => x.IsAlive())).ToList();
            }

            // Do this if the player is allowed to target allies but not enemies (e.g. items, some spells/abilities)
            else if (target_allies && !target_enemies)
            {
                if (pcu_list.Count == 1)
                {
                    CurrentTarget = pcu_list[0];
                    return true;
                }

                valid_targets = pcu_list;
            }

            // Do this if the player is allowed to target enemies but not allies (e.g. attacks, some spells/abilities)
            else if (!target_allies && target_enemies)
            {
                if (monster_list.Where(x => x.IsAlive()).Count() == 1)
                {
                    CurrentTarget = monster_list.Where(x => x.IsAlive()).ToList()[0];
                    return true;
                }

                valid_targets = monster_list.Where(x => x.IsAlive()).ToList();
            }

            else
            {
                throw new Exception("Exception in 'choose_target': at least one of 'target_allies' or 'target_enemies' must be true");
            }

            c_methods.PrintDivider();
            Console.WriteLine(action_desc);

            int counter = 0;
            foreach (Unit unit in valid_targets)
            {
                /* Looks like this: 
                 *       [1] Target A
                 *       [2] Target B
                 *       [3] Target C
                 * Input [#] (or type "back"): 
                 */
                Console.WriteLine($"      [{counter + 1} {unit.Name}");
            }

            while (true)
            {
                string chosen = c_methods.Input("Input [#]: ");

                try
                {
                    CurrentTarget = valid_targets[int.Parse(chosen) - 1];
                }

                catch (Exception ex) {
                    if (ex is ArgumentException || ex is IndexOutOfRangeException)
                    {
                        if (c_methods.IsExitString(chosen))
                        {
                            return false;
                        }

                        continue;
                    }
                }

                return true;
            }
        }

        public Unit(string name, UnitType unittype)
        {
            Type = unittype;
            Name = name;
            HP = 20;
            MaxHP = 20;
            MP = 5;
            MaxMP = 5;
            Attack = 8;
            Defense = 5;
            PAttack = 8;
            PDefense = 5;
            MAttack = 8;
            MDefense = 5;
            Speed = 6;
            Evasion = 3;
            Level = 1;

            if (unittype == UnitType.player)
            {
                Active = true;
                CurrentXP = 0;
                RequiredXP = 3;
                AP = 10;
                MaxAP = 10;
            }

            else if (unittype == UnitType.monster || unittype == UnitType.boss)
            {
                DroppedItems = new List<Item>();
                MClass = MonsterClass.melee;
                StatusOnAttack = Status.paralyzation;
                IsDefending = false;
                DroppedGold = 5;
                DroppedXP = 5;
                AttackMessage = "attacks";
                AsciiArt = "";

                if (unittype == UnitType.boss)
                {
                    
                }
            }
        }
    }

    public class PCUStorage
    {
        readonly Unit player = new Unit("", Unit.UnitType.player);
        readonly Unit solou = new Unit("Solou", Unit.UnitType.player);
        readonly Unit chili = new Unit("Chili", Unit.UnitType.player);
        readonly Unit chyme = new Unit("Chyme", Unit.UnitType.player);
        readonly Unit storm = new Unit("Storm", Unit.UnitType.player);
        readonly Unit parsto = new Unit("Parsto", Unit.UnitType.player);
        readonly Unit adorine = new Unit("Adorine", Unit.UnitType.player);
        readonly Common c_methods = new Common();

        // Returns ALL PCUs, alive, dead, active, and inactive
        public List<Unit> GetAllPCUs()
        {
            return new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };
        }

        // Returns all PCUs that are alive, regardless of whether they're active or not
        public List<Unit> GetAlivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };

            pcu_list = pcu_list.Where(x => x.IsAlive()).ToList();

            return pcu_list;
        }

        // Returns all PCUs that are active, regardless of whether they're alive or not
        public List<Unit> GetActivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };

            pcu_list = pcu_list.Where(x => x.Active).ToList();

            return pcu_list;
        }

        // Returns all PCUs that are both alive and active
        public List<Unit> GetAliveActivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };

            pcu_list = pcu_list.Where(x => x.Active && x.IsAlive()).ToList();

            return pcu_list;
        }
    }

    public class MonsterGenerator
    {
        readonly Common c_methods = new Common();

        public Unit GenerateMonster()
        {
            return new Unit("Whispering Goblin", Unit.UnitType.monster);
        }
    }

    public class PartyInfo
    {
        public GameState Gamestate { get; set; }
        public Mode MusicboxMode { get; set; }
        public List<Town> VisitedTowns { get; set; }
        public Tile CurrentTile { get; set; }
        public Tile RespawnTile { get; set; }
        public Town CurrentTown { get; set; }
        public int GP { get; set; }
        public int StepsWithoutBattle { get; set; }
        public int Difficulty { get; set; }
        public int AtlasStrength { get; set; }
        public string Music { get; set; }
        public string CurrentProvince { get; set; }
        public string MusicboxFolder { get; set; }
        public bool MusicboxIsPlaying { get; set; }
        public bool DoSpawns { get; set; }

        public List<string> FriendNames = new List<string>();

        public enum GameState { overworld = 1, battle, town }
        public enum Mode { AtoZ = 1, ZtoA, shuffle }

        public PartyInfo()
        {
            Gamestate = GameState.overworld;
            MusicboxMode = Mode.AtoZ;
            VisitedTowns = new List<Town>();
            CurrentTile = new Tile();
            RespawnTile = new Tile();
            CurrentTown = new Town();
            GP = 20;
            StepsWithoutBattle = 0;
            Difficulty = 0;
            AtlasStrength = 1;
            Music = "../Music/Through the Forest.ogg";
            CurrentProvince = "Overshire";
            MusicboxFolder = "";
            MusicboxIsPlaying = false;
            DoSpawns = true;

            FriendNames = new List<string>()
            {
                "apollo kalar", "apollokalar", "apollo_kalar",
                "flygon jones", "flygonjones", "flygon_jones",
                "starkiller106024", "starkiller", "star killer",
                "atomic vexal", "vexal", "wave vex",
                "therichpig", "therichpig64", "spaghettipig64", "spaghettipig",
                "theeethersplash", "the aether splash", "aethersplash", "aether splash"
            };
        }
    }

    public class PartyInfoStorage
    {
        public PartyInfo party_info = new PartyInfo();

        public PartyInfo GetPartyInfo()
        {
            return party_info;
        }
    }
}
