import sys
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
        dialogue = []
        for w in self.conversations:
            if w.active and not w.repeat:
                try:
                    if not w.started:
                        dialogue.append(w.sentences)
                except AttributeError:
                    dialogue.append(w.sentences)
        else:
            for x in self.conversations:
                if x.active and x.repeat:
                    dialogue.append(x.sentences)
                    break
        for y in dialogue[:]:
            for z in y:
                input(self.name + ': "' + z + '" | Press enter/return ')
            dialogue.remove(y)
            print('-'*25) if dialogue else ''
            for obj in self.conversations:
                if obj.sentences == y:
                    y = obj
            if isinstance(y, Quest) and not y.started:
                obj.give_quest()


class Conversation:
    def __init__(self, sentences, repeat=False, active=False):
        self.sentences = sentences
        self.repeat = repeat
        self.active = active


class Quest(Conversation):
    def __init__(self, sentences, name, desc, q_giver, reward, req_lvl=1,
                 started=False, finished=False, repeat=False, active=False):
        Conversation.__init__(self, sentences, repeat, active)
        self.name = name
        self.desc = desc
        self.q_giver = q_giver
        self.req_lvl = req_lvl
        self.started = started
        self.finished = finished

    def give_quest(self):
        print('-'*25)
        print(''.join([self.name, ': \n  ', '\n  '.join([x for x in self.desc])]))
        print('-'*25)
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


# Name: Philliard -- Town: Nearton
philliard_phrase_1 = Conversation(["Hello, adventurer!",
                                   "Welcome to the Kingdom of Pythonia."], active=True)
philliard = NPC('Philliard', [philliard_phrase_1])

# Name: Alfred -- Town: Nearton
alfred_phrase_1 = Conversation(["It is rumored that a mighty gel-creature lives south-east",
                                "of this very town. I'd be careful around there if I were you."], active=True)
alfred_phrase_2 = Conversation(["Come back here when you defeat the evil",
                               "Master Slime. Good luck!"])
alfred_quest_1 = Quest(["...Actually, now that I think about it, do you think you could possibly",
                        "dispose of this vile creature? His location is 0'N, 1'E."], 'A Slimy Specimen',
                        ["Defeat the dreaded Master Slime at location 0'N, 1'E and then",
                        "return to Alfred in Nearton."], 'Alfred', [30, 50], active=True)


def alfqst_us1():
    # Stands for "Alfred Quest 1 -- Upon start
    # Changes one of his dialogue options to reflect a quest beginning.
    global alfred_phrase_1
    global alfred_phrase_2
    bosses.master_slime.active = True
    alfred_phrase_1.active = False
    alfred_phrase_2.active = True


alfred_quest_1.upon_starting = alfqst_us1
alfred = NPC('Alfred', [alfred_phrase_1, alfred_phrase_2, alfred_quest_1])

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
