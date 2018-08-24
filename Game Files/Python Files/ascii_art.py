# This file is part of Peasants' Ascension.
#
# Peasants' Ascension is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peasants' Ascension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

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
                   _
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

    "Bard":
        """
                  _
                 /O\\
                *-|-*
                  |
                 / \\
    %s"""
}

# Sprites used for items
item_sprites = {
    "Potion": """\
     _ _
     | |
    /   \\
    | P |
    \\___/""",

    "Elixir": """\
     _ _
     | |
    /   \\
    | E |
    \\___/""",

    "Rejuv": """\
     _ _
     | |
    /   \\
    | R |
    \\___/""",

    "Status": """\
     _ _
     | |
    /   \\
    | S |
    \\___/""",

    "Alchemy": """\
     _ _
     | |
    /   \\
    | A |
    \\___/""",

    "Bow": """\
      ______
     /      \\
    /~~~~~~~~\\""",

    "Dagger": """\
      /\\
      ||
     _||_
      ||""",

    "Short Sword": """\
          /|
         //
        //
       //
    \_//_/
     //""",

    "Sword": """\
            /|
           //
          //
         //
        //
       //
    \_//_/
     //""",

    "Fists": """\
     ___
    /|||\\
    \\   /
     | |""",

    "Amulet": """\
     ___
    /   \\
    |   |
     \ /
     {A}""",

    "Wizard Hat": """\
        /\\
       /* \\
    __/  * \__
    ----------""",

    "Spear": """\
       ,
    ~~/
     /
    /""",

    "Axe": """\
    ^_/\\
    |_  |
    | \/
    |
    |
    |""",

    "Book": """\
     _____
    |Livre|
    |=====|
    |     |
    |_____|""",

    "Stiletto": """\
     |
     |
    _|_
     |""",

    "Hammer": """\
     ________
    |        |
    |________|
        ||
        ||
        ||
        ||""",

    "Mace": """\
     ____
    |    |
    |____|
      ||
      ||
      ||
      ||""",

    "Knuckles": """\
     _  _  _  _
    / \/ \/ \/ \\
    \_/\_/\_/\_/""",

    "Gloves": """\
        _  _  _ 
       | || || |
      _| || || |
     | | || || |
      \\        |
       \_______|""",

    "Staff": """\
    ~\\O/~
      |
      |
      |
      |""",

    "Twig": """\
    `/
     |
     /""",

    "Crossbow": """\
     ___/\___
    /   ||   \\
        ||   /
     \\  ||  /
      ~~||~~
        ||
        ||""",

    "Hat": """\
       ____
    __|____|__
    ----------""",

    "Shirt": """\
     ____  ____
    |__  \/  __|
       |    |
       |    |
       |____|""",

    "Pants": """\
     ______
    |      |
    |  __  |
    | |  | |
    | |  | |
    | |  | |""",

    "Helmet": """\
    |\_____/|
    |  ___  |
    |_/   \_|""",

    "Robe": """\
     ____  ____
    |__ *   *__|
       | *  |
       |   *|
       |____|""",

    "Robe Pants": """\
        __
       / *\\
      /  * \\
     / *  * \\
    |________|""",

    "misc": """\
     ____
    /    \\
         |
        /
       /
       |
       O""",

    "Sling Shot": """\
    |~~~~~|
     \___/
       |
       |
       |""",

    "Div Rod": """\
    ~\   /~
      \_/
       |
       |=
       |""",

    "Gem": """\
      _____
     /  _  \\
    |  |_|  |
     \_____/""",

    "Shovel": """\
      __
     /  \\
    |____|
      ||
      ||
      ||
      ||
      ||
      /\\
     /==\\""",

    "Cap": """\
       ____
    ~~/    \\
     | O__O |
      \/  \/""",

    "Wand": """\
    []
    ||
    ||
    ||
    ||""",

    "Map": """\
    |~~~~~~~~~|
    |  >>> x  |
    |   MAP   |
    |~~~~~~~~~|""",

    "Boots": """\
    >>|---|
     >|   |____
      |        |
      |--------|""",

    "Lockpick": """\
     ___
    |///|
    |---|
    |   |
    |___|""",

    "Music Box": """\
    ___  o   o
   | - | |   |
   |   |  \\ /
   |_o_|   |
      \\___/""",

    "alchemy_kit": """\
     _
    | |
    | |
    /-\\
   / - \\
  / --- \\
 /_______\\""",

    "hoe": """\
    ______
   /_____/
       //
      // 
     //
    //""",

    "kazoo": """\
        _
     __| |_______
    |___________/""",

    "flute": """\
     _______________________
    |_[O]_____o_o_o_o_o_o_o_|""",

    "drum": """\
    n_______n________n
    |\\      /\\      /|
    | \\    /  \\    / |
    |  \\  /    \\  /  |
    |___\\/______\\/___|
    u       u        u""",

    "trumpet": """\
                               /\\
          ________I_I_I_______/ |
    D====/  __________________  |
          \  \__|| || ||___/ /\\ |
           \________________/  \/
                 u  u  u""",

    "violin": """\
        =|||=
        =|||=
         |||
         |||
         |||
       _-|||-_
      /  |||  \\
      \\  |||  /
      / }ooo{ \\
      \\_______/""",

    "bagpipes": """\
         //
        //       //
      _//_____  //
     /        \\//_
    |             \\======
     \\____        /=====
       ||  \\     /=====
       ||   \\___/
       ||""",

    "kilt": """\
         ____
        |_|_||
       /_|_|_|\\
      /_|_|_|_|\\
     /_|_|_|_|_|\\
    /_|_|_|_|_|_|\\"""
}