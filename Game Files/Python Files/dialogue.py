# This file is part of Peasants' Ascension.
#
# Peasants' Ascension is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peasants' Ascension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

import json
import sys
import copy

import items
import units
import save_load

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Conversation:
    def __init__(self, dialogue, conv_id, active=False):
        self.dialogue = dialogue
        self.active = active
        self.conv_id = conv_id

    def after_talking(self):
        pass


class Quest(Conversation):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, started=False, finished=False, active=False):
        Conversation.__init__(self, dialogue, conv_id, active)
        self.name = name  # The name of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.started = started  # is True if the quest has been started, false otherwise
        self.finished = finished  # is True if the quest is complete, false otherwise

    def give_quest(self):
        print('-'*save_load.divider_size)
        print(f'{self.q_giver} is offering you the quest "{self.name}".')

        while True:
            accept = main.s_input('Do you accept this quest? | Y/N: ').lower()

            if accept.startswith('y'):
                print('-'*save_load.divider_size)
                print(f'{self.q_giver}: "Terrific! Thank you for your help!"')
                main.s_input("\nPress enter/return ")
                self.started = True
                self.upon_starting()

                return

            elif accept.startswith('n'):
                print('-'*save_load.divider_size)
                print(f'{self.q_giver}: "Oh... That\'s fine. Come back later if you change your mind."')

                return

    def completion(self):
        self.upon_completing()

        print("Quest Complete!")
        print(f"You've received {self.reward[0]} XP and {self.reward[1]} GP for completing this quest.")
        main.s_input('\nPress enter/return')

        main.party_info['gp'] += self.reward[1]
        units.player.exp += self.reward[0]
        units.player.level_up()

        self.active = False

    def upon_starting(self):
        pass

    def upon_completing(self):
        pass


# -- Name: Solou -- Town: Nearton
def solou_c1_at():
    global solou_convo_1

    units.solou.enabled = True
    solou_convo_1.active = False

    print('-'*save_load.divider_size)
    print("Solou the Mage has been added to your party!")
    main.s_input('\nPress enter/return ')


solou_convo_1 = Conversation("""""", "solou_c1", active=True)
solou_convo_1.after_talking = solou_c1_at


def solou_q1_us():
    global joseph_quest_1

    joseph_convo_2.active = True
    joseph_quest_1.active = True


solou_quest_1 = Quest("A Courier's Resignation [MAIN QUEST]", """""", "Solou", [25, 25], "solou_q1", active=True)
solou_quest_1.upon_starting = solou_q1_us


# -- Name: Joseph -- Town: Overshire City
joseph_convo_1 = Conversation("Greetings, young adventurer. Welcome to Overshire.", "joseph_c1", active=True)


def joseph_c2_at():
    global joseph_convo_2

    joseph_convo_2.active = False
    solou_quest_1.completion()


joseph_convo_2 = Conversation("""\
Ah, Solou! Long time no see! I see you've taken up adventuring.
It must be nice to finally put that spellbook of yours to use!
Oh, what's this? A letter for me? Well, I'll be sure to read this
later. Thank you for delivering this to me!""", "joseph_c2")
joseph_convo_2.after_talking = joseph_c2_at

joseph_convo_3 = Conversation("""\
Go visit my friend Azura in Parceon. She knows more about this than
I do. Parceon is located at 24\u00b0N, 28\u00b0E in case you forgot.""", "joseph_c3")

joseph_quest_1 = Quest("To Parceon! [MAIN QUEST]", """\
Ah, Solou! Long time no see! I see you've taken up adventuring.
It must be nice to finally put that spellbook of yours to use!
*Solou and Joseph chat for a while. As mayor of Overshire, Joseph
is already well aware of Celeste being kidnapped.* Ah, so you adventurers
are questing to save his daughter? Well, I happen to know of a person
whose information would prove invaluable to you. Her name is Azura, and
she is the head of the Sorcerer's guild. She has been studying tomes and
has supposedly come up with a possible solution. She lives in a town
called Parceon, located at 24\u00b0N, 28\u00b0E.""", "Joseph", [75, 75], "joseph_q1")


def joseph_q1_us():
    global joseph_convo_3
    global joseph_convo_1

    joseph_convo_1.active = False
    joseph_convo_3.active = True


# -- Name: Orius -- Town: Valice

# -- Name: Azura -- Town: Parceon
azura_convo_1 = Conversation("""\
Hello, I'm Azura, leader of this town and head of the Sorcerer's Guild.
I'm quite busy right now, so please come back later if you wish to speak
to me.""", "azura_c1", active=True)

