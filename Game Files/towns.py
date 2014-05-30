import sys
import time
import copy
import inv_system
import world
import npcs
import pygame

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()


class Town:
    def __init__(self, name, desc, people, x, y, inn=True, inn_cost=0, gen_store=True, gs_level=1):
        self.name = name  # The town's name (i.e. New York City)
        self.desc = desc  # A brief description of the town
        self.x = x  # X-coordinate on map
        self.y = y  # Y-coordinate on map
        self.people = people  # A list that contains the NPCs you can talk to
        self.inn = inn  # If true, the town contains an inn
        self.inn_cost = inn_cost  # How much money it costs to sleep at the inn
        self.gen_store = gen_store  # If true, the town contains a General Store
        self.gs_level = gs_level  # The higher this value is, the better the
                                  # items the store will sell.

    def town_choice(self):
        print('-'*25)
        print('Welcome to {0}!\n{1}'.format(self.name, '-'*25))
        while True:
            print("""What do you wish to do?
      [1] --> Town Desc
      [2] --> Buildings
      [3] --> People
      [4] --> Player Info
      [5] --> View Inventory
      [6] --> Exit""")
            while True:
                choice = input('Input [#]: ')
                if choice == '1':
                    print('-'*25)
                    input(''.join([self.desc, '\nPress Enter/Return ']))
                    print('-'*25)
                elif choice == '2':
                    print('-'*25)
                    self.inside_town()
                    print('-'*25)
                elif choice == '3':
                    print('-'*25)
                    self.speak_to_npcs()
                    print('-'*25)
                elif choice == '4':
                    print('-'*25)
                    main.player.player_info()
                    print('-'*25)
                elif choice == '5':
                    print('-'*25)
                    inv_system.pick_category()
                    print('-'*25)
                elif choice == '6':
                    pygame.mixer.music.load(world.position['reg_music'])
                    pygame.mixer.music.play(-1)
                    print('-'*25)
                    return
                else:
                    continue
                break

    def new_location(self):  # Translate the location of newly-found towns
        if self.y >= 0:      # into a string, then add to inventory.
            foo = "'N"
        else:
            foo = "'S"
        if self.x >= 0:
            bar = "'E"
        else:
            bar = "'W"
        spam = ''.join([str(x) for x in [self.name, ': ', str(self.y), foo, ', ', str(self.x), bar]])
        if spam not in inv_system.inventory['coord']:
            inv_system.inventory['coord'].append(spam)
            print('-'*25)
            print("{0}'s location has been added to the coordinates page of your inventory.".format(self.name))

    def inside_town(self):
        gen_words = ['general store', 'gen', 'gen store', 'shop', 'store', 's', 'g']
        inn_words = ['inn', 'hotel', 'motel', 'save', 'sleep', 'bed', 'i']
        buildings = []
        while True:
            spam = False
            if self.inn and not self.gen_store:
                print('There is an Inn in this town.')
                buildings = gen_words
            elif self.gen_store and not self.inn:
                print('There is a General Store in this town.')
                buildings = inn_words
            elif self.gen_store and self.inn:
                print('There is both an Inn and a General Store in this town.')
                buildings = inn_words[:]
                buildings.extend(gen_words)
            if buildings:
                while not spam:
                    selected = input('What building would you like to enter? | Input Building Name (or type "exit"): ')
                    try:
                        selected = selected.lower()
                    except AttributeError:
                        continue
                    if selected in buildings:
                        pygame.mixer.music.load('Music\\Mayhem in the Village.ogg')
                        pygame.mixer.music.play(-1)
                        if selected in gen_words:
                            self.town_gen()
                            spam = True
                        elif selected in inn_words:
                            if self.town_inn():
                                spam = True
                        print('-'*25)
                        pygame.mixer.music.load('Music\\Chickens (going peck peck peck).ogg')
                        pygame.mixer.music.play(-1)
                    elif selected in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        return

    def town_inn(self):
        print('-'*25)
        print('Inn Keeper: "Greetings, Traveler!"')
        while True:
            choice = input('"Would you like to stay at our inn? {0}" | Yes or No: '.format(
                "It's free, y'know." if not self.inn_cost else ' '.join(
                ["One Night is", str(self.inn_cost), "GP."])))
            try:
                choice = choice.lower()
            except AttributeError:
                continue
            if choice in ['yes', 'y', 'yeah']:
                print()
                if main.static['gp'] >= self.inn_cost:
                    print('"Good night, Traveler."')
                    print('Sleeping...')
                    time.sleep(1.5)
                    main.static['gp'] -= self.inn_cost
                    main.player.hp = copy.copy(main.static['hp_p'])
                    main.player.mp = copy.copy(main.static['mp_p'])
                    print('Your HP and MP have been fully restored. ')
                    print('-'*25)
                    main.save_game()
                    return True
                else:
                    print('"...You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')
                return True
            elif choice in ['no', 'n', 'nope']:
                return False

    def town_gen(self):  # Let the player purchase items from the General Store
        stock = []       # A list containing objects the player can purchase
        for item in inv_system.gs_stock:
            stock.append(item[self.gs_level - 1])
        print('-'*25)
        print('Owner: "Welcome, Traveler!"')
        while True:
            b_s = input('Do you want to [b]uy or [s]ell items? | Input letter (or type "exit"): ')
            try:
                b_s = b_s.lower()
            except AttributeError:
                continue
            if b_s.startswith('b'):
                while True:
                    print('"Well, here\'s what I have in my stock: "')
                    for num, item in enumerate(stock):
                        print(''.join(['[', str(num + 1), '] ', str(item), ' --> ', str(item.buy), ' GP']))
                    print('You have {0} GP'.format(main.static['gp']))
                    while True:
                        purchase = input('Input [#] (or type "back"): ')
                        try:
                            purchase = int(purchase) - 1
                            if purchase < 0:
                                continue
                        except ValueError:
                            try:
                                purchase = purchase.lower()
                            except AttributeError:
                                continue
                            if purchase in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                return
                            else:
                                continue
                        try:
                            i = stock[purchase]
                        except IndexError:
                            continue
                        print('-'*25)
                        print(i.desc)
                        print('-'*25)
                        while True:
                            confirm = input("\"Ya want {0} {1}? It'll cost ya {2} GP.\" | Yes or No: ".format(
                                'these' if str(i).endswith('s') else 'this', str(i), i.buy))
                            try:
                                confirm = confirm.lower()
                            except AttributeError:
                                continue
                            if confirm in ['yes', 'y']:
                                if main.static['gp'] >= i.buy:
                                    inv_system.inventory[i.cat].append(i)
                                    main.static['gp'] -= i.buy
                                    print('-'*25)
                                    input('You purchase the {0} (-{1} GP). (Press enter/return).'.format(str(i), i.buy))
                                    print('-'*25)
                                else:
                                    input('"Hey, you don\'t even have enough GP for this {0}!" (Press enter/return)'.format(
                                        str(i)))
                                    print()
                                break
                            elif confirm in ['no', 'n']:
                                print()
                                break
                        break
            elif b_s.startswith('s'):
                spam = True
                while spam:
                    print("""Categories:
      [1] Armor
      [2] Consumables
      [3] Weapons
      [4] Miscellaneous""")
                    while True:
                        cat = input('Input [#] (or type "back"): ')
                        try:
                            cat = cat.lower()
                        except AttributeError:
                            pass
                        if cat in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                            break
                        elif cat == '1':
                            cat = 'armor'
                            vis_cat = 'Armor'
                        elif cat == '2':
                            cat = 'consum'
                            vis_cat = 'Consumables'
                        elif cat == '3':
                            cat = 'weapons'
                            vis_cat = 'Weapons'
                        elif cat == '4':
                            cat = 'misc'
                            vis_cat = 'Miscellaneous'
                        else:
                            continue
                        if cat in inv_system.inventory:
                            if inv_system.inventory[cat]:
                                if cat not in ['weapons', 'armor']:
                                    inv_system.pick_item(cat, vis_cat, gs=True)
                                    print('-'*25)
                                else:
                                    if [x for x in inv_system.inventory[cat] if not x.equip]:
                                        inv_system.pick_item(cat, vis_cat, gs=True)
                                        print('-'*25)
                                    else:
                                        print('-'*25)
                                        print('The "{0}" category is empty...'.format(vis_cat))
                                        print('-'*25)
                                break
                            else:
                                print('-'*25)
                                print('The "{0}" category is empty...'.format(vis_cat))
                                print('-'*25)
                                break
            elif b_s in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                return

    def speak_to_npcs(self):
        while True:
            print('NPCs:\n      ' + '\n      '.join(["[" + str(x + 1) + "] " + npc.name for x, npc in enumerate(
                self.people)]))
            while True:
                npc = input('Input [#] (or type "exit"): ')
                try:
                    npc = int(npc) - 1
                    if npc < 0:
                        continue
                except (ValueError, TypeError):
                    try:
                        npc = npc.lower()
                    except AttributeError:
                        continue
                    if npc in ['e', 'x', 'exit', 'b', 'back', 'c', 'cancel']:
                        return
                    else:
                        continue
                try:
                    npc = self.people[npc]
                except IndexError:
                    continue
                pygame.mixer.music.load('Music\\Mayhem in the Village.ogg')
                pygame.mixer.music.play(-1)
                print('-'*25)
                npc.speak()
                print('-'*25)
                pygame.mixer.music.load('Music\\Chickens (going peck peck peck).ogg')
                pygame.mixer.music.play(-1)
                break

