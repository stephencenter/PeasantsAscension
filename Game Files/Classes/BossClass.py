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

import sys
import copy
import json
import random

import npcs
import units
import battle
import items as i_items
import inv_system
import sounds

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Boss(units.Monster):
    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad, lvl, items, gold,
                 experience, attk_msg, active=True, element='none'):

        units.Monster.__init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)
        self.items = items
        self.active = active
        self.lvl = lvl
        self.element = element
        self.experience = experience
        self.gold = gold
        self.attk_msg = attk_msg
        self.monster_name = copy.copy(self.name)

    def max_stats(self):
        self.hp = copy.copy(self.max_hp)
        self.mp = copy.copy(self.max_mp)

    # noinspection PyMethodMayBeStatic
    def new_location(self, add=True):
        # Translate the location of the boss into a string, and then store it in the player's inventory
        mpi = main.party_info

        coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
        coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
        coord_z = f"""{mpi["z"] if mpi["z"] != 0 else ""}{"'UP" if mpi["z"] > 0 else "'DOWN" if mpi['z'] < 0 else ""}"""

        new_coords = f"{self.name}: {coord_y}, {coord_x}, {coord_z}"

        if add and new_coords not in inv_system.inventory['coord']:
            inv_system.inventory['coord'].append(new_coords)
            print('-'*25)
            print(f"You quickly mark down the location of {self.name}'s lair.")
            input("\nPress enter/return ")

        else:

            return new_coords

    def upon_defeating(self):
        pass
