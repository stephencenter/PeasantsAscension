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

import json
import logging
import sys
import time

import pygame

import inv_system
import items
import npcs
import save_load
import sounds
import tiles
from TownClass import Town, Tavern, Chest, House

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

# OVERWORLD TOWNS
nearton_h1_c1 = Chest([20], 1, "N-H1-C1")
nearton_h1_c2 = Chest([10, items.s_rejuv], 1, "N-H1-C2")
nearton_h1 = House("Philliard", [nearton_h1_c1, nearton_h1_c2])

nearton_h2_c1 = Chest([5, items.bone_bag, items.fairy_dust, items.feathers], 1, "N-H2-C1")
nearton_h2 = House("Alfred", [nearton_h2_c1])

town_nearton = Town('Nearton', """\
Nearton: A small village in the central region of the Forest. It is in this
very town where numerous brave adventurers have begun their journey. Nearton
is just your standard run-of-the-mill village: it has a general store, an inn,
and a few small houses. An old man  is standing near one of the houses, and
appears to be very troubled about something.""",
                    [npcs.philliard, npcs.alfred, npcs.saar, npcs.npc_solou], [nearton_h1, nearton_h2], 0, 1, "nearton")

southford_h1_c1 = Chest([35], 2, "S-H1-C1")
southford_h1 = House("Lazaro", [southford_h1_c1])

town_southford = Town('Southford', """\
Southford: A fair-size town in the South-East of the Inner Central Forest.
The inhabitants of this town are known for being quite wise, and may
provide you with helpful advice.""", [npcs.wesley, npcs.sondalar, npcs.lazaro], [southford_h1], 2, 1, "southford")

town_overshire = Town('Overshire', """\
Overshire: A city in the northwestern region of the Forest. Overshire is the
capital of Harconia, and as such is very densely populated. The city is
separated into three sectors: the upper-class inner portion consisting of
a castle surrounded by reinforced stone walls, a lower-class outer portion
comprised of smalls buildings and huts, and a middle-class section situated in
between. As an outsider, you are forbidden to enter the upper two, but are
welcome to do as you wish in the lower.""",
                      [npcs.joseph, npcs.stewson, npcs.jeffery, npcs.harthos], [],
                      5, 2, "overshire")

town_charsulville = Town('Charsulville', """\
Charsulville: A plain village in the south east
region of the Forest. It is home to nothing special, although it's cheap
inn service and higher-quality products it sells more than makes up for this.
There is a ragged beggar standing in the middle of the road.""", [npcs.ethos, npcs.typhen], [], 2, 2, "charsulville")

town_fort_sigil = Town('Fort Sigil', """\
Fort Sigil: A small village in the northern region
of the Forest. The citizens of this town have worked tremendously hard to
convert the rarely-used fort into a hospitable village, and have done
fairly well. Despite it's rich backstory, Fort Sigil doesn't get many
visitors. Perhaps there's a reason...""",[npcs.seriph, npcs.rivesh], [], 1, 3, "fort_sigil")

town_tripton = Town('Tripton', """\
Tripton: When the town of Tripton was being built, the people working on the
project failed to notice that another town, Fallville, just so happened to be
located mere meters away from the new town's borders. Merchants in Tripton
became very successful, as their superior bartering tactics allowed them to
easily steal business from Fallvillian merchants. This has led to a bitter,
and sometimes violent, rivalry between the two towns, particularly between the
village leaders.""", [npcs.kyle], [], 3, 3, "tripton")

town_fallville = Town('Fallville', """\
Fallville: When the town of Tripton was being built, the people working on the
project failed to notice that another town, Fallville, just so happened to be
located mere meters away from the new town's borders. Merchants in Tripton
became very successful, as their superior bartering tactics allowed them to
easily steal business from Fallvillian merchants. This has led to a bitter,
and sometimes violent, rivalry between the two towns, particularly between the
village leaders.""", [npcs.krystin, npcs.frederick], [], 1, 2, "fallville")

