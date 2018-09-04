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
    def __init__(self, dialogue, conv_id, active):
        self.dialogue = dialogue
        self.active = active
        self.conv_id = conv_id

    def after_talking(self):
        pass


class Quest(Conversation):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(dialogue, conv_id, active)
        self.name = name  # The name of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.accept_msg = accept_msg  # The text that's displayed if you accept the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.started = False  # is True if the quest has been started, false otherwise
        self.finished = False  # is True if the quest is complete, false otherwise

    def give_quest(self):
        print('-'*save_load.divider_size)
        print(f'{self.q_giver} is offering you the quest "{self.name}".')

        while True:
            accept = main.s_input('Do you accept this quest? | Y/N: ').lower()

            if accept.startswith('y'):
                print('-'*save_load.divider_size)
                print(f'{self.q_giver}: "{self.accept_msg}"')
                main.s_input("\nPress enter/return ")
                self.started = True
                self.upon_starting()

                return

            elif accept.startswith('n'):
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
class SolouConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


solou_convo_a = SolouConvoA("""\
Hey, sir! Hold it right there! You, you're the one I'm supposed to deliver
this letter to! The King couldn't remember your name but he gave me this
drawing and it looks exactly like you, so it must be you! Here goes!
Ahem... "Dear Mayors of Overshire: I regret to inform you that due to the
increasing costs of maintaining the Kingdom, taxes are being increased 2%
effective next month, and will increase a further 2% the following month.
I trust that your tax collectors can handle this and that your guards can
handle any resistance to this change from citizens. Thank you for your
cooporation. Signed, King Harconius II."
""", "solou_c1", True)


class SolouConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        units.solou.enabled = True

        print("-"*save_load.divider_size)
        print("Solou has joined your party!")
        main.s_input("\nPress enter/return ")
        print("-"*save_load.divider_size)


solou_convo_b = SolouConvoB("""\
Okay, that's all it said. Good luck with that tax stuff... Wait, what do you
mean you're not a mayor? You're just a peasant?! That explains a lot, like why
you're wearing that instead of more typical mayoral attire... Well this is bad.
I've never delievered a letter to the wrong person before, I'm not really sure
what to do... I'm just a courier for the King, I just deliver letters. They
don't teach me how to make decisions. Well one's thing for sure, I can't let
you get the news out about these tax increases. I'm gonna have to follow you 
around to make sure you don't snitch! Actually, I can't just follow you around,
I have more letters to deliver, you're gonna have to come with me.""", "solou_c2", True)


class SolouConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


solou_convo_c = SolouConvoC("""\
Okay, I've made a decision. Which is a big deal for me, like I said I'm
not great at that. But I've decided that I'm done being a courier. I've always
wanted to be a master wizard, and you look like you're someone destined for
greatness. Just kidding, you look like a mess. But I sense adventure in you!
So we're gonna go on an adventure. Just for the heck of it! Maybe later we'll
get some crazy fantasy world motivation that will drive us into saving the
world, but not now. Before we leave though, let's read this one last letter I
have. I know you shouldn't snoop, but who cares, it's probably not that
important anyway.""", "solou_c3", True)


class SolouQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        set_active(solou_convo_a, False)
        set_active(solou_convo_b, False)
        set_active(solou_convo_c, False)
        set_active(solou_convo_d, True)
        set_active(solou_convo_e, True)


solou_quest_a = SolouQuestA("A Courier's Resignation [MAIN QUEST]", "Solou", """\
Ahem... "Dear Joseph, Mayor of Overshire: Hello Joseph, I have terrible news.
This news is urgent, and it's important that you do not tell anyone else about
this unless it is absolutely necessary. My newborn daughter has been kidnapped.
My wife Isabella was secretly pregnant, hence her lack of public appearances
for the past several months. The public does not know she was with child.
Orsephius, the Duke of the Province of Thex, has privately claimed 
responsibility for the abduction. This is the true reason that I have closed 
off all city gates and province borders. From a military standpoint, Thex is 
weak. We would have no problem rescuing my daughter. However, my scouts have
determined that there is an impenetrable forcefield generated by Magestite
surrounding the island. Magestite is completely resistant to magic, there's
absolutely no way through. I'm calling a meeting in the castle in three weeks
to discuss plans on how to deal with this. Please be there. Thank you, Signed
King Harconius II." That's... what it said. Oh no, this is REALLY bad. The King
had a daughter? And she's been kidnapped? And Thex is responsible?! It says 
that it was to be delivered to Joseph, the Mayor of Overshire City. We 
absolutely have to deliver this letter RIGHT NOW.""",
                            "Okay cool, let's go deliver this thing.", [50, 50], "solou_q1", True)


class SolouConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        set_active(solou_convo_d, False)

        items.add_item("fast_map")
        print("-"*save_load.divider_size)
        print("Solou gave you a fast travel atlas! Access it from the Tools menu.")
        main.s_input("\nPress enter/return ")
        print("-"*save_load.divider_size)


