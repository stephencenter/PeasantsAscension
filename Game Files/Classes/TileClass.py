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
# ------------------------------------------------------------------------ #
# Map of the Arcadian Continent: http://tinyurl.com/arcadia-map-v5

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input


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
