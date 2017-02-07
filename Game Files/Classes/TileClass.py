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
# ------------------------------------------------------------------------ #


class Tile:
    def __init__(self, name, tile_id, region, desc, m_level, to_n=None, to_s=None, to_e=None, to_w=None, to_up=None,
                 to_dn=None, town_list=(), boss_list=(), gem_list=(), enterable=True, level_req=1):
        self.name = name
        self.tile_id = tile_id
        self.region = region
        self.desc = desc
        self.m_level = m_level
        self.to_n = to_n
        self.to_s = to_s
        self.to_e = to_e
        self.to_w = to_w
        self.to_up = to_up
        self.to_dn = to_dn
        self.enterable = enterable
        self.town_list = town_list
        self.boss_list = boss_list
        self.gem_list = gem_list
        self.level_req = level_req

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