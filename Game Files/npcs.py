# This file is part of PythoniusRPG.
#
# PythoniusRPG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PythoniusRPG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PythoniusRPG.  If not, see <http://www.gnu.org/licenses/>.

import sys
import json
import copy

import bosses
import inv_system
import pets
import items

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

"""
Info for reading this file:

This file contains all data regarding the logic behind quests, NPCs, and conversations.
Every NPC has at least one conversation, and most (but not all) have at least one quest.
Because of the way that the game works, the person you visit to finish the quest is ALWAYS
the same person who gave it to you in the first place (this is subject to change if I
can find a way around this without breaking the already existing quests).

The quests are divided into three categories: Main Questline, Side-story arcs, and side quests.
The main questline consists of all quests required to finish the game (when a way to do so is
implemented) and it generally all follows the same story-arc. Side-story arcs include
side-storyline that spans multiple quests, such as the Graveyard storyline. Side quests are
single-quest story arcs that have almost nothing to do with the main plot.

Naming style:

If an object name ends with "_ucX", where X is an integer, then it handles what happens
    when a quest is completed.

If an object name ends with "_usX", where X is an integer, then it handles what happens
    when a quest is started.

"""


class NPC:
    def __init__(self, name, conversations):
        self.name = name
        self.conversations = conversations

    def speak(self):
        # Print the NPC's dialogue to the player
        dialogue = []
        for w in self.conversations:
            if w.active and not w.repeat:

                try:
                    if not w.started:  # Quests
                        dialogue.append(w.sentences)
                    elif w.started and w.finished and w.active:
                        dialogue = [w.end_dialogue]
                        break

                except AttributeError:  # Non-quests
                    dialogue.append(w.sentences)

        else:
            for x in self.conversations:

                if x.active and x.repeat:
                    dialogue.append(x.sentences)

                    break

        for y in dialogue[:]:

            # Dialogue is being modified, so we're iterating over a copy of it.
            padding = len(max(y, key=len))

            for z in y:
                input(''.join([self.name.title(), ': ', z, ' '*(padding - len(z)), ' | [ENTER] ']))

            dialogue.remove(y)
            print('-'*25) if dialogue else ''

            for obj in self.conversations:

                if isinstance(obj, Quest) and obj.end_dialogue == y:
                    y = obj
                elif obj.sentences == y:
                    y = obj

            if isinstance(y, Quest) and not y.started:
                y.give_quest()
            elif isinstance(y, Quest) and y.finished:
                y.completion()

            try:
                y.after_talking()
            except AttributeError:
                pass


class Conversation:
    def __init__(self, sentences, repeat=False, active=False):
        self.sentences = sentences
        self.repeat = repeat  # True if the conversation is generic and unimportant
        self.active = active

    def __str__(self):
        # Returns a unique string based on the content of the conversation.
        # This is used as a dictionary key to save information about conversations.
        try:
            return ' | '.join([x[0:12] for x in self.sentences])
        except IndexError:
            return ' | '.join([x[::-1] for x in self.sentences])


