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

import copy
import json
import math
import random
import re
import sys

import pygame

import dialogue
import abilities
import ascii_art
import battle
import items
import magic
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

        self.status_ail = ['alive']  # Current Status Ailment
        self.max_hp = copy.copy(self.hp)
        self.max_mp = copy.copy(self.mp)


class PlayableCharacter(Unit):
    # A class for characters whose main.s_input can be directly controlled by the player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad, class_='', enabled=True):
        Unit.__init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)

        self.class_ = class_         # PCU's Class
        self.off_element = 'none'    # PCU's Element
        self.def_element = 'none'    # PCU's Element
        self.enabled = enabled       # Whether the PCU has been recruited or not
        self.exp = 0                 # Experience
        self.req_xp = 3              # Required XP to level up
        self.move = ''               # What move the character chose during battle
        self.ap = 10                 # The number of "Action Points" that the user has remaining
        self.max_ap = 10             # The number of maximum Action Points the user can have at one time

        self.target = Monster('', '', '', '', '', '', '', '', '', '', '')  # The target of the PCU's current action
        self.c_ability = abilities.Ability('', '', '')  # The ability that the PCU is currently casting
        self.c_spell = magic.Spell('', '', '', '', '', '')  # The spell that the PCU is currently casting

        self.attributes = {'int': 1,  # Intelligence, for Mages
                           'wis': 1,  # Wisdom, for Paladins
                           'str': 1,  # Strength, for Warriors
                           'con': 1,  # Constitution, for Monks
                           'dex': 1,  # Dexterity, for Assassins
                           'per': 1,  # Perception, for Rangers
                           'fte': 1}  # Fate

        # This dictionary will contain numerous variables that interact with abilties in battle
        self.ability_vars = {'ascend_used': False,
                             'berserk': False,
                             'rolling': False}

    def choose_name(self):
        while True:
            # Ask the player for their name, and remove any non alphanumeric/dash characters from it
            # Also remove beginning/ending whitespace, and repeated spaces
            choice1 = main.s_input('What is your name, young adventurer? | Input Name: ')
            choice2 = ' '.join(re.sub('[^\w\-_ ]', '', choice1).split())

            # If your original choice contained characters, but the filtered version didn't,
            # this message will pop up.
            if choice1 and not choice2:
                print("I'm sorry, I didn't quite catch that.")
                main.s_input('\nPress enter/return ')
                print('-'*save_load.divider_size)
                continue

            # You can't name yourself nothing. Sorry but that's the rules.
            if not (choice1 or choice2):
                continue

            self.name = choice2

            while True:
                if self.name.lower() == 'y':
                    print("""Your name's "y", eh? Must be in a hurry.""")
                    main.s_input('\nPress enter/return ')
                    print('-' * save_load.divider_size)

                elif self.name.lower() in main.friend_names:
                    print(f"Ah, {self.name}! My dear friend, it is great to see you again!")
                    main.s_input('\nPress enter/return ')
                    print('-' * save_load.divider_size)

                elif self.name.lower() == "frisk":
                    print("Frisk? Sorry, no hard mode for you in this game.")
                    main.s_input('\nPress enter/return ')
                    print('-' * save_load.divider_size)

                else:
                    y_n = main.s_input(f'So, your name is "{self.name}?" | Y/N: ').lower()

                    if y_n.startswith('n'):
                        print('-'*save_load.divider_size)
                        self.name = ''
                        break

                    elif not y_n.startswith('y'):
                        continue

                    print('-'*save_load.divider_size)

                return

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
            pygame.mixer.music.load('../Music/Adventures in Pixels.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(save_load.music_vol)

            rem_points = 0  # Remaining Skill Points
            while self.exp >= self.req_xp:
                print('-'*save_load.divider_size)
                self.lvl += 1
                print(f"{self.name} has advanced to level {self.lvl}!")

                rem_points += 5
                magic.new_spells(self)

                if self.class_ == 'warrior':
                    self.attk += 3
                    self.dfns += 3
                    self.m_attk += 1
                    self.m_dfns += 1
                    self.p_dfns += 3
                    self.spd += 1
                    self.evad += 1
                    self.max_hp += 2
                    self.max_mp += 1

                elif self.class_ == 'mage':
                    self.p_dfns += 1
                    self.p_attk += 2
                    self.m_attk += 3
                    self.m_dfns += 3
                    self.dfns += 1
                    self.spd += 1
                    self.evad += 1
                    self.max_hp += 1
                    self.max_mp += 3

                elif self.class_ == 'assassin':
                    self.p_dfns += 2
                    self.attk += 3
                    self.dfns += 1
                    self.m_attk += 1
                    self.m_dfns += 1
                    self.spd += 3
                    self.evad += 3
                    self.max_hp += 1
                    self.max_mp += 1

                elif self.class_ == 'ranger':
                    self.p_attk += 3
                    self.p_dfns += 1
                    self.m_attk += 1
                    self.m_dfns += 1
                    self.dfns += 1
                    self.spd += 3
                    self.evad += 3
                    self.max_hp += 1
                    self.max_mp += 2

                elif self.class_ == 'monk':
                    self.p_dfns += 1
                    self.attk += 3
                    self.dfns += 1
                    self.m_attk += 1
                    self.m_dfns += 1
                    self.spd += 3
                    self.evad += 3
                    self.max_hp += 1
                    self.max_mp += 2

                elif self.class_ == 'paladin':
                    self.p_dfns += 1
                    self.attk += 1
                    self.dfns += 3
                    self.m_attk += 1
                    self.m_dfns += 3
                    self.spd += 1
                    self.evad += 1
                    self.max_hp += 3
                    self.max_mp += 2

                self.exp -= self.req_xp
                self.req_xp = math.ceil((math.pow(self.lvl*2, 2) - self.lvl))

                fix_stats()

            # The player restores all their health and mana when they level up
            self.hp = copy.copy(self.max_hp)
            self.mp = copy.copy(self.max_mp)
            self.status_ail = ['alive']

            print('-'*save_load.divider_size)
            self.skill_points(rem_points)
            print('-'*save_load.divider_size)

            save_load.save_game()

            return

    def skill_points(self, rem_points):
        while rem_points > 0:
            print(f"{self.name} has {rem_points} skill point{'s' if rem_points > 1 else ''} left to spend.")

            skill = main.s_input("""Choose a skill to increase:
      [1] INTELLIGENCE, The attribute of MAGES
      [2] WIDSOM, the attribute of PALADINS
      [3] STRENGTH,The attribute of WARRIORS
      [4] CONSTITUTION, the attribute of MONKS
      [5] DEXTERITY, the attribute of ASSASSINS
      [6] PERCEPTION, the attribute of RANGERS
      [7] FATE, the forgotten attribute
      [8] DIFFICULTY, the forbidden attribute
Input [#]: """).lower()

            if skill and skill[0] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                if skill[0] == '1':
                    act_skill = 'int'
                    vis_skill = 'INTELLIGENCE'
                    message = """\
Increasing INTELLIGENCE will provide:
    +1 Magic Attack
    +1 Magic Defense
    +1 MP
    +Mage Ability Power"""

                elif skill[0] == '2':
                    act_skill = 'wis'
                    vis_skill = 'WISDOM'
                    message = """\
Increasing WISDOM will provide:
    +1 Heal from healing spells (Non-paladins)
    +2 Heal from healing spells (Paladins)
    +2 MP
    +Paladin Ability Power"""

                elif skill[0] == '3':
                    act_skill = 'str'
                    vis_skill = 'STRENGTH'
                    message = """\
Increasing STRENGTH will provide:
    +1 Physical Attack
    +1 Physical Defense
    +1 Pierce Defense
    +Warrior Ability Power"""

                elif skill[0] == '4':
                    act_skill = 'con'
                    vis_skill = 'CONSTITUTION'
                    message = """\
Increasing CONSTITUTION will provide:
    +1 HP
    +1 Physical Defense
    +1 Pierce Defense
    +1 Magic Defense
    +Monk Ability Power"""

                elif skill[0] == '5':
                    act_skill = 'dex'
                    vis_skill = 'DEXTERITY'
                    message = """\
Increasing DEXTERITY will provide:
    +1 Physical Attack
    +1 Speed
    +1 Evasion
    +Assassin Ability Power"""

                elif skill[0] == '6':
                    act_skill = 'per'
                    vis_skill = 'PERCEPTION'
                    message = """\
Increasing PERCEPTION will provide:
    +1 Pierce Attack
    +1 Pierce Defense
    +1 Evasion
    +Ranger Ability Power"""

                elif skill[0] == '7':
                    act_skill = 'fte'
                    vis_skill = 'FATE'
                    message = """\
Increasing FATE will provide:
    +1 to a random attribute (won't choose DIFFICULTY or FATE)
    +1 to a second random attribute (won't choose DIFFICULTY or FATE)
    +Knowledge that your destiny is predetermined and nothing matters"""

                elif skill[0] == '8':
                    act_skill = "dif"
                    vis_skill = "DIFFICULTY"
                    message = """\
Increasing DIFFICULTY will provide:
    +0.5% Enemy Physical Attack (Applies to entire party)
    +0.5% Enemy Pierce Attack (Applies to entire party)
    +0.5% Enemy Magic Attack (Applies to entire party)
    +More challenging experience"""

                print('-'*save_load.divider_size)

                if act_skill == 'dif':
                    print(f"Current {vis_skill}: {main.party_info['dif']}")

                else:
                    print(f"Current {vis_skill}: {self.attributes[act_skill]}")

                print(message)
                print('-'*save_load.divider_size)

                while True:
                    y_n = main.s_input(f"Increase {self.name}'s {vis_skill}? | Y/N: ").lower()

                    if y_n.startswith('n'):
                        print('-'*save_load.divider_size)
                        break

                    elif y_n.startswith('y'):
                        self.increase_attribute(act_skill)

                    else:
                        continue

                    if act_skill == 'dif':
                        print('-'*save_load.divider_size)
                        print("Difficulty increased!")
                        print("The enemies of your world have grown in power!")

                    if act_skill != 'fte':
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
Level: {self.lvl} | Class: {self.class_.title()}
HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp} | Statuses: {', '.join([x.title() for x in self.status_ail])}
Physical Attack: {self.attk} | Magic Attack: {self.m_attk} | Pierce Attack {self.p_attk}
Phsyical Defense: {self.dfns} | Magic Defense: {self.m_dfns} | Pierce Defense {self.p_dfns}
Speed: {self.spd} | Evasion: {self.evad}
XP: {self.exp}/{self.req_xp} | GP: {main.party_info['gp']}