azura_convo_2 = Conversation("""\
Hello, I'm Azura, leader of this town and head of the Sorcerer's Guild.
I'm quite busy right now, so please come back later if you wish to speak
to me... Oh, what's that? Joseph of Overshire City sent you? Well in that
case, I suppose that I can take some time off from my duties to speak
to you. What is it that you need? ...I see. I know of a way to rescue
King Harconius II's daughter, as Joseph probably told you. It's quite
dangerous, however - none of the King's men have survived the journey.
Looking at you, however, I see much potential. There is one problem,
however: Our Kingdom has been infiltrated by the Thexus. I have no way
of verifying whether or not you are one of them. Actually, now that I
think about it, perhaps there IS a way... How about this: My father,
Raidon, has been having some problems lately. If you go help him out,
then you will have earned my trust. He lives in the town of Ambercreek, a
village right outside the exit of Barrier Cave. Good luck.""", "azura_c2")


def azura_c1_at():
    global azura_convo_2
    global azura_convo_3

    print('You write down the coordinates of Ambercreek.')
    main.s_input("\nPress enter/return ")
    azura_convo_2.active = False
    azura_convo_3.active = True


azura_convo_2.after_talking = azura_c1_at

azura_convo_3 = Conversation("""\
My father, Raidon, lives in the town of Ambercreek at -7\u00b0S, -51\u00b0W. Good luck!""", "azura_c3")


# -- Name: Raidon -- Town: Ambercreek
raidon_convo_1 = Conversation("""FILLER TEXT""", "raidon_c1", active=True)


# ---------------------------------------------------------------------------- #
# SIDE-STORY ARCS

# -- Graveyard Story-arc:
# --- Name: Stewson -- Town: Overshire
stewson_convo_1 = Conversation("""\
Our amazing Kingdom has 6 different regions: Tundra in the northwest, Swamp
in the southeast, Mountains in the northeast, and Desert in the southwest.
The Forest lies in the center, while the Shore surrounds them. There's a
small region somewhere around here that is the cause of much worry and panic
in this town: The Graveyard. Inside lies a dangerous apparition, feared by
all who have seen it. As the captain of the guard, my men and I have tried
and failed countless times to defeat that wretched ghost!""", "stewson_c1", active=True)

stewson_quest_1 = Quest('The Shadowy Spirit', """\
I wish someone would do something about this terrible ghost... Hey! You're a
strong adventurer, perhaps you could defeat this phantom? It's at position
8\u00b0N, -12\u00b0W.""", 'Stewson', [50, 75], "stewson_q1", active=True)

stewson_convo_2 = Conversation("""\
Please save us from this monstrous wraith!""", "stewson_c2")

stewson_convo_3 = Conversation("""\
You... you actually defeated it?! Thank you ever so much! Finally my men and
I can rest, and the town is safe! Take this, it is the least our town can
do for your bravery.""", "stewson_c3")

stewson_convo_4 = Conversation("Thank you again for your help, adventurer!", "stewson_c4")


def stewson_q1_us():
    global stewson_convo_1
    global stewson_convo_2
    units.menacing_phantom.active = True
    stewson_convo_1.active = False
    stewson_convo_2.active = True


def stewson_q1_uc():
    global stewson_convo_3
    global rivesh_convo_2
    global rivesh_quest_1

    stewson_convo_3.active = True
    rivesh_convo_2.active = False
    rivesh_quest_1.active = True
    print('-'*save_load.divider_size)
    print('You now have experience defeating ghosts!')
    main.s_input("\nPress enter/return ")


stewson_quest_1.upon_starting = stewson_q1_us
stewson_quest_1.upon_completing = stewson_q1_uc

# --- Name: Seriph -- Town: Fort Sigil
seriph_convo_1 = Conversation("""\
...You actually came to this town? And of your own free will, too?! You are
truly a fool, although I suppose your bravery is admirable.""", "seriph_c1", active=True)
seriph_convo_2 = Conversation("""\
What?! You're going to try to kill the evil spirit? You're truly stupider
than I thought. I wish you good luck nonetheless.""", "seriph_c2")
seriph_convo_3 = Conversation("I can't believe you killed the evil spirit! We cannot thank you enough!", "seriph_c3")

# --- Name: Rivesh -- Town: Fort Sigil
rivesh_convo_1 = Conversation("""\
Welcome, brave adventurer. I'm sure that you've been informed of the
problems around here, so I'd recommend... Oh, what's that? You haven't?
Well in that case, let me tell you. A long time ago, a number of foolish
adventurers, searching for fame and glory, stumbled upon this fort.
Inside, they found a terrifying ghost, which they oh-so-cunningly
defeated -- or so they thought! No, instead the ghost had grown tired
of the pointless battle, and decided to hide in the shadows of the unsuspecting
"heroes". When they least expected it, the ghost possessed them! As
punishment for their foolishness, the evil spirit now forcefully takes a
victim from this town every 10 days and forbids its inhabitants from leaving!""", "rivesh_c1", active=True)

