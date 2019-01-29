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
import random

import pygame

import towns
import items
import units

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
        if (no_adj_tiles == 1) 
        {
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
                return @"
                 ________
                | X     E
                |________ X = Player Party\n"
        }
            

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


class DungeonTile(Tile):
    def __init__(self, name, tile_id, desc, x, y, distance):
        super().__init__(name, tile_id, desc, None, None, None, None, None, None, [], [], [], False, False, False)

        self.x = x
        self.y = y
        self.distance = distance
        self.deadend = False


class Cell:
    # A cell is a cluster of adjacent tiles accessible by teleportation via the world map
    def __init__(self, name, m_level, store_level, music, enemy_groups, cell_id):
        self.name = name
        self.music = music
        self.enemy_groups = enemy_groups
        self.m_level = m_level  # A tuple that specifies the level range enemies can be encountered at
        self.store_level = store_level  # An integer that specifies what level the stores in this cell are at
        self.cell_id = cell_id


class RandomizedDungeon:
    def __init__(self, name, desc, m_level, x_cap, y_cap, num_floors, music, enemy_groups, cell_id):
        self.name = name
        self.desc = desc
        self.m_level = m_level
        self.x_cap = x_cap
        self.y_cap = y_cap
        self.num_floors = num_floors
        self.music = music
        self.enemy_groups = enemy_groups
        self.cell_id = cell_id

        self.generate_dungeon()

    def generate_dungeon(self):
        # This is an algorithm that is used to generate random mazes, called "dungeons".
        # First, generate a base tile at coordinates 0, 0, and add it to the list of tiles
        self.primary_tile = DungeonTile(f"Inside {self.name}", f"{self.cell_id}1", self.desc, 0, 0, 0)
        self.tiles = [self.primary_tile]

        # Set this tile as the "current tile"
        c_tile = self.primary_tile
        while True:
            # Randomly choose a direction to create a tile in. If there is already a tile in that spot,
            # checked using the tile_exists() method, or if that spot would be outside the maze boundaries,
            # then choose a different direction.
            direction = random.choice(["up", "left", "right", "down"])

            if direction == "up" and \
                    not self.tile_exists(c_tile.x, c_tile.y + 1) and \
                    not c_tile.y + 1 > self.y_cap:

                new_tile = DungeonTile(f"Inside {self.name}", f"{self.cell_id}{len(self.tiles) + 1}",
                                       self.desc, c_tile.x, c_tile.y + 1, c_tile.distance + 1)

                self.tiles.append(new_tile)
                c_tile.to_n = new_tile.tile_id
                new_tile.to_s = c_tile.tile_id

                c_tile = new_tile

            elif direction == "down" and \
                    not self.tile_exists(c_tile.x, c_tile.y - 1) and \
                    not c_tile.y - 1 < 0:

                new_tile = DungeonTile(f"Inside {self.name}", f"{self.cell_id}{len(self.tiles) + 1}",
                                       self.desc, c_tile.x, c_tile.y - 1, c_tile.distance + 1)

                self.tiles.append(new_tile)
                c_tile.to_s = new_tile.tile_id
                new_tile.to_n = c_tile.tile_id
                c_tile = new_tile

            elif direction == "right" and \
                    not self.tile_exists(c_tile.x + 1, c_tile.y) and \
                    (self.x_cap > c_tile.x + 1 > -self.x_cap):

                new_tile = DungeonTile(f"Inside {self.name}", f"{self.cell_id}{len(self.tiles) + 1}",
                                       self.desc, c_tile.x + 1, c_tile.y, c_tile.distance + 1)

                self.tiles.append(new_tile)
                c_tile.to_e = new_tile.tile_id
                new_tile.to_w = c_tile.tile_id
                c_tile = new_tile

            elif direction == "left" and \
                    not self.tile_exists(c_tile.x - 1, c_tile.y) and \
                    (self.x_cap > c_tile.x - 1 > -self.x_cap):

                new_tile = DungeonTile(f"Inside {self.name}", f"{self.cell_id}{len(self.tiles) + 1}",
                                       self.desc, c_tile.x - 1, c_tile.y, c_tile.distance + 1)

                self.tiles.append(new_tile)
                c_tile.to_w = new_tile.tile_id
                new_tile.to_e = c_tile.tile_id
                c_tile = new_tile

            else:
                # If all directions are either out of bounds or have a tile located there already, then the algorithm
                # has reached a 'dead-end'. We mark the tile as a dead end, because dead ends are where items and
                # bosses can be found.
                if not self.has_free_adjacent_space(c_tile.x, c_tile.y):
                    c_tile.deadend = True

                    for n_tile in self.tiles:
                        # If the algorithm reaches a dead end, then it will search through the list of tiles
                        # until it finds one that has an available space next to it.
                        if self.has_free_adjacent_space(n_tile.x, n_tile.y):
                            c_tile = n_tile

                            break

                    # If no tile can be found with a free adjacent space next to it, then the maze generation is
                    # complete. 
                    else:
                        return

    def tile_exists(self, x, y):
        for tile in self.tiles:
            if x == tile.x and y == tile.y:
                return True

        return False

    def has_free_adjacent_space(self, x, y):
        return not all([
            (self.tile_exists(x - 1, y) or not (self.x_cap > x - 1 > -self.x_cap)),
            (self.tile_exists(x + 1, y) or not (self.x_cap > x + 1 > -self.x_cap)),
            (self.tile_exists(x, y + 1) or y + 1 > self.y_cap),
            (self.tile_exists(x, y - 1) or y - 1 < 0)
        ])