solou_convo_d = SolouConvoD("""\
All of the city gates throughout the entire Kingdom are currently closed, 
King's orders, in order to keep out the monsters. This isn't a problem for me,
because I have written approval from the King, but you've got nothing. They 
won't let you through. Luckily, I've got this handy tool that can help us out 
here. It's called a "Fast Travel Atlas", and it can help us get around. They're
banned throughout the Kingdom due to their use in a string of murders a few 
years ago, but I hid one away just in case. If we're discreet about it, we 
won't have to worry about getting caught. This is just a basic model of the 
Atlas, it only allows teleporting through this province, Overshire. We'll have 
to acquire more pages to travel to other provinces. Let's get going.""", "solou_c4", False)


class SolouConvoE(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


solou_convo_e = SolouConvoE("""\
Aghhh, we wouldn't have gotten involved with any of this if you'd just told me
you weren't the mayor sooner! That letter literally began with "Dear Mayors of 
Overshire" you should have known right then and there that the letter wasn't 
for you and then spoken up about it!""", "solou_c5", False)


# -- Name: Joseph -- Town: Overshire City
class JosephConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


joseph_convo_a = JosephConvoA("""\
Greetings, young adventurer. Welcome to Overshire.""", "joseph_c1", True)


class JosephConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        set_active(joseph_convo_b, False)
        solou_quest_a.completion()


joseph_convo_b = JosephConvoB("""\
Ah, Solou! Long time no see! I see you've taken up adventuring.
It must be nice to finally put that spellbook of yours to use!
Oh, what's this? A letter for me? Well, I'll be sure to read this
later. Thank you for delivering this to me!""", "joseph_c2", False)


class JosephConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


joseph_convo_c = JosephConvoC("""\
Go visit my friend Azura in Parceon. She knows more about this than
I do. Parceon is located at 24\u00b0N, 28\u00b0E in case you forgot.""", "joseph_c3", False)


class JosephQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        set_active(joseph_convo_a, False)
        set_active(joseph_convo_c, True)


joseph_quest_a = JosephQuestA("To Parceon! [MAIN QUEST]", "Joseph", """\
Ah, Solou! Long time no see! I see you've taken up adventuring.
It must be nice to finally put that spellbook of yours to use!
*Solou and Joseph chat for a while. As mayor of Overshire, Joseph
is already well aware of Celeste being kidnapped.* Ah, so you adventurers
are questing to save his daughter? Well, I happen to know of a person
whose information would prove invaluable to you. Her name is Azura, and
she is the head of the Sorcerer's guild. She has been studying tomes and
has supposedly come up with a possible solution. She lives in a town
called Parceon, located at 24\u00b0N, 28\u00b0E.""",
                              "Thank you, good luck with your quest.", [75, 75], "joseph_q1", False)


# -- Name: Orius -- Town: Valice

# -- Name: Azura -- Town: Parceon
class AzuraConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


azura_convo_a = AzuraConvoA("""\
Hello, I'm Azura, leader of this town and head of the Sorcerer's Guild.
I'm quite busy right now, so please come back later if you wish to speak
to me.""", "azura_c1", True)


class AzuraConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        print('You write down the coordinates of Ambercreek.')
        main.s_input("\nPress enter/return ")

        set_active(azura_convo_b, False)
        set_active(azura_convo_c, True)


azura_convo_b = AzuraConvoB("""\
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
village right outside the exit of Barrier Cave. Good luck.""", "azura_c2", False)


class AzuraConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


azura_convo_c = AzuraConvoC("""\
My father, Raidon, lives in the town of Ambercreek at -7\u00b0S, -51\u00b0W. Good luck!""", "azura_c3", False)


# -- Name: Raidon -- Town: Ambercreek
class RaidonConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


raidon_convo_a = RaidonConvoA("""\
""", "raidon_c1", True)


# ---------------------------------------------------------------------------- #
# SIDE-STORY ARCS

# -- Graveyard Story-arc:
# --- Name: Stewson -- Town: Overshire
class StewsonConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_a = Conversation("""\
Our amazing Kingdom has 6 different regions: Tundra in the northwest, Swamp
in the southeast, Mountains in the northeast, and Desert in the southwest.
The Forest lies in the center, while the Shore surrounds them. There's a
small region somewhere around here that is the cause of much worry and panic
in this town: The Graveyard. Inside lies a dangerous apparition, feared by
all who have seen it. As the captain of the guard, my men and I have tried
and failed countless times to defeat that wretched ghost!""", "stewson_c1", True)


class StewsonQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        units.menacing_phantom.active = True
        set_active(stewson_convo_a, False)
        set_active(stewson_convo_b, True)

    def upon_completing(self):
        set_active(stewson_convo_c, True)
        set_active(rivesh_convo_b, False)
        set_active(rivesh_quest_a, True)

        print('-' * save_load.divider_size)
        print('You now have experience defeating ghosts!')
        main.s_input("\nPress enter/return ")


stewson_quest_a = StewsonQuestA('The Shadowy Spirit', 'Stewson', """\
I wish someone would do something about this terrible ghost... Hey! You're a
strong adventurer, perhaps you could defeat this phantom? It's at position.
8\u00b0N, -12\u00b0W.""", "Oh, thank you for being so courageous! Good luck defeating the ghost!",
                                [50, 75], "stewson_q1", True)


class StewsonConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_b = StewsonConvoB("""\
Please save us from this monstrous wraith!""", "stewson_c2", False)


class StewsonConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_c = StewsonConvoC("""\
You... you actually defeated it?! Thank you ever so much! Finally my men and
I can rest, and the town is safe! Take this, it is the least our town can
do for your bravery.""", "stewson_c3", False)


class StewsonConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stewson_convo_d = Conversation("""\
Thank you again for your help, adventurer!""", "stewson_c4", False)


# --- Name: Seriph -- Town: Fort Sigil
class SeriphConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


seriph_convo_a = SeriphConvoA("""\
...You actually came to this town? And of your own free will, too?! You are
truly a fool, although I suppose your bravery is admirable.""", "seriph_c1", True)


class SeriphConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


seriph_convo_b = SeriphConvoB("""\
What?! You're going to try to kill the evil spirit? You're truly stupider
than I thought. I wish you good luck nonetheless.""", "seriph_c2", False)


class SeriphConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


seriph_convo_c = SeriphConvoC("""\
Wuh... you killed it? Thats impossible, that wretched spectre has been haunting
us for decades... But I suppose it must be true, I can't feel its presence anymore.
Thank you hero, we are forever in your debt.""", "seriph_c3", False)


# --- Name: Rivesh -- Town: Fort Sigil
class RiveshConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_a = RiveshConvoA("""\
Welcome, brave adventurer. I'm sure that you've been informed of the
problems around here, so I'd recommend... Oh, what's that? You haven't?
Well in that case, let me tell you. A long time ago, a number of foolish
adventurers, searching for fame and glory, stumbled upon this fort.
Inside, they found a terrifying ghost, which they oh-so-cunningly
defeated -- or so they thought! No, instead the ghost had grown tired
of the pointless battle, and decided to hide in the shadows of the unsuspecting
"heroes". When they least expected it, the ghost possessed them! As
punishment for their foolishness, the evil spirit now forcefully takes a
victim from this town every 10 days and forbids its inhabitants from leaving!""", "rivesh_c1", True)


class RiveshConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_b = RiveshConvoB("""\
Hey... I don't suppose that you have any experience with fighting ghosts,
do you? No? Ok then. If you find someone who has defeated a very menacing
phantom before, please request that they come help us!""", "rivesh_c2", True)


class RiveshConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_c = RiveshConvoC("""\
Help us, young adventurer! You are the only one who can save us from this
terrible spirit!""", "rivesh_c3", False)


class RiveshConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_d = RiveshConvoD("""\
Y-you defeated the evil spirit? Praise Guido's beard! We are free of this
curse! You are forever in our gratitude, young hero!""", "rivesh_c4", False)


class RiveshConvoE(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


rivesh_convo_e = RiveshConvoE("""\
Thanks again, hero! We are forever indebted to you!""", "rivesh_c5", False)


class RiveshQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        units.cursed_spectre.active = True
        set_active(rivesh_convo_a, False)
        set_active(rivesh_convo_b, False)
        set_active(rivesh_convo_c, True)
        set_active(seriph_convo_a, False)
        set_active(seriph_convo_b, True)

    def upon_completing(self):
        set_active(rivesh_convo_d, True)
        set_active(seriph_convo_b, False)
        set_active(seriph_convo_c, True)


rivesh_quest_a = RiveshQuestA("The Curse of Fort Sigil", "Rivesh", """\
Hey... I don't suppose that you have any experience with fighting ghosts,
do you? Wait, what's that? You defeated the Phantom that was haunting the
Overshire Graveyard!? Well in that case, we may just have a chance!
Please help us, oh please!""", "I knew His Divinity would send someone to save us! Thank you hero!",
                              [200, 200], "rivesh_q1", False)


# ---------------------------------------------------------------------------- #
# SIDEQUESTS

# --ALFRED OF NEARTON--
class AlfredConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_a = AlfredConvoA("""\
It is rumored that a mighty jelly-creature lives south of this very town. 
Supposedly he's been devourering wild animals in the forest at a terrifying
rate, which is causing a lot of trouble for local hunters! And we're worried
that if he gets bored of his food in the forest that he'll come for us!
Unfortunately, the local militia is busy dealing with something else, so we
can't count on them to stop it. I'd be careful around there if I were you.""", "alfred_c1", True)


class AlfredQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        units.master_slime.active = True
        set_active(alfred_convo_a, False)
        set_active(alfred_convo_b, True)

    def upon_completing(self):
        set_active(alfred_convo_c, False)
        set_active(alfred_convo_d, True)


alfred_quest_a = AlfredQuestA('A Slimy Specimen', 'Alfred', """\
...Actually, now that I think about it, do you think you could possibly
dispose of this vile creature? It's located just south of here.""",
                              "Great, I'm glad we'll finally be free of this monster!", [30, 50], "alfred_q1", True)


class AlfredConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_b = AlfredConvoB("""\
Come back here when you defeat the evil Master Slime. Good luck!""", "alfred_c2", False)


class AlfredConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_c = AlfredConvoC("""\
You defeated the evil Master Slime?! Amazing! Now we can sleep easy at night
knowing our animals are safe. Take this, adventurer, you've earned it.""", "alfred_c3", False)


class AlfredConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alfred_convo_d = AlfredConvoD("""\
Greetings, Hero! Good luck on your adventures!""", "alfred_c4", False)


# -- Name: Kyle -- Town: Tripton
class KyleConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


kyle_convo_a = KyleConvoA("""\
Greeting, traveller. I am Kyle, Tripton's Village Elder. You aren't from
Fallville, right? Good. Those stupid Fallvillians need to get away from our
land! It's they're fault they made a town that was so easy to miss! I don't
care if we have to go to war with those dingbats, I'm not leaving this spot!""", "kyle_c1", True)


class KyleConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


kyle_convo_b = KyleConvoB("""\
Adventurer, we have heard reports that a mighty beast is in our land!
None of our men are willing to risk their lives to stop it. We are doomed.""", "kyle_c2", False)


class KyleConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        global alden_quest_a

        set_active(kyle_convo_c, False)
        set_active(kyle_convo_d, True)

        if krystin_convo_d.active:
            alden_quest_a.finished = True
            set_active(alden_convo_b, False)


kyle_convo_c = KyleConvoC("""\
The mighty monster has fallen? Thank god! What's this you say? The Fallvillians
defeated it? I supposed we owe them our lives. Perhaps we should think about
negotiating peace...""", "kyle_c3", False)


class KyleConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


kyle_convo_d = KyleConvoD("Welcome, adventurer, to the town of Tripton!", "kyle_c4", False)


# -- Name: Krystin -- Town: Fallville
class KrystinConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


krystin_convo_a = KrystinConvoA("""\
Hello, I am the Village Elder of Fallville. We don't take kindly to Triptonians
around here, so tell us if you see any. What I don't understand is that the
silly Triptonians blame us for their poor eyesight. It's all their fault, and
they know it!""", "krystin_c1", True)


class KrystinConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


krystin_convo_b = KrystinConvoB("""\
AHHH! Help! There's a m-m-monster out there! Someone go kill it! AHHH!""", "krystin_c2", False)


class KrystinConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        global alden_quest_a

        set_active(krystin_convo_c, False)
        set_active(krystin_convo_d, True)

        if kyle_convo_d.active:
            alden_quest_a.finished = True
            set_active(alden_convo_b, False)


krystin_convo_c = KrystinConvoC("""\
What, the monster is dead? Thank goodness! Oh, so the Triptonians killed it?",
Well then... I guess that we owe them our gratitude. Perhaps we should think",
about negotiating peace...""", "krystin_c3", False)


class KrystinConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


krystin_convo_d = KrystinConvoD("""\
Greetings, hero! Welcome to Fallville.""", "krystin_c4", False)


# -- Name: Frederick -- Town: Fallville
class FrederickConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


frederick_convo_a = FrederickConvoA("""\
I hear that there is a wise sage that has taken up residence in a small
cottage southwest of this town. I would go and talk to him, but monsters
have been roaming around the outskirts of town lately and it just isn't safe
to travel anymore.""", "frederick_c1", True)


class FrederickConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


frederick_convo_b = FrederickConvoB("""\
There's a monster outside of town, and a big one at that! It looks like some
sort of spider... I hope to god our militia can handle it!""", "frederick_c2", False)


class FrederickConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


frederick_convo_c = FrederickConvoC("""\
Thank heavens, the mighty beast has fallen.""", "frederick_c3", False)


# -- Name: Alden -- Town: Small Cottage
class AldenQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        units.terr_tarant.active = True
        set_active(alden_convo_a, True)
        set_active(kyle_convo_a, False)
        set_active(kyle_convo_b, True)
        set_active(krystin_convo_a, False)
        set_active(krystin_convo_b, True)
        set_active(frederick_convo_a, False)
        set_active(frederick_convo_b, True)

    def upon_completing(self):
        set_active(alden_convo_c, True)


alden_quest_a = AldenQuestA("Stop the Strife", 'Alden', """\
Greetings, adventurer. I'm sure that you have heard of the conflict going on
between the villages of Fallville and Tripton. I have an idea on how to settle
this foul feud, but alas, I cannot perform it due to my old and fragile
state. You, however, appear to be a very young and capable adventurer. Do you
perhaps think that you could help me? I need you to go defend the towns of
Fallville and Tripton from a terrible monster. This is a monster I will be
summoning, of course. Afterwards, spread word in the two towns that an
anonymous warrior from the opposite town defeated it! This should bring an end
to their constant bickering. I will summon the monster at coordinates
-23\u00b0S, -11\u00b0W.""", "Thank you. Hopefully this feud will finally come to an end.",
                            [175, 200], "alden_q1", True)


class AldenConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alden_convo_a = AldenConvoA("""\
I've summoned the mighty beast. Now hurry up and dispose of it before it causes any damage.""", "alden_c1", False)


class AldenConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alden_convo_b = AldenConvoB("""\
You've defeated him? Good, now go talk to the village elders! Good luck!""", "alden_c2", False)


class AldenConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


alden_convo_c = AldenConvoC("""\
Thanks again, hero. You've saved those towns a lot of trouble.""", "alden_c3", False)


# -- Name: Polmor -- Town: Whistumn
class PolmorConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


polmor_convo_a = PolmorConvoA("""\
Our poor daughter! Serena and I have been working on a cure, but
we cannot find anyone stup-I mean brave enough to gather the
resources we need. All is lost if we cannot get the ingredients.""", "polmor_c1", True)


class PolmorConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
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

            polmor_quest_a.finished = True
            print('-'*save_load.divider_size)


polmor_convo_b = PolmorConvoB("""\
Please, return once you have obtained one Monster Fang, one Serpent Scale
and one Fairy Dust. You must save our daughter!""", "polmor_c2", False)


class PolmorConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


polmor_convo_c = PolmorConvoC("""\
...Wait, what?! You obtained the items we needed? You are our savior! We owe
our lives to you, you are truly a hero! *He walks over to his wife, and the
two begin mixing the ingredients to make the cure for Hatchnuk's Blight*
At last, we have the cure! Let us not waste time. *The two administer the
medicine to their daughter, and she immediately begins feeling better.* Oh joy
of joys! Our daughter is healed! How can we ever repay you, oh noble adventurer
and vanquisher of the Blight? Here, take this. It is the absolute least that we
can do.""", "polmor_c3", False)


class PolmorQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        set_active(serena_convo_a, False)
        set_active(serena_convo_b, True)
        set_active(polmor_convo_a, False)
        set_active(polmor_convo_b, True)

    def upon_completing(self):
        set_active(serena_convo_c, True)
        set_active(serena_convo_b, False)
        set_active(polmor_convo_b, False)

        print('-'*save_load.divider_size)
        print('Serena and Polmor will now heal you for free if you visit them!')


polmor_quest_a = Quest("Fight Against the Blight", "Polmor", """\
Wait a minute... I am so stupid! According to my calculations, you are the
legendary adventurer of Nearton! Yes, it must be you , adventurer, help our
daughter! The only way to get the ingredients is to defeat several monsters
and collect their remains. Specifically, I need one Fairy Dust, one Serpent
Scale, and one Monster Fang. You're the only one who can save her!""",
                       "Thank you so much! I'm glad people like you exist!", [450, 450], "polmor_q1", True)


# -- Name: Serena -- Town: Whistumn
class SerenaConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


serena_convo_a = SerenaConvoA("""\
Oh, woe is me! My daughter has fallen ill from a terrible disease! They call
it "Hatchnuk's Blight", and it is very deadly. Oh, what am I to do?
*sobs uncontrollably*""", "serena_c1", True)


class SerenaConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


serena_convo_b = SerenaConvoB("""\
You are a good man, trying to help our daughter! Good luck on your quest!""", "serena_c2", False)


class SerenaConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        units.heal_pcus(1)
        print('-'*save_load.divider_size)
        print('Polmor and Serena get to work on healing your party...')
        main.smart_sleep(2)
        print('Your party has been fully healed.')
        main.s_input("\nPress enter/return ")


serena_convo_c = SerenaConvoC("""\
You are our heroes! Here, allow us to treat your wounds.""", "serena_c3", False)


# -- Name: Matthew -- Town: Lantonum
class MatthewConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        set_active(matthew_convo_a, False)


matthew_convo_a = MatthewConvoA("""\
*You try to talk to the man in the bar, but he is too busy listening to
music on his 'iSound' to notice you. Suddenly, a peasant walks up behind
him, screams 'Witch!', grabs the iSound, and smashes it to bits on the floor.
He then proceeds to set it on fire and bury the ashes in the dirt behind the
bar.*""", "matt_c1", True)


class MatthewQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        set_active(matthew_convo_a, False)
        set_active(matthew_convo_b, True)

    def upon_completing(self):
        set_active(matthew_convo_e, True)


matthew_quest_a = MatthewQuestA('iSounds Good', "Matthew", """\
Dangit, that happens all the time! Those idiots keep calling my iSound MP3
player a witch - this is the fifth one I've gone through this week! The
company that makes them only sells them in Elysium, as nobody in Harconia
could tell an MP3 player from a brick if their life depended on it. Hey, I'll
tell you want: If you go to Cesura, the train town near the border of Harconia
and Elysium, and buy me a new iSound, I will reward you greatly. Remember:
iSounds have watermelons on the back. If you get one with a grapefruit, then
you're just paying a lot of money for a cheap knockoff brand. And definitely
stay away from papaya phones. Can you do that for me?""",
                                "Okay thanks man. I really need this iSound.", [1250, 1250], "matt_q1", True)


class MatthewConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        self.active = False
        items.remove_item("musicbox")


matthew_convo_b = MatthewConvoB("""\
Hello, friend! Have you gotten me a new iSound yet?""", "matt_c2", False)


class MatthewConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        self.active = False


matthew_convo_c = MatthewConvoC("""\
No? That's okay. Just pick one up for me when you get the chance. You can
purchase them at the town of Cesura, located at 123\u00b0N, 58\u00b0E.""", "matt_c3", False)


class MatthewConvoD(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def after_talking(self):
        global matthew_quest_a

        matthew_quest_a.finished = True
        set_active(matthew_convo_d, False)


matthew_convo_d = MatthewConvoD("""\
You have? Wonderful! *He takes the iSound from your hand and pulls out 1250 GP*""", "matt_c4", False)


class MatthewConvoE(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


matthew_convo_e = MatthewConvoE("""\
*He looks quite depressed.*""", "matt_c5", False)


# -- Name: Pime -- Town: Sanguion
class PimeConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)

    def pime_c1_at(self):
        self.active = False
        set_active(pime_quest_a, True)


pime_convo_a = PimeConvoA("""\
Hello, traveller! You do not look familiar - quick, come inside, it's not been
safe to stay out here for the past few weeks. *Pime ushers you into a tavern
filled with people whom he seems to be quite friendly with. They likewise are
quite kind to you.* My name is Pime. I am the chief of this town, and the head
of Sanguion's militia. As I'm sure you know, me, and all the other people in
this inn, are vampires. Do not be alarmed! We only feast on wild animals and
the dead. As of late, a new group of vampire hunters named the 'Anti-blood Squad'. 
Not only do these terrorists have an extraordinarily uncreative name, but they've 
also been capturing our friends and family and are torturing, ransoming, and even 
killing them! We vampires are not harmful to society, and do not deserve this 
kind of treatment! Our loved ones are dying to those monsters, and we don't have 
anywhere near enough manpower to put a stop to it! What are we to do?!""", "pime_c1", True)


class PimeQuestA(Quest):
    def __init__(self, name, q_giver, dialogue, accept_msg, reward, conv_id, active):
        super().__init__(name, q_giver, dialogue, accept_msg, reward, conv_id, active)

    def upon_starting(self):
        set_active(pime_convo_a, False)
        set_active(pime_convo_b, True)
        # units.anti_blood_squad.active = True

    def upon_completing(self):
        set_active(pime_convo_c, True)


pime_quest_a = PimeQuestA("The Hated Hunter", "Pime", """\
Hey - you look like quite the seasoned adventurer. Maybe you could help
us! I hope this isn't too much to ask, but could you possibly defeat
these hunters? They're causing us so much pain, we need someone to get rid of 
him.""", "Thank you, hopefully these guys will leave us alone if you teach them a lesson.",
                          [1000, 1000], "pime_q1", True)


class PimeConvoB(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


pime_convo_b = PimeConvoB("""\
Please deal with those blasted vampire hunters! Their hideout
is located at -68\u00b0S, -93\u00b0W.""", "pime_c3", False)


class PimeConvoC(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


pime_convo_c = PimeConvoC("""\
Thank you every so much for ridding us of those vile terrorists! You are
forever in our gratitude!""", "pime_c4", False)


# ----------------------------------------------------------------------------#
# UNIMPORTANT CHARACTERS

# -- Name: Philliard -- Town: Nearton
class PhilliardConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


philliard_convo_a = PhilliardConvoA("""\
Hello, adventurer! Welcome to the Kingdom of Harconia!""", "philliard_c1", True)


# -- Name: Saar -- Town: Nearton
class SaarConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


saar_convo_a = SaarConvoA("""\
Have you heard that the King has ordered the indefinite closure of all the
city gates throughout the kingdom? You can't enter or leave any city or 
province without written approval from King Harconius himself. Says that i's
because of 'the monsters'. All the big merchants and bankers got written 
approval so easily but all of my requests have fallen on deaf ears it seems. 
My music needs to be heard by the masses!""", "saar_c1", True)


# -- Name: Wesley -- Town: Southford
class WesleyConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


wesley_convo_a = WesleyConvoA("""\
I'm glad the King finally ordered all the city gates closed! The monster
attacks were getting ridiculous. Back in the good days, a few years ago,
being ambushed by monsters was a once-in-a-lifetime thing. They usually
just kept to their camps or caves, preying on the wildlife. But I guess
that's just not how things are anymore, so closing the gates was the right
call.""", "wesley_c1", True)


# -- Name: Lazaro -- Town: Southford
class LazaroConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


lazaro_convo_a = LazaroConvoA("""\
Greetings, adventurer from Nearton! How do I know who you are, you ask? Well,
I am Lazaro, the Oracle of Southford! Let me give you some advice that will 
help keep you alive during battle: you aren't officially dead in battle until
the end of your turn! If an ally heals you before the turn ends, you can
recover from mortal damage, preventing you from dying. Very useful, it's saved
my friends' lives many times before.""", "lazaro_c1", True)


# -- Name: Sondalar -- Town: Overshire City
class SondalarConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


sondalar_convo_a = SondalarConvoA("""\
Help me with this moral dilemma I'm having. The King recently closed all the
city gates in an effort to reduce the number of monster attacks. Anyone who
wants to enter or leave a city or province needs written approval from the
King. Well, I managed to get approval pretty easily, but my competitors didn't
seem to fare as well. We've gone from dozens of successful merchants in
Overshire to only a handful. My trade business has never been stronger,
but in turn these other merchants have lost their livelihood. What should I do?""", "sondalar_c1", True)


# -- Name: Harthos -- Town: Overshire City
class HarthosConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


harthos_convo_a = HarthosConvoA("""\
Welcome to Overshire, stranger! Our Kingdom's capital is pretty big, so try
not to get lost, haha!""", "harthos_c1", True)


# -- Name: Sakura -- Town: Principalia
class SakuraConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


sakura_convo_a = SakuraConvoA("""\
HALT! State your business! Ah, you want to see the King, do you?
Well, the King is currently in Overshire. Sakura cannot imagine
that he is accepting visitors right now, though. Unless you have
something really important to tell him, such as how to save his
daughter, Sakura doesn't see you talking to him in your future.
Now get out of here, Sakura is busy!""", "sakura_c1", True)


# -- Name: Jeffery -- Town: Principalia
class JefferyConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


jeffery_convo_a = JefferyConvoA("""\
Sometimes I wish the Great Fog Wall didn't exist. Y'know, that dreaded barrier
surrounding the entire Kingdom? Absolutely nothing can get through the fog. 
Light can't travel through it, sound can't travel through it, and magic just 
fizzles whenever you try to manipulate it. Even the sturdiest  ships money can 
buy can't survive the dangerous waters. Nobody knows where the fog came from. 
I've spent my entire life traveling throughout the Kingdom, experiencing all
that it has to offer. I wonder what, if anything lies out there? Just imagine 
what strange and wonderful people, foods, and nature a far away land could hold!""", "jeffery_c1", True)


# -- Name: Ethos -- Town: Valice
class EthosConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


# TODO
ethos_convo_a = EthosConvoA("""\
Hey, have you heard the news? All city gates are closed, effective immediately.
Sounds like a great thing, guaranteed protection from all those horrible
monsters and such. Just because""", "ethos_c1", True)


# -- Name: Typhen -- Town: Valice
class TyphenConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


typhen_convo_a = TyphenConvoA("""\
I've heard that when you use healing spells, you restore additional HP based
on your wisdom. And paladins supposedly get an even larger restoration bonus
when they heal!""", "typhen_c1", True)


# -- Name: Fly -- Town: New Ekanmar
class FlyConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


fly_convo_a = FlyConvoA("""\
Hello, adventurer! My name is Fly, Duke of Celemia. I'm quite busy right now,
please come back later if you wish to speak to me.""", "fly_c1", True)


# -- Name: Stravi -- Town: New Ekanmar
class StraviConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


stravi_convo_a = StraviConvoA("""\
Greetings, young traveller. I am Stravi, Duchess of Celemia. My husband
and I are on important business relating to the recent kidnapping of King
Harconius II's daughter, Celeste. Please return in a few weeks if you wish
to speak to Fly and me. Oh, and whatever you do, do not under ANY
circumstances mention the word 'chandelier' to my husband. It makes him very
upset for some reason.""", "stravi_c1", True)


# -- Name: Caesar -- Town: New Ekanmar
class CaesarConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


caesar_convo_a = CaesarConvoA("""\
*Caesar, Fly's pet strawberry dragon, runs away and hides behind
his owner before you get a chance to converse with him.*""", "caesar_c1", True)


# -- Name: Strathius -- Town: Ravenstone
class StrathiusConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


strathius_convo_a = StrathiusConvoA("""\
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
Always keep a stash of items to cure these sicknesses man.""", "strathius_c1", True)


# -- Name: Sugulat -- Town: Ambercreek
class SugulatConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


sugulat_convo_a = SugulatConvoA("""\
Greetings! My name is Sugulat, Duke of Chin'tor and legendary digger of
holes. Y'know, you look like a nice guy. I'm going to tell you a little
secret: If you buy a shovel from the general store, you can dig up valuable
gems in certain places! They're all over the place, there's usually at least
one in every area you visit.""", "sugalat_c1", True)


# -- Name: Morrison -- Town: Cesura
class MorrisonConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


morrison_convo_a = MorrisonConvoA("""\
Hello, sir! I'm Morrison, the head engineer of Cesura! I'm a native Elysian,
and have only been here for around a year, so I'm pretty new to this place!
Most of my time is spent making sure that these trains run properly. By the
way, do you know what \"witch\" means? Hythic isn't my first language, and the
townsfolk keep calling me that when I turn on the trains. Witch is a good
thing, right?""", "morrison_c1", True)


# -- Name: Ariver -- Town: Sanguion
class AriverConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


ariver_convo_a = AriverConvoA("""\
*Ariver mistakes you for a vampire hunter and runs quickly into his house,
locking the doors, shutting the windows, and closing the blinds. As you begin
walking away, scratching your head in confusion, you see him look out the
window and walk back outside, having determined you are not a threat at the
moment.*""", "ariver_c1", True)


# -- Name: Fitzgerald -- Town: Valenfall
class FitzgeraldConvoA(Conversation):
    def __init__(self, dialogue, conv_id, active):
        super().__init__(dialogue, conv_id, active)


fitz_convo_a = FitzgeraldConvoA("""\
*hic* Pay no attention to the behind behind the curtain! *The man appears to
be quite drunk. You also notice a distinct lack of any curtain nearby.*
*hic* Drop that, you thief! Give me back my penny-loafers! *You slowly walk
away from the raving drunk.*""", "fitz_c1", True)


all_dialogue = {
    solou_convo_a.conv_id: solou_convo_a,
    solou_quest_a.conv_id: solou_quest_a,
    solou_convo_b.conv_id: solou_convo_b,
    solou_convo_c.conv_id: solou_convo_c,
    solou_convo_d.conv_id: solou_convo_d,
    solou_convo_e.conv_id: solou_convo_e,

    rivesh_convo_a.conv_id: rivesh_convo_a,
    rivesh_convo_b.conv_id: rivesh_convo_b,
    rivesh_convo_c.conv_id: rivesh_convo_c,
    rivesh_convo_d.conv_id: rivesh_convo_d,
    rivesh_convo_e.conv_id: rivesh_convo_e,
    rivesh_quest_a.conv_id: rivesh_quest_a,

    alfred_convo_a.conv_id: alfred_convo_a,
    alfred_convo_b.conv_id: alfred_convo_b,
    alfred_convo_c.conv_id: alfred_convo_c,
    alfred_convo_d.conv_id: alfred_convo_d,
    alfred_quest_a.conv_id: alfred_quest_a,

    stewson_convo_a.conv_id: stewson_convo_a,
    stewson_convo_b.conv_id: stewson_convo_b,
    stewson_convo_c.conv_id: stewson_convo_c,
    stewson_convo_d.conv_id: stewson_convo_d,
    stewson_quest_a.conv_id: stewson_quest_a,

    kyle_convo_a.conv_id: kyle_convo_a,
    kyle_convo_b.conv_id: kyle_convo_b,
    kyle_convo_c.conv_id: kyle_convo_c,
    kyle_convo_d.conv_id: kyle_convo_d,

    krystin_convo_a.conv_id: krystin_convo_a,
    krystin_convo_b.conv_id: krystin_convo_b,
    krystin_convo_c.conv_id: krystin_convo_c,
    krystin_convo_d.conv_id: krystin_convo_d,

    frederick_convo_a.conv_id: frederick_convo_a,
    frederick_convo_b.conv_id: frederick_convo_b,
    frederick_convo_c.conv_id: frederick_convo_c,

    joseph_convo_a.conv_id: joseph_convo_a,
    joseph_convo_b.conv_id: joseph_convo_b,
    joseph_convo_c.conv_id: joseph_convo_c,
    joseph_quest_a.conv_id: joseph_quest_a,

    alden_quest_a.conv_id: alden_quest_a,
    alden_convo_a.conv_id: alden_convo_a,
    alden_convo_b.conv_id: alden_convo_b,
    alden_convo_c.conv_id: alden_convo_c,

    azura_convo_a.conv_id: azura_convo_a,
    azura_convo_b.conv_id: azura_convo_b,
    azura_convo_c.conv_id: azura_convo_c,

    polmor_convo_a.conv_id: polmor_convo_a,
    polmor_convo_b.conv_id: polmor_convo_b,
    polmor_convo_c.conv_id: polmor_convo_c,
    polmor_quest_a.conv_id: polmor_quest_a,

    serena_convo_a.conv_id: serena_convo_a,
    serena_convo_b.conv_id: serena_convo_b,
    serena_convo_c.conv_id: serena_convo_c,

    matthew_convo_a.conv_id: matthew_convo_a,
    matthew_quest_a.conv_id: matthew_quest_a,
    matthew_convo_b.conv_id: matthew_convo_b,
    matthew_convo_c.conv_id: matthew_convo_c,
    matthew_convo_d.conv_id: matthew_convo_d,
    matthew_convo_e.conv_id: matthew_convo_e,

    pime_convo_a.conv_id: pime_convo_a,
    pime_quest_a.conv_id: pime_quest_a,
    pime_convo_b.conv_id: pime_convo_b,
    pime_convo_c.conv_id: pime_convo_c,

    lazaro_convo_a.conv_id: lazaro_convo_a,

    philliard_convo_a.conv_id: philliard_convo_a,

    fly_convo_a.conv_id: fly_convo_a,

    stravi_convo_a.conv_id: stravi_convo_a,

    sakura_convo_a.conv_id: sakura_convo_a,

    sugulat_convo_a.conv_id: sugulat_convo_a,

    raidon_convo_a.conv_id: raidon_convo_a,

    caesar_convo_a.conv_id: caesar_convo_a,

    wesley_convo_a.conv_id: wesley_convo_a,

    seriph_convo_a.conv_id: seriph_convo_a,

    strathius_convo_a.conv_id: strathius_convo_a,

    ariver_convo_a.conv_id: ariver_convo_a,

    fitz_convo_a.conv_id: fitz_convo_a,

    harthos_convo_a.conv_id: harthos_convo_a,

    typhen_convo_a.conv_id: typhen_convo_a,

    sondalar_convo_a.conv_id: sondalar_convo_a,

    morrison_convo_a.conv_id: morrison_convo_a,

    ethos_convo_a.conv_id: ethos_convo_a,

    jeffery_convo_a.conv_id: jeffery_convo_a,

    saar_convo_a.conv_id: saar_convo_a,

    seriph_convo_b.conv_id: seriph_convo_b,

    seriph_convo_c.conv_id: seriph_convo_c
}


def set_active(conv_obj, new_state):
    global all_dialogue

    for key in all_dialogue:
        if all_dialogue[key].conv_id == conv_obj.conv_id:
            all_dialogue[key].active = new_state

            return

    raise Exception(f"{conv_obj} is not a valid Conversation!")


def serialize_dialogue(path):
    json_dialogue = {}

    for c in [all_dialogue[key] for key in all_dialogue]:
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
        for c in [all_dialogue[key] for key in all_dialogue]:
            if key == c.conv_id:
                if isinstance(c, Quest):
                    all_dialogue[key].active, all_dialogue[key].started, all_dialogue[key].finished = \
                        j_log[key][0], j_log[key][1], j_log[key][2]
                else:
                    all_dialogue[key].active = j_log[key][0]


for item1 in copy.copy(globals()):
    if isinstance(globals()[item1], Conversation) and globals()[item1] not in [all_dialogue[x] for x in all_dialogue]:
        print(f"{item1} not in all_dialogue!")
