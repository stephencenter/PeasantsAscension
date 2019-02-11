using System.Collections.Generic;
using System.Linq;
using System;

namespace Data
{
    public static class TownManager
    {
        private static readonly List<Town> town_list = new List<Town>()
        {

        };

        public static List<Town> GetTownList()
        {
            return town_list;
        }

        public static Town FindTownWithID(string town_id)
        {
            return GetTownList().Single(x => x.TownID == town_id);
        }

        public static bool SearchForTowns(bool enter = true)
        {
            if (TileManager.FindTileWithID(CInfo.CurrentTile).TownList.Count == 0)
            {
                return false;
            }

            foreach (string town_id in TileManager.FindTileWithID(CInfo.CurrentTile).TownList)
            {
                Town town = FindTownWithID(town_id);
                CMethods.PrintDivider();

                while (true)
                {
                    string yes_no = CMethods.Input($"The town of {town.TownName} is nearby. Enter? Yes or No: ");

                    if (CMethods.IsYesString(yes_no))
                    {
                        CInfo.RespawnTile = CInfo.CurrentTile;
                        town.EnterTown();
                        return true;
                    }

                    else if (CMethods.IsNoString(yes_no))
                    {
                        CMethods.PrintDivider();
                        break;
                    }
                }
            }

            return true;
        }
    }

    public class Town
    {
        public string TownName { get; set; }
        public string TownID { get; set; }

        public void EnterTown()
        {

        }
    }
}
