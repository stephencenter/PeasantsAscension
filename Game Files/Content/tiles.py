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
from TileClass import Tile

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# -- INNER CENTRAL FOREST -- #
icf_desc = """Your party lies in the inner portion of the Central Forest. This
very forest is home to thousands of people and animal species, and,
unfortunately, several kinds of monsters. There are trees in all directions as
far as the eye can see, each towering over a hundred feet tall. The ground is
scattered with the occasional rock and a plentiful supply of leaves twigs. In
other words, it's your standard forest. The Inner Central Forest makes up only a
small fraction of the 150 million acre Central Forest, and is surrounded by a
12-foot wide moat."""

in_for_n = Tile("Inner Central Forest", "I-CF-N", "Province of Overshire", icf_desc, "forest", 1,
                to_s="I-CF-C",
                to_e="I-CF-NE",
                to_w="I-CF-NW",
                to_n="I-CF-Bridge")
in_for_s = Tile("Inner Central Forest", "I-CF-S", "Province of Overshire", icf_desc, "forest", 1,
                to_n="I-CF-C",
                to_w="I-CF-SW",
                to_e="I-CF-SE",
                to_s="I-CF-SS")
in_for_e = Tile("Inner Central Forest", "I-CF-E", "Province of Overshire", icf_desc, "forest", 1,
                to_n="I-CF-NE",
                to_w="I-CF-C",
                to_s="I-CF-SE",
                to_e="I-CF-EE")
in_for_w = Tile("Inner Central Forest", "I-CF-W", "Central Forest", icf_desc, "forest", 1,
                to_s="I-CF-SW",
                to_e="I-CF-C",
                to_n="I-CF-NW",
                to_w="I-CF-WW")
in_for_c = Tile("Inner Central Forest", "I-CF-C", "Province of Overshire", icf_desc, "forest", 1,
                to_n="I-CF-N",
                to_w="I-CF-W",
                to_e="I-CF-E",
                to_s="I-CF-S")
in_for_nw = Tile("Inner Central Forest", "I-CF-NW", "Province of Overshire", icf_desc, "forest", 2,
                 to_s="I-CF-W",
                 to_e="I-CF-N",
                 to_w="I-CF-NWW")
in_for_se = Tile("Inner Central Forest", "I-CF-SE", "Province of Overshire", icf_desc, "forest", 2,
                 to_w="I-CF-S",
                 to_n="I-CF-E",
                 to_s="I-CF-SSE",
                 to_e="I-CF-SEE")
in_for_sw = Tile("Inner Central Forest", "I-CF-SW", "Province of Overshire", icf_desc, "forest", 2,
                 to_e="I-CF-S",
                 to_n="I-CF-W",
                 to_s="I-CF-SSW",
                 to_w="I-CF-SWW")
in_for_ww = Tile("Inner Central Forest", "I-CF-WW", "Province of Overshire", icf_desc, "forest", 2,
                 to_e="I-CF-W",
                 to_n="I-CF-NWW",
                 to_s="I-CF-SWW",
                 to_w="I-CF-WWW")
in_for_www = Tile("Inner Central Forest", "I-CF-WWW", "Province of Overshire", icf_desc, "forest", 3,
                  to_e="I-CF-WW",
                  to_n="I-CF-NWWW",
                  to_s="I-CF-SWWW")
in_for_ee = Tile("Inner Central Forest", "I-CF-EE", "Province of Overshire", icf_desc, "forest", 2,
                 to_e="I-CF-EEE",
                 to_w="I-CF-E",
                 to_n="I-CF-NEE",
                 to_s="I-CF-SEE")
in_for_eee = Tile("Inner Central Forest", "I-CF-EEE", "Province of Overshire", icf_desc, "forest", 2,
                  to_w="I-CF-EE",
                  to_s="I-CF-SEEE",
                  to_n="I-CF-NEEE")
in_for_ss = Tile("Inner Central Forest", "I-CF-SS", "Province of Overshire", icf_desc, "forest", 2,
                 to_n="I-CF-S",
                 to_w="I-CF-SSW",
                 to_e="I-CF-SSE")
in_for_ssw = Tile("Inner Central Forest", "I-CF-SSW", "Province of Overshire", icf_desc, "forest", 2,
                  to_e="I-CF-SS",
                  to_n="I-CF-SW",
                  to_w="I-CF-SSWW")
in_for_sww = Tile("Inner Central Forest", "I-CF-SWW", "Province of Overshire", icf_desc, "forest", 2,
                  to_n="I-CF-WW",
                  to_e="I-CF-SW",
                  to_s="I-CF-SSWW",
                  to_w="I-CF-SWWW")
in_for_swww = Tile("Inner Central Forest", "I-CF-SWWW", "Province of Overshire", icf_desc, "forest", 3,
                   to_n="I-CF-WWW",
                   to_e="I-CF-SWW",
                   to_s="I-CF-SSWWW")
in_for_sswww = Tile("Inner Central Forest", "I-CF-SSWWW", "Province of Overshire", icf_desc, "forest", 3,
                    to_n="I-CF-SWWW",
                    to_e="I-CF-SSWW")