class Quest(Conversation):
    def __init__(self, sentences, name, desc, q_giver, reward, end_dialogue,
                 req_lvl=1, started=False, finished=False, repeat=False, active=False):
        Conversation.__init__(self, sentences, repeat, active)
        self.name = name  # The name of the quest
        self.desc = desc  # A brief summary of the goal of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.req_lvl = req_lvl  # The level that you must be at to begin the quest
        self.started = started  # is True if the quest has been started, false otherwise
        self.finished = finished  # is True if the quest is complete, false otherwise
        self.end_dialogue = end_dialogue  # What is printed when the quest is over

    def __str__(self):
        try:
            return ': '.join([self.q_giver, ' | '.join([x[0:6] for x in self.sentences])])
        except IndexError:
            return ': '.join([self.q_giver, ' | '.join([x[::-1] for x in self.sentences])])

    def give_quest(self):
        print('-'*25)
        print(''.join([self.name, ': \n  ', '\n  '.join([x for x in self.desc])]))
        print('-'*25)

        if self.req_lvl > main.player.lvl:
            print('You are not a high enough level to begin the quest "{0}".\
(Must be level {1})'.format(self.name, self.req_lvl))

        print('{0} is offering you the quest, "{1}".'.format(self.q_giver, self.name))

        while True:
            accept = input('Do you accept this quest? | Yes or No: ')

            accept = accept.lower()

            if accept.startswith('y'):
                print('-'*25)
                print('{0}: "Terrific! Come see me when you are finished."'.format(self.q_giver))
                self.started = True
                self.upon_starting()

                return

            elif accept.startswith('n'):
                print('-'*25)
                print('{0}: "...Oh. Come back later if you change your mind."'.format(self.q_giver))

                return

    def completion(self):
        self.upon_completing()

        print("Quest Complete!")
        print("You've received {0} XP and {1} GP for completing this quest.".format(
            self.reward[0], self.reward[1]))
        input('Press Enter/Return')

        main.player.exp += self.reward[0]
        main.misc_vars['gp'] += self.reward[1]
        main.player.level_up()

        self.active = False

#----------------------------------------------------------------------------#
# MAIN/STORYLINE QUESTS & NPCS

# -- Name: Philliard -- Town: Nearton
philliard_phrase_1 = Conversation(["Hello, adventurer!",
                                   "Welcome to the Kingdom of Pythonia."], active=True)

philliard_phrase_2 = Conversation(["Greetings! Huh, what's this? You have a letter for me?",
                                   "Ah, it's from Joseph. Thank you, kind adventurer.",
                                   "I assume you are heading back to see Joseph. Please",
                                   "bring him this message. Best of luck, traveller!"])


def pp2_at():
    # Stands for "Philliard Phrase II -- After Talking"
    for item in inv_system.inventory['q_items']:
        if item.name == 'Message from Joseph':
            inv_system.inventory['q_items'].remove(item)
            break

    inv_system.inventory['q_items'].append(copy.copy(items.message_philliard))
    philliard_phrase_2.active = False
    philliard_phrase_1.active = True
    joseph_quest_1.finished = True


philliard_phrase_2.after_talking = pp2_at

philliard = NPC('Philliard', [philliard_phrase_1, philliard_phrase_2])

# -- Name: Joseph -- Town: Charsulville
joseph_phrase_1 = Conversation(['Greetings, young adventurer. Welcome to Charsulville.'
                                ], active=True)
joseph_phrase_2 = Conversation(['Report back to me when you have delivered that letter.'])

joseph_phrase_3 = Conversation(["I'd recommend that you give my friend Azura a visit at",
                                "Parceon. That town is located somewhere around \
24\u00b0N, 28\u00b0E",
                                "if I'm remembering correctly."
                                ])

joseph_quest_1 = Quest(["Wait a second... are you who I think you are? I've recieved",
                        'word that a traveller from Nearton was heading',
                        "this way. Yes, that MUST be you they're talking",
                        'about! Could you please do me a favor and take',
                        "this message to Philliard in Nearton? Nearton,",
                        "in case you've forgotton, is at 1\u00b0N, 0\u00b0E."],
                       'An Important Message',
                       ["Deliver a message (located in your Quest Items) to Philliard in Nearton,",
                        "located at 1\u00b0N, 0\u00b0E, and then return to Joseph in \
Charsulville."],
                       'Joseph', [15, 25],
                       ["You have delivered the message? Thank you ever so",
                        "much! You have no idea how much trouble you've saved me.",
                        "Hmm? What was the letter about, you ask? 'Twas very",
                        "important information from King Pythonius II himself! Now",
                        "that Philliard is in possession of the letter, I can tell",
                        "you its contents. If case you don't know, there is a neighboring",
                        "island-nation to the south of Pythonia called \"Thex\". Thex",
                        "is home to the stealthiest and most deadly assassins in all of ",
                        "Arcadia, a fact that has been the cause of much tension between",
                        "Pythonia and them. This unease has never really led to anything",
                        "until now. And unfortunately, they made the first move. Celeste,",
                        "King Pythonius's daughter, has been kidnapped and is being",
                        "held hostage on their island! This is terrible news, and",
                        "we are unable to do anything about it. Thex has placed a",
                        "magical barrier around their island, and there is no way",
                        "to break it. I've heard word about a possible solution.",
                        "Supposedly, the head of the Sorcerer's Guild in Parceon has",
                        "discovered something about an ancient prophecy related to this.",
                        "You might want to go give her a visit if you want any more",
                        "information. Parceon, if I recall correctly, is somewhere",
                        "around 24\u00b0N, 28\u00b0E. Good luck on your adventures!",
                        "Oh, and take this as a reward!"], active=True)


