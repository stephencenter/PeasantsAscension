using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public static class CMethods
    {
        // When this is set to true, all Inputs() will auto-return a random 
        // character instead of requesting user input. Also reduces the
        // duration of all SmartSleep() methods to 0.1 seconds. 
        public static readonly bool debugging = false;

        public static string Input(string prompt = "", bool local_do_blips = true)
        {
            Console.Write(prompt);

            if (debugging)
            {
                string chosen = GetRandomFromIterable("abcdefghijklmnopqrstuvwxyz1234567890").ToString();
                Console.WriteLine(chosen);
                return chosen;
            }

            else
            {
                return Console.ReadLine();
            }
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

        public static void PressEnterReturn()
        {
            Input("\nPress enter/return ");
        }

        public static List<string> SplitBy79(string the_string, int num = 79)
        {
            List<string> sentences = new List<string>();
            string current_sentence = "";

            foreach (string word in the_string.Split())
            {
                if ((current_sentence + word).Count() > num)
                {
                    sentences.Add(current_sentence);
                    current_sentence = "";
                }

                current_sentence += $"{word} ";

                current_sentence = string.Join("", new List<string>() { current_sentence, word, " " });
            }

            if (string.IsNullOrEmpty(current_sentence))
            {
                sentences.Add(current_sentence);
            }

            return sentences;
        }

        public static int Clamp(int value, int min, int max)
        {
            // If value < min, returns min, if value > max, returns max. Otherwise, returns value
            // Used to impose both an upper and lower bound on Stats - for example, Evasion must be between 1 and 256.
            return Math.Max(min, Math.Min(max, value));
        }

        public static void TextScrollWrite(string the_string, int spacing = 25)
        {
            the_string = string.Join("", new List<string>() { the_string, "\n" });

            int counter = 0;
            foreach (char character in the_string)
            {
                Console.Write(character);

                if (character != ' ' && counter + 1 != the_string.Count())
                {
                    SmartSleep(spacing);
                }
            }
        }

        public static string TextScrollInput(string the_string, int spacing = 25)
        {
            TextScrollWrite(the_string, spacing);
            return Input(the_string[the_string.Length - 1].ToString());
        }

        public static bool IsExitString(string the_string)
        {
            List<string> ValidExitStrings = new List<string>() { "e", "x", "exit", "b", "back", "cancel" };
            return ValidExitStrings.Contains(the_string.ToLower());
        }

        public static bool IsYesString(string the_string)
        {
            List<string> ValidYesStrings = new List<string>() { "y", "ye", "yes", "yup", "yeah", "ya", "yeh", "yah", "yea" };
            return ValidYesStrings.Contains(the_string.ToLower());
        }

        public static bool IsNoString(string the_string)
        {
            List<string> ValidNoStrings = new List<string>() { "n", "no", "nope", "nah", "nuh uh", "nay", "negative" };
            return ValidNoStrings.Contains(the_string.ToLower());
        }

        public static T GetRandomFromIterable<T>(IEnumerable<T> iterable)
        {
            Random rng = new Random();
            return iterable.ToList()[rng.Next(iterable.Count())];
        }

        public static void SmartSleep(int milliseconds)
        {
            // Reduce the duration of the sleep to 0.1 seconds if debugging is set to true
            if (debugging)
            {
                Thread.Sleep(100);
            }

            else
            {
                Thread.Sleep(milliseconds);
            }

            // Clear the Key Buffer so that all inputs made during the Thread.Sleep() will be ignored
            while (Console.KeyAvailable)
            {
                Console.ReadKey(true);
            }
        }
    }

    public static class CEnums
    {
        public enum Status { silence, poison, weakness, blindness, paralyzation, sleep, muted, alive, dead }
        public enum Element { fire, water, electric, earth, wind, grass, ice, light, dark, neutral }
        public enum CharacterClass { warrior, ranger, mage, assassin, paladin, monk, bard, any }
        public enum MonsterClass { melee, ranged, magic }
        public enum EquipmentType { head, body, legs, weapon, accessory }
        public enum WeaponType { melee, ranged, instrument }
        public enum DamageType { physical, piercing, magical }
        public enum GameState { overworld, battle, town }
        public enum MusicboxMode { AtoZ, ZtoA, shuffle }
        public enum SpellCategory { buff, attack, healing }
        public enum InventoryCategory { }

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

        public static string EnumToString(Enum the_enum)
        {
            Dictionary<Enum, string> StatusNameMap = new Dictionary<Enum, string>()
            {
                { Status.silence, "Silenced" },
                { Status.poison, "Poisoned" },
                { Status.weakness, "Weakened" },
                { Status.blindness, "Blindned" },
                { Status.paralyzation, "Paralyzed" },
                { Status.muted, "Muted" },
                { Status.sleep, "Asleep" },
                { Status.alive, "Alive" },
                { Status.dead, "Dead" },

                { Element.fire, "Fire" },
                { Element.water, "Water" },
                { Element.electric, "Electric" },
                { Element.earth, "Earth" },
                { Element.wind, "Wind" },
                { Element.grass, "Grass" },
                { Element.ice, "Ice" },
                { Element.light, "Light" },
                { Element.dark, "Dark" },
                { Element.neutral, "Neutral" },

                { CharacterClass.warrior, "Warrior" },
                { CharacterClass.ranger, "Ranger" },
                { CharacterClass.mage, "Mage" },
                { CharacterClass.assassin, "Assassin" },
                { CharacterClass.paladin, "Paladin" },
                { CharacterClass.monk, "Monk" },
                { CharacterClass.bard, "Bard" },

                { MonsterClass.melee, "Melee" },
                { MonsterClass.ranged, "Ranged" },
                { MonsterClass.magic, "Magic" },

                { EquipmentType.head, "Head" },
                { EquipmentType.body, "Body" },
                { EquipmentType.legs, "Legs" },
                { EquipmentType.weapon, "Weapon" },
                { EquipmentType.accessory, "Accessory" },

                { WeaponType.melee, "Melee" },
                { WeaponType.ranged, "Ranged" },
                { WeaponType.instrument, "Instrument" },

                { DamageType.physical, "Physical" },
                { DamageType.magical, "Magical" },
                { DamageType.piercing, "Piercing" },

                { MusicboxMode.AtoZ, "A-to-Z" },
                { MusicboxMode.ZtoA, "Z-to-A" },
                { MusicboxMode.shuffle, "Shuffle" },

                { SpellCategory.buff, "Buff" },
                { SpellCategory.attack, "Attack" },
                { SpellCategory.healing, "Healing" }
            };

            return StatusNameMap[the_enum];
        }

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
}
