namespace Scripts
{
    public class TileManager
    {
        protected string Name { get; set; }
        protected string Description { get; set; }
        protected DirectionInfo ToNorth { get; set; }
        protected DirectionInfo ToSouth { get; set; }
        protected DirectionInfo ToWest { get; set; }
        protected DirectionInfo ToEast { get; set; }
    }

    public class DirectionInfo
    {
        public bool Accessible { get; set; }
        public string Explanation { get; set; }
    }
}