def jphqst_us1():
    # Stands for "Joseph Quest I - Upon Starting
    global philliard_phrase_1
    global philliard_phrase_2
    global joseph_phrase_1
    global joseph_phrase_2

    philliard_phrase_1.active = False
    philliard_phrase_2.active = True
    joseph_phrase_1.active = False
    joseph_phrase_2.active = True
    inv_system.inventory['q_items'].append(copy.copy(items.message_joseph))


def jphqst_uc1():
    # Stands for "Joseph Quest I - Upon Completing
    global joseph_phrase_1
    global joseph_phrase_2
    global azura_phrase_1
    global azura_phrase_2

    joseph_phrase_2.active = False
    joseph_phrase_3.active = True

    azura_phrase_1.active = False
    azura_phrase_2.active = True

    print('-'*25)
    print("You've recieved a Magic Compass from Joseph.")
    input('It has been added to the "Misc" section of your inventory. | Press enter/return ')
    input('You write down the coordinates of Parceon. | Press enter/return ')

    inv_system.inventory['misc'].append(items.magic_compass)
    towns.town8.new_location()


joseph_quest_1.upon_starting = jphqst_us1
joseph_quest_1.upon_completing = jphqst_uc1

joseph = NPC('Joseph', [joseph_phrase_1, joseph_quest_1, joseph_phrase_2, joseph_phrase_3])

# -- Name: Azura -- Town: Parceon
azura_phrase_1 = Conversation(["Hello, I'm Azura, leader of this town and head of the",
                               "Sorcerer's Guild. I'm quite busy right now, so please",
                               "come back later if you wish to speak to me."], active=True)

azura_phrase_2 = Conversation(["Hello, I'm Azura, leader of this town and head of the",
                               "Sorcerer's Guild. I'm quite busy right now, so please",
                               "come back later if you wish to speak to me... Oh, what's",
                               "that? Joseph of Charsulville sent you? Well in that case,",
                               "I suppose that I can take some time off from my duties to",
                               "speak to you. What is it that you need? ...I see. I know of",
                               "a way to rescue King Pythonius II's daughter, as Joseph probably",
                               "told you. It's quite dangerous, however - none of the King's",
                               "men have survived the journey. Looking at you, however, I",
                               "see much potential. There is one problem, however: Our Kingdom",
                               "has been infiltrated by the Thexus. I have no way of verifying",
                               "whether or not you are one of them.",
                               "Actually, now that I think about it, perhaps there IS a way...",
                               "How about this: My father, Raidon, has been having some",
                               "problems lately. If you go help him out, then you will have",
                               "earned my trust. He lives in the town of Ambercreek, a village",
                               "right along the border of the Forest and Mountain regions.",
                               "The town is located at -7\u00b0S, -51\u00b0W. Good luck."])


def ap1_at():
    global azura_phrase_2
    global azura_phrase_3

    input('You write down the coordinates of Ambercreek. | Press enter/return ')
    azura_phrase_2.active = False
    azura_phrase_3.active = True


azura_phrase_2.after_talking = ap1_at

azura_phrase_3 = Conversation(["My father, Raidon, lives in the town if Ambercreek at",
                               "-7\u00b0S, -51\u00b0W. Good luck!"])

