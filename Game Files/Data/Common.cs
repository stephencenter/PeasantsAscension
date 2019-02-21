using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Reflection;
using System.Threading;

namespace Data
{
    // Here we store classes that contain useful methods, enums, and data 
    // that would not fit in any other class
    public static class CMethods
    {
        public static Random rng = new Random();

        // Input Methods
        public static string SingleCharInput(string prompt)
        {
            // Immediately returns the next key the user presses without them needing to press enter
            // Used when you KNOW the player will only have 9 or less options to choose from
            Console.Write(prompt);

            if (CInfo.Debugging)
            {
                return DebugInput();
            }

            string x = Console.ReadKey().KeyChar.ToString();
            Console.WriteLine();

            if (SavefileManager.do_blips)
            {
                SoundManager.item_pickup.SmartPlay();
            }

            return x;
        }

        public static string MultiCharInput(string prompt)
        {
            // Requires you to press enter before your string is accepted
            // Used when typing in a name or selecting from a list of 
            // more than 9 items
            Console.Write(prompt);

            if (CInfo.Debugging)
            {
                return DebugInput();
            }

            string x = Console.ReadLine();

            if (SavefileManager.do_blips)
            {
                SoundManager.item_pickup.SmartPlay();
            }

            return x;
        }

        public static string FlexibleInput(string prompt, int option_count)
        {
            // FlexibleInput allows you to use SCI when the option list is small, and MCI
            // when it is big
            // Used when you don't know how many options there will be, such as when selecting
            // inventory items or spells
            if (option_count < 10)
            {
                return SingleCharInput(prompt);
            }

            return MultiCharInput(prompt);
        }

        public static void PressAnyKeyToContinue(string prompt = "\nPress any key to continue ")
        {
            // Use this when you don't care what key the user hits, you just need
            // them to hit one
            Console.Write(prompt);

            if (!CInfo.Debugging)
            {
                Console.ReadKey(true);
            }

            if (SavefileManager.do_blips)
            {
                SoundManager.item_pickup.SmartPlay();
            }

            Console.WriteLine();
        }

        // String parsers
        public static bool IsExitString(string the_string)
        {
            List<string> ValidExitStrings = new List<string>() { "e", "x", "exit", "b", "back", "cancel" };
            return ValidExitStrings.Contains(the_string.ToLower());
        }

        public static bool IsYesString(string the_string)
        {
            List<string> ValidYesStrings = new List<string>() { "y", "ye", "yes", "yup", "yeah", "ya", "yeh", "yah", "yea", "yeehaw" };
            return ValidYesStrings.Contains(the_string.ToLower());
        }

        public static bool IsNoString(string the_string)
        {
            List<string> ValidNoStrings = new List<string>() { "n", "no", "nope", "nah", "nuh uh", "nay", "negative" };
            return ValidNoStrings.Contains(the_string.ToLower());
        }

        // Other Methods
        public static void SmartSleep(int milliseconds)
        {
            // Reduce the duration of the sleep to 0.1 seconds if debugging is set to true
            if (CInfo.Debugging)
            {
                Thread.Sleep(100);
            }

            else
            {
                Thread.Sleep(milliseconds);
            }

            // Clear the Key Buffer so that all inputs made during the Thread.Sleep() will be ignored\
            while (Console.KeyAvailable)
            {
                Console.ReadKey(true);
            }
        }

        public static T GetRandomFromIterable<T>(IEnumerable<T> iterable)
        {
            return iterable.ToList()[rng.Next(iterable.Count())];
        }

        public static void PrintDivider(int length = 0)
        {
            if (length != 0)
            {
                Console.WriteLine(new string('-', length));
            }

            else
            {
                Console.WriteLine(new string('-', SavefileManager.divider_size));
            }
        }

        public static List<string> SplitBy79(string the_string, int num = 79)
        {
            List<string> sentences = new List<string>();
            string current_sentence = "";

            foreach (string word in the_string.Split())
            {
                if ((current_sentence + word).Length > num)
                {
                    sentences.Add(current_sentence);
                    current_sentence = "";
                }

                current_sentence += $"{word} ";

                current_sentence = string.Concat(new List<string>() { current_sentence, word, " " });
            }

            if (string.IsNullOrEmpty(current_sentence))
            {
                sentences.Add(current_sentence);
            }

            return sentences;
        }

        public static double Clamp(double value, double min, double max)
        {
            // If value < min, returns min, if value > max, returns max. Otherwise, returns value
            // Used to impose both an upper and lower bound on Stats - for example, Evasion must be between 1 and 256.
            return Math.Max(min, Math.Min(max, value));
        }

        public static string DebugInput()
        {
            string chosen = GetRandomFromIterable("abcdefghijklmnopqrstuvwxyz1234567890").ToString();
            Console.WriteLine(chosen);
            return chosen;
        }
    }

    public static class CEnums
    {
        public enum Status
        {
            [Description("Silenced")] silence = 0,
            [Description("Poisoned")] poison,
            [Description("Weakened")] weakness,
            [Description("Blinded")] blindness,
            [Description("Paralyzed")] paralyzation,
            [Description("Asleep")] sleep,
            [Description("Muted")] muted,
            [Description("Alive")] alive,
            [Description("Dead")] dead
        }

        public enum Element
        {
            [Description("Fire")] fire = 0,
            [Description("Water")] water,
            [Description("Electric")] electric,
            [Description("Earth")] earth,
            [Description("Wind")] wind,
            [Description("Grass")] grass,
            [Description("Ice")] ice,
            [Description("Light")] light,
            [Description("Dark")] dark,
            [Description("Neutral")] neutral
        }

