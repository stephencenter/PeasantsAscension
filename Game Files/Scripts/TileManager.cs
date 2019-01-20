using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    public static class TileManager
    {
        /* =========================== *
         *            LISTS            *
         * =========================== */
        private static readonly List<Tile> tile_list = new List<Tile>()
        {

        };

        private static readonly List<Cell> cell_list = new List<Cell>()
        {

        };

        private static readonly List<Province> province_list = new List<Province>()
        {

        };

        /* =========================== *
         *           METHODS           *
         * =========================== */
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
            // Takes in a TileID, returns the tile that matches the ID
            try
            {
                return GetTileList().Single(x => x.TileID == tile_id);
            }

            catch (Exception ex)
            {
                // InvalidOperationException means that .Single() found either 0 provinces matching prov_id, or more than 1
                if (ex is InvalidOperationException)
                {
                    throw new Exception($"Tile with id {tile_id} either doesn't exist or is duplicated");
                }

                throw ex;
            }
        }

        public static Cell FindCellWithID(string cell_id)
        {
            // Takes in a CellID, returns the cell that matches the ID
            try
            {
                return GetCellList().Single(x => x.CellID == cell_id);
            }

            catch (Exception ex)
            {
                // InvalidOperationException means that .Single() found either 0 cells matching cell_id, or more than 1
                if (ex is InvalidOperationException)
                {
                    throw new Exception($"Tile with id {cell_id} either doesn't exist or is duplicated");
                }

                throw ex;
            }
        }

        public static Province FindProvinceWithID(string prov_id)
        {
            // Takes in a ProvID, returns the province that matches the ID
            try
            {
                return GetProvinceList().Single(x => x.ProvID == prov_id);
            }

            catch (Exception ex)
            {

                // InvalidOperationException means that .Single() found either 0 provinces matching prov_id, or more than 1
                if (ex is InvalidOperationException)
                {
                    throw new Exception($"Province with id {prov_id} either doesn't exist or is duplicated");
                }

                throw ex;
            }
        }

        public static Cell FindCellWithTileID(string tile_id)
        {
            // Takes in a TileID, returns the cell that matches the ID
            try
            {
                return GetCellList().Single(x => x.TileList.Contains(tile_id));
            }

            catch (Exception ex)
            {
                // InvalidOperationException means that .Single() found either 0 cells matching tile_id, or more than 1
                if (ex is InvalidOperationException)
                {
                    throw new Exception($"Cell containing tile with id {tile_id} either doesn't exist or is duplicated");
                }

                throw ex;
            }
        }

        public static Province FindProvinceWithTileID(string tile_id)
        {
            // Takes in a TileID, returns the province that matches the ID
            try
            {
                return GetProvinceList().Single(x => x.CellList.Contains(tile_id));
            }

            catch (Exception ex)
            {
                // InvalidOperationException means that .Single() found either 0 provinces matching tile_id, or more than 1
                if (ex is InvalidOperationException)
                {
                    throw new Exception($"Province containing tile with id {tile_id} either doesn't exist or is duplicated");
                }

                throw ex;
            }
        }
    }

    public class Tile
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public string ToNorth { get; set; }
        public string ToSouth { get; set; }
        public string ToWest { get; set; }
        public string ToEast { get; set; }
        public string TileID { get; set; }

        public Tile(string name, string desc, string north, string south, string west, string east, string tile_id)
        {
            Name = name;
            Description = desc;
            ToNorth = north;
            ToSouth = south;
            ToWest = west;
            ToEast = east;
            TileID = tile_id;
        }
    }

    public class Cell
    {
        // Cells are containers for tiles
        // They store information related to monster spawning, music, and store item quality
        // which are all cell-specific and not tile-specific
        public string CellName { get; set; }
        public List<string> TileList { get; set; }
        public string PrimaryTile { get; set; }
        public List<CEnums.MonsterGroup> MonsterGroups { get; set; }
        public string Music { get; set; }
        public int MinMonsterLevel { get; set; }
        public int MaxMonsterLevel { get; set; }
        public int StoreLevel { get; set; }
        public string CellID { get; set; }

        public void VerifyAllTilesExist()
        {
            // This method verifies that all of the TileIDs in the TileList correspond to real tiles
            // This will throw an error if any fake TileIDs are found
            TileList.ForEach(x => TileManager.FindTileWithID(x));
            TileManager.FindTileWithID(PrimaryTile);
        }

        public Cell(string name, List<string> tile_list, string music, List<CEnums.MonsterGroup> m_groups, int min_lvl, int max_lvl, int store_level, string cell_id)
        {
            CellName = name;
            TileList = tile_list;
            Music = music;
            MonsterGroups = m_groups;
            MinMonsterLevel = min_lvl;
            MaxMonsterLevel = max_lvl;
            StoreLevel = store_level;
            CellID = cell_id;

            VerifyAllTilesExist();
        }
    }

    public class Province
    {
        public string ProvinceName { get; set; }
        public List<string> CellList { get; set; }
        public string ProvID { get; set; }

        public void VerifyAllCellsExist()
        {
            // This method verifies that all of the CellIDs in the CellList correspond to real cells
            // This will throw an error if any fake CellIDs are found
            CellList.ForEach(x => TileManager.FindCellWithID(x));
        }

        public Province(string name, List<string> cells, string prov_id)
        {
            ProvinceName = name;
            CellList = cells;
            ProvID = prov_id;

            VerifyAllCellsExist();
        }
    }
}
