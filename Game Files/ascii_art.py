#   This file is part of Peasants' Ascension.
#
#	 Peasants' Ascension is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Peasants' Ascension is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.
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

    "Anubis":
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
   O   \\
--{|}--*|
   |   /
  / \\
        %s""",

    "Ghoul":
    """
 O
-|-
/ \\
        %s""",

    "Goblin Chieftain":
    """
 , `o`
 |--|-
 | / \\
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

# Sprites used for items
item_sprites = {
    "Potion": Fore.RED + """
     _ _
     | |
    /   \\
    | P |
    \\___/
""" + Style.RESET_ALL + Fore.RESET,

    "Elixir": Fore.BLUE + """
     _ _
     | |
    /   \\
    | E |
    \\___/
""" + Style.RESET_ALL + Fore.RESET,

    "Rejuv": Fore.MAGENTA + """
     _ _
     | |
    /   \\
    | R |
    \\___/
""" + Style.RESET_ALL + Fore.RESET,

    "Status": Fore.YELLOW + """
     _ _
     | |
    /   \\
    | S |
    \\___/
""" + Style.RESET_ALL + Fore.RESET,

    "Bow": Style.DIM + Fore.YELLOW + """
      ______
     /      \\
    /""" + Style.RESET_ALL + Fore.WHITE + """~~~~~~~~""" + Style.DIM + Fore.YELLOW + """\\
""" + Style.RESET_ALL + Fore.RESET,

    "Dagger": Style.BRIGHT + Fore.BLACK + """
      /\\
      ||
     """ + Fore.RED + """_""" + Fore.BLACK + """||""" + Fore.RED + """_""" + Fore.BLACK + """
      ||
""" + Style.RESET_ALL + Fore.RESET,

    "Short Sword": Fore.WHITE + Style.DIM + """
          /|
         //
        //
       //
    """ + Fore.RED + """\_""" + Fore.WHITE + """//""" + Fore.RED + """_/
     """ + Fore.YELLOW + """//
""" + Style.RESET_ALL + Fore.RESET,

    "Sword": Fore.WHITE + Style.DIM + """
            /|
           //
          //
         //
        //
       //
    """ + Fore.RED + """\_""" + Fore.WHITE + """//""" + Fore.RED + """_/
     """ + Fore.YELLOW + """//
""" + Style.RESET_ALL + Fore.RESET,

    "Fists": Fore.YELLOW + """
     ___
    /|||\\
    \\   /
     | |
""" + Style.RESET_ALL + Fore.RESET,

    "Amulet": Fore.BLACK + Style.BRIGHT + """
     ___
    /   \\
    |   |
     \ /
     """ + Style.NORMAL + Fore.GREEN + """{A}
""" + Style.RESET_ALL + Fore.RESET,

    "Wizard Hat": Fore.BLUE + """
        /\\
       /""" + Fore.YELLOW + """*""" + Fore.BLUE + """ \\
    __/  """ + Fore.YELLOW + """*""" + Fore.BLUE + """ \__
    ----------
""" + Style.RESET_ALL + Fore.RESET,

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

    "Book": Fore.YELLOW + Style.DIM + """
     _____
    |""" + Style.RESET_ALL + Fore.WHITE + """Livre""" + Fore.YELLOW + Style.DIM + """|
    |""" + Fore.RED + Style.BRIGHT + """=====""" + Fore.YELLOW + Style.DIM + """|
    |     |
    |_____|
""" + Style.RESET_ALL + Fore.RESET,

    "Compass": Fore.BLUE + """
     _____
    /  """ + Fore.RED + """N""" + Fore.BLUE + """  \\""" + Fore.RED + """
    W  ^> E""" + Fore.BLUE + """
    \__""" + Fore.RED + """S""" + Fore.BLUE + """__/
""" + Style.RESET_ALL + Fore.RESET,

    "Stiletto": Fore.WHITE + Style.DIM + """
     |
     |
    _|_
     |
""" + Style.RESET_ALL + Fore.RESET,

    "Hammer": Style.BRIGHT + Fore.BLACK + """
     ________
    |        |
    |________|""" + Style.DIM + Fore.YELLOW + """
        ||
        ||
        ||
        ||
""" + Style.RESET_ALL + Fore.RESET,

    "Mace": Style.BRIGHT + Fore.BLACK + """
     ____
    |    |
    |____|""" + Style.DIM + Fore.YELLOW + """
      ||
      ||
      ||
      ||
""" + Style.RESET_ALL + Fore.RESET,

    "Knuckles": Fore.WHITE + """
     _  _  _  _
    / \/ \/ \/ \\
    \_/\_/\_/\_/
""" + Style.RESET_ALL + Fore.RESET,

    "Gloves": Style.BRIGHT + Fore.BLACK + """
    |\\""" + Style.DIM + Fore.YELLOW + """_""" + Style.BRIGHT + Fore.BLACK + """/|
    """ + Style.DIM + Fore.YELLOW + """|   |
     | |
""" + Style.RESET_ALL + Fore.RESET,

    "Staff": Fore.RED + """
    ~""" + Fore.YELLOW + """\\""" + Fore.BLUE + """O""" + Fore.YELLOW + """/""" + Fore.RED + """~
      """ + Fore.YELLOW + """|
      |
      |
      |
""" + Style.RESET_ALL + Fore.RESET,

    "Twig": Fore.GREEN + """
    `""" + Fore.YELLOW + Style.DIM + """/
     |
     /
""" + Style.RESET_ALL + Fore.RESET,

    "Crossbow": Style.DIM + Fore.YELLOW + """
     ___/\___
    /   ||   \\
    """ + Fore.WHITE + """\\""" + Style.DIM + Fore.YELLOW + """   ||   """ + Fore.WHITE + """/
     \\""" + Style.DIM + Fore.YELLOW + """  ||  """ + Fore.WHITE + """/
      ~~""" + Style.DIM + Fore.YELLOW + """||""" + Fore.WHITE + """~~"""
        + Style.DIM + Fore.YELLOW + """
        ||
        ||
        ||
""" + Style.RESET_ALL + Fore.RESET,

    "Hat": Fore.YELLOW + """
       ____
    __|____|__
    ----------
""" + Style.RESET_ALL + Fore.RESET,

    "Shirt": Style.DIM + Fore.YELLOW + """
     ____  ____
    |__  \/  __|
       |    |
       |    |
       |____|
""" + Style.RESET_ALL + Fore.RESET,

    "Pants": Style.DIM + Fore.YELLOW + """
     ______
    |      |
    |  __  |
    | |  | |
    | |  | |
    | |  | |
""" + Style.RESET_ALL + Fore.RESET,

    "Helmet": Style.DIM + Fore.YELLOW + """
    |\_____/|
    |  ___  |
    |_/   \_|
""" + Style.RESET_ALL + Fore.RESET,

    "Robe": Fore.BLUE + """
     ____  ____
    |__ """ + Fore.YELLOW + """*   *""" + Fore.BLUE + """__|
       | """ + Fore.YELLOW + """*""" + Fore.BLUE + """  |
       |   """ + Fore.YELLOW + """*""" + Fore.BLUE + """|
       |____|
""" + Style.RESET_ALL + Fore.RESET,

    "Robe Pants": Fore.BLUE + """
        __
       / """ + Fore.YELLOW + """*""" + Fore.BLUE + """\\
      /  """ + Fore.YELLOW + """*""" + Fore.BLUE + """ \\
     / """ + Fore.YELLOW + """*  *""" + Fore.BLUE + """ \\
    |________|
""" + Style.RESET_ALL + Fore.RESET,

    "Misc": Fore.WHITE + """
     ____
    /    \\
         |
        /
       /
       |
       O
""" + Style.RESET_ALL + Fore.RESET,

    "Sling Shot": Fore.YELLOW + Style.DIM + """
    |""" + Fore.WHITE + """~~~~~""" + Fore.YELLOW + """|
     \___/
       |
       |
       |
""" + Style.RESET_ALL + Fore.RESET,
    "Div Rod": Fore.RED + """
    ~""" + Fore.YELLOW + Style.DIM + """\   /""" + Style.NORMAL + Fore.RED + """~
      """ + Fore.YELLOW + Style.DIM + """\_/
       |
       |=
       |
""" + Style.RESET_ALL + Fore.RESET,

    "Gem": Fore.WHITE + """
      _____
     /  _  \\
    |  |_|  |
     \_____/
""" + Style.RESET_ALL + Fore.RESET,

    "Shovel": Style.BRIGHT + Fore.BLACK + """
      __
     /  \\
    |____|""" + Style.DIM + Fore.YELLOW + """
      ||
      ||
      ||
      ||
      ||
      /\\
     /""" + Style.BRIGHT + Fore.RED + """==""" + Style.DIM + Fore.YELLOW + """\\
""" + Style.RESET_ALL + Fore.RESET,

    "Cap": Style.DIM + Fore.YELLOW + """
       ____
    ~~/    \\
     | O__O |
      \/  \/
""" + Style.RESET_ALL + Fore.RESET,

    "Wand": Style.DIM + Fore.GREEN + """
    []""" + Fore.YELLOW + """
    ||
    ||
    ||
    ||
""" + Style.RESET_ALL + Fore.RESET,

    "Map": Fore.YELLOW + """
    |~~~~~~~~~|
    |  """ + Fore.RED + """>>> x  """ + Fore.YELLOW + """|
    |   """ + Fore.WHITE + """MAP   """ + Fore.YELLOW + """|
    |~~~~~~~~~|
""" + Style.RESET_ALL + Fore.RESET,

    "Boots": Fore.WHITE + """
    >>""" + Fore.YELLOW + Style.DIM + """|---|
     """ + Fore.WHITE + """>""" + Fore.YELLOW + Style.DIM + """|   |____
      |        |
      |--------|
""" + Style.RESET_ALL + Fore.RESET
}