in_for_nww = Tile("Inner Central Forest", "I-CF-NWW", "Province of Overshire", icf_desc, "forest", 2,
                  to_w="I-CF-NWWW",
                  to_s="I-CF-WW",
                  to_e="I-CF-NW")
in_for_nwww = Tile("Inner Central Forest", "I-CF-NWWW", "Province of Overshire", icf_desc, "forest", 3,
                   to_e="I-CF-NWW",
                   to_s="I-CF-WWW")
in_for_nee = Tile("Inner Central Forest", "I-CF-NEE", "Province of Overshire", icf_desc, "forest", 2,
                  to_e="I-CF-NEEE",
                  to_s="I-CF-EE",
                  to_w="I-CF-NE")
in_for_neee = Tile("Inner Central Forest", "I-CF-NEEE", "Province of Overshire", icf_desc, "forest", 3,
                   to_w="I-CF-NEE",
                   to_s="I-CF-EEE")
in_for_sse = Tile("Inner Central Forest", "I-CF-SSE", "Province of Overshire", icf_desc, "forest", 2,
                  to_n="I-CF-SE",
                  to_w="I-CF-SS",
                  to_e="I-CF-SSEE")
in_for_see = Tile("Inner Central Forest", "I-CF-SEE", "Province of Overshire", icf_desc, "forest", 2,
                  to_w="I-CF-SE",
                  to_n="I-CF-EE",
                  to_s="I-CF-SSEE",
                  to_e="I-CF-SEEE")
in_for_ssee = Tile("Inner Central Forest", "I-CF-SSEE", "Province of Overshire", icf_desc, "forest", 3,
                   to_n="I-CF-SEE",
                   to_w="I-CF-SSE",
                   to_e="I-CF-SSEEE")
in_for_seee = Tile("Inner Central Forest", "I-CF-SEEE", "Province of Overshire", icf_desc, "forest", 3,
                   to_n="I-CF-EEE",
                   to_w="I-CF-SEE",
                   to_s="I-CF-SSEEE")
in_for_sseee = Tile("Inner Central Forest", "I-CF-SSEEE", "Province of Overshire", icf_desc, "forest", 3,
                    to_n="I-CF-SEEE",
                    to_w="I-CF-SSEE")

nearton_tile = Tile("Town of Nearton", "I-CF-NE", "Province of Overshire", icf_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", "forest", 2,
                    town_list=[towns.town_nearton],
                    to_s="I-CF-E",
                    to_w="I-CF-N",
                    to_e="I-CF-NEE")

southford_tile = Tile("Town of Southford", "I-CF-SSWW", "Province of Overshire", icf_desc + """\n
The town of Southford is mere minutes away from this point! Stopping by
there might be a smart idea.""", "forest", 2,
                      town_list=[towns.town_southford],
                      to_e="I-CF-SSW",
                      to_n="I-CF-SWW",
                      to_w="I-CF-SSWWW")

icf_bridge = Tile("Inner Forest Bridge", "I-CF-Bridge", "Province of Overshire", icf_desc + """\n
This bridge extends over the 12ft-wide moat surrounding the Inner Central Forest, meant
to help protect its citizens from the harmful monsters outside it. Weaker monsters still
manage to make their way in though.""", "forest", 0,
                  to_s="I-CF-N",
                  to_n="W-CF-2A")

# -- CENTRAL FOREST -- #
cenf_desc = """The Central Forest is a massive forest that comprises about
one-third the area of the Overshire Province. With trees that tower over even
the tallest giants in Harconia, the towns here have made quite a fortune off
of selling lumber to the more barren parts of the Kingdom. Unfornunately, one
set of trees tends to look like another set of trees, and so it tends to be
incredibly difficult to maintain ones whereabouts here without a compass. The
Central Forest is cut off from the rest of Overshire by the collosal Terrius
Mountain Range, nearly impossible to climb without expensive equipment or flight
magic. If one does wish to pass the Mountain, however, there are alternatives.
A sprawling cave system known as the "Barrier Cave" is built into the mountain.
If one were brave enough, and strong enough, it would be possible to traverse
this cave without dying. The environment in the Barrier Cave, while incredibly
hostile to humans and other civilized species, is the perfect breeding ground
for powerful monsters."""

# Quadrant `A`
cenf_tile_1a = Tile("Central Forest", "W-CF-1A", "Province of Overshire", cenf_desc, "forest", 3,
                    to_e="W-CF-2A",
                    to_n="W-CF-4A",
                    to_w="W-CF-3B")
cenf_tile_2a = Tile("Central Forest", "W-CF-2A", "Province of Overshire", cenf_desc, "forest", 3,
                    to_s="I-CF-Bridge",
                    to_w="W-CF-1A",
                    to_e="W-CF-3A",
                    to_n="W-CF-5A")
cenf_tile_3a = Tile("Central Forest", "W-CF-3A", "Province of Overshire", cenf_desc, "forest", 3,
                    to_w="W-CF-2A",
                    to_n="W-CF-6A")
