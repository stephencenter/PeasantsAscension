import sys
import time
import copy
import inv_system
import world
import items

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

class Town:
    def __init__(self, name, desc, x, y, inn=True, inn_cost=0, gen_store=True, gs_level=1):
        self.name = name
        self.desc = desc
        self.x = x # X-coordinate on map
        self.y = y # Y-coordinate on map
        self.inn = inn # If true, the town contains an inn
        self.inn_cost = inn_cost
        self.gen_store = gen_store # If true, the town contains a General Store
        self.gs_level = gs_level # The higher this value is, the better the
                                 # items the store will sell.

    def town_choice(self):
        print('-'*25)
        print('Welcome to %s!' % (self.name))
        while True:
            choice = input('1. Town Desc; 2. Enter Town; 3. Player Info; 4. View Inv; 5. Exit | Input #(1-5): ')
            if choice == '1':
                print('-'*25)
                print(self.desc)
                print('-'*25)
            elif choice == '2':
                print('-'*25)
                self.inside_town()
                print('-'*25)
            elif choice == '3':
                print('-'*25)
                main.player.player_info()
                print('-'*25)
            elif choice == '4':
                print('-'*25)
                inv_system.pick_catagory()
                print('-'*25)
            elif choice == '5':
                print('-'*25)
                return

    def new_location(self): # Tranlate the location of newly-found towns
        if self.y >= 0:     # into a string, then add to inventory.
            foo = "'N"
        else:
            foo = "'S"
        if self.x >= 0:
            bar = "'E"
        else:
            bar = "'W"
        spam = self.name + ': ' + str(self.y) + foo + ', ' + str(self.x) + bar
        if spam not in inv_system.inventory['coord']:
            inv_system.inventory['coord'].append(spam)
            print('-'*25)
            print('%s\'s location has been added to the coordinates page of your inventory.' % (self.name))

    def inside_town(self):
        if self.inn:
            self.town_inn()
            if self.gen_store:
                print('-'*25)
        if self.gen_store:
            self.town_gen()

    def town_inn(self):
        print('There is an Inn in this town.')
        while True:
            y_n = input('Do you want to visit the inn? | Yes or No: ')
            try:
                y_n = y_n.lower()
            except AttributeError:
                continue
            if y_n in ['yes', 'y']:
                print('-'*25)
                print('Inn Keeper: "Greetings, Traveler!"')
                print()
                while True:
                    choice = input('"Would you like to stay at our inn? %s" | Yes or No: ' % (
                    "It's free, y'know." if not self.inn_cost else ' '.join(["One Night is", str(self.inn_cost), "GP."])))
                    try:
                        choice = choice.lower()
                    except AttributeError:
                        continue
                    if choice in ['yes', 'y']:
                        print()
                        if main.static['gp'] >= self.inn_cost:
                            print('"Good night, Traveler."')
                            print('Sleeping...')
                            time.sleep(2)
                            main.static['gp'] -= self.inn_cost
                            main.player.hp = copy.copy(main.static['hp_p'])
                            main.player.mp = copy.copy(main.static['mp_p'])
                            print('Your HP and MP have been fully restored. ')
                            print('-'*25)
                            main.save_game()
                        else:
                            print('"...You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')
                        return
                    elif choice in ['no', 'n']:
                        return
            elif y_n in ['no', 'n']:
                return

    def town_gen(self): # Let the player purchase items from the General Store
        stock = []      # A list containing actual instances of "Item"
        str_stock = []  # A readable, non-functioning version of "stock"
        for type in inv_system.gs_stock:
            item = type[self.gs_level - 1]
            if isinstance(item, inv_system.Item):
                stock.append(item)
                str_stock.append(str(item) + ', ')
            else:
                str_stock.append(item)
        str_stock = ''.join(str_stock)
        print('There is a General Store in this town.')
        while True:
            y_n = input('Do you want to shop at the General Store? | Yes or No: ')
            try:
                y_n = y_n.lower()
            except AttributeError:
                continue
            if y_n in ['yes', 'y']:
                print('-'*25)
                print('Owner: "Welcome, Traveler!"')
                print()
                while True:
                    b_s = input('"Are ya buying, or are ya selling?" | Input "Buy" or "Sell" (or type "exit"): ')
                    try:
                        b_s = b_s.lower()
                    except AttributeError:
                        continue
                    if b_s in ['sell', 's']:
                        items.sell_item()
                        print('-'*25)
                        continue
                    elif b_s in ['buy', 'b']:
                        pass
                    elif b_s == 'exit':
                        return
                    else:
                        continue
                    print('-'*25)
                    spam = True
                    while True:
                        if spam:
                            print('Stock: ' + str_stock)
                            print()
                        else:
                            print('-'*25)
                            break
                        while True:
                            purchase = input('"What item would ya like to buy?" | %s GP | Input Item Name (or type "back"): ' % (main.static['gp']))
                            if purchase == '':
                                continue
                            try:
                                purchase = purchase.title()
                            except AttributeError:
                                continue
                            if purchase == 'Back':
                                spam = False
                                break
                            elif purchase in str_stock:
                                for i in stock:
                                    if str(i) == purchase:
                                        break
                            else:
                                continue
                            print('-'*25)
                            print(i.desc)
                            print('-'*25)
                            while True:
                                confirm = input("\"Ya want %s %s? It'll cost ya %s GP.\" | Yes or No: " % (
                                'these' if str(i).endswith('s') else 'this', str(i), i.buy))
                                try:
                                    confirm = confirm.lower()
                                except AttributeError:
                                    continue
                                if confirm in ['yes', 'y']:
                                    if main.static['gp'] >= i.buy:
                                        inv_system.add_item(i)
                                        main.static['gp'] -= i.buy
                                        print('-'*25)
                                        input('You purchase the %s (-%s GP). (Press enter/return to continue).' % (str(i), i.buy))
                                        print('-'*25)
                                    else:
                                        input('"Hey, you don\'t even have enough GP for this %s! (Press enter/return)"' % (str(i)))
                                        print()
                                    break
                                elif confirm in ['no', 'n']:
                                    print()
                                    break
                            break
            elif y_n in ['no', 'n']:
                return