# List of Towns:
town1 = Town('Nearton', """Nearton: a small village in the central region of t\
he Forest.
It is in this very town where numerous brave adventurers have begun
their journey. Nearton has a general store, an inn, and a few small houses.
An old man is standing near one of the houses, and appears to be talking
to a small group of strangers.""", [npcs.philliard, npcs.alfred], 0, 1)

town2 = Town('Southford', """Southford: A fair-size town in the central-southe\
rn region of the Forest.
This town is well-known for its wise inhabitants. Some of the elders here
are rumored to be masters of the arcane arts, and may be willing to train
your magical abilities for a reasonable price. There is a general store, an
inn, and several houses in this town.""", [npcs.wesley], -2, -6, inn_cost=2)

town3 = Town('Overshire', """Overshire: A city in the northwestern region of th\
e Forest.
Overshire is the capitol of the Forest, and as such is very densely populated.
The city is separated into three sectors: the upper-class inner portion, the
lower-class outer portion, with the middle-class section situated in between.
As an outsider, you are forbidden to enter the upper two, but are welcome to
do as you wish in the lower.""", [npcs.stewson], -11, 13, inn_cost=5, gs_level=2)

town_list = [town1, town2, town3]


def search_towns(pos_x, pos_y, enter=True):
        # Check to see if there is a
    # town where the player is located
    for town in town_list:
        if town.x == pos_x and town.y == pos_y:
            if enter:
                print('-'*25)
                while True:
                    y_n = input('There is a town nearby. Do you wish to investigate? | Yes or No: ')
                    try:
                        y_n = y_n.lower()
                    except AttributeError:
                        continue
                    if y_n in ['yes', 'y']:
                        pygame.mixer.music.load('Music\\Chickens (going peck peck peck).ogg')
                        pygame.mixer.music.play(-1)
                        world.save_coords(town.x, town.y)
                        town.new_location()
                        town.town_choice()
                        return
                    elif y_n in ['no', 'n']:
                        print('-'*25)
                        return
            else:
                return True
    else:
        return False
