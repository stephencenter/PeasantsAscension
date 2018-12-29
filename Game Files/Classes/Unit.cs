using System.Collections.Generic;
using System.Linq;
using Classes.Items;

namespace Classes
{
    public class Unit
    {
        // General Unit Properties
        public enum Element { fire = 1, water, electric, earth, wind, grass, ice, light, dark, none }
        public Dictionary<Element, List<Element>> ElementChart = new Dictionary<Element, List<Element>>
        {
            {Element.fire, new List<Element> {Element.water, Element.ice } },
            {Element.water, new List<Element> {Element.electric, Element.fire } },
            {Element.electric, new List<Element> {Element.earth, Element.water } },
            {Element.earth, new List<Element> {Element.wind, Element.electric } },
            {Element.wind, new List<Element> {Element.grass, Element.earth } },
            {Element.grass, new List<Element> {Element.ice, Element.wind } },
            {Element.ice, new List<Element> {Element.fire, Element.grass } },
            {Element.light, new List<Element> {Element.light, Element.dark } },
            {Element.dark, new List<Element> {Element.dark, Element.light } }
        };

        public enum Status { silence = 1, poison, weakness, blindness, paralyzation, alive, dead }
        public List<Status> Statuses = new List<Status> { Status.alive };

        public UnitType Type { get; set; }
        public string Name { get; set; }
        public int HP { get; set; }
        public int MaxHP { get; set; }
        public int MP { get; set; }
        public int MaxMP { get; set; }
        public int Attack { get; set; }
        public int Defense { get; set; }
        public int PAttack { get; set; }
        public int PDefense { get; set; }
        public int MAttack { get; set; }
        public int MDefense { get; set; }
        public int Speed { get; set; }
        public int Evasion { get; set; }
        public int Level { get; set; }

        public Element off_element = Element.none;
        public Element def_element = Element.none;

        // Player Attributes
        public CharacterClass PClass { get; set; }
        public bool Active { get; set; }
        public int CurrentXP { get; set; }
        public int RequiredXP { get; set; }
        public int AP { get; set; }
        public int MaxAP { get; set; }
        public int CurrentTarget { get; set; }
        public int CurrentMove { get; set; }
        public int CurrentAbility { get; set; }
        public int CurrentSpell { get; set; }

        public Dictionary<string, int> Attributes = new Dictionary<string, int>()
        {
            { "int", 1 },
            { "wis", 1 },
            { "str", 1 },
            { "con", 1 },
            { "dex", 1 },
            { "per", 1 },
            { "cha", 1 },
            { "fte", 1 }
        };

        public Dictionary<string, bool> AbilityFlags = new Dictionary<string, bool>()
        {
            {"ascend_used", false },
            {"berserk", false },
            {"rolling", false }
        };

        public Dictionary<string, int> TempStats = new Dictionary<string, int>()
        {
            { "attack", 0 },
            { "defense", 0 },
            { "p_attack", 0 },
            { "p_defense", 0 },
            { "m_attack", 0 },
            { "m_defense", 0 },
            { "speed", 0 },
            { "evasion", 0 }
        };

        public enum CharacterClass { warrior = 1, ranger, mage, assassin, paladin, monk, bard }

        // Monster Attributes
        public MonsterClass MClass { get; set; }
        public Status StatusOnAttack { get; set; }
        public bool IsDefending { get; set; }
        public int DroppedGold { get; set; }
        public int DroppedXP { get; set; }
        public List<Item> DroppedItems { get; set; }
        public string AttackMessage { get; set; }
        public string AsciiArt { get; set; }

        public enum MonsterClass { melee = 1, ranged, magic }

        // TO-DO!! Get this working in C#
        //self.ability_vars = {
        //    'poison_pow': 0,
        //    'poison_dex': 0,
        //    'disarmed': False,
        //    'knockout_turns': 0,
        //    'judgement_day': 0,
        //    'taunted': [0, None],
        //    'drained': False
        //}
        
        public enum UnitType { player=1, monster, boss}
       
        public void SetTempStats()
        {
            TempStats["attack"] = Attack;
            TempStats["defense"] = Defense;
            TempStats["p_attack"] = PAttack;
            TempStats["p_defense"] = PDefense;
            TempStats["m_attack"] = MAttack;
            TempStats["m_defense"] = MDefense;
            TempStats["speed"] = Speed;
            TempStats["evasion"] = Evasion;
        }

        public bool IsAlive()
        {
            return !Statuses.Contains(Unit.Status.dead);
        }

        public bool IsPCU()
        {
            return Type == UnitType.player;
        }

