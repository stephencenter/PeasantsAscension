import sys
import json
import bosses
import inv_system

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]


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
            for z in y:
                input(self.name + ': "' + z + '" | Press enter/return ')
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


class Conversation:
    def __init__(self, sentences, repeat=False, active=False):
        self.sentences = sentences
        self.repeat = repeat  # True if the conversation is generic and unimportant
        self.active = active

    def __str__(self):
        # Returns a unique string based on the content of the conversation.
        # This is used as a dictionary key to save information about conversations.
        return ''.join([x[0:6] for x in self.sentences])

class Quest(Conversation):
    def __init__(self, sentences, name, desc, q_giver, reward, end_dialogue,
                 req_lvl=1, started=False, finished=False, repeat=False, active=False):
        Conversation.__init__(self, sentences, repeat, active)
        self.name = name  # The name of the quest
        self.desc = desc  # A breif summary of the goal of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.req_lvl = req_lvl  # The level that you must be at to begin the quest
        self.started = started  # is True if tje quest has been started, false otherwise
        self.finished = finished  # is True if the quest is complete, false otherwise
        self.end_dialogue = end_dialogue  # What is printed when the quest is over

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
            try:
                accept = accept.lower()
            except AttributeError:
                continue
            if accept in ['yes', 'y']:
                print('-'*25)
                print('{0}: "Terrific! Come see me when you are finished."'.format(self.q_giver))
                self.started = True
                self.upon_starting()
                return
            elif accept in ['no', 'n']:
                print('-'*25)
                print('{0}: "...Oh. Come back later if you change your mind."'.format(self.q_giver))
                return

    def completion(self):
        main.player.exp += self.reward[0]
        main.static['gp'] += self.reward[1]
        print("You've recieved {0} XP and {1} GP for completing this quest.".format(self.reward[0], self.reward[1]))
        self.upon_completing()
        self.active = False


# Name: Philliard -- Town: Nearton
philliard_phrase_1 = Conversation(["Hello, adventurer!",
                                   "Welcome to the Kingdom of Pythonia."], active=True)
philliard = NPC('Philliard', [philliard_phrase_1])

# Name: Alfred -- Town: Nearton
alfred_phrase_1 = Conversation(["It is rumored that a mighty gel-creature lives south-east",
                                "of this very town. I'd be careful around there if I were you."], active=True)
alfred_phrase_2 = Conversation(["Come back here when you defeat the evil",
                               "Master Slime. Good luck!"])
alfred_phrase_3 = Conversation(["Greetings, Hero! Good luck on your adventures!"], repeat=True)

alfred_quest_1 = Quest(["...Actually, now that I think about it, do you think you could possibly",
                        "dispose of this vile creature? His location is 0'N, 1'E."], 'A Slimy Specimen',
                        ["Defeat the dreaded Master Slime at location 0'N, 1'E and then",
                        "return to Alfred in Nearton."], 'Alfred', [30, 50],
                        ["You defeated the evil Master Slime?!",
                        "Amazing! Take this, adventurer, you've earned it."], active=True)

def alfqst_us1():
    # Stands for "Alfred Quest 1 -- Upon Starting
    # Changes one of his dialogue options to reflect a quest beginning.
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

# Name: Wesley -- Town: Southford
wesley_phrase_1 = Conversation(["Adventurers around this area say that monsters tend",
                                "to be stronger the farther from 0'N, 0'E that you travel.",
                                "However, monsters there also give better loot. Be careful."], active=True)
wesley = NPC('Wesley', [wesley_phrase_1])

# Name: Stewson -- Town: Overshire
stewson_phrase_1 = Conversation(["Our amazing Kingdom has 6 different regions:",
                                "Tundra in the northwest, Swamp in the southeast,",
                                "Mountains in the northeast, and Desert in the southwest.",
                                "The Forest lies in the center, while the Beach surrounds them."], active=True)
stewson = NPC('Stewson', [stewson_phrase_1])

all_dialogue = [
    philliard_phrase_1,
    alfred_phrase_1, alfred_phrase_2, alfred_phrase_3, alfred_quest_1,
    stewson_phrase_1
    ]

def serialize_dialogue(path):
    json_dialogue = {}
    for c in all_dialogue:
        if isinstance(c, Quest):
            json_dialogue[str(c)] = [c.active, c.repeat, c.started, c.finished]
        else:
            json_dialogue[str(c)] = [c.active, c.repeat]
    with open(path, encoding='utf-8', mode='w') as h:
        json.dump(json_dialogue, h, indent=4, separators=(', ', ': '))

def deserialize_dialogue(path):
    global all_dialogue
    with open(path, encoding='utf-8', mode='r') as h:
        j_log = json.load(h)
    for key in j_log:
        for c in all_dialogue[:]:
            if key == str(c):
                if isinstance(c, Quest):
                    c.active, \
                    c.repeat, \
                    c.started, \
                    c.finished = \
                    j_log[key][0], \
                    j_log[key][1], \
                    j_log[key][2], \
                    j_log[key][3]
                else:
                    c.active, \
                    c.repeat = \
                    j_log[key][0], \
                    j_log[key][1]
