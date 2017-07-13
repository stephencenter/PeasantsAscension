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

import sys

import save_load
import dialogue as d

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
    def __init__(self, name, occupation, conversations, active=True):
        self.name = name
        self.occupation = occupation
        self.conversations = conversations

    def __str__(self):
        return self.name

    def speak(self):
        # Print the NPC's dialogue to the player
        print(f"{self.name}, the {self.occupation}:")
        for convo in [x for x in self.conversations if x.active]:
            for sentence in main.chop_by_79(convo.dialogue):
                main.s_input(f" {sentence}")

            if isinstance(convo, d.Quest) and not convo.started:
                convo.give_quest()

            elif isinstance(convo, d.Quest) and convo.finished:
                convo.completion()

            convo.after_talking()
            print('-'*save_load.divider_size)


npc_solou = NPC("Solou", "Page", [d.solou_convo_1, d.solou_convo_2, d.solou_convo_3, d.solou_quest_1])

joseph = NPC('Joseph', "Mayor of Overshire", [d.joseph_convo_1, d.joseph_quest_1, d.joseph_convo_2, d.joseph_convo_3])

orius = NPC("Orius", "Mayor of Charsulville", [])

azura = NPC('Azura', "Sorcerers' Guildmaster", [d.azura_convo_1, d.azura_convo_2, d.azura_convo_3])

raidon = NPC('Raidon', "Village Shaman", [d.raidon_convo_1])

stewson = NPC('Stewson', "Captain of the Guard", [d.stewson_convo_1, d.stewson_convo_2,
                                                  d.stewson_convo_3, d.stewson_quest_1])

seriph = NPC('Seriph', "Blacksmith", [d.seriph_convo_1, d.seriph_convo_2, d.seriph_convo_3])

rivesh = NPC('Rivesh', "Village Elder", [d.rivesh_convo_1, d.rivesh_convo_2, d.rivesh_convo_3,
                                         d.rivesh_convo_4, d.rivesh_quest_1])

alfred = NPC('Alfred', "Cobbler", [d.alfred_convo_1, d.alfred_convo_2, d.alfred_quest_1,
                                   d.alfred_convo_3, d.alfred_convo_4])

kyle = NPC('Kyle', "Village Elder", [d.kyle_convo_1, d.kyle_convo_2, d.kyle_convo_3, d.kyle_convo_4])

krystin = NPC('Krystin', "Village Elder", [d.krystin_convo_1, d.krystin_convo_2, d.krystin_convo_3, d.krystin_convo_4])

frederick = NPC('Frederick', "Scholar", [d.frederick_convo_1, d.frederick_convo_2, d.frederick_convo_3])

alden = NPC('Alden', "Sage", [d.alden_quest_1, d.alden_convo_1, d.alden_convo_2, d.alden_convo_3])

polmor = NPC('Polmor', "Engineer", [d.polmor_convo_1, d.polmor_quest_1, d.polmor_convo_2])

matthew = NPC('Matthew', "Interstellar Traveller", [d.matthew_convo_1, d.matthew_quest_1, d.matthew_convo_2,
                                                    d.matthew_convo_3, d.matthew_convo_4, d.matthew_convo_5])

pime = NPC('Pime', "Vampire Shaman", [d.pime_convo_1, d.pime_convo_2, d.pime_quest_1, d.pime_convo_3, d.pime_convo_4])

philliard = NPC('Philliard', "Scribe", [d.philliard_convo_1])

sondalar = NPC('Sondalar', "Goods Peddler", [d.sondalar_convo_1])

saar = NPC("Saar", "Bard", [d.saar_convo_1])

wesley = NPC('Wesley', "Peasant", [d.wesley_convo_1])

lazaro = NPC('Lazaro', "Oracle", [d.lazaro_convo_1])

typhen = NPC('Typhen', "Novice Cleric", [d.typhen_convo_1])

jeffery = NPC('Jeffery', "Gossipping Serf", [d.jeffery_convo_1])

harthos = NPC("Harthos", "Lumberjack", [d.harthos_convo_1])

ethos = NPC('Ethos', "Courier", [d.ethos_convo_1])

flysio = NPC('Flysio', "Baron of Celemia", [d.flysio_convo_1])

stravi = NPC('Stravi', "Flysio's Wife", [d.stravi_convo_1])

caesar = NPC('Caesar', "Flysio's Pet", [d.caesar_convo_1])

sakura = NPC('Sakura', "Head of the Royal Guard", [d.sakura_convo_1])

strathius = NPC("Strathius", "Druid", [d.strathius_convo_1])

sugulat = NPC('Sugulat', "Baron of Simphet", [d.sugulat_convo_1])

serena = NPC('Serena', "Scientist", [d.serena_convo_1, d.serena_convo_2, d.serena_convo_3])

morrison = NPC('Morrison', "Engineer", [d.morrison_convo_1])

ariver = NPC('Ariver', "Vampire", [d.ariver_convo_1])

fitzgerald = NPC("Fitzgerald the Drunk", "Raving Alcoholic", [d.fitz_convo_1])