azura = NPC('Azura', [azura_phrase_1, azura_phrase_2, azura_phrase_3])

# -- Name: Raidon -- Town: Ambercreek
raidon_phrase_1 = Conversation(["FILLER TEXT"], active=True)

raidon = NPC('Raidon', [raidon_phrase_1])

#----------------------------------------------------------------------------#
# STORY-STORY ARCS

# -- Graveyard Story-arc:
# --- Name: Stewson -- Town: Overshire
stewson_phrase_1 = Conversation(["Our amazing Kingdom has 6 different regions:",
                                 "Tundra in the northwest, Swamp in the southeast,",
                                 "Mountains in the northeast, and Desert in the southwest.",
                                 "The Forest lies in the center, while the Shore surrounds them.",
                                 "There's a small region somewhere around here that is the",
                                 "cause of much worry and panic in this town: The Graveyard.",
                                 "Inside lies a dangerous aparrition, feared by all who have \
seen it.",
                                 ], active=True)

stewson_phrase_2 = Conversation(["Please save us from this monsterous wraith!"])

stewson_phrase_3 = Conversation(["Thank you again for your help, adventurer!"])

stewson_quest_1 = Quest(["I wish someone would do something about this terrible",
                         "ghost... Hey! You're a strong adventurer, perhaps you",
                         "could defeat this phantom? It's at position 8\u00b0N, -12\u00b0W."],
                        'The Shadowy Spirit',
                        ["Defeat the feared Menacing Phantom at location",
                         "8\u00b0N, -12\u00b0W and then return to Stewson in Overshire."],
                        'Stewson', [50, 75],
                        ["You... you actually defeated it?! Thank you ever so much!",
                         "Take this, it is the least our town can do for your bravery."],
                        active=True)


def stwqst_us1():
    global stewson_phrase_1
    global stewson_phrase_2
    bosses.menac_phantom.active = True
    stewson_phrase_1.active = False
    stewson_phrase_2.active = True


def stwqst_uc1():
    global stewson_phrase_3
    global rivesh_phrase_2
    global rivesh_quest_1

    stewson_phrase_3.active = True
    rivesh_phrase_2.active = False
    rivesh_quest_1.active = True
    print('-'*25)
    input('You have recieved a Cherub pet! | Press Enter/Return ')
    inv_system.inventory['pets'].append(pets.pet_cherub)
    input('You now have experience defeating ghosts! | Press Enter/Return ')


stewson_quest_1.upon_starting = stwqst_us1
stewson_quest_1.upon_completing = stwqst_uc1

stewson = NPC('Stewson', [stewson_phrase_1, stewson_phrase_2, stewson_phrase_3, stewson_quest_1])

# --- Name: Seriph -- Town: Fort Sigil
seriph_phrase_1 = Conversation(['...You actually came to this town? And of your own',
                                'free will, too?! I was going to say that you were either',
                                'very brave or very stupid, but on second thought, the latter',
                                'is far more likely.'], active=True)

seriph_phrase_2 = Conversation(["What?! You're going to try to kill the evil spirit?",
                                "You're truely stupider than I thought. I wish you"
                                "good luck nonetheless."])

seriph_phrase_3 = Conversation(["I still can't believe that you killed the evil spirit!",
                                "We cannot thank you enough!"])

seriph = NPC('Seriph', [seriph_phrase_1, seriph_phrase_2, seriph_phrase_3])

# --- Name: Rivesh -- Town: Fort Sigil
rivesh_phrase_1 = Conversation(["Welcome, brave adventurer. I'm sure that you've been",
                                "informed of the problems around here, so I'd recommend...",
                                "Oh, what's that? You haven't? Well in that case, let me tell",
                                "you. A long time ago, a number of foolish adventurers,",
                                "searching for fame and glory, stumbled upon this fort.",
                                "Inside, they found a terrifying ghost, which they",
                                "oh-so-cunningly defeated -- or so they thought! No,",
                                "instead the ghost had grown tired of the pointless battle,",
                                "and decided to hide in the shadows of the unsuspecting 'heros'.",
                                "When they least expected it, the ghost possessed them!",
                                "As punishment for their foolishness, the evil spirit",
                                "now forcefully takes a victim from this town every 10 days",
                                "and forbids its inhabitants from leaving!"], active=True)

