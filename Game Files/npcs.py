# This file is part of Peasants' Ascension.
#
# Peasants' Ascension is free software: you can redistribute it and/or modify
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

import sys
import json
import copy
import random

import bosses
import inv_system
import items
import units

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

# Info for reading this file:
#
# This file contains all data regarding the logic behind quests, NPCs, and conversations.
# Every NPC has at least one conversation, and most (but not all) have at least one quest.
# Because of the way that the game works, the person you visit to finish the quest is ALWAYS
# the same person who gave it to you in the first place (this is subject to change if I
# can find a way around this without breaking the already existing quests).
#
# The quests are divided into three categories: Main Questline, Side-story arcs, and side quests.
# The main questline consists of all quests required to finish the game (when a way to do so is
# implemented) and it generally all follows the same story-arc. Side-story arcs include
# side-storyline that spans multiple quests, such as the Graveyard storyline. Side quests are
# single-quest story arcs that have almost nothing to do with the main plot.


class NPC:
    def __init__(self, name, conversations, occupation):
        self.name = name
        self.conversations = conversations
        self.occupation = occupation

    def __str__(self):
        return self.name

    def speak(self):

        # Print the NPC's dialogue to the player
        dialogue = []
        for w in self.conversations:
            if w.active:
                try:
                    if not w.started:  # Quests
                        dialogue.append(w.sentences)

                    elif w.started and w.finished and w.active:
                        dialogue = [w.end_dialogue]
                        break

                except AttributeError:  # Non-quests
                    dialogue.append(w.sentences)

        for y in dialogue[:]:

            # Create some padding so that everything lines up properly and looks nice
            padding = len(max(y, key=len))

            for z in y:
                if z != '-'*25:
                    input(''.join([self.name.title(), ': ', z, ' '*(padding - len(z)), ' | [ENTER] ']))

                else:
                    print(z)

            dialogue.remove(y)

            if dialogue:
                print('-'*25)

            for obj in self.conversations:
                if (isinstance(obj, Quest) and obj.end_dialogue == y) or obj.sentences == y:
                    y = obj

            if isinstance(y, Quest) and not y.started:
                y.give_quest()

            elif isinstance(y, Quest) and y.finished:
                y.completion()

            if hasattr(y, "after_talking"):
                y.after_talking()


class Conversation:
    def __init__(self, sentences, active=False):
        self.sentences = sentences
        self.active = active

    def __str__(self):
        for x in globals():
            if globals()[x] == self:
                return x


class Quest(Conversation):
    def __init__(self, sentences, name, desc, q_giver, reward, end_dialogue,
                 started=False, finished=False, active=False):
        Conversation.__init__(self, sentences, active)
        self.name = name  # The name of the quest
        self.desc = desc  # A brief summary of the goal of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.started = started  # is True if the quest has been started, false otherwise
        self.finished = finished  # is True if the quest is complete, false otherwise
        self.end_dialogue = end_dialogue  # What is printed when the quest is over

    def __str__(self):
        for x in globals():
            if globals()[x] == self:
                return x

    def give_quest(self):
        print('-'*25)
        print(''.join([self.name, ': \n  ', '\n  '.join([x for x in self.desc])]))
        print('-'*25)

        print(f'{self.q_giver} is offering you the quest "{self.name}".')

        while True:
            accept = input('Do you accept this quest? | Yes or No: ').lower()

            if accept.startswith('y'):
                print('-'*25)
                print(f'{self.q_giver}: "Terrific! Thank you for your help!"')
                self.started = True
                self.upon_starting()

                return

            elif accept.startswith('n'):
                print('-'*25)
                print(f'{self.q_giver}: "Oh... That\'s fine. Come back later if you change your mind."')

                return

    def completion(self):
        self.upon_completing()

        print("Quest Complete!")
        print(f"You've received {self.reward[0]} XP and {self.reward[1]} GP for completing this quest.")
        input('\nPress enter/return')

        main.party_info['gp'] += self.reward[1]
        units.player.exp += self.reward[0]
        units.player.level_up()

        self.active = False

#----------------------------------------------------------------------------#
# MAIN/STORYLINE QUESTS & NPCS

# -- Name: Solou -- Town: Nearton
solou_phrase_1 = Conversation(["H-hello! My name is Solou, wizard in training!",
                               "Well, the truth is that I'm actually a page for King Harconius II,",
                               "but my one dream is to become a master sorceress! Uh, well anyway",
                               "I'm here delivering a letter to a person named... oh wait a minute,",
                               "what did you say your name was? Yay, this letter is for you then!",
                               "As it is sensitive information, I am required by law to read it to you",
                               "and then dispose of it with fire!",
                               "*Ahem*: ",
                               '   "As captain of the 7th Platoon of the Harconian Army, you',
                               "    are hereby entrusted with the following information and a",
                               "    mission. Princess Celeste, heiress to the throne and daughter",
                               "    of His Majesty King Harconius II, has been kidnapped by the",
                               "    Thexus, a group of incredibly skilled and well-trained",
                               "    assassins from the island-nation of Thex. We know with 100%",
                               "    confidence her exact whereabouts, but the main issue is",
                               "    actually getting there. The island of Thex is encompassed by a",
                               "    seemingly indestructible barrier. It appears to be being",
                               "    generated by magestite, causing any chance of dispelling it",
                               "    to be futile. We need you to do everything in your power to",
                               "    figure out a way to infiltrate the island and retrieve",
                               '    Celeste. Signed, Chancellor Zadael".',
                               "I hope that this information will prove us- what's that? You're",
                               "NOT captain of the 7th platoon? You're just an adventurous",
                               "peasant? Uh oh, this isn't good! Now that I think of it, I don't think",
                               "our army even has a 7th platoon. This is really bad! Well I certainly",
                               "can't return to Zadael and tell him that I gave information to the",
                               "wrong person! He'd skin my hide for that! Oh no what do I do...",
                               "Hey, I've got an idea - how about I go adventuring with you? Like I said",
                               "Earlier, I've always dreamed of being a master sorceress, and joining",
                               "a mighty adventurer like yourself on your quest might help me achieve",
                               "my dreams! I'm sure that my wizardry would be of great use to you, too!"],
                              active=True)