        public enum CharacterClass
        {
            [Description("Warrior")] warrior = 0,
            [Description("Mage")] mage,
            [Description("Assassin")] assassin,
            [Description("Ranger")] ranger,
            [Description("Monk")] monk,
            [Description("Paladin")] paladin,
            [Description("Bard")] bard,
            [Description("Agriculturalist")] agriculturalist,
            [Description("Any")] any
        }

        public enum EquipmentType
        {
            [Description("Armor")] armor = 0,
            [Description("Weapon")] weapon,
            [Description("Accessory")] accessory
        }

        public enum WeaponType
        {
            [Description("Melee")] melee = 0,
            [Description("Ranged")] ranged,
            [Description("Instrument")] instrument
        }

        public enum DamageType
        {
            [Description("Physical")] physical = 0,
            [Description("Piercing")] piercing,
            [Description("Magical")] magical
        }

        public enum GameState
        {
            [Description("Overworld")] overworld = 0,
            [Description("Battle")] battle,
            [Description("Town")] town
        }

        public enum MusicboxMode
        {
            [Description("A to Z")] AtoZ = 0,
            [Description("Z to A")] ZtoA,
            [Description("Shuffle")] shuffle
        }

        public enum SpellCategory
        {
            [Description("Buff")] buff = 0,
            [Description("Attack")] attack,
            [Description("Healing")] healing,
            [Description("All")] all
        }

        public enum InvCategory
        {
            [Description("Quest")] quest = 0,
            [Description("Consumables")] consumables,
            [Description("Weapons")] weapons,
            [Description("Armor")] armor,
            [Description("Tools")] tools,
            [Description("Accessories")] accessories,
            [Description("Misc")] misc
        }

        public enum MonsterGroup
        {
            [Description("Animal")] animal = 0,
            [Description("Monster")] monster,
            [Description("Humanoid")] humanoid,
            [Description("Undead")] undead,
            [Description("Dungeon")] dungeon
        }

        public enum PlayerAttribute
        {
            [Description("Strength")] strength = 0,
            [Description("Intelligence")] intelligence,
            [Description("Dexterity")] dexterity,
            [Description("Perception")] perception,
            [Description("Constitution")] constitution,
            [Description("Wisdom")] wisdom,
            [Description("Charisma")] charisma,
            [Description("Fate")] fate
        }

        public static string EnumToString(this Enum value)
        {
            Type type = value.GetType();
            string name = Enum.GetName(value.GetType(), value);

            if (name != null)
            {
                FieldInfo field = type.GetField(name);
                if (field != null)
                {
                    if (Attribute.GetCustomAttribute(field, typeof(DescriptionAttribute)) is DescriptionAttribute attr)
                    {
                        return attr.Description;
                    }
                }
            }

            return null;
        }

        // element_matchup[key][0] is the element that key is weak to
        // element_matchup[key][1] is the element that key is resistant to
        public static Dictionary<Element, List<Element>> ElementChart = new Dictionary<Element, List<Element>>
        {
            { Element.fire, new List<Element> { Element.water, Element.ice } },
            { Element.water, new List<Element> { Element.electric, Element.fire } },
            { Element.electric, new List<Element> { Element.earth, Element.water } },
            { Element.earth, new List<Element> { Element.wind, Element.electric } },
            { Element.wind, new List<Element> { Element.grass, Element.earth } },
            { Element.grass, new List<Element> { Element.ice, Element.wind } },
            { Element.ice, new List<Element> { Element.fire, Element.grass } },
            { Element.light, new List<Element> { Element.dark, Element.light } },
            { Element.dark, new List<Element> { Element.light, Element.dark } }
        };

        public static DamageType CharacterClassToDamageType(CharacterClass p_class)
        {
            Dictionary<CharacterClass, DamageType> damage_type_map = new Dictionary<CharacterClass, DamageType>()
            {
                { CharacterClass.warrior, DamageType.physical },
                { CharacterClass.assassin, DamageType.physical },
                { CharacterClass.monk, DamageType.physical },
                { CharacterClass.paladin, DamageType.physical },
                { CharacterClass.mage, DamageType.piercing },
                { CharacterClass.bard, DamageType.piercing },
                { CharacterClass.ranger, DamageType.piercing }
            };

            return damage_type_map[p_class];
        }
    }

    public static class CInfo
    {
        // Unsaved Things
        public static bool MusicboxIsPlaying = false;
        public static int StepsWithoutBattle = 0;
        public static CEnums.GameState Gamestate = CEnums.GameState.overworld;
        public static readonly string GameVersion = "v1.0.0";
        public static readonly bool Debugging = false;

        public static readonly List<string> FriendNames = new List<string>()
        {
            "apollo kalar", "apollokalar", "apollo_kalar",
            "flygon jones", "flygonjones", "flygon_jones",
            "starkiller106024", "starkiller", "star killer",
            "atomic vexal", "vexal", "wave vex",
            "therichpig", "therichpig64", "spaghettipig64", "spaghettipig", "pastahog", "pastahog64",
            "theaethersplash", "the aether splash", "aethersplash", "aether splash"
        };

        // Saved Things
        public static CEnums.MusicboxMode MusicboxMode = CEnums.MusicboxMode.AtoZ;
        public static List<string> DefeatedBosses = new List<string>();
        public static int GP = 20;
        public static int Difficulty = 0;
        public static int AtlasStrength = 1;
        public static string MusicboxFolder = "";
        public static string CurrentTile = "nearton_s";
        public static string RespawnTile = "nearton_tile";
        public static bool DoSpawns = true;
        public static bool HasCheated = false;
    }
}
