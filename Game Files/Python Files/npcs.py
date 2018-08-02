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
                        d.all_dialogue[d.solou_convo_a.conv_id],
                        d.all_dialogue[d.solou_convo_b.conv_id],
                        d.all_dialogue[d.solou_convo_c.conv_id],
                        d.all_dialogue[d.solou_quest_a.conv_id],
                        d.all_dialogue[d.solou_convo_d.conv_id],
                        d.all_dialogue[d.solou_convo_e.conv_id]
                    ]
                }, "npc_solou")

joseph = NPC('Joseph', "Mayor of Overshire",
             {
                 "overshire_city": [
                     d.all_dialogue[d.joseph_convo_a.conv_id],
                     d.all_dialogue[d.joseph_quest_a.conv_id],
                     d.all_dialogue[d.joseph_convo_b.conv_id],
                     d.all_dialogue[d.joseph_convo_c.conv_id]
                 ],
             }, "npc_joseph")

orius = NPC("Orius", "Mayor of Valice", [], "npc_orius")

azura = NPC('Azura', "Sorcerers' Guildmaster",
            {
                "parceon": [
                    d.all_dialogue[d.azura_convo_a.conv_id],
                    d.all_dialogue[d.azura_convo_b.conv_id],
                    d.all_dialogue[d.azura_convo_c.conv_id]
                ],
            }, "npc_azura")

raidon = NPC('Raidon', "Village Shaman",
             {
                 "ambercreek": [
                     d.all_dialogue[d.raidon_convo_a.conv_id]
                 ]
             }, "npc_raidon")

stewson = NPC('Stewson', "Captain of the Guard",
              {
                  "sardooth": [
                      d.all_dialogue[d.stewson_convo_a.conv_id],
                      d.all_dialogue[d.stewson_convo_b.conv_id],
                      d.all_dialogue[d.stewson_convo_c.conv_id],
                      d.all_dialogue[d.stewson_quest_a.conv_id]
                  ],
              }, "npc_stewson")

seriph = NPC('Seriph', "Blacksmith",
             {
                 "fort_sigil": [
                     d.all_dialogue[d.seriph_convo_a.conv_id],
                     d.all_dialogue[d.seriph_convo_b.conv_id],
                     d.all_dialogue[d.seriph_convo_c.conv_id]
                 ],
             }, "npc_seriph")

rivesh = NPC('Rivesh', "Village Elder",
             {
                 "fort_sigil": [
                     d.all_dialogue[d.rivesh_convo_a.conv_id],
                     d.all_dialogue[d.rivesh_convo_b.conv_id],
                     d.all_dialogue[d.rivesh_convo_c.conv_id],
                     d.all_dialogue[d.rivesh_convo_d.conv_id],
                     d.all_dialogue[d.rivesh_quest_a.conv_id]
                 ]
             }, "npc_rivesh")

alfred = NPC('Alfred', "Cobbler",
             {
                 "nearton": [
                    d.all_dialogue[d.alfred_convo_a.conv_id],
                    d.all_dialogue[d.alfred_convo_b.conv_id],
                    d.all_dialogue[d.alfred_convo_c.conv_id],
                    d.all_dialogue[d.alfred_quest_a.conv_id],
                    d.all_dialogue[d.alfred_convo_d.conv_id]
                 ]
             }, "npc_alfred")

kyle = NPC('Kyle', "Village Elder",
           {
               "tripton": [
                   d.all_dialogue[d.kyle_convo_a.conv_id],
                   d.all_dialogue[d.kyle_convo_b.conv_id],
                   d.all_dialogue[d.kyle_convo_c.conv_id],
                   d.all_dialogue[d.kyle_convo_d.conv_id]
               ],
           }, "npc_kyle")

krystin = NPC('Krystin', "Village Elder",
              {
                  "fallville": [
                      d.all_dialogue[d.krystin_convo_a.conv_id],
                      d.all_dialogue[d.krystin_convo_b.conv_id],
                      d.all_dialogue[d.krystin_convo_c.conv_id],
                      d.all_dialogue[d.krystin_convo_d.conv_id]
                  ]
              }, "npc_krystin")

frederick = NPC('Frederick', "Scholar",
                {
                    "fallville": [
                        d.all_dialogue[d.frederick_convo_a.conv_id],
                        d.all_dialogue[d.frederick_convo_b.conv_id],
                        d.all_dialogue[d.frederick_convo_c.conv_id]
                    ],
                }, "npc_frederick")

alden = NPC('Alden', "Sage",
            {
                "tripton": [
                    d.all_dialogue[d.alden_quest_a.conv_id],
                    d.all_dialogue[d.alden_convo_a.conv_id],
                    d.all_dialogue[d.alden_convo_b.conv_id],
                    d.all_dialogue[d.alden_convo_c.conv_id]
                ]
            }, "npc_alden")

polmor = NPC('Polmor', "Engineer",
             {
                 "whistumn": [
                     d.all_dialogue[d.polmor_convo_a.conv_id],
                     d.all_dialogue[d.polmor_quest_a.conv_id],
                     d.all_dialogue[d.polmor_convo_b.conv_id]
                 ],
             }, "npc_polmor")

