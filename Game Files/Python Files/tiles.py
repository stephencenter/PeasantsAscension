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

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()
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


class Tile:
    def __init__(self, name, tile_id, province, desc, biome,  m_level,
                 to_n=None, to_s=None, to_e=None, to_w=None, to_up=None, to_dn=None,
                 town_list=(), boss_list=(), gem_list=(),
                 allow_recursion=False, allow_oneway=False, allow_noneuclidean=False):
        self.name = name
        self.tile_id = tile_id
        self.province = province
        self.desc = desc
        self.biome = biome
        self.m_level = m_level
        self.to_n = to_n
        self.to_s = to_s
        self.to_e = to_e
        self.to_w = to_w
        self.to_up = to_up
        self.to_dn = to_dn
        self.town_list = town_list
        self.boss_list = boss_list
        self.gem_list = gem_list

        # Allowing Recusion means that tiles can enter back into themselves. For example, tile_1.to_s = tile_1
        self.allow_recursion = allow_recursion

        # Allowing one-way paths means that tiles can have passages into other tiles that do not allow returning in the
        # direction one came from. For example, tile_1.to_s = tile_2; tile_2.to_n = None
        self.allow_oneway = allow_oneway

        # Allowing Non-euclidean geometry means that tiles can have passages that lead to different tiles when returning
        # in the direction one came from. For example, tile_1.to_s = tile_2, tile_2.to_n = tile_3
        self.allow_noneuclidean = allow_noneuclidean

        # NOTE: The above three restrictions are NOT hard restrictions! They simply give an alert when starting up the
        # game if one attempts to, for example, use non-euclidean geometry with allow_noneuclidean set to False.

    def generate_ascii(self):
        no_adj_tiles = len([t for t in [self.to_up,
                                        self.to_dn,
                                        self.to_w,
                                        self.to_s,
                                        self.to_n,
                                        self.to_e] if t is not None])

        # Calculate which tile ascii art to display
        if no_adj_tiles == 1:
            if self.to_n:
                return """
            | N |
            |   |
            | X |
            |___| X = Player Party\n"""

            elif self.to_s:
                return """
             ___
            |   |
            | X |
            |   |
            | S | X = Player Party\n"""

            elif self.to_w:
                return """
        ________
        W     X |
        ________| X = Player Party\n"""

            elif self.to_e:
                return """
             ________
            | X     E
            |________ X = Player Party\n"""

            elif self.to_dn or self.to_up:
                return """
             ___
            | X |
            |___| X = Player Party\n"""

        elif no_adj_tiles == 2:
            if self.to_n and self.to_w:
                return """
            | N |
        ____|   |
        W     X |
        ________| X = Player Party\n"""

            elif self.to_n and self.to_e:
                return """
            | N |
            |   |____
            | X    E
            |________ X = Player Party\n"""

            elif self.to_n and self.to_s:
                return """
            | N |
            |   |
            | X |
            |   |
            | S | X = Player Party\n"""

            elif self.to_w and self.to_e:
                return """
        _____________
        W     X     E
        _____________ X = Player Party\n"""

            elif self.to_w and self.to_s:
                return """
        ________
        W     X |
        ____    |
            |   |
            | S | X = Player Party\n"""

            elif self.to_e and self.to_s:
                return """
             ________
            | X     E
            |    ____
            |   |
            | S | X = Player Party\n"""

            elif self.to_up and self.to_dn:
                return """
             ___
            | X |
            |___| X = Player Party\n"""

            elif self.to_n and (self.to_up or self.to_dn):
                return """
            | N |
            |   |
            | X |
            |___| X = Player Party\n"""

            elif self.to_s and (self.to_up or self.to_dn):
                return """
             ___
            |   |
            | X |
            |   |
            | S | X = Player Party\n"""

            elif self.to_e and (self.to_up or self.to_dn):
                return """
             ________
            | X     E
            |________ X = Player Party\n"""

            elif self.to_w and (self.to_up or self.to_dn):
                return """
        ________
        W     X |
        ________| X = Player Party\n"""

        elif no_adj_tiles == 3:
            if self.to_n and self.to_w and self.to_e:
                return """
            | N |
        ____|   |____
        W     X     E
        _____________ X = Player Party\n"""

            elif self.to_n and self.to_w and self.to_s:
                return """
            | N |
        ____|   |
        W     X |
        ____    |
            |   |
            | S | X = Player Party\n"""

            elif self.to_n and self.to_e and self.to_s:
                return """
            | N |
            |   |____
            | X     E
            |    ____
            |   |
            | S | X = Player Party\n"""

            elif self.to_w and self.to_e and self.to_s:
                return """
        _____________
        W     X     E
        ____     ____
            |   |
            | S | X = Player Party\n"""

            elif self.to_w and self.to_n and (self.to_up or self.to_dn):
                return """
            | N |
        ____|   |
        W     X |
        ________| X = Player Party\n"""

            elif self.to_w and self.to_s and (self.to_up or self.to_dn):
                return """
        ________
        W     X |
        ____    |
            |   |
            | S | X = Player Party\n"""

            elif self.to_w and self.to_e and (self.to_up or self.to_dn):
                return """
        _____________
        W     X     E
        _____________ X = Player Party\n"""

            elif self.to_n and self.to_e and (self.to_up or self.to_dn):
                return """
            | N |
            |   |____
            | X    E
            |________ X = Player Party\n"""

            elif self.to_s and self.to_e and (self.to_up or self.to_dn):
                return """
             ________
            | X     E
            |    ____
            |   |
            | S | X = Player Party\n"""

            elif self.to_n and self.to_s and (self.to_up or self.to_dn):
                return """
            | N |
            |   |
            | X |
            |   |
            | S | X = Player Party\n"""

        elif no_adj_tiles >= 4:
            if self.to_n and self.to_w and self.to_e and self.to_s:
                return """
            | N |
        ____|   |____
        W     X     E
        ____     ____
            |   |
            | S | X = Player Party\n"""


