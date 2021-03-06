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
import itertools

import pygame

import items
import dialogue
import abilities
import ascii_art
import battle
import magic
import save_load
import sounds
import tiles

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
    def __init__(self, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad):
        self.hp = hp              # Health
        self.mp = mp              # Mana Points
        self.attk = attk          # Physical Attack
        self.dfns = dfns          # Physical Defense
        self.p_attk = p_attk      # Pierce Attack
        self.p_dfns = p_dfns      # Pierce Defense
        self.m_attk = m_attk      # Magical Attack
        self.m_dfns = m_dfns      # Magical Defense
        self.spd = spd            # Speed
        self.evad = evad          # Evasion
        self.lvl = 1              # Level

        self.status_ail = ['alive']  # Current Status Ailment
        self.max_hp = copy.copy(self.hp)
        self.max_mp = copy.copy(self.mp)

        self.name = ''
        self.off_element = 'neutral'  # PCU's Element
        self.def_element = 'neutral'  # PCU's Element


class PlayableCharacter(Unit):
    # A class for characters whose main.s_input can be directly controlled by the player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad, class_='', enabled=True):
        super().__init__(hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)

        self.name = name
        self.class_ = class_          # PCU's Class
        self.enabled = enabled        # Whether the PCU has been recruited or not
        self.exp = 0                  # Experience
        self.req_xp = 3               # Required XP to level up
        self.move = ''                # What move the character chose during battle
        self.ap = 10                  # The number of "Action Points" that the user has remaining
        self.max_ap = 10              # The number of maximum Action Points the user can have at one time

        self.target = Monster('', '', '', '', '', '', '', '', '', '')  # The target of the PCU's current action
        self.c_ability = abilities.Ability('', '', '')  # The ability that the PCU is currently casting
        self.c_spell = magic.Spell('', '', '', '', '', '')  # The spell that the PCU is currently casting

        self.attributes = {'int': 1,  # Intelligence, for Mages
                           'wis': 1,  # Wisdom, for Paladins
                           'str': 1,  # Strength, for Warriors
                           'con': 1,  # Constitution, for Monks
                           'dex': 1,  # Dexterity, for Assassins
                           'per': 1,  # Perception, for Rangers
                           'cha': 1,  # Charisma, for Bards
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
      [1] Mage: Master of the arcane arts
      [2] Assassin: Proficient in both stealth and murder
      [3] Ranger: Fast and evasive, good with a bow
      [4] Paladin: Holy knight whose healing prowess is unmatched
      [5] Monk: Fighter whose fists are a worthy oppenent to any blade
      [6] Warrior: Excellent soldier, good balance of offense and defense
      [7] Bard: True team-player and master musician
Input [#]: """)

            try:
                class_ = {'1': "mage",
                          '2': "assassin",
                          '3': "ranger",
                          '4': "paladin",
                          '5': "monk",
                          '6': "warrior",
                          '7': "bard"}[class_]

                class_desc = {'mage': """\
    -Can use abilities that scale off Intelligence
    -Capable of learning every spell
    -Deals Pierce Damage with Standard Attacks
    -Deals 50% damage with Standard Attacks
    -High Magical Attack/Defense and MP
    -Average HP, Speed, and Evasion
    -Low Pierce Attack and Pierce/Physical Defense""",

                              'assassin': """\
    -Can use abilities that scale off Dexterity
    -Deals Physical Damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -High Speed, Physical Attack, and Evasion
    -Average HP, Pierce Defense, and Physical Defense
    -Low Magical Attack/Defense and MP""",

                              'ranger': """\
    -Can use abilities that scale off Perception
    -Deals Pierce Damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -High Pierce Attack, Speed, and Evasion
    -Average MP, HP, and Pierce Defense
    -Low HP, Pierce/Physcial Defense, and Magical Attack""",

                              'paladin': """\
    -Can use abilities that scale off Wisdom
    -Can learn all Healing spells and offensive Light spells
    -Deals Physical Damage with Standard Attacks
    -High Magical/Physical Defense
    -Average MP, HP, and Pierce Defense
    -Low Physical/Magical Attack, Speed, and Evasion""",

                              'monk': """\
    -Can use abilities that scale off Constitution
    -Capable of learning all Buff spells
    -Deals Physical damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -High Physical Attack, Speed, and Evasion
    -Average MP and Magical Attack
    -Low Pierce/Physical Defense and HP""",

                              'warrior': """\
    -Can use abilities that scale off Strength
    -Deals Physical Damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -High Pierce/Physical Defense and Physical Attack
    -Average HP
    -Low Magical Attack/Defense, Speed, Evasion, and MP""",

                              'bard': """\
    -Can use abilities that scale of Charisma
    -Deals Magical Damage with Standard Attacks
    -Deals 75% damage with Magical Spells
    -Has 6 Abilities instead of 4
    -High Evasion
    -Average MP, Speed, and Magical Defense
    -Low HP, Magical Attack, and Physical/Pierce Defense"""}[class_]

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
            sounds.play_music('../Music/Adventures in Pixels.ogg')

            rem_points = 0  # Remaining Skill Points
            while self.exp >= self.req_xp:
                print('-'*save_load.divider_size)
                self.lvl += 1
                print(f"{self.name} has advanced to level {self.lvl}!")

                rem_points += 3
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
                    self.p_dfns += 2
                    self.attk += 1
                    self.dfns += 3
                    self.m_attk += 1
                    self.m_dfns += 3
                    self.spd += 1
                    self.evad += 1
                    self.max_hp += 2
                    self.max_mp += 2

                elif self.class_ == 'bard':
                    self.p_dfns += 1
                    self.dfns += 1
                    self.m_attk += 1
                    self.m_dfns += 2
                    self.spd += 2
                    self.evad += 3
                    self.max_hp += 1
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
      [3] STRENGTH, The attribute of WARRIORS
      [4] CONSTITUTION, the attribute of MONKS
      [5] DEXTERITY, the attribute of ASSASSINS
      [6] PERCEPTION, the attribute of RANGERS
      [7] CHARISMA, the attribute of BARDS
      [8] FATE, the forgotten attribute
      [9] DIFFICULTY, the forbidden attribute
Input [#]: """).lower()

            if skill and skill[0] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                if skill[0] == '1':
                    act_skill = 'int'
                    vis_skill = 'INTELLIGENCE'
                    message = """\
Increasing INTELLIGENCE will provide:
    +1 Magical Attack
    +1 Magical Defense
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
    +1 Magical Defense
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
                    act_skill = 'cha'
                    vis_skill = 'CHARISMA'
                    message = """\
Increasing CHARISMA will provide:
    +Items cost 1% less (caps at 50% original cost)
    +Items sell for 1% more (caps at 200% original sell value)
    +Only the highest CHARISMA in party contributes to these
    +Bard Ability Power"""

                elif skill[0] == '8':
                    act_skill = 'fte'
                    vis_skill = 'FATE'
                    message = """\
Increasing FATE will provide:
    +1 to a random attribute (won't choose DIFFICULTY or FATE)
    +1 to a second random attribute (won't choose DIFFICULTY or FATE)
    +Knowledge that your destiny is predetermined and nothing matters"""

                elif skill[0] == '9':
                    act_skill = "dif"
                    vis_skill = "DIFFICULTY"
                    message = """\
Increasing DIFFICULTY will provide:
    +0.5% Enemy Physical Attack (Applies to entire party)
    +0.5% Enemy Pierce Attack (Applies to entire party)
    +0.5% Enemy Magical Attack (Applies to entire party)
    +More challenging experience"""

                else:
                    continue

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
        fix_stats()

        m_w = {'fire': 'water',
               'water': 'electric',
               'electric': 'earth',
               'earth': 'wind',
               'wind': 'grass',
               'grass': 'ice',
               'ice': 'fire',
               'neutral': 'neutral',
               'light': 'dark',
               'dark': 'light'}[self.def_element]

        print(f"""-{self.name}'s Stats-
Level {self.lvl} {self.class_.title()}
Statuses: {', '.join([x.title() for x in self.status_ail])}
XP: {self.exp}/{self.req_xp} / GP: {main.party_info['gp']}

HP: {self.hp}/{self.max_hp} / MP: {self.mp}/{self.max_mp} / AP: {self.ap}/{self.max_ap}
Physical: {self.attk} Attack / {self.dfns} Defense
Magical: {self.m_attk} Attack / {self.m_dfns} Defense
Piercing: {self.p_attk} Attack / {self.p_dfns} Defense
Speed: {self.spd}
Evasion: {self.evad}
Elements: Attacks are {self.off_element.title()} / Defense is {self.def_element.title()} / \
Weak to {m_w.title()}

Intelligence: {self.attributes['int']} 
Wisdom: {self.attributes['wis']}
Strength: {self.attributes['str']}
Constitution: {self.attributes['con']}
Dexterity: {self.attributes['dex']}
Perception: {self.attributes['per']}
Charisma: {self.attributes['cha']}
Difficulty: {main.party_info['dif']}""")

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

            elif items.equipped[inv_name]['weapon'].type_ == 'instrument':
                random.choice(sounds.bard_sounds[items.equipped[inv_name]['weapon'].item_id]).play()
                print(f'{self.name} starts playing their {player_weapon.name} at the {self.target.name}...')

            else:
                sounds.aim_weapon.play()
                print(f'{self.name} aims carefully at the {self.target.name} using their {player_weapon.name}...')

            main.smart_sleep(0.75)

            if items.equipped[inv_name]['weapon'].type_ == 'melee':
                dam_dealt = deal_damage(self, self.target, "physical")

            elif items.equipped[inv_name]['weapon'].type_ == 'ranged':
                dam_dealt = deal_damage(self, self.target, "piercing")

            else:
                dam_dealt = deal_damage(self, self.target, "magical")

            # Check for attack accuracy.
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
            sounds.play_music(main.party_info['music'])

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
                        chosen = main.s_input('Input [#] (or type "back"): ').lower()
                        try:
                            self.c_ability = all_abilities[int(chosen) - 1]

                        except (IndexError, ValueError):
                            if chosen in ['e', 'x', 'exit', 'b', 'back']:
                                print('-'*save_load.divider_size)
                                print(battle_options.format(self.name))
                                do_loop = False
                                break

                            continue

                        # Abilities cost AP to cast, just like spells cost MP.
                        if self.ap < self.c_ability.ap_cost:
                            print('-' * save_load.divider_size)
                            print(f"{self.name} doesn't have enough AP to cast {self.c_ability.name}!")
                            main.s_input("\nPress enter/return ")
                            break

                        # Ascend is an ability that is more powerful the later in the battle you use it.
                        # To balance this it's only usable once per battle.
                        elif self.c_ability == abilities.ascend and self.ability_vars['ascend_used']:
                            print('-' * save_load.divider_size)
                            print("Ascend can only be used once per battle.")
                            main.s_input("\nPress enter/return ")
                            break

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
                                storm,
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

    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)
        self.status = ''  # The status effect that will be applied to the player if RNGsus wills it
        self.is_poisoned = False
        self.is_defending = False
        self.class_ = None

        self.gold = 0
        self.experience = 0
        self.items = []
        self.drop_list = []
        self.attk_msg = "attacks"
        self.ascii_art = ''

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

    def get_drops(self):
        if random.randint(0, 4) == 0:  # 20% chance
            self.items = [random.choice(self.drop_list).item_id]

    def monster_level(self):
        minlvl, maxlvl = tiles.find_cell_with_tile_id(main.party_info['current_tile'].tile_id).m_level
        self.lvl = random.randrange(minlvl, maxlvl)

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
            print(monster.ascii_art % f"The {self.name} is making a move!\n")

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
                                       storm,
                                       parsto,
                                       adorine
                                       ] if x.enabled and 'dead' not in x.status_ail])

        if self.ability_vars['taunted'][0] == battle.turn_counter:
            self.m_target = self.ability_vars['taunted'][1]

    def battle_turn(self):
        pass


# =========================== #
#       MAGIC MONSTERS        #
# =========================== #


class MagicMonster(Monster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.class_multiplier = {'hp': 1,      # HP
                                 'mp': 1.5,      # MP
                                 'attk': 0.5,    # Physical Attack
                                 'dfns': 0.65,    # Physical Defense
                                 'p_attk': 0.5,  # Pierce Attack
                                 'p_dfns': 0.65,  # Pierce Defense
                                 'm_attk': 1.5,  # Magical Attack
                                 'm_dfns': 1.5,  # Magical Defense
                                 'spd': 1,     # Speed
                                 'evad': 1}    # Evasion

        self.species_multiplier = {'hp': 1,      # HP
                                   'mp': 1,      # MP
                                   'attk': 1,    # Physical Attack
                                   'dfns': 1,    # Physical Defense
                                   'p_attk': 1,  # Pierce Attack
                                   'p_dfns': 1,  # Pierce Defense
                                   'm_attk': 1,  # Magical Attack
                                   'm_dfns': 1,  # Magical Defense
                                   'spd': 1,     # Speed
                                   'evad': 1}    # Evasion

    def battle_turn(self):
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

            # Magical Attack
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

    def apply_multipliers(self):
        self.hp *= (self.class_multiplier['hp']*self.species_multiplier['hp'])
        self.mp *= (self.class_multiplier['mp']*self.species_multiplier['mp'])
        self.attk *= (self.class_multiplier['attk']*self.species_multiplier['attk'])
        self.dfns *= (self.class_multiplier['dfns']*self.species_multiplier['dfns'])
        self.p_attk *= (self.class_multiplier['p_attk']*self.species_multiplier['p_attk'])
        self.p_dfns *= (self.class_multiplier['p_dfns']*self.species_multiplier['p_dfns'])
        self.m_attk *= (self.class_multiplier['m_attk']*self.species_multiplier['m_attk'])
        self.m_dfns *= (self.class_multiplier['m_dfns']*self.species_multiplier['m_dfns'])
        self.spd *= (self.class_multiplier['spd']*self.species_multiplier['spd'])
        self.evad *= (self.class_multiplier['evad']*self.species_multiplier['evad'])


class Oread(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Oread"
        self.off_element = "earth"
        self.def_element = "earth"
        self.attk_msg = "casts a basic earth spell on"
        self.drop_list = [items.fairy_dust, items.eye_balls]
        self.ascii_art = """
   O
/}-|-{\\
  / \\
        %s"""


class Willothewisp(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Will-o'-the-wisp"
        self.off_element = "fire"
        self.def_element = "fire"
        self.attk_msg = "casts a basic fire spell on"
        self.drop_list = [items.fairy_dust, items.burnt_ash]
        self.ascii_art = """
  )\^^/(
 / o  o \\
|        |
 \______/
        %s"""


class Naiad(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Naiad"
        self.off_element = "water"
        self.def_element = "water"
        self.attk_msg = "casts a basic water spell on"
        self.drop_list = [items.fairy_dust, items.water_vial]
        self.ascii_art = """
   O
/}-|-{\\
  / \\
        %s"""


class Necromancer(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Necromancer"
        self.off_element = "dark"
        self.def_element = "dark"
        self.attk_msg = "casts a basic dark spell on"
        self.drop_list = [items.ripped_cloth, items.demonic_essence]
        self.ascii_art = """
 _^_
  O
`-|-
 / \\
        %s"""


class CorruptThaumaturge(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Corrupt Thaumaturge"
        self.off_element = "ice"
        self.def_element = "ice"
        self.attk_msg = "casts a basic ice spell on"
        self.drop_list = [items.ripped_cloth, items.mysterious_runes]
        self.ascii_art = """
 _^_
  O
`-|-
 / \\
        %s"""


class Imp(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Imp"
        self.off_element = "fire"
        self.def_element = "neutral"
        self.attk_msg = "casts a basic fire spell on"
        self.drop_list = [items.wing_piece, items.fairy_dust]
        self.ascii_art = """
 'o'
 -|-
 / \\
        %s"""


class Spriggan(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Spriggan"
        self.off_element = "grass"
        self.def_element = "grass"
        self.attk_msg = "casts a basic grass spell on"
        self.drop_list = [items.living_bark, items.fairy_dust]
        self.ascii_art = """
 }o{
3-|-E
 / \\
        %s"""


class Alicorn(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Alicorn"
        self.off_element = "light"
        self.def_element = "light"
        self.attk_msg = "casts a basic light spell on"
        self.drop_list = [items.unicorn_horn, items.angelic_essence]
        self.ascii_art = """
         ,
  ~~\\ ">
 [===]'
/    |
        %s"""


class WindWraith(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Wind Wraith"
        self.off_element = "wind"
        self.def_element = "wind"
        self.attk_msg = "casts a basic wind spell on"
        self.drop_list = [items.ectoplasm, items.demonic_essence]
        self.ascii_art = """
 (O)
~/ \\~
 | |
  V
        %s"""


class LightningGhost(MagicMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Lightning Ghost"
        self.off_element = "electric"
        self.def_element = "electric"
        self.attk_msg = "casts a basic electric spell on"
        self.drop_list = [items.ectoplasm, items.demonic_essence]
        self.ascii_art = """
 (O)
~/ \\~
 | |
  V
        %s"""


# =========================== #
#       RANGED MONSTERS       #
# =========================== #

class RangedMonster(Monster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.class_multiplier = {'hp': 0.9,      # HP
                                 'mp': 1,      # MP
                                 'attk': 0.8,    # Physical Attack
                                 'dfns': 0.8,    # Physical Defense
                                 'p_attk': 1.5,  # Pierce Attack
                                 'p_dfns': 1.2,  # Pierce Defense
                                 'm_attk': 0.8,  # Magical Attack
                                 'm_dfns': 1,  # Magical Defense
                                 'spd': 1.5,     # Speed
                                 'evad': 1.5}    # Evasion

        self.species_multiplier = {'hp': 1,      # HP
                                   'mp': 1,      # MP
                                   'attk': 1,    # Physical Attack
                                   'dfns': 1,    # Physical Defense
                                   'p_attk': 1,  # Pierce Attack
                                   'p_dfns': 1,  # Pierce Defense
                                   'm_attk': 1,  # Magical Attack
                                   'm_dfns': 1,  # Magical Defense
                                   'spd': 1,     # Speed
                                   'evad': 1}    # Evasion

    def battle_turn(self):
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


    def apply_multipliers(self):
        self.hp *= (self.class_multiplier['hp']*self.species_multiplier['hp'])
        self.mp *= (self.class_multiplier['mp']*self.species_multiplier['mp'])
        self.attk *= (self.class_multiplier['attk']*self.species_multiplier['attk'])
        self.dfns *= (self.class_multiplier['dfns']*self.species_multiplier['dfns'])
        self.p_attk *= (self.class_multiplier['p_attk']*self.species_multiplier['p_attk'])
        self.p_dfns *= (self.class_multiplier['p_dfns']*self.species_multiplier['p_dfns'])
        self.m_attk *= (self.class_multiplier['m_attk']*self.species_multiplier['m_attk'])
        self.m_dfns *= (self.class_multiplier['m_dfns']*self.species_multiplier['m_dfns'])
        self.spd *= (self.class_multiplier['spd']*self.species_multiplier['spd'])
        self.evad *= (self.class_multiplier['evad']*self.species_multiplier['evad'])


class FireAnt(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Fire Ant"
        self.off_element = 'fire'
        self.def_element = 'fire'
        self.attk_msg = "spits a firey glob of acid at"
        self.drop_list = [items.antennae, items.burnt_ash]
        self.ascii_art = """
O0o"
'\''
        %s"""


class NagaBowwoman(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Naga Bow-woman"
        self.off_element = 'neutral'
        self.def_element = 'water'
        self.attk_msg = "fires a volley of arrows at"
        self.drop_list = [items.serpent_scale, items.serpent_tongue]
        self.ascii_art = """
       o  \\
      -|--|
\\   ___/ /
 \\_/
        %s"""


class IceSoldier(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Ice Soldier"
        self.off_element = 'ice'
        self.def_element = 'ice'
        self.attk_msg = 'fires a single hyper-cooled arrow at'
        self.drop_list = [items.chain_link, items.blood_vial]
        self.ascii_art = """
  O   \\
--|--*|
  |   /
 / \\
        %s"""


class FrostBat(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Frost Bat"
        self.off_element = 'ice'
        self.def_element = 'ice'
        self.attk_msg = 'spits a frozen glob of acid at'
        self.drop_list = [items.monster_fang, items.wing_piece]
        self.ascii_art = """
/}-''-{\\
  ^  ^
        %s"""


class SparkBat(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Spark Bat"
        self.off_element = 'electric'
        self.def_element = 'electric'
        self.attk_msg = 'spits an electrified glob of acid at'
        self.drop_list = [items.monster_fang, items.wing_piece]
        self.ascii_art = """
/}-''-{\\
  ^  ^
        %s"""


class SkeletonBoneslinger(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Skeleton Boneslinger"
        self.off_element = 'dark'
        self.def_element = 'dark'
        self.attk_msg = 'grabs a nearby bone and slings it at'
        self.drop_list = [items.bone_bag, items.demonic_essence]
        self.ascii_art = """
   O    v
--{|}--*|
   |    ^
  / \\
        %s"""


class UndeadCrossbowman(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Undead Crossbowman"
        self.off_element = 'dark'
        self.def_element = 'dark'
        self.attk_msg = 'fires a bone-tipped crossbow bolt at'
        self.drop_list = [items.chain_link, items.bone_bag]
        self.ascii_art = """
  O  __
--|--*|>
  |  
 / \\
        %s"""


class RockGiant(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Rock Giant"
        self.off_element = "earth"
        self.def_element = "earth"
        self.attk_msg = "hurls a giant boulder at"
        self.drop_list = [items.golem_rock, items.broken_crystal]
        self.ascii_art = """
    O
*--|-|--*
   |_|
  _/ \\_
        %s"""


class GoblinArcher(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Goblin Archer"
        self.off_element = 'neutral'
        self.def_element = 'neutral'
        self.attk_msg = "fires an arrow at"
        self.drop_list = [items.ripped_cloth, items.eye_balls]
        self.ascii_art = """
  o  \\
--|--|
 / \\ /
        %s"""


class GiantLandSquid(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Giant Land-Squid"
        self.off_element = "water"
        self.def_element = "water"
        self.attk_msg = "shoots a black, inky substance at"
        self.drop_list = [items.ink_sack, items.slime_vial]
        self.ascii_art = """
 \\[**]/
  |()|
 / || \\
/  ||  \\
        %s"""


class VineLizard(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Vine Lizard"
        self.off_element = "grass"
        self.def_element = "grass"
        self.attk_msg = "spits an acidic string of vines at"
        self.drop_list = [items.serpent_scale, items.living_bark]
        self.ascii_art = """
~-:=:>
        %s"""


class TenguRanger(RangedMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Tengu Ranger"
        self.off_element = "earth"
        self.def_element = "earth"
        self.attk_msg = "catapults a stone javelin towards"
        self.drop_list = [items.wing_piece, items.feathers]
        self.ascii_art = """
  'O>    ,
/}-|-{\\./
  / \\  /
        %s"""


# =========================== #
#       MELEE MONSTERS        #
# =========================== #


class MeleeMonster(Monster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.class_multiplier = {'hp': 1.2,      # HP
                                 'mp': 1,      # MP
                                 'attk': 1.5,    # Physical Attack
                                 'dfns': 1.5,    # Physical Defense
                                 'p_attk': 0.5,  # Pierce Attack
                                 'p_dfns': 1.5,  # Pierce Defense
                                 'm_attk': 0.5,  # Magical Attack
                                 'm_dfns': 0.5,  # Magical Defense
                                 'spd': 0.65,     # Speed
                                 'evad': 1}    # Evasion

        self.species_multiplier = {'hp': 1,      # HP
                                   'mp': 1,      # MP
                                   'attk': 1,    # Physical Attack
                                   'dfns': 1,    # Physical Defense
                                   'p_attk': 1,  # Pierce Attack
                                   'p_dfns': 1,  # Pierce Defense
                                   'm_attk': 1,  # Magical Attack
                                   'm_dfns': 1,  # Magical Defense
                                   'spd': 1,     # Speed
                                   'evad': 1}    # Evasion

    def battle_turn(self):
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

    def apply_multipliers(self):
        self.hp *= (self.class_multiplier['hp']*self.species_multiplier['hp'])
        self.mp *= (self.class_multiplier['mp']*self.species_multiplier['mp'])
        self.attk *= (self.class_multiplier['attk']*self.species_multiplier['attk'])
        self.dfns *= (self.class_multiplier['dfns']*self.species_multiplier['dfns'])
        self.p_attk *= (self.class_multiplier['p_attk']*self.species_multiplier['p_attk'])
        self.p_dfns *= (self.class_multiplier['p_dfns']*self.species_multiplier['p_dfns'])
        self.m_attk *= (self.class_multiplier['m_attk']*self.species_multiplier['m_attk'])
        self.m_dfns *= (self.class_multiplier['m_dfns']*self.species_multiplier['m_dfns'])
        self.spd *= (self.class_multiplier['spd']*self.species_multiplier['spd'])
        self.evad *= (self.class_multiplier['evad']*self.species_multiplier['evad'])


class GiantCrab(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Giant Crab"
        self.off_element = "water"
        self.def_element = "water"
        self.attk_msg = "snaps its massive claws at"
        self.drop_list = [items.crab_claw, items.shell_fragment]
        self.ascii_art = """
{}     {}
 \\_o-o_/
   \\ /
   ^ ^
        %s"""


class BogSlime(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Bog Slime"
        self.off_element = "grass"
        self.def_element = "grass"
        self.attk_msg = "jiggles menacingly at"
        self.drop_list = [items.slime_vial, items.water_vial]
        self.ascii_art = """
 /----\\
/______\\
        %s"""


class Mummy(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Mummy"
        self.off_element = "fire"
        self.def_element = "dark"
        self.attk_msg = "meanders over and grabs"
        self.drop_list = [items.burnt_ash, items.ripped_cloth]
        self.ascii_art = """
~o
 |==
 |
 |\\
        %s"""


class SandGolem(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Sand Golem"
        self.off_element = "rock"
        self.def_element = "rock"
        self.attk_msg = "begins to pile sand on"
        self.drop_list = [items.golem_rock, items.broken_crystal]
        self.ascii_art = """
    O
*--|-|--*
   |_|
  _/ \\_
        %s"""


class MossOgre(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Moss Ogre"
        self.off_element = "grass"
        self.def_element = "grass"
        self.attk_msg = "swings a tree trunk like a club at"
        self.drop_list = [items.bone_bag, items.monster_skull]
        self.ascii_art = """
    O
*--|-|--*
   |_|
  _/ \\_
        %s"""


class Troll(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Troll"
        self.off_element = "neutral"
        self.def_element = "neutral"
        self.attk_msg = "swings its mighty battleaxe at"
        self.drop_list = [items.monster_skull, items.eye_balls]
        self.ascii_art = """
 O
-|-!
/ \\
        %s"""


class Griffin(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Griffin"
        self.off_element = "wind"
        self.def_element = "wind"
        self.attk_msg = "swipes with its ferocious claws at"
        self.drop_list = [items.animal_fur, items.wing_piece]
        self.ascii_art = """
  ~~\\ ">
 [===]'
/    |
        %s"""


class GiantWorm(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Giant Worm"
        self.off_element = "earth"
        self.def_element = "earth"
        self.attk_msg = "burrows into the ground and starts charging towards"
        self.drop_list = [items.monster_fang, items.slime_vial]
        self.ascii_art = """
\\   ___/
 \\_/
        %s"""


class Zombie(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Zombie"
        self.off_element = "dark"
        self.def_element = "dark"
        self.attk_msg = "charges and tries to bite"
        self.drop_list = [items.monster_skull, items.blood_vial]
        self.ascii_art = """
 o
 |==
 |
 |\\
        %s"""


class SnowWolf(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Snow Wolf"
        self.off_element = "ice"
        self.def_element = "ice"
        self.attk_msg = "claws and bites at"
        self.drop_list = [items.animal_fur, items.monster_fang]
        self.ascii_art = """
    ^-,
~/--/
 `  `
        %s"""


class LesserYeti(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Lesser Yeti"
        self.off_element = "ice"
        self.def_element = "ice"
        self.attk_msg = "begins to maul"
        self.drop_list = [items.animal_fur, items.monster_fang]
        self.ascii_art = """
    O
*--|-|--*
   |_|
  _/ \\_
        %s"""


class SludgeRat(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Sludge Rat"
        self.off_element = "neutral"
        self.def_element = "neutral"
        self.attk_msg = "ferociously chomps at"
        self.drop_list = [items.monster_skull, items.rodent_tail]
        self.ascii_art = """
~-[--]>
  *  *
        %s"""


class SeaSerpent(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Sea Serpent"
        self.off_element = "water"
        self.def_element = "water"
        self.attk_msg = "charges head-first into"
        self.drop_list = [items.serpent_scale, items.serpent_tongue]
        self.ascii_art = """
\\   ___/^*
 \\_/
        %s"""


class Beetle(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Beetle"
        self.off_element = "earth"
        self.def_element = "grass"
        self.attk_msg = "charges horn-first into"
        self.drop_list = [items.beetle_shell, items.antennae]
        self.ascii_art = """
 ______
/______\C
 ''''''
        %s"""


class Harpy(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Harpy"
        self.off_element = "wind"
        self.def_element = "wind"
        self.attk_msg = "dives claws-first towards"
        self.drop_list = [items.wing_piece, items.feathers]
        self.ascii_art = """
   O
/}-|-{\\
  / \\
        %s"""


class FallenKnight(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Fallen Knight"
        self.off_element = "light"
        self.def_element = "dark"
        self.attk_msg = "thrusts its heavenly spear towards"
        self.drop_list = [items.chain_link, items.blood_vial]
        self.ascii_art = """
, (v)
|--|-
| / \\
        %s"""


class DevoutProtector(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Devout Protector"
        self.off_element = "light"
        self.def_element = "light"
        self.attk_msg = "swings its holy hammer towards"
        self.drop_list = [items.angelic_essence, items.mysterious_runes]
        self.ascii_art = """

 O [=]
-|--|
/ \\
        %s"""


class Calculator(MeleeMonster):
    def __init__(self, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        super().__init__(hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad)

        self.name = "Calculator"
        self.off_element = "neutral"
        self.def_element = "neutral"
        self.attk_msg = "casts its mathemagical spell on"
        self.drop_list = [items.calculus_homework, items.graph_paper, items.protractor, items.ruler, items.textbook]
        self.ascii_art = """
 ..
[==]
[==]
        %s"""


animal_group = [FireAnt, FrostBat, SparkBat, SludgeRat, GiantLandSquid, GiantCrab, SnowWolf, Beetle, VineLizard,
                GiantWorm]

monster_group = [Willothewisp, Alicorn, WindWraith, BogSlime, SandGolem, Griffin, Harpy, SeaSerpent, NagaBowwoman]

humanoid_group = [Troll, MossOgre, LesserYeti, RockGiant, GoblinArcher, Oread, TenguRanger, Naiad, Imp, Spriggan]

undead_group = [Zombie, UndeadCrossbowman, LightningGhost, Mummy, SkeletonBoneslinger]

dungeon_group = [Calculator, Necromancer, CorruptThaumaturge, IceSoldier, FallenKnight, DevoutProtector]


class Boss(Monster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                 lvl, b_items, gold, experience, attk_msg, boss_id):
        super().__init__(hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)

        self.name = name
        self.items = b_items
        self.lvl = lvl
        self.experience = experience
        self.gold = gold
        self.attk_msg = attk_msg
        self.boss_id = boss_id

        self.lackies = None
        self.active = False

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


# =========================== #
#           BOSSES            #
# =========================== #

# == MASTER SLIME == #
class MasterSlimeBoss(Boss, MeleeMonster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                 lvl, b_items, gold, experience, attk_msg, boss_id):

        super().__init__(name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                         lvl, b_items, gold, experience, attk_msg, boss_id)

        self.active = False
        self.off_element = 'neutral'
        self.def_element = 'neutral'
        self.lackies = None
        self.ascii_art = """
   M
 /---\\
/_____\\
        %s"""

    def upon_defeating(self):
        dialogue.alfred_quest_a.finished = True
        dialogue.alfred_convo_b.active = False
        dialogue.alfred_convo_c.active = True

    def battle_turn(self):
        MeleeMonster.battle_turn(self)


master_slime = MasterSlimeBoss('Master Slime',
                               35, 5,   # 35 HP and 5 MP
                               15, 10,  # 12 Attack, 5 Defense
                               6, 10,   # 6 Pierce Attack, 5 Pierce Defense
                               8, 0,    # 8 Magical Attack, 0 Magical Defense
                               6, 6,    # 6 Speed, 6 Evasion
                               3,       # Level 3
                               ["s_vial", "s_vial", "s_vial"],  # Drops 3 slime vials
                               25, 25,  # Gives 25 XP and 25 GP
                               "jiggles ferociously and begins to attack", "master_slime")


# == GOBLIN CHIEFTAIN == #
class GoblinChieftainBoss(Boss, MeleeMonster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                 lvl, b_items, gold, experience, attk_msg, boss_id):
        super().__init__(name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                         lvl, b_items, gold, experience, attk_msg, boss_id)

        self.active = True
        self.off_element = 'neutral'
        self.def_element = 'neutral'
        self.lackies = None
        self.ascii_art = """
 , `o`
 |--|-
 | / \\
        %s"""

    def battle_turn(self):
        MeleeMonster.battle_turn(self)


goblin_chieftain = GoblinChieftainBoss('Goblin Chieftain',
                                       50, 10,  # 50 HP and 10 MP
                                       20, 20,  # 20 Attack, 20 Defense
                                       12, 15,  # 12 Pierce Attack, 15 Pierce Defense
                                       8, 12,   # 8 Magical Attack, 12 Magical Defense
                                       15, 7,   # 15 Speed, 7 Evasion
                                       5,       # Level 5
                                       [],      # Drops no items
                                       45, 45,  # Gives 45 XP and 45 GP
                                       "readies his great spear and begins to stab", "goblin_cheiftain")


# == MENACING PHANTOM == #
class MenacingPhantomBoss(Boss, MagicMonster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                 lvl, b_items, gold, experience, attk_msg, boss_id):
        super().__init__(name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                         lvl, b_items, gold, experience, attk_msg, boss_id)

        self.lackies = None
        self.off_element = 'dark'
        self.def_element = 'dark'
        self.active = False
        self.ascii_art = """
 (O)
~/ \\~
 | |
  V
        %s"""

    def upon_defeating(self):
        # Stands for "Menacing Phantom -- Upon Defeating"
        dialogue.stewson_quest_a.finished = True
        dialogue.stewson_convo_b.active = False

    def battle_turn(self):
        MagicMonster.battle_turn(self)


menacing_phantom = MenacingPhantomBoss('Menacing Phantom',
                                       75, 50,  # 75 HP and 50 MP
                                       10, 20,  # 10 Attack, 20 Defense
                                       5, 20,   # 5 Pierce Attack, 20 Pierce Defense
                                       35, 25,  # 35 Magical Attack, 25 Magical Defense
                                       20, 15,  # 20 Speed, 15 Evasion
                                       8,       # Level 8
                                       [],      # Drops no items
                                       75, 75,  # Gives 75 XP and 75 GP
                                       "calls upon its ethereal power and casts a hex on", "menacing_phantom")


# == TERRIBLE TARANTULOID == #  (Adventure in Pixels)
class TerribleTarantuloidBoss(Boss, MeleeMonster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                 lvl, b_items, gold, experience, attk_msg, boss_id):
        super().__init__(name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                         lvl, b_items, gold, experience, attk_msg, boss_id)

        self.active = False
        self.off_element = 'neutral'
        self.def_element = 'neutral'
        self.lackies = None
        self.ascii_art = """
|   |
 \\o/
--0--
--0--
 / \\
        %s"""

    def upon_defeating(self):
        dialogue.krystin_convo_b.active = False
        dialogue.krystin_convo_c.active = True
        dialogue.kyle_convo_b.active = False
        dialogue.kyle_convo_c.active = True
        dialogue.alden_convo_a.active = False
        dialogue.alden_convo_b.active = True

    def battle_turn(self):
        MeleeMonster.battle_turn(self)


terr_tarant = TerribleTarantuloidBoss('Terrible Tarantuloid',
                                      100, 25,   # 100 Health, 25 Mana
                                      45, 30,    # 45 Attack, 30 Defense
                                      25, 15,    # 25 Pierce Attack, 15 Pierce Defense
                                      15, 25,    # 15 Magical Attack, 25 Magical Defense
                                      35, 25,    # 35 Speed, 25 Evasion
                                      12,        # Level 12
                                      [],        # Drops no items
                                      150, 150,  # Gives 150 XP and 150 GP
                                      "readies its venomous fangs and bites", "terrible_tarantuloid")


# == CURSED SPECTRE == #
class CursedSpectreBoss(Boss, MagicMonster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                 lvl, b_items, gold, experience, attk_msg, boss_id):
        super().__init__(name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                         lvl, b_items, gold, experience, attk_msg, boss_id)

        self.lackies = None
        self.off_element = 'dark'
        self.def_element = 'dark'
        self.active = False
        self.ascii_art = """
 (O)
~/ \\~
 | |
  V
        %s"""

    def upon_defeating(self):
        dialogue.rivesh_convo_c.active = False
        dialogue.rivesh_quest_a.finished = True

    def battle_turn(self):
        MagicMonster.battle_turn(self)


cursed_spectre = CursedSpectreBoss('Cursed Spectre',
                                   125, 75,             # 125 Health, 75 Mana
                                   15, 30,              # 15 Attack, 30 Defense
                                   20, 25,              # 20 Pierce Attack, 25 Pierce Defense
                                   50, 35,              # 50 Magical Attack, 35 Magical Defense
                                   25, 20,              # 25 Speed, 20 Evasion
                                   15,                  # Level 15
                                   [],                  # Drops no items
                                   250, 250,            # Gives 250 XP and 250 GP
                                   "calls upon its ethereal power and casts a hex on", "cursed_spectre")


# == GIANT ENT == #
class GiantEntBoss(Boss, MeleeMonster):
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                 lvl, b_items, gold, experience, attk_msg, boss_id):
        super().__init__(name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad,
                         lvl, b_items, gold, experience, attk_msg, boss_id)

        self.active = False
        self.off_element = 'grass'
        self.def_element = 'grass'
        self.lackies = None
        self.ascii_art = """
\\\\\\''///
  |oo|
  |~~|
  /vv\\
"""

    def battle_turn(self):
        MeleeMonster.battle_turn(self)


giant_ent = GiantEntBoss('Giant Ent',
                         125, 35,         # 125 Health, 75 Mana
                         35, 50,          # 35 Attack, 50 Defense
                         15, 50,          # 15 Pierce Attack, 50 Pierce Defense
                         20, 15,          # 20 Magical Attack, 15 Magical Defense
                         15, 5,           # 15 Speed, 5 Evasion
                         15,              # Level 15
                         [],              # Drops no items
                         250, 250,        # Gives 250 XP and 250 GP
                         "slowly lumbers over and whacks", "giant_ent")

boss_list = [goblin_chieftain, master_slime, menacing_phantom, terr_tarant, cursed_spectre, giant_ent]
defeated_bosses = []  # Make sure you can only defeat the boss one time


def check_bosses():
    global monster

    for boss in main.party_info['current_tile'].boss_list:
        if boss.boss_id not in defeated_bosses and boss.active:
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
    # "Neutral" element is neutral to all elements
    # All other interactions are neutral

    a_elem = attacker.off_element
    t_elem = target.def_element

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
    if (a_elem == 'neutral' or t_elem == 'neutral') or (a_elem == t_elem):
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
    global storm
    global parsto
    global chyme

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)

    # Pronounced "So-low"
    solou = PlayableCharacter('Solou', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='mage', enabled=False)
    # Pronounced... Chili
    chili = PlayableCharacter('Chili', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='monk', enabled=False)
    # Pronounced "Adore-een"
    adorine = PlayableCharacter('Adorine', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='warrior', enabled=False)
    # Pronounced "Parse-toe"
    parsto = PlayableCharacter("Parsto", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='ranger', enabled=False)
    # Rhymes with "Chime"
    chyme = PlayableCharacter("Chyme", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='paladin', enabled=False)
    # Pronounced... Storm
    storm = PlayableCharacter("Storm", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, class_='assassin', enabled=False)

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
        items.equipped['player']['weapon'] = copy.copy(items.iron_hoe)

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
        items.equipped['player']['weapon'] = copy.copy(items.garden_gloves)

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

    elif player.class_ == "bard":
        player.max_mp += 3
        player.m_dfns += 1
        player.m_attk += 3
        player.hp -= 1
        player.dfns -= 1
        player.p_dfns -= 1
        items.equipped['player']['weapon'] = copy.copy(items.kazoo)
        items.add_item("musicbox")

    player.hp = copy.copy(player.max_hp)
    player.mp = copy.copy(player.max_mp)

    save_load.save_game(verbose=False)


def spawn_monster():
    monster_groups = tiles.find_cell_with_tile_id(main.party_info['current_tile'].tile_id).enemy_groups
    monster_groups = list(itertools.chain.from_iterable(monster_groups))

    for unit_object in ['monster', 'monster_2', 'monster_3']:
        globals()[unit_object] = random.choice(monster_groups)(10, 5, 3, 2, 3, 2, 3, 2, 3, 2)
        globals()[unit_object].monster_level()
        globals()[unit_object].apply_multipliers()
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
    global storm
    global adorine
    global monster

    # Make an abbreviation for battle.temp_stats so a later part doesn't have to be multi-line
    bts = battle.temp_stats

    for x in [player, solou, chili, chyme, parsto, storm, adorine]:
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
                storm,
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
    storm.target = ''
    chili.target = ''
    solou.target = ''
    chyme.target = ''

    player.c_spell = ''
    parsto.c_spell = ''
    adorine.c_spell = ''
    storm.c_spell = ''
    chili.c_spell = ''
    solou.c_spell = ''
    chyme.c_spell = ''

    player.c_ability = ''
    parsto.c_ability = ''
    adorine.c_ability = ''
    storm.c_ability = ''
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
        json.dump(storm.__dict__, f, indent=4, separators=(', ', ': '))
    with open(p_path, mode='w', encoding='utf-8') as f:
        json.dump(parsto.__dict__, f, indent=4, separators=(', ', ': '))


def deserialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Load the JSON files and translate them into "PlayableCharacter" objects
    global player
    global solou
    global chili
    global adorine
    global chyme
    global storm
    global parsto

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    solou = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    chili = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    adorine = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    chyme = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
    storm = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3, enabled=False)
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
        storm.__dict__ = json.load(f)
    with open(p_path, encoding='utf-8') as f:
        parsto.__dict__ = json.load(f)

    for x in [player, solou, chili, adorine, chyme, storm, parsto]:
        x.reset_ability_vars()


def serialize_bosses(path):
    json_bosslist = {}

    for boss in boss_list:
        json_bosslist[boss.boss_id] = boss.active

    with open(path, encoding='utf-8', mode='w') as i:
        json.dump(json_bosslist, i)


def deserialize_bosses(path):
    global boss_list

    with open(path, encoding='utf-8') as i:
        json_bosslist = json.load(i)

    for key in json_bosslist:
        for boss in boss_list:
            if key == boss.boss_id:
                boss.active = json_bosslist[key]


player = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
solou = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
chili = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
adorine = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
storm = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
parsto = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
chyme = PlayableCharacter('', '', '', '', '', '', '', '', '', '', '')
monster = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
monster_2 = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
monster_3 = Monster(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)



