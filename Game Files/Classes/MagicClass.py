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

import sys
import json
import random
import time
import math
import pygame

import UnitClass
import units
import battle
import inv_system
import sounds
import ascii_art
import magic

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# This is the message that is printed if you attempt to use magic
# without the required amount of mana.
out_of_mana = "-------------------------\n{0} doesn't have enough mana to cast {1}."


class Spell:
    def __init__(self, name, desc, mana, req_lvl, a_c=('mage',)):
        self.name = name
        self.desc = desc
        self.mana = mana
        self.req_lvl = req_lvl
        self.a_c = a_c  # These are the classes that are able to obtain this spell

    def __str__(self):
        return self.name

    def use_mana(self, user):
        user.mp -= self.mana
        if user.mp < 0:
            user.mp = 0


class Healing(Spell):
    # Healing spells are spells that restore your HP during battle
    def __init__(self, name, desc, mana, req_lvl, health, thresh, a_c=('mage', 'paladin')):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.health = health
        self.thresh = thresh

    def __str__(self):
        return self.name

    def use_magic(self, user, is_battle):
        Spell.use_mana(self, user)
        target = user.target

        # Healing spells will always restore a minimum of user.hp*thresh.
        # e.g. A spell that heals 20 HP but has a 20% threshold will restore 20 HP for someone
        # with 45 max HP, but will restore 32 HP for someone with 160 max HP.
        # In addition to this, the user restores an additional 2*Wisdom, unless they are a
        # Paladin in which case it it 4*Wisdom.
        if self.health < target.hp*self.thresh:
            if user.class_ == 'paladin':
                total_heal = target.hp*self.thresh + 4*user.attributes['wis']

            else:
                total_heal = 2*user.attributes['wis']

        else:
            if user.class_ == 'paladin':
                total_heal = self.health + 4*user.attributes['wis']

            else:
                total_heal = self.health + 2*user.attributes['wis']

        target.hp += total_heal

        if target.hp > target.max_hp:
            target.hp -= (target.hp - target.max_hp)

        target.hp = math.ceil(target.hp)

        sounds.magic_healing.play()

        if is_battle:
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
            print(f'Using "{self.name}", {target.name} is healed by {total_heal} HP!')

        else:
            print('-'*25)
            print(f'Using "{self.name}", {target.name} is healed by {total_heal} HP!')
            input("\nPress enter/return ")
            print('-'*25)


class Damaging(Spell):
    # Damaging spells are spells that deal damage to the enemy during battle.
    # Just like normal attacks, they have a chance to miss based on
    # the enemy's evade stat.
    def __init__(self, name, desc, mana, req_lvl, damage, element, a_c=('mage',)):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.damage = damage
        self.element = element

    def __str__(self):
        return self.name

    def use_magic(self, user):
        Spell.use_mana(self, user)
        target = user.target

        print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
        print(f'{user.name} attempts to summon a powerful spell...')

        sounds.magic_attack.play()
        main.smart_sleep(0.75)
        dam_dealt = UnitClass.deal_damage(user, target, "magical", spell_power=self.damage)

        # If the monster's evasion (with a max of 256) is higher than the user's accuracy roll, the spell will land
        if random.randint(1, 512) in range(target.evad, 512):
            sounds.enemy_hit.play()
            target.hp -= dam_dealt
            print(f'Using the power of {self.name}, {user.name} deals {dam_dealt} damage to the {target.monster_name}!')

        else:
            sounds.attack_miss.play()
            print(f"The {target.monster_name} narrowly dodges {user.name}'s spell!")


class Buff(Spell):
    # Buffs are spells that temporarily raise the player's stats
    # during battle. They last until the battle is over, at which
    # point the player's stats will return to normal.
    def __init__(self, name, desc, mana, req_lvl, increase, stat, a_c=('mage', 'monk')):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.increase = increase
        self.stat = stat

    def __str__(self):
        return self.name

    def use_magic(self, user):
        Spell.use_mana(self, user)
        target = user.target

        print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

        if user == target:
            print(f"{user.name} raises their stats using the power of {self.name}!")

        else:
            print(f"{user.name} raises {target.name}'s stats using the power of {self.name}!")

        sounds.buff_spell.play()

        battle.temp_stats[target.name][self.stat] *= 1 + self.increase
        battle.temp_stats[target.name][self.stat] = math.ceil(battle.temp_stats[user.name][self.stat])
        units.fix_stats()