rivesh_convo_2 = Conversation("""\
Hey... I don't suppose that you have any experience with fighting ghosts,
do you? No? Ok then. If you find someone who has defeated a very menacing
phantom before, please request that they come help us!""", "rivesh_c2", active=True)

rivesh_convo_3 = Conversation("""\
Help us, young adventurer! You are the only one who can save us from this
terrible spirit!""", "rivesh_c3")

rivesh_convo_4 = Conversation("""\
Y-you defeated the evil spirit? Praise Guido's beard! We are free of this
curse! You are forever in our gratitude, young hero!""", "rivesh_q1")

rivesh_convo_5 = Conversation("""\
Thanks again, hero! We are forever indebted to you!""", "rivesh_c4")

rivesh_quest_1 = Quest("The Curse of Fort Sigil", """\
Hey... I don't suppose that you have any experience with fighting ghosts,
do you? Wait, what's that? You defeated the Phantom that was haunting the
Overshire Graveyard!? Well in that case, we may just have a chance!
Please help us, oh please!""", "Rivesh", [200, 200], "rivesh_q1")


def rivesh_q1_us():
    global rivesh_convo_1
    global rivesh_convo_2
    global rivesh_convo_3
    global seriph_convo_1
    global seriph_convo_2

    rivesh_convo_1.active = False
    rivesh_convo_2.active = False
    rivesh_convo_3.active = True
    seriph_convo_1.active = False
    seriph_convo_2.active = True
    units.cursed_spectre.active = True


def rivesh_q1_uc():
    global rivesh_convo_4
    global seriph_convo_2
    global seriph_convo_3

    rivesh_convo_4.active = True
    seriph_convo_2.active = False
    seriph_convo_3.active = True


rivesh_quest_1.upon_starting = rivesh_q1_us
rivesh_quest_1.upon_completing = rivesh_q1_uc


# ---------------------------------------------------------------------------- #
# SIDEQUESTS

# --ALFRED OF NEARTON--
alfred_convo_1 = Conversation("""\
It is rumored that a mighty jelly-creature lives south of this very town. 
Supposedly he's been devourering wild animals in the forest at a terrifying
rate, which is causing a lot of trouble for local hunters! And we're worried
that if he gets bored of his food in the forest that he'll come for us!
Unfortunately, the local militia is busy dealing with something else, so we
can't count on them to stop it. I'd be careful around there if I were you.""", "alfred_c1", active=True)


def alfred_q1_us():
    # Stands for "Alfred Quest 1 -- Upon Starting
    # Changes some of his dialogue options to reflect a quest beginning.
    global alfred_convo_1
    global alfred_convo_2
    units.master_slime.active = True
    alfred_convo_1.active = False
    alfred_convo_2.active = True


def alfred_q1_uc():
    # Stands for "Alfred Quest 1 -- Upon Completing
    global alfred_convo_3
    global alfred_convo_4
    alfred_convo_3.active = False
    alfred_convo_4.active = True


alfred_quest_1 = Quest('A Slimy Specimen', """\
...Actually, now that I think about it, do you think you could possibly
dispose of this vile creature? It's located just south of here.""", 'Alfred', [30, 50], "alfred_q1", active=True)
alfred_quest_1.upon_starting = alfred_q1_us
alfred_quest_1.upon_completing = alfred_q1_uc

alfred_convo_2 = Conversation("""\
Come back here when you defeat the evil Master Slime. Good luck!""", "alfred_c2")

alfred_convo_3 = Conversation("""\
You defeated the evil Master Slime?! Amazing! Now we can sleep easy at night
knowing our animals are safe. Take this, adventurer, you've earned it.""", "aldred_c3")

alfred_convo_4 = Conversation("""\
Greetings, Hero! Good luck on your adventures!""", "alfred_c4")

# -- Name: Kyle -- Town: Tripton
kyle_convo_1 = Conversation("""\
Greeting, traveller. I am Kyle, Tripton's Village Elder. You aren't from
Fallville, right? Good. Those stupid Fallvillians need to get away from our
land! It's they're fault they made a town that was so easy to miss! I don't
care if we have to go to war with those dingbats, I'm not leaving this spot!""", "kyle_c1", active=True)

kyle_convo_2 = Conversation("""\
Adventurer, we have heard reports that a mighty beast is in our land!
None of our men are willing to risk their lives to stop it. We are doomed.""", "kyle_c2")

kyle_convo_4 = Conversation("Welcome, adventurer, to the town of Tripton!", "kyle_c4")


def kyle_c3_at():
    # Stands for "Kyle Phrase 3: After Talking"
    global kyle_convo_3
    global kyle_convo_4
    global alden_quest_1
    global alden_convo_2

    kyle_convo_3.active = False
    kyle_convo_4.active = True

    if krystin_convo_4.active:
        alden_quest_1.finished = True
        alden_convo_2.active = False