def solou_p1_at():
    # Stands for "Solou Phrase I -- After Talking
    units.solou.enabled = True
    solou_phrase_1.active = False
    solou_phrase_2.active = True
    print("Solou the Mage has been added to your party!")
    input('\nPress enter/return ')
    print('-'*25)

solou_phrase_1.after_talking = solou_p1_at

solou_phrase_2 = Conversation(["No time to chat, we gotta get back to adventuring!"])

solou_quest_1 = Quest(["Before I resign as page and begin adventuring with you, it's only",
                       "fair that I finish delivering the letters I was given. They're",
                       "addressed to... ah - they're addressed to a few specific towns,",
                       "not to any specific person. That usually means that we must take",
                       "them to the mayor of said town, who will usually have the town",
                       "crier relay the message to the citizens. The first town we must visit",
                       "is Overshire, located northwest of here. I believe it's exact coordinates",
                       "are 13\u00b0N, -11\u00b0W. It's a massive place, there's no way we can",
                       "miss it."],
                      "A Courier's Resignation [MAIN QUEST]",
                      ["Travel over to Overshire and speak to the mayor. Overshire is located",
                       "at 13\u00b0N, -11\u00b0W, northwest of Nearton. Beware of the nearby graveyard!"],
                      "Solou", [25, 25], [], active=True)


def solou_q1_us():
    global joseph_quest_1

    joseph_phrase_2.active = True
    joseph_quest_1.active = True


solou_quest_1.upon_starting = solou_q1_us


def solou_q1_uc():
    pass


npc_solou = NPC("Solou", [solou_phrase_1, solou_phrase_2, solou_quest_1], "Page")

# -- Name: Joseph -- Town: Overshire
joseph_phrase_1 = Conversation(['Greetings, young adventurer. Welcome to Overshire.'], active=True)
joseph_phrase_2 = Conversation(["Ah, Solou! Long time no see! I see you've taken up adventuring.",
                                "It must be nice to finally put that spellbook of yours to use!",
                                "Oh, what's this? A letter for me? Well, I'll be sure to read this",
                                "later. Thank you for delivering this to me!"])


def joseph_p2_at():
    global joseph_phrase_2

    joseph_phrase_2.active = False
    solou_quest_1.completion()


joseph_phrase_2.after_talking = joseph_p2_at

joseph_phrase_3 = Conversation(["Go visit my friend Azura in Parceon. She knows more about this than",
                                "I do. Parceon is located at 24\u00b0N, 28\u00b0E in case you forgot"])

joseph_quest_1 = Quest(["Ah, Solou! Long time no see! I see you've taken up adventuring.",
                        "It must be nice to finally put that spellbook of yours to use!",
                        "*Solou and Joseph chat for a while. As mayor of Overshire, Joseph",
                        "is already well aware of Celeste being kidnapped.* Ah, so you adventurers",
                        "are questing to save his daughter? Well, I happen to know of a person",
                        "whose information would prove invaluable to you. Her name is Azura, and",
                        "she is the head of the Sorcerer's guild. She has been studying tomes and",
                        "has supposedly come up with a possible solution. She lives in a town",
                        "called Parceon, located at 24\u00b0N, 28\u00b0E."],
                       "To Parceon! [MAIN QUEST]",
                       ["Visit Azura at Parceon, located at24\u00b0N, 28\u00b0E, and",
                        "tell her that Joseph sent you. She has information that will",
                        "help you on your journey."], "Joseph", [75, 75], [])


def joseph_q1_us():
    global joseph_phrase_2
    global joseph_phrase_1

    joseph_phrase_1.active = False
    jospeh_phrase_3.active = True

joseph = NPC('Joseph', [joseph_phrase_1, joseph_quest_1, joseph_phrase_2, joseph_phrase_3], "Mayor of Overshire")

# -- Name: Orius -- Town: Charsulville
orius = NPC("Orius", [], "Mayor of Charsulville")

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
                               "a way to rescue King Harconius II's daughter, as Joseph probably",
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


def azura_p1_at():
    global azura_phrase_2
    global azura_phrase_3

    print('You write down the coordinates of Ambercreek.')
    input("\nPress enter/return ")
    azura_phrase_2.active = False
    azura_phrase_3.active = True


azura_phrase_2.after_talking = azura_p1_at

azura_phrase_3 = Conversation(["My father, Raidon, lives in the town of Ambercreek at",
                               "-7\u00b0S, -51\u00b0W. Good luck!"])

azura = NPC('Azura', [azura_phrase_1, azura_phrase_2, azura_phrase_3], "Sorcerer's Guildmaster")

# -- Name: Raidon -- Town: Ambercreek
raidon_phrase_1 = Conversation(["FILLER TEXT"], active=True)

raidon = NPC('Raidon', [raidon_phrase_1], "Village Shaman")

#----------------------------------------------------------------------------#
# SIDE-STORY ARCS

# -- Graveyard Story-arc:
# --- Name: Stewson -- Town: Overshire
stewson_phrase_1 = Conversation(["Our amazing Kingdom has 6 different regions:",
                                 "Tundra in the northwest, Swamp in the southeast,",
                                 "Mountains in the northeast, and Desert in the southwest.",
                                 "The Forest lies in the center, while the Shore surrounds them.",
                                 "There's a small region somewhere around here that is the",
                                 "cause of much worry and panic in this town: The Graveyard.",
                                 "Inside lies a dangerous apparition, feared by all who have seen it.",
                                 "As the captain of the guard, my men and I have tried",
                                 "and failed countless times to defeat that wretched ghost!",
                                 ], active=True)

stewson_phrase_2 = Conversation(["Please save us from this monstrous wraith!"])

stewson_phrase_3 = Conversation(["Thank you again for your help, adventurer!"])

