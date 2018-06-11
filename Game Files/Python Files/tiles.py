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


class Tile:
    def __init__(self, name, tile_id, desc,
                 to_n=None, to_s=None, to_e=None, to_w=None, to_up=None, to_dn=None,
                 town_list=(), boss_list=(), gem_list=(),
                 allow_recursion=False, allow_oneway=False, allow_noneuclidean=False):
        self.name = name
        self.tile_id = tile_id
        self.desc = desc
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


class Cell:
    # A cell is a cluster of adjacent tiles accessible by teleportation via the world map
    def __init__(self, name, biome, tiles, primary_tile, m_level, cell_id):
        self.name = name
        self.biome = biome
        self.tiles = tiles
        self.primary_tile = primary_tile  # Where you appear when you teleport to this cell
        self.m_level = m_level  # A tuple that specifies the level range enemies can be encountered at
        self.cell_id = cell_id


class Province:
    # Provinces are sections of the world map that contain Cells. They are accessible via the world map,
    def __init__(self, name, cells, prov_id):
        self.name = name
        self.cells = cells
        self.prov_id = prov_id


# nearton_tile
nearton_desc = """\
Nearton is surrounded by a large, natural moat. Past that, trees as far as the
eyes can see."""

nearton_tile = Tile("Town of Nearton", "nearton_tile", nearton_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""",
                    town_list=[towns.town_nearton],
                    to_n="I-BF-N",
                    to_w="I-BF-W",
                    to_e="I-BF-E",
                    to_s="I-BF-S")
nearton_sw = Tile("Nearton Outskirts", "I-BF-SW", nearton_desc,
                  to_e="I-BF-S",
                  to_n="I-BF-W")
nearton_s = Tile("Nearton Outskirts", "I-BF-S", nearton_desc,
                 to_n="nearton_tile",
                 to_w="I-BF-SW",
                 to_e="I-BF-SE")
nearton_se = Tile("Nearton Outskirts", "I-BF-SE", nearton_desc,
                  to_w="I-BF-S",
                  to_n="I-BF-E")
nearton_w = Tile("Nearton Outskirts", "I-BF-W", nearton_desc,
                 to_s="I-BF-SW",
                 to_e="nearton_tile",
                 to_n="I-BF-NW")
nearton_e = Tile("Nearton Outskirts", "I-BF-E", nearton_desc,
                 to_n="I-BF-NE",
                 to_w="nearton_tile",
                 to_s="I-BF-SE")
nearton_nw = Tile("Nearton Outskirts", "I-BF-NW", nearton_desc,
                  to_s="I-BF-W",
                  to_e="I-BF-N")
nearton_n = Tile("Nearton Outskirts", "I-BF-N", nearton_desc,
                 to_s="nearton_tile",
                 to_e="I-BF-NE",
                 to_w="I-BF-NW",
                 gem_list=[items.amethyst_gem])
nearton_ne = Tile("Nearton Outskirts", "I-BF-NE", nearton_desc,
                  to_w="I-BF-N",
                  to_s="I-BF-E")

nearton_cell = Cell("Nearton", "forest", [nearton_tile,
                                          nearton_w,
                                          nearton_ne,
                                          nearton_e,
                                          nearton_s,
                                          nearton_n,
                                          nearton_se,
                                          nearton_nw,
                                          nearton_sw],
                    nearton_tile, (1, 4), "nearton_cell")

# southford_tile
southford_desc = """"""

southford_tile = Tile("Town of Southford", "southford_tile", southford_desc + """\n
The town of Southford is mere minutes away from this point! Stopping by
there might be a smart idea.""",
                      to_s="BF-2A",
                      to_w="BF-4A",
                      to_e="BF-6A",
                      to_n="BF-8A")
southford_sw = Tile("Southford Outskirts", "BF-1A", southford_desc,
                    to_e="BF-2A",
                    to_n="BF-4A")
southford_s = Tile("Southford Outskirts", "BF-2A", southford_desc,
                   to_w="BF-1A",
                   to_e="BF-3A",
                   to_n="southford_tile")
southford_se = Tile("Southford Outskirts", "BF-3A", southford_desc,
                    to_w="BF-2A",
                    to_n="BF-6A")
southford_w = Tile("Southford Outskirts", "BF-4A", southford_desc,
                   to_s="BF-1A",
                   to_e="southford_tile",
                   to_n="BF-7A")
southford_e = Tile("Southford Outskirts", "BF-6A", southford_desc,
                   to_s="BF-3A",
                   to_w="southford_tile",
                   to_n="BF-9A")
southford_nw = Tile("Southford Outskirts", "BF-7A", southford_desc,
                    to_s="BF-4A",
                    to_e="BF-8A")
southford_n = Tile("Southford Outskirts", "BF-8A", southford_desc,
                   to_s="southford_tile",
                   to_w="BF-7A",
                   to_e="BF-9A")
southford_ne = Tile("Southford Outskirts", "BF-9A", southford_desc,
                    to_s="BF-6A",
                    to_w="BF-8A")

southford_cell = Cell("Southford", "forest", [southford_tile,
                                              southford_w,
                                              southford_ne,
                                              southford_e,
                                              southford_s,
                                              southford_n,
                                              southford_se,
                                              southford_nw,
                                              southford_sw],
                      southford_tile, (2, 5), "southford_cell")
# OVERSHIRE
o_city_desc = """"""

o_city_tile = Tile("Overshire City", "o_city_tile", o_city_desc,
                   to_s="o_city_s",
                   to_w="o_city_w",
                   to_e="o_city_e",
                   to_n="o_city_n",
                   town_list=[towns.town_overshire_city])
o_city_sw = Tile("Overshire City Outskirts", "o_city_sw", o_city_desc,
                 to_e="o_city_s",
                 to_n="o_city_w")
o_city_s = Tile("Overshire City Outskirts", "o_city_s", o_city_desc,
                to_w="o_city_sw",
                to_e="o_city_se",
                to_n="o_city_tile")
o_city_se = Tile("Overshire City Outskirts", "o_city_se", o_city_desc,
                 to_w="o_city_s",
                 to_n="o_city_e")
o_city_w = Tile("Overshire City Outskirts", "o_city_w", o_city_desc,
                to_s="o_city_sw",
                to_e="o_city_tile",
                to_n="o_city_nw")
o_city_e = Tile("Overshire City Outskirts", "o_city_e", o_city_desc,
                to_w="o_city_tile",
                to_s="o_city_se",
                to_n="o_city_ne")
o_city_nw = Tile("Overshire City Outskirts", "o_city_nw", o_city_desc,
                 to_s="o_city_w",
                 to_e="o_city_n")
o_city_n = Tile("Overshire City Outskirts", "o_city_n", o_city_desc,
                to_s="o_city_tile",
                to_w="o_city_nw",
                to_e="o_city_ne")
o_city_ne = Tile("Overshire City Outskirts", "o_city_ne", o_city_desc,
                 to_s="o_city_e",
                 to_w="o_city_n")
o_city_cell = Cell("Overshire City", "forest", [o_city_tile,
                                                o_city_w,
                                                o_city_ne,
                                                o_city_e,
                                                o_city_s,
                                                o_city_n,
                                                o_city_se,
                                                o_city_nw,
                                                o_city_sw],
                   o_city_tile, (3, 6), "o_city_cell")
#
# bfor_tile_1c = Tile("Barrier Forest", "BF-1C", bfor_desc, 5,
#                     to_e="BF-2C",
#                     to_n="BF-4C")
# bfor_tile_2c = Tile("Barrier Forest", "BF-2C", bfor_desc, 5,
#                     to_e="BF-3C",
#                     to_n="BF-5C",
#                     to_w="BF-1C")
# bfor_tile_3c = Tile("Barrier Forest", "BF-3C", bfor_desc, 5,
#                     to_e="BF-1B",
#                     to_n="BF-6C",
#                     to_w="BF-2C")
# bfor_tile_4c = Tile("Barrier Forest", "BF-4C", bfor_desc, 5,
#                     to_e="BF-5C",
#                     to_n="BF-7C",
#                     to_s="BF-1C")
# bfor_tile_5c = Tile("Barrier Forest", "BF-5C", bfor_desc, 5,
#                     to_e="BF-6C",
#                     to_n="BF-8C",
#                     to_s="BF-2C",
#                     to_w="BF-4C")
# bfor_tile_6c = Tile("Barrier Forest", "BF-6C", bfor_desc, 5,
#                     to_e="BF-4B",
#                     to_s="BF-3C",
#                     to_w="BF-5C",
#                     to_n="BF-9C")
# bfor_tile_7c = Tile("Barrier Forest", "BF-7C", bfor_desc, 5,
#                     to_e="BF-8C",
#                     to_s="BF-4C")
# bfor_tile_8c = Tile("Barrier Forest", "BF-8C", bfor_desc, 5,
#                     to_e="BF-9C",
#                     to_s="BF-5C",
#                     to_w="BF-7C")
# bfor_tile_9c = Tile("Barrier Forest", "BF-9C", bfor_desc, 5,
#                     to_e="BF-7B",
#                     to_w="BF-8C",
#                     to_s="BF-6C")
overshire_province = Province("Overshire", [nearton_cell,
                                            southford_cell,
                                            o_city_cell],
                              "overshire_prov")

downpour_province = Province("Downpour", [], "downpour_prov")
flute_province = Province("Flute", [], "flute_prov")
deltora_province = Province("Deltora", [], "deltora_prov")
parriway_province = Province("Parriway", [], "parriway_prov")
chintor_province = Province("Chin'tor", [], "chintor_prov")
camberlite_province = Province("Camberlite", [], "camberlite_prov")
whitlock_province = Province("Whitlock", [], "whitlock_prov")
kohrin_province = Province("Kohrin", [], "kohrin_prov")
pelamora_province = Province("Pelamora", [], "pelamora_prov")
celemia_province = Province("Celemia", [], "celemia_prov")
thex_province = Province("Thex", [], "thex_prov")

all_provinces = [overshire_province,
                 downpour_province,
                 flute_province,
                 deltora_province,
                 parriway_province,
                 chintor_province,
                 camberlite_province,
                 whitlock_province,
                 kohrin_province,
                 pelamora_province,
                 celemia_province,
                 thex_province]
all_cells = [cell for sublist in [prov.cells for prov in all_provinces] for cell in sublist]
all_tiles = [tile for sublist in [cell.tiles for cell in all_cells] for tile in sublist]

# valid_provinces and valid_biomes are lists of strings that are allowed to be used as biome/proivince names
# This is to prevent errors such as typos and whatnot, as there's no reason to use any other biome/proivince names
valid_provinces = ["Overshire",
                   "Thex",
                   "Celemia",
                   "Pelamora",
                   "Parriway",
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
    # Input tile_id, get back the tile with the matching ID

    for tile in all_tiles:
        if tile.tile_id == tile_id:
            return tile

    return False


def find_cell_with_id(cell_id):
    # Input cell_id, get back the cell with the matching ID

    for cell in all_cells:
        if cell.cell_id == cell_id:
            return cell

    return False


def find_prov_with_id(prov_id):
    # Input prov_id, get back the province with the matching ID

    for prov in all_provinces:
        if prov.prov_id == prov_id:
            return prov

    return False


def find_prov_with_tile_id(tile_id):
    # Input tile_id, get back the province that contains the tile with matching ID

    tile = find_tile_with_id(tile_id)

    for prov in all_provinces:
        for cell in prov.cells:
            if tile in cell.tiles:
                return prov

    return False


def find_cell_with_tile_id(tile_id):
    # Input tile_id, get back the cell that contains the tile with matching ID

    tile = find_tile_with_id(tile_id)

    for cell in all_cells:
        if tile in cell.tiles:
            return cell

    return False


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


for item7 in all_cells:
    if item7.biome not in valid_biomes:
        print(f"{item7} has an invalid biome!")

for item8 in all_provinces:
    if item8.name not in valid_provinces:
        print(f"{item8} has an invalid province!")