class Province:
    # Provinces are sections of the world map that contain Cells. They are accessible via the world map,
    def __init__(self, name, cells, prov_id):
        self.name = name
        self.cells = cells
        self.prov_id = prov_id


# =========================== #
#       OVERSHIRE CELLS       #
# =========================== #

# NEARTON
class NeartonCell(Cell):
    def __init__(self, name, m_level, store_level, music, enemy_groups, cell_id):
        super().__init__(name, m_level, store_level, music, enemy_groups, cell_id)
        # I create a dedicated class for each cell so I can put all of the tile data inside it, keeping
        # the file clean and easy to read

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
                         to_e="I-BF-SE",
                         boss_list=[units.master_slime])
        nearton_se = Tile("Nearton Outskirts", "I-BF-SE", nearton_desc,
                          to_w="I-BF-S",
                          to_n="I-BF-E",
                          gem_list=[items.agate_gem])
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
                          to_e="I-BF-N",
                          boss_list=[units.goblin_chieftain])
        nearton_n = Tile("Nearton Outskirts", "I-BF-N", nearton_desc,
                         to_s="nearton_tile",
                         to_e="I-BF-NE",
                         to_w="I-BF-NW",
                         gem_list=[items.amethyst_gem])
        nearton_ne = Tile("Nearton Outskirts", "I-BF-NE", nearton_desc,
                          to_w="I-BF-N",
                          to_s="I-BF-E")

        self.tiles = [nearton_tile,
                      nearton_w,
                      nearton_ne,
                      nearton_e,
                      nearton_s,
                      nearton_n,
                      nearton_se,
                      nearton_nw,
                      nearton_sw]
        self.primary_tile = nearton_tile


nearton_cell = NeartonCell("Nearton", (1, 3), 1, "../Music/Through the Forest.ogg",
                           [units.animal_group, units.monster_group], "nearton_cell")


# SOUTHFORD
class SouthfordCell(Cell):
    def __init__(self, name, m_level, store_level, music, enemy_groups, cell_id):
        super().__init__(name, m_level, store_level, music, enemy_groups, cell_id)

        southford_desc = """"""

        southford_tile = Tile("Town of Southford", "southford_tile", southford_desc + """\n
        The town of Southford is mere minutes away from this point! Stopping by
        there might be a smart idea.""",
                              town_list=[towns.town_southford],
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
                           to_n="BF-7A",
                           gem_list=[items.sapphire_gem])
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

        self.tiles = [southford_tile,
                      southford_w,
                      southford_ne,
                      southford_e,
                      southford_s,
                      southford_n,
                      southford_se,
                      southford_nw,
                      southford_sw]
        self.primary_tile = southford_tile


