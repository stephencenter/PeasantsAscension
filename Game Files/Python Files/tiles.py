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

import copy
import sys

import pygame

import towns
import items
import units
from TileClass import Tile

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# -- Inner Forest -- #
if_desc = """Your party lies in the inner portion of the Barrier Forest. This
very forest is home to thousands of people and animal species, and,
unfortunately, several kinds of monsters. There are trees in all directions as
far as the eye can see, each towering over a hundred feet tall. The ground is
scattered with the occasional rock and a plentiful supply of leaves twigs. In
other words, it's your standard forest. The Inner Forest makes up only a
small fraction of the gargantuan Barrier Forest, and is surrounded by a
12-foot wide moat."""

in_for_n = Tile("Inner Forest", "I-BF-N", "Overshire", if_desc, "forest", 1, 0, 1,
                to_s="I-BF-C",
                to_e="I-BF-NE",
                to_w="I-BF-NW",
                to_n="I-BF-Bridge",
                gem_list=[items.amethyst_gem])
in_for_s = Tile("Inner Forest", "I-BF-S", "Overshire", if_desc, "forest", 1, 0, -1,
                to_n="I-BF-C",
                to_w="I-BF-SW",
                to_e="I-BF-SE",
                to_s="I-BF-SS")
in_for_e = Tile("Inner Forest", "I-BF-E", "Overshire", if_desc, "forest", 1, 1, 0,
                to_n="I-BF-NE",
                to_w="I-BF-C",
                to_s="I-BF-SE",
                to_e="I-BF-EE")
in_for_w = Tile("Inner Forest", "I-BF-W", "Overshire", if_desc, "forest", 1, -1, 0,
                to_s="I-BF-SW",
                to_e="I-BF-C",
                to_n="I-BF-NW",
                to_w="I-BF-WW")
in_for_c = Tile("Inner Forest", "I-BF-C", "Overshire", if_desc, "forest", 1, 0, 0,
                to_n="I-BF-N",
                to_w="I-BF-W",
                to_e="I-BF-E",
                to_s="I-BF-S")
in_for_nw = Tile("Inner Forest", "I-BF-NW", "Overshire", if_desc, "forest", 2, -1, 1,
                 to_s="I-BF-W",
                 to_e="I-BF-N",
                 to_w="I-BF-NWW")
in_for_se = Tile("Inner Forest", "I-BF-SE", "Overshire", if_desc, "forest", 2, 1, -1,
                 to_w="I-BF-S",
                 to_n="I-BF-E",
                 to_s="I-BF-SSE",
                 to_e="I-BF-SEE")
in_for_sw = Tile("Inner Forest", "I-BF-SW", "Overshire", if_desc, "forest", 2, -1, -1,
                 to_e="I-BF-S",
                 to_n="I-BF-W",
                 to_s="I-BF-SSW",
                 to_w="I-BF-SWW")
in_for_ww = Tile("Inner Forest", "I-BF-WW", "Overshire", if_desc, "forest", 2, -2, 0,
                 to_e="I-BF-W",
                 to_n="I-BF-NWW",
                 to_s="I-BF-SWW",
                 to_w="I-BF-WWW")
in_for_www = Tile("Inner Forest", "I-BF-WWW", "Overshire", if_desc, "forest", 3, -3, 0,
                  to_e="I-BF-WW",
                  to_n="I-BF-NWWW",
                  to_s="I-BF-SWWW",
                  gem_list=[items.opal_gem])
in_for_ee = Tile("Inner Forest", "I-BF-EE", "Overshire", if_desc, "forest", 2, 2, 0,
                 to_e="I-BF-EEE",
                 to_w="I-BF-E",
                 to_n="I-BF-NEE",
                 to_s="I-BF-SEE")
in_for_eee = Tile("Inner Forest", "I-BF-EEE", "Overshire", if_desc, "forest", 2, 3, 0,
                  to_w="I-BF-EE",
                  to_s="I-BF-SEEE",
                  to_n="I-BF-NEEE")
in_for_ss = Tile("Inner Forest", "I-BF-SS", "Overshire", if_desc, "forest", 2, 0, -2,
                 to_n="I-BF-S",
                 to_w="I-BF-SSW",
                 to_e="I-BF-SSE")
