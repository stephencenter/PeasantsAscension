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

import dialogue as d
import save_load

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
    def __init__(self, name, occupation, conversations, npc_id, active=True):
        self.name = name
        self.occupation = occupation
        self.convos = conversations
        self.active = active
        self.npc_id = npc_id

    def speak(self):
        # Print the NPC's dialogue to the player
        print(f"{self.name}, the {self.occupation}:")

        convo_list = self.convos[main.party_info['current_town']]

        for convo in [x for x in convo_list if not isinstance(x, d.Quest) and x.active]:
            for sentence in main.chop_by_79(convo.dialogue):
                main.s_input(sentence)

            convo.after_talking()

        for convo in [x for x in convo_list if isinstance(x, d.Quest) and x.active]:
            if isinstance(convo, d.Quest) and convo.finished:
                convo.completion()

            for sentence in main.chop_by_79(convo.dialogue):
                main.s_input(sentence)

            if isinstance(convo, d.Quest) and not convo.started:
                convo.give_quest()

        print('-'*save_load.divider_size)


npc_solou = NPC("Solou", "Page",
                {
                    "nearton": [
                        d.solou_convo_1,
                        d.solou_quest_1
                    ]
                }, "npc_solou")

joseph = NPC('Joseph', "Mayor of Overshire",
             {
                 "overshire_city": [
                     d.joseph_convo_1,
                     d.joseph_quest_1,
                     d.joseph_convo_2,
                     d.joseph_convo_3
                 ],
             }, "npc_joseph")

orius = NPC("Orius", "Mayor of Valice", [], "npc_orius")

azura = NPC('Azura', "Sorcerers' Guildmaster",
            {
                "parceon": [
                    d.azura_convo_1,
                    d.azura_convo_2,
                    d.azura_convo_3
                ],
            }, "npc_azura")

raidon = NPC('Raidon', "Village Shaman", {"ambercreek": [d.raidon_convo_1]}, "npc_raidon")

stewson = NPC('Stewson', "Captain of the Guard",
              {
                  "overshire_city": [
                      d.stewson_convo_1,
                      d.stewson_convo_2,
                      d.stewson_convo_3,
                      d.stewson_quest_1
                  ],
              }, "npc_stewson")

seriph = NPC('Seriph', "Blacksmith",
             {
                 "fort_sigil": [
                     d.seriph_convo_1,
                     d.seriph_convo_2,
                     d.seriph_convo_3
                 ],
             }, "npc_seriph")

rivesh = NPC('Rivesh', "Village Elder",
             {
                 "fort_sigil": [
                     d.rivesh_convo_1,
                     d.rivesh_convo_2,
                     d.rivesh_convo_3,
                     d.rivesh_convo_4,
                     d.rivesh_quest_1
                 ]
             }, "npc_rivesh")

alfred = NPC('Alfred', "Cobbler",
             {
                 "nearton": [
                    d.alfred_convo_1,
                    d.alfred_convo_2,
                    d.alfred_quest_1,
                    d.alfred_convo_3,
                    d.alfred_convo_4
                 ]
             }, "npc_alfred")

kyle = NPC('Kyle', "Village Elder",
           {
               "tripton": [
                   d.kyle_convo_1,
                   d.kyle_convo_2,
                   d.kyle_convo_3,
                   d.kyle_convo_4
               ],
           }, "npc_kyle")

krystin = NPC('Krystin', "Village Elder",
              {
                  "fallville": [
                      d.krystin_convo_1,
                      d.krystin_convo_2,
                      d.krystin_convo_3,
                      d.krystin_convo_4
                  ]
              }, "npc_krystin")

frederick = NPC('Frederick', "Scholar",
                {
                    "fallville": [
                        d.frederick_convo_1,
                        d.frederick_convo_2,
                        d.frederick_convo_3
                    ],
                }, "npc_frederick")

alden = NPC('Alden', "Sage",
            {
                "tripton": [
                    d.alden_quest_1,
                    d.alden_convo_1,
                    d.alden_convo_2,
                    d.alden_convo_3
                ]
            }, "npc_alden")

polmor = NPC('Polmor', "Engineer",
             {
                 "whistumn": [
                     d.polmor_convo_1,
                     d.polmor_quest_1,
                     d.polmor_convo_2
                 ],
             }, "npc_polmor")

serena = NPC('Serena', "Scientist",
             {
                 "whistumn": [
                     d.serena_convo_1,
                     d.serena_convo_2,
                     d.serena_convo_3
                 ],
             }, "npc_serena")

matthew = NPC('Matthew', "Matt",
              {
                  "lantonum": [
                      d.matthew_convo_1,
                      d.matthew_quest_1,
                      d.matthew_convo_2,
                      d.matthew_convo_3,
                      d.matthew_convo_4,
                      d.matthew_convo_5
                  ]
              }, "npc_matthew")

pime = NPC('Pime', "Vampire Shaman",
           {
               "sanguion": [
                   d.pime_convo_1,
                   d.pime_convo_2,
                   d.pime_quest_1,
                   d.pime_convo_3,
                   d.pime_convo_4
               ],
           }, "npc_pime")

philliard = NPC('Philliard', "Scribe", {"nearton": [d.philliard_convo_1]}, "npc_philliard")

sondalar = NPC('Sondalar', "Goods Peddler", {"southford": [d.sondalar_convo_1]}, "npc_sondalar")

saar = NPC("Saar", "Bard", {"nearton": [d.saar_convo_1]}, "npc_saar")

wesley = NPC('Wesley', "Peasant", {"southford": [d.wesley_convo_1]}, "npc_wesley")

lazaro = NPC('Lazaro', "Oracle", {"southford": [d.lazaro_convo_1]}, "npc_lazaro")

typhen = NPC('Typhen', "Novice Cleric", {"valice": [d.typhen_convo_1]}, "npc_typhen")

jeffery = NPC('Jeffery', "Gossipping Serf", {"overshire_city": [d.jeffery_convo_1]}, "npc_jeffery")

harthos = NPC("Harthos", "Lumberjack", {"overshire_city": [d.harthos_convo_1]}, "npc_harthos")

ethos = NPC('Ethos', "Courier", {"valice": [d.ethos_convo_1]}, "npc_ethos")

fly = NPC('Fly', "Duke of Celemia", {"new_ekanmar": [d.fly_convo_1]}, "npc_fly")

stravi = NPC('Stravi', "Duchess of Celemia", {"new_ekanmar": [d.stravi_convo_1]}, "npc_stravi")

caesar = NPC('Caesar', "Fly's Pet", {"new_ekanmar": [d.caesar_convo_1]}, "npc_caesar")

sakura = NPC('Sakura', "Head of the Royal Guard", {"principalia": [d.sakura_convo_1]}, "npc_sakrura")

strathius = NPC("Strathius", "Druid", {"ravenstone": [d.strathius_convo_1]}, "npc_strathius")

sugulat = NPC('Sugulat', "Duke of Chin'tor",  {"ambercreek": [d.sugulat_convo_1]}, "npc_sugalat")

morrison = NPC('Morrison', "Engineer", {"cesura": [d.morrison_convo_1]}, "npc_morrison")

ariver = NPC('Ariver', "Vampire", {"sanguion": [d.ariver_convo_1]}, "npc_ariver")

fitzgerald = NPC("Fitzgerald", "Raving Alcoholic", {"valenfall": [d.fitz_convo_1]}, "npc_fitzgerald")
