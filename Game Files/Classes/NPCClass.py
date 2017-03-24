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

import save_load
import units

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
    def __init__(self, name, conversations, occupation, active=True):
        self.name = name
        self.conversations = conversations
        self.occupation = occupation
        self.active = active

    def __str__(self):
        return self.name

    def speak(self):
        # Print the NPC's dialogue to the player
        dialogue = []
        for w in self.conversations:
            if w.active:
                dialogue.append(w.chop())

        for y in dialogue[:]:
            # Create some padding so that everything lines up properly and looks nice
            padding = len(max(y, key=len))

            for z in y:
                input(z)

            dialogue.remove(y)

            if dialogue:
                print('-'*save_load.divider_size)

            for obj in self.conversations:
                if (isinstance(obj, Quest) and obj.end_dialogue == y) or obj.sentences == y:
                    y = obj

            if isinstance(y, Quest) and not y.started:
                y.give_quest()

            elif isinstance(y, Quest) and y.finished:
                y.completion()

            y.after_talking()


class Conversation:
    def __init__(self, dialogue, conv_id, active=False):
        self.dialogue = dialogue
        self.active = active
        self.conv_id = conv_id

    def chop(self):
        sentences = []
        current_sentence = ''

        for word in self.dialogue.split():
            if len(current_sentence + word) > 79:
                sentences.append(current_sentence)
                current_sentence = ''

            current_sentence += f' {word}'

        return sentences

    def after_talking(self):
        pass


class Quest(Conversation):
    def __init__(self, name, dialogue, q_giver, reward, conv_id, started=False, finished=False, active=False):
        Conversation.__init__(self, dialogue, active)
        self.name = name  # The name of the quest
        self.q_giver = q_giver  # The name of the person who gave you the quest
        self.reward = reward  # A list [experience, gold] of your reward for the quest
        self.started = started  # is True if the quest has been started, false otherwise
        self.finished = finished  # is True if the quest is complete, false otherwise
        self.conv_id = conv_id

    def give_quest(self):
        print('-'*save_load.divider_size)
        print(f'{self.q_giver} is offering you the quest "{self.name}".')

        while True:
            accept = input('Do you accept this quest? | Yes or No: ').lower()

            if accept.startswith('y'):
                print('-'*save_load.divider_size)
                print(f'{self.q_giver}: "Terrific! Thank you for your help!"')
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
        input('\nPress enter/return')

        main.party_info['gp'] += self.reward[1]
        units.player.exp += self.reward[0]
        units.player.level_up()

        self.active = False

    def upon_starting(self):
        pass

    def upon_completing(self):
        pass
