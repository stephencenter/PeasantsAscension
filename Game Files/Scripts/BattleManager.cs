﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public static class BattleManager
    {
        public static int turn_counter;

        public static void BattleSystem(bool is_bossfight)
        {
            Random rng = new Random();

            List<Monster> monster_list = new List<Monster>() { UnitManager.GenerateMonster() };
            List<PlayableCharacter> active_pcus = UnitManager.GetActivePCUs();
            turn_counter = 0;

            // 33% chance to add a second monster
            if (rng.Next(0, 100) > 66)
            {
                monster_list.Add(UnitManager.GenerateMonster());

                // 33% chance to add a third monster if a second monster was already added
                if (rng.Next(0, 100) > 66)
                {
                    monster_list.Add(UnitManager.GenerateMonster());
                }
            }

            if (is_bossfight)
            {
                Console.WriteLine($"The legendary {monster_list[0].Name} has awoken!");
                // sounds.play_music("../../../Music/Terrible Tarantuloid.ogg")
            }

            else
            {
                if (monster_list.Count == 1)
                {
                    Console.WriteLine($"A {monster_list[0].Name} suddenly appeared out of nowhere!");
                }

                else if (monster_list.Count == 2)
                {
                    Console.WriteLine($"A {monster_list[0].Name} and 1 other monster suddenly appeared out of nowhere!");
                }

                else if (monster_list.Count > 2)
                {
                    Console.WriteLine($"A {monster_list[0].Name} and {monster_list.Count - 1} other monsters suddenly appeared out of nowhere!"); ;
                }

                // sounds.play_music('../Music/Ruari 8-bit Battle.ogg')
            }

            CMethods.SmartSleep(1000);

            // Create a temporary copy of all of the player's stats. These copies are what will be modified in-battle by 
            // spells, abilities, etc. so that they will return to normal after battle (although they in fact were never 
            // touched to begin with)
            active_pcus.ForEach(x => x.SetTempStats());

            // While all active party members are alive, continue the battle
            while (monster_list.Any(x => x.HP > 0) && active_pcus.Any(x => x.HP > 0))
            {
                turn_counter++;

                List<dynamic> speed_list = new List<dynamic>();
                active_pcus.ForEach(x => speed_list.Add(x));
                monster_list.ForEach(x => speed_list.Add(x));

                // Display the stats for every battle participant
                DisplayBattleStats(active_pcus, monster_list);

                // Iterate through each active players
                foreach (PlayableCharacter character in UnitManager.GetAliveActivePCUs())
                {
                    if (0 < character.HP && character.HP <= character.MaxHP * 0.20)
                    {
                        Console.WriteLine($"Warning: {character.Name}'s HP is low, heal as soon as possible!");
                        SoundManager.health_low.Play();
                        CMethods.SmartSleep(1333);
                    }

                    character.PlayerChoice(monster_list);

                    if (character != UnitManager.GetAliveActivePCUs().Last())
                    {
                        CMethods.PrintDivider();
                    } 
                }

                // Iterate through each unit in the battle from fastest to slowest
                foreach (dynamic unit in speed_list)
                {
                    if (unit.IsAlive())
                    {
                        if (monster_list.All(x => x.HP <= 0))
                        {
                            break;
                        }

                        CMethods.PrintDivider();

                        // Leave the battle if the player runs away
                        if (unit is PlayableCharacter && unit.PlayerExecuteMove(monster_list) == "ran")
                        {
                            return;
                        }

                        else if (unit is Monster)
                        {
                            unit.MonsterExecuteMove();
                        }

                        if (active_pcus.Any(x => x.HP > 0))
                        {
                            if (monster_list.Any(x => x.HP > 0) && unit.IsAlive())
                            {
                                CMethods.PressEnterReturn();
                            }

                            else if (monster_list.All(x => x.HP <= 0))
                            {
                                break;
                            }
                        }

                        else
                        {
                            break;
                        }
                    }

                    // If any unit died on this turn, set their health to 0 and set their status as 'dead'
                    foreach (dynamic other_unit in speed_list)
                    {
                        if (other_unit is PlayableCharacter && other_unit.HP <= 0 && other_unit.IsAlive())
                        {
                            other_unit.HP = 0;
                            other_unit.Statuses = new List<CEnums.Status> { CEnums.Status.dead };
                            SoundManager.ally_death.Play();

                            CMethods.PrintDivider();
                            Console.WriteLine($"{other_unit.Name} has fallen to the monsters!");
                            CMethods.PressEnterReturn();
                        }

                        else if (other_unit is Monster && other_unit.HP <= 0 && other_unit.IsAlive())
                        {
                            other_unit.HP = 0;
                            other_unit.Statuses = new List<CEnums.Status> { CEnums.Status.dead };
                            SoundManager.enemy_death.Play();

                            CMethods.PrintDivider();
                            Console.WriteLine($"The {other_unit.Name} was defeated by your party!");
                            CMethods.PressEnterReturn();
                        }
                    }
                }
            }

            // Determine the results of the battle and react accordingly
            AfterBattle(active_pcus, monster_list, is_bossfight);
        }

        public static void AfterBattle(List<PlayableCharacter> active_pcus, List<Monster> monster_list, bool is_bossfight)
        {
            CMethods.PrintDivider();

            foreach(PlayableCharacter pcu in active_pcus)
            {
                pcu.FixAllStats();
            }

            foreach(Monster monster in monster_list)
            {
                monster.FixAllStats();
            }

            if (active_pcus.Any(x => x.IsAlive()))
                {
                    // sounds.play_music("../../../Music/Python_RM.ogg")
                    if (is_bossfight)
                    {
                        Console.WriteLine($"The mighty {monster_list[0].Name} has been slain!");
                        PartyInfo.DefeatedBosses.Add(monster_list[0].UnitID);
                        monster_list[0].UponDefeating();
                    }

                    else
                    {
                        Console.WriteLine($"The {monster_list[0].Name} falls to the ground dead as a stone.");
                    }

                    int gold_drops = 0;
                    monster_list.ForEach(x => gold_drops += new List<int>() { 1, x.DroppedGold, (int)(1.8 * x.Level) }.Max());

                    int expr_drops = 0;
                    monster_list.ForEach(x => expr_drops += new List<int>() { 1, x.DroppedXP, (int)(Math.Pow(1.3, x.Level)) }.Max());

                    Dictionary<string, string> item_drops = new Dictionary<string, string>();
                    foreach (Monster monster in monster_list)
                    {
                        if (monster.DroppedItem != null || monster.GetDrops())
                        {
                            item_drops.Add(monster.Name, monster.DroppedItem);
                        }
                    }

                    PartyInfo.GP += gold_drops;
                    CMethods.Input($"Your party got {gold_drops} GP!");

                    foreach (PlayableCharacter pcu in active_pcus)
                    {
                        pcu.CurrentXP += expr_drops;
                        CMethods.Input($"{pcu.Name} gained {expr_drops} XP!");
                    }

                    foreach (KeyValuePair<string, string> drop in item_drops)
                    {
                        CMethods.Input($"The {drop.Key} dropped a {ItemManager.FindItemWithID(drop.Value).Name}!");
                        InventoryManager.AddItemToInventory(drop.Value);
                    }

                    foreach (PlayableCharacter pcu in active_pcus)
                    {
                        pcu.PlayerLevelUp();
                    }

                    // sounds.play_music(main.party_info['music'])
                }

                else
                {
                    // sounds.play_music("../../../Music/Power-Up.ogg")
                    Console.WriteLine($"Despite your best efforts, the {monster_list[0].Name} has killed your party.");
                    CMethods.PrintDivider();

                    bool auto_yes = false;
                    while (true)
                    {
                        string y_n;

                        if (auto_yes)
                        {
                            y_n = "y";
                        }

                        else
                        {
                            y_n = CMethods.Input("Do you wish to continue playing? | Yes or No: ");
                        }

                        if (CMethods.IsYesString(y_n))
                        {
                            PartyInfo.CurrentTile = PartyInfo.RespawnTile;
                            UnitManager.HealAllPCUs(1, true, true, true);
                            //sounds.play_music(main.party_info['music'])

                            return;
                        }

                        else if (CMethods.IsNoString(y_n))
                        {
                            while (true)
                            {
                                string y_n2 = CMethods.Input("Are you sure you want to quit and lose unsaved progress? |  Y/N: ");

                                if (CMethods.IsYesString(y_n2))
                                {
                                    auto_yes = true;
                                    break;
                                }

                                else if (CMethods.IsNoString(y_n2))
                                {
                                    System.Environment.Exit(0);
                                }
                            }
                        }
                    }
                }
        }

        public static bool RunAway(Unit runner, List<Monster> monster_list)
        {
            Random rng = new Random();

            Console.WriteLine($"{runner.Name} is making a move!\n");
            Console.WriteLine($"Your party tries to make a run for it...");
            CMethods.SmartSleep(750);

            int chance;

            // Running has a 30% chance of success if the runner is paralyzed, regardless of 
            if (runner.HasStatus(CEnums.Status.paralyzation))
            {
                chance = 30;
            }

            // Running has a 70% chance of success if the runner:
            //     1. Has a higher speed than the fastest monster, but a lower evasion than the most evasive monster
            //     2. Has a higher evasion than the most evasive monster, but a lower speed than the fastest monster
            else if ((runner.Speed > monster_list.Select(x => x.Speed).Max()) != (runner.Evasion > monster_list.Select(x => x.Evasion).Max()))
            {
                chance = 70;
            }

            // Running has an 90% chance of success if the runner is both:
            //    1. Faster than the fastest monster
            //    2. More evasive than the most evasive monster
            else if ((runner.Speed > monster_list.Select(x => x.Speed).Max()) && (runner.Evasion > monster_list.Select(x => x.Evasion).Max()))
            {
                chance = 90;
            }

            // In all other scenarios, running has a 50% chance to succeed
            else
            {
                chance = 50;
            }

            if (rng.Next(0, 100) < chance)
            {
                SoundManager.buff_spell.Play();
                Console.WriteLine("Your party managed to escape!");
                CMethods.PressEnterReturn();

                return true;
            }

            else
            {
                SoundManager.debuff.Play();
                Console.WriteLine("Your party's escape attempt failed!");
                return false;
            }
        }

        public static bool BattleInventory(Unit user)
        {
            return true;
            //def battle_inventory(user):
            //    # The player can use items from the Consumables category of their inventory during battles.
            //    while True:
            //        print('Battle Inventory: ')

            //        for x, y in enumerate(items.inventory['consumables']) :
            //            print(f'      [{x + 1}] {y.name}')

            //        while True:
            //            item = main.s_input('Input [#] (or type "exit"): ').lower()

            //            try:
            //                item = items.inventory['consumables'][int(item) - 1]

            //            except(IndexError, ValueError):
            //                if item in ['e', 'x', 'exit', 'b', 'back']:
            //                    print('-'*save_load.divider_size)
            //                    return False

            //                continue

            //            if isinstance(item, items.StatusPotion) :
            //                if item.status != user.status_ail:
            //                    print('-'*save_load.divider_size)
            //                    print(f'{user.name} is not {item.status}, they have no reason to drink that.')
            //                    main.s_input("\nPress enter/return ")
            //                    print('-'*save_load.divider_size)
            //                    break

            //            print('-' * save_load.divider_size)
            //            item.use_item(user)
            //            return True
        }

        public static void DisplayTeamStats(List<Unit> unit_list)
        {
            int player_pad1 = unit_list.Select(x => x.Name.Length).Max();
            int player_pad2 = unit_list.Select(x => $"{x.HP}/{x.MaxHP} HP".Length).Max();
            int player_pad3 = unit_list.Select(x => $"{x.MP}/{x.MaxMP} MP".Length).Max();

            foreach (Unit unit in unit_list)
            {
                string pad1 = new string(' ', (player_pad1 - unit.Name.Length));
                string pad2 = new string(' ', (player_pad2 - $"{unit.HP}/{unit.MaxHP} HP".Length));
                string pad3 = new string(' ', (player_pad3 - $"{unit.MP}/{unit.MaxMP} MP".Length));

                string status_list = "";
                foreach (CEnums.Status status in unit.Statuses)
                {
                    if (status_list == "")
                    {
                        status_list = CEnums.EnumToString(status);
                    }

                    else
                    {
                        status_list = string.Join(", ", new List<string>() { status_list, CEnums.EnumToString(status) });
                    }
                }

                Console.WriteLine($"  {unit.Name}{pad1} | {unit.HP}/{unit.MaxHP} HP {pad2}| {unit.MP}/{unit.MaxMP} MP {pad3}| LVL: {unit.Level} | STATUS: {status_list}");
            }
        }

        public static void DisplayBattleStats(List<PlayableCharacter> active_pcus, List<Monster> monster_list)
        {
            foreach (PlayableCharacter unit in active_pcus)
            {
                unit.FixAllStats();
            }

            foreach(Monster unit in monster_list)
            {
                unit.FixAllStats();
            }

            CMethods.PrintDivider();

            Console.WriteLine("Your party: ");
            DisplayTeamStats(active_pcus.Select(x => (Unit)x).ToList());

            Console.WriteLine("Enemy team: ");
            DisplayTeamStats(monster_list.Select(x => (Unit)x).ToList());

            CMethods.PrintDivider();
        }
    }
}
