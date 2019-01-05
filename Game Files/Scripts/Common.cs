using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public class CommonMethods
    {
        public string Input(string prompt)
        {
            Console.Write(prompt);
            return Console.ReadLine();
        }

        public void PrintDivider()
        {
            // Initialize the settings manager
            SavefileManager settings_manager = new SavefileManager();

            Console.WriteLine(new string('-', settings_manager.GetDividerSize()));
        }

        public void PressEnterReturn()
        {
            Input("\nPress enter/return ");
        }

        public List<string> SplitBy79(string the_string, int num = 79)
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

            if (current_sentence != "")
            {
                sentences.Add(current_sentence);
            }

            return sentences;
        }

        public bool IsExitString(string the_string)
        {
            List<string> ValidExitStrings = new List<string>() { "e", "x", "exit", "b", "back", "cancel" };

            if (ValidExitStrings.Contains(the_string.ToLower()))
            {
                return true;
            }

            return false;
        }

        public int Clamp(int value, int max, int min)
        {
            return Math.Max(min, Math.Min(max, value));
        }

        public void TextScrollWrite(string the_string, int spacing = 25)
        {
            the_string = string.Join("", new List<string>() { the_string, "\n" });

            int counter = 0;
            foreach (char character in the_string)
            {
                Console.Write(character);

                if (character != ' ' && counter + 1 != the_string.Count())
                {
                    Thread.Sleep(spacing);
                }
            }
        }

        public string TextScrollInput(string the_string, int spacing = 25)
        {
            TextScrollWrite(the_string, spacing);
            return Input(the_string[the_string.Length - 1].ToString());
        }
    }

    public class CEnums
    {
        public enum UnitType { player, monster, boss }
        public enum Status { silence, poison, weakness, blindness, paralyzation, muted, alive, dead }
        public enum Element { fire, water, electric, earth, wind, grass, ice, light, dark, neutral }
        public enum CharacterClass { warrior, ranger, mage, assassin, paladin, monk, bard, any }
        public enum MonsterClass { melee, ranged, magic }
        public enum EquipmentType { head, body, legs, weapon, accessory }
        public enum WeaponType { melee, ranged, instrument }
        public enum DamageType { physical, piercing, magical }

        // element_matchup[key][0] is the element that key is weak to
        // element_matchup[key][1] is the element that key is resistant to
        public Dictionary<Element, List<Element>> ElementChart = new Dictionary<Element, List<Element>>
        {
            {Element.fire, new List<Element> { Element.water, Element.ice } },
            {Element.water, new List<Element> { Element.electric, Element.fire } },
            {Element.electric, new List<Element> { Element.earth, Element.water } },
            {Element.earth, new List<Element> { Element.wind, Element.electric } },
            {Element.wind, new List<Element> { Element.grass, Element.earth } },
            {Element.grass, new List<Element> { Element.ice, Element.wind } },
            {Element.ice, new List<Element> { Element.fire, Element.grass } },
            {Element.light, new List<Element> { Element.dark, Element.light } },
            {Element.dark, new List<Element> { Element.light, Element.dark } }
        };

        public string EnumToString(Enum the_enum)
        {
            Dictionary<Enum, string> StatusNameMap = new Dictionary<Enum, string>()
            {
                {Status.silence, "Silenced"},
                {Status.poison, "Poisoned"},
                {Status.weakness, "Weakened"},
                {Status.blindness, "Blindned"},
                {Status.paralyzation, "Paralyzed" },
                {Status.muted, "Muted"},
                {Status.alive, "Alive"},
                {Status.dead, "Dead"},

                {UnitType.player, "Player" },
                {UnitType.monster, "Monster" },
                {UnitType.boss, "Boss" },

                {Element.fire, "Fire"},
                {Element.water, "Water"},
                {Element.electric, "Electric"},
                {Element.earth, "Earth"},
                {Element.wind, "Wind"},
                {Element.grass, "Grass"},
                {Element.ice, "Ice"},
                {Element.light, "Light"},
                {Element.dark, "Dark"},
                {Element.neutral, "Neutral"},

                {CharacterClass.warrior, "Warrior" },
                {CharacterClass.ranger, "Ranger"},
                {CharacterClass.mage, "Mage"},
                {CharacterClass.assassin, "Assassin"},
                {CharacterClass.paladin, "Paladin"},
                {CharacterClass.monk, "Monk"},
                {CharacterClass.bard, "Bard"},

                {MonsterClass.melee, "Melee"},
                {MonsterClass.ranged, "Ranged"},
                {MonsterClass.magic, "Magic"},

                {EquipmentType.head, "Head"},
                {EquipmentType.body, "Body"},
                {EquipmentType.legs, "Legs"},
                {EquipmentType.weapon, "Weapon"},
                {EquipmentType.accessory, "Accessory"},

                {WeaponType.melee, "Melee"},
                {WeaponType.ranged, "Ranged"},
                {WeaponType.instrument, "Instrument"},

                {DamageType.physical, "Physical"},
                {DamageType.magical, "Magical"},
                {DamageType.piercing, "Piercing"}
            };

            return StatusNameMap[the_enum];
        }

        public DamageType CharacterClassToDamageType(CharacterClass p_class)
        {
            Dictionary<CharacterClass, DamageType> damage_type_map = new Dictionary<CharacterClass, DamageType>()
            {
                {CharacterClass.warrior, DamageType.physical},
                {CharacterClass.assassin, DamageType.physical},
                {CharacterClass.monk, DamageType.physical},
                {CharacterClass.paladin, DamageType.physical},
                {CharacterClass.mage, DamageType.piercing},
                {CharacterClass.bard, DamageType.piercing},
                {CharacterClass.ranger, DamageType.piercing}
            };

            return damage_type_map[p_class];
        }
    }
}