rivesh_phrase_2 = Conversation(["Hey... I don't suppose that you have any experiecne",
                                "with fighting ghosts, do you? No? Ok then. If you find",
                                "someone who has defeated a very menacing phantom before,",
                                "please request that they come help us!"], active=True)

rivesh_phrase_3 = Conversation(["Help us, young adventurer! You are the only one",
                                "who can save us from this terrible ghool!"])

rivesh_phrase_4 = Conversation(["Thanks again, hero! We are forever indebted to you!"])

rivesh_quest_1 = Quest(["Hey... I don't suppose that you have any experience",
                        "with fighting ghosts, do you? Wait, what's that? You",
                        "defeated the Phantom that was haunting the Overshire",
                        "Graveyard!? Well in that case, we may just have a chance!",
                        "Please help us, oh please!"], "The Curse of Fort Sigil",
                       ["Rid Fort Sigil of its curse by defeating the evil spirit at",
                       "coordinates 22\u00b0N, 3\u00b0E."], "Rivesh", [200, 200],
                       ["Y-you defeated the evil spirit? Praise Guido's beard! We are",
                        "free of this curse! You are forever in our gratitude, young hero!"])


def rivqst_us1():
    global rivesh_phrase_1
    global rivesh_phrase_2
    global rivesh_phrase_3
    global seriph_phrase_1
    global seriph_phrase_2

    rivesh_phrase_1.active = False
    rivesh_phrase_2.active = False
    rivesh_phrase_3.active = True
    seriph_phrase_1.active = False
    seriph_phrase_2.active = True
    bosses.cursed_spect.active = True


def rivqst_uc1():
    global rivesh_phrase_4
    global seriph_phrase_2
    global seriph_phrase_3

    rivesh_phrase_4.active = True
    seriph_phrase_2.active = False
    seriph_phrase_3.active = True


rivesh_quest_1.upon_starting = rivqst_us1
rivesh_quest_1.upon_completing = rivqst_uc1

rivesh = NPC('Rivesh', [rivesh_phrase_1, rivesh_phrase_2,
                        rivesh_phrase_3, rivesh_phrase_4, rivesh_quest_1])

#----------------------------------------------------------------------------#
# SIDEQUESTS

# -- Name: Alfred -- Town: Nearton
alfred_phrase_1 = Conversation(["It is rumored that a mighty gel-creature lives south-east",
                                "of this very town. I'd be careful around there if I were you."],
                               active=True)
alfred_phrase_2 = Conversation(["Come back here when you defeat the evil",
                                "Master Slime. Good luck!"])

alfred_phrase_3 = Conversation(["Greetings, Hero! Good luck on your adventures!"], repeat=True)

alfred_quest_1 = Quest(["...Actually, now that I think about it, do you think you could possibly",
                        "dispose of this vile creature? His location is 0\u00b0N, 1\u00b0E."],
                       'A Slimy Specimen',
                       ["Defeat the dreaded Master Slime at location 0\u00b0N, 1\u00b0E and then",
                        "return to Alfred in Nearton."], 'Alfred', [30, 50],
                       ["You defeated the evil Master Slime?!",
                        "Amazing! Take this, adventurer, you've earned it."], active=True)


def alfqst_us1():
    # Stands for "Alfred Quest 1 -- Upon Starting
    # Changes some of his dialogue options to reflect a quest beginning.
    global alfred_phrase_1
    global alfred_phrase_2
    bosses.master_slime.active = True
    alfred_phrase_1.active = False
    alfred_phrase_2.active = True


def alfqst_uc1():
    # Stands for "Alfred Quest 1 -- Upon Completing
    global alfred_phrase_3
    alfred_phrase_3.active = True


