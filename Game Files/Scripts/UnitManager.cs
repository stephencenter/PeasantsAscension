using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public class UnitManager
    {
        readonly Unit player = new Unit(CEnums.UnitType.player, "John", "_player", true);
        readonly Unit solou = new Unit(CEnums.UnitType.player, "Solou", "_solou", true);
        readonly Unit chili = new Unit(CEnums.UnitType.player, "Chili", "_chili", true);
        readonly Unit chyme = new Unit(CEnums.UnitType.player, "Chyme", "_chyme", false);
        readonly Unit storm = new Unit(CEnums.UnitType.player, "Storm", "_storm", false);
        readonly Unit parsto = new Unit(CEnums.UnitType.player, "Parsto", "_parsto", false);
        readonly Unit adorine = new Unit(CEnums.UnitType.player, "Adorine", "_adorine", false);
        readonly CommonMethods c_methods = new CommonMethods();

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

        public Unit GenerateMonster()
        {
            return new Unit(CEnums.UnitType.monster, "Whispering Goblin");
        }
    }

    public class Unit
    {
        // General Unit Properties
        public Dictionary<CEnums.Element, List<CEnums.Element>> ElementChart = new Dictionary<CEnums.Element, List<CEnums.Element>>
        {
            {CEnums.Element.fire, new List<CEnums.Element> { CEnums.Element.water, CEnums.Element.ice } },
            {CEnums.Element.water, new List<CEnums.Element> { CEnums.Element.electric, CEnums.Element.fire } },
            {CEnums.Element.electric, new List<CEnums.Element> { CEnums.Element.earth, CEnums.Element.water } },
            {CEnums.Element.earth, new List<CEnums.Element> { CEnums.Element.wind, CEnums.Element.electric } },
            {CEnums.Element.wind, new List<CEnums.Element> { CEnums.Element.grass, CEnums.Element.earth } },
            {CEnums.Element.grass, new List<CEnums.Element> { CEnums.Element.ice, CEnums.Element.wind } },
            {CEnums.Element.ice, new List<CEnums.Element> { CEnums.Element.fire, CEnums.Element.grass } },
            {CEnums.Element.light, new List<CEnums.Element> { CEnums.Element.light, CEnums.Element.dark } },
            {CEnums.Element.dark, new List<CEnums.Element> { CEnums.Element.dark, CEnums.Element.light } }
        };
        public CEnums.Element off_element = CEnums.Element.none;
        public CEnums.Element def_element = CEnums.Element.none;
        public CEnums.UnitType Type { get; set; }
        public List<CEnums.Status> Statuses = new List<CEnums.Status> { CEnums.Status.alive, CEnums.Status.blindness };

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
        public string PCUID { get; set; }
        public CEnums.CharacterClass PClass { get; set; }
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

        public Dictionary<string, dynamic> PlayerAbilityFlags = new Dictionary<string, dynamic>()
        {
            {"ascend_used", false },
            {"berserk", false },
            {"rolling", false }
        };

        // Monster Attributes
        public CEnums.MonsterClass MClass { get; set; }
        public CEnums.Status StatusOnAttack { get; set; }
        public bool IsDefending { get; set; }
        public int DroppedGold { get; set; }
        public int DroppedXP { get; set; }
        public List<ItemManager> DroppedItems { get; set; }
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

        // Unit methods
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
            return !HasStatus(CEnums.Status.dead);
        }

        public bool IsPCU()
        {
            return Type == CEnums.UnitType.player;
        }

        public bool IsMonster()
        {
            return (Type == CEnums.UnitType.monster || Type == CEnums.UnitType.boss);
        }

        public bool IsBoss()
        {
            return Type == CEnums.UnitType.boss;
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
            CommonMethods c_methods = new CommonMethods();

            HP = c_methods.Clamp(HP, MaxHP, 0);
            MP = c_methods.Clamp(MP, MaxMP, 0);
            AP = c_methods.Clamp(AP, MaxAP, 0);

            Evasion = Math.Min(256, Evasion);
            Statuses = Statuses.Distinct().ToList();

            TempStats["evasion"] = Math.Min(PlayerAbilityFlags["rolling"] ? 512 : 256, TempStats["evasion"]);

            if (HP > 0 && !IsAlive())
            {
                Statuses = new List<CEnums.Status>() { CEnums.Status.alive };
            }

            if (!IsAlive())
            {
                Statuses = new List<CEnums.Status>() { CEnums.Status.dead };
            }
        }

        // Player methods
        public void PrintBattleOptions()
        {
            Console.WriteLine($"Pick {Name}'s Move:\n      [1] Standard Attack\n      [2] Use Magic\n      [3] Use Abilities\n      [4] Use Items\n      [5] Run");
        }

        public void PlayerChoice(List<Unit> monster_list)
        {
            // Initialize some important method helpers
            CommonMethods c_methods = new CommonMethods();
            SpellManager spell_manager = new SpellManager();
            AbilityManager ability_manager = new AbilityManager();
            InventoryManager inv_manager = new InventoryManager();
            SoundManager sound_manager = new SoundManager();
            BattleManager battle_manager = new BattleManager();

            PrintBattleOptions();

            while (true)
            {
                string c_move = c_methods.Input("Input [#]: ");

                try
                {
                    CurrentMove = string.Join("", c_move.Where(x => char.IsDigit(x)))[0];
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
                    if (HasStatus(CEnums.Status.silence))
                    {
                        sound_manager.debuff.Play();
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
                        int padding = a_list.Select(x => x.AbilityName.Length).Max();

                        int counter = 0;
                        foreach (Ability ability in a_list)
                        {
                            int true_pad = padding - ability.AbilityName.Length;
                            Console.WriteLine($"      [{counter + 1}] {ability.AbilityName} {new string('-', true_pad)}--> {ability.APCost} AP");
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
                                    if (c_methods.IsExitString(chosen_ability))
                                    {
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
                    c_methods.PrintDivider();

                    var x = new List<int>();
                    if (!inv_manager.GetInventory()["consumables"].Any())
                    {
                        sound_manager.debuff.Play();
                        Console.WriteLine("Your party has no consumables!");

                        c_methods.PressEnterReturn();
                        c_methods.PrintDivider();
                        PrintBattleOptions();

                        continue;
                    }

                    if (HasStatus(CEnums.Status.muted))
                    {
                        sound_manager.debuff.Play();
                        Console.WriteLine($"{Name} can't use items when muted!");

                        c_methods.PressEnterReturn();
                        c_methods.PrintDivider();
                        PrintBattleOptions();

                        continue;
                    }

                    if (!battle_manager.BattleInventory(this))
                    {
                        PrintBattleOptions();

                        continue;
                    }

                    c_methods.PressEnterReturn();
                    return;
                }

                // Run
                else if (CurrentMove == '5')
                {
                    return;
                }
            }
        }

        public string PCUExecuteMove(List<Unit> monster_list)
        {
            /*
            if isinstance(self.target, Monster) and 'dead' in self.target.status_ail:
                self.target = random.choice([x for x in battle.m_list if 'dead' not in x.status_ail])

            inv_name = self.name if self != player else 'player'
            player_weapon = items.equipped[inv_name]['weapon']

            print(f"-{self.name}'s Turn-")

            # PCUs regain 1 Action Point per turn. This regeneration is paused on turns where
            # the player uses an ability.
            if self.move != '3':
                self.ap += 1

            # Check to see if the PCU is poisoned
            if 'poisoned' in self.status_ail and monster.hp > 0:
                main.smart_sleep(0.75)
                sounds.poison_damage.play()
                poison_damage = math.floor(self.hp/5)
                self.hp -= poison_damage

                print(f'{self.name} took poison damage! (-{poison_damage} HP)')

                if self.hp <= 0:
                    return */

            Random rng = new Random();
            InventoryManager inv_manager = new InventoryManager();

            // sounds.item_pickup.stop()

            // If the player's target is an enemy, and the target died before the player's turn began,
            // then the attack automatically redirects to a random living enemy.
            if (CurrentTarget != null && CurrentTarget.IsMonster() && !CurrentTarget.IsAlive())
            {
                CurrentTarget = monster_list[rng.Next(monster_list.Count)];
            }

            Weapon player_weapon = inv_manager.GetEquipped(PCUID)["weapon"];

            Console.WriteLine($"-{Name}'s Turn-");

            // PCUs regenerate 1 Action Point per turn, unless they used an ability that turn
            if (CurrentMove != '3')
            {
                AP++;
            }

            if (HasStatus(CEnums.Status.poison))
            {
                Thread.Sleep(750);

                // sounds.poison_damage.play()

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
                if (status != CEnums.Status.alive && rng.Next(0, 5) == 0)
                {
                    // sounds.buff_spell.play()
                }
            }

            return "run";
        
            /*
            for x in self.status_ail:
                if x != "alive" and random.randint(0, 3) == 3:
                    sounds.buff_spell.play()
                    self.status_ail = [y for y in self.status_ail if y != x]
                    print(f"{self.name} is no longer {x}!")
                    main.smart_sleep(0.5)
                    break

            # Basic Attack
            if self.move == '1':
                print(ascii_art.player_art[self.class_.title()] % f"{self.name} is making a move!\n")

                if items.equipped[inv_name]['weapon'].type_ == 'melee':
                    sounds.sword_slash.play()
                    print(f'{self.name} fiercely attacks the {self.target.name} using their {player_weapon.name}...')

                elif items.equipped[inv_name]['weapon'].type_ == 'instrument':
                    random.choice(sounds.bard_sounds[items.equipped[inv_name]['weapon'].item_id]).play()
                    print(f'{self.name} starts playing their {player_weapon.name} at the {self.target.name}...')

                else:
                    sounds.aim_weapon.play()
                    print(f'{self.name} aims carefully at the {self.target.name} using their {player_weapon.name}...')

                main.smart_sleep(0.75)

                if items.equipped[inv_name]['weapon'].type_ == 'melee':
                    dam_dealt = deal_damage(self, self.target, "physical")

                elif items.equipped[inv_name]['weapon'].type_ == 'ranged':
                    dam_dealt = deal_damage(self, self.target, "piercing")

                else:
                    dam_dealt = deal_damage(self, self.target, "magical")

                # Check for attack accuracy.
                if random.randint(1, 512) in range(self.target.evad, 512):
                    print(f"{self.name}'s attack connects with the {self.target.name}, dealing {dam_dealt} damage!")

                    sounds.enemy_hit.play()
                    self.target.hp -= dam_dealt

                else:
                    print(f"The {self.target.name} narrowly avoids {self.name}'s attack!")
                    sounds.attack_miss.play()

            if self.move == '2':
                self.c_spell.use_magic(self, True)

            elif self.move == '3':
                print(ascii_art.player_art[self.class_.title()] % f"{self.name} is making a move!\n")
                self.c_ability.use_ability(self)

            # Run away!
            elif self.move == '5' and battle.run_away(self):
                sounds.play_music(main.party_info['music'])

                return 'Ran'

            return */
        }

        public bool ChooseTarget(List<Unit> monster_list, string action_desc, bool target_allies, bool target_enemies, bool allow_dead, bool allow_inactive)
        {
            // Initialize important method helpers
            CommonMethods c_methods = new CommonMethods();
            UnitManager unit_manager = new UnitManager();

            // A list of PCUs that are valid for targetting (could be unused if target_allies is false)
            List<Unit> pcu_list;

            if (allow_inactive)
            {
                if (allow_dead)
                {
                    // YES to dead PCUs, YES to inactive PCUs
                    pcu_list = unit_manager.GetAllPCUs();
                }

                else
                {
                    // NO to dead PCUs, YES to inactive PCUs
                    pcu_list = unit_manager.GetAlivePCUs();
                }
            }

            else
            {
                if (allow_dead)
                {
                    // YES to dead PCUs, NO to inactive PCUs
                    pcu_list = unit_manager.GetActivePCUs();
                }

                else
                {
                    // NO to dead PCUs, NO to inactive PCUs
                    pcu_list = unit_manager.GetAliveActivePCUs();
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
                Console.WriteLine($"      [{counter + 1} {unit.Name}");
            }

            while (true)
            {
                string chosen = c_methods.Input("Input [#]: ");

                try
                {
                    CurrentTarget = valid_targets[int.Parse(chosen) - 1];
                }

                catch (Exception ex)
                {
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

        // Monster methods
        public string MonsterExecuteMove()
        {
            return "run";
        }

        // Constructors
        public Unit(CEnums.UnitType unit_type, string name)
        {
            // Create a monster
            if (unit_type != CEnums.UnitType.monster)
            {
                throw new Exception("Can't create a non-monster with this constructor");
            }

            Type = CEnums.UnitType.monster;
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

            DroppedItems = new List<ItemManager>();
            MClass = CEnums.MonsterClass.melee;
            StatusOnAttack = CEnums.Status.paralyzation;
            IsDefending = false;
            DroppedGold = 5;
            DroppedXP = 5;
            AttackMessage = "attacks";
            AsciiArt = "";
        }

        public Unit(CEnums.UnitType unit_type, string name, string pcu_id, bool active)
        {
            // Create a pcu
            if (unit_type != CEnums.UnitType.player)
            {
                throw new Exception("Can't create a non-player with this constructor");
            }

            Type = CEnums.UnitType.player;
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

            PCUID = pcu_id;
            Active = active;
            CurrentXP = 0;
            RequiredXP = 3;
            AP = 10;
            MaxAP = 10;
        }
    }

    public class PartyInfo
    {
        public GameState Gamestate { get; set; }
        public Mode MusicboxMode { get; set; }
        public List<TownManager> VisitedTowns { get; set; }
        public TileManager CurrentTile { get; set; }
        public TileManager RespawnTile { get; set; }
        public TownManager CurrentTown { get; set; }
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
            VisitedTowns = new List<TownManager>();
            CurrentTile = new TileManager();
            RespawnTile = new TileManager();
            CurrentTown = new TownManager();
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