in_for_ssw = Tile("Inner Forest", "I-BF-SSW", "Overshire", if_desc, "forest", 2, -1, -2,
                  to_e="I-BF-SS",
                  to_n="I-BF-SW",
                  to_w="I-BF-SSWW")
in_for_sww = Tile("Inner Forest", "I-BF-SWW", "Overshire", if_desc, "forest", 2, -2, -1,
                  to_n="I-BF-WW",
                  to_e="I-BF-SW",
                  to_s="I-BF-SSWW",
                  to_w="I-BF-SWWW")
in_for_swww = Tile("Inner Forest", "I-BF-SWWW", "Overshire", if_desc, "forest", 3, -3, -1,
                   to_n="I-BF-WWW",
                   to_e="I-BF-SWW",
                   to_s="I-BF-SSWWW")
in_for_sswww = Tile("Inner Forest", "I-BF-SSWWW", "Overshire", if_desc, "forest", 3, -3, -2,
                    to_n="I-BF-SWWW",
                    to_e="I-BF-SSWW")
in_for_nww = Tile("Inner Forest", "I-BF-NWW", "Overshire", if_desc, "forest", 2, -2, 1,
                  to_w="I-BF-NWWW",
                  to_s="I-BF-WW",
                  to_e="I-BF-NW")
in_for_nwww = Tile("Inner Forest", "I-BF-NWWW", "Overshire", if_desc, "forest", 3, -3, 1,
                   to_e="I-BF-NWW",
                   to_s="I-BF-WWW",
                   boss_list=[units.whisp_goblin])
in_for_nee = Tile("Inner Forest", "I-BF-NEE", "Overshire", if_desc, "forest", 2, 2, 1,
                  to_e="I-BF-NEEE",
                  to_s="I-BF-EE",
                  to_w="I-BF-NE")
in_for_neee = Tile("Inner Forest", "I-BF-NEEE", "Overshire", if_desc, "forest", 3, 3, 1,
                   to_w="I-BF-NEE",
                   to_s="I-BF-EEE")
in_for_sse = Tile("Inner Forest", "I-BF-SSE", "Overshire", if_desc, "forest", 2, 1, -2,
                  to_n="I-BF-SE",
                  to_w="I-BF-SS",
                  to_e="I-BF-SSEE")
in_for_see = Tile("Inner Forest", "I-BF-SEE", "Overshire", if_desc, "forest", 2, 2, -1,
                  to_w="I-BF-SE",
                  to_n="I-BF-EE",
                  to_s="I-BF-SSEE",
                  to_e="I-BF-SEEE",
                  boss_list=[units.master_slime])
in_for_ssee = Tile("Inner Forest", "I-BF-SSEE", "Overshire", if_desc, "forest", 3, 2, -2,
                   to_n="I-BF-SEE",
                   to_w="I-BF-SSE",
                   to_e="I-BF-SSEEE")
in_for_seee = Tile("Inner Forest", "I-BF-SEEE", "Overshire", if_desc, "forest", 3, 3, -1,
                   to_n="I-BF-EEE",
                   to_w="I-BF-SEE",
                   to_s="I-BF-SSEEE")
in_for_sseee = Tile("Inner Forest", "I-BF-SSEEE", "Overshire", if_desc, "forest", 3, 3, -2,
                    to_n="I-BF-SEEE",
                    to_w="I-BF-SSEE")

nearton_tile = Tile("Town of Nearton", "I-BF-NE", "Overshire", if_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", "forest", 2, 1, 1,
                    town_list=[towns.town_nearton],
                    to_s="I-BF-E",
                    to_w="I-BF-N",
                    to_e="I-BF-NEE")

southford_tile = Tile("Town of Southford", "I-BF-SSWW", "Overshire", if_desc + """\n
The town of Southford is mere minutes away from this point! Stopping by
there might be a smart idea.""", "forest", 2, -2, -2,
                      town_list=[towns.town_southford],
                      to_e="I-BF-SSW",
                      to_n="I-BF-SWW",
                      to_w="I-BF-SSWWW")

if_bridge = Tile("Inner Forest Bridge", "I-BF-Bridge", "Overshire", if_desc + """\n
This bridge extends over the 12ft-wide moat surrounding the Inner Forest, meant
to help protect its citizens from the harmful monsters outside it. Weaker monsters still
manage to make their way in though.""", "forest", 1, 0, 2,
                 to_s="I-BF-N",
                 to_n="BF-2A")

