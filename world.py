import sys
import battle
import monsters
import towns
import random

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
    """Adjust the player's x/y coordinates based on inputed direction."""
    setup_vars()
    while True:
        global position
        check_region()
        towns.search_towns(position['x'], position['y'])
        if position['x'] >= 0:
            position['h'] = '°E'
        else:
            position['h'] = '°W'
        if position['y'] >= 0:
            position['v'] = '°N'
        else:
            position['v'] = '°S'
        while True:
            direction = input('Position: %s%s, %s%s | %s | Which direction do you want to travel in? | N, S, E, W: ' % (position['y'], position['v'], position['x'], position['h'], position['reg']))
            try:
                direction = direction.lower()
            except AttributeError:
                continue
            if direction in north or direction in south or direction in east or direction in west:
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
                position['avg'] = int((abs(position['x']) + abs(position['y']))/2)        
                spam = random.randint(0, 3)
                eggs = random.randint(0, 3)
                if spam == eggs:
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
    if x in range(-50, 51) and y in range(-50, 51):
        region = 'Plains'
    elif x in range(-115, 0) and y in range(1, 116):
        region = 'Tundra'
    elif x in range(-115, 1) and y in range(-115, 0):
        region = 'Forest'
    elif x in range(1, 116) and y in range(0, 116):
        region = 'Desert'
    elif x in range(0, 116) and y in range(-115, 1):
        region = 'Swamp'
    elif abs(x) in range(116, 126) or abs(y) in range(116, 126):
        region = 'Beach'
    if position['reg'] != region:
        print('-'*25)
        print('You have left the %s region and are now entering the %s region.' % (position['reg'], region))
        print('-'*25)
        position['reg'] = region