alfred_quest_1.upon_starting = alfqst_us1
alfred_quest_1.upon_completing = alfqst_uc1

alfred = NPC('Alfred', [alfred_phrase_1, alfred_phrase_2,
                        alfred_quest_1, alfred_phrase_3])

# -- Name: Kyle -- Town: Tripton
kyle_phrase_1 = Conversation(["Greeting, traveller. I am Kyle, Tripton's Village Elder.",
                              "You aren't from Fallville, right? Good.",
                              "Those stupid Fallvillians need to get away from our",
                              "land! It's they're fault they made a town that was so",
                              "easy to miss! I don't care if we have to go to war",
                              "with those dingbats, I'm not leaving this spot!"], active=True)

kyle_phrase_2 = Conversation(["Adventurer, we have heard reports that a mighty",
                              "beast is in our land! None of our men are willing",
                              "to risk their lives to stop it. We are doomed."])

kyle_phrase_3 = Conversation(["The mighty monster has fallen? Thank god!",
                              "What's this you say? The Fallvillians defeated it?",
                              "We owe them our lives. Perhaps we should think",
                              "about negotiating peace..."])


def kyle_p3_at():
    # Stands for "Kyle Phrase 3: After Talking"
    global kyle_phrase_3
    global kyle_phrase_4
    global alden_quest_1
    global alden_phrase_2

    kyle_phrase_3.active = False
    kyle_phrase_4.active = True
    if krystal_phrase_4.active:
        alden_quest_1.finished = True
        alden_phrase_2.active = False


kyle_phrase_3.after_talking = kyle_p3_at

kyle_phrase_4 = Conversation(["Welcome, adventurer, to the town of Tripton!"])

kyle = NPC('Kyle', [kyle_phrase_1, kyle_phrase_2, kyle_phrase_3, kyle_phrase_4])


# -- Name: Krystal -- Town: Fallville
krystal_phrase_1 = Conversation(["Hello, I am the Village Elder of Fallville. We don't take",
                                 "kindly to Triptonians around here, so tell us if",
                                 "you see any. What I don't understand is that the",
                                 "silly Triptonians blame us for their poor eyesight.",
                                 "It's all their fault, and they know it!"], active=True)

krystal_phrase_2 = Conversation(["AHHH! Help! There's a m-m-monster out there!",
                                 "Someone go kill it! AHHH!"])

krystal_phrase_3 = Conversation(["What, the monster is dead? Thank goodness!",
                                 "Oh, so the Triptonians killed it? Well then... I",
                                 "guess that we owe them our gratitude. Perhaps we",
                                 "should think about negotiating peace..."])


def krys_p3_at():
    # Stands for "Krystal Phrase 3: After Talking"
    global krystal_phrase_3
    global krystal_phrase_4
    global alden_quest_1
    global alden_phrase_2

    krystal_phrase_3.active = False
    krystal_phrase_4.active = True
    if kyle_phrase_4.active:
        alden_quest_1.finished = True
        alden_phrase_2.active = False


krystal_phrase_3.after_talking = krys_p3_at

krystal_phrase_4 = Conversation(["Greetings, hero! Welcome to Fallville."])

krystal = NPC('Krystal', [krystal_phrase_1, krystal_phrase_2,
                          krystal_phrase_3, krystal_phrase_4])


# -- Name: Frederick -- Town: Fallville
frederick_phrase_1 = Conversation(["I hear that there is a wise sage that has taken up",
                                   "residence in a small cottage southwest of this town.",
                                   "I would go and talk to him, but I have things to do."],
                                  active=True)

frederick_phrase_2 = Conversation(["There's a monster outside of town, and a big",
                                   "one at that! I hope it goes away..."])

frederick_phrase_3 = Conversation(["Thank heavens, the mighty beast has fallen."])

frederick = NPC('Frederick', [frederick_phrase_1, frederick_phrase_2, frederick_phrase_3])


