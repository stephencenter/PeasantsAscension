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
        public const string sav_acquired_gems = "/acquired_gems.json";    // Acquired Gems
        public const string sav_def_bosses = "/def_bosses.json";          // Defeated Bosses
        public const string sav_equip_items = "/equip_items.json";        // Equipped Items
        public const string sav_inventory = "/inventory.json";            // Inventory
        public const string sav_misc_boss_info = "/misc_boss_info.json";  // Misc Boss Info
        public const string sav_party_info = "/party_info.json";          // Party Info
        public const string sav_quests_dia = "/quests_dia.json";          // Quests & Dialogue
        public const string sav_spellbook = "/spellbook.json";            // Spellbook
        public const string sav_chests = "/chests.json";                  // Chest Info

        // PCU Save Files
        public const string sav_play = "/play_stats.json";        // Player Stats
        public const string sav_solou = "/solou_stats.json";      // Solou"s Stats
        public const string sav_chili = "/chili_stats.json";      // Chili"s Stats
        public const string sav_chyme = "/chyme_stats.json";      // Chyme"s Stats
        public const string sav_parsto = "/parsto_stats.json";    // Parsto"s Stats
        public const string sav_adorine = "/adorine_stats.json";  // Adorine"s Stats
        public const string sav_ran_af = "/storm_stats.json";     // Storm"s Stats

        public const string base_dir = "../Save Files";
        public const string temp_dir = "temp";

        public static void SaveTheGame()
        {

        }

        public static void LoadTheGame()
        {
            /*
            global adventure_name

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
                main.party_info['musicbox_isplaying'] = False

                return */
        }

        public static void ApplySettings()
        {

        }
    }
}
