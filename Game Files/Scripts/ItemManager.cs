using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    public static class ItemManager
    {
        private static readonly List<dynamic> item_list = new List<dynamic>()
        {
            /* =========================== *
             *           WEAPONS           *
             * =========================== */
            new Weapon("Fists", "The oldest weapon known to man.",
                0, 0, CEnums.WeaponType.melee, CEnums.CharacterClass.any, CEnums.Element.neutral, "weapon_fists"),
            
            /* =========================== *
             *            ARMOR            *
             * =========================== */
            new Armor("None", "You should probably get some armor.",
                0, 0, 0, new List<CEnums.CharacterClass>() {}, new List<CEnums.CharacterClass>() {}, "no_armor"),
            
            /* =========================== *
             *         ACCESSORIES         *
             * =========================== */
            new ElementAccessory("None", "You should probably get an accessory.", 0, CEnums.Element.neutral, "no_access")
        };

        public static List<dynamic> GetItemList()
        {
            return item_list;
        }

        public static Item FindItemWithID(string item_id)
        {
            return GetItemList().Single(x => x.ItemID == item_id);
        }
    }

    public abstract class Item
    {
        // The basic item class. Items are stored in the "inventory" dictionary. All
        // item-subclasses inherit from this class.
        public string Name { get; set; }
        public string Description { get; set; }
        public int Value { get; set; }
        public bool IsImportant { get; set; }
        public CEnums.InvCategory Category { get; set; }
        public string ItemID { get; set; }

        public abstract void UseItem(PlayableCharacter user);

        // Constructor
        protected Item(string name, string desc, int value, bool imp, CEnums.InvCategory cat, string item_id)
        {
            Name = name;
            Description = desc;
            Value = value;
            IsImportant = imp;
            Category = cat;
            ItemID = item_id;
        }
    }

    public class Ingredient : Item
    {
        public string Flavor { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            Console.WriteLine("It's called an ingredient, but you probably shouldn't eat it.");
            CMethods.PressEnterReturn();
        }

        public Ingredient(string name, string desc, int value, string flavor, string item_id) : base(name, desc, value, false, CEnums.InvCategory.misc, item_id)
        {

        }
    }

    /* =========================== *
     *          EQUIPMENT          *
     * =========================== */
    public abstract class Equipment : Item
    {
        public CEnums.EquipmentType EquipType { get; set; }

        public abstract void Unequip(PlayableCharacter unequipper);

        // Constructor
        protected Equipment(string name, string desc, int value, CEnums.InvCategory cat, string item_id) : base(name, desc, value, false, cat, item_id)
        {

        }        
    }

    public class Weapon : Equipment
    {
        // Items that increase your damage by a percentage.
        public double Power { get; set; }
        public CEnums.WeaponType WeaponType { get; set; }
        public CEnums.CharacterClass PClass { get; set; }
        public CEnums.Element Element { get; set; }

        public override void UseItem(PlayableCharacter equipper)
        {
            throw new NotImplementedException();
            /*
            if user.class_ in self.class_ or not self.class_:
                equip_item(self.item_id, user)

                print(f'{user.name} equips the {self.name}.')
                main.s_input("\nPress enter/return ")

            else:
                print(f"This {self.name} is f{self.class_req[3:]}.")

                main.s_input("\nPress enter/return ") */
        }

        public override void Unequip(PlayableCharacter unequipper)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public Weapon(string name, string desc, int value, double power, CEnums.WeaponType w_type, CEnums.CharacterClass p_class, CEnums.Element element, string item_id) : base(name, desc, value, CEnums.InvCategory.weapons, item_id)
        {
            Power = power;
            WeaponType = w_type;
            PClass = p_class;
            Element = element;
            EquipType = CEnums.EquipmentType.weapon;
        }
    }

    public class Armor : Equipment
    {
        // Items that give the player a percent resistance to all damage,
        // but reduce player speed and evasion to compensate
        public double Resist { get; set; }
        public double Penalty { get; set; }

        // Proficient classes get a 1.5x increase in resist, and a 1.5x decrease in penalty
        // Non-proficient classes get a 1.5x decrease in resist, and a 1.5x increase in penalty
        public List<CEnums.CharacterClass> ProficientClasses { get; set; }
        public List<CEnums.CharacterClass> NonProficientClasses { get; set; }

        public override void UseItem(PlayableCharacter equipper)
        {
            throw new NotImplementedException();
            /*
            if user.class_ in self.class_ or not self.class_:
                equip_item(self.item_id, user)
                print(f'{user.name} equips the {self.name}.')
                main.s_input("\nPress enter/return ")

            else:
                print(f"This {self.name} is f{self.class_req[3:]}.")

                main.s_input("\nPress enter/return ") */
        }

        public override void Unequip(PlayableCharacter unequipper)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public Armor(string name, string desc, int value, double resist, double penatly, List<CEnums.CharacterClass> prof_classes, List<CEnums.CharacterClass> nonprof_classes, string item_id) :  base(name, desc, value, CEnums.InvCategory.weapons, item_id)
        {
            Resist = resist;
            Penalty = penatly;
            ProficientClasses = prof_classes;
            NonProficientClasses = nonprof_classes;
            EquipType = CEnums.EquipmentType.armor;
        }
    }

    public class ElementAccessory : Equipment
    {
        // Gives the player an element used when taking damage
        public CEnums.Element Element { get; set; }

        public override void UseItem(PlayableCharacter equipper)
        {
            throw new NotImplementedException();
            /*
            def use_item(self, user) :
                equip_item(self.item_id, user)
                user.def_element = self.def_element

                print(f'{user.name} equips the {self.name}. Their element is now set to {self.def_element}.')
                main.s_input("\nPress enter/return ") */
        }

        public override void Unequip(PlayableCharacter unequipper)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public ElementAccessory(string name, string desc, int value, CEnums.Element element, string item_id) : base(name, desc, value, CEnums.InvCategory.accessories, item_id)
        {
            Element = element;
        }
    }

    public class ActionAccessory : Equipment
    {
        public int BonusAP { get; set; }

        public override void UseItem(PlayableCharacter equipper)
        {
            throw new NotImplementedException();
        }

        public override void Unequip(PlayableCharacter unequipper)
        {
            throw new NotImplementedException();
        }

        // Constructor
        protected ActionAccessory(string name, string desc, int value, int bonus_ap, string item_id) : base(name, desc, value, CEnums.InvCategory.accessories, item_id)
        {
            BonusAP = bonus_ap;
        }
    }

    /* =========================== *
     *           POTIONS           *
     * =========================== */
    public class HealthManaPotion : Item
    {
        // Items that restore your HP, MP, or both
        public int Health { get; set; }
        public int Mana { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
            /*
            print(f'{user.name} consumes the {self.name}...')

            main.smart_sleep(0.75)
            sounds.magic_healing.SmartPlay()

            if self.heal > 0:
                user.hp += self.heal
                print(f"{user.name} restored {self.heal} HP with the {self.name}!")

            if self.mana > 0:
                user.mp += self.mana
                print(f"{user.name} restored {self.mana} MP with the {self.name}!")

            units.fix_stats()

            if main.party_info['gamestate'] != 'battle':
                main.s_input("\nPress enter/return ")

            remove_item(self.item_id) */
        }

        // Constructor
        public HealthManaPotion(string name, string desc, int value, int heal, int mana, string item_id) : base(name, desc, value, false, CEnums.InvCategory.consumables, item_id)
        {
            Health = heal;
            Mana = mana;
        }
    }

    public class StatusPotion : Item
    {
        public CEnums.Status Status { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
            /*
            if self.status in user.status_ail:
                sounds.buff_spell.SmartPlay()
                user.status_ail = [x for x in user.status_ail if x != self.status]

                print(f'{user.name} consumes the {self.name}...')
                main.smart_sleep(0.75)
                sounds.magic_healing.SmartPlay()

                print(f"{user.name} is no longer {self.status}!")

                if main.party_info['gamestate'] != 'battle':
                    main.s_input("\nPress enter/return ")

                remove_item(self.item_id)

            else:
                print(f"Drinking this {self.name} probably wouldn't do anything.")
                main.s_input("\nPress enter/return ") */
        }

        // Constructor
        public StatusPotion(string name, string desc, int value, CEnums.Status status, string item_id) : base(name, desc, value, false, CEnums.InvCategory.consumables, item_id)
        {
            Status = status;
        }
    }

    public class AttractPotion : Item
    {
        public int NumberOfSteps { get; set; }
        public int MonsterCount { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public AttractPotion(string name, string desc, int value, int numsteps, int moncount, string item_id) : base(name, desc, value, false, CEnums.InvCategory.consumables, item_id)
        {
            NumberOfSteps = numsteps;
            MonsterCount = moncount;
        }
    }

    public class RepelPotion : Item
    {
        public int NumberOfSteps { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public RepelPotion(string name, string desc, int value, int numsteps, string item_id) : base(name, desc, value, false, CEnums.InvCategory.consumables, item_id)
        {
            NumberOfSteps = numsteps;
        }
    }

    public class BombPotion : Item
    {
        public bool MultiTargeted { get; set; }
        public int Damage { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public BombPotion(string name, string desc, int value, bool multitarget, int damage, string item_id) : base(name, desc, value, false, CEnums.InvCategory.consumables, item_id)
        {
            MultiTargeted = multitarget;
            Damage = damage;
        }
    }

    public class XPGoldPotion : Item
    {
        public int GoldChange { get; set; }
        public int XPChange { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public XPGoldPotion(string name, string desc, int value, int gold_change, int xp_change, string item_id) : base(name, desc, value, false, CEnums.InvCategory.consumables, item_id)
        {
            GoldChange = gold_change;
            XPChange = xp_change;
        }
    }

    public class GameCrashPotion : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            throw new Exception("You asked for this.");
        }

        // Constructor
        public GameCrashPotion(string name, string desc, int value, string item_id) : base(name, desc, value, false, CEnums.InvCategory.consumables, item_id)
        {

        }
    }

    /* =========================== *
     *            TOOLS            *
     * =========================== */
    public class Shovel : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
            /*
            if main.party_info['gamestate'] == 'town':
                print("What, here? You can't just start digging up a town!")
                main.s_input("\nPress enter/return")
                return

            print("Digging...")
            sounds.foot_steps.SmartPlay()
            main.smart_sleep(1)

            print("Digging...")
            sounds.foot_steps.SmartPlay()
            main.smart_sleep(1)

            print("Still digging...")
            sounds.foot_steps.SmartPlay()
            main.smart_sleep(1)

            try:
                c_gem = [x for x in main.party_info['current_tile'].gem_list if x.item_id not in acquired_gems][0]

            except IndexError:
                 c_gem = None

            if c_gem:
                sounds.unlock_chest.SmartPlay()
                print(f"Aha, your party found a {c_gem.name}! Might be a good idea to sell it.")
                main.s_input("\nPress enter/return ")

                acquired_gems.append(c_gem.item_id)
                add_item(c_gem.item_id)

            else:
                print("No luck, your party didn't find anything.")
                main.s_input("\nPress enter/return ") */
        }

        // Constructor
        public Shovel(string name, string desc, int value, string item_id) : base(name, desc, value, true, CEnums.InvCategory.tools, item_id)
        {

        }
    }

    public class FastTravelAtlas : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
            /*
            if main.party_info['gamestate'] == 'town':
                print("Fast Travel Atlases can't be used in towns.")
                main.s_input("\nPress enter/return")
                return

            self.choose_prov() */
        }

        private static void ChooseProvince()
        {
            /*
            avail_provs = tiles.all_provinces[:main.party_info['map_pow']]

            if len(avail_provs) == 1:
                self.choose_cell(avail_provs[0])

                return

            while True:
                print(f"Available Provinces [Pages: {main.party_info['map_pow']}]: ")
                for num, x in enumerate(avail_provs) :
                    print(f"      [{num + 1}] {x.name}")

                while True:
                    chosen = main.s_input('Input [#] (or type "exit"): ')

                    try:
                        chosen = avail_provs[int(chosen) - 1]

                    except(IndexError, ValueError):
                        if chosen in ['e', 'x', 'exit', 'b', 'back']:
                            print('-'*save_load.divider_size)
                            return False

                        continue

                    print('-' * save_load.divider_size)
                    self.choose_cell(chosen)

                    return */
        }

        private static void ChooseCell(Province prov)
        {
            /*
            while True:
                print(f"{prov.name} Province Locations: ")
                for num, x in enumerate(prov.cells) :
                    print(f"      [{num + 1}] {x.name}")

                do_loop = True
                while do_loop:
                    chosen = main.s_input('Input [#] (or type "back"): ')

                    try:
                        chosen = prov.cells[int(chosen) - 1]

                    except(IndexError, ValueError):
                        if chosen in ['e', 'x', 'exit', 'b', 'back']:
                            print('-' * save_load.divider_size)
                            return

                        continue

                    print("-"*save_load.divider_size)
                    while True:
                        y_n = main.s_input(f"Warp to {chosen.name}? | Yes or No: ").lower()

                        if y_n.startswith('y'):
                            if 'has_teleported' not in main.party_info:
                                main.party_info['has_teleported'] = False

                            if main.party_info['has_teleported']:
                                print("-"*save_load.divider_size)
                                print("Your party peers into the Fast Travel Atlas and begins to phase out of reality.")
                                print("Upon waking you're exactly where you wanted to be.")
                                main.s_input("\nPress enter/return ")

                            else:
                                print("-"*save_load.divider_size)
                                print("You begin to feel strange - your body feels light and all you hear is silence.")
                                print("Your vision starts going blank... All of your senses quickly turning off until")
                                print("you're left with nothing but your thoughts...")
                                main.s_input("\nPress enter/return ")
                                print("...")
                                main.smart_sleep(1)
                                print("...")
                                main.smart_sleep(1)
                                print("...")
                                main.smart_sleep(1)
                                sounds.enemy_hit.SmartPlay()
                                print("CRASH! Your senses re-emerge you've landed on your back... Oh, you're exactly where")
                                print("you teleported to!")
                                main.s_input("\nPress enter/return ")

                            main.party_info['has_teleported'] = True
                            main.party_info['prov'] = prov.name
                            main.party_info['current_tile'] = chosen.primary_tile

                            if main.party_info['music'] != chosen.music:
                                main.party_info['music'] = chosen.music
                                SoundManager.PlayCellMusic();

                            towns.search_towns()
                            return

                        if y_n.startswith('n'):
                            print('-'*save_load.divider_size)
                            do_loop = False

                            break */
        }

        // Constructor
        public FastTravelAtlas(string name, string desc, int value, string item_id) : base(name, desc, value, true, CEnums.InvCategory.tools, item_id)
        {

        }
    }

    public class LockpickKit : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public LockpickKit(string name, string desc, int value, string item_id) : base(name, desc, value, true, CEnums.InvCategory.tools, item_id)
        {

        }
    }

    public class MonsterEncyclopedia : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
            /*
            
            m_w = {'fire': 'water',
                    'water': 'electric',
                    'electric': 'earth',
                    'earth': 'wind',
                    'wind': 'grass',
                    'grass': 'ice',
                    'ice': 'fire',
                    'neutral': 'neutral',
                    'light': 'dark',
                    'dark': 'light'}[user.target.def_element]

            print(f"""{user.target.name.upper()}'s STATS:
            Physical: { user.target.attk}
            Attack / {user.target.dfns} Defense
            Magical: {user.target.m_attk} Attack / {user.target.m_dfns} Defense
            Piercing: {user.target.p_attk} Attack / {user.target.p_dfns} Defense
            Speed: {user.target.spd}
            Evasion: {user.target.evad}
            Elements: Attacks are { user.target.def_element.title()} / Defense is {user.target.off_element.title()} / \
            Weak to { m_w.title()}""") */
        }

        public MonsterEncyclopedia(string name, string desc, int value, string item_id) : base(name, desc, value, true, CEnums.InvCategory.tools, item_id)
        {

        }
    }

    public class PocketAlchemyLab : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
            /*
            chosen_ingredients = []
    available_flavors = {}

            for item in inventory['misc']:
                if isinstance(item, Ingredient) :
                    if item.flavor in available_flavors:
                        available_flavors[item.flavor].append(item)

                    else:
                        available_flavors[item.flavor] = [item]

            if not(available_flavors and len([val for lst in available_flavors.values() for val in lst]) >= 3) :
                print("You need at least three flavors to make a potion!")
                main.s_input("\nPress enter/return ")

                return

            while len(chosen_ingredients) != 3:
                available_flavors = {}

                for item in inventory['misc']:
                    if isinstance(item, Ingredient) :
                        if item.flavor in available_flavors:
                            available_flavors[item.flavor].append(item)

                        else:
                            available_flavors[item.flavor] = [item]

    print("Flavors in your inventory: ")

                list_flavors = sorted(list(available_flavors.keys()))

                for num, flavor in enumerate(list_flavors) :
                    print(f"      [{num + 1}] {flavor.title()}")

                while True:
                    chosen = main.s_input('Input [#] (or type "exit"): ').lower()

                    try:
                        chosen = available_flavors[list_flavors[int(chosen) - 1]]

                    except(IndexError, ValueError):
                        if chosen in ['e', 'x', 'exit', 'b', 'back']:
                            return

                        continue

                    chosen_ingredient = self.choose_ingredients(chosen)
                    chosen_ingredients.append(chosen_ingredient)

                    print('-' * save_load.divider_size)
                    print(f"Added a {chosen_ingredient.name} to the mix.")

                    if len(chosen_ingredients) != 3:
                        print(f"{3 - len(chosen_ingredients)} ingredients remaining!")

                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)

                    else:
                        print("All ingredients added! Time to start brewing!")
                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)

                    break

            self.make_potion(chosen_ingredients) */
        }

        private static void ChooseIngredients(List<Ingredient> ingredients)
        {
            /*
            print('-'*save_load.divider_size)
            print(f"'{ingredients[0].flavor.title()}' Ingredients: ")

            for num, ingredient in enumerate(ingredients) :
                print(f"      [{num + 1}] {ingredient.name}")

            while True:
                chosen = main.s_input("Input [#]: ")

                try:
                    chosen = ingredients[int(chosen) - 1]

                except(IndexError, ValueError):
                    continue

                remove_item(chosen.item_id)

                return chosen */
        }
        
        private static void BrewPotion(List<Ingredient> ingredients)
        {
            /*
            flavor_map = {
                "strange": [attract_potion_1, attract_potion_2, attract_potion_3],
                "mystic": [repel_potion_1, repel_potion_2, repel_potion_3],
                "rigid": [missile_potion_1, missile_potion_2, missile_potion_3],
                "flowing": [grenade_potion_1, grenade_potion_2, grenade_potion_3],
                "dark": [greed_potion_1, greed_potion_2, greed_potion_3],
                "natural": [temperance_potion_1, temperance_potion_2, temperance_potion_3],
                "mathematical": [gamecrash_potion, gamecrash_potion, gamecrash_potion]
            }

            added_flavors = [ing.flavor for ing in ingredients]
            chosen_flavor = random.choice(added_flavors)
            chosen_power = added_flavors.count(chosen_flavor)
            chosen_potion = flavor_map[chosen_flavor][chosen_power - 1]

            print("Brewing...")
            sounds.potion_brew.SmartPlay()
            main.smart_sleep(1)
            print("Brewing...")
            sounds.potion_brew.SmartPlay()
            main.smart_sleep(1)
            print("Brewing...")
            sounds.potion_brew.SmartPlay()
            main.smart_sleep(1)

            sounds.unlock_chest.SmartPlay()
            add_item(chosen_potion.item_id)
            print(f"Success! You brewed a {chosen_potion.name}!")
            main.s_input("\nPress enter/return ") */
        }

        public PocketAlchemyLab(string name, string desc, int value, string item_id) : base(name, desc, value, true, CEnums.InvCategory.tools, item_id)
        {

        }
    }

    public class MusicBox : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
            /*
            print(f"Musicbox is currently {'on' if main.party_info['musicbox_isplaying'] else 'off'}")
            print(f"Musicbox is set to {main.party_info['musicbox_mode']}")

            if main.party_info['musicbox_folder']:
                print(f"Musicbox is set to play music from {main.party_info['musicbox_folder']}/")

            else:
                print("Musicbox does not have a directory set")

            self.choose_option() */
        }

        private static void ChooseOption()
        {
            /*
            def choose_option(self) :
                print("-"*save_load.divider_size)
                while True:
                    print("What should you do with the Musicbox?")
                    print(f"      [1] Turn {'off' if main.party_info['musicbox_isplaying'] else 'on'}")
                    print("      [2] Change play order")
                    print("      [3] Set music directory")

                    while True:
                        chosen = main.s_input('Input [#] (or type "exit"): ')

                        if chosen == '1':
                            if main.party_info['musicbox_folder']:
                                main.party_info['musicbox_isplaying'] = not main.party_info['musicbox_isplaying']

                                if main.party_info['musicbox_isplaying']:
                                    pygame.mixer.music.stop()
                                    self.create_process()
                                    main.party_info['musicbox_process'].start()

                                else:
                                    main.party_info['musicbox_process'].terminate()
                                    pygame.mixer.music.play(-1)

                                print("-"*save_load.divider_size)
                                print(f"You turn {'on' if main.party_info['musicbox_isplaying'] else 'off'} the musicbox")
                                main.s_input("\nPress enter/return ")
                                print("-"*save_load.divider_size)

                                break

                            else:
                                print("-"*save_load.divider_size)
                                print("You need to set a music directory first!")
                                main.s_input("\nPress enter/return ")
                                print("-"*save_load.divider_size)

                                break

                        elif chosen == '2':
                            print("-"*save_load.divider_size)
                            self.play_order()
                            print("-"*save_load.divider_size)

                            break

                        elif chosen == '3':
                            print("-"*save_load.divider_size)
                            self.choose_directory()
                            print("-"*save_load.divider_size)

                            break

                        elif chosen in ['e', 'x', 'exit', 'b', 'back']:
                            return */
        }

        private static void CreateMusicProcess()
        {
            /*
            main.party_info['musicbox_process'] = multiprocessing.Process(
                target = self.playlist,
                args = (
                    main.party_info['musicbox_folder'],
                    main.party_info['musicbox_mode']
                )
            ) */
        }

        private static void ChoosePlayOrder()
        {
            /*
            print("Which setting do you want for the musicbox?")
            print("      [1] A->Z")
            print("      [2] Z->A")
            print("      [3] Shuffle")

            while True:
                chosen = main.s_input('Input [#] (or type "back"): ')

                if chosen in ['e', 'x', 'exit', 'b', 'back']:
                    return

                elif chosen == '1':
                    main.party_info['musicbox_mode'] = "A->Z"
                    print("-"*save_load.divider_size)
                    print("Musicbox set to play from A->Z.")

                elif chosen == '2':
                    main.party_info['musicbox_mode'] = "Z->A"
                    print("-"*save_load.divider_size)
                    print("Musicbox set to play from Z->A.")

                elif chosen == '3':
                    main.party_info['musicbox_mode'] = "shuffle"
                    print("-"*save_load.divider_size)
                    print("Musicbox set to shuffle.")

                else:
                    continue

                if main.party_info['musicbox_isplaying']:
                    print("You'll need to restart your musicbox to apply this change.")

                main.s_input("\nPress enter/return ")

                return */
        }

        private static void ChooseMusicDirectory()
        {
            /*
            while True:
                folder = main.s_input("Type the directory path, type 'explore', or type 'back': ")

                if folder.lower() == "explore":
                    print("-" * save_load.divider_size)
                    folder = self.select_root()

                    if not folder:
                        print("-" * save_load.divider_size)
                        continue

                elif folder.lower() in ['e', 'x', 'exit', 'b', 'back']:
                    return

                else:
                    if not os.path.isdir(folder):
                        print("-" * save_load.divider_size)
                        print(f"{folder} is not a valid directory")
                        main.s_input("\nPress enter/return ")
                        print("-" * save_load.divider_size)
                        continue

                print("-" * save_load.divider_size)
                for file in os.listdir(folder):
                    if any(map(file.endswith, ['.ogg', 'flac', '.mp3', '.wav'])) :

                        main.party_info['musicbox_folder'] = folder
                        print(f"Directory set to {folder}")

                        if main.party_info['musicbox_isplaying']:
                            print("You'll need to restart your musicbox to apply this change.")

                        main.s_input("\nPress enter/return ")

                        return

                else:
                    print("Couldn't find any .ogg, .flac, .mp3, or .wav files in that directory.")
                    while True:
                        y_n = main.s_input("Select a different directory? | Yes or No: ")

                        if y_n.startswith("y"):
                            print("-" * save_load.divider_size)
                            break

                        elif y_n.startswith("n"):
                            return */
        }
        
        private static void SelectRoot()
        {
            /*
            drive_list = []
            for drive in range(ord('A'), ord('N')):
                if os.path.exists(chr(drive) + ':'):
                    drive_list.append(chr(drive))

            if len(drive_list) > 1:
                while True:
                    print("Select a drive: ")

                    for num, x in enumerate(drive_list) :
                        print(f"      [{num + 1}] {x}:/")

                    while True:
                        chosen = main.s_input("Input [#] (or type back): ")

                        try:
                            chosen = drive_list[int(chosen) - 1]

                        except(IndexError, ValueError):
                            if chosen in ['e', 'x', 'exit', 'b', 'back']:
                                return False

                            else:
                                continue

                        return self.file_explorer(f"{chosen}:")

            else:
                return self.file_explorer(f"{drive_list[0]}:") */
        }
        
        private static void FileExplorer(string root)
        {
            /*
            current_path = [root]

            while True:
                print("-"*save_load.divider_size)
                available_dirs = []

                print(f"Current Path: {'/'.join(current_path)}/")
                for file in os.listdir(f"{'/'.join(current_path)}/"):
                    if os.path.isdir('/'.join([x for x in current_path] + [file])):
                        available_dirs.append(file)
                        print(f"      [{len(available_dirs)}] {file}")

                    else:
                        print(f"          {file}")

                while True:
                    chosen = main.s_input('Input [#], type "choose" to choose this folder, or type "back": ').lower()

                    try:
                        chosen = available_dirs[int(chosen) - 1]
                        current_path.append(chosen)

                        break

                    except (IndexError, ValueError):
                        if chosen == "choose":
                            return '/'.join(current_path)

                        elif chosen in ['e', 'x', 'exit', 'b', 'back']:
                            if len(current_path) > 1:
                                current_path.pop()
                                break

                            else:
                                return False */
        }
        
        private static void RunPlaylist(string folder)
        {
            /*
            import pygame

            pygame.mixer.pre_init()
            pygame.mixer.init()

            song_list = []

            for file in os.listdir(folder):
                if any(map(file.endswith, ['.ogg', 'flac', '.mp3', '.wav'])) :
                    song_list.append(file)

            if mode == 'A->Z':
                song_list = sorted(song_list)

            if mode == 'Z->A':
                song_list = sorted(song_list, reverse= True)

            if mode == 'shuffle':
                random.shuffle(song_list)

            for song in song_list:
                try:
                    pygame.mixer.music.load(f"{folder}/{song}")
                    pygame.mixer.music.SmartPlay()

                    while pygame.mixer.music.get_busy():
                        pass

                except pygame.error:
                    pass */
        }

        public MusicBox(string name, string desc, int value, string item_id) : base(name, desc, value, true, CEnums.InvCategory.tools, item_id)
        {

        }
    }
}
