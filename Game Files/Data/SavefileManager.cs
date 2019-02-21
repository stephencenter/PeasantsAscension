using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Text.RegularExpressions;

namespace Data
{
    public static class SavefileManager
    {
        public static int divider_size = 25;
        public static bool do_blips = true;
        public static float music_vol = 1;
        public static float sound_vol = 1;
        public static string adventure_name;

        // Save Files
        public const string sav_acquired_gems = "acquired_gems.json";    // Acquired Gems
        public const string sav_def_bosses = "def_bosses.json";          // Defeated Bosses
        public const string sav_equipment = "equipment.json";            // Equipment
        public const string sav_inventory = "inventory.json";            // Inventory
        public const string sav_boss_flags = "boss_flags.json";          // Misc Boss Info
        public const string sav_game_info = "game_info.json";            // Party Info
        public const string sav_dialogue_flags = "dialogue_flags.json";  // Quests & Dialogue
        public const string sav_chests = "chests.json";                  // Chest Info

        // PCU Save Files
        public const string sav_player = "player_stats.json";    // Player Stats
        public const string sav_solou = "solou_stats.json";      // Solou's Stats
        public const string sav_chili = "chili_stats.json";      // Chili's Stats
        public const string sav_chyme = "chyme_stats.json";      // Chyme's Stats
        public const string sav_parsto = "parsto_stats.json";    // Parsto's Stats
        public const string sav_adorine = "adorine_stats.json";  // Adorine's Stats
        public const string sav_storm = "storm_stats.json";      // Storm's Stats
        public const string sav_kaltoh = "kaltoh_stats.json";    // Kaltoh's Stats

        public const string base_dir = "Save Files";
        public const string temp_dir = "temp";

        public static void ApplySettings()
        {

        }

        public static void SetAdventureName()
        {
            // This function asks the player for an "adventure name". This is the
            // name of the directory in which his/her save files will be stored.

            while (true)
            {
                // Certain OSes don't allow certain characters, so this removes those characters
                // and replaces them with whitespace. The player is then asked if this is okay.
                string adventure = CMethods.MultiCharInput("Finally, what do you want to name this adventure? ");

                // This line removes all characters that are not alphanumeric, spaces, dashes, or underscores
                // We also remove repeated spaces like "Hello    world" => "Hello world"
                // Finally we .Trim() to remove leading or ending whitespace like "    Hello world    " => "Hello world"
                adventure = Regex.Replace(Regex.Replace(adventure, @"[^\w\s\-]*", ""), @"\s+", " ").Trim();

                // Make sure the adventure name isn't blank
                if (string.IsNullOrEmpty(adventure))
                {
                    continue;
                }

                // You also can't use "temp", because this is reserved for other features
                else if (adventure.ToLower() == "temp")
                {
                    Console.WriteLine("Please choose a different name, that one definitely won't do!");
                    CMethods.PressAnyKeyToContinue();
                    continue;
                }

                // Make sure that the folder doesn't already exist
                else if (Directory.Exists(adventure))
                {
                    Console.WriteLine("I've already read about adventures with that name; be original!");
                    CMethods.PressAnyKeyToContinue();
                    continue;
                }

                // Max adventure name length is 35
                else if (adventure.Length > 35)
                {
                    Console.WriteLine("That adventure name is far too long, it would never catch on!");
                    CMethods.PressAnyKeyToContinue();
                    continue;
                }

                while (true)
                {
                    string yes_no = CMethods.SingleCharInput($"You want your adventure to be remembered as '{adventure}'? | [Y]es or [N]o: ").ToLower();

                    if (CMethods.IsYesString(yes_no))
                    {
                        adventure_name = adventure;
                        return;
                    }

                    else if (CMethods.IsNoString(yes_no))
                    {
                        CMethods.PrintDivider();
                        break;
                    }
                }
            }
        }