kyle_convo_3 = Conversation("""\
The mighty monster has fallen? Thank god! What's this you say? The Fallvillians
defeated it? I supposed we owe them our lives. Perhaps we should think about
negotiating peace...""", "kyle_c3")
kyle_convo_3.after_talking = kyle_c3_at

# -- Name: Krystin -- Town: Fallville
krystin_convo_1 = Conversation("""\
Hello, I am the Village Elder of Fallville. We don't take kindly to Triptonians
around here, so tell us if you see any. What I don't understand is that the
silly Triptonians blame us for their poor eyesight. It's all their fault, and
they know it!""", "krystin_c1", active=True)
krystin_convo_2 = Conversation("AHHH! Help! There's a m-m-monster out there! Someone go kill it! AHHH!", "krystin_c2")
krystin_convo_4 = Conversation("""\
Greetings, hero! Welcome to Fallville.""", "krystin_c4")


def krystin_c3_at():
    # Stands for "Krystin Phrase 3: After Talking"
    global krystin_convo_3
    global krystin_convo_4
    global alden_quest_1
    global alden_convo_2

    krystin_convo_3.active = False
    krystin_convo_4.active = True

    if kyle_convo_4.active:
        alden_quest_1.finished = True
        alden_convo_2.active = False


krystin_convo_3 = Conversation("""\
What, the monster is dead? Thank goodness! Oh, so the Triptonians killed it?",
Well then... I guess that we owe them our gratitude. Perhaps we should think",
about negotiating peace...""", "krystin_c3")
krystin_convo_3.after_talking = krystin_c3_at


# -- Name: Frederick -- Town: Fallville
frederick_convo_1 = Conversation("""\
I hear that there is a wise sage that has taken up residence in a small
cottage southwest of this town. I would go and talk to him, but monsters
have been roaming around the outskirts of town lately and it just isn't safe
to travel anymore.""", "frederick_c1", active=True)
frederick_convo_2 = Conversation("""\
There's a monster outside of town, and a big one at that! I hope it goes away.""", "frederick_c2")
frederick_convo_3 = Conversation("Thank heavens, the mighty beast has fallen.", "frederick_c3")


# -- Name: Alden -- Town: Small Cottage
def alden_q1_us():
    global alden_convo_1
    global krystin_convo_1
    global kyle_convo_1
    global krystin_convo_2
    global kyle_convo_2
    global frederick_convo_1
    global frederick_convo_2

    alden_convo_1.active = True
    kyle_convo_1.active = False
    kyle_convo_2.active = True
    krystin_convo_1.active = False
    krystin_convo_2.active = True
    frederick_convo_1.active = False
    frederick_convo_2.active = True
    units.terr_tarant.active = True


def alden_q1_uc():
    global alden_convo_3
    global alden_quest_1

    alden_quest_1.active = False
    alden_convo_3.active = True


alden_quest_1 = Quest("Stop the Strife", """\
Greetings, adventurer. I'm sure that you have heard of the conflict going on
between the villages of Fallville and Tripton. I have an idea on how to settle
this foul feud, but alas, I cannot perform it due to my old and fragile
state. You, however, appear to be a very young and capable adventurer. Do you
perhaps think that you could help me? I need you to go defend the towns of
Fallville and Tripton from a terrible monster. This is a monster I will be
summoning, of course. Afterwards, spread word in the two towns that an
anonymous warrior from the opposite town defeated it! This should bring an end
to their constant bickering. I will summon the monster at coordinates
-23\u00b0S, -11\u00b0W.""",  'Alden', [175, 200], "alden_q1", active=True)
alden_quest_1.upon_starting = alden_q1_us
alden_quest_1.upon_completing = alden_q1_uc

alden_convo_1 = Conversation("""\
I've summoned the mighty beast. Now hurry up and dispose of it before it causes any damage.""", "alden_c1")

alden_convo_2 = Conversation("""\
You've defeated him? Good, now go talk to the village elders! Good luck!""", "alden_c2")

alden_convo_3 = Conversation("""\
Thanks again, hero. You've saved those towns a lot of trouble.""", "alden_c3")


# -- Name: Polmor -- Town: Whistumn
polmor_convo_1 = Conversation("""\
Our poor daughter! Serena and I have been working on a cure, but
we cannot find anyone stup-I mean brave enough to gather the
resources we need. All is lost if we cannot get the ingredients.""", "polmor_c1", active=True)

polmor_convo_2 = Conversation("""\
Please, return once you have obtained one Monster Fang, one Serpent Scale
and one Fairy Dust. You must save our daughter!""", "polmor_c2")

polmor_convo_3 = Conversation("""\
...Wait, what?! You obtained the items we needed? You are our savior! We owe
our lives to you, you are truly a hero! *He walks over to his wife, and the
two begin mixing the ingredients to make the cure for Hatchnuk's Blight*
At last, we have the cure! Let us not waste time. *The two administer the
medicine to their daughter, and she immediately begins feeling better.* Oh joy
of joys! Our daughter is healed! How can we ever repay you, oh noble adventurer
and vanquisher of the Blight? Here, take this. It is the absolute least that we
can do.""", "polmor_c3")


