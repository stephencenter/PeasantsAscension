#   This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
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

import copy
import json
import math
import random
import re
import sys

import pygame

import abilities
import ascii_art
import battle
import inv_system
import items
import magic
import npcs
import save_load
import sounds

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

battle_options = """Pick {0}'s Move:
      [1] Standard Attack
      [2] Use Magic
      [3] Use Abilities
      [4] Use Items
      [5] Run"""


class Unit:
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad):
        self.name = name          # Name
        self.hp = hp              # Health
        self.mp = mp              # Mana Points
        self.attk = attk          # Attack
        self.dfns = dfns          # Defense
        self.p_attk = p_attk      # Pierce Attack
        self.p_dfns = p_dfns      # Pierce Defense
        self.m_attk = m_attk      # Magic Attack
        self.m_dfns = m_dfns      # Magic Defense
        self.spd = spd            # Speed
        self.evad = evad          # Evasion
        self.lvl = 1              # Level
        self.element = 'none'     # Player's Element
        self.status_ail = 'none'  # Current Status Ailment

        self.max_hp = copy.copy(self.hp)
        self.max_mp = copy.copy(self.mp)


class PlayableCharacter(Unit):
    # A class for characters whose main.s_input can be directly controlled by the player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad, class_='', enabled=True):
        Unit.__init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)

        self.class_ = class_      # PCU's Class
        self.element = 'none'     # PCU's Element
        self.status_ail = 'none'  # Current Status Ailment
        self.enabled = enabled    # Whether the PCU has been recruited or not
        self.exp = 0              # Experience
        self.extra_sp = 0         # Extra Skill Points
        self.ext_gol = 0          # Extra Gold Pieces
        self.ext_exp = 0          # Extra Experience
        self.req_xp = 3           # Required XP to level up
        self.move = ''            # What move the character chose during battle
        self.ap = 10              # The number of "Action Points" that the user has remaining
        self.max_ap = 10          # The number of maximum Action Points the user can have at one time

        self.target = Monster('', '', '', '', '', '', '', '', '', '', '')  # The target of the PCU's current action
        self.c_ability = abilities.Ability('', '', '')  # The ability that the PCU is currently casting
        self.c_spell = magic.Spell('', '', '', '', '', '')  # The spell that the PCU is currently casting

        self.attributes = {'int': 1,  # Intelligence, for Mages
                           'wis': 1,  # Wisdom, for Paladins
                           'str': 1,  # Strength, for Warriors
                           'con': 1,  # Constitution, for Monks
                           'dex': 1,  # Dexterity, for Assassins
                           'per': 1,  # Perception, for Rangers
                           'for': 1}  # Fortune

        self.ability_vars = {}  # This dictionary will contain numerous variables that interact with abilties in battle

    def choose_name(self):
        while True:
            # Ask the player for their name, and remove any pipe characters from it
            choice = main.s_input('What is your name, young adventurer? | Input Name: ')

            if not ''.join(choice.split()):
                continue

            temp_name = re.sub('[^\w\-_ ]', '', choice)

            for x, y in enumerate(temp_name):
                try:
                    if not (y == ' ' and temp_name[x + 1] == ' '):
                        self.name = ''.join([self.name, y])

                except IndexError:
                    pass

            if self.name[0] == ' ':
                self.name = self.name[1:]

            if not ''.join(self.name.split()) and ''.join(choice.split()):
                continue

            if self.name.lower() in ["flygon jones", "apollo kalar", "cynder887"]:
                print(f"Ah, {self.name}! My dear friend, it is great to see you again!")
                main.s_input('\nPress enter/return ')
                print('-'*save_load.divider_size)

                return

            while True:
                y_n = main.s_input(f'So, your name is {self.name}? | Y/N: ').lower()

                if y_n.startswith('y'):
                    print('-'*save_load.divider_size)
                    return

                elif y_n.startswith('n'):
                    self.name = ''
                    print()

                    break

    def choose_class(self):
        while True:
            class_ = main.s_input(f"""{self.name}, which class would you like to train as?
      [1] Mage: Master of the arcane arts capable of using all spells, but has low defense.
      [2] Assassin: Deals damage quickly and has high speed and evasion. Can poison foes.
      [3] Ranger: An evasive long-distance fighter who uses bows and deals pierce damage.
      [4] Paladin: Heavy-armor user who excels at holy and healing magic and uses hammers.
      [5] Monk: A master of unarmed combat. High evasion and capable of using buff spells.
      [6] Warrior: High defense stats and attack. Can tank lots of hits with its high HP.
Input [#]: """)

            try:
                class_ = {'1': "mage",
                          '2': "assassin",
                          '3': "ranger",
                          '4': "paladin",
                          '5': "monk",
                          '6': "warrior"}[class_]

                class_desc = {'mage': """\
    -Can use abilities that scale off Intelligence
    -Capable of learning every spell
    -Magic damage scales with equipped weapon
    -Deals Pierce Damage with Standard Attacks
    -Deals 50% damage with Standard Attacks
    -High Magic Attack, Magic Defense, and MP
    -Average HP, Speed, and Evasion
    -Low Pierce/Physical Attack and Pierce/Physical Defense""",

                              'assassin': """\
    -Can use abilities that scale off Dexterity
    -Physical damage scales with equipped weapon
    -Deals Physical Damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -High Speed and Physical Attack
    -Above-average Evasion
    -Average HP, Pierce Defense, and Physical Defense
    -Low Magic Defense, MP, and Magic Attack""",

                              'ranger': """\
    -Can use abilities that scale off Perception
    -Pierce Damage scales with equipped weapon
    -Deals Pierce Damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -High Pierce Attack and Evasion
    -Above-average Speed
    -Average MP, HP, and Pierce Defense
    -Low Defense and Magic Attack""",

                              'paladin': """\
    -Can use abilities that scale off Wisdom
    -Bonus healing from spells is 4*Wisdom instead of 2*Wisdom
    -Can learn all Healing spells and offensive Light spells
    -Physical Damage scales with equipped weapon
    -Deals Physical Damage with Standard Attacks
    -Above-average HP, Physical/Pierce/Magic defense, and Physical Attack
    -Average Magic-attack and MP
    -Low Speed and Evasion""",

                              'monk': """\
    -Can use abilities that scale off Constitution
    -Capable of learning all Buff spells
    -Physical damage scales with equipped weapon
    -Deals Physical damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -Above-average Physical Attack, Speed, Evasion, and HP
    -Average MP and Magical Attack
    -Low Pierce Defense and Physical Defense""",

                              'warrior': """\
    -Can use abilities that scale off Strength
    -Physical damage scales with equipped weapon
    -Deals Physical Damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -High Pierce Defense, Physical Attack and Defense, and HP
    -Low Magic Attack and Defense, Low Speed and Evasion, and Low MP"""}[class_]

            except KeyError:
                continue

            print('-'*save_load.divider_size)
            print(f"Information about {class_.title()}s: ")
            print(class_desc)
            print('-'*save_load.divider_size)

            while True:
                y_n = main.s_input(f'You wish to be of the {class_.title()} class? | Y/N: ').lower()

                if y_n.startswith('y'):
                    print('-'*save_load.divider_size)
                    self.class_ = class_

                    return

                elif y_n.startswith('n'):
                    print()
                    break

    def level_up(self):
        if self.exp >= self.req_xp:
            print()

            pygame.mixer.music.load('Content/Music/Adventures in Pixels.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(save_load.music_vol)

            # The player restores all their health and mana when they level up
            self.hp = copy.copy(self.max_hp)
            self.mp = copy.copy(self.max_mp)
            self.status_ail = 'none'

            rem_points = 0  # Remaining Skill Points
            extra_points = 0  # The number of extra skill points the player will receive

            if self.exp >= self.req_xp:
                print("-"*save_load.divider_size)

            while self.exp >= self.req_xp:
                self.lvl += 1
                print(f"{self.name} has advanced to level {self.lvl}!")

                rem_points += 5
                extra_points += self.extra_sp
                magic.new_spells(self)

                if self.class_ == 'warrior':
                    self.p_dfns += 4
                    self.attk += 4
                    self.dfns += 4
                    self.m_attk += 1
                    self.m_dfns += 1
                    self.spd += 1
                    self.evad += 1
                    self.hp += 4
                    self.mp += 1

                elif self.class_ == 'mage':
                    self.p_dfns += 1
                    self.attk += 1
                    self.dfns += 1
                    self.m_attk += 4
                    self.m_dfns += 4
                    self.spd += 2
                    self.evad += 2
                    self.hp += 2
                    self.mp += 4

                elif self.class_ == 'assassin':
                    self.p_dfns += 2
                    self.attk += 4
                    self.dfns += 2
                    self.m_attk += 1
                    self.m_dfns += 1
                    self.spd += 5
                    self.evad += 3
                    self.hp += 2
                    self.mp += 1

                elif self.class_ == 'ranger':
                    self.p_attk += 4
                    self.p_dfns += 2
                    self.dfns += 1
                    self.m_attk += 1
                    self.m_dfns += 2
                    self.spd += 3
                    self.evad += 4
                    self.hp += 2
                    self.mp += 2

                elif self.class_ == 'monk':
                    self.p_dfns += 1
                    self.attk += 4
                    self.dfns += 1
                    self.m_attk += 2
                    self.m_dfns += 2
                    self.spd += 3
                    self.evad += 3
                    self.hp += 3
                    self.mp += 2

                elif self.class_ == 'paladin':
                    self.p_dfns += 3
                    self.attk += 3
                    self.dfns += 3
                    self.m_attk += 2
                    self.m_dfns += 3
                    self.spd += 1
                    self.evad += 1
                    self.hp += 3
                    self.mp += 2

                self.exp -= self.req_xp
                self.req_xp = math.ceil((math.pow(self.lvl*2, 2) - self.lvl))

                fix_stats()

            print('-'*save_load.divider_size)
            self.skill_points(rem_points, extra_points)

            self.max_hp = copy.copy(self.hp)
            self.max_mp = copy.copy(self.mp)

            print('-'*save_load.divider_size)
            save_load.save_game()

            return

    def skill_points(self, rem_points, extra_points):
        if extra_points:
            print(f"{self.name}'s great fortune has granted them {extra_points} additional skill points!")
            rem_points += extra_points

        while rem_points > 0:
            print(f"{self.name} has {rem_points} skill point{'s' if rem_points > 1 else ''} left to spend.")

            skill = main.s_input("""Choose a skill to increase:
      [I]ntelligence - The attribute of Mages. Increases magic stats and MP.
      [W]isdom - The attribute of Paladins. Improves healing spells and increases MP.
      [S]trength -  The attribute of Warriors. Increases physical attack and defense.
      [C]onstitution - The attribute of Monks. Increases defensive stats and HP.
      [D]exterity - The attribute of Assassins. Increases evasion, speed and physical attack.
      [P]erception - The attribute of Rangers. Increases pierce stats and evasion.
      [F]ortune - No class affiliation. Increases GP, XP, and Skill Point gain.
Input [L]etter: """)

            skill = skill.lower()

            if any(map(skill.startswith, ['i', 'w', 's', 'c', 'd', 'p', 'f'])):
                if skill.startswith('i'):
                    act_skill = 'int'
                    vis_skill = 'Intelligence'

                elif skill.startswith('w'):
                    act_skill = 'wis'
                    vis_skill = 'Wisdom'

                elif skill.startswith('s'):
                    act_skill = 'str'
                    vis_skill = 'Strength'

                elif skill.startswith('c'):
                    act_skill = 'con'
                    vis_skill = 'Constitution'

                elif skill.startswith('d'):
                    act_skill = 'dex'
                    vis_skill = 'Dexterity'

                elif skill.startswith('p'):
                    act_skill = 'per'
                    vis_skill = 'Perception'

                else:
                    act_skill = 'for'
                    vis_skill = 'Fortune'

                print('-'*save_load.divider_size)
                print(f'Current {vis_skill}: {self.attributes[act_skill]}')

                if self.extra_sp == 10 and act_skill == 'for':
                    print(f"{self.name}'s additional skill points from Fortune has already reached the maximum of 10.")
                    print("Instead, upgrading Fortune will provide 2x the extra experience and gold from enemies.")

                while True:
                    y_n = main.s_input(f"Increase {self.name}'s {vis_skill}? | Y/N: ")
                    y_n = y_n.lower()

                    if not (y_n.startswith('y') or y_n.startswith('n')):
                        continue

                    if y_n.startswith('n'):
                        print('-'*save_load.divider_size)
                        break

                    if any(map(skill.startswith, ['d', 'c', 'i', 'w', 'p', 'f', 's'])):
                        self.increase_attribute(skill)

                    else:
                        continue

                    print('-'*save_load.divider_size)
                    print(f"{self.name}'s {vis_skill} has increased!")

                    # Decrement remaining points
                    rem_points -= 1

                    print('-'*save_load.divider_size) if rem_points else ''

                    break

        print(f'\n{self.name} is out of skill points.')

    def player_info(self):
        inv_name = self.name if self != player else 'player'
        fix_stats()

        print(f"""-{self.name}'s Stats-
Level: {self.lvl} | Class: {self.class_.title()} | Element: {self.element.title()}
HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp} | Status Ailment: {self.status_ail.upper()}
Attack: {self.attk} | M. Attack: {self.m_attk} | P. Attack {self.p_attk}
Defense: {self.dfns} | M. Defense: {self.m_dfns} | P. Defense {self.p_dfns}
Speed: {self.spd} | Evasion: {self.evad}
INT: {self.attributes['int']} | WIS: {self.attributes['wis']} | STR: {self.attributes['str']} | CON: \
{self.attributes['con']} | DEX: {self.attributes['dex']} | PER: {self.attributes['per']} | FOR: {self.attributes['for']}
Experience Pts: {self.exp}/{self.req_xp} | Gold Pieces: {main.party_info['gp']}

-Equipped Items-
Weapon: {inv_system.equipped[inv_name]['weapon']}
Accessory: {inv_system.equipped[inv_name]['access']}
Armor:
  Head: {inv_system.equipped[inv_name]['head']}
  Body: {inv_system.equipped[inv_name]['body']}
  Legs: {inv_system.equipped[inv_name]['legs']}""")

        main.s_input('\nPress enter/return ')

    def battle_turn(self):
        inv_name = self.name if self != player else 'player'
        player_weapon = inv_system.equipped[inv_name]['weapon']

        print(f"-{self.name}'s Turn-")

        # Check to see if the PCU is poisoned
        if self.status_ail == 'poisoned' and monster.hp > 0:
            main.smart_sleep(0.5)
            sounds.poison_damage.play()
            poison_damage = math.floor(self.hp/5)
            self.hp -= poison_damage

            print(f'{self.name} took poison damage! (-{poison_damage} HP)')

            if self.hp <= 0:
                return

        # There's a 1 in 4 chance for the players status effect to wear off each turn.
        if self.status_ail != 'none' and random.randint(0, 3) == 0:
            sounds.buff_spell.play()
            print(f"{self.name}'s afflictions have worn off! They are no longer {self.status_ail}.")
            self.status_ail = 'none'
            main.smart_sleep(0.5)

        # Basic Attack
        if self.move == '1':
            print(ascii_art.player_art[self.class_.title()] % f"{self.name} is making a move!\n")

            if inv_system.equipped[inv_name]['weapon'].type_ == 'melee':
                sounds.sword_slash.play()
                print(f'{self.name} fiercely attacks the {self.target.name} using their {player_weapon}...')

            else:
                sounds.aim_weapon.play()
                print(f'{self.name} aims carefully at the {self.target.name} using their {player_weapon}...')

            main.smart_sleep(0.75)

            if inv_system.equipped[inv_name]['weapon'].type_ == 'melee':
                dam_dealt = deal_damage(self, self.target, "physical")

            else:
                dam_dealt = deal_damage(self, self.target, "piercing")

            # Check for attack accuracy
            if random.randint(1, 512) in range(self.target.evad, 512):
                print(f"{self.name}'s attack connects with the {self.target.name}, dealing {dam_dealt} damage!")

                sounds.enemy_hit.play()
                self.target.hp -= dam_dealt

            else:
                print(f"The {self.target.name} narrowly avoids {self.name}'s attack!")
                sounds.attack_miss.play()

        if self.move == '2':
            self.c_spell.use_magic(self, True)

        elif self.move == '3':
            print(ascii_art.player_art[self.class_.title()] % f"{self.name} is making a move!\n")
            self.c_ability.use_ability(self)

        # Run away!
        elif self.move == '5' and battle.run_away(self):
            pygame.mixer.music.load(main.party_info['reg_music'])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(save_load.music_vol)

            return 'Ran'

        return

    def player_choice(self):
        print(battle_options.format(self.name))

        while True:
            self.move = main.s_input("Input [#]: ")

            try:
                self.move = re.sub("[^0-9]", '', self.move)[0]

            except IndexError:
                continue

            # Standard Attack
            if self.move == '1':
                self.choose_target(f"Who should {self.name} attack?")
                return

            # Use Magic
            elif self.move == '2':
                print('-'*save_load.divider_size)

                if self.status_ail == 'silenced':
                    sounds.debuff.play()
                    main.s_input(f"{self.name} is silenced! | Press enter/return ")
                    print(battle_options.format(self.name))

                    continue

                if not magic.pick_cat(self):
                    print(battle_options.format(self.name))

                    continue

                return

            # Use Abilities
            elif self.move == '3':
                do_loop = True
                while do_loop:
                    print('-'*save_load.divider_size)
                    print(f"{self.class_.title()} Abilities ({self.name} has {self.ap}/{self.max_ap} AP remaining)")

                    for num, ability in enumerate(abilities.a_abilities[self.class_]):
                        print(f"      [{num + 1}] {ability.name} --> {ability.ap_cost} AP")

                    while True:
                        try:
                            chosen = main.s_input('Input [#] (or type "back"): ').lower()
                            self.c_ability = abilities.a_abilities[self.class_][int(chosen) - 1]

                            if self.ap < self.c_ability.ap_cost:
                                print('-'*save_load.divider_size)
                                print(f"{self.name} doesn't have enough AP to cast {self.c_ability.name}!")
                                input("\nPress enter/return ")

                                break

                        except (IndexError, ValueError):
                            if chosen in ['e', 'x', 'exit', 'b', 'back']:
                                print('-'*save_load.divider_size)
                                print(battle_options.format(self.name))
                                do_loop = False
                                break

                        self.ap -= self.c_ability.ap_cost
                        self.c_ability.before_ability(self)
                        return

            # Use Items
            elif self.move == '4':
                print('-'*save_load.divider_size)

                if not inv_system.inventory['consumables']:
                    main.s_input('Your party has no battle items! | Press enter/return ')
                    print(battle_options.format(self.name))

                    continue

                if self.status_ail == "muted":
                    sounds.debuff.play()
                    main.s_input(f"{self.name} is muted! | Press enter/return ")
                    print(battle_options.format(self.name))

                    continue

                if not battle.battle_inventory(self):
                    print(battle_options.format(self.name))

                    continue

                main.s_input('\nPress enter/return ')
                return

            # Run
            elif self.move == '5':
                return

    def choose_target(self, action_desc, ally=False, enemy=True):
        pcu_list = [x for x in [player,
                                solou,
                                xoann,
                                chyme,
                                ran_af,
                                adorine,
                                parsto] if x.enabled]

        if enemy and not ally:
            if len([x for x in battle.m_list if x.status_ail != 'dead']) == 1:
                self.target = [x for x in battle.m_list if x.status_ail != 'dead'][0]

                return

            this_list = [x for x in battle.m_list if x.status_ail != 'dead']

        elif ally and not enemy:
            if len(pcu_list) == 1:
                self.target = pcu_list[0]

                return

            this_list = pcu_list

        elif ally and enemy:
            this_list = pcu_list + [x for x in battle.m_list if x.status_ail != 'dead']

        else:
            raise Exception('Incorrect arguments - at least one of "ally" or "enemy" must be true.')

        print('-'*save_load.divider_size)
        print(action_desc)

        for x, y in enumerate(this_list):
            print(f"      [{x + 1}] {y.name}")

        while True:
            chosen = main.s_input("Input [#]: ").lower()

            try:
                self.target = this_list[int(chosen) - 1]

            except (IndexError, ValueError):
                continue

            return

    def increase_attribute(self, attribute):
        if attribute.startswith('i'):
            self.m_dfns += 1
            self.m_attk += 1
            self.mp += 2
            self.attributes['int'] += 1

        elif attribute.startswith('w'):
            self.mp += 2
            self.attributes['wis'] += 1

        elif attribute.startswith('s'):
            self.attk += 1
            self.p_dfns += 1
            self.dfns += 1
            self.attributes['str'] += 1

        elif attribute.startswith('c'):
            self.max_hp += 1
            self.dfns += 1
            self.p_dfns += 1
            self.m_dfns += 1
            self.attributes['con'] += 1

        elif attribute.startswith('d'):
            self.attk += 1
            self.spd += 1
            self.evad += 1
            self.attributes['dex'] += 1

        elif attribute.startswith('p'):
            self.p_attk += 1
            self.p_dfns += 1
            self.evad += 1
            self.attributes['per'] += 1

        elif attribute.startswith('f'):
            if self.extra_sp == 10:
                self.ext_gol += 2
                self.ext_exp += 2

            else:
                self.extra_sp += 1
                self.ext_gol += 1
                self.ext_exp += 1

            self.attributes['for'] += 1


class Monster(Unit):
    # All monsters use this class. Bosses use a sub-class called
    # "Boss" (located in bosses.py) which inherits from this.
    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        Unit.__init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)
        self.monster_name = ''  # The name of the monsters species (so a Fast Goblin's monster_name would be Goblin)
        self.status = ''        # The status effect that will be applied to the player if RNGsus wills it
        self.is_poisoned = False
        self.is_defending = False
        self.class_ = None

        self.gold = 0
        self.experience = 0
        self.items = 0

        self.ability_vars = {
            'poison_pow': 0,
            'poison_dex': 0
            }  # This dictionary will contain numerous variables that interact with abilties in battle

    def monst_level(self):
        self.lvl = main.party_info['current_tile'].m_level

        for x in range(1, self.lvl):
            self.hp += 5
            self.mp += 4
            self.attk += 4
            self.dfns += 3
            self.p_attk += 4
            self.p_dfns += 3
            self.m_attk += 4
            self.m_dfns += 3
            self.spd += 3
            self.evad += 2

        self.max_hp = self.hp
        self.max_mp = self.mp

    def give_status(self, target):
        # Attempt to give the target a status ailment
        status = random.choice([x for x in ['poisoned',
                                            'silenced',
                                            'weakened',
                                            'blinded',
                                            'paralyzed',
                                            'muted'] if x != target.status_ail])

        print(f'The {self.monster_name} is attempting to make {self.m_target.name} {status}...')
        main.smart_sleep(0.75)

        # There's a 50% chance that the status spell will work
        if random.randint(0, 1) == 1:
            sounds.buff_spell.play()
            print(f'{self.m_target.name} is now {status}!')
            target.status_ail = status

        else:
            sounds.debuff.play()
            print(f'The {self.monster_name} failed to make {self.m_target.name} {status}!')

        self.mp -= self.max_mp*0.1

    def monst_name(self):
        m_type = {'Central Forest': ['Goblin Archer', 'Spriggan', 'Imp', 'Bat',
                                     'Beetle' if player.name != "Flygon Jones" else "Calculator"],

                  'Harconian Coastline': ['Shell Mimic', 'Giant Crab', 'Naiad', 'Sea Serpent', 'Squid'],

                  'Glacian Plains': ['Ice Soldier', 'Minor Yeti', 'Corrupt Thaumaturge', 'Arctic Wolf', 'Frost Bat'],

                  'Bogthorn Marsh': ['Bog Slime', 'Moss Ogre', "Will-o'-the-wisp", 'Vine Lizard', 'Sludge Rat'],

                  'Arcadian Desert': ['Mummy', 'Sand Golem', 'Anubis', 'Fire Ant', 'Naga'],

                  'Terrius Mt. Range': ['Troll', 'Rock Giant', 'Oread', 'Tengu', 'Giant Worm'],

                  'Overshire Graveyard': ['Zombie', 'Undead Archer', 'Necromancer', 'Skeleton', 'Ghoul'],

                  'Aethus': ['Alicorn', 'Griffin', 'Wraith', 'Harpy', 'Flying Serpent']
                  }

        self.name = m_type[main.party_info['reg']][random.randint(0, 4)]

        # A list of monster-types and what AI they are to have
        magic_enemies = ['Naiad', "Will-o'the-wisp", 'Anubis', 'Oread', 'Necromancer', 'Wraith',
                         'Alicorn', 'Flying Serpent', 'Imp', 'Corrupt Thaumaturge', 'Spriggan']

        melee_enemies = ['Shell Mimic', 'Giant Crab', 'Bog Slime', 'Mummy', 'Sand Golem',
                         'Moss Ogre', 'Vine Lizard', 'Troll', 'Ghoul', 'Griffin', 'Tengu',
                         'Giant Worm', 'Zombie', 'Arctic Wolf', 'Minor Yeti', 'Sludge Rat',
                         'Sea Serpent', 'Beetle', 'Calculator', 'Harpy']

        ranged_enemies = ['Fire Ant', 'Naga', 'Ice Soldier', 'Frost Bat', 'Bat',
                          'Skeleton', 'Squid', 'Rock Giant', 'Undead Archer', 'Goblin Archer']

        # Assign the correct AI and stats to each kind of monster
        if self.name in magic_enemies:
            self.battle_turn = self.magic_ai
            self.magic_stats()

        elif self.name in melee_enemies:
            self.battle_turn = self.melee_ai
            self.melee_stats()

        elif self.name in ranged_enemies:
            self.battle_turn = self.ranged_ai
            self.ranger_stats()

        # Set the flavor text to match the attack style of various monsters
        biting_monsters = ['Vine Lizard', 'Beetle', 'Zombie', 'Ghoul', 'Arctic Wolf', 'Sea Serpent', 'Shell Mimic']
        charging_monsters = ['Giant Worm', 'Bog Slime']
        slashing_monsters = ['Griffin', 'Tengu', 'Harpy', 'Sludge Rat', 'Giant Crab']
        whacking_monsters = ['Troll', 'Rock Giant']
        spitting_monsters = ['Frost Bat', 'Squid', 'Fire Ant', 'Bat']
        arrow_monsters = ['Naga', 'Ice Soldier', 'Undead Archer', 'Goblin Archer', 'Skeleton']
        fist_monsters = ['Moss Ogre', 'Minor Yeti', 'Sand Golem', 'Mummy']
        magic_monsters = ['Imp', 'Naiad', "Will-o'the-wisp", 'Anubis', 'Oread', 'Necromancer', 'Wraith', 'Alicorn',
                          'Flying Serpent', 'Corrupt Thaumaturge', 'Spriggan']
        math_monsters = ['Calculator']

        if self.name in biting_monsters:
            self.attk_msg = "bears its fangs and tries to bite"
        elif self.name in charging_monsters:
            self.attk_msg = "puts all its weight into trying to charge"
        elif self.name in slashing_monsters:
            self.attk_msg = "reveals its claws and prepares to slash"
        elif self.name in whacking_monsters:
            self.attk_msg = "finds a nearby rock and prepares to use it to beat"
        elif self.name in spitting_monsters:
            self.attk_msg = "begins to spit a dangerous projectile at"
        elif self.name in arrow_monsters:
            self.attk_msg = "readies its bow to fire a volley of arrows at"
        elif self.name in fist_monsters:
            self.attk_msg = "prepares its fists to smash"
        elif self.name in magic_monsters:
            self.attk_msg = "draws from its magical essence to destroy"
        elif self.name in math_monsters:
            self.attk_msg = "begins calculating the hell out of"

        # Prepare to add the modifier onto the name
        self.monster_name = copy.copy(self.name)

        modifiers = ['Slow', 'Fast', 'Powerful', 'Ineffective', 'Nimble', 'Clumsy', 'Armored', 'Broken', 'Mystic',
                     'Foolish', 'Strong', 'Weak', 'Observant', 'Obtuse']

        modifier = random.choice(modifiers)

        if self.name == "Goblin" and random.randint(0, 50) == 42:
            self.modifier = "Whispering"
            self.attk *= 1.2
            self.dfns *= 1.2
            self.m_attk *= 1.2
            self.m_dfns *= 1.2
            self.p_attk *= 1.2
            self.p_dfns *= 1.2
            self.evad *= 1.2
            self.spd *= 1.2

        elif modifier == 'Slow':  # Very-low speed, below-average speed
            self.spd /= 1.3
            self.evad /= 1.1
        elif modifier == 'Fast':  # Very-high speed, above-average speed
            self.spd *= 1.3
            self.evad *= 1.1
        elif modifier == 'Nimble':  # Very-high evasion, above-average speed
            self.evad *= 1.3
            self.spd *= 1.1
        elif modifier == 'Clumsy':  # Very-low evasion, below-average speed
            self.evad /= 1.3
            self.spd /= 1.1
        elif modifier == 'Powerful':  # High attack stats
            self.attk *= 1.2
            self.m_attk *= 1.2
            self.p_attk *= 1.2
        elif modifier == 'Ineffective':  # Low attack stats
            self.attk /= 1.2
            self.m_attk /= 1.2
            self.p_attk /= 1.2
        elif modifier == 'Armored':  # High defense stats
            self.dfns *= 1.2
            self.m_dfns *= 1.2
            self.p_dfns *= 1.2
        elif modifier == 'Broken':  # Low defense stats
            self.dfns /= 1.2
            self.m_dfns /= 1.2
            self.p_dfns /= 1.2
        elif modifier == 'Observant':  # High ranged stats
            self.p_attk *= 1.2
            self.p_dfns *= 1.2
        elif modifier == 'Obtuse':  # Low ranged stats
            self.p_attk /= 1.2
            self.p_dfns /= 1.2
        elif modifier == 'Strong':  # High melee stats
            self.attk *= 1.2
            self.dfns *= 1.2
        elif modifier == 'Weak':  # Low melee stats
            self.attk /= 1.2
            self.dfns /= 1.2
        elif modifier == 'Mystic':  # High magic stats
            self.m_attk *= 1.2
            self.m_dfns *= 1.2
            self.mp *= 1.2
        elif modifier == 'Foolish':  # Low magic stats
            self.m_attk /= 1.2
            self.m_dfns /= 1.2

        # Adjust for problems that may happen with enemy stats
        for stat in ['self.attk', 'self.dfns', 'self.p_attk', 'self.p_dfns', 'self.m_attk', 'self.m_dfns',
                     'self.spd', 'self.evad', 'self.mp', 'self.max_mp', 'self.hp', 'self.max_hp']:

            if eval(stat) < 1:  # Enemy stats cannot be lower than one
                exec(f"{stat} = 1")

            exec(f"{stat} = math.ceil({stat})")  # Enemy stats must be integers

        if self.monster_name == "Calculator":
            self.element = 'grass'
            self.status = 'fucked'
            self.status_msg = "was imbued with bullshit, causing severe fuckage!"

        elif main.party_info['reg'] == 'Glacian Plains':
            self.element = 'ice'
            self.status = 'frostbitten'
            self.status_msg = "was imbued with frost, causing painful frostbite!"

        elif main.party_info['reg'] == 'Arcadian Desert':
            self.element = 'fire'
            self.status = 'blinded'
            self.status_msg = "brought upon a sandstorm, causing temporary blindness!"

        elif main.party_info['reg'] == 'Terrius Mt. Range':
            self.element = 'earth'
            self.status = 'paralyzed'
            self.status_msg = "hit a nerve ending, causing temporary paralysis!"

        elif main.party_info['reg'] == 'Harconian Coastline':
            self.element = 'water'
            self.status = 'muted'
            self.status_msg = "caused organizational issues, leading to impaired item usage!"

        elif main.party_info['reg'] == 'Central Forest':
            self.element = 'electric'
            self.status = 'weakened'
            self.status_msg = "drained its target's energy, causing temporary weakness!"

        elif main.party_info['reg'] == 'Bogthorn Marsh':
            self.element = 'grass'
            self.status = 'poisoned'
            self.status_msg = "was imbued with deadly toxins that will slowly drain health!"

        elif main.party_info['reg'] == 'Overshire Graveyard':
            self.element = 'death'
            self.status = 'poisoned'
            self.status_msg = "poisoned their target using noxious fumes!"

        elif main.party_info['reg'] == 'Aethus':
            self.element = 'wind'
            self.status = 'blinded'
            self.status_msg = "brought upon the winds, dampening their target's vision!"

        self.name = ' '.join([modifier, self.name]) if modifier else self.name

        # Give the monster a set of items to drop if RNGsus wills it
        if random.randint(0, 4) == 0:  # 20% chance
            self.items = random.choice(items.monster_drop_list[self.monster_name])

    def melee_stats(self):
        # Set stats for melee-class monsters
        self.hp *= 1.2
        self.hp = math.ceil(self.hp)
        self.max_hp = copy.copy(self.hp)

        self.attk *= 1.5
        self.attk = math.ceil(self.attk)

        self.p_attk *= 0.5
        self.p_attk = math.ceil(self.p_attk)

        self.m_attk *= 0.5
        self.m_attk = math.ceil(self.m_attk)

        self.dfns *= 1.5
        self.dfns = math.ceil(self.dfns)

        self.p_dfns *= 1.5
        self.p_dfns = math.ceil(self.p_dfns)

        self.m_dfns *= 0.5
        self.m_dfns = math.ceil(self.m_dfns)

        self.spd *= 0.5
        self.spd = math.ceil(self.spd)

        self.class_ = 'warrior'

    def magic_stats(self):
        # Set stats for Mage-class monsters
        self.mp *= 1.5
        self.mp = math.ceil(self.mp)
        self.max_mp = copy.copy(self.mp)

        self.attk *= 0.5
        self.attk = math.ceil(self.attk)

        self.p_attk *= 0.5
        self.p_attk = math.ceil(self.p_attk)

        self.m_attk *= 1.5
        self.m_attk = math.ceil(self.m_attk)

        self.dfns *= 0.65
        self.dfns = math.ceil(self.dfns)

        self.p_dfns *= 0.65
        self.p_dfns = math.ceil(self.p_dfns)

        self.m_dfns *= 1.5
        self.m_dfns = math.ceil(self.m_dfns)

        self.class_ = 'mage'

    def ranger_stats(self):
        # Set stats for Ranger-class monsters
        self.hp *= 0.9
        self.hp = math.ceil(self.hp)
        self.max_hp = copy.copy(self.hp)

        self.attk *= 0.8
        self.attk = math.ceil(self.attk)

        self.p_attk *= 1.5
        self.p_attk = math.ceil(self.p_attk)

        self.m_attk *= 0.8
        self.m_attk = math.ceil(self.m_attk)

        self.dfns *= 0.8
        self.dfns = math.ceil(self.dfns)

        self.p_dfns *= 1.2
        self.p_dfns = math.ceil(self.p_dfns)

        self.spd *= 1.5
        self.spd = math.ceil(self.spd)

        self.evad *= 1.5
        self.evad = math.ceil(self.evad)

        self.class_ = 'ranger'

    def base_turn(self):
        self.get_target()

        print(f"-{self.monster_name}'s Turn-")
        print(ascii_art.monster_art[self.monster_name] % f"The {self.monster_name} is making a move!\n")
        self.do_abilities()
        self.battle_turn()

    def do_abilities(self):
        if self.status_ail == 'poisoned':
            damage = math.ceil(self.ability_vars['poison_pow']*self.max_hp + self.ability_vars['poison_dex'])
            self.hp -= damage
            print(f"The {self.monster_name} took {damage} damage from poison!")
            sounds.poison_damage.play()
            main.smart_sleep(0.75)

    def get_target(self):
        self.m_target = random.choice([x for x in [
                                     player,
                                     solou,
                                     xoann,
                                     chyme,
                                     ran_af,
                                     parsto,
                                     adorine
                                     ] if x.enabled and x.status_ail != 'dead'])

    def magic_ai(self):
        # 16.67% chance for the enemy to give a status ailment
        if self.m_target.status_ail == "none" and random.randint(0, 5) == 0 and self.mp >= self.max_mp*0.1:
            self.give_status(self.m_target)

        # Magic heal
        elif self.hp <= self.max_hp/5 and self.mp >= self.max_mp*0.2:
            print(f'The {self.monster_name} is casting a healing spell on itself...')
            main.smart_sleep(0.75)
            print(f'The {self.monster_name} heals itself for {max([self.hp*0.2, 20])} HP!')

            sounds.magic_healing.play()

            self.hp += max([self.hp*0.2, 20])

            if self.hp > self.max_hp:
                self.hp -= (self.hp - self.max_hp)

            self.mp -= self.max_mp*0.2

        # Magic Attack
        elif self.mp >= self.max_mp*0.15:

            sounds.magic_attack.play()

            print(f'The {self.monster_name} is preparing to cast a spell on {self.m_target.name}!')
            main.smart_sleep(0.75)

            dam_dealt = deal_damage(self, self.m_target, "magical")
            if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                sounds.enemy_hit.play()
                print(f"The {self.monster_name}'s spell deals {dam_dealt} damage to {self.m_target.name}!")

                self.m_target.hp -= dam_dealt

            else:
                sounds.attack_miss.play()
                print(f"The {self.monster_name}'s spell narrowly misses {self.m_target.name}!")

            self.mp -= self.max_mp*0.15

        # Non-magic Attack
        else:
            sounds.aim_weapon.play()
            print(f'The {self.monster_name} {self.attk_msg} {self.m_target.name}')

            main.smart_sleep(0.75)

            dam_dealt = deal_damage(self, self.m_target, "piercing")
            if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                sounds.enemy_hit.play()
                print(f"The {self.monster_name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

                self.m_target.hp -= dam_dealt

            else:
                sounds.attack_miss.play()
                print(f"The {self.monster_name}'s attack narrowly misses {self.m_target.name}!")

    def ranged_ai(self):
        # At the moment, Ranged monsters are only capable of attacking
        print(f'The {self.monster_name} {self.attk_msg} {self.m_target.name}!')
        sounds.aim_weapon.play()

        main.smart_sleep(0.75)

        if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
            dam_dealt = deal_damage(self, self.m_target, 'piercing')

            print(f"The {self.monster_name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

            self.m_target.hp -= dam_dealt
            sounds.enemy_hit.play()

        else:
            sounds.attack_miss.play()
            print(f"The {self.monster_name}'s attack narrowly misses {self.m_target.name}!")

    def melee_ai(self):
        # Melee monsters have a 1 in 6 (16.667%) chance to defend
        if random.randint(0, 5) == 0 and not self.is_defending:
            self.is_defending = True
            sounds.buff_spell.play()

            self.dfns *= 2
            self.m_dfns *= 2
            self.p_dfns *= 2

            self.dfns = math.ceil(self.dfns)
            self.p_dfns = math.ceil(self.p_dfns)
            self.m_dfns = math.ceil(self.m_dfns)

            print(f"The {self.monster_name} defends itself from attacks for one turn!")

        # Set defense back to normal if the monster defended last turn
        elif self.is_defending:
            self.is_defending = False

            self.dfns /= 2
            self.m_dfns /= 2
            self.p_dfns /= 2
            self.dfns = math.floor(self.dfns)
            self.m_dfns = math.floor(self.m_dfns)
            self.p_dfns = math.floor(self.p_dfns)

        # If the monster doesn't defend, then it will attack!
        if not self.is_defending:
            sounds.sword_slash.play()
            print(f'The {self.monster_name} {self.attk_msg} {self.m_target.name}!')
            main.smart_sleep(0.75)

            dam_dealt = deal_damage(self, self.m_target, "physical")
            if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                sounds.enemy_hit.play()
                print(f"The {self.monster_name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

                self.m_target.hp -= dam_dealt

            else:
                sounds.attack_miss.play()
                print(f"The {self.monster_name}'s attack narrowly misses {self.m_target.name}!")



class Boss(Monster):
    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad, lvl, b_items, gold,
                 experience, attk_msg, active=True, element='none'):

        Monster.__init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)
        self.items = b_items
        self.active = active
        self.lvl = lvl
        self.element = element
        self.experience = experience
        self.gold = gold
        self.attk_msg = attk_msg
        self.monster_name = copy.copy(self.name)

    def max_stats(self):
        self.hp = copy.copy(self.max_hp)
        self.mp = copy.copy(self.max_mp)

    # noinspection PyMethodMayBeStatic
    def new_location(self, add=True):
        # Translate the location of the boss into a string, and then store it in the player's inventory
        mpi = main.party_info

        coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
        coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
        coord_z = f"""{mpi["z"] if mpi["z"] != 0 else ""}{"'UP" if mpi["z"] > 0 else "'DOWN" if mpi['z'] < 0 else ""}"""

        new_coords = f"{self.name}: {coord_y}, {coord_x}, {coord_z}"

        if add and new_coords not in inv_system.inventory['coord']:
            inv_system.inventory['coord'].append(new_coords)
            print('-'*save_load.divider_size)
            print(f"You quickly mark down the location of {self.name}'s lair.")
            main.s_input("\nPress enter/return ")

        else:

            return new_coords

    def upon_defeating(self):
        pass


# Boss: Master Slime -- Position: 0'N, 1'E
def mastslim_ud():
    npcs.alfred_quest_1.finished = True
    npcs.alfred_convo_2.active = False


master_slime = Boss('Master Slime',
                    35, 5,   # 35 HP and 5 MP
                    12, 5,   # 12 Attack, 5 Defense
                    6, 5,    # 6 Pierce Attack, 5 Pierce Defense
                    8, 0,    # 8 Magic Attack, 0 Magic Defense
                    6, 6,    # 6 Speed, 6 Evasion
                    3,       # Level 3
                    None,    # Drops no items
                    25, 25,  # Gives 25 XP and 25 GP
                    "jiggles ferociously and begins to attack",
                    active=False)

master_slime.battle_turn = master_slime.melee_ai
master_slime.upon_defeating = mastslim_ud

# Boss: Goblin Chieftain -- Position: 4'N, -2'W
whisp_goblin = Boss('Goblin Chieftain',
                    50, 10,  # 50 HP and 10 MP
                    20, 20,  # 20 Attack, 20 Defense
                    12, 15,  # 12 Pierce Attack, 15 Pierce Defense
                    8, 12,   # 8 Magic Attack, 12 Magic Defense
                    15, 7,   # 15 Speed, 7 Evasion
                    5,       # Level 5
                    None,    # Drops no items
                    45, 45,  # Gives 45 XP and 45 GP
                    "readies his great spear and begins to stab")

whisp_goblin.battle_turn = whisp_goblin.melee_ai


# Boss: Menacing Phantom -- Position: 8'N, -12'W
def menacphan_ud():
    # Stands for "Menacing Phantom -- Upon Defeating"
    npcs.stewson_quest_1.finished = True
    npcs.stewson_convo_2.active = False


menac_phantom = Boss('Menacing Phantom',
                     75, 50,  # 75 HP and 50 MP
                     10, 20,  # 10 Attack, 20 Defense
                     5, 20,   # 5 Pierce Attack, 20 Pierce Defense
                     35, 25,  # 35 Magic Attack, 25 Magic Defense
                     20, 15,  # 20 Speed, 15 Evasion
                     8,       # Level 8
                     None,    # Drops no items
                     75, 75,  # Gives 75 XP and 75 GP
                     "calls upon its ethereal power and casts a hex on",
                     active=False, element='dark')

menac_phantom.battle_turn = menac_phantom.magic_ai
menac_phantom.upon_defeating = menacphan_ud


# Boss: Terrible Tarantuloid -- Position: -23'S, -11'W  (Adventure in Pixels)
def terrtar_ud():
    npcs.krystin_convo_2.active = False
    npcs.krystin_convo_3.active = True
    npcs.kyle_convo_2.active = False
    npcs.kyle_convo_3.active = True
    npcs.alden_convo_1.active = False
    npcs.alden_convo_2.active = True


terr_tarant = Boss('Terrible Tarantuloid',
                   100, 25,   # 100 Health, 25 Mana
                   45, 30,    # 45 Attack, 30 Defense
                   25, 15,    # 25 Pierce Attack, 15 Pierce Defense
                   15, 25,    # 15 Magic Attack, 25 Magic Defense
                   35, 25,    # 35 Speed, 25 Evasion
                   12,        # Level 12
                   None,      # Drops no items
                   150, 150,  # Gives 150 XP and 150 GP
                   "readies its venomous fangs and bites")

terr_tarant.battle_turn = terr_tarant.melee_ai
terr_tarant.upon_defeating = terrtar_ud


# Boss: Cursed Spectre -- Position 22'N, 3'E
def cursspect_ud():
    npcs.rivesh_convo_3.active = False
    npcs.rivesh_quest_1.finished = True


cursed_spect = Boss('Cursed Spectre',
                    125, 75,             # 125 Health, 75 Mana
                    15, 30,              # 15 Attack, 30 Defense
                    20, 25,              # 20 Pierce Attack, 25 Pierce Defense
                    50, 35,              # 50 Magic Attack, 35 Magic Defense
                    25, 20,              # 25 Speed, 20 Evasion
                    15,                  # Level 15
                    None,                # Drops no items
                    250, 250,            # Gives 250 XP and 250 GP
                    "calls upon its ethereal power and casts a hex on",
                    element='dark', active=False)

cursed_spect.battle_turn = cursed_spect.magic_ai
cursed_spect.upon_defeating = cursspect_ud

# Boss: Ent -- Position: 27'N, 15'E
giant_ent = Boss('Giant Ent',
                 125, 35,         # 125 Health, 75 Mana
                 35, 50,          # 35 Attack, 50 Defense
                 15, 50,          # 15 Pierce Attack, 50 Pierce Defense
                 20, 15,          # 20 Magic Attack, 15 Magic Defense
                 15, 5,           # 15 Speed, 5 Evasion
                 15,              # Level 15
                 None,            # Drops no items
                 250, 250,        # Gives 250 XP and 250 GP
                 "slowly lumbers over and whacks",
                 element='grass', active=True)

giant_ent.battle_turn = giant_ent.melee_ai

boss_list = [whisp_goblin, master_slime, menac_phantom, terr_tarant, cursed_spect, giant_ent]
defeated_bosses = []  # Make sure you can only defeat the boss one time


def check_bosses():
    global monster

    for boss in main.party_info['current_tile'].boss_list:
        if boss.name not in defeated_bosses and boss.active:
            print('-'*save_load.divider_size)

            if boss.new_location(add=False) not in inv_system.inventory['coord']:
                print('You feel the presence of an unknown entity...')

            else:
                print(f'You come across the lair of the {boss.name}.')

            while True:
                if boss.new_location(add=False) not in inv_system.inventory['coord']:
                    y_n = main.s_input('Do you wish to investigate? | Y/N: ')

                else:
                    y_n = main.s_input(f'Do you wish to confront the {boss.name}? | Y/N: ')

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    monster = boss
                    boss.max_stats()
                    boss.new_location()
                    print('-'*save_load.divider_size)

                    battle.battle_system(is_boss=True)

                    return True

                elif y_n.startswith('n'):
                    return True

    else:
        return False


def deal_damage(attacker, target, damage_type, absolute=0, spell_power=0):
    # Attacker - the Unit that is attacking
    # Target - the Unit that is being attacked
    # Damage Type - the type of damage being dealt (magical, physical, or piercing)
    # Absolute - Whether or not the damage should be affected by crits, armor, status ailments, etc.

    if isinstance(attacker, PlayableCharacter):
        t_equip = inv_system.equipped[attacker.name if attacker != player else 'player']
        weapon_dmg = t_equip['weapon'].power

        attack = battle.temp_stats[attacker.name]['attk']
        p_attack = battle.temp_stats[attacker.name]['p_attk']
        m_attack = battle.temp_stats[attacker.name]['m_attk']

    else:
        attack = attacker.attk
        p_attack = attacker.p_attk
        m_attack = attacker.m_attk

        weapon_dmg = 0

    if isinstance(target, PlayableCharacter):
        t_equip = inv_system.equipped[target.name if target != player else 'player']
        resist = sum([t_equip[armor].defense for armor in t_equip if isinstance(t_equip[armor], items.Armor)])

        defense = battle.temp_stats[target.name]['dfns']
        p_defense = battle.temp_stats[target.name]['p_dfns']
        m_defense = battle.temp_stats[target.name]['m_dfns']

    else:
        defense = target.dfns
        p_defense = target.p_dfns
        m_defense = target.p_attk

        resist = 0

    if absolute:
        target.hp -= absolute

    else:
        if damage_type == 'physical':
            dam_dealt = (attack - defense/2)*(1 + resist)*(1 + weapon_dmg)

            # Mages deal half damage with non-magical attacks
            if attacker.class_ == 'mage':
                dam_dealt /= 2

        elif damage_type == 'piercing':
            dam_dealt = (p_attack - p_defense/2)*(1 + resist)*(1 + weapon_dmg)

            if attacker.status_ail == 'blinded':
                dam_dealt /= 2
                print(f"{attacker.name}'s poor vision reduces their attack damage by half!")

            # Mages deal half damage with non-magical attacks
            if attacker.class_ == 'mage':
                dam_dealt /= 2

        elif damage_type == 'magical':
            dam_dealt = (m_attack - m_defense/2)*(1 + resist)*(1 + spell_power)

            # Classes that aren't mages or paladins deal 0.75x damage with magical attacks
            if attacker.class_ not in ['mage', 'paladin']:
                dam_dealt *= 0.75

        else:
            raise Exception('Incorrect value for "damage_type" - must be physical, piercing, or magical')

        if random.randint(1, 100) <= 15:
            dam_dealt *= 1.5
            sounds.critical_hit.play()
            print("It's a critical hit! 1.5x damage!")

            main.smart_sleep(0.5)

        dam_dealt = eval_element(attacker, target, dam_dealt)

        if dam_dealt < 1:
            dam_dealt = 1

        if dam_dealt > 999:
            dam_dealt = 999

        return math.ceil(dam_dealt)


def eval_element(attacker, target, damage):
    # Fire < Water < Electricity < Earth < Wind < Grass < Ice < Fire
    # Light < Dark and Dark < Light
    # "None" element is neutral to all elements
    # All other interactions are neutral

    # Set everything to be lowercase, just incase
    a_elem = attacker.element.lower()
    t_elem = target.element.lower()

    # element_matchup[key][0] is the element that key is weak to
    # element_matchup[key][1] is the element that key is resistant to
    element_matchup = {
        'fire': ['water', 'ice'],
        'water': ['electric', 'fire'],
        'electric': ['earth', 'water'],
        'earth': ['grass', 'electric'],
        'wind': ['ice', 'earth'],
        'grass': ['wind', 'wind'],
        'ice': ['fire', 'grass'],
        'light': ['light', 'dark'],
        'dark': ['dark', 'light']
    }

    # If either the attacker or the target have no element, OR the target and the attacker both have the same element,
    # then do not modify the damage (1x multiplier)
    if (a_elem == 'none' or t_elem == 'none') or (a_elem == t_elem):
        return damage

    if element_matchup[a_elem][1] == t_elem:
        return math.ceil(damage*1.5)

    elif element_matchup[a_elem][0] == t_elem:
        return math.ceil(damage/1.5)

    return damage


def create_player():
    global player
    global solou
    global xoann
    global adorine
    global ran_af
    global parsto
    global chyme

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)

    # Pronounced "So-low"
    solou = PlayableCharacter('Solou', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='mage', enabled=False)
    # Pronounced "Zo-ann"
    xoann = PlayableCharacter('Xoann', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='assassin', enabled=False)
    # Pronounced "Adore-een"
    adorine = PlayableCharacter('Adorine', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='warrior', enabled=False)
    # Pronounced "Rahn-ahf"
    ran_af = PlayableCharacter("Ran'Af", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='monk', enabled=False)
    # Pronounced "Parse-toe"
    parsto = PlayableCharacter("Parsto", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='ranger', enabled=False)
    # Rhymes with "Chime"
    chyme = PlayableCharacter("Chyme", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='paladin', enabled=False)

    # Set the player's max HP and MP
    player.max_hp = copy.copy(player.hp)
    player.max_mp = copy.copy(player.mp)

    player.choose_name()
    player.choose_class()
    save_load.set_adventure_name()

    if player.class_ == "warrior":
        player.max_hp += 5
        player.max_mp -= 1
        player.dfns += 3
        player.p_dfns += 2
        player.attk += 3
        player.spd -= 1
        player.evad -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.wdn_sht)

    elif player.class_ == "mage":
        player.max_hp += 1
        player.max_mp += 6
        player.m_attk += 4
        player.m_dfns += 3
        inv_system.equipped['player']['weapon'] = copy.copy(items.mag_twg)

    elif player.class_ == "assassin":
        player.max_hp += 2
        player.max_mp += 1
        player.attk += 3
        player.dfns += 2
        player.spd += 4
        player.evad += 2
        inv_system.equipped['player']['weapon'] = copy.copy(items.stn_dag)

    elif player.class_ == "ranger":
        player.max_mp += 2
        player.p_attk += 4
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        inv_system.equipped['player']['weapon'] = copy.copy(items.slg_sht)

    elif player.class_ == "monk":
        player.max_hp += 2
        player.max_mp += 2
        player.attk += 3
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        player.dfns -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.fists)

    elif player.class_ == "paladin":
        player.max_hp += 3
        player.max_mp += 4
        player.m_dfns += 3
        player.m_attk += 3
        player.dfns += 3
        player.p_dfns += 3
        player.attk += 3
        player.spd -= 1
        player.evad -= 1
        magic.spellbook['player']['Healing'].append(magic.min_heal)
        magic.spellbook['player']['Damaging'].append(magic.purify)
        inv_system.equipped['player']['weapon'] = copy.copy(items.rbr_mlt)

    player.hp = copy.copy(player.max_hp)
    player.mp = copy.copy(player.max_mp)
    print('-'*save_load.divider_size)

    save_load.save_game(verbose=False)