# -- Name: Alden -- Town: Small Cottage (1)
alden_quest_1 = Quest(["Greetings, adventurer. I'm sure that you have heard of the",
                       "confict going on between the villages of Fallville and",
                       "Tripton. I have an idea on how to settle this foul feud,",
                       "but alas, I cannot perform it due to my old and fragile",
                       "state. You, however, appear to be a very young and capable",
                       "adventurer. Do you perhaps think that you could help me?",
                       "I need you to go defend the towns of Fallville and Tripton",
                       "from a terrible monster. This is a monster I will be summoning,",
                       "of course. Afterwards, spread word in the two towns",
                       "that an anonymous warrior from the opposite town defeated it!",
                       "This should bring an end to their constant bickering.",
                       "I will summon the monster at coordinates -23\u00b0S, -11\u00b0W."],
                      "Stop the Strife",
                      ["Defeat the monster at location -23\u00b0S, -11\u00b0W and then inform",
                       "The village elders at Tripton and Fallville of the opposite",
                       "village's bravery."], 'Alden', [175, 200],
                      ["Welcome back, brave adventurer. I have already received word",
                       "of the monster's defeat. I thank you ever so much for helping",
                       "us, hero."], active=True)


def aldqst_us1():
    global alden_phrase_1
    global krystal_phrase_1
    global kyle_phrase_1
    global krystal_phrase_2
    global kyle_phrase_2
    global frederick_phrase_1
    global frederick_phrase_2

    alden_phrase_1.active = True
    krystal_phrase_1.active = False
    kyle_phrase_1.active = False
    krystal_phrase_2.active = True
    kyle_phrase_2.active = True
    frederick_phrase_1.active = False
    frederick_phrase_2.active = True

    bosses.terr_tarrant.active = True


def aldqst_uc1():
    global alden_phrase_3
    global alden_quest_1

    alden_quest_1.active = False
    alden_phrase_3.active = True


alden_quest_1.upon_starting = aldqst_us1
alden_quest_1.upon_completing = aldqst_uc1

alden_phrase_1 = Conversation(["I've summoned the mighty beast. Now hurry up",
                               "and dispose of it before it causes any damage."])

alden_phrase_2 = Conversation(["You've defeated him? Good, now go talk to the village",
                               "elders! Good luck!"])

alden_phrase_3 = Conversation(["Thanks again, hero. You've saved those towns",
                               "a lot of trouble."])

alden = NPC('Alden', [alden_quest_1, alden_phrase_1, alden_phrase_2, alden_phrase_3])

#----------------------------------------------------------------------------#
# UNIMPORTANT CHARACTERS

# -- Name: Wesley -- Town: Southford
wesley_phrase_1 = Conversation(["Adventurers around this area say that monsters tend",
                                "to be stronger the farther from 0\u00b0N, 0\u00b0E that you \
travel.",
                                "However, monsters there also give better loot. Be careful."
                                ], active=True)

wesley = NPC('Wesley', [wesley_phrase_1])

# -- VName: Jeffery -- Town: Overshire
jeffery_phrase_1 = Conversation(["I heard that there was a man in a town far south-east of here",
                                 "who was in need of a messenger. I think the town was somewhere",
                                 "around -8\u00b0S, 20\u00b0E. Something like that."],
                                active=True)

jeffery = NPC('Jeffery', [jeffery_phrase_1])

# -- Name: Ethos -- Town: Charsulville
ethos_phrase_1 = Conversation(['Any smart adventurer would keep track of town coordinates',
                               'and powerful monsters in their inventory. If you get lost,',
                               'check there.'], active=True)

ethos = NPC('Ethos', [ethos_phrase_1])

# -- Name: F. Jones -- Town: Neo-Ekanmar
f_jones_phrase_1 = Conversation(['Hello, adventurer! My name if Fly. I used to be the Emperor of',
                                 'The Flysconian Empire, until that wrechted Pythonius messed',
                                 'things up! His people revolted, and then his friend Sugulat',
                                 'came in and overthrew us. He drove my people out of our lands,',
                                 'and now this town is all we have left. Please, leave me be.'],
                                active=True)

