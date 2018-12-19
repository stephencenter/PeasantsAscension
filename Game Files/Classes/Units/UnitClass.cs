using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classes.Units
{
    public class UnitClass
    {
        public enum Element { fire = 1, water, electric, earth, wind, grass, ice, light, dark }
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

        public enum Status { silence = 1, poison, weakness, blindness, paralyzation }
        public List<string> statuses = new List<string> { };

        public string name { get; set; }
        public int hp { get; set; }
        public int max_hp { get; set; }
        public int mp { get; set; }
        public int max_mp { get; set; }
        public int attack { get; set; }
        public int defense { get; set; }
        public int p_attack { get; set; }
        public int p_defense { get; set; }
        public int m_attack { get; set; }
        public int m_defense { get; set; }
        public int speed { get; set; }
        public int evasion { get; set; }
        public int level { get; set; }

        public Element off_element { get; set; }
        public Element def_element { get; set; }

        public UnitClass(String n, int m_hp, int m_mp, int attk, int dfns, int p_attk, int p_dfns, int m_attk, int m_dfns, int spd, int evad, int lvl)
        {
            name = n;
            max_hp = m_hp;
            hp = m_hp;
            max_mp = m_mp;
            mp = m_mp;
            attack = attk;
            defense = dfns;
            p_attack = p_attk;
            p_defense = p_dfns;
            m_attack = m_attk;
            m_defense = m_dfns;
            speed = spd;
            evasion = evad;
            level = lvl;
        }
    }
}