# NEARTON
nearton_desc = """\
Nearton is surrounded by a large, natural moat. Past that, trees as far as the
eyes can see."""

nearton_tile = Tile("Town of Nearton", "NEARTON", "Overshire", nearton_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", "forest", 2,
                    town_list=[towns.town_nearton],
                    to_n="I-BF-N",
                    to_w="I-BF-W",
                    to_e="I-BF-E",
                    to_s="I-BF-S")
nearton_sw = Tile("Nearton Outskirts", "I-BF-SW", "Overshire", nearton_desc, "forest", 2,
                  to_e="I-BF-S",
                  to_n="I-BF-W")
nearton_s = Tile("Nearton Outskirts", "I-BF-S", "Overshire", nearton_desc, "forest", 1,
                 to_n="NEARTON",
                 to_w="I-BF-SW",
                 to_e="I-BF-SE")
nearton_se = Tile("Nearton Outskirts", "I-BF-SE", "Overshire", nearton_desc, "forest", 2,
                  to_w="I-BF-S",
                  to_n="I-BF-E")
nearton_w = Tile("Nearton Outskirts", "I-BF-W", "Overshire", nearton_desc, "forest", 1,
                 to_s="I-BF-SW",
                 to_e="NEARTON",
                 to_n="I-BF-NW")
nearton_e = Tile("Nearton Outskirts", "I-BF-E", "Overshire", nearton_desc, "forest", 1,
                 to_n="I-BF-NE",
                 to_w="NEARTON",
                 to_s="I-BF-SE")
nearton_nw = Tile("Nearton Outskirts", "I-BF-NW", "Overshire", nearton_desc, "forest", 2,
                  to_s="I-BF-W",
                  to_e="I-BF-N")
nearton_n = Tile("Nearton Outskirts", "I-BF-N", "Overshire", nearton_desc, "forest", 1,
                 to_s="NEARTON",
                 to_e="I-BF-NE",
                 to_w="I-BF-NW",
                 gem_list=[items.amethyst_gem])
nearton_ne = Tile("Nearton Outskirts", "I-BF-NE", "Overshire", nearton_desc, "forest", 1,
                  to_w="I-BF-N",
                  to_s="I-BF-E")

# SOUTHFORD
southford_desc = """"""

southford_tile = Tile("Town of Southford", "SOUTHFORD", "Overshire", southford_desc + """\n
The town of Southford is mere minutes away from this point! Stopping by
there might be a smart idea.""", "forest", 3,
                      to_s="BF-2A",
                      to_w="BF-4A",
                      to_e="BF-6A",
                      to_n="BF-8A")