        public bool IsMonster()
        {
            return Type == UnitType.monster;
        }

        public Unit(string name, UnitType unittype)
        {
            Type = unittype;
            Name = name;
            HP = 20;
            MaxHP = 20;
            MP = 5;
            MaxMP = 5;
            Attack = 8;
            Defense = 5;
            PAttack = 8;
            PDefense = 5;
            MAttack = 8;
            MDefense = 5;
            Speed = 6;
            Evasion = 3;
            Level = 1;

            if (unittype == UnitType.player)
            {
                Active = true;
                CurrentXP = 0;
                RequiredXP = 3;
                AP = 10;
                MaxAP = 10;
            }

            else if (unittype == UnitType.monster || unittype == UnitType.boss)
            {
                DroppedItems = new List<Item>();
                MClass = MonsterClass.melee;
                StatusOnAttack = Status.paralyzation;
                IsDefending = false;
                DroppedGold = 5;
                DroppedXP = 5;
                AttackMessage = "attacks";
                AsciiArt = "";

                if (unittype == UnitType.boss)
                {

                }
            }
        }
    }

    public class PCUStorage
    {
        public Unit player = new Unit("", Unit.UnitType.player);
        public Unit solou = new Unit("Solou", Unit.UnitType.player);
        public Unit chili = new Unit("Chili", Unit.UnitType.player);
        public Unit chyme = new Unit("Chyme", Unit.UnitType.player);
        public Unit storm = new Unit("Storm", Unit.UnitType.player);
        public Unit parsto = new Unit("Parsto", Unit.UnitType.player);
        public Unit adorine = new Unit("Adorine", Unit.UnitType.player);


        public List<Unit> GetAllPCUs()
        {
            return new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };
        }

        public List<Unit> GetAlivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };

            foreach (Unit pcu in pcu_list)
            {
                if (pcu.Statuses.Contains(Unit.Status.dead))
                {
                    pcu_list.Remove(pcu);
                }
            }

            return pcu_list;
        }

        public List<Unit> GetActivePCUs()
        {
            var pcu_list = new List<Unit>() { player, solou, chili, chyme, storm, parsto, adorine };

            foreach (Unit pcu in pcu_list.ToList())
            {
                if (!pcu.Active)
                {
                    pcu_list.Remove(pcu);
                }
            }

            return pcu_list;
        }
    }

    public class MonsterGenerator
    {
        public Unit GenerateMonster()
        {
            return new Unit("Whispering Goblin", Unit.UnitType.monster);
        }
    }

    public class PartyInfo
    {
        public GameState Gamestate { get; set; }
        public Mode MusicboxMode { get; set; }
        public List<Town> VisitedTowns { get; set; }
        public Tile CurrentTile { get; set; }
        public Tile RespawnTile { get; set; }
        public Town CurrentTown { get; set; }
        public int GP { get; set; }
        public int StepsWithoutBattle { get; set; }
        public int Difficulty { get; set; }
        public int AtlasStrength { get; set; }
        public string Music { get; set; }
        public string CurrentProvince { get; set; }
        public string MusicboxFolder { get; set; }
        public bool MusicboxIsPlaying { get; set; }
        public bool DoSpawns { get; set; }

        public List<string> FriendNames = new List<string>();

        public enum GameState { overworld = 1, battle, town }
        public enum Mode { AtoZ = 1, ZtoA, shuffle }

        public PartyInfo()
        {
            Gamestate = GameState.overworld;
            MusicboxMode = Mode.AtoZ;
            VisitedTowns = new List<Town>();
            CurrentTile = new Tile();
            RespawnTile = new Tile();
            CurrentTown = new Town();
            GP = 20;
            StepsWithoutBattle = 0;
            Difficulty = 0;
            AtlasStrength = 1;
            Music = "../Music/Through the Forest.ogg";
            CurrentProvince = "Overshire";
            MusicboxFolder = "";
            MusicboxIsPlaying = false;
            DoSpawns = true;

            FriendNames = new List<string>()
            {
                "apollo kalar", "apollokalar", "apollo_kalar",
                "flygon jones", "flygonjones", "flygon_jones",
                "starkiller106024", "starkiller", "star killer",
                "atomic vexal", "vexal", "wave vex",
                "therichpig", "therichpig64", "spaghettipig64", "spaghettipig",
                "theeethersplash", "the aether splash", "aethersplash", "aether splash"
            };
        }
    }

    public class PartyInfoStorage
    {
        public PartyInfo party_info = new PartyInfo();

        public PartyInfo GetPartyInfo()
        {
            return party_info;
        }
    }
}
