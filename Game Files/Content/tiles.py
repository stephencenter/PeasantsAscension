#   This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
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
icf_desc = """Your party lies in the inner portion of the Central Forest. This very forest
is home to thousands of people and animal species, and, unfortunately, several kinds
of monsters. There are trees in all directions as far as the eye can see, each
towering over a hundred feet tall. The ground is scattered with the occasional rock
and a plentiful supply of leaves twigs. In other words, it's your standard forest.
The Inner Central Forest makes up only a small fraction of the 150 million acre
Central Forest, and is surrounded by a 12-foot wide moat."""

in_for_n = Tile("Inner Central Forest", "I-CF-N", "Central Forest", icf_desc, 1,
                to_s="I-CF-C",
                to_e="Nearton",
                to_w="I-CF-NW",
                to_n="I-CF-Bridge")
in_for_s = Tile("Inner Central Forest", "I-CF-S", "Central Forest", icf_desc, 1,
                to_n="I-CF-C",
                to_w="Southford",
                to_e="I-CF-SE")
in_for_e = Tile("Inner Central Forest", "I-CF-E", "Central Forest", icf_desc, 1,
                to_n="Nearton",
                to_w="I-CF-C",
                to_s="I-CF-SE")
in_for_w = Tile("Inner Central Forest", "I-CF-W", "Central Forest", icf_desc, 1,
                to_s="Southford",
                to_e="I-CF-C",
                to_n="I-CF-NW")
in_for_c = Tile("Inner Central Forest", "I-CF-C", "Central Forest", icf_desc, 1,
                to_n="I-CF-N",
                to_w="I-CF-W",
                to_e="I-CF-E",
                to_s="I-CF-S")
in_for_nw = Tile("Inner Central Forest", "I-CF-NW", "Central Forest", icf_desc, 2,
                 to_s="I-CF-W",
                 to_e="I-CF-N")
in_for_se = Tile("Inner Central Forest", "I-CF-SE", "Central Forest", icf_desc, 2,
                 to_w="I-CF-S",
                 to_n="I-CF-E")

nearton_tile = Tile("Town of Nearton", "Nearton", "Central Forest", icf_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", 2,
                    town_list=[towns.town_nearton],
                    to_s="I-CF-E",
                    to_w="I-CF-N")

southford_tile = Tile("Town of Southford", "Southford", "Central Forest", icf_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", 2,
                      town_list=[towns.town_southford],
                      to_e="I-CF-S",
                      to_n="I-CF-W")

icf_bridge = Tile("Inner Forest Bridge", "I-CF-Bridge", "Central Forest", icf_desc + """\n
This bridge extends over the 12ft-wide moat surrounding the Inner Central Forest, meant
to help protect its citizens from the harmful monsters outside it. Weaker monsters still
manage to make their way in though.""", 0,
                  to_s="I-CF-N",
                  to_n="W-CF-2A")

# -- WEST OF THE HYTHOS RIVER -- #
whr_desc = """The Central Forest is divided into two smaller regions by the
immeasurably-large Hythos River. Your party lies to the West of this river,
in an area aptly-referred to as "West of the Hythos River". Known to the
denizens as "West Hythos", this land is home to dozens of towns and - despite
the efforts of the Harconian Militia - uncountable swaths of evils beasts.
While not nearly as dense tree-wise as the Inner Forest, West Hythos more than
makes makes up for it in size. Around 70% of the 150-million acre Central
Forest lies right here in West Hythos. Without a compass it would be incredibly
difficult to maintain ones whereabouts here."""

# Quadrant `A`
whr_tile_1a = Tile("West of the Hythos River", "W-CF-1A", "Central Forest", whr_desc, 3,
                   to_e="W-CF-2A",
                   to_n="W-CF-4A",
                   to_w="W-CF-3B")
whr_tile_2a = Tile("West of the Hythos River", "W-CF-2A", "Central Forest", whr_desc, 3,
                   to_s="I-CF-Bridge",
                   to_w="W-CF-1A",
                   to_e="W-CF-3A",
                   to_n="W-CF-5A")
whr_tile_3a = Tile("West of the Hythos River", "W-CF-3A", "Central Forest", whr_desc, 3,
                   to_w="W-CF-2A",
                   to_n="W-CF-6A")
whr_tile_4a = Tile("West of the Hythos River", "W-CF-4A", "Central Forest", whr_desc, 4,
                   to_s="W-CF-1A",
                   to_e="W-CF-5A",
                   to_n="W-CF-7A",
                   to_w="W-CF-6B")
whr_tile_5a = Tile("West of the Hythos River", "W-CF-5A", "Central Forest", whr_desc, 3,
                   to_s="W-CF-2A",
                   to_w="W-CF-4A",
                   to_e="W-CF-6A",
                   to_n="W-CF-8A")