def polmor_q1_us():
    global serena_convo_2
    global serena_convo_1
    global polmor_convo_2
    global polmor_convo_1

    serena_convo_1.active = False
    serena_convo_2.active = True
    polmor_convo_1.active = False
    polmor_convo_2.active = True


def polmor_q1_uc():
    global serena_convo_2
    global serena_convo_3
    global polmor_convo_2

    serena_convo_3.active = True
    serena_convo_2.active = False
    polmor_convo_2.active = False
    polmor_quest_1.active = False

    print('-'*save_load.divider_size)
    print('Serena and Polmor will now heal you for free if you visit them!')


polmor_quest_1 = Quest("Fight Against the Blight", """\
Wait a minute... I am so stupid! According to my calculations, you are the
legendary adventurer of Nearton! Yes, it must be you , adventurer, help our
daughter! The only way to get the ingredients is to defeat several monsters
and collect their remains. Specifically, I need one Fairy Dust, one Serpent
Scale, and one Monster Fang. You're the only one who can save her!""", "Polmor", [450, 450], "polmor_q1", active=True)
polmor_quest_1.upon_starting = polmor_q1_us
polmor_quest_1.upon_completing = polmor_q1_uc


def polmor_c2_at():
    # Check the player's inventory for the objects necessary to finish the quest.
    any_fangs = False
    any_scales = False
    any_dust = False

    for item in items.inventory['misc']:
        if item.name == 'Monster Fang':
            any_fangs = True

        elif item.name == 'Serpent Scale':
            any_scales = True

        elif item.name == 'Fairy Dust':
            any_dust = True

    if any_fangs and any_scales and any_dust:
        # Iterate over a copy to prevent problems
        for item in items.inventory['misc'][:]:
            if item.name == 'Monster Fang' and any_fangs:
                items.inventory['misc'].remove(item)
                any_fangs = False

            elif item.name == 'Serpent Scale' and any_scales:
                items.inventory['misc'].remove(item)
                any_scales = False

            elif item.name == 'Fairy Dust' and any_dust:
                items.inventory['misc'].remove(item)
                any_dust = False

        polmor_quest_1.finished = True
        print('-'*save_load.divider_size)

        # TODO!!
        # npcs.polmor.speak()


polmor_convo_2.after_talking = polmor_c2_at


# -- Name: Matthew -- Town: Lantonum


def matthew_c1_at():
    global matthew_convo_1
    matthew_convo_1.active = False


matthew_convo_1 = Conversation("""\
*You try to talk to the man in the bar, but he is too busy listening to
music on his 'iSound' to notice you. Suddenly, a peasant walks up behind
him, screams 'Witch!', grabs the iSound, and smashes it to bits on the floor.
He then proceeds to set it on fire and bury the ashes in the dirt behind the
bar.*""", "matt_c1", active=True)
matthew_convo_1.after_talking = matthew_c1_at


def matthew_c2_at():
    global matthew_convo_3
    global matthew_convo_4
    global matthew_convo_2

    matthew_convo_2.active = False

    items.remove_item("musicbox")

    # TODO!!
    # npcs.matthew.speak()


matthew_convo_2 = Conversation("""\
Hello, friend! Have you gotten me a new iSound yet?""", "matt_c2")
matthew_convo_2.after_talking = matthew_c2_at


def matthew_c3_at():
    global matthew_convo_3
    matthew_convo_3.active = False


matthew_convo_3 = Conversation("""\
No? That's okay. Just pick one up for me when you get the chance. You can
purchase them at the town of Cesura, located at 123\u00b0N, 58\u00b0E.""", "matt_c3")
matthew_convo_3.after_talking = matthew_c3_at


def matthew_c4_at():
    global matthew_quest_1
    global matthew_convo_4

    matthew_quest_1.finished = True
    matthew_convo_4.active = False

    # TODO!!
    # npcs.matthew.speak()


matthew_convo_4 = Conversation("""\
You have? Wonderful! *He takes the iSound from your hand and pulls out 1250 GP*""", "matt_c4")
matthew_convo_4.after_talking = matthew_c4_at

matthew_convo_5 = Conversation("""\
*He looks quite depressed.*""", "matt_c5")


def matthew_q1_us():
    global matthew_convo_1
    global matthew_convo_2

    matthew_convo_1.active = False
    matthew_convo_2.active = True


def matthew_q1_uc():
    global matthew_convo_5
    global matthew_quest_1
    matthew_convo_5.active = True
    matthew_quest_1.active = False


