using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Scripts
{
    public class Common
    {
        readonly SaveLoad settings = new SaveLoad();

        public string Input(string prompt)
        {
            Console.Write(prompt);
            return Console.ReadLine();
        }

        public void DisplayDivider()
        {
            Console.WriteLine(new String('-', settings.GetDividerSize()));
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

                current_sentence = String.Join("", new List<string>() { current_sentence, word, " " });
            }

            if (current_sentence != "")
            {
                sentences.Add(current_sentence);
            }

            return sentences;
        }

        public void TextScrollWrite(string the_string, int spacing = 25)
        {
            the_string = String.Join("", new List<string>() { the_string, "\n" });

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

        public int Clamp(int value, int max, int min)
        {
            return Math.Max(min, Math.Min(max, value));
        }

        public bool IsExitString(string the_string)
        {
            List<string> ValidExitStrings = new List<string>() { "e", "x", "exit", "b", "back", "cancel"};

            if (ValidExitStrings.Contains(the_string))
            {
                return true;
            }

            return false;
        }
    }
}
