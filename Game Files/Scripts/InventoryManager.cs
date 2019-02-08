using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    public static class InventoryManager
    {
        private static Dictionary<CEnums.InvCategory, List<string>> inventory = new Dictionary<CEnums.InvCategory, List<string>>()
        {
            { CEnums.InvCategory.quest, new List<string>() { } },
            { CEnums.InvCategory.consumables, new List<string>() { } },
            { CEnums.InvCategory.weapons, new List<string>() { } },
            { CEnums.InvCategory.armor, new List<string>() { } },
            { CEnums.InvCategory.tools, new List<string>() { } },
            { CEnums.InvCategory.accessories, new List<string>() { } },
            { CEnums.InvCategory.misc, new List<string>() {} }
        };

        private static Dictionary<string, Dictionary<CEnums.EquipmentType, string>> equipment = new Dictionary<string, Dictionary<CEnums.EquipmentType, string>>()
        {
             {
                "_player", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_solou", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_chili", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_chyme", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_storm", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_parsto", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_adorine", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_kaltoh", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.armor, "no_armor" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },
        };

        private readonly static Dictionary<CEnums.EquipmentType, string> default_equip_map = new Dictionary<CEnums.EquipmentType, string>()
        {
            { CEnums.EquipmentType.accessory, "no_access" },
            { CEnums.EquipmentType.armor, "no_armor" },
            { CEnums.EquipmentType.weapon, "weapon_fists" }
        };

        /* =========================== *
         *    COLLECTION RETRIEVERS    *
         * =========================== */
        public static Dictionary<CEnums.InvCategory, List<Item>> GetInventory()
        {
            // We have to convert the inventory from a list of ItemIDs into a list of Items.
            // Storing only the ItemIDs instead of the full items makes it much simpler to
            // serialize and deserialize the inventory when saving.
            Dictionary<CEnums.InvCategory, List<Item>> new_inventory = new Dictionary<CEnums.InvCategory, List<Item>>();

            foreach (KeyValuePair<CEnums.InvCategory, List<string>> kvp in inventory)
            {
                new_inventory[kvp.Key] = kvp.Value.Select(x => ItemManager.FindItemWithID(x)).ToList();
            }

            // It's important to note that this does NOT return the inventory! 
            // It returns a completely new object - modifying this value will
            // NOT modify the actual inventory! 
            // To modify the real inventory, use AddItemToInventory() and RemoveItemFromInventory().
            return new_inventory;
        }

        public static Dictionary<CEnums.EquipmentType, Equipment> GetEquipment(string pcu_id)
        {
            // The equipment dictionary only stores ItemIDs, not actual items. So we have to convert
            // them into real items before we return the dictionary
            Dictionary<CEnums.EquipmentType, Equipment> real_equipped = new Dictionary<CEnums.EquipmentType, Equipment>()
            {
                { CEnums.EquipmentType.weapon, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.weapon]) as Equipment },
                { CEnums.EquipmentType.armor, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.armor]) as Equipment },
                { CEnums.EquipmentType.accessory, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.accessory]) as Equipment }
            };

            // It's important to note that this does NOT return the equipment! 
            // It returns a completely new object - modifying this value will
            // NOT modify the actual equipment! 
            // To modify the real equipment, use EquipItem() and UnequipItem().
            return real_equipped;
        }

        /* =========================== *
         *           METHODS           *
         * =========================== */
        public static void AddItemToInventory(string item_id)
        {
            // Adds the item_id to the inventory
            CEnums.InvCategory item_cat = ItemManager.FindItemWithID(item_id).Category;
            inventory[item_cat].Add(item_id);
        }

        public static void RemoveItemFromInventory(string item_id)
        {
            // Removes the item_id from the inventory
            CEnums.InvCategory item_cat = ItemManager.FindItemWithID(item_id).Category;
            inventory[item_cat].Remove(item_id);
        }

        public static void EquipItem(PlayableCharacter equipper, string item_id)
        {
            // Equips the item_id to equipper
            CEnums.EquipmentType equip_type = (ItemManager.FindItemWithID(item_id) as Equipment).EquipType;

            if (GetEquipment(equipper.UnitID)[equip_type].ItemID != default_equip_map[equip_type])
            {
                AddItemToInventory(GetEquipment(equipper.UnitID)[equip_type].ItemID);
            }

            equipment[equipper.UnitID][equip_type] = item_id;
            RemoveItemFromInventory(item_id);
        }

        public static void UnequipItem(PlayableCharacter unequipper, string item_id)
        {
            // Unequips the item_id from the unequipper
            CEnums.EquipmentType equip_type = (ItemManager.FindItemWithID(item_id) as Equipment).EquipType;
            equipment[unequipper.UnitID][equip_type] = default_equip_map[equip_type];
            AddItemToInventory(item_id);
        }

        public static void PickInventoryCategory()
        {
            while (true)
            {
                Console.WriteLine("Your Inventory: ");
                Console.WriteLine("      [1] Armor");
                Console.WriteLine("      [2] Weapons");
                Console.WriteLine("      [3] Accessories");
                Console.WriteLine("      [4] Consumables");
                Console.WriteLine("      [5] Tools");
                Console.WriteLine("      [6] Quest Items");
                Console.WriteLine("      [7] Miscellaneous");
                Console.WriteLine("      [8] View Equipment");
                Console.WriteLine("      [9] View Quests");

                while (true)
                {
                    string chosen = CMethods.Input("Input [#] (or type 'exit'): ").ToLower();
                    CEnums.InvCategory category;

                    if (CMethods.IsExitString(chosen))
                    {
                        return;
                    }

                    else if (chosen == "1")
                    {
                        category = CEnums.InvCategory.armor;
                    }

                    else if (chosen == "2")
                    {
                        category = CEnums.InvCategory.weapons;
                    }

                    else if (chosen == "3")
                    {
                        category = CEnums.InvCategory.accessories;
                    }

                    else if (chosen == "4")
                    {
                        category = CEnums.InvCategory.consumables;
                    }

                    else if (chosen == "5")
                    {
                        category = CEnums.InvCategory.tools;
                    }

                    else if (chosen == "6")
                    {
                        category = CEnums.InvCategory.quest;
                    }

                    else if (chosen == "7")
                    {
                        category = CEnums.InvCategory.misc;
                    }

                    else if (chosen == "8")
                    {
                        // Equipped items aren't actually stored in the inventory, so they need their own function to handle them
                        PickEquipmentItem();
                        break;
                    }

                    else if (chosen == "9")
                    {
                        // Quests have their own function, because they aren't actually instances of the Item class
                        ViewQuests();
                        break;
                    }

                    else
                    {
                        continue;
                    }

                    if (GetInventory()[category].Any())
                    {
                        PickInventoryItem(category, false);
                        break;
                    }

                    else
                    {
                        CMethods.PrintDivider();
                        Console.WriteLine($"Your part has no {CEnums.EnumToString(category)}.");
                        CMethods.PressEnterReturn();
                        CMethods.PrintDivider();
                        break;
                    }
                }
            }
        }

        public static void PickInventoryItem(CEnums.InvCategory category, bool selling)
        {
            // Select an object to interact with in your inventory
            // If "selling == True" that means that items are being sold, and not used.

            while (true)
            {
                CMethods.PrintDivider();
                List<string> item_ids = DisplayInventory(category, selling);

                while (true)
                {
                    string chosen = CMethods.Input("Input [#] (or type 'exit'): ").ToLower();

                    try
                    {
                        chosen = item_ids[int.Parse(chosen) - 1];
                    }

                    catch (Exception ex)
                    {
                        if (ex is FormatException || ex is ArgumentOutOfRangeException)
                        {
                            if (CMethods.IsExitString(chosen))
                            {
                                CMethods.PrintDivider();
                                return;
                            }

                            continue;
                        }

                        throw;
                    }

                    // If you're selling items at a general store, you have to call a different function
                    if (selling)
                    {
                        SellItem(chosen);

                        if (!GetInventory()[category].Any(x => x.IsImportant))
                        {
                            return;
                        }
                    }

                    else
                    {
                        PickInventoryAction(chosen);

                        if (!GetInventory()[category].Any())
                        {
                            return;
                        }
                    }

                    break;
                }
            }
        }

        public static List<string> DisplayInventory(CEnums.InvCategory category, bool selling)
        {
            List<string> id_inventory = GetInventory()[category].Select(x => x.ItemID).ToList();
            List<Tuple<string, string, int>> quantity_inv = new List<Tuple<string, string, int>>();

            // This creates a tuple of every item in the inventory and its quantity, and adds it to quantity_inv
            id_inventory.Distinct().ToList().ForEach(x => quantity_inv.Add(new Tuple<string, string, int>(ItemManager.FindItemWithID(x).Name, x, id_inventory.Count(y => y == x))));
            
            if (selling)
            {
                /*
                List<Tuple<string, int>> sellable_inv = quantity_inv.Where(x => !ItemManager.FindItemWithID(x.Item1).IsImportant).ToList();

                int padding;

                try
                {
                    padding = sellable_inv.Select(x => $"{x.Item1} x {x.Item2}".Length).Max();
                } 

                catch (Exception ex)
                {
                    if (ex is ArgumentException)
                    {
                        padding = 1;
                    }

                    throw;
                }

                int extra_pad = sellable_inv.Select(x => x.Item1);
                /*
                sellable_inv = [it for it in quantity_inv if not find_item_with_id(it[1]).imp]

                try:
                    padding = len(max([it2[0] + f" x {it2[2]}" for it2 in sellable_inv], key= len))

                except ValueError:
                    padding = 1

                extra_pad = len(str(len([it3[0] for it3 in sellable_inv]) + 1))

                print(f'{vis_cat}:')

                highest_charisma = max([pcu.attributes['cha'] for pcu in [units.player,
                                                                            units.solou,
                                                                            units.chili,
                                                                            units.chyme,
                                                                            units.adorine,
                                                                            units.parsto]]) - 1

                for num, b in enumerate(sellable_inv) :
                    sell_value = find_item_with_id(b[1]).value//5
                    modified_value = math.ceil(max([sell_value * (1 + 0.01 * highest_charisma), sell_value * 2]))

                    fp = '-'*(padding - (len(b[0]) + len(f" x {b[2]}")) + (extra_pad - len(str(num + 1))))
                    print(f"      [{num + 1}] {b[0]} x {b[2]} {fp}--> {modified_value} GP each")

                return [x[1] for x in sellable_inv] */

                return id_inventory;
            }

            else
            {
                Console.WriteLine($"{CEnums.EnumToString(category)}: ");

                int counter = 0;
                foreach (Tuple<string, string, int> item in quantity_inv)
                {
                    Console.WriteLine($"      [{counter + 1}] {item.Item1} x {item.Item3}");
                    counter++;
                }

                return quantity_inv.Select(x => x.Item2).ToList();
            }
        }

        public static void PickInventoryAction(string item_id)
        {
            Item this_item = ItemManager.FindItemWithID(item_id);

            // Loop while the item is in the inventory
            while (true)
            {
                string action;
                if (this_item is Equipment)
                {
                    // You equip weapons/armor/accessories
                    action = "Equip";
                }

                else
                {
                    // You use other items
                    action = "Use";
                }

                CMethods.PrintDivider();
                Console.WriteLine($"What should your party do with the {this_item.Name}? ");
                Console.WriteLine($"      [1] {action}");
                Console.WriteLine("      [2] Read Description");
                Console.WriteLine("      [3] Drop");
                
                while (true)
                {
                    string chosen = CMethods.Input("Input [#] (or type 'exit'): ").ToLower();


                    if (CMethods.IsExitString(chosen))
                    {
                        return;
                    }

                    else if (chosen == "1")
                    {
                        // Items of these classes require a target to be used, so we have to acquire a target first
                        if (this_item is Equipment || this_item is HealthManaPotion || this_item is StatusPotion)
                        {
                            UnitManager.player.PlayerGetTarget(new List<Monster>(), $"Who should {action} the {this_item.Name}?", true, false, true, false);
                            CMethods.PrintDivider();
                            this_item.UseItem(UnitManager.player.CurrentTarget as PlayableCharacter);
                        }

                        // Other items can just be used normally
                        else
                        {
                            CMethods.PrintDivider();
                            this_item.UseItem(UnitManager.player);
                        }

                        return;
                    }

                    else if (chosen == "2")
                    {
                        // Display the item description
                        CMethods.PrintDivider();
                        Console.WriteLine($"Description for '{this_item.Name}': \n");
                        Console.WriteLine(this_item.Description);
                        CMethods.PressEnterReturn();

                        break;
                    }

                    else if (chosen == "3")
                    {
                        CMethods.PrintDivider();

                        // You can't throw away important/essential items, such as tools and quest items.
                        // This is to prevent the game from becoming unwinnable.
                        if (this_item.IsImportant)
                        {
                            Console.WriteLine("Essential Items cannot be thrown away.");
                            CMethods.PressEnterReturn();
                        }

                        else
                        {
                            while (true)
                            {
                                string yes_or_no = CMethods.Input($"Throw away the {this_item.Name}? | Yes or No: ").ToLower();

                                if (CMethods.IsYesString(yes_or_no))
                                {
                                    RemoveItemFromInventory(this_item.ItemID);
                                    Console.WriteLine($"You toss the {this_item.Name} aside and continue on your journey.");
                                    CMethods.PressEnterReturn();

                                    return;
                                }

                                else if (CMethods.IsNoString(yes_or_no))
                                {
                                    Console.WriteLine($"You decide to keep the {this_item.Name}.");
                                    CMethods.PressEnterReturn();

                                    return;
                                }
                            }
                        }
                    }
                }
            }
        }

        public static void SellItem(string item_id)
        {
            /*
            // Trade player-owned objects for money (GP)
            item = find_item_with_id(item_id)

            print('-'*save_load.divider_size)

            if hasattr(item, "ascart") :
                print(ascii_art.item_sprites[item.ascart])

            for x in main.chop_by_79(item.desc):
                print(x)

            print('-'*save_load.divider_size)

            highest_charisma = max([pcu.attributes['cha'] for pcu in [units.player,
                                                                      units.solou,
                                                                      units.chili,
                                                                      units.chyme,
                                                                      units.adorine,
                                                                      units.parsto]]) - 1

            modified_value = math.ceil(max([(item.value//5)*(1 + 0.01*highest_charisma), item.value*2]))

            while True:
                y_n = main.s_input(f'Sell the {item.name} for {modified_value} GP? | Y/N: ').lower()

                if y_n.startswith('y'):
                    remove_item(item.item_id)
                    main.party_info['gp'] += modified_value
                    print(f'The shopkeeper takes the {item.name} and gives you {modified_value} GP.')
                    main.s_input('\nPress enter/return ')

                    return

                elif y_n.startswith('n'):
                    return */
        }

        public static void PickEquipmentItem()
        {
            /*
            units.player.choose_target("Choose party member to view equipment for:", ally = True, enemy = False)

            print('-' * save_load.divider_size)
            while True:
                p_equip = equipped[units.player.target.name if units.player.target != units.player else 'player']

                print(f"""{units.player.target.name}'s Equipped Items:
              [1] Weapon---- > {p_equip['weapon'].name}
              [2] Head ------> {p_equip['head'].name}
              [3] Body ------> {p_equip['body'].name}
              [4] Legs ------> {p_equip['legs'].name}
              [5] Accessory -> {p_equip['access'].name}""")

                while True:
                    selected = main.s_input('Input [#] (or type "back"): ').lower()

                    if selected in ['e', 'x', 'exit', 'b', 'back']:
                        print('-'*save_load.divider_size)
                        return

                    elif selected == '1':
                        selected = p_equip['weapon']

                    elif selected == '2':
                        selected = p_equip['head']

                    elif selected == '3':
                        selected = p_equip['body']

                    elif selected == '4':
                        selected = p_equip['legs']

                    elif selected == '5':
                        selected = p_equip['access']

                    else:
                        continue

                    if selected.item_id in ["no_head",
                                            "no_body",
                                            "no_legs",
                                            "no_access"]:

                        print('-'*save_load.divider_size)
                        print(f"{units.player.target.name} doesn't have anything equipped in that slot.")
                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)

                        break

                    print('-'*save_load.divider_size)
                    manage_equipped_2(selected)
                    print('-'*save_load.divider_size)

                    break */
        }

        public static void PickEquipmentAction(Equipment item)
        {
            /*
            global equipped

            while True:
                print(f"""What should {units.player.target.name} do with their {selected.name}?
              [1] Unequip
              [2] Read Description""")

                while True:
                    action = main.s_input('Input [#] (or type "back"): ').lower()

                    if action == '1':
                        if selected.item_id == "weapon_fist":
                            print('-'*save_load.divider_size)
                            print("Removing those would be difficult without causing damage.")
                            main.s_input("\nPress enter/return ")
                            print('-'*save_load.divider_size)

                            break

                        else:
                            unequip_item(selected.item_id, units.player.target)
                            print('-'*save_load.divider_size)
                            print(f'{units.player.target.name} unequips the {selected.name}.')
                            main.s_input("\nPress enter/return ")

                        return

                    elif action == '2':
                        print('-'*save_load.divider_size)

                        if hasattr(selected, "ascart") :
                            print(ascii_art.item_sprites[selected.ascart])

                        print(selected.desc)
                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)

                        break

                    elif action in ['e', 'x', 'exit', 'b', 'back']:
                        return */
        }

        public static void ViewQuests()
        {
            /*
            print('-'*save_load.divider_size)
            while True:
                fizz = True
                choice = main.s_input('View [f]inished or [a]ctive quests? | Input [Letter] (or type "back"): ').lower()

                print('-'*save_load.divider_size)
                if choice.startswith('f'):  // Finished Quests
                    dia_ = [x for x in dialogue.all_dialogue if isinstance(x, dialogue.Quest) and x.finished]

                elif choice.startswith('a'):
                            dia_ = [x for x in dialogue.all_dialogue if isinstance(x, dialogue.Quest) and not x.finished and x.started]

                elif choice in ['e', 'x', 'exit', 'b', 'back']:
                            return

                        else:
                            continue

                        if dia_:
                            while fizz:
                                if choice.startswith("f"):
                                    print("Finished:")

                                else:
                                    print("Active:")

                                for num, x in enumerate(dia_) :
                                    print(f'      [{num + 1}] {x.name}')

                                while True:
                                    quest = main.s_input('Input [#] (or type "back"): ').lower()

                                    try:
                                        quest = dia_[int(quest) - 1]

                                    except(IndexError, ValueError):
                                        if quest in ['e', 'x', 'exit', 'b', 'back']:
                                            fizz = False  // Break the loop twice
                                            break

                                        continue

                                    print('-'*save_load.divider_size)
                                    print(f"QUEST NAME: {quest.name}")
                                    print(f"GIVEN BY: {quest.q_giver}")

                                    for x in main.chop_by_79(quest.dialogue):
                                        print(x)

                                    main.s_input("\nPress enter/return ")
                                    print('-'*save_load.divider_size)

                                    break

                            print('-'*save_load.divider_size)

                        else:
                            print(f'Your party has no {"active" if choice.startswith("a") else "finished"} quests!')
                            main.s_input('\nPress enter/return ')
                            print('-'*save_load.divider_size) */
        }
    }
}
