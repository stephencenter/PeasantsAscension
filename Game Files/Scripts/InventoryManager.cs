using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    class InventoryManager
    {
        private Dictionary<string, List<dynamic>> inventory = new Dictionary<string, List<dynamic>>()
        {
            { "q_items", new List<dynamic>() { } },
            { "consumables",  new List<dynamic>() { } },
            { "weapons",  new List<dynamic>() { } },
            { "armor",  new List<dynamic>() { } },
            { "tools",  new List<dynamic>() { } },
            { "access",  new List<dynamic>() { } },
            { "misc",  new List<dynamic>() { } }
        };

        private Dictionary<string, Dictionary<CEnums.EquipmentType, string>> equipment = new Dictionary<string, Dictionary<CEnums.EquipmentType, string>>()
        {
             {
                "_player", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.head, "no_head" },
                     { CEnums.EquipmentType.body, "no_body" },
                     { CEnums.EquipmentType.legs, "no_legs" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_solou", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.head, "no_head" },
                     { CEnums.EquipmentType.body, "no_body" },
                     { CEnums.EquipmentType.legs, "no_legs" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_chili", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.head, "no_head" },
                     { CEnums.EquipmentType.body, "no_body" },
                     { CEnums.EquipmentType.legs, "no_legs" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_chyme", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.head, "no_head" },
                     { CEnums.EquipmentType.body, "no_body" },
                     { CEnums.EquipmentType.legs, "no_legs" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_storm", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.head, "no_head" },
                     { CEnums.EquipmentType.body, "no_body" },
                     { CEnums.EquipmentType.legs, "no_legs" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_parsto", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.head, "no_head" },
                     { CEnums.EquipmentType.body, "no_body" },
                     { CEnums.EquipmentType.legs, "no_legs" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },

             {
                "_adorine", new Dictionary<CEnums.EquipmentType, string>()
                 {
                     { CEnums.EquipmentType.weapon, "weapon_fists" },
                     { CEnums.EquipmentType.head, "no_head" },
                     { CEnums.EquipmentType.body, "no_body" },
                     { CEnums.EquipmentType.legs, "no_legs" },
                     { CEnums.EquipmentType.accessory, "no_access" }
                 }
             },
        };

        public Dictionary<string, List<dynamic>> GetInventory()
        {
            return inventory;
        }

        public Dictionary<CEnums.EquipmentType, dynamic> GetEquipment(string pcu_id)
        {
            // The equipment dictionary only stores ItemIDs, not actual items. So we have to convert
            // them into real items before we return the dictionary
            Dictionary<CEnums.EquipmentType, dynamic> real_equipped = new Dictionary<CEnums.EquipmentType, dynamic>()
            {
                { CEnums.EquipmentType.weapon, FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.weapon]) },
                { CEnums.EquipmentType.head, FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.head]) },
                { CEnums.EquipmentType.body, FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.body]) },
                { CEnums.EquipmentType.legs, FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.legs]) },
                { CEnums.EquipmentType.accessory, FindItemWithID(equipment[pcu_id][CEnums.EquipmentType.accessory]) }
            };

            return real_equipped;
        }

        public void AddItemToInventory(string item_id)
        {
            var new_item = FindItemWithID(item_id);
            GetInventory()[new_item.Category].Add(new_item);
        }

        public void RemoveItemFromInventory(string item_id)
        {
            var deleted_item = GetInventory()[FindItemWithID(item_id).Category].Single(x => x.ItemID == item_id);
            GetInventory()[FindItemWithID(item_id).Category].Remove(deleted_item);
        }

        public Item FindItemWithID(string item_id)
        {
            ItemManager item_manager = new ItemManager();
            return item_manager.GetItemList().Single(x => x.ItemID == item_id);
        }
    }
}
