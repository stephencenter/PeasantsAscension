import sys
import json
import pets
import bosses

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
            print('-' * 25) if dialogue else ''
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
        self.desc = desc  # A brief summary of the goal of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.req_lvl = req_lvl  # The level that you must be at to begin the quest
        self.started = started  # is True if the quest has been started, false otherwise
        self.finished = finished  # is True if the quest is complete, false otherwise
        self.end_dialogue = end_dialogue  # What is printed when the quest is over

    def give_quest(self):
        print('-' * 25)
        print(''.join([self.name, ': \n  ', '\n  '.join([x for x in self.desc])]))
        print('-' * 25)
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
                print('-' * 25)
                print('{0}: "Terrific! Come see me when you are finished."'.format(self.q_giver))
                self.started = True
                self.upon_starting()
                return
            elif accept in ['no', 'n']:
                print('-' * 25)
                print('{0}: "...Oh. Come back later if you change your mind."'.format(self.q_giver))
                return

    def completion(self):
        main.player.exp += self.reward[0]
        main.static['gp'] += self.reward[1]
        print("You've received {0} XP and {1} GP for completing this quest.".format(self.reward[0], self.reward[1]))
        main.player.level_up()
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

# Name: Wesley -- Town: Southford
wesley_phrase_1 = Conversation(["Adventurers around this area say that monsters tend",
    "to be stronger the farther from 0'N, 0'E that you travel.",
    "However, monsters there also give better loot. Be careful."
                               ], active=True)
wesley = NPC('Wesley', [wesley_phrase_1])

# Name: Stewson -- Town: Overshire
stewson_phrase_1 = Conversation(["Our amazing Kingdom has 6 different regions:",
     "Tundra in the northwest, Swamp in the southeast,",
     "Mountains in the northeast, and Desert in the southwest.",
     "The Forest lies in the center, while the Beach surrounds them.",
     "There's a small region somewhere around here that is the",
     "cause of much worry and panic in this town: The Graveyard.",
     "Inside lies a dangerous aparrition, feared by all who have seen it.",
                                ], active=True)

stewson_phrase_2 = Conversation(["Please save us from this monsterous wraith!"])

stewson_phrase_3 = Conversation(["Thank you again for your help, adventurer!"])

stewson_quest_1 = Quest(["I wish someone would do something about this terrible",
    "ghost... Hey! You're a strong adventurer, perhaps you",
    "could defeat this phantom? It's at position 8'N, -12'W."],
    'The Shadowy Spirit', ["Defeat the feared Menacing Phantom at location",
    "8'N, -12'W and then return to Stewson in Overshire."], 'Stewson', [50, 75],
    ["You... you actually defeated it?! Thank you ever so much!",
     "Take this, it is the least our town can do for your bravery."], active=True)


def stwqst_us1():
    global stewson_phrase_1
    global stewson_phrase_2
    bosses.menac_phantom.active = True
    stewson_phrase_1.active = False
    stewson_phrase_2.active = True

def stwqst_uc1():
    global stewson_phrase_3
    stewson_phrase_3.active = True
    print('-'*25)
    if not main.player.current_pet:
        print('You have recieved a Cherub pet!')
        main.player.current_pet = pets.pet_cherub
    else:
        print('You are being offered a Cherub pet (Healer) by Stewson.')
        print('Accepting this pet will cause your current pet to be replaced.')
        while True:
            y_n = input('Replace your {0} pet with a pet Cherub (Healer)? | Yes or No: '.format(main.current_pet.name))
            try:
                y_n = y_n.lower()
            except AttributeError:
                continue
            if y_n.startswith('y'):
                print('You have recieved a Cherub pet!')
                main.player.current_pet = pets.pet_cherub
                return
            elif y_n.startswith('n'):
                print('You have declined the offer to recieve a Cherub pet.')
                return


stewson_quest_1.upon_starting = stwqst_us1
stewson_quest_1.upon_completing = stwqst_uc1

stewson = NPC('Stewson', [stewson_phrase_1, stewson_phrase_2, stewson_phrase_3, stewson_quest_1])

# Name: Ethos -- Town: Charsulville
ethos_phrase_1 = Conversation(['Any smart adventurer would keep track of town coordinates',
    'in his inventory. If you get lost, check there.', '...', 'Raisins!'], active=True)

ethos = NPC('Ethos', [ethos_phrase_1])

# Name: Seriph -- Town: Fort Sigil
seriph_phrase_1 = Conversation(['...You actually came to this town? And of your own',
    'free will, too?! You are either very brave or very stupid.'], active=True)

seriph = NPC('Seriph', [seriph_phrase_1])

# Name: Kyle -- Town: Tripton
kyle_phrase_1 = Conversation(["Those stupid Fallvillians need to get away from our",
    "land! It's they're fault they made a town that was so",
    "easy to miss! I don't care if we have to go to war",
    "with those dingbats, I'm not leaving this spot!"], active=True)

kyle = NPC('Kyle', [kyle_phrase_1])

# Name: Krystal -- Town: Fallville
krystal_phrase_1 = Conversation(["What I don't understand is that the silly",
    "Triptonians blame us for their poor eyesight. It's all",
    "their fault, and they know it! Besides, everything would be",
    "more peaceful if we'd just put this whole mistake of",
    "theirs behind us and get along."], active=True)

krystal = NPC('Krystal', [krystal_phrase_1])

all_dialogue = [
    philliard_phrase_1, wesley_phrase_1, seriph_phrase_1,
    alfred_phrase_1, alfred_phrase_2, alfred_phrase_3, alfred_quest_1,
    stewson_phrase_1, stewson_phrase_2, stewson_phrase_3, stewson_quest_1,
    kyle_phrase_1, krystal_phrase_1
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
    with open(path, encoding='utf-8') as h:
        j_log = json.load(h)
    for key in j_log:
        for c in all_dialogue[:]:
            if key == str(c):
                if isinstance(c, Quest):
                    c.active, c.repeat, c.started, c.finished = \
                        j_log[key][0], j_log[key][1], j_log[key][2], j_log[key][3]
                else:
                    c.active, c.repeat = j_log[key][0], j_log[key][1]
