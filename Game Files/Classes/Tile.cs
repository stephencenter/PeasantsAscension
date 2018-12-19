using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classes
{
    public class Tile
    {
        protected string Name { get; set; }
        protected string Description { get; set; }
        protected DirectionInfo ToNorth { get; set; }
        protected DirectionInfo ToSouth { get; set; }
        protected DirectionInfo ToWest { get; set; }
        protected DirectionInfo ToEast { get; set; }

        public Tile(string name, string desc, DirectionInfo to_north, DirectionInfo to_south, DirectionInfo to_east, DirectionInfo to_west)
        {
            Name = Name;
            string Description = desc;
            DirectionInfo ToNorth = to_north;
            DirectionInfo ToSouth = to_south;
            DirectionInfo ToWest = to_west;
            DirectionInfo ToEast = to_east;
        }
    }

    public class DirectionInfo
    {
        public bool accessible { get; set; }
        public string explanation { get; set; }
    } 

    public class 
}