matthew_quest_1 = Quest('iSounds Good', """\
Dangit, that happens all the time! Those idiots keep calling my iSound MP3
player a witch - this is the fifth one I've gone through this week! The
company that makes them only sells them in Elysium, as nobody in Harconia
could tell an MP3 player from a brick if their life depended on it. Hey, I'll
tell you want: If you go to Cesura, the train town near the border of Harconia
and Elysium, and buy me a new iSound, I will reward you greatly. Remember:
iSounds have watermelons on the back. If you get one with a grapefruit, then
you're just paying a lot of money for a cheap knockoff brand. And definitely
stay away from papaya phones. Can you do that for me?""", "Matthew", [1250, 1250], "matt_q1", active=True)
matthew_quest_1.upon_starting = matthew_q1_us
matthew_quest_1.upon_completing = matthew_q1_uc


# -- Name: Pime -- Town: Sanguion
pime_convo_1 = Conversation("""\
Hello, traveller! You do not look familiar - quick, come inside, it's not been
safe to stay out here for the past few weeks. *Pime ushers you into a tavern
filled with people whom he seems to be quite friendly with. They likewise are
quite kind to you.* My name is Pime. I am the chief of this town, and the head
of Sanguion's militia. As I'm sure you know, me, and all the other people in
this inn, are vampires. Do not be alarmed! We only feast on wild animals and
vampire hunters. You are completely safe, as long as you are not a hunter,
that is. As of late, a new group of vampire hunters named the
'Anti-blood Squad'. Not only do these terrorists have an extraordinarily
uncreative name, but they've also been capturing our friends and family and
are torturing, ransoming, and even killing them! We vampires are not harmful
to society, and do not deserve this kind of treatment! Our loved ones are
dying to those monsters, and we don't have anywhere near enough manpower to
put a stop to it! What are we to do?!""", "pime_c1", active=True)

pime_convo_2 = Conversation("""\
Perhaps you could... nevermind, we need a more experienced individual to
help us with our plight. Come back later. *Pime needs someone who is at
least level 10. Go level up a bit!*""", "pime_c2")


pime_quest_1 = Quest("The Hated Hunter", """\
Hey - you look like quite the seasoned adventurer. Maybe you could help
us! I hope this isn't too much to ask, but could you possibly defeat
this dreaded vampire hunter for us? He's causing us so much pain, we need
someone to get rid of him.""", "Pime", [1000, 1000], "pime_q1")

pime_convo_3 = Conversation("""\
Please deal with those blasted vampire hunters! Their hideout
is located at -68\u00b0S, -93\u00b0W.""", "pime_c3")

pime_convo_4 = Conversation("""\
Thank you every so much for ridding us of those vile terrorists! You are
forever in our gratitude!""", "pime_c4")


def pime_c1_at():
    global pime_convo_2
    global pime_quest_1
    global pime_convo_1

    if units.player.lvl >= 10:
        pime_quest_1.active = True
        pime_convo_1.active = False
        pime_convo_2.active = False

    else:
        pime_convo_2.active = True


def pime_q1_us():
    global pime_convo_1
    global pime_convo_3

    pime_convo_1.active = False
    pime_convo_3.active = True
    # units.anti_blood_squad.active = True


def pime_q1_uc():
    global pime_quest_1
    global pime_convo_4

    pime_quest_1.active = False
    pime_convo_4.active = True


pime_convo_1.after_talking = pime_c1_at
pime_quest_1.upon_starting = pime_q1_us
pime_quest_1.upon_completing = pime_q1_uc


# ----------------------------------------------------------------------------#
# UNIMPORTANT CHARACTERS

# -- Name: Philliard -- Town: Nearton
philliard_convo_1 = Conversation("""\
Hello, adventurer! Welcome to the Kingdom of Harconia!""", "philliard_c1", active=True)


# -- Name: Sondalar -- Town: Nearton
sondalar_convo_1 = Conversation("""\
Greetings! Say, I haven't seen you in quite a while! I've been travelling
across the Kingdom for the past few years, and haven't had time to say hello.
Let me share some of the knowledge I gained while on my route: every town
has a general store and an inn. Make good use of them! The general store
sells all sorts of helpful equipment, and the further you travel from Nearton,
the better their stock will get! Don't ask why - all I've heard is that it's
supposedly better for business or something. Inns are helpful too. They will,
usually for a fee, heal all your wounds and give you some precious time and
space to write in that travel log you've got there. That's all I've got to say,
catch up with you soon hopefully!""", "sondalar_c1", active=True)


# -- Name: Saar -- Town: Nearton
saar_convo_1 = Conversation("""\
I haven't really explored too far away from this town. In fact, the only other
towns I've been to are Southford, located at -2\u00b0S, -2\u00b0W, and
Overshire, located at 5\u00b0N, -3\u00b0W. Overshire is a pretty big city,
though - in fact, it's the capital of our Kingdom!""", "saar_c1", active=True)


