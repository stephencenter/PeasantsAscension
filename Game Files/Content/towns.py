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

from TownClass import *
import npcs

# OVERWORLD TOWNS
nearton_h1_c1 = Chest([20], 1, "N-H1-C1")
nearton_h1_c2 = Chest([10, items.s_rejuv], 1, "N-H1-C2")
nearton_h1 = House("Philliard", [nearton_h1_c1, nearton_h1_c2])

nearton_h2_c1 = Chest([5, items.bone_bag, items.fairy_dust, items.feathers], 1, "N-H2-C1")
nearton_h2 = House("Alfred", [nearton_h2_c1])

town_nearton = Town('Nearton', """Nearton: A small village in the central region of the Forest.
It is in this very town where numerous brave adventurers have begun their
journey. Nearton is just your standard run-of-the-mill village: it has a
general store, an inn, and a few small houses. An old man  is standing
near one of the houses, and appears to be very troubled about something.""",
                    [npcs.philliard, npcs.alfred, npcs.sondalar, npcs.saar, npcs.npc_solou],
                    [nearton_h1, nearton_h2])

town_southford = Town('Southford', """Southford: A fair-size town in the central-southern region of the Forest.
The inhabitants of this town are known for being quite wise, and may
provide you with helpful advice.""",
                      [npcs.wesley, npcs.lazaro], [], inn_cost=2)

town_overshire = Town('Overshire', """Overshire: A city in the northwestern region of the Forest.
Overshire is the capital of Harconia, and as such is very densely populated.
The city is separated into three sectors: the upper-class inner portion
consisting of castle surrounded by reinforced stone walls, a lower-class
outer portion comprised of smalls buildings and huts, and a middle-class
section situated in between. As an outsider, you are forbidden to enter the
upper two, but are welcome to do as you wish in the lower.""", [npcs.joseph, npcs.stewson, npcs.jeffery, npcs.harthos],
                      [], inn_cost=5, gs_level=2)

town_charsulville = Town('Charsulville', """Charsulville: A plain village in the south east
region of the Forest. It is home to nothing special, although it's cheap
inn service and higher-quality products it sells more than makes up for this.
There is a ragged beggar standing in the middle of the road.""", [npcs.ethos, npcs.typhen], [], inn_cost=2, gs_level=2)

town_fort_sigil = Town('Fort Sigil', """Fort Sigil: A small village in the northern region
of the Forest. The citizens of this town have worked tremendously hard to
convert the rarely-used fort into a hospitable village, and have done
fairly well. Despite it's rich backstory, Fort Sigil doesn't get many
visitors. Perhaps there's a reason...""", [npcs.seriph, npcs.rivesh], [], gs_level=3)

town_tripton = Town('Tripton', """Tripton: When the town of Tripton was being built,
the people working on the project failed to notice that another town,
Fallville, just so happened to be located mere meters away from the
new town's borders. This has led to a bit of a rivalry between the
two towns, particularly between the village leaders.""", [npcs.kyle], [], inn_cost=3, gs_level=3)

town_fallville = Town('Fallville', """Fallville: When the town of Tripton was being built,
the people working on the project failed to notice that another town,
Fallville, just so happened to be located mere meters away from the
new town's borders. This has led to a bit of a rivalry between the
two towns, particularly between the village leaders.""",
                      [npcs.krystin, npcs.frederick], [], gs_level=2)

town_parceon = Town('Parceon', """Parceon: A highly populated town renown for it's rich
magical background. Parceon is home to the famous Sorcerers' Guild,
a group of unbelievably skilled and wise mages. The head of the guild,
Azura, lives in a large tower in the southwest side of the town.""",
                    [npcs.azura], [], gs_level=3)

town_sardooth = Town('Sardooth', """Sardooth: A ghost town. There has not been a single
permanent inhabitant of this town for more than 75 years. It is completely
run down, with most of the buildings having been destroyed in the Harconian
Revolution. While this town may seem interesting and historic, there is nothing
of value here.""",
                     [], [])

town_principalia = Town('Principalia', """Principalia: Principalia is the home of
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
your attention - probably because she just screamed "HALT!" at you.""",
                        [npcs.sakura], [])

town_new_ekanmar = Town('New Ekanmar', """New Ekanmar: The home of the Flyscorian Embassy in
Harconia. Prior to the Harconian Revolution, this town was the location of
a large portion of Flyscoria's troops in Harconia. The Harconians drove much of
them out, but a large number of them defected to the Harconian side and stayed.
After the war, the citizens gave up their weapons and became a peaceful town.
The vast majority of the inhabitants of this town are, naturally, Flyscors.
It seems that the Flyscorian Royal Family is visiting here - perhaps you can
talk with them for a bit.""", [npcs.f_jones, npcs.stravi, npcs.caesar], [], gs_level=3)

town_ravenstone = Town('Ravenstone', """Ravenstone: Ravenstone is a natural sanctuary,
home to dozens upon dozens of different flora and fauna. Naturally,
the majority population of Ravenstone consists of Druids and
other nature-magicians. Ravenstone is also the home of the Druids'
section of the Sorcerers' Guild. Vegetation grows on almost
every building and statue in the town. When the population of
the town is calculated, animals are counted as people. More than
35% of the population are various species of animals.""",
                       [npcs.strathius], [], gs_level=3)

town_ambercreek = Town('Ambercreek', """Ambercreek: Ambercreek is a large mining town
located in the Terrius Mt. Range. The Chin'toric embassy can be found
in the middle of this town surrounded by large stone walls and a few
guard-towers. Sugulat, the King of Chin'tor, can often be found mining
on the outskirts of town. A very troubled-looking old man is in
the southwest portion of the town near a few smaller houses.""",
                       [npcs.raidon, npcs.sugulat], [], gs_level=4, inn_cost=15)