town_parceon = Town('Parceon', """\
Parceon: A highly populated town renown for it's rich magical background.
Parceon is home to the famous Sorcerers' Guild, a group of unbelievably
skilled and wise mages who work together to establish and enforce magical law.
The head of the guild, Azura, lives in a large tower in the southwest side of
the town.""", [npcs.azura], [], 4, 3, "parceon")

town_sardooth = Town('Sardooth', """\
Sardooth: A ghost town. There has not been a single
permanent inhabitant of this town for more than 75 years. It is completely
run down, with most of the buildings having been destroyed in the Harconian
Revolution. While this town may seem interesting and historic, there is nothing
of value here.""", [], [], -1, -1, "sardooth")

town_principalia = Town('Principalia', """\
Principalia: Principalia is an unbelievably large town, rivaling the likes of
Overshire and Valice. More interestingly, this is also the current home of
King Harconius II. The main attraction here is the Pytheror Building, a
medium-large cottage that the original King Harconius I had lived in
centuries ago. Every Monarch to date has decided to instead live in
the Overshire Castle, with the exception of the current monarch,
Harconius. Harconius II has changed several things since his ancestor
lived here, however. The cottage now has access to running water,
and the cottage is surrounded by a ring of 12 archer towers, each with
2 crossbowmen and one archer at the top. Each tower is about
100 yards from the cottage. In addition, there are numerous guards
standing watch all around the building. One guard happens to catch
your attention - probably because she just screamed "HALT!" at you.""", [npcs.sakura], [], 6, 3, "principalia")

town_new_ekanmar = Town('New Ekanmar', """\
New Ekanmar: The home of the Flyscorian Embassy in
Harconia. Prior to the Harconian Revolution, this town was the location of
a large portion of Flyscoria's troops in Harconia. The Harconians drove much of
them out, but a large number of them defected to the Harconian side and stayed.
After the war, the citizens gave up their weapons and became a peaceful town.
The vast majority of the inhabitants of this town are, naturally, Flyscors.
It seems that the Flyscorian Royal Family is visiting here - perhaps you can
talk with them for a bit.""", [npcs.f_jones, npcs.stravi, npcs.caesar], [], 2, 3, "new_ekanmar")

town_ravenstone = Town('Ravenstone', """\
Ravenstone: Ravenstone is a natural sanctuary,
home to dozens upon dozens of different flora and fauna. Naturally,
the majority population of Ravenstone consists of Druids and
other nature-magicians. Ravenstone is also the home of the Druids'
section of the Sorcerers' Guild. Vegetation grows on almost
every building and statue in the town. When the population of
the town is calculated, animals are counted as people. More than
35% of the population are various species of animals.""", [npcs.strathius], [], 1, 3, "ravenstone")

town_ambercreek = Town('Ambercreek', """\
Ambercreek: Ambercreek is a large mining town
located in the Terrius Mt. Range. The Chin'toric embassy can be found
in the middle of this town surrounded by large stone walls and a few
guard-towers. Sugulat, the King of Chin'tor, can often be found mining
on the outskirts of town. A very troubled-looking old man is in
the southwest portion of the town near a few smaller houses.""",
                       [npcs.raidon, npcs.sugulat], [], 8, 4, "ambercreek")

town_whistumn = Town('Whistumn', """\
Whistumn: An ancient city situated on the border
between the Arcadian Desert and the Central Forest. The inhabitants of this town
are known for their skepticism and reasoning. Many of them are scientists and are
skilled mathematicians and engineers. This town has an ongoing rivalry with
the town of Parceon because of their magical background, but this appears
to be mostly one-sided. A saddened-looking woman and her husband are sitting
on the steps of the general store.""", [npcs.polmor, npcs.serena], [], 9, 4, "whistumn")

