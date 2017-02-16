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

import random
import json
import copy
import sys
import pygame
import math
import re

import inv_system
import items
import battle
import sounds
import magic
import ascii_art
import bosses
import units
import MagicClass

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()


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
    # A class for characters whose input can be directly controlled by the player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad, class_='', enabled=True):
        Unit.__init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)

        self.class_ = class_      # Player Class
        self.element = 'none'     # Player's Element
        self.status_ail = 'none'  # Current Status Ailment
        self.enabled = enabled    # Whether the party member has been recruited or not
        self.exp = 0              # Experience
        self.extra_sp = 0         # Extra Skill Points
        self.ext_gol = 0          # Extra Gold Pieces
        self.ext_exp = 0          # Extra Experience
        self.req_xp = 3           # Required XP to level up
        self.move = ''            # What move the character chose during battle

        self.attributes = {'int': 1,  # Intelligence, for Mages
                           'wis': 1,  # Wisdom, for Paladins
                           'str': 1,  # Strength, for Warriors
                           'con': 1,  # Constitution, for Monks
                           'dex': 1,  # Dexterity, for Assassins
                           'per': 1,  # Perception, for Rangers
                           'for': 1}  # Fortune

        self.battle_options = """Pick {0}'s Move:
      [1]: Standard Attack
      [2]: Use Magic
      [3]: Use Items
      [4]: Use Ultimate
      [5]: Run"""

    def choose_name(self):
        while True:
            # Ask the player for their name, and remove any pipe characters from it
            choice = input('What is your name, young adventurer? | Input Name: ')

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

            # Flygon Jones, Cynder887, and Apollo Kalar are all pseudonyms for my real-life
            # best friend. He also happens to be one of the primary bug-testers for the game!
            if self.name.lower() in ["flygon jones", "apollo kalar", "cynder887"]:
                print(''.join(['Ah, ', self.name, '! My dear friend, it is great to see you again!']))
                input('Press enter/return ')

                return self.name

            while True:
                y_n = input('So, your name is {0}? | Yes or No: '.format(self.name))
                y_n = y_n.lower()

                if y_n.startswith('y'):
                    print('-'*25)
                    return self.name

                elif y_n.startswith('n'):
                    self.name = ''
                    print()
                    break

    def choose_class(self):
        while True:
            class_ = input("""{0}, which class would you like to train as?\n\
          [1] Mage: Master of the arcane arts capable of using all spells, but has low defense
          [2] Assassin: Deals damage quickly and has high speed and evasion. Can poison foes
          [3] Ranger: An evasive long-distance fighter who uses bows and deals pierce damage
          [4] Paladin: Heavy-armor user who excel at holy and healing magic and uses hammers
          [5] Monk: A master of unarmed combat. High evasion and capable of using buff spells
          [6] Warrior: High defense stats and attack. Can tank lots of hits with its high HP
    Input [#]: """.format(self.name))
            print()
            try:
                class_ = {'1': "mage",
                          '2': "assassin",
                          '3': "ranger",
                          '4': "paladin",
                          '5': "monk",
                          '6': "warrior"}[class_]

            except KeyError:
                continue

            while True:
                y_n = input('You wish to be of the {0} class? | Yes or No: '.format(class_.title())).lower()

                if y_n.startswith('y'):
                    print('-'*25)
                    return class_

                elif y_n.startswith('n'):
                    print()
                    break

    def level_up(self):
        if self.exp >= self.req_xp:
            print()

            pygame.mixer.music.load('Content/Music/Adventures in Pixels.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            # The player restores all their health and mana when they level up
            self.hp = copy.copy(self.max_hp)
            self.mp = copy.copy(self.max_mp)
            self.status_ail = 'none'

            rem_points = 0  # Remaining Skill Points
            extra_points = 0  # The number of extra skill points the player will receive

            while self.exp >= self.req_xp:
                sounds.item_pickup.play()
                self.lvl += 1
                print("{0} has advanced to level {1}!".format(self.name, self.lvl))

                if self.lvl == 5:
                    print('\n{0} now understands the true potential of their class!'.format(self.name))
                    print('{0} can activate this potential in the form of a "class ability"'.format(self.name))
                    print('once per battle. Use it wisely!\n')
                    input('Press enter/return ')

                rem_points += 5
                extra_points += self.extra_sp
                magic.new_spells(self)

                if self.class_ == 'warrior':
                    # Total gain: 21 pts.
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
                    # Total gain: 21 pts.
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
                    # Total gain: 21 pts.
                    self.p_dfns += 2
                    self.attk += 4
                    self.dfns += 2
                    self.m_attk += 2
                    self.m_dfns += 1
                    self.spd += 5
                    self.evad += 2
                    self.hp += 2
                    self.mp += 1

                elif self.class_ == 'ranger':
                    # Total gain: 21 pts.
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
                    # Total gain: 21 pts.
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
                    # Total gain: 21 pts.
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

                units.fix_stats()

            print('-'*25)
            self.skill_points(rem_points, extra_points)

            self.max_hp = copy.copy(self.hp)
            self.max_mp = copy.copy(self.mp)

            print('-'*25)
            main.save_game()

            return

    def skill_points(self, rem_points, extra_points):
        if extra_points:
            print("{0}'s great fortune has granted them {1} additional skill points!".format(self.name, extra_points))
            rem_points += extra_points

        while rem_points > 0:
            print('{0} has {1} skill point{2} left to spend.'.format(
                self.name, rem_points, 's' if rem_points > 1 else ''
            ))

            skill = input("""Choose a skill to advance:
    [I]ntelligence - Use powerful magic with higher magic stats and MP!
    [W]isdom - Cast powerful healing magics with higher proficiency and MP!
    [S]trength -  Smash through enemies with higher attack and defense!
    [C]onstitution - Become a tank with higher defense stats and HP!
    [D]exterity - Improve your aerobic ability with higher evade/speed stats!
    [P]erception - Eliminate your enemies with ease using higher pierce and evasion!
    [F]ortune - Increase your luck in hopes of getting more GP, XP, and skill points!
Input letter: """)

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

                print('-'*25)
                print('Current {0}: {1}'.format(vis_skill, self.attributes[act_skill]))

                if self.extra_sp == 10 and act_skill == 'for':
                    print("{0}'s additional skill points from Fortune has already reached the maximum of 10.")
                    print("Instead, upgrading Fortune will provide 2x the extra experience and gold from enemies.")

                while True:
                    y_n = input("Increase {0}'s {1}? | Yes or No: ".format(self.name, vis_skill))
                    y_n = y_n.lower()

                    if not (y_n.startswith('y') or y_n.startswith('n')):
                        continue

                    if y_n.startswith('n'):
                        print('-'*25)
                        break

                    if skill.startswith('i'):
                        self.m_dfns += 1
                        self.m_attk += 1
                        self.mp += 2
                        self.attributes['int'] += 1

                    elif skill.startswith('w'):
                        self.mp += 2
                        self.attributes['wis'] += 1

                    elif skill.startswith('s'):
                        self.attk += 1
                        self.p_dfns += 1
                        self.dfns += 1
                        self.attributes['str'] += 1

                    elif skill.startswith('c'):
                        self.max_hp += 1
                        self.dfns += 1
                        self.p_dfns += 1
                        self.m_dfns += 1
                        self.attributes['con'] += 1

                    elif skill.startswith('d'):
                        self.spd += 1
                        self.p_attk += 1
                        self.evad += 1
                        self.attributes['dex'] += 1

                    elif skill.startswith('p'):
                        self.p_attk += 1
                        self.p_dfns += 1
                        self.evad += 1
                        self.attributes['per'] += 1

                    elif skill.startswith('f'):
                        if self.extra_sp == 10:
                            self.ext_gol += 2
                            self.ext_exp += 2

                        else:
                            self.extra_sp += 1
                            self.ext_gol += 1
                            self.ext_exp += 1

                        self.attributes['for'] += 1

                    else:
                        continue

                    print('-'*25)
                    print("{0}'s {1} has increased!".format(self.name, vis_skill))

                    # Decrement remaining points
                    rem_points -= 1

                    print('-'*25) if rem_points else ''

                    break

        print('\n{0} is out of skill points.'.format(self.name))

    def player_info(self):
        inv_name = self.name if self != units.player else 'player'
        units.fix_stats()

        print(f"""-{self.name}'s Stats-
Level: {self.lvl} | Class: {self.class_.title()} | Element: {self.element.title()}
HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp} | Status Ailment: {self.status_ail.title()}
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

        input('\nPress enter/return ')

    def player_damage(self):
        # The formula for PCUs dealing damage

        # Base damage is equal to the PCU's attack stat minus half the target's defense
        # For example, if the PCU's attack stat is 20, and the target has 10 defense, the
        # attack will deal 20 - (10/2) = 15 damage. This number is then further modified
        # based on the PCU/target's elements, status ailments, weapons, armor, and critical hits.

        inv_name = self.name if self != units.player else 'player'

        if inv_system.equipped[inv_name]['weapon'].type_ != 'ranged':
            dam_dealt = battle.temp_stats[self.name]['attk'] - (units.monster.dfns/2)
            dam_dealt *= (inv_system.equipped[inv_name]['weapon'].power + 1)

            # PCUs deal 1/2 damage with melee attacks when given the weakened status ailment
            if self.status_ail == 'weakened':
                dam_dealt /= 2
                print(f"{self.name}'s weakened state reduces their attack damage by half!")

                sounds.debuff.play()
                main.smart_sleep(0.5)

            # Mages deal 1/2 damage with melee attacks
            if self.class_ == 'mage':
                dam_dealt /= 2

        else:
            dam_dealt = battle.temp_stats[self.name]['p_attk'] - (units.monster.p_dfns/2)
            dam_dealt *= (inv_system.equipped[inv_name]['weapon'].power + 1)

            # PCUs deal 1/2 damage with ranged attacks when given the blinded status ailment
            if self.status_ail == 'blinded':
                dam_dealt /= 2
                print(f"{self.name}'s poor vision reduces their attack damage by half!")

        # Increase or decrease the damage depending on the PCU/monster's elements
        dam_dealt = eval_element(self, units.monster, dam_dealt)

        # All attacks deal a minimum of one damage
        if dam_dealt < 1:
            dam_dealt = 1

        # There is a 15% chance to inflict 1.5x damage
        if random.randint(1, 100) <= 15:
            dam_dealt *= 1.5
            print("It's a critical hit! 1.5x damage!")

            sounds.critical_hit.play()
            main.smart_sleep(0.5)

        # Limit the amount of damage to 999 (as if that matters)
        if dam_dealt > 999:
            dam_dealt = 999

        return math.ceil(dam_dealt)

    def battle_turn(self):
        inv_name = self.name if self != units.player else 'player'
        player_weapon = inv_system.equipped[inv_name]['weapon']

        print(f"-{self.name}'s Turn-")

        # Check to see if the PCU is poisoned
        if self.status_ail == 'poisoned' and units.monster.hp > 0:
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

            if inv_system.equipped[inv_name]['weapon'].type_ in ['melee', 'magic']:
                sounds.sword_slash.play()
                print(f'{self.name} begins to fiercely attack the {units.monster.name} using their {player_weapon}...')

            # Ranged weapons aren't swung, so play a different sound effect
            else:
                sounds.aim_weapon.play()
                print(f'{self.name} aims carefully at the {units.monster.name} using their {player_weapon}...')

            main.smart_sleep(0.75)

            # Check for attack accuracy
            if random.randint(1, 512) in range(units.monster.evad, 512):
                dam_dealt = self.player_damage()

                print(f"{self.name}'s attack connects with the {units.monster.name}, dealing {dam_dealt} damage!")

                sounds.enemy_hit.play()
                units.monster.hp -= dam_dealt

            else:
                print(f"The {units.monster.name} narrowly avoids {self.name}'s attack!")
                sounds.attack_miss.play()

        # Class Ability
        elif self.move == '4' and not self.class_ability():
            return False

        # Run away!
        elif self.move == '5' and battle.run_away(self):
            pygame.mixer.music.load(main.party_info['reg_music'])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            return 'Ran'

        else:
            return False

        return True

    def player_choice(self):
        # Creates a lambda function that strips all non-numeric characters
        # This fixes some (possible) problems later on
        print(self.battle_options.format(self.name))

        while True:
            self.move = input("Input [#]: ")

            try:
                self.move = re.sub("[^0-9][^QWEDR]", '', self.move)[0].lower()

            except IndexError:
                continue

            if self.move in ['1', 'q']:
                self.move = '1'

            # Use Magic
            elif self.move in ['2', 'w']:
                self.move = '2'
                print('-'*25)

                if self.status_ail == 'silenced':
                    sounds.debuff.play()
                    print(f"{self.name} is silenced and cannot use spells!")
                    input("\nPress enter/return ")

                    continue

                if not magic.pick_cat(self):
                    print(self.battle_options.format(self.name))

                    continue

                input('\nPress enter/return ')

            elif self.move in ['3', 'e']:
                self.move = '3'
                print('-'*25)

                if not inv_system.inventory['consum']:
                    print('Your party has no battle-allowed items - the consumable category is empty!')
                    print("\nPress enter/return ")
                    print(self.battle_options.format(self.name))

                    continue

                if self.status_ail == "muted":
                    sounds.debuff.play()
                    print(f"{self.name} is muted and cannot access their inventory!")
                    print("\nPress enter/return ")
                    print(self.battle_options.format(self.name))

                    continue

                if not battle.battle_inventory(self):
                    print(self.battle_options.format(self.name))

                    continue

                input('\nPress enter/return ')

            # Let the player repick if they try to use their class ability when they can't
            elif self.move in ['4', 'r']:
                self.move = '5'
                if self.lvl < 5:
                    # You must be at least level 5 to use your class ability
                    print('-'*25)
                    print(f"{self.name} has not yet realized their class's inner potential!")
                    input("\nPress enter/return ")
                    print('-'*25)
                    print(self.battle_options.format(self.name))

                    continue

                elif battle.temp_stats[self.name]['ability_used']:
                    # You can only use your ability once per battle.
                    print('{self.name} feels too drained to use their class ability again.')
                    print('-'*25)
                    print(self.battle_options.format(self.name))

                    continue

            # Battle Inventory
            elif self.move in ['5', 'd']:
                self.move = '5'

            else:
                continue

            return

    def class_ability(self):
        # Class abilities are special abilities only available to characters of certain classes.
        # Their purpose is to help make the characters more diverse, as well as encourage more
        # strategy being used.

        inv_name = self.name if self != units.player else 'player'
        battle.temp_stats[self.name]['ability_used'] = True

        print(ascii_art.player_art[self.class_.title()] % "{0} is making a move!\n".format(self.name))
        print("{0} uses the knowledge they've gained to unleash their class ability!".format(self.name))

        # Ranger Ability: Scout
        if self.class_ == 'ranger':
            # The ranger class identifies their enemy and prints their stats.
            # This is really useful for defeating bosses, which are often weak to
            # certain types and elements of attacks.

            print('-'*25)
            print('ABILITY: SCOUT')
            print('-'*25)

            print(f'As a Ranger, {self.name} identifies their enemy and focuses, increasing their pierce attack!')

            input("Press enter/return to view your enemy's stats ")

            print('-'*25)
            print("{0}'s STATS:".format(units.monster.name.upper()))

            print("""Attack: {0} | M. Attack: {1} | P. Attack: {2} | Speed: {3}
    Defense: {4} | M. Defense: {5} | P. Defense: {6} | Evasion: {7}
    Element: {8} | Elemental Weakness: {9}""".format(units.monster.attk, units.monster.m_attk, units.monster.p_attk,
                                                     units.monster.spd, units.monster.dfns, units.monster.m_dfns,
                                                     units.monster.p_dfns, units.monster.evad,
                                                     units.monster.element.title(),
                                                     {'fire': 'Water',
                                                      'water': 'Electric',
                                                      'electric': 'Earth',
                                                      'earth': 'Grass',
                                                      'grass': 'Wind',
                                                      'wind': 'Ice',
                                                      'ice': 'Fire',
                                                      'none': 'None',
                                                      'life': 'Death',
                                                      'death': 'Life'}[units.monster.element]))

            battle.temp_stats[self.name]['p_attk'] *= 1.35

            return True

        # Warrior Ability: Warrior's Spirit
        elif self.class_ == 'warrior':
            print('-'*25)
            print("ABILITY: WARRIOR'S SPIRIT")
            print('-'*25)
            print('As a Warrior, you channel your inner-strength and restore health and defense!')

            self.hp += math.ceil(max([0.35*self.max_hp, 35]))

            battle.p_temp_stats['dfns'] *= 1.35
            battle.p_temp_stats['m_dfns'] *= 1.35
            battle.p_temp_stats['p_dfns'] *= 1.35

            if self.hp > self.max_hp:
                self.hp -= (self.hp - self.max_hp)
            if self.mp > self.max_mp:
                self.mp -= (self.mp - self.max_mp)

            return True

        # Mage Ability: Artificial Intelligence
        elif self.class_ == "mage":
            print('-'*25)
            print("ABILITY: ARTIFICIAL INTELLIGENCE")
            print('-'*25)
            print('As a Mage, you focus intently and sharply increase your magical prowess!')
            print('Your magic attack and defense increase, and you regain MP!')

            self.mp += math.ceil(max([0.35*self.max_mp, 35]))

            if self.mp > self.max_mp:
                self.mp -= (self.mp - self.max_mp)

            battle.temp_stats[self.name]['m_attk'] *= 1.35
            battle.temp_stats[self.name]['m_dfns'] *= 1.35

            return True

        # Assassin Ability: Lethal Injection
        elif self.class_ == "assassin":
            print('-'*25)
            print("ABILITY: LETHAL INJECTION")
            print('-'*25)
            print('As an Assassin, you discreetly inject poison into your enemy!')

            units.monster.is_poisoned = True

            return True

        # Paladin Ability: Divine Intervention
        elif self.class_ == "paladin":
            print('-'*25)
            print('ABILITY: DIVINE INTERVENTION')
            print('-'*25)

            print('As a Paladin, you call upon the power of His Divinity to aid you!')
            print('You enemy has been turned to the "death" element, causing your')
            print('holy spells to inflict more damage! You also regain health and MP.')

            units.monster.element = "death"

            self.hp += math.ceil(max([0.15*self.max_hp, 15]))
            self.mp += math.ceil(max([0.15*self.max_mp, 15]))

            if self.hp > self.max_hp:
                self.hp -= (self.hp - self.max_hp)
            if self.mp > self.max_mp:
                self.mp -= (self.mp - self.max_mp)

            return True

        # Monk Ability: Chakra-smash
        elif self.class_ == 'monk':
            # Essentially a 2.5x crit. As an added bonus, this attack has a 15%
            # chance to get a crit itself, resulting in a total of an 3.75x critical.
            # This attack lowers the user defenses by 25% for three turns to balance it out.
            # If the user is weakened, this attack ignores that and will deal full damage anyway.
            print('-'*25)
            print('ABILITY: CHAKRA-SMASH')
            print('-'*25)

            print('As a monk, {0} meditates and focus their inner chi.'.format(self.name))
            print('After a brief moment of confusion from the enemy, {0} strikes, dealing'.format(self.name))
            print("an immense amount of damage in a single, powerful strike! As a result, {0}'s".format(self.name))
            print('defenses have been lowered by 15% until the end of the battle.\n')

            dam_dealt = (battle.p_temp_stats['attk'] - units.monster.dfns/2)*2.5
            dam_dealt *= (inv_system.equipped[inv_name]['weapon'].power + 1)
            dam_dealt = eval_element(self, units.monster, dam_dealt)

            if dam_dealt < 4:
                dam_dealt = 4

            if random.randint(1, 100) <= 15:
                main.smart_sleep(0.5)
                dam_dealt *= 1.5
                sounds.critical_hit.play()

                print("It's a critical hit! 1.5x damage!")

            if dam_dealt > 999:
                dam_dealt = 999

            main.smart_sleep(0.5)

            dam_dealt = math.ceil(dam_dealt)

            print('The attack deals {0} damage to the {1}!'.format(dam_dealt, units.monster.name))

            units.monster.hp -= dam_dealt

            battle.temp_stats[self.name]['dfns'] *= 0.85
            battle.temp_stats[self.name]['m_dfns'] *= 0.85
            battle.temp_stats[self.name]['p_dfns'] *= 0.85

            battle.temp_stats[self.name]['dfns'] = math.floor(battle.temp_stats[self.name]['dfns'])
            battle.temp_stats[self.name]['m_dfns'] = math.floor(battle.temp_stats[self.name]['m_dfns'])
            battle.temp_stats[self.name]['p_dfns'] = math.floor(battle.temp_stats[self.name]['p_dfns'])

            return True


class Monster(Unit):
    # All monsters use this class. Bosses use a sub-class called
    # "Boss" (located in bosses.py) which inherits from this.
    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad):
        Unit.__init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk, p_dfns, spd, evad)
        self.monster_name = ''  # The name of the monsters species (so a Fast Goblin's monster_name would be Goblin)
        self.status = ''        # The status effect that will be applied to the player if RNGsus wills it
        self.items = ''         # The item that the monster will drop if RNGsus wills it
        self.is_poisoned = False
        self.is_defending = False

    def physical_damage(self, mode, target):
        ise = inv_system.equipped[target.name if target != units.player else 'player']
        dr = sum([ise[armor].defense for armor in ise if isinstance(ise[armor], items.Armor)])

        if mode == 'melee':
            dam_dealt = self.attk - (battle.temp_stats[target.name]['dfns']/2)*(1 + dr)

        else:
            dam_dealt = self.p_attk - (battle.temp_stats[target.name]['p_dfns']/2)*(1 + dr)

        if random.randint(1, 100) <= 15:
            dam_dealt *= 1.5
            print("It's a critical hit! 1.5x damage!")

            sounds.critical_hit.play()
            main.smart_sleep(0.5)

        dam_dealt = eval_element(self, target, dam_dealt)

        if dam_dealt < 1:
            dam_dealt = 1

        if dam_dealt > 999:
            dam_dealt = 999

        return math.ceil(dam_dealt)

    def magical_damage(self, target):
        ise = inv_system.equipped[target.name if target != units.player else 'player']
        dr = sum([ise[armor].defense for armor in ise if isinstance(ise[armor], items.Armor)])

        dam_dealt = self.m_attk - (battle.temp_stats[target.name]['m_dfns']/2)*(1 + dr)
        dam_dealt = eval_element(self, target, dam_dealt)

        if dam_dealt < 1:
            dam_dealt = 1

        if dam_dealt > 999:
            dam_dealt = 999

        return math.ceil(dam_dealt)

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

        print(f'The {self.monster_name} is attempting to make {target.name} {status}...')
        main.smart_sleep(0.75)

        # There's a 50% chance that the status spell will work
        if random.randint(0, 1) == 1:
            sounds.buff_spell.play()
            print(f'{target.name} is now {status}!')
            target.status_ail = status

        else:
            sounds.debuff.play()
            print(f'The {self.monster_name} failed to make {target.name} {status}!')

        self.mp -= self.max_mp*0.1

    def check_poison(self):
        # Check whether the monster is poisoned or not.
        if self.is_poisoned:
            if random.randint(0, 9) == 0:  # 10% chance to recover per turn
                self.is_poisoned = False
                sounds.buff_spell.play()
                print(f'The {self.monster_name} recovered from the poison!')

                main.smart_sleep(0.5)

            else:
                poison_damage = math.floor(self.hp/6)
                self.hp -= poison_damage
                sounds.poison_damage.play()
                print(f'The {self.monster_name} took poison damage! (-{poison_damage} HP)')

                main.smart_sleep(0.5)

    def monst_name(self):
        m_type = {'Central Forest': ['Goblin Archer', 'Spriggan', 'Imp', 'Bat',
                                     'Beetle' if units.player.name != "Flygon Jones" else "Calculator"],

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
            self.attk_msg = "begins calculating the fuck out of"

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

        else:
            if modifier == 'Strong' and self.m_attk < self.attk and self.m_dfns < self.dfns:
                # High melee stats
                self.attk *= 1.2
                self.dfns *= 1.2

            elif modifier == 'Weak':
                # Low melee stats
                self.attk /= 1.2
                self.dfns /= 1.2

            elif modifier == 'Mystic' and self.m_attk > self.attk and self.m_dfns > self.dfns:
                # High magic stats
                self.m_attk *= 1.2
                self.m_dfns *= 1.2
                self.mp *= 1.2

            elif modifier == 'Foolish':
                # Low magic stats
                self.m_attk /= 1.2
                self.m_dfns /= 1.2

            else:
                modifier = ''

        # Adjust for problems that may happen with enemy stats
        for stat in ['self.attk', 'self.dfns', 'self.p_attk', 'self.p_dfns', 'self.m_attk', 'self.m_dfns',
                     'self.spd', 'self.evad']:

            if eval(stat) < 1:  # Enemy stats cannot be lower than one
                exec("{0} = 1".format(stat))

            exec("{0} = math.ceil({0})".format(stat))  # Enemy stats must be integers

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
        if not isinstance(self, bosses.Boss):
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

    def magic_ai(self):
        battle.turn_counter += 1

        target = random.choice([x for x in [
            units.player,
            units.solou,
            units.xoann,
            units.chyme,
            units.ran_af,
            units.parsto,
            units.adorine
        ] if x.enabled and x.status_ail != 'dead'])

        print(f"-{self.monster_name}'s Turn-")
        print(ascii_art.monster_art[self.monster_name] % f"The {self.monster_name} is making a move!\n")

        # 16.67% chance for the enemy to give a status ailment
        if target.status_ail == "none" and random.randint(0, 5) == 0 and self.mp >= self.max_mp*0.1:
            self.give_status(target)

        # Magic heal
        elif self.hp <= self.max_hp/5 and self.mp >= self.max_mp*0.2:
            print(f'The {self.monster_name} is attempting to cast a healing spell on itself...')
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

            print(f'The {self.monster_name} is preparing to cast a damaging spell on {target.name}!')
            main.smart_sleep(0.75)

            if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
                dam_dealt = self.magical_damage(target)

                print(f"The {self.monster_name}'s spell succeeds, and deals {dam_dealt} damage to {target.name}!")

                target.hp -= dam_dealt
                sounds.enemy_hit.play()

            else:
                sounds.attack_miss.play()
                print(f"The {self.monster_name}'s spell narrowly misses {target.name}!")

            self.mp -= self.max_mp*0.15

        # Non-magic Attack
        else:

            print(f'The {self.monster_name} {self.attk_msg} {target.name}')
            sounds.aim_weapon.play()

            main.smart_sleep(0.75)

            if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
                dam_dealt = self.physical_damage('pierce', target)

                print(f"The {self.monster_name}'s attack lands, dealing {dam_dealt} damage to {target.name}!")

                target.hp -= dam_dealt
                sounds.enemy_hit.play()

            else:
                sounds.attack_miss.play()
                print("The {0}'s attack narrowly misses {1}!".format(self.monster_name, target.name))

            self.check_poison()
            self.mp = math.ceil(self.mp)

    def ranged_ai(self):
        battle.turn_counter += 1

        target = random.choice([x for x in [
            units.player,
            units.solou,
            units.xoann,
            units.chyme,
            units.ran_af,
            units.parsto,
            units.adorine
        ] if x.enabled and x.status_ail != 'dead'])

        print(f"-{self.monster_name}'s Turn-")
        print(ascii_art.monster_art[self.monster_name] % f"The {self.monster_name} is making a move!\n")

        # At the moment, Ranged monsters are only capable of attacking
        print(f'The {self.monster_name} {self.attk_msg} {target.name}!')
        sounds.aim_weapon.play()

        main.smart_sleep(0.75)

        if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
            dam_dealt = self.physical_damage('pierce', target)

            print(f"The {self.monster_name}'s attack lands, dealing {dam_dealt} damage to {target.name}!")

            target.hp -= dam_dealt
            sounds.enemy_hit.play()

        else:
            sounds.attack_miss.play()
            print(f"The {self.monster_name}'s attack narrowly misses {target.name}!")

            self.check_poison()

    def melee_ai(self):
        battle.turn_counter += 1

        target = random.choice([x for x in [
            units.player,
            units.solou,
            units.xoann,
            units.chyme,
            units.ran_af,
            units.parsto,
            units.adorine
        ] if x.enabled and x.status_ail != 'dead'])

        print(f"-{self.monster_name}'s Turn-")
        print(ascii_art.monster_art[self.monster_name] % "The {0} is making a move!\n".format(self.monster_name))

        # Set defense back to normal if the monster defended last turn
        if self.is_defending:
            self.is_defending = False

            self.dfns /= 1.5
            self.m_dfns /= 1.5
            self.p_dfns /= 1.5
            self.dfns = math.floor(self.dfns)
            self.m_dfns = math.floor(self.m_dfns)
            self.p_dfns = math.floor(self.p_dfns)

        # Melee monsters have a 1 in 6 (16.667%) chance to defend
        elif random.randint(0, 5) == 0:
            self.is_defending = True
            sounds.buff_spell.play()

            self.dfns *= 1.5
            self.m_dfns *= 1.5
            self.p_dfns *= 1.5

            self.dfns = math.ceil(self.dfns)
            self.p_dfns = math.ceil(self.p_dfns)
            self.m_dfns = math.ceil(self.m_dfns)

            print("The {0} defends itself from further attacks! (Enemy Defense Raised!)".format(self.monster_name))

        # If the monster doesn't defend, then it will attack!
        else:
            print(f'The {self.monster_name} {self.attk_msg} {target.name}!')
            sounds.sword_slash.play()

            main.smart_sleep(0.75)

            if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
                dam_dealt = self.physical_damage('melee', target)

                print(f"The {self.monster_name}'s attack lands, dealing {dam_dealt} damage to {target.name}!")

                target.hp -= dam_dealt
                sounds.enemy_hit.play()

            else:
                sounds.attack_miss.play()
                print(f"The {self.monster_name}'s attack narrowly misses {target.name}!")

            self.check_poison()


def deal_damage(attacker, target, damage_type, do_crits=True):
    # This will contain a universal damage formula shared by the three damage types (magical, physical, piercing)
    pass


def eval_element(attacker, target, damage):
    # Fire < Water < Electricity < Earth < Wind < Grass < Ice < Fire
    # Life < Death and Death < Life
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
        'life': ['life', 'death'],
        'death': ['death', 'life']
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
