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
            { CEnums.InvCategory.misc, new List<string>() { } }
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

            return new_inventory;
        }

        public static Dictionary<CEnums.EquipmentType, Item> GetEquipment(string pcu_id)
        {
            // The equipment dictionary only stores ItemIDs, not actual items. So we have to convert
            // them into real items before we return the dictionary
            Dictionary<CEnums.EquipmentType, Item> real_equipped = new Dictionary<CEnums.EquipmentType, Item>()
            {
                { CEnums.EquipmentType.weapon, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.weapon]) },
                { CEnums.EquipmentType.armor, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.armor]) },
                { CEnums.EquipmentType.accessory, ItemManager.FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.accessory]) }
            };

            return real_equipped;
        }

        /* =========================== *
         *           METHODS           *
         * =========================== */
        public static void AddItemToInventory(string item_id)
        {
            Item new_item = ItemManager.FindItemWithID(item_id);
            GetInventory()[new_item.Category].Add(new_item);\
        }

        public static void RemoveItemFromInventory(string item_id)
        {
            Item deleted_item = GetInventory()[ItemManager.FindItemWithID(item_id).Category].First(x => x.ItemID == item_id);
            GetInventory()[ItemManager.FindItemWithID(item_id).Category].Remove(deleted_item);
        }

        public static void PickInventoryCategory()
        {
            /*
            global inventory
            while True:
                print("""Inventory Categories:
              [1] Armor
              [2] Weapons
              [3] Accessories
              [4] Consumables
              [5] Tools
              [6] Quest Items
              [7] Misc. Items
              [8] Equipped Items
              [9] Quests""")
                while True:
                    cat = main.s_input('Input [#] (or type "exit"): ').lower()

                    if cat in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    elif cat == '1':
                        cat = 'armor'
                        vis_cat = 'Armor'
                    elif cat == '2':
                        cat = 'weapons'
                        vis_cat = 'Weapons'
                    elif cat == '3':
                        cat = 'access'
                        vis_cat = 'Accessories'
                    elif cat == '4':
                        cat = 'consumables'
                        vis_cat = 'Consumables'
                    elif cat == '5':
                        cat = 'tools'
                        vis_cat = 'Tools'
                    elif cat == '6':
                        cat = 'q_items'
                        vis_cat = 'Quest Items'
                    elif cat == '7':
                        cat = 'misc'
                        vis_cat = 'Misc. Items'
                    elif cat == '8':
                        cat = 'equipped_items'
                        vis_cat = 'Equipped Items'
                    elif cat == '9':
                        cat = 'quests'
                        vis_cat = 'Quests'

                    else:
                        continue

                    if cat in inventory:
                        if inventory[cat]:
                            if cat not in ['weapons', 'armor', 'access']:
                                pick_item(cat, vis_cat)
                                print('-'*save_load.divider_size)

                            else:
                                if [x for x in inventory[cat]]:
                                    pick_item(cat, vis_cat)
                                    print('-'*save_load.divider_size)

                                else:
                                    print('-'*save_load.divider_size)
                                    print(f'Your party has no {vis_cat}.')
                                    main.s_input("\nPress enter/return ")
                                    print('-'*save_load.divider_size)

                            break

                        else:
                            print('-'*save_load.divider_size)
                            print(f'Your party has no {vis_cat}.')
                            main.s_input("\nPress enter/return ")
                            print('-'*save_load.divider_size)
                            break

                    elif cat == 'equipped_items':
                        pick_item(cat, vis_cat)
                        break

                    if cat == 'quests' and[x for x in dialogue.all_dialogue if isinstance(x, dialogue.Quest) and x.started]:
                        pick_item(cat, vis_cat)
                        break

                    else:
                        print('-'*save_load.divider_size)
                        print("Your party has no active or completed quests.")
                        main.s_input("\nPress enter/return ")
                        print('-'*save_load.divider_size)
                        break */
        }
            
        public static void PickInventoryItem(CEnums.InvCategory category, bool selling = false)
        {
            /*
            // Select an object to interact with in your inventory
            // If "selling == True" that means that items are being sold, and not used.
            def pick_item(cat, vis_cat, selling= False):
                while True:
                    // Quests have their own function, because they aren't actually instances of the Item class
                    if cat == 'quests':
                        view_quests()
                        return

                    // Equipped items aren't actually stored in the inventory, so they need their own function to handle them
                    if cat == 'equipped_items':
                        manage_equipped()
                        return

                    // The code that prints the inventory is kind of complicated so it's located in another function
                    print('-'*save_load.divider_size)
                    item_ids = print_inventory(cat, vis_cat, selling)

                    while True:
                        chosen = main.s_input('Input [#] (or type "back"): ').lower()
                        try:
                            item_id = item_ids[int(chosen) - 1]

                        except(IndexError, ValueError):
                            if chosen in ['e', 'x', 'exit', 'b', 'back']:
                                return

                            continue

                        // If you're selling items at a general store, you have to call a different function
                        if selling:
                            sell_item(item_id)

                            if not any([not i.imp for i in inventory[cat]]):
                                return

                        else:
                            pick_action(item_id)

                            if not inventory[cat]:
                                return

                        break */
        }

        public static void DisplayInventory(CEnums.InvCategory category, bool selling)
        {
            /*
            // Count the number of each item in the player's inventory, and display it alongside one copy of each item
            def print_inventory(cat, vis_cat, selling):
                    quantity_inv = []

                        temp_inv = []
                    for item_x in inventory[cat]:
                        if item_x.item_id not in temp_inv:
                            temp_inv.append(item_x.item_id)

                    for item_y in temp_inv:
                        quantity_inv.append((find_item_with_id(item_y).name,
                                             item_y,
                                             sum(i.item_id == item_y for i in inventory[cat])))

                    if not selling:
                        print(f"{vis_cat}: ")
                        for x, y in enumerate(quantity_inv) :
                            print(f'      [{x + 1}] {y[0]} x {y[2]}')

                        return [x[1] for x in quantity_inv]

                    else:
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
        }

        public static void PickInventoryAction(string item_id)
        {
            /*
            global inventory

            item = find_item_with_id(item_id)

            // Loop while the item is in the inventory
            while True:
                if any([isinstance(item, class_) for class_ in [Weapon, Armor, Accessory]]):
                    // You equip weapons/armor/accessories
                    use_equip = 'Equip'

                else:
                    // You use other items
                    use_equip = 'Use'

                print('-'*save_load.divider_size)
                action = main.s_input(f"""What should your party do with the {item.name}?
     [1] {use_equip}
     [2] Read Description
     [3] Drop
Input[#] (or type "back"): """)

                if action == '1':
                    // Items of these classes require a target to be used, so we have to acquire a target first
                    if any([isinstance(item, class_) for class_ in [Accessory, Armor, HealthManaPotion, Weapon, StatusPotion]]):
                        units.player.choose_target(f"Who should {use_equip} the {item.name}?", ally = True, enemy = False)


                      print('-' * save_load.divider_size)

                      item.use_item(units.player.target)

                        return

                    // Other items can just be used normally
                    else:
                        print('-' * save_load.divider_size)

                      item.use_item(units.player)

                        return

                elif action == '2':
                    // Display the item description
                    print('-' * save_load.divider_size)

                  print(f'-{str(item.name).upper()}-')

                    if hasattr(item, "ascart"):
                        print(ascii_art.item_sprites[item.ascart])

                    for x in main.chop_by_79(item.desc):
                        print(x)


                  main.s_input("\nPress enter/return ")


              elif action == '3':
                    print('-' * save_load.divider_size)

                    // You can't throw away important/essential items, such as one-of-a-kind tools and quest items.
                    // This is to prevent the game from becoming unwinnable.
                    if item.imp:
                        print('Essential Items cannot be thrown away.')

                      main.s_input("\nPress enter/return ")

                    else:
                        while True:
                            y_n = main.s_input(f'Should you really get rid of the {item.name}? | Y/N: ').lower()

                            if y_n.startswith('y'):
                                remove_item(item.item_id)


                              print(f'You toss the {item.name} aside and continues on your journey.')

                              main.s_input("\nPress enter/return ")

                                return

                            elif y_n.startswith('n'):
                                print(f'Your party decides to keep the {item.name} with them.')

                              main.s_input("\nPress enter/return ")

                                break

                elif action in ['e', 'x', 'exit', 'b', 'back']:
                    return */

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

        public static void ManageEquipment()
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

                    break


        def manage_equipped_2(selected):
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
                        return


        def view_quests():
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