stewson_quest_1 = Quest(["I wish someone would do something about this terrible",
                         "ghost... Hey! You're a strong adventurer, perhaps you",
                         "could defeat this phantom? It's at position 8\u00b0N, -12\u00b0W."],
                        'The Shadowy Spirit',
                        ["Defeat the feared Menacing Phantom at location",
                         "8\u00b0N, -12\u00b0W and then return to Stewson in Overshire."],
                        'Stewson', [50, 75],
                        ["You... you actually defeated it?! Thank you ever so much!",
                         "Finally my men and I can rest, and the town is safe!",
                         "Take this, it is the least our town can do for your bravery."],
                        active=True)


def stewson_q1_us():
    global stewson_phrase_1
    global stewson_phrase_2
    bosses.menac_phantom.active = True
    stewson_phrase_1.active = False
    stewson_phrase_2.active = True


def stewson_q1__uc():
    global stewson_phrase_3
    global rivesh_phrase_2
    global rivesh_quest_1

    stewson_phrase_3.active = True
    rivesh_phrase_2.active = False
    rivesh_quest_1.active = True
    print('-'*25)
    print('You now have experience defeating ghosts!')
    input("\nPress enter/return ")


stewson_quest_1.upon_starting = stewson_q1_us
stewson_quest_1.upon_completing = stewson_q1__uc

stewson = NPC('Stewson', [stewson_phrase_1, stewson_phrase_2, stewson_phrase_3, stewson_quest_1],
              "Captain of the Guard")

# --- Name: Seriph -- Town: Fort Sigil
seriph_phrase_1 = Conversation(['...You actually came to this town? And of your own',
                                'free will, too?! I was going to say that you were either',
                                'very brave or very stupid, but on second thought, the latter',
                                'is far more likely.'], active=True)

seriph_phrase_2 = Conversation(["What?! You're going to try to kill the evil spirit?",
                                "You're truly stupider than I thought. I wish you"
                                "good luck nonetheless."])

seriph_phrase_3 = Conversation(["I still can't believe that you killed the evil spirit!",
                                "We cannot thank you enough!"])

seriph = NPC('Seriph', [seriph_phrase_1, seriph_phrase_2, seriph_phrase_3], "Blacksmith")

# --- Name: Rivesh -- Town: Fort Sigil
rivesh_phrase_1 = Conversation(["Welcome, brave adventurer. I'm sure that you've been",
                                "informed of the problems around here, so I'd recommend...",
                                "Oh, what's that? You haven't? Well in that case, let me tell",
                                "you. A long time ago, a number of foolish adventurers,",
                                "searching for fame and glory, stumbled upon this fort.",
                                "Inside, they found a terrifying ghost, which they",
                                "oh-so-cunningly defeated -- or so they thought! No,",
                                "instead the ghost had grown tired of the pointless battle,",
                                "and decided to hide in the shadows of the unsuspecting 'heroes'.",
                                "When they least expected it, the ghost possessed them!",
                                "As punishment for their foolishness, the evil spirit",
                                "now forcefully takes a victim from this town every 10 days",
                                "and forbids its inhabitants from leaving!"], active=True)

rivesh_phrase_2 = Conversation(["Hey... I don't suppose that you have any experience",
                                "with fighting ghosts, do you? No? Ok then. If you find",
                                "someone who has defeated a very menacing phantom before,",
                                "please request that they come help us!"], active=True)

rivesh_phrase_3 = Conversation(["Help us, young adventurer! You are the only one",
                                "who can save us from this terrible spirit!"])

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


def rivesh_q1_us():
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


def rivesh_q1_uc():
    global rivesh_phrase_4
    global seriph_phrase_2
    global seriph_phrase_3

    rivesh_phrase_4.active = True
    seriph_phrase_2.active = False
    seriph_phrase_3.active = True


rivesh_quest_1.upon_starting = rivesh_q1_us
rivesh_quest_1.upon_completing = rivesh_q1_uc

rivesh = NPC('Rivesh', [rivesh_phrase_1, rivesh_phrase_2,
                        rivesh_phrase_3, rivesh_phrase_4, rivesh_quest_1], "Village Elder")

#----------------------------------------------------------------------------#
# SIDEQUESTS

# -- Name: Alfred -- Town: Nearton
alfred_phrase_1 = Conversation(["It is rumored that a mighty gel-creature lives south-east",
                                "of this very town. I'd be careful around there if I were you."],
                               active=True)
alfred_phrase_2 = Conversation(["Come back here when you defeat the evil",
                                "Master Slime. Good luck!"])

alfred_phrase_3 = Conversation(["Greetings, Hero! Good luck on your adventures!"])

alfred_quest_1 = Quest(["...Actually, now that I think about it, do you think you could possibly",
                        "dispose of this vile creature? His location is 0\u00b0N, 1\u00b0E."],
                       'A Slimy Specimen',
                       ["Defeat the dreaded Master Slime at location 0\u00b0N, 1\u00b0E and then",
                        "return to Alfred in Nearton."], 'Alfred', [30, 50],
                       ["You defeated the evil Master Slime?!",
                        "Amazing! Take this, adventurer, you've earned it."], active=True)


def alfred_q1_us():
    # Stands for "Alfred Quest 1 -- Upon Starting
    # Changes some of his dialogue options to reflect a quest beginning.
    global alfred_phrase_1
    global alfred_phrase_2
    bosses.master_slime.active = True
    alfred_phrase_1.active = False
    alfred_phrase_2.active = True


def alfred_q1_uc():
    # Stands for "Alfred Quest 1 -- Upon Completing
    global alfred_phrase_3
    alfred_phrase_3.active = True


alfred_quest_1.upon_starting = alfred_q1_us
alfred_quest_1.upon_completing = alfred_q1_uc

alfred = NPC('Alfred', [alfred_phrase_1, alfred_phrase_2,
                        alfred_quest_1, alfred_phrase_3], "Cobbler")

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
    if krystin_phrase_4.active:
        alden_quest_1.finished = True
        alden_phrase_2.active = False