        public static void SaveTheGame(bool silent = false)
        {
            // Save important game data to .json files
            // The silent parameter determines whether or not text is displayed
            // showing the saving happening. When true, this can be used as a
            // secret autosave.
            while (true)
            {
                string yes_no = silent ? "y" : CMethods.SingleCharInput("Do you wish to save your progress? | [Y]es or [N]o: ").ToLower();

                if (CMethods.IsYesString(yes_no))
                {
                    if (!silent)
                    {
                        Console.WriteLine("Saving...");
                        CMethods.SmartSleep(100);
                    }

                    // Make sure there isn't already a temp directory
                    if (Directory.Exists($"{base_dir}/{temp_dir}"))
                    {
                        Directory.Delete($"{base_dir}/{temp_dir}");
                    }

                    // Crete a temp directory to store the save data in, so that if the saving fails data isn't corrupted
                    Directory.CreateDirectory($"{base_dir}/{temp_dir}");

                    // Save everything as JSON objects inside .json files, and store them in the temp directory
                    JSONSerializer.SerializeEverything();

                    // Delete the existing save file
                    if (Directory.Exists($"{base_dir}/{adventure_name}"))
                    {
                        Directory.Delete($"{base_dir}/{adventure_name}");
                    }

                    // Create the save file folder
                    Directory.CreateDirectory($"{base_dir}/{adventure_name}");

                    // Move all the files from the temp directory to the save file folder
                    DirectoryInfo temp_directory = new DirectoryInfo($"{base_dir}/{temp_dir}");
                    foreach (FileInfo file in temp_directory.GetFiles("*.json"))
                    {
                        File.Move($"{base_dir}/{temp_dir}/{file.Name}", $"{base_dir}/{adventure_name}/{file.Name}");
                    }

                    Directory.Delete($"{base_dir}/{temp_dir}");

                    // Create a file with a disclaimer that warns against manually editing save files
                    string disclaimer = @"-IMPORTANT NOTE-
Editing these .json files is a VERY easy way to corrupt your save file.
Unless you are familiar with the inner-workings of the game and know
how to read/edit .json files, it's highly recommended that you turn away.";
    
                    File.WriteAllText($"{base_dir}/README.txt", disclaimer);

                    if (!silent)
                    {
                        Console.WriteLine("Game has been saved!");
                        CMethods.PressAnyKeyToContinue();
                    }

                    return;
                }

                else if (CMethods.IsNoString(yes_no))
                {
                    return;
                }
            }
        }

        public static void LoadTheGame()
        {
            // File.Exists(path);

            /*
            print('-'*divider_size)

            // Check each part of the save file
            print('Searching for valid save files...')
            main.smart_sleep(0.1)

            if not os.path.isdir(base_dir):

                print('No save files found. Starting new game...')
                main.smart_sleep(0.1)

                print('-'*divider_size)
                units.create_player()

                return

            save_files = {}
            menu_info = {}

            save_file_list = [
                sav_acquired_gems, sav_def_bosses, sav_equip_items, sav_inventory, sav_misc_boss_info, sav_party_info,
                sav_quests_dia, sav_spellbook, sav_play, sav_solou, sav_chili, sav_ran_af, sav_adorine, sav_parsto, sav_chyme,
                sav_chests
            ]

            for folder in [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]:
                // If all save-file components exist...
                if all(map(os.path.isfile, ['/'.join([base_dir, x.format(ADVENTURE_NAME=folder)]) for x in save_file_list])):
                    // ...then set the dictionary key equal to the newly-formatted save file names
                    save_files[folder] = [x.format(ADVENTURE_NAME=folder) for x in save_file_list]

                    try:
                        with open('/'.join([base_dir, folder, "menu_info.txt"]), encoding='utf-8') as f:
                            menu_info[folder] = f.read()

                    except FileNotFoundError:
                        menu_info[folder] = "Unable to load preview info"
            main.smart_sleep(0.1)

            if not save_files:
                // If there are no found save files, then have the player make a new character
                print('No save files found. Starting new game...')
                print('-'*divider_size)
                main.smart_sleep(0.1)
                units.create_player()

                return

            print('-'*divider_size)
            print(f'Found {len(save_files)} valid save file(s): ')

            // padding is a number that the game uses to determine how much whitespace is needed
            // to make certain visual elements line up on the screen.
            padding = len(max([index for index in save_files], key=len))

            // Print information about each save file and allow the player to choose which
            // file to open
            for num, fol in enumerate([key for key in sorted(save_files)]):
                print(f"      [{num + 1}] {fol}{' '*(padding - len(fol))} | {menu_info[fol]}")

            while True:
                chosen = main.s_input('Input [#] (or type "create new"): ').lower()

                try:
                    // Account for the fact that list indices start at 0
                    adventure_name = sorted(save_files)[int(chosen) - 1]

                except (IndexError, ValueError):
                    // Let the player create a new save file
                    if chosen.startswith("c"):
                        print('-'*divider_size)
                        units.create_player()
                        return

                    continue

                print('-'*divider_size)
                print(f'Loading Save File: "{sorted(save_files)[int(chosen) - 1]}"...')
                main.smart_sleep(0.1)

                format_save_names()
                deserialize_all()

                return */
        }
    }

