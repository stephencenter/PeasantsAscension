using System;
using System.Collections.Generic;
using System.Linq;
using System.Media;

namespace Scripts
{
    public static class TileManager
    {
        #region
        // Tile descriptions
        private const string nearton_desc = @"\
Nearton is surrounded by a large, natural moat. Past that, trees as far as the
eyes can see.";
        #endregion

        /* =========================== *
         *            LISTS            *
         * =========================== */
        private static readonly List<Tile> tile_list = new List<Tile>()
        {
            new Tile("Town of Nearton", "nearton_tile", nearton_desc + @"\n
The town of Nearton is mere minutes away from this point!Stopping by
there might be a smart idea.",
                town_list: new List<string>() { },
                north: "nearton_n",
                south: "nearton_s",
                east: "nearton_e",
                west: "nearton_w"),

            new Tile("Nearton Outskirts", "nearton_sw", nearton_desc,
                north: "nearton_w",                
                east: "nearton_s"),

            new Tile("Nearton Outskirts", "nearton_s", nearton_desc,
                north: "nearton_tile",
                east: "nearton_se",
                west: "nearton_sw"),

            new Tile("Nearton Outskirts", "nearton_se", nearton_desc,
                north: "nearton_e",
                west: "nearton_s"),

            new Tile("Nearton Outskirts", "nearton_w", nearton_desc,
                north: "nearton_nw",
                south: "nearton_sw",
                east: "nearton_tile"),

            new Tile("Nearton Outskirts", "nearton_e", nearton_desc,
                north: "nearton_ne",
                south: "nearton_se",
                west: "nearton_tile"),

            new Tile("Nearton Outskirts", "nearton_nw", nearton_desc,
                south: "nearton_w",
                east: "nearton_n"),

            new Tile("Nearton Outskirts", "nearton_n", nearton_desc,
                south: "nearton_tile",
                east: "nearton_ne",
                west: "nearton_nw"),

            new Tile("Nearton Outskirts", "nearton_ne", nearton_desc,
                south: "nearton_e",
                west: "nearton_n"),
        };

        private static readonly List<Cell> cell_list = new List<Cell>()
        {
            new NeartonCell()
        };