kyle_phrase_3.after_talking = kyle_p3_at

kyle_phrase_4 = Conversation(["Welcome, adventurer, to the town of Tripton!"])

kyle = NPC('Kyle', [kyle_phrase_1, kyle_phrase_2, kyle_phrase_3, kyle_phrase_4], "Village Elder")


# -- Name: Krystin -- Town: Fallville
krystin_phrase_1 = Conversation(["Hello, I am the Village Elder of Fallville. We don't take",
                                 "kindly to Triptonians around here, so tell us if",
                                 "you see any. What I don't understand is that the",
                                 "silly Triptonians blame us for their poor eyesight.",
                                 "It's all their fault, and they know it!"], active=True)

krystin_phrase_2 = Conversation(["AHHH! Help! There's a m-m-monster out there!",
                                 "Someone go kill it! AHHH!"])

krystin_phrase_3 = Conversation(["What, the monster is dead? Thank goodness!",
                                 "Oh, so the Triptonians killed it? Well then... I",
                                 "guess that we owe them our gratitude. Perhaps we",
                                 "should think about negotiating peace..."])


def krystin_p3_at():
    # Stands for "Krystin Phrase 3: After Talking"
    global krystin_phrase_3
    global krystin_phrase_4
    global alden_quest_1
    global alden_phrase_2

    krystin_phrase_3.active = False
    krystin_phrase_4.active = True
    if kyle_phrase_4.active:
        alden_quest_1.finished = True
        alden_phrase_2.active = False


krystin_phrase_3.after_talking = krystin_p3_at

krystin_phrase_4 = Conversation(["Greetings, hero! Welcome to Fallville."])

krystin = NPC('Krystin', [krystin_phrase_1, krystin_phrase_2,
                          krystin_phrase_3, krystin_phrase_4], "Village Elder")


# -- Name: Frederick -- Town: Fallville
frederick_phrase_1 = Conversation(["I hear that there is a wise sage that has taken up",
                                   "residence in a small cottage southwest of this town.",
                                   "I would go and talk to him, but monsters have been roaming",
                                   "around the outskirts of town lately and it just isn't safe",
                                   "to travel anymore."],
                                  active=True)

frederick_phrase_2 = Conversation(["There's a monster outside of town, and a big",
                                   "one at that! I hope it goes away..."])

frederick_phrase_3 = Conversation(["Thank heavens, the mighty beast has fallen."])

frederick = NPC('Frederick', [frederick_phrase_1, frederick_phrase_2, frederick_phrase_3],
                "Scholar")


