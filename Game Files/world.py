import sys
import battle
import monsters
import towns
import bosses
import random
import winsound

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

position = ''

north = ['n', 'nor', 'north']
south = ['s', 'sou', 'south']
east = ['e', 'eas', 'east']
west = ['w', 'wes', 'west']


def setup_vars():
    global position
    position = main.position


def movement_system():
    """Adjust the player's x/y coordinates based on inputted direction."""
    global position

    setup_vars()
    winsound.PlaySound(None, winsound.SND_ASYNC)
    winsound.PlaySound(position['reg_music'],
                       winsound.SND_ASYNC |
                       winsound.SND_LOOP |
                       winsound.SND_NODEFAULT)
    while True:
        if check_region():
            winsound.PlaySound(None, winsound.SND_ASYNC)
            winsound.PlaySound(position['reg_music'],
                               winsound.SND_ASYNC |
                               winsound.SND_LOOP |
                               winsound.SND_NODEFAULT)
        towns.search_towns(position['x'], position['y'])
        if position['x'] >= 0:
            position['h'] = "'E"
        else:
            position['h'] = "'W"
        if position['y'] >= 0:
            position['v'] = "'N"
        else:
            position['v'] = "'S"
        while True:
            direction = input('Position: {0}{1}, {2}{3} | {4} | Which direction do you want to travel in? | N, S, E, \
W: '.format(position['y'], position['v'],
            position['x'], position['h'],
            position['reg']))
            try:
                direction = direction.lower()
            except AttributeError:
                continue
            if [x for x in [north, south, east, west] if direction in x]:
                if direction in north:
                    if position['y'] < 125:
                        position['y'] += 1
                    else:
                        out_of_bounds()
                        continue
                elif direction in south:
                    if position['y'] > -125:
                        position['y'] -= 1
                    else:
                        out_of_bounds()
                        continue
                elif direction in west:
                    if position['x'] > -125:
                        position['x'] -= 1
                    else:
                        out_of_bounds()
                        continue
                elif direction in east:
                    if position['x'] < 125:
                        position['x'] += 1
                    else:
                        out_of_bounds()
                        continue
                position['avg'] = int(((abs(position['x'])) +
                                       (abs(position['y'])))/2)
                if not bosses.check_bosses(position['x'], position['y']):
                    if not towns.search_towns(position['x'], position['y'], enter=False):
                        is_battle = not random.randint(0, 7)
                        if is_battle:
                            monsters.spawn_monster()
                            battle.setup_vars()
                            battle.battle_system()
                break


def out_of_bounds():
    print('-'*25)
    print('Ahead of you is a seemingly endless ocean. You cannot continue in this direction.')
    print('-'*25)


def check_region():
    global position
    x, y = position['x'], position['y']
    if x in range(-50, 51) and y in range(-50, 51):  # Center of World
        region = 'Forest'
        reg_music = 'Music\\Through the Forest.wav'
    elif x in range(-115, 1) and y in range(0, 116):  # Northwest of World
        region = 'Tundra'
        reg_music = 'Music\\Arpanauts.wav'
    elif x in range(-115, 0) and y in range(-115, 1):  # Southwest of World
        region = 'Mountain'
        reg_music = 'Music\\Mountain.wav'
    elif x in range(0, 116) and y in range(0, 116):  # Northeast of world
        region = 'Desert'
        reg_music = 'Music\\Come and Find Me.wav'
    elif x in range(0, 116) and y in range(-115, 1): # Southeast of World
        region = 'Swamp'
        reg_music = 'Music\\Digital Native.wav'
    elif abs(x) in range(116, 126) or abs(y) in range(116, 126): # Edges of World
        region = 'Beach'
        reg_music = "Music\\We're all under the stars.wav"
    if position['reg'] != region:
        print('-'*25)
        print('You have left the {0} region and are now entering the {1} region.'.format(position['reg'], region))
        print('-'*25)
        position['reg'] = region
        position['reg_music'] = reg_music
        return True
    else:
        return False


def save_coords(x, y):
    global position
    position['prev_town'][0], position['prev_town'][1] = x, y


def back_to_coords():
    global position
    position['x'] = position['prev_town'][0]
    position['y'] = position['prev_town'][1]