town_whistumn = Town('Whistumn', """Whistumn: An ancient city situated on the border
between the Arcadian Desert and the Central Forest. The inhabitants of this town
are known for their skepticism and reasoning. Many of them are scientists and are
skilled mathematicians and engineers. This town has an ongoing rivalry with
the town of Parceon because of their magical background, but this appears
to be mostly one-sided. A saddened-looking woman and her husband are sitting
on the steps of the general store.""",
                     [npcs.polmor, npcs.serena], [], gs_level=4, inn_cost=13)

town_hatchnuk = Town("Hatchnuk", """Hatchnuk: Hatchnuk is the only remaining town in Harconia
that still has cases of "Hatchnuk's Blight", a plague-like disease that
killed hundreds of thousands of people during the 10th and 11th centuries.
Something about the strand that infects Hatchnuk seems to make it completely
incurable, as the disease has been running rampant for the past four centuries.
The economy of Hatchnuk has entirely collapsed, as the risk of spreading disease
is far too great for people to be walking out in the open doing business together.
As a result, there are no buildings that you are able to enter, and no people to talk
to. The only people who are around to speak to are the guards, but their plague-doctor-esque
apparel and stern looks make it clear that they are not in the mood for chit-chat.""",
                     [], [])

town_cesura = Town("Cesura", """Cesura: A town of great historical significance.
This town was named after King Cesura I, the war general during the Harconian Civil War
who helped to reunite the nation's six regions. Cesura was built on top of the site
of the Battle of Parchak, the definitive battle in the Civil War that Cesura used
to help the Central Forest win. There is a large monument to the King in the middle of
town, with the words "Here's to prosperity" written on a plaque at its feet.
An interesting thing to note is that Cesura is the only town that has a train
station. Construction of the town of Cesura was outsourced to Elysium, who is
the most technologically advanced civilization on the planet by far, having
developed and perfected the Steam Engine and later the Train before the year
1300 A.D.""",
                   [npcs.bamdeliit], [], wtrmelon_store=True)

town_sanguion = Town("Sanguion", """Sanguion: Sanguion is a save-haven for vampires. Vampires
are feared throughout Harconia, so this fairly unknown town is the only place they
can go without being persecuted. The vampires in this town are peaceful, and
actually refuse to drink the blood of intelligent lifeforms. As a matter of fact,
non-vampires who are afraid of vampires are actually more of a threat to civilization
than the actual vampires are! They look very friendly, although a few of them do look
quite scared for some reason. Perhaps you should investigate.""",
                     [npcs.pime, npcs.ariver], [], gs_level=5, inn_cost=18)

town_lantonum = Town("Lamtonum", """Lantonum: Lantonum is a small town that has the best
forge in all of Arcadia. Nearly 2/3s of all citizens of this town are
experienced blacksmiths, and 90% of all ores and minerals mined
in Chin'tor or Ambercreek are brought here. It is one of the wealthiest
cities in all of the desert region due to its Mythril, Magestite, and
Necrite bar exports.""",
                     [npcs.matthew], [], gs_level=4)

town_capwild = Town("Capwild", """Capwild: Capwild is a medium sized town situated in the
Terrius Mt. Range. Capwild is a supplier of grains and herbs for the entire region,
and makes extensive use of terrace farming to make up for the lack of arable land.""",
                    [], [], gs_level=5, inn_cost=15)

town_rymn_outpost = Town("Rymn Outpost", """Rymn Outpost: Rymn Outpost is one of the several
small villages established after the Thexian Incursion. All of the residents of this town
are soldiers or family members of soldiers, with the exception a few merchants. Rymn Outpost
is named after Rymnes, the Divinic gods of defense.""",
                         [], [], gs_level=5, inn_cost=17)

cottage1 = Town('Small Cottage', """Small Cottage: As the name would suggest,
this area only has a small cottage. An old man is tending to his
flock in a small pasture behind the building. There doesn't appear
be any other people near here.""",
                [npcs.alden], [], gs_level=-1, inn_cost=-1)


a_town_valenfall = Town("Valenfall", """Not much is known about the ancient city of Valenfall.
It's inhabitants claim that it was lifted up from the mainland several millenia ago
by his Divinity. The gods supposedly used Valenfall as the cornerstone, constructing
all of the surrounding land of Aethus around it. Valenfall is deeply intertwined with
nature, and monuments depicting the nature deities can be seen on every corner.
""", [npcs.fitzgerald], [], inn_cost=2, gs_level=4)

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

    for town in main.party_info['current_tile'].town_list:
        if enter:
            print('-'*25)

            sounds.item_pickup.play()

            while True:
                if isinstance(town, Tavern):
                    if town.new_location(add=False) not in inv_system.inventory['coord']:
                        y_n = input("How convenient, a tavern is nearby! Should your party investigate? | Yes or No: ")

                    else:
                        y_n = input(f'{town.name} is nearby. Should your party give it a visit? | Yes or No: ')

                else:
                    if town.new_location(add=False) not in inv_system.inventory['coord']:
                        y_n = input('There is a town nearby. Should your party investigate? | Yes or No: ')

                    else:
                        y_n = input(f'{town.name} is nearby. Should your party give it a visit? | Yes or No: ')

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    pygame.mixer.music.load('Content/Music/Chickens (going peck peck peck).ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(main.music_vol)

                    main.party_info['prev_town'] = main.party_info['current_tile']
                    main.party_info['p_town_xyz'] = main.party_info['x'], main.party_info['y'], main.party_info['z']

                    town.town_choice()

                    return True

                elif y_n.startswith('n'):
                    print('-'*25)
                    return True

        else:
            return bool(len(main.party_info['current_tile'].town_list))