# -- Name: Alden -- Town: Small Cottage (1)
alden_quest_1 = Quest(["Greetings, adventurer. I'm sure that you have heard of the",
                       "conflict going on between the villages of Fallville and",
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


def alden_q1_us():
    global alden_phrase_1
    global krystin_phrase_1
    global kyle_phrase_1
    global krystin_phrase_2
    global kyle_phrase_2
    global frederick_phrase_1
    global frederick_phrase_2

    alden_phrase_1.active = True
    kyle_phrase_1.active = False
    kyle_phrase_2.active = True
    krystin_phrase_1.active = False
    krystin_phrase_2.active = True
    frederick_phrase_1.active = False
    frederick_phrase_2.active = True
    bosses.terr_tarrant.active = True


def alden_q1_uc():
    global alden_phrase_3
    global alden_quest_1

    alden_quest_1.active = False
    alden_phrase_3.active = True


alden_quest_1.upon_starting = alden_q1_us
alden_quest_1.upon_completing = alden_q1_uc

alden_phrase_1 = Conversation(["I've summoned the mighty beast. Now hurry up",
                               "and dispose of it before it causes any damage."])

alden_phrase_2 = Conversation(["You've defeated him? Good, now go talk to the village",
                               "elders! Good luck!"])

alden_phrase_3 = Conversation(["Thanks again, hero. You've saved those towns",
                               "a lot of trouble."])

alden = NPC('Alden', [alden_quest_1, alden_phrase_1, alden_phrase_2, alden_phrase_3], "Sage")

# -- Name: Polmor -- Town: Whistumn
polmor_phrase_1 = Conversation(['Our poor daughter! Serena and I have been working on a cure, but',
                                'we cannot find anyone stup-I mean brave enough to gather the',
                                'resources we need. All is lost if we cannot get the ingredients.'],
                               active=True)

polmor_quest_1 = Quest(["Wait a minute... I am so stupid! According to my calculations, you",
                        'are the legendary adventurer of Nearton! Yes, it must be you!',
                        'Please, adventurer, help our daughter! The only way to get the',
                        'ingredients is to defeat several monsters and collect their remains.',
                        "You're the only one who can save her!"],
                       "Fight Against the Blight",
                       ["Collect one Fairy Dust, one Serpent Scales, and one Monster Fang",
                        "by defeating monsters, then return to Polmor in Whistumn."],
                       "Polmor", [450, 450],
                       ["...Wait, what?! You obtained the items we needed? ",
                        "You are our savior! We owe our lives to you, you are",
                        "truly a hero! *He walks over to his wife, and the two begin",
                        "mixing the ingredients to make the cure for Hatchnuk's Blight*",
                        "At last, we have the cure! Let us not waste time. *The two administer",
                        "the medicine to their daughter, and she immediately begins ",
                        "feeling better.* Oh joy of joys! Our daughter is healed! How can we",
                        "ever repay you, oh noble adventurer and vanquisher of the Blight?",
                        "Here, take this. It is the absolute least that we can do."], active=True)


def polmor_q1_us():
    global serena_phrase_2
    global serena_phrase_1
    global polmor_phrase_2
    global polmor_phrase_1

    serena_phrase_1.active = False
    serena_phrase_2.active = True
    polmor_phrase_1.active = False
    polmor_phrase_2.active = True


def polmor_q1_uc():
    global serena_phrase_2
    global ser_pol_phrase_3
    global polmor_phrase_2

    ser_pol_phrase_3.active = True
    serena_phrase_2.active = False
    polmor_phrase_2.active = False
    polmor_quest_1.active = False

    print('-'*25)
    print('Serena and Polmor will now heal you for free if you visit them!')


polmor_quest_1.upon_starting = polmor_q1_us
polmor_quest_1.upon_completing = polmor_q1_uc

polmor_phrase_2 = Conversation(['Please, return once you have obtained one Monster Fang,',
                                'one Serpent Scale, and one Fairy Dust. You must',
                                'save our daughter!'])


def polmor_p2_at():
    # Check the player's inventory for the objects necessary to finish the quest.
    any_fangs = False
    any_scales = False
    any_dust = False

    for item in inv_system.inventory['misc']:
        if item.name == 'Monster Fang':
            any_fangs = True

        elif item.name == 'Serpent Scale':
            any_scales = True

        elif item.name == 'Fairy Dust':
            any_dust = True

    if any_fangs and any_scales and any_dust:
        # Iterate over a copy to prevent problems
        for item in inv_system.inventory['misc'][:]:
            if item.name == 'Monster Fang' and any_fangs > 0:
                inv_system.inventory['misc'].remove(item)
                any_fangs = False

            elif item.name == 'Serpent Scale' and any_scales:
                inv_system.inventory['misc'].remove(item)
                any_scales = False

            elif item.name == 'Fairy Dust' and any_dust:
                inv_system.inventory['misc'].remove(item)
                any_dust = False

        polmor_quest_1.finished = True
        print('-'*25)
        polmor.speak()


polmor_phrase_2.after_talking = polmor_p2_at

ser_pol_phrase_3 = Conversation(['You are our heroes! Here, allow us to treat your wounds.'])


def ser_pol_p3_at():
    units.player.hp += (units.player.max_hp - units.player.hp)
    units.player.mp += (units.player.max_mp - units.player.mp)
    units.player.status_ail = 'none'

    units.solou.hp += (units.solou.max_hp - units.solou.hp)
    units.solou.mp += (units.solou.max_mp - units.solou.mp)
    units.solou.status_ail = 'none'

    units.ran_af.hp += (units.ran_af.max_hp - units.ran_af.hp)
    units.ran_af.mp += (units.ran_af.max_mp - units.ran_af.mp)
    units.ran_af.status_ail = 'none'

    units.adorine.hp += (units.adorine.max_hp - units.adorine.hp)
    units.adorine.mp += (units.adorine.max_mp - units.adorine.mp)
    units.adorine.status_ail = 'none'

    units.chyme.hp += (units.chyme.max_hp - units.chyme.hp)
    units.chyme.mp += (units.chyme.max_mp - units.chyme.mp)
    units.chyme.status_ail = 'none'

    units.xoann.hp += (units.xoann.max_hp - units.xoann.hp)
    units.xoann.mp += (units.xoann.max_mp - units.xoann.mp)
    units.xoann.status_ail = 'none'

    units.parsto.hp += (units.parsto.max_hp - units.parsto.hp)
    units.parsto.mp += (units.parsto.max_mp - units.parsto.mp)
    units.parsto.status_ail = 'none'

    print('-'*25)
    print('Polmor and Serena get to work on healing your party.')
    print('Your party has been restored to full HP and healed of its status ailments.')


ser_pol_phrase_3.after_talking = ser_pol_p3_at

polmor = NPC('Polmor', [polmor_phrase_1, polmor_quest_1, polmor_phrase_2, ser_pol_phrase_3],
             "Engineer")

# -- Name: Matti -- Town: Lantonum
matthew_phrase_1 = Conversation(["*You try to talk to the man in the bar, but he is too",
                                 'busy listening to music on his "iSound" to notice you.',
                                 'Suddenly, a peasant walks up behind him, screams "Witch!!",',
                                 'grabs the iSound, and smashes it to bits on the floor. He',
                                 'then proceeds to set it on fire and bury the ashes in the dirt',
                                 'behind the bar.*'], active=True)

matthew_phrase_2 = Conversation(["Hello, friend! Have you gotten me a new iSound yet?"])

matthew_phrase_3 = Conversation(["No? That's okay. Just pick one up for me when you",
                                 "get the chance. You can purchase them at the town",
                                 "of Cesura, located at 123\u00b0N, 58\u00b0E."])

matthew_phrase_4 = Conversation(["You have? Wonderful! *He takes the iSound from your",
                                 "hand and pulls out 1250 GP*"])


def matthew_p2_at():
    global matthew_phrase_3
    global matthew_phrase_4
    global matthew_phrase_2

    matthew_phrase_2.active = False

    for i in inv_system.inventory['q_items']:
        if i.name == "iSound":
            matthew_phrase_4.active = True
            inv_system.inventory['q_items'].remove(i)
            break

    else:
        matthew_phrase_3.active = True

    matthew.speak()


def matthew_p3_at():
    global matthew_phrase_3
    matthew_phrase_3.active = False


def matthew_p4_at():
    global matthew_quest_1
    global matthew_phrase_4

    matthew_quest_1.finished = True
    matthew_phrase_4.active = False

    matthew.speak()


matthew_quest_1 = Quest(["Dangit, that happens all the time! Those idiots keep calling my",
                         "iSound MP3 player a witch - this is the fifth one I've gone through",
                         "this week! The company that makes them only sells them in Elysium, as",
                         "nobody in Harconia could tell an MP3 player from a brick if their life",
                         "depended on it. Hey, I'll tell you want: If you go to Cesura, the",
                         "train town near the border of Harconia and Elysium, and buy me a new",
                         "iSound, I will reward you greatly. Remember: iSounds have watermelons",
                         "on the back. If you get one with a grapefruit, then you're just paying",
                         "a lot of money for a cheap knockoff brand. And definitely stay away",
                         "from papaya phones. Can you do that for me?"],
                        'iSounds Good',
                        ["Retrieve a new iSound MP3 Player - whatever that is - from a shop in",
                         "Cesura. Cesura is located at 123\u00b0N, 58\u00b0E. Return to Matthew",
                         "at Lantonum when you are finished."],
                        "Matthew", [1250, 1250],
                        ["Thanks, man! This latest version is supposed to be",
                         "peasant-proof, so let's hope tha- *His statement is cut off",
                         "as a local serf runs up and tackles him, pries the iSound",
                         "from his hands, tosses it into a bucket of water, observes",
                         'that it does not float, screams "WITCH", and then rushes',
                         "over to the blacksmith's shop and throws the device into",
                         "the forge. A bloody fight ensues, as the blacksmith attacks",
                         'the serf for "defiling his forge with the blood of a witch".',
                         'The serf is killed, and the town guards rush over and arrest',
                         'the blacksmith for murdering the innocent but idiotic serf.',
                         'You and Matthew look each other in the eyes, he hands you the',
                         "money, and you both leave the scene without speaking another",
                         "word.",
                         '-'*25], active=True)
def matthew_q1_us():
    global matthew_phrase_1
    global matthew_phrase_2

    matthew_phrase_1.active = False
    matthew_phrase_2.active = True


def matthew_q1_uc():
    global matthew_phrase_5
    global matthew_quest_1
    matthew_phrase_5.active = True
    matthew_quest_1.active = False

matthew_quest_1.upon_starting = matthew_q1_us
matthew_quest_1.upon_completing = matthew_q1_uc


matthew_phrase_5 = Conversation(["...", "*He looks quite depressed.*"])

matthew_phrase_2.after_talking = matthew_p2_at
matthew_phrase_3.after_talking = matthew_p3_at
matthew_phrase_4.after_talking = matthew_p4_at

matthew = NPC('Matthew', [matthew_phrase_1, matthew_quest_1, matthew_phrase_2,
                          matthew_phrase_3, matthew_phrase_4, matthew_phrase_5],
              "Interstellar Traveller")

# -- Name: Pime -- Town: Sanguion
pime_phrase_1 = Conversation(["Hello, traveller! You do not look familiar - quick, come inside,",
                              "it's not been safe to stay out here for the past few weeks.",
                              "*Pime ushers you into a tavern filled with people whom he seems",
                              "to be quite friendly with. They likewise are quite kind to you.*",
                              "My name is Pime. I am the chief of this town, and the head of",
                              "Sanguion's militia. As I'm sure you know, me, and all the other",
                              "people in this inn, are vampires. Do not be alarmed! We only feast",
                              "on wild animals and vampire hunters. You are completely safe, as",
                              "long as you are not a hunter, that is. As of late, a new group",
                              'of vampire hunters named the "Anti-blood Squad". Not only do these',
                              "terrorists have an extraordinarily uncreative name, but they've",
                              "also been capturing our friends and family and are torturing,",
                              "ransoming, and even killing them! We vampires are not harmful to",
                              "society, and do not deserve this kind of treatment! Our loved",
                              "ones are dying to those monsters, and we don't have anywhere",
                              "near enough manpower to put a stop to it! What are we to do?!",
                              ], active=True)


def pime_p1_at():
    global pime_phrase_2
    global pime_quest_1
    global pime_phrase_1

    if units.player.lvl >= 10:
        pime_quest_1.active = True
        pime_phrase_1.active = False
        pime_phrase_2.active = False

    else:
        pime_phrase_2.active = True


pime_phrase_1.after_talking = pime_p1_at

pime_phrase_2 = Conversation(["Perhaps you could... nevermind, we need a more experienced",
                              "individual to help us with our plight. Come back later.",
                              "*Pime needs someone who is at least level 10. Go level up a bit!"])

pime_quest_1 = Quest(["Hey - you look like quite the seasoned adventurer. Maybe you could help",
                      "us! I hope this isn't too much to ask, but could you possibly defeat",
                      "this dreaded vampire hunter for us? He's causing us so much pain, we need",
                      "someone to get rid of him."],
                     "The Hated Hunter",
                     ["Defeat Herises, the head of the Anti-blood Squad, as well as his lackeys.",
                      "Their base is supposedly located at -68\u00b0S, -93\u00b0W, then return",
                      "to Pime at Sanguion."], "Pime",
                     [1000, 1000],
                     ["Di... did you really defeat them? Amazing! You have saved us so much",
                      "trouble! Those horrendous villains shall not hurt our tribe anymore!",
                      "*He looks overjoyed, and gives you a great big hug. One wonders why",
                      "the hunters attacked these people in the first place.*"])


def pime_q1_us():
    global pime_phrase_1
    global pime_phrase_3

    pime_phrase_1.active = False
    pime_phrase_3.active = True
    bosses.anti_blood_squad.active = True


def pime_q1_uc():
    global pime_quest_1
    global pime_phrase_4

    pime_quest_1.active = False
    pime_phrase_4.active = True


pime_quest_1.upon_starting = pime_q1_us
pime_quest_1.upon_completing = pime_q1_uc

pime_phrase_3 = Conversation(["Please deal with those blasted vampire hunters! Their hideout",
                              "is located at -68\u00b0S, -93\u00b0W."])

pime_phrase_4 = Conversation(["Thank you every so much for ridding us of those vile",
                              "terrorists! You are forever in our gratitude!"])

pime = NPC('Pime', [pime_phrase_1, pime_phrase_2, pime_quest_1, pime_phrase_3, pime_phrase_4],
           "Vampire Shaman")

#----------------------------------------------------------------------------#
# UNIMPORTANT CHARACTERS

# -- Name: Philliard -- Town: Nearton
philliard_phrase_1 = Conversation(["Hello, adventurer!", "Welcome to the Kingdom of Harconia."], active=True)

philliard = NPC('Philliard', [philliard_phrase_1], "Scribe")

# -- Name: Sondalar -- Town: Nearton
sondalar_phrase_1 = Conversation(["Greetings! Say, I haven't seen you in quite a while!",
                                  "I've been travelling across the Kingdom for the past few",
                                  "years, and haven't had time to say hello. Let me share some",
                                  "of the knowledge I gained while on my route: every town",
                                  "has a general store and an inn. Make good use of them!",
                                  "The general store sells all sorts of helpful equipment,",
                                  "and the further you travel from Nearton, the better their",
                                  "stock will get! Don't ask why - all I've heard is that it's",
                                  "supposedly better for business or something. Inns are helpful",
                                  "too. They will, usually for a fee, heal all your wounds and",
                                  "give you some precious time and space to write in that travel",
                                  "log you've got there. That's all I've got to say, catch up with",
                                  "you soon hopefully!"], active=True)

sondalar = NPC('Sondalar', [sondalar_phrase_1], "Goods Peddler")

# -- Name: Saar -- Town: Nearton
saar_phrase_1 = Conversation(["I haven't really explored too far away from this town.",
                              "In fact, the only other towns I've been to are Southford,",
                              "located at -6\u00b0S, -2\u00b0W, and Overshire, located",
                              "at 13\u00b0N, -11\u00b0W. Overshire is a pretty",
                              "big city, though - in fact, it's the capital of our Kingdom!"],
                             active=True)

saar = NPC("Saar", [saar_phrase_1], "Bard")

# -- Name: Wesley -- Town: Southford
wesley_phrase_1 = Conversation(["Adventurers around this area say that monsters tend",
                                "to be stronger the farther from 0\u00b0N, 0\u00b0E that you travel.",
                                "However, monsters there also give better loot. Be careful."], active=True)

wesley = NPC('Wesley', [wesley_phrase_1], "Peasant")

# -- Name: Lazaro -- Town: Southford
lazaro_phrase_1 = Conversation(["Greetings, adventurer from Nearton! How do I know who",
                                "you are, you ask? Well, I am the oracle of Southford!",
                                "His Divinity told me that you would be coming. He gave",
                                "me a message:",
                                "  \"Your position is saved whenever you cross region borders",
                                "  or visit a town. If you die, you will return there!\"",
                                "That's what He said. I do not understand His words, but",
                                "I hope they serve their intended recipient well."], active=True)

lazaro = NPC('Lazaro', [lazaro_phrase_1], "Oracle")

# -- Name: Typhen -- Town: Overshire
typhen_phrase_1 = Conversation(["I've heard that when you use healing spells, you restore",
                                "additional HP based on your wisdom! Paladins supposedly get",
                                "an even larger restoration bonus when they heal!"], active=True)

typhen = NPC('Typhen', [typhen_phrase_1], "Novice Cleric")

# -- Name: Jeffery -- Town: Overshire
jeffery_phrase_1 = Conversation(["Have you heard about what happened to Princess Celeste?",
                                 "The news of her kidnapping is spreading across the kingdom",
                                 "like wildfire! Those blasted Thexians will pay for this!"],
                                active=True)

jeffery = NPC('Jeffery', [jeffery_phrase_1], "Gossipping Serf")

# -- Name: Harthos -- Town: Overshire
harthos_phrase_1 = Conversation(["Welcome to Overshire, stranger! Our Kingdom's capital is",
                                 "pretty big, so try not to get lost, haha!"], active=True)

harthos = NPC("Harthos", [harthos_phrase_1], "Lumberjack")

# -- Name: Ethos -- Town: Charsulville
ethos_phrase_1 = Conversation(['Any smart adventurer would keep track of town coordinates',
                               'and powerful monsters in their inventory. If you get lost,',
                               'check there.'], active=True)

ethos = NPC('Ethos', [ethos_phrase_1], "Courier")

# -- Name: F. Jones -- Town: New Ekanmar
f_jones_phrase_1 = Conversation(['Hello, adventurer! My name is Fly, ruler of the',
                                 "Kingdom of Flyscoria. I'm quite busy right now, please come",
                                 "back later if you wish to speak to me."],
                                active=True)

f_jones = NPC('F. Jones', [f_jones_phrase_1], "King of Flyscoria")

# -- Name: Stravi -- Town: New Ekanmar
stravi_phrase_1 = Conversation(["Greetings, young traveller. I am Stravi, Queen of Flyscoria. My",
                                "husband and I are on important business relating to the recent",
                                "kidnapping of King Harconius II's daughter, Celeste. Please",
                                "return in a few weeks if you wish to speak to Fly and me.",
                                "Oh, and whatever you do, do not under ANY circumstances mention",
                                'the word "chandelier" to my husband. It makes him very',
                                'upset for some reason.'],
                               active=True)

stravi = NPC('Stravi', [stravi_phrase_1], "Queen of Flyscoria")

# -- Name: Caesar -- Town: New Ekanmar
caesar_phrase_1 = Conversation(["*Caesar, Fly's pet strawberry dragon, runs away and hides behind",
                                'his owner before you get a chance to converse with him.*'],
                               active=True)

caesar = NPC('Caesar', [caesar_phrase_1], "Fly's Pet")

# -- Name: Sakura -- Town: Principalia
sakura_phrase_1 = Conversation(['HALT! State your business! Ah, you want to see the King, do you?',
                                'Well, the King is currently in Overshire. Sakura cannot imagine',
                                'that he is accepting visitors right now, though. Unless you have',
                                'something really important to tell him, such as how to save his',
                                "daughter, Sakura doesn't see you talking to him in your future.",
                                "Now get out of here, Sakura is busy!"],
                               active=True)

sakura = NPC('Sakura', [sakura_phrase_1], "Head of the Royal Guard")

# -- Name: Strathius -- Town: Ravenstone
strathius_phrase_1 = Conversation(["Greetings, man! I'm like, Strathius, and I'm a druid.",
                                   "I'm one with like, nature. I'm gonna give you some helpful",
                                   "advice, man. Monsters can give you these like, things, called"
                                   "\"Status Ailments\" which like, totally harsh your style brah.",
                                   "Sleepiness causes you to be totally immobilized for a few",
                                   "turns. Paralyzation makes you totally slow for a while.",
                                   "Weakness makes you like a total softy, and you don't deal",
                                   "much damage man. Poison is mega-harsh, dude. It makes you",
                                   "take a little bit of damage each, like, turn. Not cool.",
                                   "Blindness is also totally whack - it makes you aim",
                                   "like a total nut, and shoot like a noob. Silence is bad news",
                                   "for mages 'cuz it means you can't use magic for a bit.",
                                   "Always keep a stash of items to cure these sicknesses, or ",
                                   "simply like, use the spell you get at level 5."], active=True)

strathius = NPC("Strathius", [strathius_phrase_1], "Druid")

# -- Name: Sugulat -- Town: Ambercreek
sugulat_phrase_1 = Conversation(["Greetings! My name is Sugulat, Emperor of Chin'tor",
                                 "and legendary digger of holes. Y'know, you look like",
                                 "a nice guy. I'm going to tell you a little secret: If you",
                                 "buy a shovel from the general store, you can dig up valuable",
                                 "gems in certain places! They can be tricky to find, though,",
                                 "so that's why I invented the Divining Rod! Simply use it,",
                                 "and it will tell you the approximate distance between",
                                 "you and the nearest gem. You can buy it at the general store."],
                                active=True)

sugulat = NPC('Sugulat', [sugulat_phrase_1], "Emperor of Chin'tor")

# -- Name: Serena -- Town: Whistumn
serena_phrase_1 = Conversation(["Oh, woe is me! My daughter has fallen ill from a terrible",
                                """disease! They call it "Hatchnuk's Blight", and it is""",
                                "very deadly. Oh, what am I to do? *sobs uncontrollably*"],
                               active=True)

serena_phrase_2 = Conversation(['You are a good man, trying to help our daughter! Good',
                                'luck on your quest!'])

serena = NPC('Serena', [serena_phrase_1, serena_phrase_2, ser_pol_phrase_3], "Scientist")

# -- Name: Bamdeliit -- Town: Cesura
bamdeliit_phrase_1 = Conversation(["Hello, sir! I'm Bamdeliit, the head engineer of Cesura!",
                                   "I'm a native Elysian, and have only been here for around",
                                   "a year, so I'm pretty new to this place! Most of my",
                                   "time is spent making sure that these trains run properly.",
                                   'By the way, do you know what "witch" means? Hythic isn\'t my',
                                   'first language, and the townsfolk keep calling me that when',
                                   'I turn on the trains. Witch is a good thing, right?'
                                   ], active=True)

bamdeliit = NPC('Bamdeliit', [bamdeliit_phrase_1], "Engineer")

# -- Name: Ariver -- Town: Sanguion
ariver_phrase_1 = Conversation(["*Ariver mistakes you for a vampire hunter and runs quickly",
                                "into his house, locking the doors, shutting the windows, and",
                                "closing the blinds. As you begin walking away, scratching your",
                                "head in confusion, you see him look out the window and walk",
                                "back outside, having determined you are not a threat at the",
                                "moment.*"], active=True)

ariver = NPC('Ariver', [ariver_phrase_1], "Vampire")

oralyn = NPC('Oralyn', [], '')

# -- Name: Fitzgerald -- Town: Valenfall
fitz_phrase_1 = Conversation(["*hic* Pay no attention to the behind behind the curtain!",
                              "*The man appears to be quite drunk. You also notice a",
                              "distinct lack of any curtain nearby.* *hic* Drop that, you",
                              "thief! Give me back my penny-loafers! *You slowly walk away",
                              "from the raving drunk.*"], active=True)

fitzgerald = NPC("Fitzgerald the Drunk", [fitz_phrase_1], "Raving Alcoholic")

all_dialogue = [
    solou_phrase_1, solou_phrase_2, solou_quest_1,

    rivesh_phrase_1, rivesh_phrase_2, rivesh_phrase_3, rivesh_phrase_4, rivesh_quest_1,

    alfred_phrase_1, alfred_phrase_2, alfred_phrase_3, alfred_quest_1,

    stewson_phrase_1, stewson_phrase_2, stewson_phrase_3, stewson_quest_1,

    kyle_phrase_1, kyle_phrase_2, kyle_phrase_3, kyle_phrase_4,

    krystin_phrase_1, krystin_phrase_2, krystin_phrase_3, krystin_phrase_4,

    frederick_phrase_1, frederick_phrase_2, frederick_phrase_3,

    joseph_phrase_1, joseph_phrase_2, joseph_phrase_3, joseph_quest_1,

    alden_quest_1, alden_phrase_1, alden_phrase_2, alden_phrase_3,

    azura_phrase_1, azura_phrase_2, azura_phrase_3,

    polmor_phrase_1, polmor_phrase_2, polmor_quest_1, ser_pol_phrase_3,
    serena_phrase_1, serena_phrase_2,

    matthew_phrase_1, matthew_quest_1, matthew_phrase_2,
    matthew_phrase_3, matthew_phrase_4, matthew_phrase_5,

    pime_phrase_1, pime_quest_1, pime_phrase_2, pime_phrase_3, pime_phrase_4,

    philliard_phrase_1,
    f_jones_phrase_1,
    stravi_phrase_1,
    sakura_phrase_1,
    sugulat_phrase_1,
    raidon_phrase_1,
    lazaro_phrase_1,
    caesar_phrase_1,
    wesley_phrase_1,
    seriph_phrase_1,
    strathius_phrase_1,
    ariver_phrase_1,
    fitz_phrase_1,
    harthos_phrase_1,
    typhen_phrase_1,
    sondalar_phrase_1,
    saar_phrase_1
]


def serialize_dialogue(path):
    json_dialogue = {}

    for c in all_dialogue:
        if isinstance(c, Quest):
            json_dialogue[str(c)] = [c.active, c.started, c.finished]
        else:
            json_dialogue[str(c)] = [c.active]

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
                    c.active, c.started, c.finished = \
                        j_log[key][0], j_log[key][1], j_log[key][2]
                else:
                    c.active = j_log[key][0]

import towns