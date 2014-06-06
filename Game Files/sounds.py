import sys

from pygame import mixer
from pygame.mixer import Sound


if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

mixer.pre_init(44100, -16, 2, 2048)
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


def change_volume():
    for x in ['sword_slash', 'magic_attack',
              'magic_healing', 'enemy_hit',
              'foot_steps', 'aim_weapon']:
        globals()[x].set_volume(main.sound_vol)