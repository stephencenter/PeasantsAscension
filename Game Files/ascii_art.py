#   This file is part of PythoniusRPG.
#
#	 PythoniusRPG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PythoniusRPG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PythoniusRPG.  If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------------#
# This file is where ALL of the Enemy and Player ASCII
# art in the game is located.

import colorama
from colorama import init, Fore, Style

init()

player_art = {
    "Ranger":
    """
                /   o'
                |*--|>
                \\   |
                   / \\
%s""",

    "Warrior":
    """
                   O   /
                []-|--'
                   |
                  / \\
%s""",

    "Mage":
    """
                 _^_
                  O
                `-|-
                 /_\\
                 ' '
%s""",

    "Assassin":
    """
                ,  O
                 \-|-\\
                   |  `
                  / \\
%s""",

    "Paladin":
    """
                   O [=]
                []-|--|
                   |
                  / \\
%s""",

    "Monk":
    """
                  O
                *-|-*
                 /_\\
                 ' '
%s""",

    "Asleep":
    """
                   z
                  z
                 Z
                o,--<
%s"""}


monster_art = {
    "Shell Mimic":
    """
/-----\\
 o P o
\-----/
        %s""",

    "Giant Crab":
    """
{}     {}
 \\_o-o_/
   \\ /
   ^ ^
        %s""",

    "Naiad":
    """
   O
/}-|-{\\
  / \\
        %s""",

    "Sea Serpent":
    """
\\   ___/^*
 \\_/
        %s""",

    "Squid":
    """
 \\[**]/
  |()|
 / || \\
/  ||  \\
        %s""",

    "Bog Slime":
    """
 /----\\
/______\\
        %s""",

    "Moss Ogre":
    """
    O
*--|-|--*
   |_|
  _/ \\_
        %s""",

    "Sludge Rat":
    """
~-[--]>
  *  *
        %s""",

    "Will-o'-the-wisp":
    """
  )\^^/(
 / o  o \\
|        |
 \______/
        %s""",

    "Vine Lizard":
    """
~-:=:>
        %s""",

    "Goblin Archer":
    """
  o  \\
--|--|
 / \\ /
        %s""",

    "Beetle":
    """
 ______
/______\C
 ''''''
        %s""",

    "Calculator":
    """
 ..
[==]
[==]
        %s""",

    "Spriggan":
    """
 }o{
3-|-E
 / \\
        %s""",

    "Imp":
    """
 'o'
 -|-
 / \\
        %s""",

    "Bat":
    """
/}-''-{\\
  ^  ^
        %s""",

    "Mummy":
    """
~o
 |==
 |
 |\\
        %s""",

    "Sand Golem":
    """
    O
*--|-|--*
   |_|
  _/ \\_
        %s""",

    "Minubis":
    """
  'n'
  /-\\
  | |
  \\-/
        %s""",

    "Fire Ant":
    """
O0o"
'\''
        %s""",

    "Naga":
    """
       o
      -|-
\\   ___/
 \\_/
        %s""",

    "Ice Soldier":
    """
  O   \\
--|--*|
  |   /
 / \\
        %s""",

    "Minor Yeti":
    """
    O
*--|-|--*
   |_|
  _/ \\_
        %s""",

    "Corrupt Thaumaturge":
    """
 _^_
  O
`-|-
 / \\
        %s""",

    "Arctic Wolf":
    """
    ^-,
~/--/
 `  `
        %s""",

    "Frost Bat":
    """
/}-''-{\\
  ^  ^
        %s""",

    "Troll":
    """
 O
-|-!
/ \\
        %s""",

    "Rock Giant":
    """
    O
*--|-|--*
   |_|
  _/ \\_
        %s""",

    "Oread":
    """
   O
/}-|-{\\
  / \\
        %s""",

    "Tengu":
    """
  'O>    ,
/}-|-{\\./
  / \\  /
        %s""",

    "Giant Worm":
    """
\\   ___/
 \\_/
        %s""",

    "Zombie":
    """
 o
 |==
 |
 |\\
        %s""",

    "Undead Archer":
    """
  O  \\
--|--*|
  |  /
 / \\
        %s""",

    "Necromancer":
    """
 _^_
  O
`-|-
 / \\
        %s""",

    "Skeleton":
    """
   O    \
--{|}--*|
  \\|/  /
  / \\
        %s""",

    "Ghoul":
    """
 O
-|-
/ \\
        %s""",

    "Whispering Goblin":
    """
\\ `o`
 `-|-
  / \\
        %s""",
    "Master Slime":
    """
   M
 /---\\
/_____\\
        %s""",

    "Terrible Tarantuloid":
    """
|   |
 \\o/
--0--
--0--
 / \\
        %s""",

    "Menacing Phantom":
    """
 (O)
~/ \\~
 | |
  V
        %s""",

    "Cursed Spectre":
    """
 (O)
~/ \\~
 | |
  V
        %s""",

    "Giant Ent":
    """
\\\\\\''///
  |oo|
  |~~|
  /vv\\
""",

    "Alicorn":
    """
         ,
  ~~\\ ">
 [===]'
/    |
        %s""",

    "Harpy":
    """
   O
/}-|-{\\
  / \\

        %s""",

    "Wraith":
    """
 (O)
~/ \\~
 | |
  V
        %s""",
    "Flying Serpent":
    """
    /''>
 /}-| |-{\\
/  ^| |^  \\
    | |
   _/ /
  <__/
        %s""",

    "Griffin":
    """
  ~~\\ ">
 [===]'
/    |
        %s""",

    "Hunter Lackey #1":
    """
"o> \\
<|-*|-
/ \ /
        %s""",

    "Hunter Lackey #2":
    """

"o> \\
<|-*|-
/ \ /
        %s""",

    "Typhen the Vampire Hunter":
    """
  "o> \\
 /-|-*|
' / \ /
        %s"""
}