# List of Towns:
town1 = Town('Nearton', """Nearton: a small village in the central region of the Plains.
It is in this very town where numerous brave adventurers have begun
their journey. Nearton has a general store, an inn, and a few small houses.
An old man is standing near one of the houses, and appears to be talking
to a small group of strangers.""", 0, 1)

town2 = Town('Southford', """Southford: A fair-size town in the central-southern region of the Plains.
This town is well-known for its wise inhabitants. Some of the elders here
are rumored to be masters of the arcane arts, and may be willing to train
your magical abilities for a reasonable price. There is a general store and
several houses in this town.""", -2, -6, inn=False)

town3 = Town('Overshire', """Overshire: A city in the nortwestern region of the Plains.
Overshire is the capitol of the Plains, and as such is very densely populated.
The city is separated into three sectors: the upper-class inner portion, the
lower-class outer portion, with the middle-class section situated in between.
As an outsider, you are forbidden to enter the upper two, but are welcome to
do as you wish in the lower.""", -11, 13, inn_cost=6, gs_level=2)

town_list = [town1, town2, town3]

def search_towns(pos_x, pos_y): # Check to see if there is a town where the player is located
    for town in town_list:
        if town.x == pos_x and town.y == pos_y:
            while True:
                y_n = input('There is a town nearby. Do you wish to investigate? | Yes or No: ')
                try:
                    y_n = y_n.lower()
                except AttributeError:
                    continue
                if y_n in ['yes', 'y']:
                    world.save_coords(town.x, town.y)
                    town.new_location()
                    town.town_choice()
                    return
                elif y_n in ['no', 'n']:
                    print('-'*25)
                    return