locations = {
    'Terrius Mt. Range': """\
                                   _
                         .-.      / \        _
             ^^         /   \    /^./\__   _/ \\
           _        .--'\/\_ \__/.      \ /    \  ^^  ___
          / \_    _/ ^      \/  __  :'   /\/\  /\  __/   \\
         /    \  /    .'   _/  /  \   ^ /    \/  \/ .`'\_/\\
        /\/\  /\/ :' __  ^/  ^/    `--./.'  ^  `-.\ _    _:\ _
       /    \/  \  _/  \-' __/.' ^ _   \_   .'\   _/ \ .  __/ \\
     /\  .-   `. \/     \ / -.   _/ \ -. `_/   \ /    `._/  ^  \\
    /  `-.__ ^   / .-'.--'    . /    `--./ .-'  `-.  `-. `.  -  `.
  @/        `.  / /      `-.   /  .-'   / .   .'   \    \  \  .-  \%
---------------------------------------------------------------------""",

    'Arcadian Desert': """\
          \  :  /
           ' _ '
       -= ( (_) ) =-
           .   .
          /  :  \\
      .-.    '
      |.|
    /)|`|(\\
   (.(|'|)`)
~~~~`\`'./'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      |.|           ~~                                         ~~
      |`|                            ~~           ~~
     ,|'|.      (_)          ~~                         ~~
      "'"        \\"\                            ~~
           ~~     ^~^                ~~
---------------------------------------------------------------------""",

    "Harconian Coastline": """\
                                                 |
                                               \ _ /
                                            - = (_) = -
                                               /   \\
  ,\//,.\//\/.         ,\/,   ,\/.//,            |        ,~
  //o\\\\/o//o\\\\ ,.,.,   //o\   /o\\\\o\\\\                     |\\
    |   |  |  /###/#\    |     |  |                      /| \\
    |   |  |  |' '|:|    |`=.='|  |                     /_|__\\
----------------------------------------------------~~~~~~~~~~~~~~~~~""",
    "Glacian Plains": """\
                      *  .  *
                    . _\/ \/_ .
                     \  \ /  /             .      .
      ..    ..     -==>: X :<==-         _\/  \/_
      '\    /'       / _/ \_ \            _\/\/_
        \\\\//        '  /\ /\  '       _\_\_\/\/_/_/_
   _.__\\\\\///__._     *  '  *          / /_/\/\_\ \\
    '  ///\\\\\  '                          _/\/\_
        //\\\\                              /\  /\\
      ./    \.                            '      '
      ''    ''
---------------------------------------------------------------------""",
    "Central Forest": """\
            ,@@@@@@@,                         ,@@@@@@@,
    ,,,.   ,@@@@@@/@@,  .oo8888o.     ,,,.   ,@@@@@@/@@,  .oo8888o.
 ,&%%&%&&%,@@@@@/@@@@@@,8888\88/8o  ,&%%&%&&%,@@@@@/@@@@@@,8888\88/8o
,%&\%&&%&&%,@@@\@@@/@@@88\88888/88' ,%&\%&&%&&%,@@@\@@@/@@@88\88888/88'
%&&%&%&/%&&%@@\@@/ /@@@88888\88888' %&&%&%&/%&&%@@\@@/ /@@@88888\88888'
%&&%/ %&%%&&@@\ V /@@' `88\8 `/88' %&&%/ %&%%&&@@\ V /@@' `88\8 `/88'
`&%\ ` /%&'    |.|        \ '|8'    `&%\ ` /%&'    |.|        \ '|8'
    |o|        | |         | |          |o|        | |         | |
    |.|        | |         | |          |.|        | |         | |
---------------------------------------------------------------------""",
    "Bogthorn Marsh": """\
                    |                             |
                 \|\|/|/                       \|\|/|/
                \|\\\\|//|/                     \|\\\\|//|/
                 \|\|/|/                       \|\|/|/
  .-"'"-.         \\\\|//         .-"'"-.         \\\\|//       .-"'"-.
 /* * * *\         \|/         /* * * *\         \|/       /* * * *\\
:_.-:`:-._;        \|/        :_.-:`:-._;        \|/      :_.-:`:-._;
    (_)             |             (_)             |           (_)
 \|/(_)\|/ _\|/__|_\|/____\|/  \|/(_)\|/ _\|/_|__\|/____\|/\|/(_)\|/
---------------------------------------------------------------------""",
    "Overshire Graveyard": """\
        _.---,._,'
   /' _.--.<
     /'     `'
   /' _.---._____
   \.'   ___, .-'`
       /'    \\\\             .                     .
     /'       `-.          -|-                   -|-
    |                       |                     |
    |                   .-'~~~`-.             .-'~~~`-.
    |                 .'         `.         .'         `.
    |                 |  R  I  P  |         |  R  I  P  |
    |                 |           |         |           |
    |                 |           |         |           |
     \              \\\\|           |//     \\\\|           |//
---------------------------------------------------------------------""",
    "Aethus": """\
                     _  _
                   ( `   )_
                  (    )    `)
                (_   (_ .  _) _)
                                                _
                                               (  )
          _ .                              ( `  ) . )
        (  _ )_                           (_, _(  ,_)_)
      (_  _(_ ,)
---------------------------------------------------------------------""",
    "Campsite": """\
        ______
       /     /\\
      /     /  \\
     /_____/----\_    (
    "     "          ).
   _ ___          o (:') o
  (@))_))        o ~/~~\~ o
                  o  o  o
---------------------------------------------------------------------""",
    "Town": """\
    _H_              _H_               _H_                  o88o.
  .=|_|===========v==|_|============v==|_|===========.    (8%8898),
 /                |                 |                 \ ,(8888%8688)
/_________________|_________________|__________________(898%886886988)
|=|_|_|_|  =|_|_|=|X|)^^^(|X|=|/ \|=||_|_|_|=| ||_|_|=|`(86888%8%968)
|=|_|_|_|== |_|_|=|X|\___/|X|=||_||=||_____|=|_||_|_|=|___(88%%8888)
|=_________= ,-. =|""'""'""'"=""'""=|=_________== == =|_______\//`'
|=|__|__|_| //O\\\\=|X|""'""|X|=//"\\\\=|=|_|_|_|_| .---.=|.=====.||
|=|__|__|_|=|| ||=|X|_____|X|=|| ||=|=|_______|=||"||=||=====|||
|___________||_||_|=_________=||_||_|__________=|j_j|=|j==o==j| \\
---------------------------------------------------------------------""",
    "Castle": """\
                             o            o
                            /\            /\\
                           /\C\          /C/\\
      o        _   ___   _/  \/          \/  \_   ___   _        o
      /\      ]_]_[___]_[_[                  ]_]_[___]_[_[      /\\
     /%/\      |         |                    |         |      /\#\\
   _ \/__\  _  |   .-.   |___     ____     ___|   .-.   |  _  /__\/ _
  ]_]_[__]_[_[ |   ] [   |   |___|    |___|   |   ] [   | ]_]_[__]_[_[
   |     .-.|  |   ] [   |_______o____o_______|   ] [   |  |.-.     |
   |     ]_[|  |   ]_[   |.-.    /\  /\    .-.|   ]_[   |  |]_[     |
   |        |  |         |] [   /#/\/\%\   ] [|         |  |        |
   |.-.     |  |         |]_[   \/ /\ \/   ]_[|         |  |     .-.|
   |]_[     |  |   .-.   |        /  \        |   .-.   |  |     ]_[|
 __|   __   |__|   ] [   |   [][][][][][][]   |   ] [   |__|   __   |__
|  |__|  |__|  |   ] [   |  []_|_|_\/_|_|_[]  |   ] [   |  |__|  |__|  |
|______________|   ]_[   | []|_|_|_/\_|_|_|[] |   ]_[   |______________|
 |    .-.      |         |[]_|_|_|_\/_|_|_|_[]|         |     .-.     |
 |    ] [      |         |[]_|_|_|_/\_|_|_|_[]|         |     ] [     |
 |    ] [      |         |[]_|_|_|_\/_|_|_|_[]|         |     ] [     |
 |    ]_[      |         |[]_|_|_|_/\_|_|_|_[]|         |     ]_[     |
 |             |   ,),   |[]_|_|_|_\/_|_|_|_[]|   ,(,   |             |
 |    .-.      |   (,)   |[]_|_|_|_/\_|_|_|_[]|   (,)   |     .-.     |
 |    ] [      |   \_/   |[]\|/ \|/^^\|/ \|/[]|   \_/   |     ] [     |
 |    ] [      |  . | .  |[] '   '    '   ' []|  . | .  |     ] [     |
 |    ]_[      |   \|/   |[]                []|   \|/   |     ]_[     |
 |_____________|    !    |[]                []|    !    |_____________|
 ~~~~~~~~~~~~~~|_________|[]________________[]|_________|~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~/__-__-__-__-__-_\~~~~~~~~~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~~~~~/-__-__-__-__-__-__\~~~~~~~~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~~~~/__-__-__-__-__-__-__\~~~~~~~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~~~/______________________\~~~~~~~~~~~~~~~~~~~~~~~"""
}

# for x in locations.keys():
#     print(locations[x])

# for x in item_sprites.keys():
#     print(item_sprites[x])