serena = NPC('Serena', "Scientist",
             {
                 "whistumn": [
                     d.all_dialogue[d.serena_convo_a.conv_id],
                     d.all_dialogue[d.serena_convo_b.conv_id],
                     d.all_dialogue[d.serena_convo_c.conv_id]
                 ],
             }, "npc_serena")

matthew = NPC('Matthew', "Matt",
              {
                  "lantonum": [
                      d.all_dialogue[d.matthew_convo_a.conv_id],
                      d.all_dialogue[d.matthew_quest_a.conv_id],
                      d.all_dialogue[d.matthew_convo_b.conv_id],
                      d.all_dialogue[d.matthew_convo_c.conv_id],
                      d.all_dialogue[d.matthew_convo_d.conv_id],
                      d.all_dialogue[d.matthew_convo_e.conv_id]
                  ]
              }, "npc_matthew")

pime = NPC('Pime', "Vampire Shaman",
           {
               "sanguion": [
                   d.all_dialogue[d.pime_convo_a.conv_id],
                   d.all_dialogue[d.pime_convo_b.conv_id],
                   d.all_dialogue[d.pime_quest_a.conv_id],
                   d.all_dialogue[d.pime_convo_c.conv_id],
               ],
           }, "npc_pime")

philliard = NPC('Philliard', "Scribe",
                {
                    "nearton": [
                        d.all_dialogue[d.philliard_convo_a.conv_id]
                    ]
                }, "npc_philliard")

wesley = NPC('Wesley', "Peasant",
             {
                 "nearton": [
                     d.all_dialogue[d.wesley_convo_a.conv_id]
                 ]
             }, "npc_wesley")

saar = NPC("Saar", "Bard",
           {
               "southford": [
                   d.all_dialogue[d.saar_convo_a.conv_id]
               ]
           }, "npc_saar")

lazaro = NPC('Lazaro', "Oracle",
             {
                 "southford": [
                     d.all_dialogue[d.lazaro_convo_a.conv_id]
                 ]
             }, "npc_lazaro")

jeffery = NPC('Jeffery', "Traveler",
              {
                  "overshire_city": [
                      d.all_dialogue[d.jeffery_convo_a.conv_id]
                  ]
              }, "npc_jeffery")

harthos = NPC("Harthos", "Lumberjack",
              {
                  "overshire_city": [
                      d.all_dialogue[d.harthos_convo_a.conv_id]
                  ]
              }, "npc_harthos")

sondalar = NPC('Sondalar', "Goods Peddler",
               {
                   "overshire_city": [
                       d.all_dialogue[d.sondalar_convo_a.conv_id]
                   ]
               }, "npc_sondalar")

# TODO Rework Sakura into a quest giver
sakura = NPC('Sakura', "Head of the Royal Guard",
             {
                 "principalia": [
                     d.all_dialogue[d.sakura_convo_a.conv_id]
                 ]
             }, "npc_sakrura")

ethos = NPC('Ethos', "Courier",
            {
                "valice": [
                    d.all_dialogue[d.ethos_convo_a.conv_id]
                ]
            }, "npc_ethos")

typhen = NPC('Typhen', "Novice Cleric",
             {
                 "valice": [
                     d.all_dialogue[d.typhen_convo_a.conv_id]
                 ]
             }, "npc_typhen")

fly = NPC('Fly', "Duke of Celemia",
          {
              "new_ekanmar": [
                  d.all_dialogue[d.fly_convo_a.conv_id]
              ]
          }, "npc_fly")

stravi = NPC('Stravi', "Duchess of Celemia",
             {
                 "new_ekanmar": [
                     d.all_dialogue[d.stravi_convo_a.conv_id]
                 ]
             }, "npc_stravi")

caesar = NPC('Caesar', "Fly's Pet",
             {
                 "new_ekanmar": [
                     d.all_dialogue[d.caesar_convo_a.conv_id]
                 ]
             }, "npc_caesar")

strathius = NPC("Strathius", "Druid",
                {
                    "ravenstone": [
                        d.all_dialogue[d.strathius_convo_a.conv_id]
                    ]
                }, "npc_strathius")

sugulat = NPC('Sugulat', "Duke of Chin'tor",
              {
                  "ambercreek": [
                      d.all_dialogue[d.sugulat_convo_a.conv_id]
                  ]
              }, "npc_sugalat")

morrison = NPC('Morrison', "Engineer",
               {
                   "cesura": [
                       d.all_dialogue[d.morrison_convo_a.conv_id]
                   ]
               }, "npc_morrison")

ariver = NPC('Ariver', "Vampire",
             {
                 "sanguion": [
                     d.all_dialogue[d.ariver_convo_a.conv_id]
                 ]
             }, "npc_ariver")

fitzgerald = NPC("Fitzgerald", "Raving Alcoholic",
                 {
                     "valenfall": [
                         d.all_dialogue[d.fitz_convo_a.conv_id]
                     ]
                 }, "npc_fitzgerald")