southford_sw = Tile("Southford Outskirts", "BF-1A", "Overshire", southford_desc, "forest", 3,
                    to_e="BF-2A",
                    to_n="BF-4A")
southford_s = Tile("Southford Outskirts", "BF-2A", "Overshire", southford_desc, "forest", 3,
                   to_w="BF-1A",
                   to_e="BF-3A",
                   to_n="SOUTHFORD")
southford_se = Tile("Southford Outskirts", "BF-3A", "Overshire", southford_desc, "forest", 3,
                    to_w="BF-2A",
                    to_n="BF-6A")
southford_w = Tile("Southford Outskirts", "BF-4A", "Overshire", southford_desc, "forest", 3,
                   to_s="BF-1A",
                   to_e="SOUTHFORD",
                   to_n="BF-7A")
southford_e = Tile("Southford Outskirts", "BF-6A", "Overshire", southford_desc, "forest", 3,
                   to_s="BF-3A",
                   to_w="SOUTHFORD",
                   to_n="BF-9A")
southford_nw = Tile("Southford Outskirts", "BF-7A", "Overshire", southford_desc, "forest", 3,
                    to_s="BF-4A",
                    to_e="BF-8A")
southford_n = Tile("Southford Outskirts", "BF-8A", "Overshire", southford_desc, "forest", 3,
                   to_s="SOUTHFORD",
                   to_w="BF-7A",
                   to_e="BF-9A")
southford_ne = Tile("Southford Outskirts", "BF-9A", "Overshire", southford_desc, "forest", 3,
                    to_s="BF-6A",
                    to_w="BF-8A")

# OVERSHIRE
o_city_desc = """"""

o_city_tile = Tile("Overshire City", "BF-5B", "Overshire", o_city_desc, "forest", 4,
                   to_s="BF-2B",
                   to_w="BF-4B",
                   to_e="BF-6B",
                   to_n="BF-8B",
                   town_list=[towns.town_overshire_city])
o_city_sw = Tile("Overshire City Outskirts", "BF-1B", "Overshire", o_city_desc, "forest", 5,
                 to_e="BF-2B",
                 to_n="BF-4B")
o_city_s = Tile("Overshire City Outskirts", "BF-2B", "Overshire", o_city_desc, "forest", 5,
                to_w="BF-1B",
                to_e="BF-3B",
                to_n="BF-5B")
o_city_se = Tile("Overshire City Outskirts", "BF-3B", "Overshire", o_city_desc, "forest", 5,
                 to_w="BF-2B",
                 to_n="BF-6B")
o_city_w = Tile("Overshire City Outskirts", "BF-4B", "Overshire", o_city_desc, "forest", 5,
                to_s="BF-1B",
                to_e="BF-5B",
                to_n="BF-7B")
o_city_e = Tile("Overshire City Outskirts", "BF-6B", "Overshire", o_city_desc, "forest", 5,
                to_w="BF-5B",
                to_s="BF-3B",
                to_n="BF-9B")
o_city_nw = Tile("Overshire City Outskirts", "BF-7B", "Overshire", o_city_desc, "forest", 5,
                 to_s="BF-4B",
                 to_e="BF-8B")
o_city_n = Tile("Overshire City Outskirts", "BF-8B", "Overshire", o_city_desc, "forest", 5,
                to_s="BF-5B",
                to_w="BF-7B",
                to_e="BF-9B")
o_city_ne = Tile("Overshire City Outskirts", "BF-9B", "Overshire", o_city_desc, "forest", 5,
                 to_s="BF-6B",
                 to_w="BF-8B")