whr_tile_6a = Tile("West of the Hythos River", "W-CF-6A", "Central Forest", whr_desc, 4,
                   to_s="W-CF-3A",
                   to_w="W-CF-5A",
                   to_n="W-CF-9A")
whr_tile_7a = Tile("West of the Hythos River", "W-CF-7A", "Central Forest", whr_desc, 4,
                   to_s="W-CF-4A",
                   to_e="W-CF-8A")
whr_tile_8a = Tile("West of the Hythos River", "W-CF-8A", "Central Forest", whr_desc, 4,
                   to_s="W-CF-5A",
                   to_w="W-CF-7A",
                   to_e="W-CF-9A")
whr_tile_9a = Tile("West of the Hythos River", "W-CF-9A", "Central Forest", whr_desc, 4,
                   to_s="W-CF-6A",
                   to_w="W-CF-8A")

# Quadrant `B`
whr_tile_1b = Tile("West of the Hythos River", "W-CF-1B", "Central Forest", whr_desc, 5,
                   to_e="W-CF-2B",
                   to_n="W-CF-4B")
whr_tile_2b = Tile("West of the Hythos River", "W-CF-2B", "Central Forest", whr_desc, 4,
                   to_w="W-CF-1B",
                   to_e="W-CF-3B",
                   to_n="W-CF-5B")
whr_tile_3b = Tile("West of the Hythos River", "W-CF-3B", "Central Forest", whr_desc, 3,
                   to_e="W-CF-1A",
                   to_w="W-CF-2B",
                   to_n="W-CF-6B")
whr_tile_4b = Tile("West of the Hythos River", "W-CF-4B", "Central Forest", whr_desc, 5,
                   to_s="W-CF-1B",
                   to_e="W-CF-5B",
                   to_n="W-CF-7B")
whr_tile_5b = Tile("West of the Hythos River", "W-CF-5B", "Central Forest", whr_desc, 4,
                   to_s="W-CF-2B",
                   to_w="W-CF-4B",
                   to_e="W-CF-6B",
                   to_n="W-CF-8B")
whr_tile_6b = Tile("West of the Hythos River", "W-CF-6B", "Central Forest", whr_desc, 3,
                   to_w="W-CF-5B",
                   to_e="W-CF-4A",
                   to_s="W-CF-3B",
                   to_n="W-CF-9B")
whr_tile_7b = Tile("West of the Hythos River", "W-CF-7B", "Central Forest", whr_desc, 5,
                   to_s="W-CF-4B",
                   to_e="W-CF-8B")
whr_tile_8b = Tile("West of the Hythos River", "W-CF-8B", "Central Forest", whr_desc, 4,
                   to_s="W-CF-5B",
                   to_w="W-CF-7B",
                   to_e="W-CF-9B")
whr_tile_9b = Tile("West of the Hythos River", "W-CF-9B", "Central Forest", whr_desc, 3,
                   to_s="W-CF-3B",
                   to_e="W-CF-4A",
                   to_w="W-CF-5B")


# -- CENTRAL FOREST TILESETS -- #

# Inner Central Forest
icf_tiles = [nearton_tile, southford_tile, in_for_c, in_for_w, in_for_e, in_for_s,
             in_for_n, in_for_se, in_for_nw, icf_bridge]

# West of the Hythos River
whr_tiles_q_a = [whr_tile_1a, whr_tile_2a, whr_tile_3a, whr_tile_4a, whr_tile_5a,
                 whr_tile_6a, whr_tile_7a, whr_tile_8a, whr_tile_9a]

whr_tiles_q_b = [whr_tile_1b, whr_tile_2b, whr_tile_3b, whr_tile_4b, whr_tile_5b,
                 whr_tile_6b, whr_tile_7b, whr_tile_8b, whr_tile_9b]


all_tiles = icf_tiles + whr_tiles_q_a + whr_tiles_q_b  # + other tiles lists as more tiles come into existence


def find_tile_with_id(tile_id):
    # A very simple function that scans through a list of all existing Tile objects and returns the first
    # one it finds with the inputted tile_id

    for tile in all_tiles:
        if tile.tile_id == tile_id:
            return tile

    return False

# These two loops run checks on the world map, checking for errors in order to prevent crashes
for item in copy.copy(locals()):
    if isinstance(locals()[item], Tile) and locals()[item] not in all_tiles:
        print(f"{locals()[item].tile_id} is not in all_tiles")

for item2 in copy.copy(locals()):
    if isinstance(locals()[item2], Tile):
        for direction in [locals()[item2].to_s, locals()[item2].to_n, locals()[item2].to_e, locals()[item2].to_w]:
            if direction and not find_tile_with_id(direction):
                print(f"{locals()[item2].tile_id} has an invalid direction ({direction})")
