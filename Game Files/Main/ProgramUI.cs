﻿using Scripts;

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
            /*
            party_info['music'] = tiles.find_cell_with_tile_id(party_info['current_tile'].tile_id).music
            sounds.play_music(party_info['music'])

            while True:
                if not towns.search_towns():
                    print('-' * save_load.divider_size)

                available_dirs = game_ui()

                while True:
                    party_info['gamestate'] = 'overworld'
                    command = s_input('Input Command (type "help" to view command list): ').lower()

                    if command == "debug-menu":
                        debug_command()

                    elif any(map(command.startswith, [x[0] for x in available_dirs])):
                        move_command(available_dirs, command[0])

                        break

                    elif command.startswith('p'):
                        stats_command()

                    elif command.startswith('m'):
                        magic_command()

                    elif command.startswith('i'):
                        inv_command()

                    elif command.startswith('t'):
                        tools_command()

                    elif command.startswith('l'):
                        look_command()

                    elif command.startswith('r'):
                        recheck_command()

                    elif command.startswith('c'):
                        title_screen.edit_settings()

                    elif command.startswith('h'):
                        help_command()

                    else:
                        continue

                    available_dirs = game_ui() */
        }

        private static void DisplayGameUI()
        {

        }

        private static void DisplayTitlescreen()
        {
            /*
            title_logo = @"\
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
             Peasants' Ascension {game_version} -- A Text-RPG by Stephen Center
Licensed under the GNU GPLv3: [https://www.gnu.org/copyleft/gpl.html]
Check here often for updates: [http://www.reddit.com/r/PeasantsAscension/]"
    { '-' * save_load.divider_size}

    sounds.play_music('../Music/Title Screen.flac')
    print(title_logo)

    while True:
        # Give the user a choice of keys to press to do specific actions
        choice = main.s_input('[P]lay Game | [S]ettings | [C]redits | [L]ore | [E]xit | Input Letter: ').lower()

        if choice.startswith('p'):
            return

        if choice.startswith("s") and not main.do_debug:
            edit_settings()
            print(title_logo)

        if choice.startswith('c') and not main.do_debug:
            show_credits()
            print(title_logo)

        if choice.startswith('l') and not main.do_debug:
            show_history()
            print(title_logo)

        if choice.startswith('e') and not main.do_debug:
            # Exit the game
            pygame.quit()
            sys.exit() */
        }

        private static void ShowCredits()
        {
            /*
            print('-'*save_load.divider_size)

            try:
                sounds.play_music('../Music/Credits Music for an 8-bit RPG.ogg')

                # Display the credits one line at a time with specific lengths
                # of time in between each line. Syncs up with the music!
                with open('../Credits.txt') as f:
                    for number, line in enumerate(f) :
                        print(''.join(line.split("\n")))
                        main.smart_sleep([0.75])

                    main.smart_sleep(3)

                    sounds.play_music('../Music/Title Screen.flac')

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
                        sounds.item_pickup.play()

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
