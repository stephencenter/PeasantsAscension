using Classes.Units;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classes.Units
{
    public class PlayableCharacter : Unit
    {
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

        public PlayableCharacter(string name)
        {
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
        }

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

    }

    public class PCUStorage
    {
        public PlayableCharacter player = new PlayableCharacter("");
        public PlayableCharacter solou = new PlayableCharacter("Solou");
        public PlayableCharacter chili = new PlayableCharacter("Chili");
        public PlayableCharacter chyme = new PlayableCharacter("Chyme");
        public PlayableCharacter storm = new PlayableCharacter("Storm");
        public PlayableCharacter parsto = new PlayableCharacter("Parsto");
        public PlayableCharacter adorine = new PlayableCharacter("Adorine");


        public List<PlayableCharacter> GetAllPCUs()
        {
            return new List<PlayableCharacter>() { player, solou, chili, chyme, storm, parsto, adorine };
        }

        public List<PlayableCharacter> GetAlivePCUs()
        {
            var pcu_list = new List<PlayableCharacter>() { player, solou, chili, chyme, storm, parsto, adorine };

            foreach (PlayableCharacter pcu in pcu_list)
            {
                if (pcu.Statuses.Contains(Unit.Status.dead))
                {
                    pcu_list.Remove(pcu);
                }
            }

            return pcu_list;
        }

        public List<PlayableCharacter> GetActivePCUs()
        {
            var pcu_list = new List<PlayableCharacter>() { player, solou, chili, chyme, storm, parsto, adorine };

            foreach (PlayableCharacter pcu in pcu_list)
            {
                if (!pcu.Active)
                {
                    pcu_list.Remove(pcu);
                }
            }

            return pcu_list;
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

        List<string> FriendNames = new List<string>()
        {
            "apollo kalar", "apollokalar", "apollo_kalar",
            "flygon jones", "flygonjones", "flygon_jones",
            "cynder887",
            "starkiller106024", "starkiller", "star killer",
            "atomic vexal", "vexal", "wave vex",
            "therichpig", "therichpig64", "spaghettipig64", "spaghettipig",
            "theeethersplash", "the aether splash", "aethersplash", "aether splash"
        };

        public enum GameState { overworld=1, battle, town }
        public enum Mode { AtoZ=1, ZtoA, shuffle}

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
                "cynder887",
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