town_hatchnuk = Town("Hatchnuk", """\
Hatchnuk: Hatchnuk is the only remaining town in Harconia
that still has cases of "Hatchnuk's Blight", a plague-like disease that
killed hundreds of thousands of people during the 10th and 11th centuries.
Something about the strand that infects Hatchnuk seems to make it completely
incurable, as the disease has been running rampant for the past four centuries.
The economy of Hatchnuk has entirely collapsed, as the risk of spreading disease
is far too great for people to be walking out in the open doing business together.
As a result, there are no buildings that you are able to enter, and no people to talk
to. The only people who are around to speak to are the guards, but their plague-doctor-esque
apparel and stern looks make it clear that they are not in the mood for chit-chat.""", [], [], -1, -1, "hatchnuk")

town_cesura = Town("Cesura", """\
Cesura: A town of great historical significance.
This town was named after King Cesura I, the war general during the Harconian Civil War
who helped to reunite the nation's six regions. Cesura was built on top of the site
of the Battle of Parchak, the definitive battle in the Civil War that Cesura used
to help the Central Forest win. There is a large monument to the King in the middle of
town, with the words "Here's to prosperity" written on a plaque at its feet.
An interesting thing to note is that Cesura is the only town that has a train
station. Construction of the town of Cesura was outsourced to Elysium, who is
the most technologically advanced civilization on the planet by far, having
developed and perfected the Steam Engine and later the Train before the year
1300 A.D.""", [npcs.morrison], [], 10, 4, "cesura")

town_sanguion = Town("Sanguion", """\
Sanguion: Sanguion is a safe-haven for vampires. Vampires are feared throughout
Harconia, so this fairly unknown town is the only place they can go without
being persecuted. The vampires in this town are peaceful, and actually refuse
to drink the blood of intelligent lifeforms. Beware, though, as not all
vampires are as friendly as the ones who inhabit Sanguion.""", [npcs.pime, npcs.ariver], [], 15, 4, "sanguion")

town_lantonum = Town("Lamtonum", """\
Lantonum: Lantonum is a small town that has the best forge in all of Arcadia.
Nearly 2/3s of all citizens of this town are experienced blacksmiths, and 90%
of all ores and minerals mined in Chin'tor or Ambercreek are brought here. It
is one of the wealthiest cities in all of the desert region due to its Mythril,
Magestite, and Necrite bar exports.""", [npcs.matthew], [], 13, 4, "lantonum")

town_capwild = Town("Capwild", """\
Capwild: Capwild is a medium sized town situated in the Terrius Mt. Range.
Capwild is a supplier of grains and herbs for the entire region, and makes
extensive use of terrace farming to make up for the lack of arable land.
Further investigation reveals that water mages have created self-sustaining
irrigation systems as well, further enhancing Capwild's farming capabilities.""", [], [], 12, 4, "capwild")

town_rymn_outpost = Town("Rymn Outpost", """\
Rymn Outpost: Rymn Outpost is one of the several small villages established
after the Thexian Incursion. All of the residents of this town are soldiers or
family members of soldiers, with the exception a few merchants. Rymn Outpost
is named after Rymnes, the Divinic gods of defense.""", [], [], 16, 4, "rymn_outposts")

cottage1 = Town('Small Cottage', """\
Small Cottage: As the name would suggest, his area only has a small cottage.
An old man is tending to his flock in a small pasture behind the building.
There doesn't appear be any other people near here.""", [npcs.alden], [], -1, -1, "cottage1")

a_town_valenfall = Town("Valenfall", """\
Valenfall: Not much is known about the ancient city of Valenfall. It's
inhabitants claim that it was lifted up from the mainland several millenia ago
by his Divinity. The gods supposedly used Valenfall as the cornerstone,
constructing all of the surrounding land of Aethus around it. Valenfall is
deeply intertwined with nature, and monuments depicting the nature deities can
be seen on every corner.
""", [npcs.fitzgerald], [], 2, 4, "a_valenfall")