southford_cell = SouthfordCell("Southford", (2, 4), 2, '../Music/Through the Forest.ogg',
                               [units.animal_group, units.monster_group], "southford_cell")


# OVERSHIRE CITY
class OvershireCityCell(Cell):
    def __init__(self, name, m_level, store_level, music, enemy_groups, cell_id):
        super().__init__(name, m_level, store_level, music, enemy_groups, cell_id)

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
                        to_n="o_city_tile",
                        gem_list=[items.citrine_gem])
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
                         to_w="o_city_n",
                         gem_list=[items.garnet_gem])

        self.tiles = [o_city_tile,
                      o_city_w,
                      o_city_ne,
                      o_city_e,
                      o_city_s,
                      o_city_n,
                      o_city_se,
                      o_city_nw,
                      o_city_sw]
        self.primary_tile = o_city_tile


o_city_cell = OvershireCityCell("Overshire City", (3, 6), 2, '../Music/Through the Forest.ogg',
                                [units.animal_group, units.monster_group], "o_city_cell")


# PRINCIPALIA
class PrincipaliaCell(Cell):
    def __init__(self, name, m_level, store_level, music, enemy_groups, cell_id):
        super().__init__(name, m_level, store_level, music, enemy_groups, cell_id)

        principalia_desc = """"""

        principalia_tile = Tile("City of Principalia", "principalia_tile", principalia_desc,
                                to_s="principalia_s",
                                to_w="principalia_w",
                                to_e="principalia_e",
                                to_n="principalia_n",
                                town_list=[towns.town_principalia])
        principalia_sw = Tile("Principalia Outskirts", "principalia_sw", principalia_desc,
                              to_e="principalia_s",
                              to_n="principalia_w")
        principalia_s = Tile("Principalia Outskirts", "principalia_s", principalia_desc,
                             to_w="principalia_sw",
                             to_e="principalia_se",
                             to_n="principalia_tile")
        principalia_se = Tile("Principalia Outskirts", "principalia_se", principalia_desc,
                              to_w="principalia_s",
                              to_n="principalia_e",
                              gem_list=[items.diamond_gem])
        principalia_w = Tile("Principalia Outskirts", "principalia_w", principalia_desc,
                             to_s="principalia_sw",
                             to_e="principalia_tile",
                             to_n="principalia_nw")
        principalia_e = Tile("Principalia Outskirts", "principalia_e", principalia_desc,
                             to_w="principalia_tile",
                             to_s="principalia_se",
                             to_n="principalia_ne")
        principalia_nw = Tile("Principalia Outskirts", "principalia_nw", principalia_desc,
                              to_s="principalia_w",
                              to_e="principalia_n")
        principalia_n = Tile("Principalia Outskirts", "principalia_n", principalia_desc,
                             to_s="principalia_tile",
                             to_w="principalia_nw",
                             to_e="principalia_ne")
        principalia_ne = Tile("Principalia Outskirts", "principalia_ne", principalia_desc,
                              to_s="principalia_e",
                              to_w="principalia_n")

        self.tiles = [principalia_tile,
                      principalia_w,
                      principalia_ne,
                      principalia_e,
                      principalia_s,
                      principalia_n,
                      principalia_se,
                      principalia_nw,
                      principalia_sw]
        self.primary_tile = principalia_tile


principalia_cell = PrincipaliaCell("Principalia", (4, 7), 2, '../Music/Through the Forest.ogg',
                                   [units.animal_group, units.monster_group], "principalia_cell")


