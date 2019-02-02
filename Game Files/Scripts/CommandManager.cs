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
            while (true)
            {
                string command = CMethods.Input()
            }
        }
    }

    public static class CheatEngine
    {

    }
}