# These three lists are used to serialize chest data. It's easier than having to constantly add chests to lists
all_towns = [town_nearton, town_southford, town_ambercreek, town_capwild, town_cesura, town_charsulville,
             town_fallville, town_hatchnuk, town_rymn_outpost, town_lantonum, town_fort_sigil, town_sanguion,
             town_ravenstone, town_principalia, town_whistumn, town_new_ekanmar, town_overshire, town_sardooth]
all_houses = [house for sublist in [town.houses for town in all_towns] for house in sublist]
all_chests = [chest for sublist in [house.chests for house in all_houses] for chest in sublist]

# TAVERNS
tavern1 = Tavern("The Traveling Merchant Inn", 0)
tavern2 = Tavern("The Drunken Moon Tavern ", 5)
tavern3 = Tavern("The Wandering Falcon Inn", 5)
tavern4 = Tavern("The Dancing Knight Tavern", 5)
tavern5 = Tavern("The Golden Watchman Tavern", 5)
tavern6 = Tavern("The Smiling Rapier Inn", 5)
tavern7 = Tavern("The Howling Warrior Inn", 10)
tavern8 = Tavern("The Vanishing Skull Inn", 10)
tavern9 = Tavern("The Brave Foal Tavern", 10)
tavern10 = Tavern("The Cowardly Dagger Inn", 10)
tavern11 = Tavern("The Thirsty Wizard Tavern", 15)
tavern12 = Tavern("The Painted Bard Inn", 15)


def search_towns(enter=True):
    # Check to see if there is a
    # town where the player is located

    if not isinstance(main.party_info['current_tile'], tiles.Tile):
        logging.exception(f"""Error gathering tile data on {time.strftime('%m/%d/%Y at %H:%M:%S')}: """)

        main.party_info['current_tile'] = tiles.in_for_c
        main.party_info['x'], main.party_info['y'], main.party_info['z'] = 0, 0, 0
        print("There was an error gathering tile data - your party has been relocated to 0'N, 0'E.")
        input("\nPress enter/return ")

    for town in main.party_info['current_tile'].town_list:
        if enter:
            print('-'*save_load.divider_size)

            sounds.item_pickup.play()

            while True:
                if isinstance(town, Tavern):
                    y_n = input("How convenient, a tavern is nearby! Should your party investigate? | Yes or No: ")

                else:
                    if town.new_location(add=False) not in inv_system.inventory['coord']:
                        y_n = input('There is a town nearby. Should your party investigate? | Yes or No: ')

                    else:
                        y_n = input(f'{town.name} is nearby. Should your party give it a visit? | Yes or No: ')

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    pygame.mixer.music.load('Content/Music/Chickens (going peck peck peck).ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(save_load.music_vol)

                    main.party_info['prev_town'] = main.party_info['current_tile']
                    main.party_info['p_town_xyz'] = main.party_info['x'], main.party_info['y'], main.party_info['z']

                    town.town_choice()

                    return True

                elif y_n.startswith('n'):
                    print('-'*save_load.divider_size)
                    return True

        else:
            return bool(len(main.party_info['current_tile'].town_list))


def find_chest_with_id(chest_id):
    # A very simple function that scans through a list of all existing Chest objects and returns the first
    # one it finds with the inputted chest_id

    for chest in all_chests:
        if chest.chest_id == chest_id:
            return chest

    return False


def serialize_chests(path):
    with open(path, mode='w') as j:
        json.dump([(c.chest_id, c.destroyed, c.opened) for c in all_chests], j, indent=4, separators=(', ', ': '))


def deserialize_chests(path):
    with open(path, encoding='utf-8') as j:
        json_chests = json.load(j)

    for j_chest in json_chests:
        find_chest_with_id(j_chest[0]).destroyed = j_chest[1]
        find_chest_with_id(j_chest[0]).opened = j_chest[2]