# -- Barrier Forest -- #
bfor_desc = """The Barrier Forest is a massive forest that comprises about
one-third the area of the Overshire Province. With trees that tower over even
the tallest giants in Harconia, the towns here have made quite a fortune off
of selling lumber to the more barren parts of the Kingdom. The Barrier Forest 
is cut off from the rest of Overshire by the collosal Terrius Mountain Range, 
nearly impossible to climb without expensive equipment or flight magic. If one 
does wish to pass the Mountain, however, there are alternatives. A sprawling 
cave system known as the "Barrier Cave" is built into the mountain. If one were
brave enough, and strong enough, it would be possible to traverse this cave 
without dying. The environment in the Barrier Cave, while incredibly hostile to
humans and other civilized species, is the perfect breeding ground for powerful 
monsters."""

# Quadrant `A`
bfor_tile_1a = Tile("Barrier Forest", "BF-1A", "Overshire", bfor_desc, "forest", 3, -1, 3,
                    to_e="BF-2A",
                    to_n="BF-4A",
                    to_w="BF-3B")
bfor_tile_2a = Tile("Barrier Forest", "BF-2A", "Overshire", bfor_desc, "forest", 3, 0, 3,
                    to_s="I-BF-Bridge",
                    to_w="BF-1A",
                    to_e="BF-3A",
                    to_n="BF-5A")
bfor_tile_3a = Tile("Barrier Forest", "BF-3A", "Overshire", bfor_desc, "forest", 3, 1, 3,
                    to_w="BF-2A",
                    to_n="BF-6A")
bfor_tile_4a = Tile("Barrier Forest", "BF-4A", "Overshire", bfor_desc, "forest", 4, -1, 4,
                    to_s="BF-1A",
                    to_e="BF-5A",
                    to_n="BF-7A",
                    to_w="BF-6B")
bfor_tile_5a = Tile("Barrier Forest", "BF-5A", "Overshire", bfor_desc, "forest", 3, 0, 4,
                    to_s="BF-2A",
                    to_w="BF-4A",
                    to_e="BF-6A",
                    to_n="BF-8A")
bfor_tile_6a = Tile("Barrier Forest", "BF-6A", "Overshire", bfor_desc, "forest", 4, 1, 4,
                    to_s="BF-3A",
                    to_w="BF-5A",
                    to_n="BF-9A")
bfor_tile_7a = Tile("Barrier Forest", "BF-7A", "Overshire", bfor_desc, "forest", 4, -1, 5,
                    to_s="BF-4A",
                    to_e="BF-8A",
                    to_w="BF-9B")
bfor_tile_8a = Tile("Barrier Forest", "BF-8A", "Overshire", bfor_desc, "forest", 4, 0, 5,
                    to_s="BF-5A",
                    to_w="BF-7A",
                    to_e="BF-9A")
bfor_tile_9a = Tile("Barrier Forest", "BF-9A", "Overshire", bfor_desc, "forest", 4, 1, 5,
                    to_s="BF-6A",
                    to_w="BF-8A")

# Quadrant `B`
bfor_tile_1b = Tile("Barrier Forest", "BF-1B", "Overshire", bfor_desc, "forest", 5, -4, 3,
                    to_e="BF-2B",
                    to_n="BF-4B",
                    to_w="BF-3C")
bfor_tile_2b = Tile("Barrier Forest", "BF-2B", "Overshire", bfor_desc, "forest", 4, -3, 3,
                    to_w="BF-1B",
                    to_e="BF-3B",
                    to_n="BF-5B")
bfor_tile_3b = Tile("Barrier Forest", "BF-3B", "Overshire", bfor_desc, "forest", 3, -2, 3,
                    to_e="BF-1A",
                    to_w="BF-2B",
                    to_n="BF-6B")
bfor_tile_4b = Tile("Barrier Forest", "BF-4B", "Overshire", bfor_desc, "forest", 5, -4, 4,
                    to_s="BF-1B",
                    to_e="BF-5B",
                    to_n="BF-7B",
                    to_w="BF-6C")
bfor_tile_5b = Tile("Overshire City", "BF-5B", "Overshire", bfor_desc, "forest", 4, -3, 4,
                    to_s="BF-2B",
                    to_w="BF-4B",
                    to_e="BF-6B",
                    to_n="BF-8B",
                    town_list=[towns.town_overshire_city])
