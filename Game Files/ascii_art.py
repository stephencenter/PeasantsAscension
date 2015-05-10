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

player_art = {
    "Ranger":
    """
                / o'
                |*-|>
                \\/ \\
%s""",

    "Warrior":
    """
                   O  /
                []-|-'
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

    "Walking Venus":
    """
(--{
  |
  |
  -
 / \\
        %s""",

    "Vine Lizard":
    """
~-:=:>
        %s""",

    "Goblin":
    """
 o
-|-/
/ \\
        %s""",

    "Beetle":
    """
 ..
[==]
[==]
     %s""",

    "Sprite":
    """
   O
/}-|-{\\
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
 O
-|-/
 |
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

    "Undead Warrior":
    """
 O
-|-/
 |
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
   O
 -{|}-
  \\|/
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

}

# Sprites used for items (not yet implemented!)
item_sprites = {
    "Potion":
        """
     _ _
     | |
    /   \\
    | P |
    \\___/
""",

    "Bow":
        """
      ______
     /      \\
    /~~~~~~~~\\
""",

    "Dagger":
        """
    -|==>
""",

    "Short Sword":
        """
    -|===>
""",

    "Sword":
        """
    --|======>
""",

    "Fists":
        """
     ___
    /|||\\
    \\   /
     | |
""",

    "Amulet":
        """
     ___
    /   \\
    |   |
     \ /
     {A}
""",

    "Wizard Hat":
        """
        /\\
       /* \\
    __/  * \__
    ----------
""",

    "Spear":
        """
       ,
    ~~/
     /
    /
""",

    "Axe":
        """
    ^_/\\
    |_  |
    | \/
    |
    |
    |
""",

    "Book":
        """
     _____
    |Livre|
    |=====|
    |     |
    |_____|
""",

    "Compass":
        """
     _____
    /  N  \\
    W  ^> E
    \__S__/
""",

    "Stiletto":
        """
     |
     |
    _|_
     |
""",

    "Staff":
        """
    ~\O/~
      |
      |
      |
      |
""",

    "Twig":
        """
    `/
     |
     /
""",
    "Crossbow":
        """
     ___/\___
    /   ||   \\
    \   ||   /
     \  ||  /
      ~~||~~
        ||
        ||
""",

    "Hat":
        """
       ____
    __|____|__
    ----------
""",

    "Shirt":
        """
     ___|  |___
    |__      __|
       |    |
       |    |
       |____|
""",

    "Pants":
        """
     ______
    |      |
    |  __  |
    | |  | |
    | |  | |
    | |  | |
""",

    "Helmet":
        """
    |\_____/|
    |  ___  |
    |_/   \_|
""",

    "Robe":
        """
     ____  ____
    |__ *   *__|
       | *  |
       |   *|
       |____|
""",

    "Robe Pants":
        """
        __
       / *\\
      /  * \\
     / *  * \\
    |________|
"""
}