# -- Name: Wesley -- Town: Southford
wesley_convo_1 = Conversation("""\
Adventurers around this area say that monsters tend to be stronger the farther
from 0\u00b0N, 0\u00b0E that you travel. However, monsters there also give better
loot. Be careful.""", "wesley_c1", active=True)


# -- Name: Lazaro -- Town: Southford
lazaro_convo_1 = Conversation("""\
Greetings, adventurer from Nearton! How do I know who you are, you ask? Well,
I am the oracle of Southford! The Great Divinity told me that you would be coming.
He gave me a message:

"Your position is saved whenever you visit a town. If you die, you will return there!"

That's what He said. I do not understand His words, but I hope they serve",
you well.""", "lazaro_c1", active=True)


# -- Name: Typhen -- Town: Overshire
typhen_convo_1 = Conversation("""\
I've heard that when you use healing spells, you restore additional HP based
on your wisdom. And paladins supposedly get an even larger restoration bonus
when they heal!""", "typhen_c1", active=True)


# -- Name: Jeffery -- Town: Overshire
jeffery_convo_1 = Conversation("""\
Have you heard about what happened to Princess Celeste? The news of her
kidnapping is spreading across the kingdom like wildfire! Those blasted
Thexians will pay for this!""", "jeffery_c1", active=True)


# -- Name: Harthos -- Town: Overshire
harthos_convo_1 = Conversation("""\
Welcome to Overshire, stranger! Our Kingdom's capital is pretty big, so try
not to get lost, haha!""", "harthos_c1", active=True)


# -- Name: Ethos -- Town: Valice
ethos_convo_1 = Conversation("""\
Any smart adventurer would keep track of town coordinates and powerful monsters
in their inventory. If you get lost, check there.""", "ethos_c1", active=True)


# -- Name: Fly -- Town: New Ekanmar
fly_convo_1 = Conversation("""\
Hello, adventurer! My name is Fly, Duke of Celemia. I'm
quite busy right now, please come back later if you wish to speak to me.""", "fly_c1", active=True)


# -- Name: Stravi -- Town: New Ekanmar
stravi_convo_1 = Conversation("""\
Greetings, young traveller. I am Stravi, Duchess of Celemia. My husband
and I are on important business relating to the recent kidnapping of King
Harconius II's daughter, Celeste. Please return in a few weeks if you wish
to speak to Fly and me. Oh, and whatever you do, do not under ANY
circumstances mention the word 'chandelier' to my husband. It makes him very
upset for some reason.""", "stravi_c1", active=True)


# -- Name: Caesar -- Town: New Ekanmar
caesar_convo_1 = Conversation("""\
*Caesar, Fly's pet strawberry dragon, runs away and hides behind
his owner before you get a chance to converse with him.*""", "caesar_c1", active=True)


# -- Name: Sakura -- Town: Principalia
sakura_convo_1 = Conversation("""\
HALT! State your business! Ah, you want to see the King, do you?
Well, the King is currently in Overshire. Sakura cannot imagine
that he is accepting visitors right now, though. Unless you have
something really important to tell him, such as how to save his
daughter, Sakura doesn't see you talking to him in your future.
Now get out of here, Sakura is busy!""", "sakura_c1", active=True)


# -- Name: Strathius -- Town: Ravenstone
strathius_convo_1 = Conversation("""\
Greetings, man! I'm like, Strathius, and I'm a druid. I'm one with like,
nature. I'm gonna give you some helpful advice, man. Monsters can give you
these like, things, that are called \"Status Ailments\" which like, totally
harsh your style brah. Getting muted totally makes your stuff get like totally
lost, so you can't use those radical items you have in your backpack.
Paralyzation makes you totally slow for a while, so you have your
turn later and it's harder to away dog. Weakness makes you like
a total softy, and you won't deal much physical damage, man. Poison
is mega-harsh dude. It makes you take a little bit of damage each,
like, turn. Definitely not cool. Blindness is also totally whack
man - it makes you aim like a total nut and do less pierce damage.
Silence is bad news for mages 'cuz it means you can't use magic for a bit.
Always keep a stash of items to cure these sicknesses man.""", "strathius_c1", active=True)


# -- Name: Sugulat -- Town: Ambercreek
sugulat_convo_1 = Conversation("""\
Greetings! My name is Sugulat, Duke of Chin'tor and legendary digger of
holes. Y'know, you look like a nice guy. I'm going to tell you a little
secret: If you buy a shovel from the general store, you can dig up valuable
gems in certain places! They're all over the place, there's usually at least
one in every area you visit.""", "sugalat_c1", active=True)


# -- Name: Serena -- Town: Whistumn
serena_convo_1 = Conversation("""\
Oh, woe is me! My daughter has fallen ill from a terrible disease! They call
it "Hatchnuk's Blight", and it is very deadly. Oh, what am I to do?
*sobs uncontrollably*""", "serena_c1", active=True)

