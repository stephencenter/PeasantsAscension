using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classes.Units
{
    public class Unit
    {
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
    }
}
