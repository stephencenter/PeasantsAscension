using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public static class UnitManager
    {
        public static Unit player = new Unit(CEnums.UnitType.player, "John", "_player", true);
        public static Unit solou = new Unit(CEnums.UnitType.player, "Solou", "_solou", true);
        public static Unit chili = new Unit(CEnums.UnitType.player, "Chili", "_chili", true);
        public static Unit chyme = new Unit(CEnums.UnitType.player, "Chyme", "_chyme", false);
        public static Unit storm = new Unit(CEnums.UnitType.player, "Storm", "_storm", false);
        public static Unit parsto = new Unit(CEnums.UnitType.player, "Parsto", "_parsto", false);
        public static Unit adorine = new Unit(CEnums.UnitType.player, "Adorine", "_adorine", false);

        // Returns ALL PCUs, alive, dead, active, and inactive
        public static List<Unit> GetAllPCUs()
        {
            return new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };
        }

        // Returns all PCUs that are alive, regardless of whether they're active or not
        public static List<Unit> GetAlivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };
            pcu_list = pcu_list.Where(x => x.IsAlive()).ToList();

            return pcu_list;
        }

        // Returns all PCUs that are active, regardless of whether they're alive or not
        public static List<Unit> GetActivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };
            pcu_list = pcu_list.Where(x => x.Active).ToList();

            return pcu_list;
        }

        // Returns all PCUs that are both alive and active
        public static List<Unit> GetAliveActivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };
            pcu_list = pcu_list.Where(x => x.Active && x.IsAlive()).ToList();

            return pcu_list;
        }

        public static Unit GenerateMonster()
        {
            return new Unit(CEnums.UnitType.monster, "Whispering Goblin");
        }

        public static int CalculateDamage(Unit attacker, Unit target, CEnums.DamageType damage_type, int spell_power = 0, bool do_criticals = true)
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

            if (attacker.IsPCU())
            {
                weapon_power = InventoryManager.GetEquipment(attacker.PCUID)[CEnums.EquipmentType.weapon].Power;

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

            if (target.IsPCU())
            {
                double a = InventoryManager.GetEquipment(target.PCUID)[CEnums.EquipmentType.head].Resist;
                double b = InventoryManager.GetEquipment(target.PCUID)[CEnums.EquipmentType.body].Resist;
                double c = InventoryManager.GetEquipment(target.PCUID)[CEnums.EquipmentType.legs].Resist;
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

                // Mages deal half damage with non-magical attacks
                if (attacker.PClass == CEnums.CharacterClass.mage)
                {
                    final_damage /= 2;
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

                // Mages deal half damage with non-magical attacks
                if (attacker.PClass == CEnums.CharacterClass.mage)
                {
                    final_damage /= 2;
                }
            }

            else
            {
                final_damage = (int)((m_attack - m_defense / 2) * (1 + armor_resist) * (1 + spell_power));

                // Classes that aren't mages or paladins deal 0.75x damage with magical attacks
                if (attacker.PClass == CEnums.CharacterClass.mage || attacker.PClass == CEnums.CharacterClass.paladin)
                {
                    final_damage = (int) (final_damage*0.75);
                }
            }

            if (rng.Next(0, 100) < 15 && do_criticals)
            {
                final_damage = (int)(final_damage*1.5);
                SoundManager.critical_hit.Play();
                Console.WriteLine("It's a critical hit! 1.5x damage!");

                Thread.Sleep(500);
            }

            final_damage = ApplyElementalChart(attacker, target, final_damage);
            final_damage = CMethods.Clamp(final_damage, 999, 1);

            return final_damage;
        }

        public static int ApplyElementalChart(Unit attacker, Unit target, int damage)
        {
            // Fire > Ice > Grass > Wind > Electricity > Earth > Water > Fire
            // Light > Dark and Dark > Light, Dark and Light resist themselves
            // Neutral element is neutral both offensively and defensively
            // All other interactions are neutral

            CEnums.Element attacker_element = attacker.off_element;
            CEnums.Element target_element = target.def_element;

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
    }

    public static class PartyInfo
    {
        public static CEnums.GameState Gamestate = CEnums.GameState.overworld;
        public static CEnums.MusicboxMode MusicboxMode = CEnums.MusicboxMode.AtoZ;
        public static List<Town> VisitedTowns = new List<Town>();
        public static Town CurrentTown = new Town();
        public static Tile CurrentTile = new Tile();
        public static Tile RespawnTile = new Tile();
        public static int GP = 20;
        public static int StepsWithoutBattle = 0;
        public static int Difficulty = 0;
        public static int AtlasStrength = 1;
        public static string Music = "../../../Music/Through the Forest.ogg";
        public static string CurrentProvince = "Overshire";
        public static string MusicboxFolder = "";
        public static bool MusicboxIsPlaying = false;
        public static bool DoSpawns { get; set; }

        public static List<string> FriendNames = new List<string>()
        {
            "apollo kalar", "apollokalar", "apollo_kalar",
            "flygon jones", "flygonjones", "flygon_jones",
            "starkiller106024", "starkiller", "star killer",
            "atomic vexal", "vexal", "wave vex",
            "therichpig", "therichpig64", "spaghettipig64", "spaghettipig", "pastahog", "pastahog64",
            "theaethersplash", "the aether splash", "aethersplash", "aether splash"
        };
    }

    public class Unit
    {
        /* =========================== *
         *      GENERAL PROPERTIES     *
         * =========================== */
        public CEnums.Element off_element = CEnums.Element.neutral;
        public CEnums.Element def_element = CEnums.Element.neutral;
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

        /* =========================== *
         *      PLAYER PROPERTIES      *
         * =========================== */
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

        /* =========================== *
         *      MONSTER PROPERTIES     *
         * =========================== */
        public CEnums.MonsterClass MClass { get; set; }
        public CEnums.Status StatusOnAttack { get; set; }
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
            {"judgment_day", 0},
            {"taunted_turn", 0},
            {"taunted_user", null},
            {"drained", false},
            {"disarmed", false}
        };

        /* =========================== *
         *        GENERAL METHODS      *
         * =========================== */
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

            HP = CMethods.Clamp(HP, MaxHP, 0);
            MP = CMethods.Clamp(MP, MaxMP, 0);
            AP = CMethods.Clamp(AP, MaxAP, 0);

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

        /* =========================== *
         *        PLAYER METHODS       *
         * =========================== */
        public void PrintBattleOptions()
        {
            Console.WriteLine($"Pick {Name}'s Move:\n      [1] Standard Attack\n      [2] Use Magic\n      [3] Use Abilities\n      [4] Use Items\n      [5] Run");
        }

        public void PlayerChoice(List<Unit> monster_list)
        {
            PrintBattleOptions();

            while (true)
            {
                string c_move = CMethods.Input("Input [#]: ");

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

                    if (!SpellManager.PickSpellCategory())
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
                                if (ex is ArgumentException || ex is IndexOutOfRangeException)
                                {
                                    if (CMethods.IsExitString(chosen_ability))
                                    {
                                        CMethods.PrintDivider();
                                        PrintBattleOptions();

                                        return;
                                    }

                                    continue;
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

                            return;
                        }
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

        public string PlayerExecuteMove(List<Unit> monster_list)
        {
            Random rng = new Random();

            SoundManager.item_pickup.Stop();

            // If the player's target is an enemy, and the target died before the player's turn began,
            // then the attack automatically redirects to a random living enemy.
            if (CurrentTarget != null && CurrentTarget.IsMonster() && !CurrentTarget.IsAlive())
            {
                CurrentTarget = monster_list[rng.Next(monster_list.Count)];
            }

            Weapon player_weapon = InventoryManager.GetEquipment(PCUID)[CEnums.EquipmentType.weapon];

            Console.WriteLine($"-{Name}'s Turn-");

            // PCUs regenerate 1 Action Point per turn, unless they used an ability that turn
            if (CurrentMove != '3')
            {
                AP++;
            }

            if (HasStatus(CEnums.Status.poison))
            {
                Thread.Sleep(750);

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
                    Thread.Sleep(500);

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

                Thread.Sleep(750);

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

        public bool PlayerGetTarget(List<Unit> monster_list, string action_desc, bool target_allies, bool target_enemies, bool allow_dead, bool allow_inactive)
        {
            // A list of PCUs that are valid for targetting (could be unused if target_allies is false)
            List<Unit> pcu_list;

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

            CMethods.PrintDivider();
            Console.WriteLine(action_desc);

            int counter = 0;
            foreach (Unit unit in valid_targets)
            {
                Console.WriteLine($"      [{counter + 1}] {unit.Name}");
            }

            while (true)
            {
                string chosen = CMethods.Input("Input [#]: ");

                try
                {
                    CurrentTarget = valid_targets[int.Parse(chosen) - 1];
                }

                catch (Exception ex)
                {
                    if (ex is ArgumentException || ex is IndexOutOfRangeException)
                    {
                        if (CMethods.IsExitString(chosen))
                        {
                            return false;
                        }

                        continue;
                    }
                }

                return true;
            }
        }

        /* =========================== *
         *        MONSTER METHODS      *
         * =========================== */
        public void MonsterExecuteMove(int turn_count)
        {
            // Base Turn
            SoundManager.item_pickup.Stop();
            MonsterGetTarget(turn_count);

            Console.WriteLine($"-{Name}'s Turn-");

            if (!(MonsterAbilityFlags["knockout_turns"] > 0))
            {
                Console.WriteLine($"The {Name} is making a move!\n");

                if (MClass == CEnums.MonsterClass.melee)
                {
                    MonsterMeleeAI();
                }

                else if (MClass == CEnums.MonsterClass.ranged)
                {
                    MonsterRangedAI();
                }

                else if (MClass == CEnums.MonsterClass.magic)
                {
                    MonsterMagicAI();
                }
            }

            else
            {
                Console.WriteLine($"The {Name} is asleep!");
            }

            MonsterDoAbilities();
        }

        public void MonsterGetTarget(int turn_count)
        {
            Random rng = new Random();

            CurrentTarget = UnitManager.GetAliveActivePCUs()[rng.Next(UnitManager.GetAliveActivePCUs().Count)];

            if (MonsterAbilityFlags["taunted_turn"] == turn_count)
            {
                CurrentTarget = MonsterAbilityFlags["taunted_user"];
            }
        }

        public void MonsterDoAbilities()
        {
            /*
            def do_abilities(self):
            if self.ability_vars['knockout_turns']:
                self.ability_vars['knockout_turns'] -= 1

                if not self.ability_vars['knockout_turns']:
                    main.smart_sleep(0.5)
                    sounds.buff_spell.play()
                    self.status_ail = [x for x in self.status_ail if x != "asleep"]
                    print(f"The {self.name} woke up!")

                else:
                    chance = 25 if isinstance(self, Boss) else 10

                    if random.randint(0, 100) < chance:
                        main.smart_sleep(0.5)
                        sounds.buff_spell.play()
                        self.ability_vars['knockout_turns'] = 0
                        self.status_ail = [x for x in self.status_ail if x != "asleep"]
                        print(f"The {self.name} woke up early!")

            if 'poisoned' in self.status_ail:
                main.smart_sleep(0.5)
                damage = math.ceil(self.ability_vars['poison_pow'] * self.max_hp + self.ability_vars['poison_dex'])
                self.hp -= damage
                print(f"The {self.name} took {damage} damage from poison!")
                sounds.poison_damage.play()

            if self.ability_vars['judgment_day'] == battle.turn_counter:
                main.smart_sleep(0.5)
                print(f"{self.name}'s judgment day has arrived. The darkness devours it...")
                sounds.poison_damage.play()
                self.hp = 0 */
        }

        public void MonsterMeleeAI()
        {
            Random rng = new Random();

            // Melee monsters have a 1 in 6 (16.667%) chance to defend
            if (rng.Next(0, 5) == 0 && !IsDefending && !(MonsterAbilityFlags["taunted_turn"] == BattleManager.turn_counter))
            {
                IsDefending = true;
                Console.WriteLine($"The {Name} is preparing itself for enemy attacks...");
                Thread.Sleep(750);

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
            Thread.Sleep(750);

            int attack_damage = UnitManager.CalculateDamage(this, CurrentTarget, CEnums.DamageType.physical);

            if (CurrentTarget.Evasion < rng.Next(0, 512))
            {
                SoundManager.enemy_hit.Play();
                Console.WriteLine($"The {Name}'s attack deals {attack_damage} damage to {CurrentTarget}!");
            }

            else
            {
                SoundManager.attack_miss.Play();
                Console.WriteLine($"The {Name}'s attack narrowly misses {CurrentTarget.Name}!");
            }
        }

        public void MonsterRangedAI()
        {
            /*
            // At the moment, Ranged monsters are only capable of attacking
            print(f'The {self.name} {self.attk_msg} {self.m_target.name}!')
            sounds.aim_weapon.play()

            main.smart_sleep(0.75)

            if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                dam_dealt = deal_damage(self, self.m_target, 'piercing')

                print(f"The {self.name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

                self.m_target.hp -= dam_dealt
                sounds.enemy_hit.play()

            else:
                sounds.attack_miss.play()
                print(f"The {self.name}'s attack narrowly misses {self.m_target.name}!") */
        }

        public void MonsterMagicAI()
        {
            /*
            // 16.67% chance for the enemy to give a status ailment
            if not self.ability_vars['taunted'][0] == battle.turn_counter or 'silenced' in self.status_ail:
                if random.randint(0, 7) == 0 and self.mp >= self.max_mp*0.1:
                    self.give_status(self.m_target)

                    return

                // Magic heal
                elif self.hp <= self.max_hp/5 and self.mp >= self.max_mp*0.2:
                    print(f'The {self.name} is casting a healing spell on itself...')
                    main.smart_sleep(0.75)

                    healing_power = math.ceil(max([self.hp*0.2, 5]))
                    self.hp += min([self.hp*0.2, 5])
                    self.mp -= self.max_mp*0.2

                    print(f'The {self.name} heals itself for {healing_power} HP!')
                    sounds.magic_healing.play()

                    return

                // Magical Attack
                elif self.mp >= self.max_mp*0.15:

                    sounds.magic_attack.play()

                    print(f'The {self.name} is preparing to cast a spell on {self.m_target.name}!')
                    main.smart_sleep(0.75)

                    dam_dealt = deal_damage(self, self.m_target, "magical")

                    if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                        sounds.enemy_hit.play()
                        print(f"The {self.name}'s spell deals {dam_dealt} damage to {self.m_target.name}!")

                        self.m_target.hp -= dam_dealt

                    else:
                        sounds.attack_miss.play()
                        print(f"The {self.name}'s spell narrowly misses {self.m_target.name}!")

                    self.mp -= self.max_mp*0.15

                    return

            // Non-magical Attack (Pierce Damage). Only happens if taunted, silenced, or if out of mana.
            sounds.aim_weapon.play()
            print(f'The {self.name} {self.attk_msg} {self.m_target.name}')

            main.smart_sleep(0.75)

            dam_dealt = deal_damage(self, self.m_target, "piercing")

            if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                sounds.enemy_hit.play()
                print(f"The {self.name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

                self.m_target.hp -= dam_dealt

            else:
                sounds.attack_miss.play()
                print(f"The {self.name}'s attack narrowly misses {self.m_target.name}!") */
        }

        /* =========================== *
         *         CONSTRUCTORS        *
         * =========================== */
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

            DroppedItems = new List<Item>();
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
}