    public static class JSONSerializer
    {
        public static void SerializeEverything()
        {
            try
            {
                SerializeGems();
                SerializeEquipment();
                SerializeInventory();
                SerializeDialogueFlags();
                SerializeBossFlags();
                SerializeChestFlags();
                SerializePartyMemebers();
                SerializeGameInfo();
            }

            catch (Exception)
            {
                throw;
                // logging.exception(f'Error saving game on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
                // print('There was an error saving. Error message can be found in error_log.out') if verbose else ''
                // main.s_input("\nPress enter/return ") if verbose else ''
            }
        }

        private static void SerializeGameInfo()
        {
            Dictionary<string, dynamic> game_info = new Dictionary<string, dynamic>()
            {
                { "musicbox_mode", CInfo.MusicboxMode },
                { "defeated_bosses", CInfo.DefeatedBosses },
                { "gp", CInfo.GP },
                { "difficulty", CInfo.Difficulty },
                { "atlas_strength", CInfo.AtlasStrength },
                { "musicbox_folder", CInfo.MusicboxFolder },
                { "current_tile", CInfo.CurrentTile },
                { "respawn_tile", CInfo.RespawnTile },
                { "do_spawns", CInfo.DoSpawns },
                { "has_cheated", CInfo.HasCheated }
            };

            string gameinfo_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_game_info}";
            File.WriteAllText(gameinfo_string, JsonConvert.SerializeObject(game_info, Formatting.Indented));
        }

        private static void SerializePartyMemebers()
        {
            string player_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_player}";
            File.WriteAllText(player_string, JsonConvert.SerializeObject(UnitManager.player, Formatting.Indented));

            string solou_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_solou}";
            File.WriteAllText(solou_string, JsonConvert.SerializeObject(UnitManager.solou, Formatting.Indented));

            string chili_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_chili}";
            File.WriteAllText(chili_string, JsonConvert.SerializeObject(UnitManager.chili, Formatting.Indented));

            string chyme_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_chyme}";
            File.WriteAllText(chyme_string, JsonConvert.SerializeObject(UnitManager.chyme, Formatting.Indented));

            string parsto_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_parsto}";
            File.WriteAllText(parsto_string, JsonConvert.SerializeObject(UnitManager.parsto, Formatting.Indented));

            string adorine_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_adorine}";
            File.WriteAllText(adorine_string, JsonConvert.SerializeObject(UnitManager.adorine, Formatting.Indented));

            string storm_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_storm}";
            File.WriteAllText(storm_string, JsonConvert.SerializeObject(UnitManager.storm, Formatting.Indented));

            string kaltoh_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_kaltoh}";
            File.WriteAllText(kaltoh_string, JsonConvert.SerializeObject(UnitManager.kaltoh, Formatting.Indented));
        }

        private static void SerializeInventory()
        {
            string inventory_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_inventory}";
            File.WriteAllText(inventory_string, JsonConvert.SerializeObject(InventoryManager.GetRawInventory(), Formatting.Indented));
        }

        private static void SerializeEquipment()
        {
            string equipment_string = $"{SavefileManager.base_dir}/{SavefileManager.temp_dir}/{SavefileManager.sav_equipment}";
            File.WriteAllText(equipment_string, JsonConvert.SerializeObject(InventoryManager.GetRawEquipment(), Formatting.Indented));
        }

        private static void SerializeDialogueFlags()
        {

        }

        private static void SerializeBossFlags()
        {

        }

        private static void SerializeChestFlags()
        {

        }

        private static void SerializeGems()
        {

        }
    }

    public static class JSONDeserializer
    {
        public static void DeserializeEverything()
        {

        }
    }
}
