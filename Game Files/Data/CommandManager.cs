using System;
using System.Collections.Generic;
using System.Linq;

namespace Data
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
                            string yes_no = CMethods.SingleCharInput("Fight it?");

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
            SoundManager.sneaking_music.PlayLooping();

            CMethods.PrintDivider();
            Console.WriteLine("Welcome to the top-secret cheat menu!");
            while (true)
            {
                Console.WriteLine("Type 'help' to view a list of cheats");
                Console.WriteLine("Type 'exit' exit the cheat menu\n");

                while (true)
                {
                    string command = CMethods.MultiCharInput("Enter a cheat: ").ToLower();
                    List<string> keywords = command.Split().ToList();

                    if (CMethods.IsExitString(command))
                    {
                        CMethods.PrintDivider();
                        SoundManager.PlayCellMusic();
                        return;
                    }

                    else if (command.StartsWith("h"))
                    {
                        CMethods.PrintDivider();
                        CheatEngine.Help();
                        CMethods.PrintDivider();
                    }

                    // Inventory add cheat
                    else if (keywords.Count == 4 && keywords[0] == "inventory" && keywords[1] == "add")
                    {
                        CheatEngine.Flag flag = CheatEngine.InventoryAddCheat(keywords[2], keywords[3]);

                        if (flag == CheatEngine.Flag.InvalidItemID)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'item id => {keywords[2]}' is invalid for 'inventory add [item id] [quantity]'");
                        }

                        if (flag == CheatEngine.Flag.InvalidItemQuantity)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'quantity => {keywords[3]}' is invalid for 'inventory add [item_id] [quantity]'");
                        }
                    }

                    // Spawns toggle cheat
                    else if (keywords.Count == 3 && keywords[0] == "spawns" && keywords[1] == "toggle")
                    {
                        CheatEngine.Flag flag = CheatEngine.SpawnToggleCheat(keywords[2]);

                        if (flag == CheatEngine.Flag.InvalidSpawnSetting)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'true or false => {keywords[2]}' if invalid for 'spawns toggle [true or false]'");
                        }
                    }

                    // Gold add cheat
                    else if (keywords.Count == 3 && keywords[0] == "gold" && keywords[1] == "add")
                    {
                        CheatEngine.Flag flag = CheatEngine.GoldAddCheat(keywords[2]);

                        if (flag == CheatEngine.Flag.InvalidGoldQuantity)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'quantity => {keywords[2]}' is invalid for 'gold add [quantity]'");
                        }
                    }

                    // Teleport cheat
                    else if (keywords.Count == 2 && keywords[0] == "teleport")
                    {
                        CheatEngine.Flag flag = CheatEngine.TeleportCheat(keywords[1]);

                        if (flag == CheatEngine.Flag.InvalidTileID)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'tile id => {keywords[1]}' is invalid for 'teleport [tile id]'");
                        }
                    }

                    // Player xp add cheat
                    else if (keywords.Count == 4 && keywords[0] == "player" && keywords[2] == "xp")
                    {
                        CheatEngine.Flag flag = CheatEngine.PlayerXPAddCheat(keywords[1], keywords[3]);

                        if (flag == CheatEngine.Flag.InvalidUnitID)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'pcu id => {keywords[1]}' is invalid for 'player [pcu id] xp [quantity]'");
                        }

                        else if (flag == CheatEngine.Flag.InvalidXPQuantity)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'quantity => {keywords[3]}' is invalid for 'player [pcu id] xp [quantity]'");
                        }
                    }

                    // Player heal cheat
                    else if (keywords.Count == 3 && keywords[0] == "player" && keywords[2] == "heal")
                    {
                        CheatEngine.Flag flag = CheatEngine.PlayerHealCheat(keywords[1]);

                        if (flag == CheatEngine.Flag.InvalidUnitID)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'pcu id => {keywords[1]}' is invalid for 'player [pcu id] heal'");
                        }
                    }

                    else if (keywords.Count == 3 && keywords[0] == "player" && keywords[2] == "kill")
                    {
                        CheatEngine.Flag flag = CheatEngine.PlayerKillCheat(keywords[1]);

                        if (flag == CheatEngine.Flag.InvalidUnitID)
                        {
                            CMethods.PrintDivider();
                            Console.WriteLine($"'pcu id => {keywords[1]}' is invalid for 'player [pcu id] kill'");
                        }
                    }

                    else if (keywords.Count == 2 && keywords[0] == "battle" && keywords[1] == "fight")
                    {
                        CMethods.PrintDivider();
                        CheatEngine.BattleFightCheat();
                        SoundManager.sneaking_music.PlayLooping();
                        break;
                    }

                    /*
                    file
                        save
                        load */

                    else
                    {
                        CMethods.PrintDivider();
                        Console.WriteLine($"Invalid command '{command}'");
                    }

                    break;
                }
            }
        }
    }

    public static class CheatEngine
    {
        public enum Flag
        {
            Success,
            InvalidItemID,
            InvalidItemQuantity,
            InvalidSpawnSetting,
            InvalidGoldQuantity,
            InvalidTileID,
            InvalidUnitID,
            InvalidXPQuantity
        }

        public static Flag InventoryAddCheat(string item_id, string quantity)
        {
            if (!ItemManager.GetItemList().Select(x => x.ItemID).Contains(item_id))
            {
                return Flag.InvalidItemID;
            }

            if (!int.TryParse(quantity, out int true_quantity) || true_quantity < 1)
            {
                return Flag.InvalidItemQuantity;
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
            if (!bool.TryParse(new_setting, out bool true_setting))
            {
                return Flag.InvalidSpawnSetting;
            }

            CInfo.DoSpawns = true_setting;
            CMethods.PrintDivider();
            Console.WriteLine($"Monster spawns are now {(true_setting ? "enabled" : "disabled")}");

            return Flag.Success;
        }

        public static Flag GoldAddCheat(string quantity)
        {
            if (!int.TryParse(quantity, out int true_quantity) || true_quantity < 1)
            {
                return Flag.InvalidGoldQuantity;
            }

            CInfo.GP += true_quantity;
            CMethods.PrintDivider();
            Console.WriteLine($"Gave player {true_quantity} gold");

            return Flag.Success;
        }

        public static Flag TeleportCheat(string tile_id)
        {
            if (!TileManager.GetTileList().Select(x => x.TileID).Contains(tile_id))
            {
                return Flag.InvalidTileID;
            }

            CInfo.CurrentTile = tile_id;
            CMethods.PrintDivider();
            Console.WriteLine($"Teleported party to {tile_id}");

            return Flag.Success;
        }

        public static Flag PlayerXPAddCheat(string pcu_id, string quantity)
        {
            if (!UnitManager.GetAllPCUs().Select(x => x.UnitID).Contains(pcu_id))
            {
                return Flag.InvalidUnitID;
            }

            if (!int.TryParse(quantity, out int true_quantity) || true_quantity < 1)
            {
                return Flag.InvalidXPQuantity;
            }

            UnitManager.GetAllPCUs().Single(x => x.UnitID == pcu_id).CurrentXP += true_quantity;
            CMethods.PrintDivider();
            Console.WriteLine($"Gave {pcu_id} {true_quantity} XP");

            return Flag.Success;
        }

        public static Flag PlayerHealCheat(string pcu_id)
        {
            if (!UnitManager.GetAllPCUs().Select(x => x.UnitID).Contains(pcu_id))
            {
                return Flag.InvalidUnitID;
            }

            UnitManager.HealOnePCU(pcu_id, true, true, true);
            CMethods.PrintDivider();
            Console.WriteLine($"Restored all HP, MP, and AP for {pcu_id}");

            return Flag.Success;
        }

        public static Flag PlayerKillCheat(string pcu_id)
        {
            if (!UnitManager.GetAllPCUs().Select(x => x.UnitID).Contains(pcu_id))
            {
                return Flag.InvalidUnitID;
            }

            PlayableCharacter pcu = UnitManager.GetAllPCUs().Single(x => x.UnitID == pcu_id);
            pcu.Statuses = new List<CEnums.Status>() { CEnums.Status.dead };
            pcu.HP = 0;
            CMethods.PrintDivider();
            Console.WriteLine($"Set {pcu_id}'s HP to zero and flagged as dead");

            return Flag.Success;
        }

        public static void BattleFightCheat()
        {
            BattleManager.BattleSystem(false);
        }

        public static void Help()
        {
            Console.WriteLine(@"Available cheats:
 'inventory add [item id] [quantity]' => Adds quantity of item id to inventory
 'spawns toggle [true or false]' => Enables or disable monster spawns
 'gold add [quantity]' => Gives the player quantity GP
 'teleport [tile id] => Teleports the player to the tile with tile id
 'player [pcu id] xp [quantity]' => Gives the PCU quantity XP
 'player [pcu id] heal' => Fully heals the PCU
 'player [pcu id] kill' => Kills the PCU
 'battle fight' => Initiates a random encounter on the current tile
 'file save' => Saves the game
 'file load' => Loads the most recent save file");
            CMethods.PressAnyKeyToContinue();
        }
    }
}