def pick_cat(user, is_battle=True):
    inv_name = user.name if user != units.player else 'player'

    while True:
        do_continue = False
        print("""{0}'s spellbook:
      [1] Damaging Spells
      [2] Buff Spells
      [3] Healing Spells
      [4] Use Most Recent Spell""".format(user.name))
        spam = True
        while spam:
            cat = input('Input [#] (or type "exit"): ')

            if cat == '1':
                cat = 'Damaging'

            elif cat == '2':
                cat = 'Buffs'

            elif cat == '3':
                cat = 'Healing'

            elif cat == '4':
                spell = magic.spellbook[inv_name]['Previous Spell']

                if spell:
                    spell = spell[0]

                    if is_battle:
                        user.c_spell = spell

                        if isinstance(spell, Healing) or isinstance(spell, Buff):
                            user.choose_target(f"cast {spell.name} on", ally=True, enemy=False)

                            return True

                        else:
                            user.choose_target(f"cast {spell.name} on")

                            break

                    else:
                        user.choose_target(f"cast {spell.name} on", ally=True, enemy=False)
                        spell.use_magic(user, is_battle)

                        break

                else:
                    print('-'*25)
                    print(f'{user.name} has no previously used spells!')
                    print('-'*25)

                    break

            else:
                if cat.lower() in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*25)
                    return False

                else:
                    continue

            if do_continue:
                continue

            if not magic.spellbook[inv_name][cat]:
                print('-'*25)
                print('You do not yet have any spells in the {0} category.'.format(cat))
                print('-'*25)
                continue

            if pick_spell(cat, user, is_battle):
                return True

            break


def pick_spell(cat, user, is_battle):
    inv_name = user.name if user != units.player else 'player'

    print('-'*25)
    while True:
        padding = len(max([spell.name for spell in magic.spellbook[inv_name][cat]], key=len))
        print(f"{cat} Spells [{user.name} has {user.mp} mana remaining]:")

        for x, y in enumerate(magic.spellbook[inv_name][cat]):
            print(f"      [{x + 1}] {y} --{'-'*(padding - len(y.name))}> {y.mana} MP")

        while True:
            spell = input('Input [#] (or type "back"): ').lower()

            try:
                spell = magic.spellbook[inv_name][cat][int(spell) - 1]

            except (ValueError, IndexError):
                if spell in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*25)

                    return False

                continue

            if spell.mana > user.mp:
                print(out_of_mana.format(user.name, spell.name))

                break

            magic.spellbook[inv_name]['Previous Spell'] = [spell]

            if is_battle:
                user.c_spell = spell

                if isinstance(spell, Healing) or isinstance(spell, Buff):
                    user.choose_target(f"cast {spell.name} on", ally=True, enemy=False)

                    return True

                else:
                    user.choose_target(f"cast {spell.name} on")

                    break

            else:
                user.choose_target(f"cast {spell.name} on", ally=True, enemy=False)
                spell.use_magic(user, is_battle)

                break


def new_spells(character):
    # Teach the player new spells as they level up, or low-level spells not previously in the game.
    for spell in magic.all_spells:
        if isinstance(spell, Damaging):
            cat = 'Damaging'
        elif isinstance(spell, Healing) or spell.name == 'Relieve Affliction':
            cat = 'Healing'
        elif isinstance(spell, Buff):
            cat = 'Buffs'

        # Only give the character spells that they are a high enough level for
        if character.lvl >= spell.req_lvl:
            for x in magic.spellbook[character.name if character != units.player else 'player'][cat]:
                if x.name == spell.name:
                    break

            else:
                # Almost all spells can be learned by mages, but only a few can be learned by other classes
                if character.class_ not in spell.a_c:
                    continue

                sounds.item_pickup.play()
                magic.spellbook[character.name if character != units.player else 'player'][cat].append(spell)

                input(f'{character.name} has learned "{spell}", a new {cat} spell! | Press enter/return ')

