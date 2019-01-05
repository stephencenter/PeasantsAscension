using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public class BattleManager
    {
        readonly Random rng = new Random();
        readonly CEnums c_enums = new CEnums();
        readonly CommonMethods c_methods = new CommonMethods();
        readonly SoundManager sound_manager = new SoundManager();
        protected UnitManager unit_manager = new UnitManager();

        public void BattleSystem()
        {
            List<Unit> monster_list = new List<Unit>() { unit_manager.GenerateMonster() };
            List<Unit> active_pcus = unit_manager.GetActivePCUs();
            int turn_counter = 0;

            // 25% chance to add a second monster
            if (rng.Next(0, 100) > 75)
            {
                monster_list.Add(unit_manager.GenerateMonster());

                // 25% chance to add a third monster if a second monster was already added (6.25% chance for three monsters)
                if (rng.Next(0, 100) > 75)
                {
                    monster_list.Add(unit_manager.GenerateMonster());
                }
            }

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

            Thread.Sleep(1);

            // Create a temporary copy of all of the player's stats. These copies are what will be modified in-battle by 
            // spells, abilities, etc. so that they will return to normal after battle (although they in fact were never 
            // touched to begin with)
            active_pcus.ForEach(x => x.SetTempStats());

            // While all active party members are alive, continue the battle
            while (monster_list.Any(x => x.HP > 0) && active_pcus.Any(x => x.HP > 0))
            {
                turn_counter++;

                List<Unit> speed_list = active_pcus.Concat(monster_list).OrderByDescending(x => x.Speed).ToList();

                // Display the stats for every battle participant
                DisplayBattleStats(active_pcus, monster_list);

                // Iterate through each active players
                int counter = 0;
                foreach (Unit character in active_pcus)
                {
                    if (0 < character.HP && character.HP <= character.MaxHP * 0.20)
                    {
                        Console.WriteLine($"Warning: {character.Name}'s HP is low, heal as soon as possible!");
                        sound_manager.health_low.Play();
                        Thread.Sleep(1000);
                    }

                    if (character.IsAlive())
                    {
                        character.PlayerChoice(monster_list);

                        if (counter + 1 < active_pcus.Where(x => x.IsAlive()).Count())
                        {
                            c_methods.PrintDivider();
                        }
                    }
                }

                // Iterate through each unit in the battle from fastest to slowest
                foreach (Unit unit in speed_list)
                {
                    if (unit.IsAlive())
                    {
                        if (monster_list.Any(x => x.HP <= 0))
                        {
                            break;
                        }

                        c_methods.PrintDivider();

                        // Leave the battle if the player runs away
                        if ((unit.IsPCU() && unit.PCUExecuteMove(monster_list) == "ran") || (unit.IsMonster() && unit.MonsterExecuteMove() == "ran"))
                        {
                            return;
                        }

                        if (active_pcus.Any(x => x.HP > 0))
                        {
                            if (monster_list.Any(x => x.HP > 0) && unit.IsAlive())
                            {
                                c_methods.PressEnterReturn();
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
                    foreach (Unit other_unit in speed_list)
                    {
                        if (other_unit.IsPCU() && other_unit.HP <= 0 && other_unit.IsAlive())
                        {
                            other_unit.HP = 0;
                            other_unit.Statuses = new List<CEnums.Status> { CEnums.Status.dead };
                            sound_manager.ally_death.Play();

                            c_methods.PrintDivider();
                            Console.WriteLine($"{other_unit.Name} has fallen to the monsters!");
                            c_methods.PressEnterReturn();
                        }

                        else if (other_unit.IsMonster() && other_unit.HP <= 0 && other_unit.IsAlive())
                        {
                            other_unit.HP = 0;
                            other_unit.Statuses = new List<CEnums.Status> { CEnums.Status.dead };
                            sound_manager.enemy_death.Play();

                            c_methods.PrintDivider();
                            Console.WriteLine($"{other_unit.Name} was defeated by your party!");
                            c_methods.PressEnterReturn();
                        }
                    }
                }
            }

            // Determine the results of the battle and react accordingly
            AfterBattle();
        }

        public void AfterBattle()
        {
            /* Python Code
            def after_battle(is_boss) :
                # Assess the results of the battle
                print('-'*save_load.divider_size)

                for unit in enabled_pcus + m_list:
                    if unit.hp <= 0 and 'dead' not in unit.status_ail:
                        unit.hp = 0
                        unit.status_ail = ['dead']

                while True:
                    # If the monster wins...
                    if any(['dead' not in m.status_ail for m in m_list]) and all(['dead' in x.status_ail for x in enabled_pcus]):
                        sounds.play_music('../Music/Power-Up.ogg')

                        print(f'Despite your best efforts, the {units.monster.name} has killed your party.')
                        print('-'*save_load.divider_size)

                        auto_yes = False
                        while True:
                            if auto_yes:
                                y_n = 'y'

                            else:
                                y_n = main.s_input('Do you wish to continue playing? | Y/N: ').lower()

                            if y_n.startswith('y'):
                                # If you die, you return to the last town visited or 0'N, 0'W if you haven't been to a town yet.

                                main.party_info['current_tile'] = main.party_info['prev_town']
                                units.heal_pcus(1)

                                sounds.play_music(main.party_info['music'])

                                return

                            elif y_n.startswith('n'):
                                while True:
                                    y_n = main.s_input('Are you sure you want to quit and lose unsaved progress? |  Y/N: ').lower()

                                    if y_n.startswith('n') or main.do_debug:
                                        auto_yes = True

                                        break

                                    elif y_n.startswith('y'):
                                        pygame.quit()
                                        sys.exit()

                    # If the player wins...
                    elif all(['dead' in m.status_ail for m in m_list]) and any(['dead' not in x.status_ail for x in enabled_pcus]):
                        sounds.play_music('../Music/Python_RM.ogg')

                        if is_boss:
                            print(f'The almighty {units.monster.name} has been slain!')
                            units.defeated_bosses.append(units.monster.boss_id)
                            units.monster.upon_defeating()

                        else:
                            print(f'The {units.monster.name} falls to the ground, dead as a stone.')

                        # Formulas for item, gold, and experience drops
                        gold_drops = math.ceil(sum([max(1, x.gold, 2.5 * x.lvl) for x in m_list]))
                        expr_drops = math.ceil(sum([max(1, y.experience, 1.5 * *y.lvl) / 2 for y in m_list]))
                        item_drops = []

                        for monster in m_list:
                            for item in monster.items:
                                item_drops.append((monster.name, item))

                        main.party_info['gp'] += gold_drops
                        main.s_input(f'Your party has gained {gold_drops} GP! ')

                        # Each party member gets their own XP
                        for character in enabled_pcus:
                            character.exp += expr_drops
                            main.s_input(f'{character.name} gained {expr_drops} XP! ')

                        # Each monster can drop their own item
                        for drop in item_drops:
                            main.s_input(f"The {drop[0]} dropped a {items.find_item_with_id(drop[1]).name}! ")
                            items.add_item(drop[1])

                        for character in enabled_pcus:
                            character.level_up()

                        sounds.play_music(main.party_info['music'])

                        return

                    else:
                        units.player.hp = 1
                        units.player.status_ail = ['alive']

                        continue */
        }

        public bool RunAway(Unit runner)
        {
            return true;
            //def run_away(runner):
            //    print(ascii_art.player_art[runner.class_.title()] % f"{runner.name} is making a move!\n")
            //    print(f'Your party starts to run away from the {units.monster.name}...')
            //    sounds.foot_steps.play()

            //    main.smart_sleep(0.75)

            //    if 'paralyzed' in runner.status_ail:
            //        # 20% chance of success
            //        chance = 20

            //    elif bool (runner.spd > sorted(m_list, key= lambda x: x.spd, reverse= True)[0].spd) != \
            //            bool (runner.evad > sorted(m_list, key= lambda x: x.evad, reverse= True)[0].spd):
            //        # 60% chance of success
            //        chance = 60

            //    elif runner.spd > sorted(m_list, key= lambda x: x.spd, reverse= True)[0].spd and \
            //            runner.evad > sorted(m_list, key= lambda x: x.evad, reverse= True)[0].spd:
            //        # 80% chance of success
            //        chance = 80

            //    else:
            //        # 40% chance of success
            //        chance = 40

            //    if random.randint(0, 100) <= chance:
            //        sounds.buff_spell.play()
            //        print(f'Your party manages to escape from the {units.monster.name}!')
            //        main.s_input("\nPress enter/return ")
            //        return True

            //    else:
            //        sounds.debuff.play()
            //        print("Your party's attempt to escape failed!")
            //        return False
        }

        public bool BattleInventory(Unit user)
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

        public void DisplayTeamStats(List<Unit> unit_list)
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
                        status_list = c_enums.EnumToString(status);
                    }

                    else
                    {
                        status_list = string.Join(", ", new List<string>() { status_list, c_enums.EnumToString(status) });
                    }
                }

                Console.WriteLine($"  {unit.Name}{pad1} | {unit.HP}/{unit.MaxHP} HP {pad2}| {unit.MP}/{unit.MaxMP} MP {pad3}| LVL: {unit.Level} | STATUS: {status_list}");
            }
        }

        public void DisplayBattleStats(List<Unit> active_pcus, List<Unit> monster_list)
        {
            foreach (Unit unit in active_pcus.Concat(monster_list))
            {
                unit.FixAllStats();
            }

            c_methods.PrintDivider();

            Console.WriteLine("Your party: ");
            DisplayTeamStats(active_pcus);

            Console.WriteLine("Enemy team: ");
            DisplayTeamStats(monster_list);

            c_methods.PrintDivider();
        }
    }
}
