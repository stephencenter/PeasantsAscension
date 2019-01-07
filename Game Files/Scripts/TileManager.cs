using System;
using System.Collections.Generic;

namespace Scripts
{
    public static class TileManager
    {

    }

    public class Tile
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public Tile ToNorth { get; set; }
        public Tile ToSouth { get; set; }
        public Tile ToWest { get; set; }
        public Tile ToEast { get; set; }
    }

    public class Cell
    {
        public string CellName { get; set; }
        public string Music { get; set; }
        public List<List<Unit>> EnemyGroups { get; set; }
        public int MinMonsterLevel { get; set; }
        public int MaxMonsterLevel { get; set; }
        public int StoreLevel { get; set; }
        public string CellID { get; set; }

        public Cell(string name, string music, List<List<Unit>> enemy_groups, int min_lvl, int max_lvl, int store_level, string cell_id)
        {
            CellName = name;
            Music = music;
            EnemyGroups = enemy_groups;
            MinMonsterLevel = min_lvl;
            MaxMonsterLevel = max_lvl;
            StoreLevel = store_level;
            CellID = cell_id;
        }
    }

    public class Province
    {
        public string ProvinceName { get; set; }
        public List<Cell> CellList { get; set; }
        public string ProvID { get; set; }

        public Province(string name, List<Cell> cells, string prov_id)
        {
            ProvinceName = name;
            CellList = cells;
            ProvID = prov_id;
        }
    }
}
