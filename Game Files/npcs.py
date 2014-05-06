import sys

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

class Conversation:
    def __init__(self, sentences, repeat=False, active=False):
        self.sentences = sentences
        self.repeat = repeat
        self.active = active


class NPC:
    def __init__(self, name, conversations):
        self.name = name
        self.conversations = conversations

    def speak(self):
        for x in self.conversations:
            if x.active and not x.repeat:
                dialogue = x.sentences
                break
        else:
            for y in self.conversations:
                if y.active and y.repeat:
                    dialogue = y.sentences
                    break

        for z in dialogue:
            input(self.name + ': "' + z + '" | Press enter/return ')


# Name: Philliard -- Town: Nearton
philliard_phrase_1 = Conversation(["Hello, adventurer!", "Welcome to the Kingdom of Pythonia."], active=True)
philliard = NPC('Philliard', [philliard_phrase_1])

# Name: Alfred -- Town: Nearton
alfred_phrase_1 = Conversation(["It is rumored that a mighty gel-creature lives south-east of this very town.",
                                "I'd be careful around there if I were you."], active=True)
alfred = NPC('Alfred', [alfred_phrase_1])

# Name: Wesley -- Town: Southford
wesley_phrase_1 = Conversation(["""Adventurers around this area say that monsters tend
to be stronger the farther from 0'N, 0'E that you travel."""], active=True)
wesley = NPC('Wesley', [wesley_phrase_1])