        private static readonly List<Province> province_list = new List<Province>()
        {
            new Province("Overshire", new List<string>() { "nearton_cell" }, "overshire_prov")
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
                    throw new InvalidOperationException($"Tile with id {tile_id} either doesn't exist or is duplicated");
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
                string cell_id = GetCellList().Single(x => x.TileList.Contains(tile_id)).CellID;
                return GetProvinceList().Single(x => x.CellList.Contains(cell_id));
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

        public static bool VerifyTileExists(string tile_id)
        {
            return GetTileList().Select(x => x.TileID   ).Contains(tile_id);
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
        public List<string> TownList { get; set; }

        public string GenerateAsciiArt()
        {
            int num_adj_tiles = 0;

            foreach (string str in new List<string>() { ToWest, ToSouth, ToNorth, ToEast })
            {
                if (str != null)
                {
                    num_adj_tiles++;
                }
            }

            // Calculate which tile ascii art to display
            if (num_adj_tiles == 1)
            {
                if (ToNorth != null)
                {
                    return @"
                | N |
                |   |
                | X |
                |___| X = Player Party";
                }

                else if (ToSouth != null)
                {
                    return @" 
                 ___
                |   |
                | X |
                |   |
                | S | X = Player Party";
                }

                else if (ToWest != null)
                {
                    return @"
            ________
            W     X |
            ________| X = Player Party";
                }

                else if (ToEast != null)
                {
                    return @"
                 ________
                | X     E
                |________ X = Player Party";
                }

                else
                {
                    throw new Exception($"Failed to generate ascii art for tile {TileID}");
                }
            }

            else if (num_adj_tiles == 2)
            {
                if ((ToNorth != null) && (ToWest != null))
                {
                    return @"
                | N |
            ____|   |
            W     X |
            ________| X = Player Party";
                }

                else if ((ToNorth != null) && (ToEast != null))
                {
                    return @"
                | N |
                |   |____
                | X    E
                |________ X = Player Party";
                }

                else if ((ToNorth != null) && (ToSouth != null))
                {
                    return @"
                | N |
                |   |
                | X |
                |   |
                | S | X = Player Party";
                }

                else if ((ToWest != null) && (ToEast != null))
                {
                    return @"
            _____________
            W     X     E
            _____________ X = Player Party";
                }

                else if ((ToWest != null) && (ToSouth != null))
                {
                    return @"
            ________
            W     X |
            ____    |
                |   |
                | S | X = Player Party";
                }

                else if ((ToEast != null) && (ToSouth != null))
                {
                    return @"
                 ________
                | X     E
                |    ____
                |   |
                | S | X = Player Party";
                }

                else
                {
                    throw new Exception($"Failed to generate ascii art for tile {TileID}");
                }
            }

            else if (num_adj_tiles == 3)
            {
                if ((ToNorth != null) && (ToWest != null) && (ToEast != null))
                {
                    return @"
                | N |
            ____|   |____
            W     X     E
            _____________ X = Player Party";
                }


                else if ((ToNorth != null) && (ToWest != null) &&  (ToSouth != null))
                {
                    return @"
                | N |
            ____|   |
            W     X |
            ____    |
                |   |
                | S | X = Player Party";
                }

                else if ((ToNorth != null) && (ToEast != null) && (ToSouth != null))
                {
                    return @"
                | N |
                |   |____
                | X     E
                |    ____
                |   |
                | S | X = Player Party";
                }

                else if ((ToSouth != null) && (ToEast != null) && (ToSouth != null))
                {
                    return @"
            _____________
            W     X     E
            ____     ____
                |   |
                | S | X = Player Party";
                }

                else
                {
                    throw new Exception($"Failed to generate ascii art for tile {TileID}");
                }
            }

            else if (num_adj_tiles == 4)
            {
                return @"
                | N |
            ____|   |____
            W     X     E
            ____     ____
                |   |
                | S | X = Player Party";
            }

            else 
            {
                throw new Exception($"Failed to generate ascii art for tile {TileID}");
            }
        }

        public Tile(string name, string tile_id, string desc, List<string> town_list = null, string north = null, string south = null, string west = null, string east = null)
        {
            Name = name;
            Description = desc;
            ToNorth = north;
            ToSouth = south;
            ToWest = west;
            ToEast = east;
            TownList = town_list ?? new List<string>();
            TileID = tile_id;
        }
    }

    public abstract class Cell
    {
        // Cells are containers for tiles
        // They store information related to monster spawning, music, and store item quality
        // which are all cell-specific and not tile-specific
        // The Cell class is abstract. Using a constructor to create a Cell would get
        // messy so all the information is preloaded into custom Cell subclasses
        public string CellName { get; set; }
        public List<string> TileList { get; set; }
        public string PrimaryTile { get; set; }
        public List<CEnums.MonsterGroup> MonsterGroups { get; set; }
        public SoundPlayer Music { get; set; }
        public int MinMonsterLevel { get; set; }
        public int MaxMonsterLevel { get; set; }
        public int StoreLevel { get; set; }
        public string CellID { get; set; }

        protected Cell()
        {

        }
    }

    public class Province
    {
        public string ProvinceName { get; set; }
        public List<string> CellList { get; set; }
        public string ProvID { get; set; }

        public Province(string name, List<string> cells, string prov_id)
        {
            ProvinceName = name;
            CellList = cells;
            ProvID = prov_id;
        }
    }

    // Custom Cells
    internal class NeartonCell : Cell
    {
        public NeartonCell() : base() 
        {
            CellName = "Nearton"; 
            TileList = new List<string>() { "nearton_tile", "nearton_w", "nearton_ne", "nearton_e", "nearton_s", "nearton_n", "nearton_se", "nearton_nw", "nearton_sw" };
            PrimaryTile = "nearton_tile";
            MonsterGroups = new List<CEnums.MonsterGroup>() { CEnums.MonsterGroup.animal, CEnums.MonsterGroup.monster };
            Music = SoundManager.forest_music;
            MinMonsterLevel = 1;
            MaxMonsterLevel = 2 ;
            StoreLevel = 1;
            CellID = "nearton_cell";
        }
    }
}