# SARDOOTH
class SardoothCell(Cell):
    def __init__(self, name, m_level, store_level, music, enemy_groups, cell_id):
        super().__init__(name, m_level, store_level, music, enemy_groups, cell_id)

        sardooth_desc = """\
        Off in the distance you see Sardooth, a dark, dismal ghost town with nary a
        soul in sight. To the northeast lies the largest graveyard in the kingdom,
        the Overshire Graveyard."""

        sardooth_tile = Tile("Sardooth", "sardooth_tile", sardooth_desc,
                             to_s="sardooth_s",
                             to_w="sardooth_w",
                             to_e="sardooth_e",
                             to_n="sardooth_n",
                             town_list=[towns.town_sardooth])
        sardooth_sw = Tile("Sardooth Outskirts", "sardooth_sw", sardooth_desc,
                           to_e="sardooth_s",
                           to_n="sardooth_w")
        sardooth_s = Tile("Sardooth Outskirts", "sardooth_s", sardooth_desc,
                          to_w="sardooth_sw",
                          to_e="sardooth_se",
                          to_n="sardooth_tile")
        sardooth_se = Tile("Sardooth Outskirts", "sardooth_se", sardooth_desc,
                           to_w="sardooth_s",
                           to_n="sardooth_e",
                           gem_list=[items.diamond_gem])
        sardooth_w = Tile("Sardooth Outskirts", "sardooth_w", sardooth_desc,
                          to_s="sardooth_sw",
                          to_e="sardooth_tile",
                          to_n="sardooth_nw")
        sardooth_e = Tile("Sardooth Outskirts", "sardooth_e", sardooth_desc,
                          to_w="sardooth_tile",
                          to_s="sardooth_se",
                          to_n="sardooth_ne")
        sardooth_nw = Tile("Sardooth Outskirts", "sardooth_nw", sardooth_desc,
                           to_s="sardooth_w",
                           to_e="sardooth_n")
        sardooth_n = Tile("Sardooth Outskirts", "sardooth_n", sardooth_desc,
                          to_s="sardooth_tile",
                          to_w="sardooth_nw",
                          to_e="sardooth_ne")
        sardooth_ne = Tile("Sardooth Outskirts", "sardooth_ne", sardooth_desc,
                           to_s="sardooth_e",
                           to_w="sardooth_n")

        self.tiles = [sardooth_tile,
                      sardooth_w,
                      sardooth_ne,
                      sardooth_e,
                      sardooth_s,
                      sardooth_n,
                      sardooth_se,
                      sardooth_nw,
                      sardooth_sw]
        self.primary_tile = sardooth_tile


sardooth_cell = SardoothCell("Sardooth", (7, 10), 2, '../Music/song17_02.ogg',
                             [units.undead_group, units.monster_group], "sardooth_cell")

labyrinth_of_secrets = RandomizedDungeon("The Labyrinth of Unfathomable Secrets", "",
                                         (1, 3), 5, 5, 3, '../Music/Eight_Bit_Dungeon_Monster_Stomp.ogg',
                                         [units.dungeon_group, units.humanoid_group], "secret_labyrinth")

overshire_province = Province("Overshire", [nearton_cell,
                                            southford_cell,
                                            o_city_cell,
                                            principalia_cell,
                                            sardooth_cell,
                                            labyrinth_of_secrets],
                              "overshire_prov")


# =========================== #
#        DOWNPOUR CELLS       #
# =========================== #

downpour_province = Province("Downpour", [], "downpour_prov")


# =========================== #
#         FLUTE CELLS         #
# =========================== #
flute_province = Province("Flute", [], "flute_prov")


# =========================== #
#        DELTORA CELLS        #
# =========================== #
deltora_province = Province("Deltora", [], "deltora_prov")


# =========================== #
#        PARRIWAY CELLS       #
# =========================== #
parriway_province = Province("Parriway", [], "parriway_prov")


# =========================== #
#        CHIN'TOR CELLS       #
# =========================== #