cenf_tile_4a = Tile("Central Forest", "W-CF-4A", "Province of Overshire", cenf_desc, "forest", 4,
                    to_s="W-CF-1A",
                    to_e="W-CF-5A",
                    to_n="W-CF-7A",
                    to_w="W-CF-6B")
cenf_tile_5a = Tile("Central Forest", "W-CF-5A", "Province of Overshire", cenf_desc, "forest", 3,
                    to_s="W-CF-2A",
                    to_w="W-CF-4A",
                    to_e="W-CF-6A",
                    to_n="W-CF-8A")
cenf_tile_6a = Tile("Central Forest", "W-CF-6A", "Province of Overshire", cenf_desc, "forest", 4,
                    to_s="W-CF-3A",
                    to_w="W-CF-5A",
                    to_n="W-CF-9A")
cenf_tile_7a = Tile("Central Forest", "W-CF-7A", "Province of Overshire", cenf_desc, "forest", 4,
                    to_s="W-CF-4A",
                    to_e="W-CF-8A",
                    to_w="W-CF-9B")
cenf_tile_8a = Tile("Central Forest", "W-CF-8A", "Province of Overshire", cenf_desc, "forest", 4,
                    to_s="W-CF-5A",
                    to_w="W-CF-7A",
                    to_e="W-CF-9A")
cenf_tile_9a = Tile("Central Forest", "W-CF-9A", "Province of Overshire", cenf_desc, "forest", 4,
                    to_s="W-CF-6A",
                    to_w="W-CF-8A")

# Quadrant `B`
cenf_tile_1b = Tile("Central Forest", "W-CF-1B", "Province of Overshire", cenf_desc, "forest", 5,
                    to_e="W-CF-2B",
                    to_n="W-CF-4B")
cenf_tile_2b = Tile("Central Forest", "W-CF-2B", "Province of Overshire", cenf_desc, "forest", 4,
                    to_w="W-CF-1B",
                    to_e="W-CF-3B",
                    to_n="W-CF-5B")
cenf_tile_3b = Tile("Central Forest", "W-CF-3B", "Province of Overshire", cenf_desc, "forest", 3,
                    to_e="W-CF-1A",
                    to_w="W-CF-2B",
                    to_n="W-CF-6B")
cenf_tile_4b = Tile("Central Forest", "W-CF-4B", "Province of Overshire", cenf_desc, "forest", 5,
                    to_s="W-CF-1B",
                    to_e="W-CF-5B",
                    to_n="W-CF-7B")
cenf_tile_5b = Tile("Central Forest", "W-CF-5B", "Province of Overshire", cenf_desc, "forest", 4,
                    to_s="W-CF-2B",
                    to_w="W-CF-4B",
                    to_e="W-CF-6B",
                    to_n="W-CF-8B")
cenf_tile_6b = Tile("Central Forest", "W-CF-6B", "Province of Overshire", cenf_desc, "forest", 3,
                    to_w="W-CF-5B",
                    to_e="W-CF-4A",
                    to_s="W-CF-3B",
                    to_n="W-CF-9B")
cenf_tile_7b = Tile("Central Forest", "W-CF-7B", "Province of Overshire", cenf_desc, "forest", 5,
                    to_s="W-CF-4B",
                    to_e="W-CF-8B")
cenf_tile_8b = Tile("Central Forest", "W-CF-8B", "Province of Overshire", cenf_desc, "forest", 4,
                    to_s="W-CF-5B",
                    to_w="W-CF-7B",
                    to_e="W-CF-9B")
cenf_tile_9b = Tile("Central Forest", "W-CF-9B", "Province of Overshire", cenf_desc, "forest", 3,
                    to_s="W-CF-6B",
                    to_e="W-CF-7A",
                    to_w="W-CF-8B")


# -- CENTRAL FOREST TILESETS -- #

# Inner Central Forest
icf_tiles = [nearton_tile, southford_tile, in_for_c, in_for_w, in_for_e, in_for_s, in_for_n, in_for_se, in_for_nw,
             icf_bridge, in_for_ww, in_for_www, in_for_ee, in_for_eee, in_for_ss, in_for_sw, in_for_ssw, in_for_sww,
             in_for_swww, in_for_sswww, in_for_nww, in_for_nwww, in_for_nee, in_for_neee, in_for_sse, in_for_see,
             in_for_ssee, in_for_seee, in_for_sseee]

# Central Forest
cenf_tiles_q_a = [cenf_tile_1a, cenf_tile_2a, cenf_tile_3a, cenf_tile_4a, cenf_tile_5a,
                  cenf_tile_6a, cenf_tile_7a, cenf_tile_8a, cenf_tile_9a]

cenf_tiles_q_b = [cenf_tile_1b, cenf_tile_2b, cenf_tile_3b, cenf_tile_4b, cenf_tile_5b,
                  cenf_tile_6b, cenf_tile_7b, cenf_tile_8b, cenf_tile_9b]


all_tiles = icf_tiles + cenf_tiles_q_a + cenf_tiles_q_b  # + other tiles lists as more tiles come into existence


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
