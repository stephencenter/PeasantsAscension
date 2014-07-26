#   This file is part of PythoniusRPG.
#
#	 PythoniusRPG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PythoniusRPG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PythoniusRPG.  If not, see <http://www.gnu.org/licenses/>.

import sys

from pygame import mixer
from pygame.mixer import Sound


if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

mixer.pre_init(frequency=44100, buffer=1024)
mixer.init()

# Sword Slash -- Played when you attempt to physically attack an enemy
sword_slash = Sound('Sound FX/sword_slash.wav')

# Magic Attack -- Played when you attempt to use a magical attack
magic_attack = Sound('Sound FX/magic_attack.wav')

# Magic Healing -- Played when you attempt to use a magical healing spell
magic_healing = Sound('Sound FX/magic_healing.wav')

# Enemy-hit -- Played when the enemy is hit by a player attack
enemy_hit = Sound('Sound FX/enemy_hit.wav')

# Foot-steps -- Played when you move on the overworld
foot_steps = Sound('Sound FX/foot_steps.wav')

# Aim Weapon -- Played when attempting to attack with a ranged weapon
aim_weapon = Sound('Sound FX/aim_weapon.wav')

# Attack Miss -- Played when attempting to attack and then failing
attack_miss = Sound('Sound FX/attack_miss.wav')

# Got Item -- Played when you receive an item, GP, or XP.
item_pickup = Sound('Sound FX/item_pickup.wav')


def change_volume():
    for x in ['sword_slash', 'magic_attack',
              'magic_healing', 'enemy_hit',
              'foot_steps', 'aim_weapon',
              'attack_miss', 'item_pickup']:
        globals()[x].set_volume(main.sound_vol)