using System;
using System.Collections.Generic;
using System.Linq;

namespace Data
{
    public static class ItemManager
    {
        private static readonly List<Item> item_list = new List<Item>()
        {
            /* =========================== *
             *           WEAPONS           *
             * =========================== */
            #region
            new Weapon("Fists", "The oldest weapon known to man.",
                0, 0, CEnums.WeaponType.melee, CEnums.CharacterClass.any, CEnums.Element.neutral, "weapon_fists"),

            // Weapons -- Warrior
            new Weapon("Iron Hoe",  
@"Not much of a weapon, unless you really hate dirt.
-5% Damage Increase
-Only usable by Warriors", 10, 0.05, CEnums.WeaponType.melee, CEnums.CharacterClass.warrior, CEnums.Element.neutral, "iron_hoe"),

            new Weapon("Bronze Sword",
@"A light yet sturdy sword smelted from bronze.
-10% Damage Increase
-Only usable by Warriors", 150, 0.1, CEnums.WeaponType.melee, CEnums.CharacterClass.warrior, CEnums.Element.neutral, "bnz_swd"),

            new Weapon("Enhanced Bronze Sword",
@"Even better than your typical Bronze Sword.
-30% Damage Increase
-Only usable by Warriors", 300, 0.3, CEnums.WeaponType.melee, CEnums.CharacterClass.warrior, CEnums.Element.neutral, "en_bnz_swd"),

            new Weapon("Steel Spear",
@"A fair-sized spear crafted from well made steel.
-50% Damage Increase
-Only usable by Warriors", 600, 0.5, CEnums.WeaponType.melee, CEnums.CharacterClass.warrior, CEnums.Element.neutral, "stl_spr"),

            new Weapon("Enhanced Steel Spear",
@"Even better than your typical Steel Spear.
-70% Damage Increase
-Only usable by Warriors", 900, 0.7, CEnums.WeaponType.melee, CEnums.CharacterClass.warrior, CEnums.Element.neutral, "en_stl_spr"),

            new Weapon("Titanium Battleaxe",
@"A heavy and powerful axe made of high quality Titanium.
-90% Damage Increase
-Only usable by Warriors", 1200, 0.9, CEnums.WeaponType.melee, CEnums.CharacterClass.warrior, CEnums.Element.neutral, "titan_axe"),

            // Weapons -- Assassin
            new Weapon("Stone Dagger", 
@"A stone knife that you made yourself! Used to shear sheep and cut meat.
-5% Damage Increase
-Only usable by Assassins", 10, 0.05, CEnums.WeaponType.melee, CEnums.CharacterClass.assassin, CEnums.Element.neutral, "stn_dag"),

            new Weapon("Serrated Knife", 
@"A durable knife made of iron, with one side made jagged.
-10% Damage Increase
-Only usable by Assassins", 150, 0.1, CEnums.WeaponType.melee, CEnums.CharacterClass.assassin, CEnums.Element.neutral, "ser_knf"),

            new Weapon("Enhanced Serrated Knife", 
@"Even better than your typical Serrated Knife.
-30% Damage Increase
-Only usable by Assassins", 300, 0.3, CEnums.WeaponType.melee, CEnums.CharacterClass.assassin, CEnums.Element.neutral, "en_ser_knf"),

            new Weapon("Stiletto", 
@"A long, cross-shaped knife perfect for 'removing' your enemies.
-50% Damage Increase
-Only usable by Assassins", 600, 0.5, CEnums.WeaponType.melee, CEnums.CharacterClass.assassin, CEnums.Element.neutral, "stiletto"),

            new Weapon("Enhanced Stiletto",
@"Even better than your typical Stiletto.
-70% Damage Increase
-Only usable by Assassins", 900, 0.7, CEnums.WeaponType.melee, CEnums.CharacterClass.assassin, CEnums.Element.neutral, "en_stiletto"),

            new Weapon("Mythril Shortblade", 
@"A knife made of a rare and powerful material.
-90% Damage Increase
-Only usable by Assassins", 1200, 0.9, CEnums.WeaponType.melee, CEnums.CharacterClass.assassin, CEnums.Element.neutral, "myth_sb"),

            // Weapons -- Ranger
            new Weapon("Sling Shot", 
@"A weapon that could scare even the mightiest of tin-cans.
-5% Damage Increase
-Only usable by Rangers", 10, 0.05, CEnums.WeaponType.ranged, CEnums.CharacterClass.ranger, CEnums.Element.neutral, "slg_sht"),

            new Weapon("Short Bow",
@"A bow of great craftsmanship. It's kinda small, though.
-10% Damage Increase
-Only usable by Rangers", 150, 0.1, CEnums.WeaponType.ranged, CEnums.CharacterClass.ranger, CEnums.Element.neutral, "sht_bow"),

            new Weapon("Enhanced Short Bow",
@"Even better than your typical Short Bow.
-30% Damage Increase
-Only usable by Rangers", 300, 0.3, CEnums.WeaponType.ranged, CEnums.CharacterClass.ranger, CEnums.Element.neutral, "en_sht_bow"),

            new Weapon("Long Bow",
@"A much more impressive bow capable of accuracy at long distances.
-50% Damage Increase
-Only usable by Rangers", 600, 0.5, CEnums.WeaponType.ranged, CEnums.CharacterClass.ranger, CEnums.Element.neutral, "lng_bow"),

            new Weapon("Enhanced Long Bow",
@"Even better than your typical Long Bow.
-70% Damage Increase
-Only usable by Rangers", 900, 0.7, CEnums.WeaponType.ranged, CEnums.CharacterClass.ranger, CEnums.Element.neutral, "en_lng_bow"),

            new Weapon("Ashen Crossbow",
@"A beautifully-crafted crossbow made from the wood of an ash tree
-90% Damage Increase
-Only usable by Rangers", 1200, 0.9, CEnums.WeaponType.ranged, CEnums.CharacterClass.ranger, CEnums.Element.neutral, "ash_cbow"),

            // Weapons -- Mage
            new Weapon("Magical Twig", 
@"Not actually magical but it makes you feel powerful when you use it.
-5% Damage Increase
-Only usable by Mages", 10, 0.05, CEnums.WeaponType.ranged, CEnums.CharacterClass.mage, CEnums.Element.neutral, "mag_twg"),

            new Weapon("Oak Staff",
@"A wooden staff imbued with weak magical abilities.
-10% Damage Increase
-Only usable by Mages", 150, 0.1, CEnums.WeaponType.ranged, CEnums.CharacterClass.mage, CEnums.Element.neutral, "oak_stf"),

            new Weapon("Enhanced Oak Staff",
@"Even better than your typical Oak Staff.
-30% Damage Increase
-Only usable by Mages", 300, 0.3, CEnums.WeaponType.ranged, CEnums.CharacterClass.mage, CEnums.Element.neutral, "en_oak_stf"),

            new Weapon("Arcane Spellbook",
@"An intermediate spellbook for combat purposes.
-50% Damage Increase
-Only usable by Mages", 600, 0.5, CEnums.WeaponType.ranged, CEnums.CharacterClass.mage, CEnums.Element.neutral, "arc_spb"),

            new Weapon("Enhanced Arcane Spellbook",
@"Even better than your typical Arcane Spellbook.
-70% Damage Increase
-Only usable by Mages", 900, 0.7, CEnums.WeaponType.ranged, CEnums.CharacterClass.mage, CEnums.Element.neutral, "en_arc_spb"),

            new Weapon("Runic Staff",
@"A powerful staff enchanted with ancient magic.
-90% Damage Increase
-Only usable by Mages", 1200, 0.9, CEnums.WeaponType.ranged, CEnums.CharacterClass.mage, CEnums.Element.neutral, "rnc_stf"),

            // Weapons -- Paladin
            new Weapon("Rubber Mallet",
@"This can barely hammer nails, what do you expect to kill with it?
-5% Damage Increase
-Only usable by Paladins", 10, 0.05, CEnums.WeaponType.melee, CEnums.CharacterClass.paladin, CEnums.Element.neutral, "rbr_mlt"),

            new Weapon("Holy Mace",
@"An well-made iron mace imbued with the power of the heavens.
-10% Damage Increase
-Only usable by Paladins", 150, 0.1, CEnums.WeaponType.melee, CEnums.CharacterClass.paladin, CEnums.Element.neutral, "holy_mace"),

            new Weapon("Enhanced Holy Mace",
@"Even better than your typical Holy Mace.
-30% Damage Increase
-Only usable by Paladins", 300, 0.3, CEnums.WeaponType.melee, CEnums.CharacterClass.paladin, CEnums.Element.neutral, "en_holy_mace"),

            new Weapon("Hammer of Might",
@"A hammer often used by holy warriors to smash their foes.
-50% Damage Increase
-Only usable by Paladins", 600, 0.5, CEnums.WeaponType.melee, CEnums.CharacterClass.paladin, CEnums.Element.neutral, "hmr_of_mgt"),

            new Weapon("Enhanced Hammer of Might",
@"Even better than your typical Hammer of Might.
-70% Damage Increase
-Only usable by Paladins", 900, 0.7, CEnums.WeaponType.melee, CEnums.CharacterClass.paladin, CEnums.Element.neutral, "en_hmr_of_mgt"),

            new Weapon("Night's Bane",
@"A forbidden hammer used throughout history to crush unholy creatures.
-90% Damage Increase
-Only usable by Paladins", 1200, 0.9, CEnums.WeaponType.melee, CEnums.CharacterClass.paladin, CEnums.Element.neutral, "ngt_bane"),

            // Weapons -- Monk
            new Weapon("Leather Gloves",
@"Used to prevent getting cut on thorns or the teeth of your enemies.
-5% Damage Increase
-Only usable by Monks", 10, 0.05, CEnums.WeaponType.melee, CEnums.CharacterClass.monk, CEnums.Element.neutral, "leather_gloves"),

            new Weapon("Brass Knuckles",
@"A brass adornment for your knuckles providing extra punching power.
-10% Damage Increase
-Only usable by Monks", 150, 0.1, CEnums.WeaponType.melee, CEnums.CharacterClass.monk, CEnums.Element.neutral, "brass_kncls"),

            new Weapon("Enhanced Brass Knuckles",
@"Even better than your typical Brass Knuckles.
-30% Damage Increase
-Only usable by Monks", 300, 0.30, CEnums.WeaponType.melee, CEnums.CharacterClass.monk, CEnums.Element.neutral, "en_brass_kncls"),

            new Weapon("Bladed Gloves",
@"Leather gloves with sturdy steel blades protruding from them.
-50% Damage Increase
-Only usable by Monks", 600, 0.5, CEnums.WeaponType.melee, CEnums.CharacterClass.monk, CEnums.Element.neutral, "bladed_gloves"),

            new Weapon("Enhanced Bladed Gloves",
@"Even better than your typical Bladed Gloves.
-70% Damage Increase
-Only usable by Monks", 900, 0.7, CEnums.WeaponType.melee, CEnums.CharacterClass.monk, CEnums.Element.neutral, "en_bladed_gloves"),

            new Weapon("Lead-Weighted Mitts",
@"Weighted with 5 pounds of lead and tipped with steel blades.
-90% Damage Increase
-Only usable by Monks", 1200, 0.9, CEnums.WeaponType.melee, CEnums.CharacterClass.monk, CEnums.Element.neutral, "lead_bg"),

            // Weapons -- Bard
            new Weapon("Kazoo",
@"A wooden kazoo that does more to annoy your enemies than damage them.
-5% Damage Increase
-Only usable by Bards", 10, 0.05, CEnums.WeaponType.instrument, CEnums.CharacterClass.bard, CEnums.Element.neutral, "kazoo"),

            new Weapon("Flute",
@"A good-quality flute made out of wood and silver.
-10% Damage Increase
-Only usable by Bards", 150, 0.1, CEnums.WeaponType.instrument, CEnums.CharacterClass.bard, CEnums.Element.neutral, "flute"),

            new Weapon("Snare Drum",
@"A marching drum used to inspire courage in the hearts of your allies.
-30% Damage Increase
-Only usable by Bards", 300, 0.3, CEnums.WeaponType.instrument, CEnums.CharacterClass.bard, CEnums.Element.neutral, "snare_drum"),

            new Weapon("Trumpet",
@"A mighty brass trumpet that can be heard blaring from miles away.
-50% Damage Increase
-Only usable by Bards", 600, 0.5, CEnums.WeaponType.instrument, CEnums.CharacterClass.bard, CEnums.Element.neutral, "trumpet"),

            new Weapon("Violin",
@"A beautiful violin that could make even the most stone-cold weep.
-70% Damage Increase
-Only usable by Bards", 1200, 0.7, CEnums.WeaponType.instrument, CEnums.CharacterClass.bard, CEnums.Element.neutral, "violin"),

            new Weapon("Bagpipes",
@"A ridiculously loud and extravagent bagpipe made from plaid fabric. Your
allies will probably hate you if you use this.
-90% Damage Increase
-Only usable by Bards", 2400, 0.9, CEnums.WeaponType.instrument, CEnums.CharacterClass.bard, CEnums.Element.neutral, "bagpipes"),
            #endregion

            /* =========================== *
             *            ARMOR            *
             * =========================== */
            #region
            new Armor("None", "You should probably get some armor.",
                0, 0, 0, new List<CEnums.CharacterClass>() {}, new List<CEnums.CharacterClass>() {}, "no_armor"),

            // Light Armor
            new Armor("Light Armor",
@"Armor made from leather, perfect for those who need to move quickly.
-Resistance: 10%
-Movement Penalty: 10%
-Good for Assassin and Ranger (1.5x Resist, 0.67x Penalty)
-Bad for Mage and Monk (0.67x Resist, 1.5x Penalty)", 100, 0.1, 0.1,
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.assassin, CEnums.CharacterClass.ranger },
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, "light_armor"),

            // Medium Armor
            new Armor("Medium Armor",
@"Cloth clothes with chainmail underneath for a balance of speed and defense.
-Resistance: 20%
-Movement Penalty: 15%
-Good for Warrior and Agriculturalist (1.5x Resist, 0.67x Penalty)
-Bad for Mage, Monk, and Bard (0.67x Resist, 1.5x Penalty)", 200, 0.2, 0.15,
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.warrior, CEnums.CharacterClass.agriculturalist },
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk, CEnums.CharacterClass.bard }, "medium_armor"),

            // Heavy Armor
            new Armor("Heavy Armor",
@"Armor made from thick plates, perfect for those in the thick of battle.
-Resistance: 30%
-Movement Penalty: 20%
-Good for Warrior and Paladin (1.5x Resist, 0.67x Penalty)
-Bad for all other classes (0.67x Resist, 1.5x Penalty)", 400, 0.3, 0.2,
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.warrior, CEnums.CharacterClass.paladin },
                      new List<CEnums.CharacterClass>()
                      {
                          CEnums.CharacterClass.mage,
                          CEnums.CharacterClass.monk,
                          CEnums.CharacterClass.assassin,
                          CEnums.CharacterClass.ranger,
                          CEnums.CharacterClass.bard,
                          CEnums.CharacterClass.agriculturalist
                      }, "heavy_armor"),

            // Fancy Robes
            new Armor("Fancy Robes",
@"Armor made from leather, perfect for those who need to move quickly.
-Resistance: 5%
-Movement Penalty: 5%
-Good for Mage and Monk (1.5x Resist, 0.67x Penalty)
-Bad for Warrior and Paladin (0.67x Resist, 1.5x Penalty)", 75, 0.05, 0.05,
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk },
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.warrior, CEnums.CharacterClass.paladin }, "fancy_robes"),

            // Dragonhide Armor
            new Armor("Dragonhide Armor",
@"Armor made from leather, perfect for those who need to move quickly.
-Resistance: 15%
-Movement Penalty: 15%
-Good for Assassin, Ranger and Agriculturalist (1.5x Resist, 0.67x Penalty)
-Bad for Mage and Monk (0.67x Resist, 1.5x Penalty)", 250, 0.15, 0.15,
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.assassin, CEnums.CharacterClass.ranger, CEnums.CharacterClass.agriculturalist },
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.mage, CEnums.CharacterClass.monk }, "dragon_armor"),

            // Festive Clothes
            new Armor("Festive Clothes",
@"Armor made from leather, perfect for those who need to move quickly.
-Resistance: 5%
-Movement Penalty: 2%
-Good for Bard (1.5x Resist, 0.67x Penalty)
-Bad for Warrior and Paladin (0.67x Resist, 1.5x Penalty)", 50, 0.05, 0.02,
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.monk },
                      new List<CEnums.CharacterClass>() { CEnums.CharacterClass.warrior, CEnums.CharacterClass.paladin }, "festive_clothes"),
            #endregion

            /* =========================== *
             *         ACCESSORIES         *
             * =========================== */
            #region
            new ElementAccessory("None", "You should probably get an accessory.", 0, CEnums.Element.neutral, "no_access"),

            // Accessories
            // -- Elemental Accessories
            new ElementAccessory("Aquatic Amulet", "An amulet that imbues its wearer with the power of WATER.",
                                 375, CEnums.Element.water, "aquatic_amulet"),
            new ElementAccessory("Infernal Amulet", "An amulet that imbues its wearer with the power of FIRE.",
                                 375, CEnums.Element.fire, "fire_amulet"),
            new ElementAccessory("Ground Amulet", "An amulet that imbues its wearer with the power of EARTH.",
                                 375, CEnums.Element.earth, "earth_amulet"),
            new ElementAccessory("Galvanic Amulet", "An amulet that imbues its wearer with the power of ELECTRICITY.",
                                 375, CEnums.Element.electric, "electric_amulet"),
            new ElementAccessory("Tempestuous Amulet", "An amulet that imbues its wearer with the power of WIND.",
                                 375, CEnums.Element.wind, "wind_amulet"),
            new ElementAccessory("Verdant Amulet", "An amulet that imbues its wearer with the power of GRASS.",
                                 375, CEnums.Element.grass, "grass_amulet"),
            new ElementAccessory("Glacial Amulet", "An amulet that imbues its wearer with the power of ICE.",
                                 375, CEnums.Element.ice, "ice_amulet"),
            new ElementAccessory("Divine Amulet", "An amulet that imbues its wearer with the power of LIGHT.",
                                 375, CEnums.Element.light, "light_amulet"),
            new ElementAccessory("Umbral Amulet", "An amulet that imbues its wearer with the power of DARKNESS.",
                                 375, CEnums.Element.dark, "dark_amulet"),
            #endregion

            /* =========================== *
             *            TOOLS            *
             * =========================== */
            #region
            new Shovel("Expert Mining Tool", 
@"A tool used to excavate for hidden gems and minerals. Comines the functions
of a pickaxe, shovel, and hammer all into one device! Use while on the
overworld to dig for gems. Gems have pre-determined locations and do not
respawn - there is no luck involved with this tool.", 150, "shovel"),

            new FastTravelAtlas("Fast Travel Atlas", 
@"A convenient tome that allows teleportation between towns. These aren't
being made anymore, after having been banned by the King due to its use in
many recent abductions and murders. Most of the pages appear to be missing.", 0, "fast_map"),

            new MonsterEncyclopedia("Monster Encyclopedia", 
@"A book containing information on monsters. When used in battle, this will
identify the stats and weaknesses of an enemy. Has no use outside of battle.", 200, "monster_book"),

            new PocketAlchemyLab("Pocket Alchemy Lab", 
@"A nifty little Pocket Alchemy Lab! Somehow all of the necessary tools to
convert everyday ingredients into useful potions can fit in your pocket.
There are six flavors of ingredients, and each flavor corresponds to a specific
potion. Combine three ingredients to make a potion. The ratio of flavors used
determines the probability of getting each flavor potion. The quantity of the
prevailing ingredient determines the potion strength.", 200, "pocket_lab"),

            new MusicBox("Portable Musicbox", 
@"Somehow this small device has the ability to play music without need for a
bard or instruments. Select a folder full of music on your computer and this
device will replace the in-game music with your tunes!", 250, "musicbox"),

            // Lockpicks
            new LockpickKit("Wooden Lockpick Kit", 
@"A wooden lockpick kit with a 30% chance to open chests. Chests can be found
by sneaking into houses in towns.", 30, 30, "wood_lckpck"),

            new LockpickKit("Copper Lockpick Kit",
@"A copper lockpick kit with a 45% chance to open chests. Chests can be found
by sneaking into houses in towns.", 200, 45, "copper_lckpck"),

            new LockpickKit("Iron Lockpick Kit",
@"An iron lockpick kit with a 60% chance to open chests. Chests can be found
by sneaking into houses in towns.", 300, 60, "iron_lckpck"),

            new LockpickKit("Steel Lockpick Kit",
@"A steel lockpick kit with a 75% chance to open chests. Chests can be found
by sneaking into houses in towns.", 500, 75, "steel_lckpck"),

            new LockpickKit("Mythril Lockpick Kit",
@"A mythril lockpick kit with a 90% chance to open chests. Chests can be found
by sneaking into houses in towns.", 700, 90, "mythril_lckpck"),
            #endregion

            /* =========================== *
             *         OTHER STUFF         *
             * =========================== */
            #region
            new QuestItem("Message from Joseph", "A neatly written message addressed to Philliard.", 0, "message_joseph"),

            new QuestItem("Message from Philliard", "A neatly written message addressed to Joseph.", 0, "message_philliard"),

            // Gems & Valuables
            new Valuable("Pearl", "A valuable pearl. This could probably be sold for quite a bit.", 875, "pearl_gem"),

            new Valuable("Ruby", "A valuable ruby. This could be sold for quite a bit.", 875, "ruby_gem"),

            new Valuable("Sapphire", "A valuable sapphire. This could probably be sold for quite a bit.", 875, "sapphire_gem"),

            new Valuable("Emerald", "A valuable emerald. This could probably be sold for quite a bit.", 875, "emerald_gem"),

            new Valuable("Citrine", "A valuable citrine. This could probably be sold for quite a bit.", 875, "citrine_gem"),

            new Valuable("Jade", "A valuable jade. This could probably be sold for quite a bit.", 875, "jade_gem"),

            new Valuable("Opal", "A valuable opal. This could probably be sold for quite a bit.", 875, "opal_gem"),

            new Valuable("Onyx", "A valuable onyx. This could probably be sold for quite a bit.", 875, "onyx_gem"),

            new Valuable("Diamond", "A valuable diamond. This could probably be sold for quite a bit.", 875, "diamond_gem"),

            new Valuable("Amethyst", "A valuable amethyst. This could probably be sold for quite a bit.", 875, "amethyst_gem"),

            new Valuable("Topaz", "A valuable topaz. This could probably be sold for quite a bit.", 875, "topaz_gem"),

            new Valuable("Garnet", "A valuable garnet. This could probably be sold for quite a bit.", 875, "garnet_gem"),

            new Valuable("Quartz", "A valuable quartz. This could probably be sold for quite a bit.", 875, "quartz_gem"),

            new Valuable("Zircon", "A valuable zircon. This could probably be sold for quite a bit.", 875, "zircon_gem"),

            new Valuable("Agate", "A valuable agate. This could probably be sold for quite a bit.", 875, "agate_gem"),

            new Valuable("Aquamarine", "A valuable aquamarine. This could probably be sold for quite a bit.", 875, "aquamarine_gem"),

            // ALCHEMY INGREDIENTS - Dropped by monsters, used to make potions
            // Strange
            new Ingredient("Broken Crystal",
@"A chunk of crystal too powdery to be of any value. Could have useful alchemical
applications. Has a 'Strange' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "strange", "broken_crystal"),

            new Ingredient("Chain links",
@"A couple joined links of chain made from steel. Could have useful alchemical
applications. Has a 'Strange' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "strange", "chain_link"),

            new Ingredient("Bag of Bones",
@"A bag full of various bones from a now deceased creature. Could have useful
alchemical applications. Has a 'Strange' alchemical flavor. Combine with two
other ingredients in a Pocket Alchemy Lab to make a potion.", 25, "strange", "bone_bag"),

            new Ingredient("Ripped Cloth",
@"A thick, torn cloth made out of an unknown fabric. Could have useful alchemical
applications. Has a 'Strange' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "strange", "ripped_cloth"),

            new Ingredient("Living Bark",
@"This bark has a fleshy texture to it. Could have useful alchemical
applications. Has a 'Strange' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "strange", "living_bark"),

            // Mystic
            new Ingredient("Demonic Essence",
@"A strange orb that exudes a terrifying aura. Could have useful alchemical
applications. Has a 'Mystic' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mystic", "demonic_essence"),

            new Ingredient("Angelic Essence",
@"A strange orb that radiates an incredible aura. Could have useful alchemical
applications. Has a 'Mystic' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mystic", "angelic_essence"),

            new Ingredient("Strange Runestone",
@"Strange stones with even stranger symbols on it. Could have useful alchemical
applications. Has a 'Mystic' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mystic", "runestone"),

            new Ingredient("Unicorn Horn",
@"A tough and shiny horn from a mythical creature. Could have useful alchemical
applications. Has a 'Mystic' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mystic", "unicorn_horn"),

            new Ingredient("Fairy Dust",
@"Dust from a fairy. It has strange, magical properties. Could have useful
alchemical applications. Has a 'Mystic' alchemical flavor. Combine with two
other ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mystic", "fairy_dust"),

            // Rigid
            new Ingredient("Crab Claw",
@"A reddish claw from a giant crab. Could have useful alchemical applications.
Has a 'Rigid' alchemical flavor. Combine with two other ingredients in a
Pocket Alchemy Lab to make a potion.", 25, "rigid", "crab_claw"),

            new Ingredient("Shell Fragment",
@"A broken fragment of a once-beautiful shell. Could have useful alchemical
applications. Has a 'Rigid' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "rigid", "shell_fragment"),

            new Ingredient("Golem Rock",
@"A small rock that seems to glow slightly. Could have useful alchemical
applications. Has a 'Rigid' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "rigid", "golem_rock"),

            new Ingredient("Beetle Shell",
@"A bluish shell from a large beetle. Could have useful alchemical applications.
Has a 'Rigid' alchemical flavor. Combine with two other ingredients in a
Pocket Alchemy Lab to make a potion.", 25, "rigid", "beetle_shell"),

            new Ingredient("Monster Skull",
@"A broken skull from a strange creature. Could have useful alchemical
applications. Has a 'Rigid' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "rigid", "monster_skull"),

            // Flowing
            new Ingredient("Vial of Slime",
@"A small glass vial filled with gooey slime. Could have useful alchemical
applications. Has a 'Flowing' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "flowing", "slime_vial"),

            new Ingredient("Vial of Blood",
@"A small glass vial filled with the blood of some creature. Could have useful
alchemical applications. Has a 'Flowing' alchemical flavor. Combine with two
other ingredients in a Pocket Alchemy Lab to make a potion.", 25, "flowing", "blood_vial"),

            new Ingredient("Vial of Water",
@"A small glass vial filled with enchanted water. Could have useful alchemical
applications. Has a 'Flowing' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "flowing", "water_vial"),

            new Ingredient("Ink Sack",
@"A small pouch full of an inky substance. Could have useful alchemical
applications. Has a 'Flowing' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "flowing", "ink_sack"),

            new Ingredient("Ectoplasm",
@"The gooey remains from a terrifying apparition. Could have useful alchemical
applications. Has a  'Flowing' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "flowing", "ectoplasm"),

            // Dark
            new Ingredient("Burnt Ash",
@"The ashy remains of a once-living creature. Could have useful alchemical
applications. Has a 'Dark' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "dark", "burnt_ash"),

            new Ingredient("Monster Fang",
@"The sharp fang of a frightening creature. Could have useful alchemical
applications. Has a 'Dark' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "dark", "monster_fang"),

            new Ingredient("Gooey Antennae",
@"A pair of antennae from a massive, slimy insect. Could have useful alchemical
applications. Has a 'Dark' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "dark", "antennae"),

            new Ingredient("Eyeballs",
@"The visual receptors of some disgusting creature. Could have useful alchemical
applications. Has a 'Dark' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "dark", "eye_balls"),

            new Ingredient("Serpent Scale",
@"A rough scale from an unknown reptile. Could have useful alchemical
applications. Has a 'Dark' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "dark", "serpent_scale"),

            // Natural
            new Ingredient("Wing Piece",
@"A piece of wing from a flying creature. Could have useful alchemical
applications. Has a 'Natural' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "natural", "wing_piece"),

            new Ingredient("Animal Fur",
@"A wet clump of fur from a strange animal. Could have useful alchemical
applications. Has a 'Natural' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "natural", "animal_fur"),

            new Ingredient("Rodent Tail",
@"The detached tail of a hideous rodent. Could have useful alchemical
applications. Has a 'Natural' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "natural", "rodent_tail"),

            new Ingredient("Serpent Tongue",
@"A dried-up tongue from a slithery serpent. Could have useful alchemical
applications. Has a 'Natural' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "natural", "serpent_tongue"),

            new Ingredient("Feathers",
@"A veiny feather from an unknown avian creature. Could have useful alchemical
applications. Has a 'Natural' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "natural", "feathers"),

            // Mathematical
            new Ingredient("Calculus Homework",
@"A load of random symbols and gibberish. Could have useful alchemical
applications. Has a 'Mathematical' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mathematical", "c_homework"),

            new Ingredient("Graph Paper",
@"Useful paper for graphing points and lines. Could have useful alchemical
applications. Has a 'Mathematical' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mathematical", "g_paper"),

            new Ingredient("Ruler",
@"A piece of wood with lines on it. Neat! Could have useful alchemical
applications. Has a 'Mathematical' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mathematical", "ruler"),

            new Ingredient("Protractor and Compass",
@"Instruments used to make shapes and angles. Could have useful alchemical
applications. Has a 'Mathematical' alchemical flavor. Combine with two other
ingredients in a Pocket Alchemy Lab to make a potion.", 25, "mathematical", "protractor")
            #endregion
        };

        public static List<Item> GetItemList()
        {
            return item_list;
        }

        public static Item FindItemWithID(string item_id)
        {
            return GetItemList().Single(x => x.ItemID == item_id);
        }

        public static bool VerifyItemExists(string item_id)
        {
            return GetItemList().Select(x => x.ItemID).Contains(item_id);
        }
    }

    public abstract class Item
    {
        // The basic item class. Items are stored in the "inventory" dictionary. All
        // item-subclasses inherit from this class.
        public string ItemName { get; set; }
        public string Description { get; set; }
        public int Value { get; set; }
        public bool IsImportant { get; set; }
        public CEnums.InvCategory Category { get; set; }
        public string ItemID { get; set; }

        public abstract void UseItem(PlayableCharacter user);

        // Constructor
        protected Item(string name, string desc, int value, bool imp, CEnums.InvCategory cat, string item_id)
        {
            ItemName = name;
            Description = desc;
            Value = value;
            IsImportant = imp;
            Category = cat;
            ItemID = item_id;
        }
    }

    /* =========================== *
     *        MISCELLANEOUS        *
     * =========================== */
    public class QuestItem : Item
    {
        public override void UseItem(PlayableCharacter user)
        {
            Console.WriteLine("This looks important, you should definitely hold on to it.");
            CMethods.PressAnyKeyToContinue();
        }

        public QuestItem(string name, string desc, int value, string item_id) : base(name, desc, value, true, CEnums.InvCategory.quest, item_id)
        {

        }
    }

    public class Valuable : Item
    {       
        public override void UseItem(PlayableCharacter user)
        {
            Console.WriteLine("You could probably make a lot of gold selling this.");
            CMethods.PressAnyKeyToContinue();
        }

        public Valuable(string name, string desc, int value, string item_id) : base(name, desc, value, false, CEnums.InvCategory.misc, item_id)
        {     

        }
    }

    public class Ingredient : Item
    {
        public string Flavor { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            Console.WriteLine("It's called an ingredient, but you probably shouldn't eat it.");
            CMethods.PressAnyKeyToContinue();
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
            if (equipper.PClass == PClass)
            {
                InventoryManager.EquipItem(equipper, ItemID);
                Console.WriteLine($"{equipper.Name} equips the {ItemName}.");
                CMethods.PressAnyKeyToContinue();
            }

            else
            {
                Console.WriteLine($"{equipper.Name} must be a {CEnums.EnumToString(PClass)} to equip this.");
                CMethods.PressAnyKeyToContinue();
            }
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
            InventoryManager.EquipItem(equipper, ItemID);
            Console.WriteLine($"{equipper.Name} equips the {ItemName}.");

            if (ProficientClasses.Contains(equipper.PClass))
            {
                Console.WriteLine($"It feels light and comfortable.");
            }

            else if (NonProficientClasses.Contains(equipper.PClass))
            {
                Console.WriteLine($"It feels bulky and cumbersome.");
            }

            CMethods.PressAnyKeyToContinue();
        }

        public override void Unequip(PlayableCharacter unequipper)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public Armor(string name, string desc, int value, double resist, double penatly, List<CEnums.CharacterClass> prof_classes, List<CEnums.CharacterClass> nonprof_classes, string item_id) :  base(name, desc, value, CEnums.InvCategory.armor, item_id)
        {
            Resist = resist;
            Penalty = penatly;
            ProficientClasses = prof_classes;
            NonProficientClasses = nonprof_classes;
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
                main.s_input(@"nPress enter/return ") */
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
                main.s_input(@"nPress enter/return ")

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
                    main.s_input(@"nPress enter/return ")

                remove_item(self.item_id)

            else:
                print(f"Drinking this {self.name} probably wouldn't do anything.")
                main.s_input(@"nPress enter/return ") */
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
            throw new DivideByZeroException("You asked for this.");
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
                main.s_input(@"nPress enter/return")
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
                main.s_input(@"nPress enter/return ")

                acquired_gems.append(c_gem.item_id)
                add_item(c_gem.item_id)

            else:
                print("No luck, your party didn't find anything.")
                main.s_input(@"nPress enter/return ") */
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
                main.s_input(@"nPress enter/return")
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
                        y_n = main.s_input(f"Warp to {chosen.name}? | [Y]es or [N]o: ").lower()

                        if y_n.startswith('y'):
                            if 'has_teleported' not in main.party_info:
                                main.party_info['has_teleported'] = False

                            if main.party_info['has_teleported']:
                                print("-"*save_load.divider_size)
                                print("Your party peers into the Fast Travel Atlas and begins to phase out of reality.")
                                print("Upon waking you're exactly where you wanted to be.")
                                main.s_input(@"nPress enter/return ")

                            else:
                                print("-"*save_load.divider_size)
                                print("You begin to feel strange - your body feels light and all you hear is silence.")
                                print("Your vision starts going blank... All of your senses quickly turning off until")
                                print("you're left with nothing but your thoughts...")
                                main.s_input(@"nPress enter/return ")
                                print("...")
                                main.smart_sleep(1)
                                print("...")
                                main.smart_sleep(1)
                                print("...")
                                main.smart_sleep(1)
                                sounds.enemy_hit.SmartPlay()
                                print("CRASH! Your senses re-emerge you've landed on your back... Oh, you're exactly where")
                                print("you teleported to!")
                                main.s_input(@"nPress enter/return ")

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
        public int LockpickPower { get; set; }

        public override void UseItem(PlayableCharacter user)
        {
            throw new NotImplementedException();
        }

        // Constructor
        public LockpickKit(string name, string desc, int value, int power, string item_id) : base(name, desc, value, true, CEnums.InvCategory.tools, item_id)
        {
            LockpickPower = power;
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

            print(f"{user.target.name.upper()}'s STATS:
            Physical: { user.target.attk}
            Attack / {user.target.dfns} Defense
            Magical: {user.target.m_attk} Attack / {user.target.m_dfns} Defense
            Piercing: {user.target.p_attk} Attack / {user.target.p_dfns} Defense
            Speed: {user.target.spd}
            Evasion: {user.target.evad}
            Elements: Attacks are { user.target.def_element.title()} / Defense is {user.target.off_element.title()} / \
            Weak to { m_w.title()}") */
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
                main.s_input(@"nPress enter/return ")

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

                        main.s_input(@"nPress enter/return ")
                        print('-'*save_load.divider_size)

                    else:
                        print("All ingredients added! Time to start brewing!")
                        main.s_input(@"nPress enter/return ")
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
            main.s_input(@"nPress enter/return ") */
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
                                main.s_input(@"nPress enter/return ")
                                print("-"*save_load.divider_size)

                                break

                            else:
                                print("-"*save_load.divider_size)
                                print("You need to set a music directory first!")
                                main.s_input(@"nPress enter/return ")
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

                main.s_input(@"nPress enter/return ")

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
                        main.s_input(@"nPress enter/return ")
                        print("-" * save_load.divider_size)
                        continue

                print("-" * save_load.divider_size)
                for file in os.listdir(folder):
                    if any(map(file.endswith, ['.ogg', 'flac', '.mp3', '.wav'])) :

                        main.party_info['musicbox_folder'] = folder
                        print(f"Directory set to {folder}")

                        if main.party_info['musicbox_isplaying']:
                            print("You'll need to restart your musicbox to apply this change.")

                        main.s_input(@"nPress enter/return ")

                        return

                else:
                    print("Couldn't find any .ogg, .flac, .mp3, or .wav files in that directory.")
                    while True:
                        y_n = main.s_input("Select a different directory? | [Y]es or [N]o: ")

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