bfor_tile_6b = Tile("Barrier Forest", "BF-6B", "Overshire", bfor_desc, "forest", 3, -2, 4,
                    to_w="BF-5B",
                    to_e="BF-4A",
                    to_s="BF-3B",
                    to_n="BF-9B")
bfor_tile_7b = Tile("Barrier Forest", "BF-7B", "Overshire", bfor_desc, "forest", 5, -4, 5,
                    to_s="BF-4B",
                    to_e="BF-8B",
                    to_w="BF-9C")
bfor_tile_8b = Tile("Barrier Forest", "BF-8B", "Overshire", bfor_desc, "forest", 4, -3, 5,
                    to_s="BF-5B",
                    to_w="BF-7B",
                    to_e="BF-9B")
bfor_tile_9b = Tile("Barrier Forest", "BF-9B", "Overshire", bfor_desc, "forest", 3, -2, 5,
                    to_s="BF-6B",
                    to_e="BF-7A",
                    to_w="BF-8B")

bfor_tile_1c = Tile("Barrier Forest", "BF-1C", "Overshire", bfor_desc, "forest", 5, -7, 3,
                    to_e="BF-2C",
                    to_n="BF-4C")
bfor_tile_2c = Tile("Barrier Forest", "BF-2C", "Overshire", bfor_desc, "forest", 5, -6, 3,
                    to_e="BF-3C",
                    to_n="BF-5C",
                    to_w="BF-1C")
bfor_tile_3c = Tile("Barrier Forest", "BF-3C", "Overshire", bfor_desc, "forest", 5, -5, 3,
                    to_e="BF-1B",
                    to_n="BF-6C",
                    to_w="BF-2C")
bfor_tile_4c = Tile("Barrier Forest", "BF-4C", "Overshire", bfor_desc, "forest", 5, -7, 4,
                    to_e="BF-5C",
                    to_n="BF-7C",
                    to_s="BF-1C")
bfor_tile_5c = Tile("Barrier Forest", "BF-5C", "Overshire", bfor_desc, "forest", 5, -6, 4,
                    to_e="BF-6C",
                    to_n="BF-8C",
                    to_s="BF-2C",
                    to_w="BF-4C")
bfor_tile_6c = Tile("Barrier Forest", "BF-6C", "Overshire", bfor_desc, "forest", 5, -5, 4,
                    to_e="BF-4B",
                    to_s="BF-3C",
                    to_w="BF-5C",
                    to_n="BF-9C")
bfor_tile_7c = Tile("Barrier Forest", "BF-7C", "Overshire", bfor_desc, "forest", 5, -7, 5,
                    to_e="BF-8C",
                    to_s="BF-4C")
bfor_tile_8c = Tile("Barrier Forest", "BF-8C", "Overshire", bfor_desc, "forest", 5, -6, 5,
                    to_e="BF-9C",
                    to_s="BF-5C",
                    to_w="BF-7C")
bfor_tile_9c = Tile("Barrier Forest", "BF-9C", "Overshire", bfor_desc, "forest", 5, -5, 5,
                    to_e="BF-7B",
                    to_w="BF-8C",
                    to_s="BF-6C")


# -- Barrier Forest TILESETS -- #

# Inner Forest
icf_tiles = [nearton_tile, southford_tile, in_for_c, in_for_w, in_for_e, in_for_s, in_for_n, in_for_se, in_for_nw,
             if_bridge, in_for_ww, in_for_www, in_for_ee, in_for_eee, in_for_ss, in_for_sw, in_for_ssw, in_for_sww,
             in_for_swww, in_for_sswww, in_for_nww, in_for_nwww, in_for_nee, in_for_neee, in_for_sse, in_for_see,
             in_for_ssee, in_for_seee, in_for_sseee]

# Barrier Forest
bfor_tiles_q_a = [bfor_tile_1a, bfor_tile_2a, bfor_tile_3a, bfor_tile_4a, bfor_tile_5a,
                  bfor_tile_6a, bfor_tile_7a, bfor_tile_8a, bfor_tile_9a]

bfor_tiles_q_b = [bfor_tile_1b, bfor_tile_2b, bfor_tile_3b, bfor_tile_4b, bfor_tile_5b,
                  bfor_tile_6b, bfor_tile_7b, bfor_tile_8b, bfor_tile_9b]