# Sprites used for items (not yet implemented!)
item_sprites = {
    "Potion": Fore.RED + """
     _ _
     | |
    /   \\
    | P |
    \\___/
""" + Fore.RESET,
    "Elixir": Fore.BLUE + """
     _ _
     | |
    /   \\
    | E |
    \\___/
""" + Fore.RESET,

    "Bow":
        """
      ______
     /      \\
    /~~~~~~~~\\
""" + Fore.RESET,

    "Dagger":
        """
      /\\
      ||
     _||_
      ||
""" + Fore.RESET,

    "Short Sword":
        """
          /|
         //
        //
       //
    \_//_/
     //
""" + Fore.RESET,

    "Sword":
        """
            /|
           //
          //
         //
        //
       //
    \_//_/
     //

""" + Fore.RESET,

    "Fists":
        """
     ___
    /|||\\
    \\   /
     | |
""" + Fore.RESET,

    "Amulet":
        """
     ___
    /   \\
    |   |
     \ /
     {A}
""" + Fore.RESET,

    "Wizard Hat":
        """
        /\\
       /* \\
    __/  * \__
    ----------
""" + Fore.RESET,

    "Spear": Fore.WHITE + """
       ,
    """ + Fore.RED + """~~""" + Style.DIM + Fore.YELLOW + """/
     /
    /
""" + Style.RESET_ALL + Fore.RESET,

    "Axe": Fore.RED + """
    ^""" + Style.BRIGHT + Fore.BLACK + """_/\\""" + Style.DIM + Fore.YELLOW + """
    |""" + Style.BRIGHT + Fore.BLACK + """_  |""" + Style.DIM + Fore.YELLOW + """
    |""" + Style.BRIGHT + Fore.BLACK + """ \/""" + Style.DIM + Fore.YELLOW + """
    |
    |
    |
""" + Style.RESET_ALL + Fore.RESET,

    "Book":
        """
     _____
    |Livre|
    |=====|
    |     |
    |_____|
""" + Fore.RESET,

    "Compass":
        """
     _____
    /  N  \\
    W  ^> E
    \__S__/
""" + Fore.RESET,

    "Stiletto":
        """
     |
     |
    _|_
     |
""" + Fore.RESET,

    "Hammer":
    """
     ________
    |        |
    |________|
        ||
        ||
        ||
        ||
""" + Fore.RESET,

    "Mace":
    """
     ____
    |    |
    |____|
      ||
      ||
      ||
      ||
""" + Fore.RESET,

    "Knuckles": Fore.WHITE + """
     _  _  _  _
    / \/ \/ \/ \\
    \_/\_/\_/\_/
""" + Fore.RESET,

    "Gloves":
    """
    |\_/|
    |   |
     | |
""" + Fore.RESET,

    "Staff":
        """
    ~\O/~
      |
      |
      |
      |
""" + Fore.RESET,

    "Twig": Fore.GREEN + """
    `""" + Fore.YELLOW + Style.DIM + """/
     |
     /
""" + Style.RESET_ALL + Fore.RESET,

    "Crossbow":
        """
     ___/\___
    /   ||   \\
    \   ||   /
     \  ||  /
      ~~||~~
        ||
        ||
""" + Fore.RESET,

    "Hat":
        """
       ____
    __|____|__
    ----------
""" + Fore.RESET,

    "Shirt":
        """
     ____  ____
    |__  \/  __|
       |    |
       |    |
       |____|
""" + Fore.RESET,

    "Pants":
        """
     ______
    |      |
    |  __  |
    | |  | |
    | |  | |
    | |  | |
""" + Fore.RESET,

    "Helmet":
        """
    |\_____/|
    |  ___  |
    |_/   \_|
""" + Fore.RESET,

    "Robe":
        """
     ____  ____
    |__ *   *__|
       | *  |
       |   *|
       |____|
""" + Fore.RESET,

    "Robe Pants":
        """
        __
       / *\\
      /  * \\
     / *  * \\
    |________|
""" + Fore.RESET,

    "Misc":
        """
     ____
    /    \\
         |
        /
       /
       |
       O
""" + Fore.RESET,

    "Sling Shot":
        """
    |~~~~~|
     \___/
       |
       |
       |
""" + Fore.RESET,
    "Div Rod":
        """
    ~\   /~
      \_/
       |
       |=
       |
""" + Fore.RESET,

    "Gem":
        """
      _____
     /  _  \\
    |  |_|  |
     \_____/
""" + Fore.RESET,

    "Shovel":
        """
      __
     /  \\
    |____|
      ||
      ||
      ||
      ||
      ||
      /\\
     /==\\
""" + Fore.RESET,

    "Cap":
        """
       ____
    ~~/    \\
     | O__O |
      \/  \/
""" + Fore.RESET,

    "Wand":
        """
    []
    ||
    ||
    ||
    ||
""" + Fore.RESET,

    "Map":
        """
    |~~~~~~~~~|
    |  >>> x  |
    |   MAP   |
    |~~~~~~~~~|
""" + Fore.RESET,

    "Boots":
        """

    >>|---|
     >|   |____
      |        |
      |--------|
""" + Fore.RESET,

    "Healer Pet":
        """
       _
     _| |_
    |_PET_|
      |_|
""" + Fore.RESET,

    "Fighter Pet":
        """
      |
      | PET
    <-|-----<<
      |
      |
""" + Fore.RESET
}

for x in item_sprites.keys():
    print(item_sprites[x])