#
# bfor_tile_1c = Tile("Barrier Forest", "BF-1C", "Overshire", bfor_desc, "forest", 5, -7, 3,
#                     to_e="BF-2C",
#                     to_n="BF-4C")
# bfor_tile_2c = Tile("Barrier Forest", "BF-2C", "Overshire", bfor_desc, "forest", 5, -6, 3,
#                     to_e="BF-3C",
#                     to_n="BF-5C",
#                     to_w="BF-1C")
# bfor_tile_3c = Tile("Barrier Forest", "BF-3C", "Overshire", bfor_desc, "forest", 5, -5, 3,
#                     to_e="BF-1B",
#                     to_n="BF-6C",
#                     to_w="BF-2C")
# bfor_tile_4c = Tile("Barrier Forest", "BF-4C", "Overshire", bfor_desc, "forest", 5, -7, 4,
#                     to_e="BF-5C",
#                     to_n="BF-7C",
#                     to_s="BF-1C")
# bfor_tile_5c = Tile("Barrier Forest", "BF-5C", "Overshire", bfor_desc, "forest", 5, -6, 4,
#                     to_e="BF-6C",
#                     to_n="BF-8C",
#                     to_s="BF-2C",
#                     to_w="BF-4C")
# bfor_tile_6c = Tile("Barrier Forest", "BF-6C", "Overshire", bfor_desc, "forest", 5, -5, 4,
#                     to_e="BF-4B",
#                     to_s="BF-3C",
#                     to_w="BF-5C",
#                     to_n="BF-9C")
# bfor_tile_7c = Tile("Barrier Forest", "BF-7C", "Overshire", bfor_desc, "forest", 5, -7, 5,
#                     to_e="BF-8C",
#                     to_s="BF-4C")
# bfor_tile_8c = Tile("Barrier Forest", "BF-8C", "Overshire", bfor_desc, "forest", 5, -6, 5,
#                     to_e="BF-9C",
#                     to_s="BF-5C",
#                     to_w="BF-7C")
# bfor_tile_9c = Tile("Barrier Forest", "BF-9C", "Overshire", bfor_desc, "forest", 5, -5, 5,
#                     to_e="BF-7B",
#                     to_w="BF-8C",
#                     to_s="BF-6C")

# Overshire Tiles
nearton_tiles = [nearton_tile, nearton_w, nearton_ne, nearton_e, nearton_s,
                 nearton_n, nearton_se, nearton_nw, nearton_sw]
southford_tiles = [southford_tile, southford_w, southford_ne, southford_e, southford_s,
                   southford_n, southford_se, southford_nw, southford_sw]
o_city_tiles = [o_city_tile, o_city_w, o_city_ne, o_city_e, o_city_s, o_city_n,
                o_city_se, o_city_nw, o_city_sw]

overshire_tiles = nearton_tiles + southford_tiles + o_city_tiles

all_tiles = overshire_tiles

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


# This loop checks to make sure that every tile is in the all_tiles list, because otherwise
# the find_tile_with_id() function won't be able to access that tile.
for item in copy.copy(locals()):
    if isinstance(locals()[item], Tile) and locals()[item] not in all_tiles:
        print(f"{locals()[item].tile_id} is not in all_tiles!")

# This loop checks to make sure that all set directions for each tile correspond to valid tiles.
for item2 in all_tiles:
    for direction in [item2.to_s, item2.to_n, item2.to_e, item2.to_w]:
        if direction and not find_tile_with_id(direction):
            print(f"{item2.tile_id} has an invalid direction ({direction})!")

# This loop checks to make sure all tile_id's are unique
for item3 in all_tiles:
    if item3 != find_tile_with_id(item3.tile_id):
        print(f"{item3.tile_id} is being used as a Tile ID for multiple tiles!")

# This optional loop checks to make sure no tiles are "adjacent to themselves"
# e.g. North on tile_a leads to tile_a
for item4 in all_tiles:
    for direction in [item4.to_s, item4.to_n, item4.to_e, item4.to_w]:
        if direction == item4.tile_id and not item4.allow_recursion:
            print(f"{item4.tile_id} leads to itself - is this intended?")

# This optional loop checks to make sure tiles are two-way passages
# e.g. North on tile_a leads to tile_b, South on tile_b does nothing
for item5 in all_tiles:
    if any([item5.to_s and not find_tile_with_id(item5.to_s).to_n,
            item5.to_n and not find_tile_with_id(item5.to_n).to_s,
            item5.to_w and not find_tile_with_id(item5.to_w).to_e,
            item5.to_e and not find_tile_with_id(item5.to_e).to_w]) and not item5.allow_oneway:
        print(f"{item5.tile_id} has one-way passages - is this intended?")

# This optional loop checks to make sure all tiles are two-way passages that specifically correspond to eachother
# e.g. North on tile_a leads to tile_b, South on tile_b leads to tile_c
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

# This loop checks to make sure all tiles have valid province/biome names
for item7 in all_tiles:
    if item7.province not in valid_provinces:
        print(f"{item7.tile_id} has an invalid province name!")

    if item7.biome not in valid_biomes:
        print(f"{item7.tile_id} has an invalid biome name!")