serena_convo_2 = Conversation("""\
You are a good man, trying to help our daughter! Good luck on your quest!""", "serena_c2")

serena_convo_3 = Conversation("""\
You are our heroes! Here, allow us to treat your wounds.""", "serena_c3")


def serena_c3_at():
    units.heal_pcus(1)
    print('-'*save_load.divider_size)
    print('Polmor and Serena get to work on healing your party...')
    main.smart_sleep(2)
    print('Your party has been fully healed.')
    main.s_input("\nPress enter/return ")


serena_convo_3.after_talking = serena_c3_at


# -- Name: Morrison -- Town: Cesura
morrison_convo_1 = Conversation("""\
Hello, sir! I'm Morrison, the head engineer of Cesura! I'm a native Elysian,
and have only been here for around a year, so I'm pretty new to this place!
Most of my time is spent making sure that these trains run properly. By the
way, do you know what \"witch\" means? Hythic isn't my first language, and the
townsfolk keep calling me that when I turn on the trains. Witch is a good
thing, right?""", "morrison_c1", active=True)


# -- Name: Ariver -- Town: Sanguion
ariver_convo_1 = Conversation("""\
*Ariver mistakes you for a vampire hunter and runs quickly into his house,
locking the doors, shutting the windows, and closing the blinds. As you begin
walking away, scratching your head in confusion, you see him look out the
window and walk back outside, having determined you are not a threat at the
moment.*""", "ariver_c1", active=True)


# -- Name: Fitzgerald -- Town: Valenfall
fitz_convo_1 = Conversation("""\
*hic* Pay no attention to the behind behind the curtain! *The man appears to
be quite drunk. You also notice a distinct lack of any curtain nearby.*
*hic* Drop that, you thief! Give me back my penny-loafers! *You slowly walk
away from the raving drunk.*""", "fitz_c1", active=True)


all_dialogue = [
    solou_convo_1, solou_quest_1,

    rivesh_convo_1, rivesh_convo_2, rivesh_convo_3, rivesh_convo_4, rivesh_convo_5, rivesh_quest_1,

    alfred_convo_1, alfred_convo_2, alfred_convo_3, alfred_convo_4, alfred_quest_1,

    stewson_convo_1, stewson_convo_2, stewson_convo_3, stewson_convo_4, stewson_quest_1,

    kyle_convo_1, kyle_convo_2, kyle_convo_3, kyle_convo_4,

    krystin_convo_1, krystin_convo_2, krystin_convo_3, krystin_convo_4,

    frederick_convo_1, frederick_convo_2, frederick_convo_3,

    joseph_convo_1, joseph_convo_2, joseph_convo_3, joseph_quest_1,

    alden_quest_1, alden_convo_1, alden_convo_2, alden_convo_3,

    azura_convo_1, azura_convo_2, azura_convo_3,

    polmor_convo_1, polmor_convo_2, polmor_convo_3, polmor_quest_1,
    serena_convo_1, serena_convo_2, serena_convo_3,

    matthew_convo_1, matthew_quest_1, matthew_convo_2,
    matthew_convo_3, matthew_convo_4, matthew_convo_5,

    pime_convo_1, pime_quest_1, pime_convo_2, pime_convo_3, pime_convo_4,

    lazaro_convo_1,

    philliard_convo_1,
    fly_convo_1,
    stravi_convo_1,
    sakura_convo_1,
    sugulat_convo_1,
    raidon_convo_1,
    caesar_convo_1,
    wesley_convo_1,
    seriph_convo_1,
    strathius_convo_1,
    ariver_convo_1,
    fitz_convo_1,
    harthos_convo_1,
    typhen_convo_1,
    sondalar_convo_1,
    morrison_convo_1,
    ethos_convo_1,
    jeffery_convo_1,
    saar_convo_1,
    seriph_convo_2,
    seriph_convo_3
]


def serialize_dialogue(path):
    json_dialogue = {}

    for c in all_dialogue:
        if isinstance(c, Quest):
            json_dialogue[c.conv_id] = [c.active, c.started, c.finished]

        else:
            json_dialogue[c.conv_id] = [c.active]

    with open(path, encoding='utf-8', mode='w') as f:
        json.dump(json_dialogue, f, indent=4, separators=(', ', ': '))


def deserialize_dialogue(path):
    global all_dialogue

    with open(path, encoding='utf-8') as f:
        j_log = json.load(f)

    for key in j_log:
        for c in all_dialogue[:]:
            if key == c.conv_id:
                if isinstance(c, Quest):
                    c.active, c.started, c.finished = j_log[key][0], j_log[key][1], j_log[key][2]
                else:
                    c.active = j_log[key][0]


for item1 in copy.copy(globals()):
    if isinstance(globals()[item1], Conversation) and globals()[item1] not in all_dialogue:
        print(f"{item1} not in all_dialogue!")