-Attributes-
Intelligence: {self.attributes['int']} 
Wisdom: {self.attributes['wis']}
Strength: {self.attributes['str']}
Constitution: {self.attributes['con']}
Dexterity: {self.attributes['dex']}
Perception: {self.attributes['per']}
Difficulty: {main.party_info['dif']}

-Equipment-
Weapon: {items.equipped[inv_name]['weapon'].name}
Accessory: {items.equipped[inv_name]['access'].name}
Armor:
  Head: {items.equipped[inv_name]['head'].name}
  Body: {items.equipped[inv_name]['body'].name}
  Legs: {items.equipped[inv_name]['legs'].name}
Defensive Element: {self.def_element.title()} | Offensive Element: {self.off_element.title()}""")

        main.s_input('\nPress enter/return ')

    def battle_turn(self):
        sounds.item_pickup.stop()

        # If the player's target is an enemy, and the target died before the player's turn began,
        # then the attack automatically redirects to a random living enemy.
        if isinstance(self.target, Monster) and 'dead' in self.target.status_ail:
            self.target = random.choice([x for x in battle.m_list if 'dead' not in x.status_ail])

        inv_name = self.name if self != player else 'player'
        player_weapon = items.equipped[inv_name]['weapon']

        print(f"-{self.name}'s Turn-")

        # PCUs regain 1 Action Point per turn. This regeneration is paused on turns where
        # the player uses an ability.
        if self.move != '3':
            self.ap += 1

        # Check to see if the PCU is poisoned
        if 'poisoned' in self.status_ail and monster.hp > 0:
            main.smart_sleep(0.75)
            sounds.poison_damage.play()
            poison_damage = math.floor(self.hp/5)
            self.hp -= poison_damage

            print(f'{self.name} took poison damage! (-{poison_damage} HP)')

            if self.hp <= 0:
                return

        for x in self.status_ail:
            if x != "alive" and random.randint(0, 3) == 3:
                sounds.buff_spell.play()
                self.status_ail = [y for y in self.status_ail if y != x]
                print(f"{self.name} is no longer {x}!")
                main.smart_sleep(0.5)
                break

        # Basic Attack
        if self.move == '1':
            print(ascii_art.player_art[self.class_.title()] % f"{self.name} is making a move!\n")

            if items.equipped[inv_name]['weapon'].type_ == 'melee':
                sounds.sword_slash.play()
                print(f'{self.name} fiercely attacks the {self.target.name} using their {player_weapon.name}...')

            else:
                sounds.aim_weapon.play()
                print(f'{self.name} aims carefully at the {self.target.name} using their {player_weapon.name}...')

            main.smart_sleep(0.75)

            if items.equipped[inv_name]['weapon'].type_ == 'melee':
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
            pygame.mixer.music.load(main.party_info['music'])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(save_load.music_vol)

            return 'Ran'

        return

    def player_choice(self):
        print(battle_options.format(self.name))

        while True:
            self.move = main.s_input("Input [#]: ")

            try:
                self.move = ''.join([char for char in self.move if char.isnumeric])[0]

            except IndexError:
                continue

            # Standard Attack
            if self.move == '1':
                self.choose_target(f"Who should {self.name} attack?")
                return

            # Use Magic
            elif self.move == '2':
                print('-'*save_load.divider_size)

                # Silence is a status ailment that prevents using spells
                if 'silenced' in self.status_ail:
                    sounds.debuff.play()
                    print(f"{self.name} can't use spells when silenced!")
                    main.s_input("\nPress enter/return ")
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
                    print(f"{self.name}'s Abilities | {self.ap}/{self.max_ap} AP remaining")

                    # List of all abilities usable by the PCU's class
                    all_abilities = abilities.a_abilities[self.class_] + \
                        abilities.a_abilities['player' if self == player else self.name]

                    # This is used to make sure that the AP costs of each ability line up. Purely asthetic.
                    padding = len(max(all_abilities, key=lambda x: x.name).name)

                    # Print out the list of abilities the player's class can uses
                    for num, ability in enumerate(all_abilities):
                        real_pad = padding - len(ability.name)
                        print(f"      [{num + 1}] {ability.name} {'-'*real_pad}--> {ability.ap_cost} AP")

                    while True:
                        try:
                            chosen = main.s_input('Input [#] (or type "back"): ').lower()
                            self.c_ability = all_abilities[int(chosen) - 1]

                            # Abilities cost AP to cast, just like spells cost MP.
                            if self.ap < self.c_ability.ap_cost:
                                print('-'*save_load.divider_size)
                                print(f"{self.name} doesn't have enough AP to cast {self.c_ability.name}!")
                                main.s_input("\nPress enter/return ")

                                break

                            # Ascend is an ability that is more powerful the later in the battle you use it.
                            # To balance this it's only usable once per battle.
                            elif self.c_ability == abilities.ascend and self.ability_vars['ascend_used']:
                                print('-'*save_load.divider_size)
                                print("Ascend can only be used once per battle.")
                                main.s_input("\nPress enter/return ")
                                break

                        except (IndexError, ValueError):
                            if chosen in ['e', 'x', 'exit', 'b', 'back']:
                                print('-'*save_load.divider_size)
                                print(battle_options.format(self.name))
                                do_loop = False
                                break

                            continue

                        self.ap -= self.c_ability.ap_cost
                        self.c_ability.before_ability(self)
                        return

            # Use Items
            elif self.move == '4':
                print('-'*save_load.divider_size)

                # You can only use consumable items during battle
                if not items.inventory['consumables']:
                    print('Your party has no consumables!')
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)
                    print(battle_options.format(self.name))

                    continue

                # Mute is a status ailment that prevents using items
                if 'muted' in self.status_ail:
                    sounds.debuff.play()
                    print(f"{self.name} can't use items when muted!")
                    main.s_input("\nPress enter/return ")
                    print('-'*save_load.divider_size)
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

    def choose_target(self, action_desc, ally=False, enemy=True, allow_dead=False):
        # choose_target is a function that lets the player choose what unit to target with their next action
        pcu_list = [x for x in [player,
                                solou,
                                chili,
                                chyme,
                                ran_af,
                                adorine,
                                parsto] if x.enabled and (True if 'dead' not in x.status_ail or allow_dead else False)]

        # Do this if the player is allowed to target enemies but not allies (e.g. attacks, some spells/abilities)
        if enemy and not ally:
            if len([x for x in battle.m_list if 'dead' not in x.status_ail]) == 1:
                self.target = [x for x in battle.m_list if 'dead' not in x.status_ail][0]

                return

            this_list = [x for x in battle.m_list if 'dead' not in x.status_ail]

        # Do this if the player is allowed to target allies but not enemies (e.g. items, some spells/abilities)
        elif ally and not enemy:
            if len(pcu_list) == 1:
                self.target = pcu_list[0]

                return

            this_list = pcu_list

        # Do this if both allies and enemies are valid targets (e.g. some abilities and spells)
        elif ally and enemy:
            this_list = pcu_list + [x for x in battle.m_list if 'dead' not in x.status_ail]

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
        if attribute == 'int':
            self.m_dfns += 1
            self.m_attk += 1
            self.max_mp += 1
            self.attributes['int'] += 1

        elif attribute == 'wis':
            self.max_mp += 2
            self.attributes['wis'] += 1

        elif attribute == 'str':
            self.attk += 1
            self.p_dfns += 1
            self.dfns += 1
            self.attributes['str'] += 1

        elif attribute == 'con':
            self.max_hp += 1
            self.dfns += 1
            self.p_dfns += 1
            self.m_dfns += 1
            self.attributes['con'] += 1

        elif attribute == 'dex':
            self.attk += 1
            self.spd += 1
            self.evad += 1
            self.attributes['dex'] += 1

        elif attribute == 'per':
            self.p_attk += 1
            self.p_dfns += 1
            self.evad += 1
            self.attributes['per'] += 1

        elif attribute == 'fte':
            # Fate gives you 1 point in two randomly chosen attributes. Can choose the same attribute twice.
            # Cannot choose Fate or Difficulty as the attribute.
            self.attributes['fte'] += 1
            rand_attr1 = random.choice([('int', 'Intelligence'),
                                        ('wis', 'Wisdom'),
                                        ('str', 'Strength'),
                                        ('con', 'Constitution'),
                                        ('dex', 'Dexterity'),
                                        ('per', 'Perception')])

            rand_attr2 = random.choice([('int', 'Intelligence'),
                                        ('wis', 'Wisdom'),
                                        ('str', 'Strength'),
                                        ('con', 'Constitution'),
                                        ('dex', 'Dexterity'),
                                        ('per', 'Perception')])

            self.increase_attribute(rand_attr1[0])
            self.increase_attribute(rand_attr2[0])

            print('-'*save_load.divider_size)
            print(f"{self.name} gained one point in {rand_attr1[1]} from FATE!")
            print(f"{self.name} gained one point in {rand_attr2[1]} from FATE!")
            main.s_input("\nPress enter/return ")

        elif attribute == 'dif':
            main.party_info['dif'] += 1

    def reset_ability_vars(self):
        self.ability_vars = {'ascend_used': False,
                             'berserk': False,
                             'rolling': False}


class Monster(Unit):
    # All monsters use this class. Bosses use a sub-class called "Boss" which inherits from this.

    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        Unit.__init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)
        self.status = ''  # The status effect that will be applied to the player if RNGsus wills it
        self.is_poisoned = False
        self.is_defending = False
        self.class_ = None

        self.off_element = 'none'
        self.def_element = 'none'

        self.gold = 0
        self.experience = 0
        self.items = 0

        # This dictionary contains numerous variables that interact with abilties in battle
        self.ability_vars = {
            'poison_pow': 0,
            'poison_dex': 0,
            'disarmed': False,
            'knockout_turns': 0,
            'judgement_day': 0,
            'taunted': [0, None],
            'drained': False}

    def give_status(self, target):
        # Attempt to give the target a status ailment
        status = random.choice([x for x in ['poisoned',
                                            'silenced',
                                            'weakened',
                                            'blinded',
                                            'paralyzed',
                                            'muted'] if x not in target.status_ail])

        print(f'The {self.name} is attempting to make {self.m_target.name} {status}...')
        sounds.aim_weapon.play()
        main.smart_sleep(0.75)

        # There's a 50% chance that the status spell will work
        if random.randint(0, 1) == 1:
            sounds.buff_spell.play()
            print(f'{self.m_target.name} is now {status}!')
            target.status_ail.append(status)

        else:
            sounds.debuff.play()
            print(f'The {self.name} failed to make {self.m_target.name} {status}!')

        self.mp -= self.max_mp*0.1

    def monster_generation(self):
        m_type = {'forest': ['Goblin Archer', 'Spriggan', 'Imp', 'Bat', 'Beetle'],

                  'shore': ['Shell Mimic', 'Giant Crab', 'Naiad', 'Sea Serpent', 'Squid'],

                  'tundra': ['Ice Soldier', 'Minor Yeti', 'Corrupt Thaumaturge', 'Arctic Wolf', 'Frost Bat'],

                  'swamp': ['Bog Slime', 'Moss Ogre', "Will-o'-the-wisp", 'Vine Lizard', 'Sludge Rat'],

                  'desert': ['Mummy', 'Sand Golem', 'Anubis', 'Fire Ant', 'Naga'],

                  'mountain': ['Troll', 'Rock Giant', 'Oread', 'Tengu', 'Giant Worm'],

                  'graveyard': ['Zombie', 'Undead Archer', 'Necromancer', 'Skeleton', 'Ghoul'],

                  'sky': ['Alicorn', 'Griffin', 'Wraith', 'Harpy', 'Flying Serpent']
                  }

        if player.name.lower() in main.friend_names:
            m_type['forest'].append("Calculator")

        self.name = random.choice(m_type[main.party_info['biome']])

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

        if main.party_info['biome'] == 'forest':
            self.def_element = 'electric'
            self.off_element = 'electric'

        elif main.party_info['biome'] == 'tundra':
            self.def_element = 'ice'
            self.off_element = 'ice'

        elif main.party_info['biome'] == 'desert':
            self.def_element = 'fire'
            self.off_element = 'fire'

        elif main.party_info['biome'] == 'mountain':
            self.def_element = 'earth'
            self.off_element = 'earth'

        elif main.party_info['biome'] == 'shore':
            self.def_element = 'water'
            self.off_element = 'water'

        elif main.party_info['biome'] == 'swamp':
            self.def_element = 'grass'
            self.off_element = 'grass'

        elif main.party_info['biome'] == 'graveyard':
            self.def_element = 'death'
            self.off_element = 'death'

        elif main.party_info['biome'] == 'sky':
            self.def_element = 'wind'
            self.off_element = 'wind'

        # Give the monster a set of items to drop if RNGsus wills it
        if random.randint(0, 4) == 0:  # 20% chance
            self.items = random.choice(items.monster_drop_list[self.name])

    def monster_level(self):
        self.lvl = main.party_info['current_tile'].m_level

        for x in range(1, self.lvl):
            self.hp += 5
            self.mp += 3
            self.attk += 3
            self.dfns += 3
            self.p_attk += 3
            self.p_dfns += 3
            self.m_attk += 3
            self.m_dfns += 3
            self.spd += 3
            self.evad += 2

        self.max_hp = self.hp
        self.max_mp = self.mp

    def monster_modifiers(self):
        # Monsters with >40 level are called "Greater"
        # Monsters with <10 level are called "Lesser"
        # Goblins also randomly have a chance to be "Whipsering", which is an inside joke with a friend of mine
        self.m_name = copy.copy(self.name)

        if self.name == "Goblin" and random.randint(0, 50) == 42:
            self.name = ''.join(["Whispering ", self.name])

        elif self.lvl < 10:
            self.name = ''.join(["Lesser ", self.name])

        elif self.lvl > 40:
            self.name = ''.join(["Greater ", self.name])

        # Monsters are given one of 14 different "modifiers", which increase/decrease some of their stats
        # This is to help spice up the game and make it less predictable
        modifier = random.choice(['Slow', 'Fast',
                                  'Nimble', 'Clumsy',
                                  'Powerful', 'Ineffective',
                                  'Armored', 'Broken',
                                  'Mystic', 'Foolish',
                                  'Strong', 'Weak',
                                  'Observant', 'Obtuse'])

        if modifier == "Slow":  # Very-low speed, below-average speed
            self.spd /= 1.3
            self.evad /= 1.1
        elif modifier == "Fast":  # Very-high speed, above-average speed
            self.spd *= 1.3
            self.evad *= 1.1
        elif modifier == "Nimble":  # Very-high evasion, above-average speed
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

    def monster_class_stats(self):
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

        elif self.name in melee_enemies:
            self.battle_turn = self.melee_ai

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

        elif self.name in ranged_enemies:
            self.battle_turn = self.ranged_ai

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
        # Set stats for melee-class monsters

    def monster_difficulty(self):
        self.attk += self.attk*0.0005*main.party_info['dif']
        self.m_attk += self.m_attk*0.0005*main.party_info['dif']
        self.p_attk += self.p_attk*0.0005*main.party_info['dif']

    def monster_fix_stats(self):
        # Adjust for problems that may happen with enemy stats
        self.attk = max(1, math.ceil(self.attk))
        self.dfns = max(1, math.ceil(self.dfns))
        self.p_attk = max(1, math.ceil(self.p_attk))
        self.p_dfns = max(1, math.ceil(self.p_dfns))
        self.m_attk = max(1, math.ceil(self.m_attk))
        self.m_dfns = max(1, math.ceil(self.m_dfns))
        self.spd = max(1, math.ceil(self.spd))
        self.evad = max(1, math.ceil(self.evad))
        self.mp = max(1, math.ceil(self.mp))
        self.max_mp = max(1, math.ceil(self.max_mp))
        self.hp = max(1, math.ceil(self.hp))
        self.max_hp = max(1, math.ceil(self.max_hp))

    def base_turn(self):
        sounds.item_pickup.stop()
        self.get_target()

        print(f"-{self.name}'s Turn-")

        if not self.ability_vars['knockout_turns']:
            print(ascii_art.monster_art[self.m_name] % f"The {self.name} is making a move!\n")

        else:
            print(f"The {self.name} is asleep!")

        if not self.ability_vars['knockout_turns']:
            self.battle_turn()

        self.do_abilities()

    def do_abilities(self):
        if self.ability_vars['knockout_turns']:
            self.ability_vars['knockout_turns'] -= 1

            if not self.ability_vars['knockout_turns']:
                main.smart_sleep(0.5)
                sounds.buff_spell.play()
                self.status_ail = [x for x in self.status_ail if x != "asleep"]
                print(f"The {self.name} woke up!")

            else:
                chance = 25 if isinstance(self, Boss) else 10

                if random.randint(0, 100) < chance:
                    main.smart_sleep(0.5)
                    sounds.buff_spell.play()
                    self.ability_vars['knockout_turns'] = 0
                    self.status_ail = [x for x in self.status_ail if x != "asleep"]
                    print(f"The {self.name} woke up early!")

        if 'poisoned' in self.status_ail:
            main.smart_sleep(0.5)
            damage = math.ceil(self.ability_vars['poison_pow']*self.max_hp + self.ability_vars['poison_dex'])
            self.hp -= damage
            print(f"The {self.name} took {damage} damage from poison!")
            sounds.poison_damage.play()

        if self.ability_vars['judgement_day'] == battle.turn_counter:
            main.smart_sleep(0.5)
            print(f"{self.name}'s judgement day has arrived. The darkness devours it...")
            sounds.poison_damage.play()
            self.hp = 0

    def get_target(self):
        self.m_target = random.choice([x for x in [
                                       player,
                                       solou,
                                       chili,
                                       chyme,
                                       ran_af,
                                       parsto,
                                       adorine
                                       ] if x.enabled and 'dead' not in x.status_ail])

        if self.ability_vars['taunted'][0] == battle.turn_counter:
            self.m_target = self.ability_vars['taunted'][1]

    def magic_ai(self):
        # 16.67% chance for the enemy to give a status ailment
        if not self.ability_vars['taunted'][0] == battle.turn_counter or 'silenced' in self.status_ail:
            if random.randint(0, 7) == 0 and self.mp >= self.max_mp*0.1:
                self.give_status(self.m_target)

                return

            # Magic heal
            elif self.hp <= self.max_hp/5 and self.mp >= self.max_mp*0.2:
                print(f'The {self.name} is casting a healing spell on itself...')
                main.smart_sleep(0.75)

                healing_power = math.ceil(max([self.hp*0.2, 5]))
                self.hp += min([self.hp*0.2, 5])
                self.mp -= self.max_mp*0.2

                print(f'The {self.name} heals itself for {healing_power} HP!')
                sounds.magic_healing.play()

                return

            # Magic Attack
            elif self.mp >= self.max_mp*0.15:

                sounds.magic_attack.play()

                print(f'The {self.name} is preparing to cast a spell on {self.m_target.name}!')
                main.smart_sleep(0.75)

                dam_dealt = deal_damage(self, self.m_target, "magical")

                if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                    sounds.enemy_hit.play()
                    print(f"The {self.name}'s spell deals {dam_dealt} damage to {self.m_target.name}!")

                    self.m_target.hp -= dam_dealt

                else:
                    sounds.attack_miss.play()
                    print(f"The {self.name}'s spell narrowly misses {self.m_target.name}!")

                self.mp -= self.max_mp*0.15

                return

        # Non-magical Attack (Pierce Damage). Only happens if taunted, silenced, or if out of mana.
        sounds.aim_weapon.play()
        print(f'The {self.name} {self.attk_msg} {self.m_target.name}')

        main.smart_sleep(0.75)

        dam_dealt = deal_damage(self, self.m_target, "piercing")

        if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
            sounds.enemy_hit.play()
            print(f"The {self.name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

            self.m_target.hp -= dam_dealt

        else:
            sounds.attack_miss.play()
            print(f"The {self.name}'s attack narrowly misses {self.m_target.name}!")

    def ranged_ai(self):
        # At the moment, Ranged monsters are only capable of attacking
        print(f'The {self.name} {self.attk_msg} {self.m_target.name}!')
        sounds.aim_weapon.play()

        main.smart_sleep(0.75)

        if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
            dam_dealt = deal_damage(self, self.m_target, 'piercing')

            print(f"The {self.name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

            self.m_target.hp -= dam_dealt
            sounds.enemy_hit.play()

        else:
            sounds.attack_miss.play()
            print(f"The {self.name}'s attack narrowly misses {self.m_target.name}!")

    def melee_ai(self):
        # Melee monsters have a 1 in 6 (16.667%) chance to defend
        if random.randint(0, 5) == 0 and not self.is_defending \
                and not self.ability_vars['taunted'][0] == battle.turn_counter:
            self.is_defending = True
            print(f"The {self.name} is preparing itself for enemy attacks...")
            main.smart_sleep(0.75)

            self.dfns *= 2
            self.m_dfns *= 2
            self.p_dfns *= 2

            print(f"The {self.name}'s defense stats increased by 2x for one turn!")
            sounds.buff_spell.play()

        # Set defense back to normal if the monster defended last turn
        elif self.is_defending:
            print(f"The {self.name} stops defending, returning its defense stats to normal.")
            self.is_defending = False
            self.dfns /= 2
            self.m_dfns /= 2
            self.p_dfns /= 2

        # If the monster doesn't defend, then it will attack!
        if not self.is_defending:
            sounds.sword_slash.play()
            print(f'The {self.name} {self.attk_msg} {self.m_target.name}!')
            main.smart_sleep(0.75)

            dam_dealt = deal_damage(self, self.m_target, "physical")
            if random.randint(1, 512) in range(battle.temp_stats[self.m_target.name]['evad'], 512):
                sounds.enemy_hit.play()
                print(f"The {self.name}'s attack deals {dam_dealt} damage to {self.m_target.name}!")

                self.m_target.hp -= dam_dealt

            else:
                sounds.attack_miss.play()
                print(f"The {self.name}'s attack narrowly misses {self.m_target.name}!")


class Boss(Monster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad, lvl, b_items, gold,
                 experience, attk_msg, active=True, off_element='none', def_element='none'):
        Monster.__init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)

        self.off_element = off_element
        self.def_element = def_element
        self.items = b_items
        self.active = active
        self.lvl = lvl
        self.experience = experience
        self.gold = gold
        self.attk_msg = attk_msg
        self.m_name = copy.copy(self.name)

    def max_stats(self):
        self.hp = copy.copy(self.max_hp)
        self.mp = copy.copy(self.max_mp)

        self.ability_vars = {
            'poison_pow': 0,
            'poison_dex': 0,
            'disarmed': False,
            'knockout_turns': 0,
            'judgement_day': 0,
            'taunted': [0, None],
            'drained': False}

        self.status_ail = ['alive']

    def upon_defeating(self):
        pass


# Boss: Master Slime -- Position: 0'N, 1'E
def mastslim_ud():
    dialogue.alfred_quest_1.finished = True
    dialogue.alfred_convo_2.active = False


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
    dialogue.stewson_quest_1.finished = True
    dialogue.stewson_convo_2.active = False


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
                     off_element='dark', def_element='dark', active=False)

menac_phantom.battle_turn = menac_phantom.magic_ai
menac_phantom.upon_defeating = menacphan_ud


# Boss: Terrible Tarantuloid -- Position: -23'S, -11'W  (Adventure in Pixels)
def terrtar_ud():
    dialogue.krystin_convo_2.active = False
    dialogue.krystin_convo_3.active = True
    dialogue.kyle_convo_2.active = False
    dialogue.kyle_convo_3.active = True
    dialogue.alden_convo_1.active = False
    dialogue.alden_convo_2.active = True


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
    dialogue.rivesh_convo_3.active = False
    dialogue.rivesh_quest_1.finished = True


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
                    off_element='dark', def_element='dark', active=False)

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
                 off_element='grass', def_element='grass', active=True)

giant_ent.battle_turn = giant_ent.melee_ai

boss_list = [whisp_goblin, master_slime, menac_phantom, terr_tarant, cursed_spect, giant_ent]
defeated_bosses = []  # Make sure you can only defeat the boss one time


def check_bosses():
    global monster

    for boss in main.party_info['current_tile'].boss_list:
        if boss.name not in defeated_bosses and boss.active:
            print('-'*save_load.divider_size)
            print('You feel the presence of an unknown entity...')

            while True:
                y_n = main.s_input('Do you wish to investigate? | Y/N: ').lower()

                if y_n.startswith('y'):
                    monster = boss
                    boss.max_stats()
                    print('-'*save_load.divider_size)

                    battle.battle_system(is_boss=True)

                    return True

                elif y_n.startswith('n'):
                    return True

    else:
        return False


def deal_damage(attacker, target, damage_type, spell_power=0, do_criticals=True):
    # Attacker - the Unit that is attacking
    # Target - the Unit that is being attacked
    # Damage Type - the type of damage being dealt (magical, physical, or piercing)

    if isinstance(attacker, PlayableCharacter):
        t_equip = items.equipped[attacker.name if attacker != player else 'player']
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
        t_equip = items.equipped[target.name if target != player else 'player']
        resist = sum([t_equip[armor].defense for armor in t_equip if isinstance(t_equip[armor], items.Armor)])

        defense = battle.temp_stats[target.name]['dfns']
        p_defense = battle.temp_stats[target.name]['p_dfns']
        m_defense = battle.temp_stats[target.name]['m_dfns']

    else:
        defense = target.dfns
        p_defense = target.p_dfns
        m_defense = target.p_attk

        resist = 0

    if damage_type == 'physical':
        dam_dealt = (attack - defense/2)*(1 + resist)*(1 + weapon_dmg)

        # Weakeness reduces physical damage by 1/2
        if 'weakened' in attacker.status_ail:
            dam_dealt /= 2
            print(f"{attacker.name}'s weakness reduces their attack damage by half!")

        # Mages deal half damage with non-magical attacks
        if attacker.class_ == 'mage':
            dam_dealt /= 2

    elif damage_type == 'piercing':
        dam_dealt = (p_attack - p_defense/2)*(1 + resist)*(1 + weapon_dmg)

        # Blindness reduces piercing damage by 1/2
        if 'blinded' in attacker.status_ail:
            dam_dealt /= 2
            print(f"{attacker.name}'s blindness reduces their attack damage by half!")

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

    if random.randint(1, 100) <= 15 and do_criticals:
        dam_dealt *= 1.5
        sounds.critical_hit.play()
        print("It's a critical hit! 1.5x damage!")

        main.smart_sleep(0.5)

    dam_dealt = min(max(1, eval_element(attacker, target, dam_dealt)), 999)

    return math.ceil(dam_dealt)


def eval_element(attacker, target, damage):
    # Fire < Water < Electricity < Earth < Wind < Grass < Ice < Fire
    # Light < Dark and Dark < Light
    # "None" element is neutral to all elements
    # All other interactions are neutral

    # Set everything to be lowercase, just incase
    a_elem = attacker.off_element.lower()
    t_elem = target.def_element.lower()

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
    global chili
    global adorine
    global ran_af
    global parsto
    global chyme

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)

    # Pronounced "So-low"
    solou = PlayableCharacter('Solou', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='mage', enabled=False)
    # Pronounced "Zo-ann"
    chili = PlayableCharacter('Chili', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='assassin', enabled=False)
    # Pronounced "Adore-een"
    adorine = PlayableCharacter('Adorine', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='warrior', enabled=False)
    # Pronounced "Rahn-ahf"
    ran_af = PlayableCharacter("Ran'af", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='monk', enabled=False)
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
        items.equipped['player']['weapon'] = copy.copy(items.wdn_sht)

    elif player.class_ == "mage":
        player.max_hp += 1
        player.max_mp += 6
        player.m_attk += 4
        player.m_dfns += 3
        items.equipped['player']['weapon'] = copy.copy(items.mag_twg)

    elif player.class_ == "assassin":
        player.max_hp += 2
        player.max_mp += 1
        player.attk += 3
        player.dfns += 2
        player.spd += 4
        player.evad += 2
        items.equipped['player']['weapon'] = copy.copy(items.stn_dag)

    elif player.class_ == "ranger":
        player.max_mp += 2
        player.p_attk += 4
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        items.equipped['player']['weapon'] = copy.copy(items.slg_sht)

    elif player.class_ == "monk":
        player.max_hp += 2
        player.max_mp += 2
        player.attk += 3
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        player.dfns -= 1
        items.equipped['player']['weapon'] = copy.copy(items.fists)

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
        items.equipped['player']['weapon'] = copy.copy(items.rbr_mlt)

    player.hp = copy.copy(player.max_hp)
    player.mp = copy.copy(player.max_mp)

    save_load.save_game(verbose=False)


def spawn_monster():
    for unit_object in ['monster', 'monster_2', 'monster_3']:
        globals()[unit_object] = Monster('', 10, 5, 3, 2, 3, 2, 3, 2, 3, 2)
        globals()[unit_object].monster_generation()
        globals()[unit_object].monster_level()
        globals()[unit_object].monster_class_stats()
        globals()[unit_object].monster_modifiers()
        globals()[unit_object].monster_fix_stats()


def fix_stats():
    # Makes sure that that no-one ever has stats that would cause the game to malfunction.
    # e.g. no negative HP/MP/AP, no non-integer HP/MP/AP, etc.
    # This function also acts as a hard-cap for evasion, which is limited to a max of 256
    # (50% dodge chance). This is to prevent people from min-maxing their evasion to cheese
    # their way through the game, and also prevents monsters from being invincible.

    global player
    global solou
    global chili
    global chyme
    global parsto
    global ran_af
    global adorine
    global monster

    # Make an abbreviation for battle.temp_stats so a later part doesn't have to be muilti-line
    bts = battle.temp_stats

    for x in [player, solou, chili, chyme, parsto, ran_af, adorine]:
        x.hp, x.mp, x.ap = max(0, x.hp), max(0, x.mp), max(0, x.ap)
        x.hp, x.mp, x.ap = min(x.max_hp, x.hp), min(x.max_mp, x.mp), min(x.max_ap, x.ap)
        x.hp, x.mp, x.ap = math.ceil(x.hp), math.ceil(x.mp), math.ceil(x.ap)
        x.evad = min(256, x.evad)
        x.status_ail = list(set(x.status_ail))

        if isinstance(bts, dict):
            bts[x.name]['evad'] = min(512 if x.ability_vars['rolling'] else 256, bts[x.name]['evad'])

        if x.hp > 0 and 'dead' in x.status_ail:
            x.status_ail = ['alive']

        if 'dead' in x.status_ail:
            x.status_ail = ['dead']

    for y in battle.m_list:
        y.hp, y.mp = max(0, y.hp), max(0, y.mp)
        y.hp, y.mp = min(y.max_hp, y.hp), min(y.max_mp, y.mp)
        y.hp, y.mp = math.ceil(y.hp), math.ceil(y.mp)
        y.evad = min(256, y.evad)

        if y.hp > 0 and 'dead' in y.status_ail:
            y.status_ail = ['alive']

        if 'dead' in y.status_ail:
            y.status_ail = ['dead']


def heal_pcus(percentage):
    for pcu in [player,
                solou,
                chili,
                chyme,
                ran_af,
                parsto,
                adorine]:

        pcu.hp += pcu.max_hp*percentage
        pcu.mp += pcu.max_mp*percentage
        pcu.ap += pcu.max_ap*percentage
        pcu.status_ail = ['alive']

    fix_stats()


def serialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Save the "PlayableCharacter" objects as JSON files
    player.target = ''
    parsto.target = ''
    adorine.target = ''
    ran_af.target = ''
    chili.target = ''
    solou.target = ''
    chyme.target = ''

    player.c_spell = ''
    parsto.c_spell = ''
    adorine.c_spell = ''
    ran_af.c_spell = ''
    chili.c_spell = ''
    solou.c_spell = ''
    chyme.c_spell = ''

    player.c_ability = ''
    parsto.c_ability = ''
    adorine.c_ability = ''
    ran_af.c_ability = ''
    chili.c_ability = ''
    solou.c_ability = ''
    chyme.c_ability = ''

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(player.__dict__, f, indent=4, separators=(', ', ': '))
    with open(s_path, mode='w', encoding='utf-8') as f:
        json.dump(solou.__dict__, f, indent=4, separators=(', ', ': '))
    with open(x_path, mode='w', encoding='utf-8') as f:
        json.dump(chili.__dict__, f, indent=4, separators=(', ', ': '))
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
    global chili
    global adorine
    global chyme
    global ran_af
    global parsto

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    solou = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    chili = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    adorine = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    chyme = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    ran_af = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    parsto = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)

    with open(path, encoding='utf-8') as f:
        player.__dict__ = json.load(f)
    with open(s_path, encoding='utf-8') as f:
        solou.__dict__ = json.load(f)
    with open(x_path, encoding='utf-8') as f:
        chili.__dict__ = json.load(f)
    with open(a_path, encoding='utf-8') as f:
        adorine.__dict__ = json.load(f)
    with open(r_path, encoding='utf-8') as f:
        chyme.__dict__ = json.load(f)
    with open(f_path, encoding='utf-8') as f:
        ran_af.__dict__ = json.load(f)
    with open(p_path, encoding='utf-8') as f:
        parsto.__dict__ = json.load(f)

    for x in [player, solou, chili, adorine, chyme, ran_af, parsto]:
        x.reset_ability_vars()


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
chili = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
adorine = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
ran_af = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
parsto = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
chyme = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
monster = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
monster_2 = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
monster_3 = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
