using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    public static class CommandManager
    {
        public static void MoveCommand(List<Tuple<char, string>> available_dirs, char direction)
        {
            Random rng = new Random();
            SoundManager.foot_steps.SmartPlay();

            CInfo.CurrentTile = available_dirs.Single(x => x.Item1 == direction).Item2;

            // If none of these fucntions return True, then a battle can occur.
            if (new List<bool>() { /* UnitManager.CheckForBosses(),*/ TownManager.SearchForTowns(enter: false) }.All(x => x == false))
            {
                // There is a 1 in 4 chance for a battle to occur (25%)
                // However, a battle cannot occur if the number of steps since the last battle is less than three,
                // and is guaranteed to occur if the number of steps is above 10.
                bool is_battle = rng.Next(0, 3) == 0;

                if (CInfo.StepsWithoutBattle > 10)
                {
                    is_battle = true;
                }

                else if (CInfo.StepsWithoutBattle < 3)
                {
                    is_battle = false;
                }

                // It is possible to disable spawns using cheats
                if (is_battle && CInfo.DoSpawns)
                {
                    CMethods.PrintDivider();
                    CInfo.StepsWithoutBattle = 0;
                    int highest_perception = UnitManager.GetAllPCUs().Select(x => x.Attributes["per"]).Max();

                    if (highest_perception > rng.Next(0, 100))
                    {
                        Console.WriteLine($"You see a monster - it has not detected you yet.");

                        while (true)
                        {
                            string yes_no = CMethods.Input("Fight it?");

                            if (CMethods.IsYesString(yes_no)) 
                            {
                                CMethods.PrintDivider();
                                BattleManager.BattleSystem(false);
                            }

                            else if (CMethods.IsNoString(yes_no))
                            {
                                break;
                            }
                        }
                    }

                    else
                    {
                        BattleManager.BattleSystem(false);
                    }
                }

                else
                {
                    CInfo.StepsWithoutBattle++;
                }
            }            
        }

        public static void CheatCommand()
        {
            CMethods.PrintDivider();
            Console.WriteLine("Welcome to the top-secret cheat menu!");
            Console.WriteLine("Type 'help' to view a list of cheats");
            Console.WriteLine("Type 'exit' exit the cheat menu\n");

            while (true)
            {
                string command = CMethods.Input("Enter a cheat: ").ToLower();
                List<string> keywords = command.Split().ToList();
                
                if (keywords.Count == 4 && keywords[0] == "inventory")
                {
                    if (keywords[1] == "add")
                    {
                        CheatEngine.Flag flag = CheatEngine.InventoryAddCheat(keywords[2], keywords[3]);

                        if (flag == CheatEngine.Flag.InvalidItemID)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine("Invalid 'item id' for 'inventory add [item id] [quantity]'");
                        }

                        if (flag == CheatEngine.Flag.InvalidItemQuantity)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine("Invalid 'quantity' for 'inventory add [item_id] [quantity]'");
                        }
                    }
                }

                else if (keywords.Count == 2 && keywords[0] == "spawns")
                {
                    CheatEngine.Flag flag = CheatEngine.SpawnToggleCheat(keywords[1]);

                    if (flag == CheatEngine.Flag.InvalidSpawnSetting)
                    {
                        CMethods.PrintDivider();
                        Console.WriteLine("Invalid 'true or false' for 'spawns [true or false]'");
                    }
                }

                else
                {
                    CMethods.PrintDivider();
                    Console.WriteLine($"Invalid command '{command}'");
                }
                    /*
                inventory
                    add
                        [item_id]
                            [quantity]
                    remove
                        [item_id]
                            [quantity]
            
                spawns
                    true
                    false
    
                gold
                    add 
                        [quantity]
                    remove
                        [quantity]
    
                teleport
                    [tile_id]
    
                player
                    [pcu_id]
                        active
                            [bool]
                        xp
                            [quantity]
                        heal
                        kill

                battle
                    fight
    
                file
                    save
                    load */
            }
        }
    }

    public static class CheatEngine
    {
        public enum Flag { Success, InvalidItemID, InvalidItemQuantity, InvalidSpawnSetting }

        public static Flag InventoryAddCheat(string item_id, string quantity)
        {
            int true_quantity;

            try
            {
                ItemManager.FindItemWithID(item_id);
            }

            catch (Exception ex)
            {
                if (ex is InvalidOperationException)
                {
                    return Flag.InvalidItemID;
                }

                throw ex;
            }

            try
            {
                true_quantity = int.Parse(quantity);

                if (true_quantity < 1)
                {
                    throw new FormatException();
                }
            }

            catch (Exception ex)
            {
                if (ex is FormatException)
                {
                    return Flag.InvalidItemQuantity;
                }

                throw ex;
            }


            for (int i = 0; i < true_quantity;  i++)
            {
                InventoryManager.AddItemToInventory(item_id);
            }

            CMethods.PrintDivider();
            Console.WriteLine($"Added {item_id} x{quantity} to inventory");

            return Flag.Success;
        }

        public static Flag SpawnToggleCheat(string new_setting)
        {
            bool bool_setting;

            try
            {
                bool_setting = bool.Parse(new_setting);
            }

            catch (Exception ex)
            {
                if (ex is FormatException)
                {
                    return Flag.InvalidSpawnSetting;
                }

                throw ex;
            }

            CMethods.PrintDivider();
            CInfo.DoSpawns = bool_setting;
            Console.WriteLine($"Monster spawns are now {(bool_setting ? "enabled" : "disabled")}");

            return Flag.Success;
        }
    }
}
