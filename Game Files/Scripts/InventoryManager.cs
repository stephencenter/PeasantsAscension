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

        private Dictionary<string, Dictionary<CEnums.EquipmentType, dynamic>> equipped = new Dictionary<string, Dictionary<CEnums.EquipmentType, dynamic>>()
        {
             {
                "_player", new Dictionary<CEnums.EquipmentType, dynamic>()
                 {
                     { CEnums.EquipmentType.weapon, null },
                     { CEnums.EquipmentType.head, null },
                     { CEnums.EquipmentType.body, null },
                     { CEnums.EquipmentType.legs, null },
                     { CEnums.EquipmentType.accessory, null }
                 }
             },

             {
                "_solou", new Dictionary<CEnums.EquipmentType, dynamic>()
                 {
                     { CEnums.EquipmentType.weapon, null },
                     { CEnums.EquipmentType.head, null },
                     { CEnums.EquipmentType.body, null },
                     { CEnums.EquipmentType.legs, null },
                     { CEnums.EquipmentType.accessory, null }
                 }
             },

             {
                "_chili", new Dictionary<CEnums.EquipmentType, dynamic>()
                 {
                     { CEnums.EquipmentType.weapon, null },
                     { CEnums.EquipmentType.head, null },
                     { CEnums.EquipmentType.body, null },
                     { CEnums.EquipmentType.legs, null },
                     { CEnums.EquipmentType.accessory, null }
                 }
             },

             {
                "_chyme", new Dictionary<CEnums.EquipmentType, dynamic>()
                 {
                     { CEnums.EquipmentType.weapon, null },
                     { CEnums.EquipmentType.head, null },
                     { CEnums.EquipmentType.body, null },
                     { CEnums.EquipmentType.legs, null },
                     { CEnums.EquipmentType.accessory, null }
                 }
             },

             {
                "_storm", new Dictionary<CEnums.EquipmentType, dynamic>()
                 {
                     { CEnums.EquipmentType.weapon, null },
                     { CEnums.EquipmentType.head, null },
                     { CEnums.EquipmentType.body, null },
                     { CEnums.EquipmentType.legs, null },
                     { CEnums.EquipmentType.accessory, null }
                 }
             },

             {
                "_parsto", new Dictionary<CEnums.EquipmentType, dynamic>()
                 {
                     { CEnums.EquipmentType.weapon, null },
                     { CEnums.EquipmentType.head, null },
                     { CEnums.EquipmentType.body, null },
                     { CEnums.EquipmentType.legs, null },
                     { CEnums.EquipmentType.accessory, null }
                 }
             },

             {
                "_adorine", new Dictionary<CEnums.EquipmentType, dynamic>()
                 {
                     { CEnums.EquipmentType.weapon, null },
                     { CEnums.EquipmentType.head, null },
                     { CEnums.EquipmentType.body, null },
                     { CEnums.EquipmentType.legs, null },
                     { CEnums.EquipmentType.accessory, null }
                 }
             },
        };

        public Dictionary<string, List<dynamic>> GetInventory()
        {
            return inventory;
        }

        public Dictionary<CEnums.EquipmentType, dynamic> GetEquipment(string pcu_id)
        {
            return equipped[pcu_id];
        }

        public void AddItemToInventory(int item_id)
        {
            var new_item = FindItemWithID(item_id);
            GetInventory()[new_item.Category].Add(new_item);
        }

        public void RemoveItemFromInventory(int item_id)
        {
            var deleted_item = GetInventory()[FindItemWithID(item_id).Category].Single(x => x.ItemID == item_id);
            GetInventory()[FindItemWithID(item_id).Category].Remove(deleted_item);
        }

        public Item FindItemWithID(int item_id)
        {
            ItemManager item_manager = new ItemManager();
            return item_manager.GetItemList().Single(x => x.ItemID == item_id);
        }
    }
}