def spawn_monster():
    for unit_object in ['monster', 'monster_2', 'monster_3']:
        globals()[unit_object] = Monster('', 10, 5, 3, 2, 3, 2, 3, 2, 3, 2)
        globals()[unit_object].monst_name()
        globals()[unit_object].monst_level()


def fix_stats():
    # Makes sure that that no-one ever has 1) stats that are above their maximum, 2) stats that are negative,
    # and 3) stats that are not integers.

    global player
    global solou
    global xoann
    global chyme
    global parsto
    global ran_af
    global adorine
    global monster

    if player.hp < 0:
        player.hp = 0
    if solou.hp < 0:
        solou.hp = 0
    if xoann.hp < 0:
        xoann.hp = 0
    if chyme.hp < 0:
        chyme.hp = 0
    if parsto.hp < 0:
        parsto.hp = 0
    if ran_af.hp < 0:
        ran_af.hp = 0
    if adorine.hp < 0:
        adorine.hp = 0

    if player.mp < 0:
        player.mp = 0
    if solou.mp < 0:
        solou.mp = 0
    if xoann.mp < 0:
        xoann.mp = 0
    if chyme.mp < 0:
        chyme.mp = 0
    if parsto.mp < 0:
        parsto.mp = 0
    if ran_af.mp < 0:
        ran_af.mp = 0
    if adorine.mp < 0:
        adorine.mp = 0

    if player.hp > player.max_hp:
        player.hp -= (player.hp - player.max_hp)
    if solou.hp > solou.max_hp:
        solou.hp -= (solou.hp - solou.max_hp)
    if xoann.hp > xoann.max_hp:
        xoann.hp -= (xoann.hp - xoann.max_hp)
    if chyme.hp > chyme.max_hp:
        chyme.hp -= (chyme.hp - chyme.max_hp)
    if parsto.hp > parsto.max_hp:
        parsto.hp -= (parsto.hp - parsto.max_hp)
    if ran_af.hp > ran_af.max_hp:
        ran_af.hp -= (ran_af.hp - ran_af.max_hp)
    if adorine.hp > adorine.max_hp:
        adorine.hp -= (adorine.hp - adorine.max_hp)

    if player.mp > player.max_mp:
        player.mp -= (player.mp - player.max_mp)
    if solou.mp > solou.max_mp:
        solou.mp -= (solou.mp - solou.max_mp)
    if xoann.mp > xoann.max_mp:
        xoann.mp -= (xoann.mp - xoann.max_mp)
    if chyme.mp > chyme.max_mp:
        chyme.mp -= (chyme.mp - chyme.max_mp)
    if parsto.mp > parsto.max_mp:
        parsto.mp -= (parsto.mp - parsto.max_mp)
    if ran_af.mp > ran_af.max_mp:
        ran_af.mp -= (ran_af.mp - ran_af.max_mp)
    if adorine.mp > adorine.max_mp:
        adorine.mp -= (adorine.mp - adorine.max_mp)

    player.hp = math.ceil(player.hp)
    player.mp = math.ceil(player.mp)
    parsto.hp = math.ceil(parsto.hp)
    parsto.mp = math.ceil(parsto.mp)
    adorine.hp = math.ceil(adorine.hp)
    adorine.mp = math.ceil(adorine.mp)
    ran_af.hp = math.ceil(ran_af.hp)
    ran_af.mp = math.ceil(ran_af.mp)
    xoann.hp = math.ceil(xoann.hp)
    xoann.mp = math.ceil(xoann.mp)
    solou.hp = math.ceil(solou.hp)
    solou.mp = math.ceil(solou.mp)
    chyme.hp = math.ceil(chyme.hp)
    chyme.mp = math.ceil(chyme.mp)

    if adorine.evad > 256:
        adorine.evad = 256
    if ran_af.evad > 256:
        ran_af.evad = 256
    if solou.evad > 256:
        solou.evad = 256
    if xoann.evad > 256:
        xoann.evad = 256
    if chyme.evad > 256:
        chyme.evad = 256
    if parsto.evad > 256:
        parsto.evad = 256

    if player.hp > 0 and player.status_ail == 'dead':
        player.status_ail = 'none'
    if solou.hp > 0 and solou.status_ail == 'dead':
        solou.status_ail = 'none'
    if xoann.hp > 0 and xoann.status_ail == 'dead':
        xoann.status_ail = 'none'
    if chyme.hp > 0 and chyme.status_ail == 'dead':
        chyme.status_ail = 'none'
    if parsto.hp > 0 and parsto.status_ail == 'dead':
        parsto.status_ail = 'none'
    if ran_af.hp > 0 and ran_af.status_ail == 'dead':
        ran_af.status_ail = 'none'
    if adorine.hp > 0 and adorine.status_ail == 'dead':
        adorine.status_ail = 'none'

    try:
        monster.hp = math.ceil(monster.hp)
        monster.mp = math.ceil(monster.mp)

        if monster.hp < 0:
            monster.hp = 0
        if monster.mp < 0:
            monster.mp = 0

        if monster.hp > monster.max_hp:
            monster.hp -= (monster.hp - monster.max_hp)
        if monster.mp > monster.max_mp:
            monster.mp -= (monster.mp - monster.max_mp)

        if monster.evad > 256:
            monster.evad = 256

        monster_2.hp = math.ceil(monster_2.hp)
        monster_2.mp = math.ceil(monster_2.mp)

        if monster_2.hp < 0:
            monster_2.hp = 0
        if monster_2.mp < 0:
            monster_2.mp = 0

        if monster_2.hp > monster_2.max_hp:
            monster_2.hp -= (monster_2.hp - monster_2.max_hp)
        if monster_2.mp > monster_2.max_mp:
            monster_2.mp -= (monster_2.mp - monster_2.max_mp)

        if monster_2.evad > 256:
            monster_2.evad = 256

        monster_3.hp = math.ceil(monster_3.hp)
        monster_3.mp = math.ceil(monster_3.mp)

        if monster_3.hp < 0:
            monster_3.hp = 0
        if monster_3.mp < 0:
            monster_3.mp = 0

        if monster_3.hp > monster_3.max_hp:
            monster_3.hp -= (monster_3.hp - monster_3.max_hp)
        if monster_3.mp > monster_3.max_mp:
            monster_3.mp -= (monster_3.mp - monster_3.max_mp)

        if monster_3.evad > 256:
            monster_3.evad = 256

    except (AttributeError, TypeError):
        if not any([isinstance(monster, str), isinstance(monster_2, str), isinstance(monster_3, str)]):
            raise


def serialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Save the "PlayableCharacter" objects as JSON files
    player.target = ''
    parsto.target = ''
    adorine.target = ''
    ran_af.target = ''
    xoann.target = ''
    solou.target = ''
    chyme.target = ''

    player.c_spell = ''
    parsto.c_spell = ''
    adorine.c_spell = ''
    ran_af.c_spell = ''
    xoann.c_spell = ''
    solou.c_spell = ''
    chyme.c_spell = ''

    player.c_ability = ''
    parsto.c_ability = ''
    adorine.c_ability = ''
    ran_af.c_ability = ''
    xoann.c_ability = ''
    solou.c_ability = ''
    chyme.c_ability = ''

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(player.__dict__, f, indent=4, separators=(', ', ': '))
    with open(s_path, mode='w', encoding='utf-8') as f:
        json.dump(solou.__dict__, f, indent=4, separators=(', ', ': '))
    with open(x_path, mode='w', encoding='utf-8') as f:
        json.dump(xoann.__dict__, f, indent=4, separators=(', ', ': '))
    with open(a_path, mode='w', encoding='utf-8') as f:
        json.dump(adorine.__dict__, f, indent=4, separators=(', ', ': '))
    with open(r_path, mode='w', encoding='utf-8') as f:
        json.dump(chyme.__dict__, f, indent=4, separators=(', ', ': '))
    with open(f_path, mode='w', encoding='utf-8') as f:
        json.dump(ran_af.__dict__, f, indent=4, separators=(', ', ': '))
    with open(p_path, mode='w', encoding='utf-8') as f:
        json.dump(parsto.__dict__, f, indent=4, separators=(', ', ': '))


def deserialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Load the JSON files and translate them into "PlayableCharacter" objects
    global player
    global solou
    global xoann
    global adorine
    global chyme
    global ran_af
    global parsto

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    solou = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    xoann = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    adorine = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    chyme = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    ran_af = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    parsto = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)

    with open(path, encoding='utf-8') as f:
        player.__dict__ = json.load(f)
    with open(s_path, encoding='utf-8') as f:
        solou.__dict__ = json.load(f)
    with open(x_path, encoding='utf-8') as f:
        xoann.__dict__ = json.load(f)
    with open(a_path, encoding='utf-8') as f:
        adorine.__dict__ = json.load(f)
    with open(r_path, encoding='utf-8') as f:
        chyme.__dict__ = json.load(f)
    with open(f_path, encoding='utf-8') as f:
        ran_af.__dict__ = json.load(f)
    with open(p_path, encoding='utf-8') as f:
        parsto.__dict__ = json.load(f)


def serialize_bosses(path):
    json_bosslist = {}

    for boss in boss_list:
        json_bosslist[boss.name] = boss.active

    with open(path, encoding='utf-8', mode='w') as i:
        json.dump(json_bosslist, i)


def deserialize_bosses(path):
    global boss_list

    with open(path, encoding='utf-8') as i:
        json_bosslist = json.load(i)

    for key in json_bosslist:
        for boss in boss_list:
            if key == boss.name:
                boss.active = json_bosslist[key]

player = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
solou = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
xoann = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
adorine = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
ran_af = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
parsto = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
chyme = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
monster = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
monster_2 = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
monster_3 = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