# FORT SIGIL
class FortSigilCell(Cell):
    def __init__(self, name, m_level, store_level, music, enemy_groups, cell_id):
        super().__init__(name, m_level, store_level, music, enemy_groups, cell_id)

        fort_sigil_desc = """"""

        fort_sigil_tile = Tile("Town of Fort Sigil", "fort_sigil_tile", fort_sigil_desc,
                               to_s="fort_sigil_s",
                               to_w="fort_sigil_w",
                               to_e="fort_sigil_e",
                               to_n="fort_sigil_n",
                               town_list=[towns.town_fort_sigil])
        fort_sigil_sw = Tile("Fort Sigil Outskirts", "fort_sigil_sw", fort_sigil_desc,
                             to_e="fort_sigil_s",
                             to_n="fort_sigil_w")
        fort_sigil_s = Tile("Fort Sigil Outskirts", "fort_sigil_s", fort_sigil_desc,
                            to_w="fort_sigil_sw",
                            to_e="fort_sigil_se",
                            to_n="fort_sigil_tile")
        fort_sigil_se = Tile("Fort Sigil Outskirts", "fort_sigil_se", fort_sigil_desc,
                             to_w="fort_sigil_s",
                             to_n="fort_sigil_e")
        fort_sigil_w = Tile("Fort Sigil Outskirts", "fort_sigil_w", fort_sigil_desc,
                            to_s="fort_sigil_sw",
                            to_e="fort_sigil_tile",
                            to_n="fort_sigil_nw")
        fort_sigil_e = Tile("Fort Sigil Outskirts", "fort_sigil_e", fort_sigil_desc,
                            to_w="fort_sigil_tile",
                            to_s="fort_sigil_se",
                            to_n="fort_sigil_ne")
        fort_sigil_nw = Tile("Fort Sigil Outskirts", "fort_sigil_nw", fort_sigil_desc,
                             to_s="fort_sigil_w",
                             to_e="fort_sigil_n")
        fort_sigil_n = Tile("Fort Sigil Outskirts", "fort_sigil_n", fort_sigil_desc,
                            to_s="fort_sigil_tile",
                            to_w="fort_sigil_nw",
                            to_e="fort_sigil_ne")
        fort_sigil_ne = Tile("Fort Sigil Outskirts", "fort_sigil_ne", fort_sigil_desc,
                             to_s="fort_sigil_e",
                             to_w="fort_sigil_n")

        self.tiles = [fort_sigil_tile,
                      fort_sigil_w,
                      fort_sigil_ne,
                      fort_sigil_e,
                      fort_sigil_s,
                      fort_sigil_n,
                      fort_sigil_se,
                      fort_sigil_nw,
                      fort_sigil_sw]
        self.primary_tile = fort_sigil_tile


fort_sigil_cell = FortSigilCell("Fort Sigil", (5, 8), 2, '../Music/Through the Forest.ogg',
                                [units.animal_group, units.monster_group], "fort_sigil_cell")

chintor_province = Province("Chin'tor", [fort_sigil_cell], "chintor_prov")


# =========================== #
#      CAMBERLITE CELLS       #
# =========================== #

camberlite_province = Province("Camberlite", [], "camberlite_prov")


# =========================== #
#        WHITLOCK CELLS       #
# =========================== #

whitlock_province = Province("Whitlock", [], "whitlock_prov")


# =========================== #
#         KOHRIN CELLS        #
# =========================== #

kohrin_province = Province("Kohrin", [], "kohrin_prov")


# =========================== #
#        PELAMORA CELLS       #
# =========================== #

pelamora_province = Province("Pelamora", [], "pelamora_prov")


# =========================== #
#        CELEMIA CELLS        #
# =========================== #

celemia_province = Province("Celemia", [], "celemia_prov")


# =========================== #
#         THEX CELLS          #
# =========================== #

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

# valid_provinces is lists of strings that are allowed to be used as proivince names
# This is to prevent errors such as typos and whatnot, as there's no reason to use any other proivince names
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
    for check_direction in [item2.to_s, item2.to_n, item2.to_e, item2.to_w]:
        if check_direction and not find_tile_with_id(check_direction):
            print(f"{item2.tile_id} has an invalid direction ({check_direction})!")

# This loop checks to make sure all tile_id's are unique
for item3 in all_tiles:
    if item3 != find_tile_with_id(item3.tile_id):
        print(f"{item3.tile_id} is being used as a Tile ID for multiple tiles!")

# This optional loop checks to make sure no tiles are "adjacent to themselves"
# e.g. North on tile_a leads to tile_a
for item4 in all_tiles:
    for check_direction in [item4.to_s, item4.to_n, item4.to_e, item4.to_w]:
        if check_direction == item4.tile_id and not item4.allow_recursion:
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


for item7 in all_provinces:
    if item7.name not in valid_provinces:
        print(f"{item7} has an invalid province!")
