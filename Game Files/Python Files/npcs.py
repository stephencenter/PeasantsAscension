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

        for convo in convo_list:
            if isinstance(convo, d.Quest):
                if convo.active and (convo.finished or not convo.started):
                    if convo.finished:
                        convo.completion()
                        continue

                    for sentence in main.chop_by_79(convo.dialogue):
                        main.s_input(sentence)

                    if not convo.started:
                        convo.give_quest()

            else:
                if convo.active:
                    for sentence in main.chop_by_79(convo.dialogue):
                        main.s_input(sentence)

                    convo.after_talking()

        print("-"*save_load.divider_size)


npc_solou = NPC("Solou", "Page",
                {
                    "nearton": [
                        d.solou_convo_a,
                        d.solou_convo_b,
                        d.solou_convo_c,
                        d.solou_quest_a,
                        d.solou_convo_d,
                        d.solou_convo_e
                    ]
                }, "npc_solou")

joseph = NPC('Joseph', "Mayor of Overshire",
             {
                 "overshire_city": [
                     d.joseph_convo_a,
                     d.joseph_quest_a,
                     d.joseph_convo_b,
                     d.joseph_convo_c
                 ],
             }, "npc_joseph")

orius = NPC("Orius", "Mayor of Valice", [], "npc_orius")

azura = NPC('Azura', "Sorcerers' Guildmaster",
            {
                "parceon": [
                    d.azura_convo_a,
                    d.azura_convo_b,
                    d.azura_convo_c
                ],
            }, "npc_azura")

raidon = NPC('Raidon', "Village Shaman", {"ambercreek": [d.raidon_convo_a]}, "npc_raidon")

stewson = NPC('Stewson', "Captain of the Guard",
              {
                  "sardooth": [
                      d.stewson_convo_a,
                      d.stewson_convo_b,
                      d.stewson_convo_c,
                      d.stewson_quest_a
                  ],
              }, "npc_stewson")

seriph = NPC('Seriph', "Blacksmith",
             {
                 "fort_sigil": [
                     d.seriph_convo_a,
                     d.seriph_convo_b,
                     d.seriph_convo_c
                 ],
             }, "npc_seriph")

rivesh = NPC('Rivesh', "Village Elder",
             {
                 "fort_sigil": [
                     d.rivesh_convo_a,
                     d.rivesh_convo_b,
                     d.rivesh_convo_c,
                     d.rivesh_convo_d,
                     d.rivesh_quest_a
                 ]
             }, "npc_rivesh")

alfred = NPC('Alfred', "Cobbler",
             {
                 "nearton": [
                    d.alfred_convo_a,
                    d.alfred_convo_b,
                    d.alfred_convo_c,
                    d.alfred_quest_a,
                    d.alfred_convo_d
                 ]
             }, "npc_alfred")

kyle = NPC('Kyle', "Village Elder",
           {
               "tripton": [
                   d.kyle_convo_a,
                   d.kyle_convo_b,
                   d.kyle_convo_c,
                   d.kyle_convo_d
               ],
           }, "npc_kyle")

krystin = NPC('Krystin', "Village Elder",
              {
                  "fallville": [
                      d.krystin_convo_a,
                      d.krystin_convo_b,
                      d.krystin_convo_c,
                      d.krystin_convo_d
                  ]
              }, "npc_krystin")

frederick = NPC('Frederick', "Scholar",
                {
                    "fallville": [
                        d.frederick_convo_a,
                        d.frederick_convo_b,
                        d.frederick_convo_c
                    ],
                }, "npc_frederick")

alden = NPC('Alden', "Sage",
            {
                "tripton": [
                    d.alden_quest_a,
                    d.alden_convo_a,
                    d.alden_convo_b,
                    d.alden_convo_c
                ]
            }, "npc_alden")

polmor = NPC('Polmor', "Engineer",
             {
                 "whistumn": [
                     d.polmor_convo_a,
                     d.polmor_quest_a,
                     d.polmor_convo_b
                 ],
             }, "npc_polmor")

serena = NPC('Serena', "Scientist",
             {
                 "whistumn": [
                     d.serena_convo_a,
                     d.serena_convo_b,
                     d.serena_convo_c
                 ],
             }, "npc_serena")

matthew = NPC('Matthew', "Matt",
              {
                  "lantonum": [
                      d.matthew_convo_a,
                      d.matthew_quest_a,
                      d.matthew_convo_b,
                      d.matthew_convo_c,
                      d.matthew_convo_d,
                      d.matthew_convo_e
                  ]
              }, "npc_matthew")

pime = NPC('Pime', "Vampire Shaman",
           {
               "sanguion": [
                   d.pime_convo_a,
                   d.pime_convo_b,
                   d.pime_quest_a,
                   d.pime_convo_c,
               ],
           }, "npc_pime")

philliard = NPC('Philliard', "Scribe", {"nearton": [d.philliard_convo_a]}, "npc_philliard")

wesley = NPC('Wesley', "Peasant", {"nearton": [d.wesley_convo_a]}, "npc_wesley")

saar = NPC("Saar", "Bard", {"southford": [d.saar_convo_a]}, "npc_saar")

lazaro = NPC('Lazaro', "Oracle", {"southford": [d.lazaro_convo_a]}, "npc_lazaro")

jeffery = NPC('Jeffery', "Traveler", {"overshire_city": [d.jeffery_convo_a]}, "npc_jeffery")

harthos = NPC("Harthos", "Lumberjack", {"overshire_city": [d.harthos_convo_a]}, "npc_harthos")

sondalar = NPC('Sondalar', "Goods Peddler", {"overshire_city": [d.sondalar_convo_a]}, "npc_sondalar")

# TODO Rework Sakura into a quest giver
sakura = NPC('Sakura', "Head of the Royal Guard", {"principalia": [d.sakura_convo_a]}, "npc_sakrura")

ethos = NPC('Ethos', "Courier", {"valice": [d.ethos_convo_a]}, "npc_ethos")

typhen = NPC('Typhen', "Novice Cleric", {"valice": [d.typhen_convo_a]}, "npc_typhen")

fly = NPC('Fly', "Duke of Celemia", {"new_ekanmar": [d.fly_convo_a]}, "npc_fly")

stravi = NPC('Stravi', "Duchess of Celemia", {"new_ekanmar": [d.stravi_convo_a]}, "npc_stravi")

caesar = NPC('Caesar', "Fly's Pet", {"new_ekanmar": [d.caesar_convo_a]}, "npc_caesar")

strathius = NPC("Strathius", "Druid", {"ravenstone": [d.strathius_convo_a]}, "npc_strathius")

sugulat = NPC('Sugulat', "Duke of Chin'tor",  {"ambercreek": [d.sugulat_convo_a]}, "npc_sugalat")

morrison = NPC('Morrison', "Engineer", {"cesura": [d.morrison_convo_a]}, "npc_morrison")

ariver = NPC('Ariver', "Vampire", {"sanguion": [d.ariver_convo_a]}, "npc_ariver")

fitzgerald = NPC("Fitzgerald", "Raving Alcoholic", {"valenfall": [d.fitz_convo_a]}, "npc_fitzgerald")
