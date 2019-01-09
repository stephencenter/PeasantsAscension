using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    public static class TileManager
    {
        private static readonly List<Tile> tile_list  = new List<Tile>()
        {

        };

        private static readonly List<Cell> cell_list = new List<Cell>()
        {

        };

        private static readonly List<Province> province_list = new List<Province>()
        {

        };

        public static List<Tile> GetTileList()
        {
            return tile_list;
        }

        public static List<Cell> GetCellList()
        {
            return cell_list;
        }

        public static List<Province> GetProvinceList()
        {
            return province_list;
        }

        public static Tile FindTileWithID(string tile_id)
        {
            return GetTileList().Single(x => x.TileID == tile_id);
        }

        public static Cell FindCellWithID(string cell_id)
        {
            return GetCellList().Single(x => x.CellID == cell_id);
        }

        public static Province FindProvinceWithID(string prov_id)
        {
            return GetProvinceList().Single(x => x.ProvID == prov_id);
        }

        public static Cell FindCellWithTileID(string tile_id)
        {
            return GetCellList().Single(x => x.TileList.Contains(FindTileWithID(tile_id)));
        }

        public static Province FindProvinceWithTileID(string tile_id)
        {
            return GetProvinceList().Single(x => x.CellList.Contains(FindCellWithTileID(tile_id)));
        }
    }

    public class Tile
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public Tile ToNorth { get; set; }
        public Tile ToSouth { get; set; }
        public Tile ToWest { get; set; }
        public Tile ToEast { get; set; }
        public string TileID { get; set; }
    }

    public class Cell
    {
        public string CellName { get; set; }
        public List<Tile> TileList { get; set; }
        public List<List<Unit>> EnemyGroups { get; set; }
        public string Music { get; set; }
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