bfor_tiles_q_c = [bfor_tile_1c, bfor_tile_2c, bfor_tile_3c, bfor_tile_4c, bfor_tile_5c,
                  bfor_tile_6c, bfor_tile_7c, bfor_tile_8c, bfor_tile_9c]

all_tiles = icf_tiles + bfor_tiles_q_a + bfor_tiles_q_b  + bfor_tiles_q_c

# valid_provinces and valid_biomes are lists of strings that are allowed to be used as biome/proivince names
# This is to prevent errors such as typos and whatnot, as there's no reason to use any other biome/proivince names
valid_provinces = ["Overshire",
                   "Thex",
                   "Celemia",
                   "Pelamora",
                   "Simphet",
                   "Camberlite",
                   "Kohrin",
                   "Deltora",  # Deltora quest was one of my favorite book series growing up <3
                   "Flute",
                   "Chin'tor",
                   "Whitlock",
                   "Downpour"]

valid_biomes = ["sky",
                "graveyard",
                "cave",
                "underworld",
                "castle",
                "desert",
                "forest",
                "shore",
                "swamp",
                "mountain",
                "tundra"]


def find_tile_with_id(tile_id):
    # A very simple function that scans through a list of all existing Tile objects and returns the first
    # one it finds with the inputted tile_id

    for tile in all_tiles:
        if tile.tile_id == tile_id:
            return tile

    return False

# These loops run checks on the world map, checking for errors in order to prevent crashes and weird behaviors
for item in copy.copy(locals()):
    if isinstance(locals()[item], Tile) and locals()[item] not in all_tiles:
        print(f"{locals()[item].tile_id} is not in all_tiles!")

for item2 in all_tiles:
    for direction in [item2.to_s, item2.to_n, item2.to_e, item2.to_w]:
        if direction and not find_tile_with_id(direction):
            print(f"{item2.tile_id} has an invalid direction ({direction})!")

for item3 in all_tiles:
    if item3 != find_tile_with_id(item3.tile_id):
        print(f"{item3.tile_id} is being used as a Tile ID for multiple tiles!")


for item4 in all_tiles:
    for direction in [item4.to_s, item4.to_n, item4.to_e, item4.to_w]:
        if direction == item4.tile_id and not item4.allow_recursion:
            print(f"{item4.tile_id} leads to itself - is this intended?")

for item5 in all_tiles:
    if any([item5.to_s and not find_tile_with_id(item5.to_s).to_n,
            item5.to_n and not find_tile_with_id(item5.to_n).to_s,
            item5.to_w and not find_tile_with_id(item5.to_w).to_e,
            item5.to_e and not find_tile_with_id(item5.to_e).to_w]) and not item5.allow_oneway:
        print(f"{item5.tile_id} has one-way passages - is this intended?")

for item6 in all_tiles:
    is_error = False

    if item6.to_s and find_tile_with_id(item6.to_s).to_n and not item6.allow_noneuclidean:
        if item6.tile_id != find_tile_with_id(item6.to_s).to_n and not item6.allow_noneuclidean:
            is_error = True

    if item6.to_n and find_tile_with_id(item6.to_n).to_s and not item6.allow_noneuclidean:
        if item6.tile_id != find_tile_with_id(item6.to_n).to_s and not item6.allow_noneuclidean:
            is_error = True

    if item6.to_w and find_tile_with_id(item6.to_w).to_e and not item6.allow_noneuclidean:
        if item6.tile_id != find_tile_with_id(item6.to_w).to_e and not item6.allow_noneuclidean:
            is_error = True

    if item6.to_e and find_tile_with_id(item6.to_e).to_w and not item6.allow_noneuclidean:
        if item6.tile_id != find_tile_with_id(item6.to_e).to_w and not item6.allow_noneuclidean:
            is_error = True

    if is_error:
        print(f"{item6.tile_id} has non-euclidean passages - is this intended?")

for item7 in all_tiles:
    if item7.province not in valid_provinces:
        print(f"{item7.tile_id} has an invalid province name!")

    if item7.biome not in valid_biomes:
        print(f"{item7.tile_id} has an invalid biome name!")

for tile1 in all_tiles:
    for tile2 in all_tiles:
        if tile1 != tile2 and tile1.x == tile2.x and tile1.y == tile2.y and tile1.z == tile2.z:
            print(f"{tile1.tile_id} and {tile2.tile_id} have the same coordiantes!")