f_jones = NPC('F. Jones', [f_jones_phrase_1])

# -- Name: Stravi -- Town: Neo-Ekanmar
stravi_phrase_1 = Conversation(['Please, forgive my husband, Fly. He is very emotionial about',
                                "the whole revolution thing, I'd recommend just letting him be.",
                                "Oh, and whatever you do, do NOT under any circumstances mention",
                                'the word "chandelier". It makes him very upset for some reason.'],
                               active=True)

stravi = NPC('Stravi', [stravi_phrase_1])

# -- Name: Sakura -- Town: Principalia
sakura_phrase_1 = Conversation(['Hello, sir! What can Sakura do for you? Ah, you want to see the',
                                'King? The King is currently in Overshire. Sakura cannot imagine',
                                'that he is accepting visitors right now, though. Unless you have',
                                'something really important to tell him, such as how to save his',
                                "daughter, Sakura doesn't see you talking to him in your future."],
                               active=True)

sakura = NPC('Sakura', [sakura_phrase_1])

# -- Name: Sugulat -- Town: Ambercreek
sugulat_phrase_1 = Conversation(['Greetings! My name is Sugulat, Emperor of D\u00fC Haven',
                                 "and legendary digger of holes. Y'know, you look like",
                                 "a nice guy. I'm going to tell you a little secret: If you",
                                 "buy a shovel from the general store, you can dig up valuable",
                                 "gems in certain places! They can be tricky to find, though,",
                                 "so that's why I invented the Divining Rod! Simply use it,",
                                 "and it will tell you the approximate distance between",
                                 "you and the nearest gem. You can buy it at the general store."],
                                active=True)

sugulat = NPC('Sugulat', [sugulat_phrase_1])

all_dialogue = [
    philliard_phrase_1, philliard_phrase_2,
    wesley_phrase_1, seriph_phrase_1,
    rivesh_phrase_1, rivesh_phrase_2, rivesh_phrase_3, rivesh_phrase_4, rivesh_quest_1,
    alfred_phrase_1, alfred_phrase_2, alfred_phrase_3, alfred_quest_1,
    stewson_phrase_1, stewson_phrase_2, stewson_phrase_3, stewson_quest_1,
    kyle_phrase_1, kyle_phrase_2, kyle_phrase_3, kyle_phrase_4,
    krystal_phrase_1, krystal_phrase_2, krystal_phrase_3, krystal_phrase_4,
    frederick_phrase_1, frederick_phrase_2, frederick_phrase_3,
    joseph_phrase_1, joseph_phrase_2, joseph_phrase_3, joseph_quest_1,
    alden_quest_1, alden_phrase_1, alden_phrase_2, alden_phrase_3,
    azura_phrase_1, azura_phrase_2, azura_phrase_3, f_jones_phrase_1,
    stravi_phrase_1, sakura_phrase_1, sugulat_phrase_1, raidon_phrase_1
]


def serialize_dialogue(path):
    json_dialogue = {}

    for c in all_dialogue:
        if isinstance(c, Quest):
            json_dialogue[str(c)] = [c.active, c.repeat, c.started, c.finished]
        else:
            json_dialogue[str(c)] = [c.active, c.repeat]

    with open(path, encoding='utf-8', mode='w') as f:
        json.dump(json_dialogue, f, indent=4, separators=(', ', ': '))


def deserialize_dialogue(path):
    global all_dialogue

    with open(path, encoding='utf-8') as f:
        j_log = json.load(f)

    for key in j_log:
        for c in all_dialogue[:]:
            if key == str(c):
                if isinstance(c, Quest):
                    c.active, c.repeat, c.started, c.finished = \
                        j_log[key][0], j_log[key][1], j_log[key][2], j_log[key][3]
                else:
                    c.active, c.repeat = j_log[key][0], j_log[key][1]

import towns