using Scripts;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Main
{
    internal static class ProgramUI
    {
        internal static void Run()
        {
            SavefileManager.ApplySettings();  // Set the volume and save file settings...
            DisplayTitlescreen();             // ...display the titlescreen...
            SavefileManager.LoadTheGame();    // ...check for save files...
            MainGameLoop();                   // ...and then start the game!
        }

        private static void MainGameLoop()
        {
            SoundManager.PlayCellMusic();

            while (true)
            {
                if (!TownManager.SearchForTowns())
                {
                    CMethods.PrintDivider();
                }

                DisplayGameUI();
                List<Tuple<char, string>> available_dirs = GetAvailableDirections();

                while (true)
                {
                    CInfo.Gamestate = CEnums.GameState.overworld;
                    string command = CMethods.Input("Input Command (type 'help' to view command list): ").ToLower();

                    if (command == "letmecheat")
                    {
                        // CommandManager.CheatCommand();
                    }

                    else if (available_dirs.Any(x => command.StartsWith(x.Item1.ToString())))
                    {
                        CommandManager.MoveCommand(available_dirs, command[0]);
                        break;
                    }

                    else if (command.StartsWith("p"))
                    {
                        // stats_command()
                    }

                    else if (command.StartsWith("m"))
                    {
                        // magic_command()
                    }

                    else if (command.StartsWith("i"))
                    {
                        // inv_command()
                    }

                    else if (command.StartsWith("t"))
                    {
                        // tools_command()
                    }

                    else if (command.StartsWith("l"))
                    {
                        // look_command()
                    }

                    else if (command.StartsWith("r"))
                    {
                        // recheck_command()
                    }

                    else if (command.StartsWith("c"))
                    {
                        // title_screen.edit_settings()
                    }

                    else if (command.StartsWith("h"))
                    {
                        // help_command()
                    }

                    else
                    {
                        continue;
                    }

                    DisplayGameUI();

                    available_dirs = GetAvailableDirections();
                }
            }
        }

        private static void DisplayGameUI()
        {
            Tile tile = TileManager.FindTileWithID(CInfo.CurrentTile);
            List<Tuple<char, string>> available_dirs = GetAvailableDirections();

            Console.WriteLine("-CURRENT LOCATION-");
            Console.WriteLine($"{tile.GenerateAsciiArt()}\n");
            Console.WriteLine($"Region [{tile.Name}] | Province: [{TileManager.FindProvinceWithTileID(tile.TileID).ProvinceName}]");

            foreach (Tuple<char, string> direction in available_dirs)
            {
                if (direction.Item1 == 'n')
                {
                    Console.Write("    To the [N]orth");
                }

                else if (direction.Item1 == 's')
                {
                    Console.Write("    To the [S]outh");
                }

                else if (direction.Item1 == 'e')
                {
                    Console.Write("    To the [E]ast");
                }

                else if (direction.Item1 == 'w')
                {
                    Console.Write("    To the [W]est");
                }

                string adj_tile = TileManager.FindTileWithID(direction.Item2).Name;
                Console.WriteLine($" lies the {adj_tile}");
            }
        }

        private static List<Tuple<char, string>> GetAvailableDirections()
        {
            List<Tuple<char, string>> available_dirs = new List<Tuple<char, string>>() { };
            Tile tile = TileManager.FindTileWithID(CInfo.CurrentTile);

            // Tells the player which directions are available to go in
            foreach (string location in new List<string>() { tile.ToNorth, tile.ToSouth, tile.ToEast, tile.ToWest })
            {
                if ((location == tile.ToNorth) && (location != null))
                {
                    available_dirs.Add(new Tuple<char, string>('n', location));
                }

                else if ((location == tile.ToSouth) && (location != null))
                {
                    available_dirs.Add(new Tuple<char, string>('s', location));
                }

                else if ((location == tile.ToEast) && (location != null))
                {
                    available_dirs.Add(new Tuple<char, string>('e', location));
                }

                else if ((location == tile.ToWest) && (location != null))
                {
                    available_dirs.Add(new Tuple<char, string>('w', location));
                }
            }

            return available_dirs;
        }

        private static void DisplayTitlescreen()
        {
            string title_card = $@"\
     ____                            _       _
    |  _ \ ___  __ _ ___  __ _ _ __ | |_ ___( )
    | |_) / _ \/ _` / __|/ _` | '_ \| __/ __|/
    |  __/  __/ (_| \__ \ (_| | | | | |_\__ \\
    |_|   \___|\__,_|___/\__,_|_| |_|\__|___/
            _                           _
        / \   ___  ___ ___ _ __  ___(_) ___  _ __
        / _ \ / __|/ __/ _ \ '_ \/ __| |/ _ \| '_ \\
        / ___ \\\__ \ (_|  __/ | | \__ \ | (_) | | | |
        /_/   \_\___/\___\___|_| |_|___/_|\___/|_| |_|
                Peasants' Ascension {CInfo.GameVersion} -- A Text-RPG by Stephen Center
    Licensed under the GNU GPLv3: [https://www.gnu.org/copyleft/gpl.html]
    Check here often for updates: [http://www.reddit.com/r/PeasantsAscension/]";
            SoundManager.title_music.PlayLooping();
            Console.WriteLine(title_card);
            CMethods.PrintDivider();

            while (true)
            {
                // Give the user a choice of keys to press to do specific actions
                string choice = CMethods.Input("[P]lay Game | [S]ettings | [C]redits | [E]xit | Input Letter: ").ToLower();

                if (choice.StartsWith("p"))
                {
                    return;
                }

                if (choice.StartsWith("s") && !CInfo.Debugging)
                {
                    EditSettings();
                    Console.WriteLine(title_card);
                }

                if (choice.StartsWith("c") && !CInfo.Debugging)
                {
                    ShowCredits();
                    Console.WriteLine(title_card);
                }

                if (choice.StartsWith("e") && !CInfo.Debugging)
                {
                    Environment.Exit(1);
                }
            }
        }

        private static void ShowCredits()
        {
            /*
            print('-'*save_load.divider_size)

            try:
                SoundManager.credits_music.PlayLooping();

                # Display the credits one line at a time with specific lengths
                # of time in between each line. Syncs up with the music!
                with open('../Credits.txt') as f:
                    for number, line in enumerate(f) :
                        print(''.join(line.split("\n")))
                        main.smart_sleep([0.75])

                    main.smart_sleep(3)

                    SoundManager.title_music.PlayLooping();

            except FileNotFoundError:
                # Display this is the Credits.txt file couldn't be found
                logging.exception(f'Error finding credits.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
                print('The "credits.txt" file could not be found.')
                main.s_input("\nPress enter/return ")

            except OSError:
                # If there is a problem opening the Credits.txt file, but it does exist,
                # display this message and log the error
                logging.exception(f'Error loading credits.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
                print('There was a problem opening "credits.txt".')
                main.s_input("\nPress enter/return ") */
        }

        private static void EditSettings()
        {
            /*
            if main.do_debug:
                return

            print('-' * save_load.divider_size)

            while True:
                print(f"""\
                Config Menu:
                [1] Music Volume--->Currently set to "{int(save_load.music_vol*100)}%"
                [2] Sound Volume--->Currently set to "{int(save_load.sound_vol*100)}%"
                [3] Divider Size--->Currently set to "{save_load.divider_size}"
                [4] Enable Blips--->Currently set to "{bool(save_load.do_blip)}\"""")

                while True:
                    setting = main.s_input('Input [#] (or type "back"): ').lower()

                    if setting == '1':
                        print('-' * save_load.divider_size)
                        set_vol("music")
                        print('-' * save_load.divider_size)

                        break

                    elif setting == '2':
                        print('-' * save_load.divider_size)
                        set_vol("sound")
                        print('-' * save_load.divider_size)

                        break

                    elif setting == '3':
                        print('-' * save_load.divider_size)
                        set_divider_size()
                        print('-' * save_load.divider_size)

                        break

                    elif setting == '4':
                        print('-' * save_load.divider_size)
                        toggle_do_blip()
                        print('-' * save_load.divider_size)

                        break

                    elif setting in ['e', 'x', 'exit', 'b', 'back']:
                        print('-'*save_load.divider_size)
                        return */
        }

        public static void SetVolume()
        {
            /*
            while True:
                c_volume = save_load.music_vol if mode == "music" else save_load.sound_vol

                print(f"{mode.title()} Volume determines how loud the {mode} is. 0 is silent, 100 is loud")
                print(f'{mode.title()} Volume is currently set to {int(c_volume*100)}%')

                do_thing = True
                while do_thing:
                    new_vol = main.s_input('Input # (or type "back"): ').lower()

                    if new_vol in ['e', 'x', 'exit', 'b', 'back']:
                        return
                    try:
                        # Convert the player's input into an integer between 0 and 100
                        new_vol = max(0, min(100, int(new_vol)))

                    except ValueError:
                        continue

                    print('-'*save_load.divider_size)
                    while True:
                        y_n = main.s_input(f"{mode.title()} Volume will be set to {new_vol}%, is that okay? | Y/N: ").lower()

                        if y_n.startswith("y"):
                            if mode == "music":
                                save_load.music_vol = new_vol/100
                                pygame.mixer.music.set_volume(new_vol/100)

                            elif mode == "sound":
                                save_load.sound_vol = new_vol/100
                                sounds.change_volume()

                            config = configparser.ConfigParser()

                            if not os.path.isfile("../settings.cfg"):
                                with open("../settings.cfg", mode= 'w') as f:
                                    f.write(save_load.settings_file)

                            config.read("../settings.cfg")
                            config.set("settings", f"{mode}_vol", str(new_vol))

                            with open("../settings.cfg", mode= "w") as g:
                                config.write(g)

                            print('-' * save_load.divider_size)
                            print(f'{mode.title()} Volume set to {new_vol}%.')
                            main.s_input("\nPress enter/return ")

                            return

                        elif y_n.startswith("n"):
                            print('-'*save_load.divider_size)
                            do_thing = False
                            break */

        }

        private static void ToggleBlips()
        {
            /*
            print("Blips are the sounds that the game make when you press enter.")
            print("They can get annoying, so you have the option to turn them off.")
            print(f'Blips are currently {"enabled" if save_load.do_blip else "disabled"}.')

            while True:
                y_n = main.s_input("Toggle Blips? | Y/N: ")

                if y_n.startswith('y'):
                    if save_load.do_blip:
                        sounds.item_pickup.stop()

                    else:
                        sounds.item_pickup.SmartPlay()

                    save_load.do_blip = not save_load.do_blip

                    config = configparser.ConfigParser()

                    if not os.path.isfile("../settings.cfg"):
                        with open("../settings.cfg", mode = 'w') as f:
                            f.write(save_load.settings_file)

                    config.read("../settings.cfg")
                    config.set("settings", "do_blip", str(int(save_load.do_blip)))

                    with open("../settings.cfg", mode = "w") as g:
                        config.write(g)

                    print('-' * save_load.divider_size)
                    print(f'Blips are now {"enabled" if save_load.do_blip else "disabled"}.')
                    main.s_input("\nPress enter/return ")

                    return

                elif y_n.startswith("n"):
                    return */
        }

        private static void SetDividerSize()
        {
            /*
            while True:
                print("Dividers are long strings of dashes that seperate different bits of text.")
                print("You can change the number of dashes if you want to. Max 80, min 5.")
                print(f"Current divider size: {save_load.divider_size} dashes")

                do_thing = True
                while do_thing:
                    div_size = main.s_input('Input # (or type "back"): ').lower()

                    if div_size in ['e', 'x', 'exit', 'b', 'back']:
                        return

                    try:
                        # Convert the player's input into an integer between 5 and 80
                        div_size = max(5, min(80, int(div_size)))

                    except ValueError:
                        continue

                    print('-' * save_load.divider_size)
                    while True:
                        y_n = main.s_input(f"Divider Size will be set to {div_size}, is that okay? | Y/N: ").lower()

                        if y_n.startswith("y"):
                            save_load.divider_size = div_size
                            config = configparser.ConfigParser()

                            if not os.path.isfile("../settings.cfg"):
                                with open("../settings.cfg", mode= 'w') as f:
                                    f.write(save_load.settings_file)

                            config.read("../settings.cfg")
                            config.set("settings", "divider_size", str(div_size))

                            with open("../settings.cfg", mode= "w") as g:
                                config.write(g)

                            print('-' * save_load.divider_size)
                            print(f'Divider Size set to {div_size}.')
                            main.s_input("\nPress enter/return ")

                            return

                        elif y_n.startswith("n"):
                            do_thing = False
                            break */
        }
    }
}
