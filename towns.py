import sys
import time
import inv_system

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

class Town:
    def __init__(self, name, desc, x, y, inn=True, inn_cost=0, gen_store=True, gs_level=1):
        self.name = name
        self.desc = desc
        self.x = x
        self.y = y
        self.inn = inn
        self.inn_cost = inn_cost
        self.gen_store = gen_store
        self.gs_level = gs_level

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
            foo = '°N'
        else:
            foo = '°S'
        if self.x >= 0:
            bar = '°E'
        else:
            bar = '°W'
        spam = self.name + ': ' + str(self.y) + foo + ', ' + str(self.x) + bar
        if spam not in inv_system.inventory['coord']:
            inv_system.inventory['coord'].append(spam)

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
            if y_n in 'yes':
                print('-'*25)
                print('Inn Keeper: "Greetings, Traveler!"')
                print()
                while True:
                    if self.inn_cost == 0:
                        choice = input("\"Would you like to stay at our inn? It's free, y'know.\" | Yes or No: ")
                    else:
                        choice = input('"Would you like to stay at our inn? One night is %s GP." | Yes or No: ' % (self.inn_cost))
                    try:
                        choice = choice.lower()
                    except AttributeError:
                        continue
                    if choice in 'yes':
                        print()
                        if main.static['gp'] >= self.inn_cost:
                            print('"Good night, Traveler."')
                            print('Sleeping...')
                            time.sleep(2)
                            main.static['gp'] -= self.inn_cost
                            main.player.hp = main.static['hp_p']
                            main.player.mp = main.static['mp_p']
                            print('Your HP and MP have been fully restored. (-%s GP)' % (self.inn_cost))
                            print('-'*25)
                            main.save_game()
                        else:
                            print('"...You don\'t have enough GP. Sorry, Traveler, you can\'t stay here."')
                        return
                    elif choice in 'no':
                        return
            elif y_n in 'no':
                return

    def town_gen(self): # Let the player purchase items from the General Store
        stock = [] # A list containing actual instances of "Item"
        str_stock = [] # A readable yet non-functioning version of "stock"
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
            if y_n in 'yes':
                print('-'*25)
                print('Owner: "Welcome, Traveler!"')
                print()
                while True:
                    print('Stock: ' + str_stock)
                    print()
                    while True:
                        purchase = input('"What item would ya like to buy?" | %s GP | Input Item Name (or type "exit"): ' % (main.static['gp']))
                        try:
                            purchase = purchase.title()
                        except AttributeError:
                            continue
                        if purchase == 'Exit':
                            return
                        elif purchase in str_stock:
                            for i in stock:
                                if str(i) == purchase:
                                    break
                        else:
                            continue
                        print('-'*25)
                        print(i.desc)
                        print('-'*25)
                        if str(i).endswith('s'): # Make sure to use proper grammar!
                            spam = 'these'
                        else:
                            spam = 'this'
                        while True:
                            confirm = input("\"Ya want %s %s? It'll cost ya %s GP.\" | Yes or No: " % (spam, str(i), i.buy))
                            try:
                                confirm = confirm.lower()
                            except AttributeError:
                                continue
                            if confirm in 'yes':
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
                            elif confirm in 'no':
                                print()
                                break
                        break
            elif y_n in 'no':
                return

# List of Towns:
town1 = Town('Nearton', """Nearton: a small village in the central region of the Plains.
It is in this very town where numerous brave adventurers have begun
their journey. Nearton has a general store, an inn, and a few small houses.
An old man is standing near one of the houses, and appears to be talking
to a small group of strangers.""", 0, 0)

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
do as you wish in the lower.""", -11, 13, inn_cost=8, gs_level=2)

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
                if y_n in 'yes':
                    town.new_location()
                    town.town_choice()
                    return
                elif y_n in 'no':
                    print('-'*25)
                    return