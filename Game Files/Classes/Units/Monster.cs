using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Classes.Items;
using Classes.Units;

namespace Classes.Units
{
    public class Monster : Unit
    {
        public MonsterClass MClass { get; set; }
        public Status StatusOnAttack { get; set; }
        public bool IsDefending { get; set; }
        public int DroppedGold { get; set; }
        public int DroppedXP { get; set; }
        public List<Item> DroppedItems { get; set; }
        public string AttackMessage { get; set; }
        public string AsciiArt { get; set; }
        
        public enum MonsterClass { melee=1, ranged, magic }

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
        
        public Monster(string name)
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
    }
}
