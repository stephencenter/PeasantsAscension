using System.Collections.Generic;
using System.Linq;

namespace Scripts
{
    class InventoryManager
    {
        public Dictionary<string, List<dynamic>> inventory = new Dictionary<string, List<dynamic>>()
        {
            { "q_items", new List<dynamic>() { } },
            { "consumables",  new List<dynamic>() { } },
            { "weapons",  new List<dynamic>() { } },
            { "armor",  new List<dynamic>() { } },
            { "tools",  new List<dynamic>() { } },
            { "access",  new List<dynamic>() { } },
            { "misc",  new List<dynamic>() { } }
        };

        public Dictionary<string, Dictionary<string, dynamic>> equipped = new Dictionary<string, Dictionary<string, dynamic>>()
        {
             {"_player", new Dictionary<string, dynamic>() { {"weapon", null }, {"head", null }, {"body", null }, {"legs", null }, {"accessory", null } } },
             {"_solou", new Dictionary<string, dynamic>() { {"weapon", null }, {"head", null }, {"body", null }, {"legs", null }, {"accessory", null } } },
             {"_chili", new Dictionary<string, dynamic>() { {"weapon", null }, {"head", null }, {"body", null }, {"legs", null }, {"accessory", null } } },
             {"_chyme", new Dictionary<string, dynamic>() { {"weapon", null }, {"head", null }, {"body", null }, {"legs", null }, {"accessory", null } } },
             {"_storm", new Dictionary<string, dynamic>() { {"weapon", null }, {"head", null }, {"body", null }, {"legs", null }, {"accessory", null } } },
             {"_parsto", new Dictionary<string, dynamic>() { {"weapon", null }, {"head", null }, {"body", null }, {"legs", null }, {"accessory", null } } },
             {"_adorine",  new Dictionary<string, dynamic>() { {"weapon", null }, {"head", null }, {"body", null }, {"legs", null }, {"accessory", null } } },
        };

        public Dictionary<string, List<dynamic>> GetInventory()
        {
            return inventory;
        }

        public Dictionary<string, dynamic> GetEquipped(string pcu_id)
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
