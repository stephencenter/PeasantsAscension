using Scripts;

namespace Main
{
    class ProgramUI
    {
        public void Run()
        {
            BattleManager.BattleSystem(false);
            CMethods.PressEnterReturn();
            /* Python Code
            def game_loop():
                party_info['music'] = tiles.find_cell_with_tile_id(party_info['current_tile'].tile_id).music
                sounds.play_music(party_info['music'])

                while True:
                    if not towns.search_towns():
                        print('-'*save_load.divider_size)

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

        private void DisplayTitlescreen()
        {

        }
    }
}
