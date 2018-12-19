using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Methods
{
    public class Common
    {
        public string Input(string prompt)
        {
            Console.Write(prompt);
            return Console.ReadLine();
        }
    }
}
