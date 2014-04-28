import sys
import json
import monsters
import battle
import random
import inv_system

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

# This is the message that is printed if you attempt to use magic
# without the required amount of mana.
out_of_mana = """-------------------------
You don't have enough mana to cast that spell!
-------------------------"""

class Spell:
    def __init__(self, name, desc, mana, req_lvl):
        self.name = name
        self.desc = desc
        self.mana = mana
        self.req_lvl = req_lvl
    def use_mana(self):
        main.player.mp -= self.mana
        if main.player.mp < 0:
            main.player.mp = 0

class Healing(Spell):
    # Healing spells are spells that restore your HP during battle
    def __init__(self, name, desc, mana, req_lvl, health):
        Spell.__init__(self, name, desc, mana, req_lvl)
        self.health = health
    def __str__(self):
        return self.name
    def use_magic(self):
        if main.player.mp >= self.mana:
            print()
            Spell.use_mana(self)
            main.player.hp += self.health + int(main.static['int']/4) + random.randint(-2, 2)
            if main.player.hp > main.static['hp_p']:
                main.player.hp -= (main.player.hp - main.static['hp_p'])
            print('-Player Turn-')
            print('Using "{0}", you are healed by {1} HP!'.format(self.name, self.health))
            return True
        else:
            print(out_of_mana)
            return False

class Damaging(Spell):
    # Damaging spells are spells that deal damage to the enemy during battle.
    # Just like normal attacks, they have a chance to miss based on
    # the enemy's evade stat.
    def __init__(self, name, desc, mana, req_lvl, damage, element):
        Spell.__init__(self, name, desc, mana, req_lvl)
        self.damage = damage
        self.element = element
    def __str__(self):
        return self.name
    def use_magic(self, var, dodge):
        if main.player.mp >= self.mana:
            print()
            Spell.use_mana(self)
            attk_pwr = int(self.damage + (main.player.m_attk/3) -
                          (battle.monster.m_dfns/2) + var)
            attk_pwr = eval_element(
                       p_elem=self.element,
                       m_elem=monsters.monster.element,
                       p_dmg=attk_pwr)[0]
            print('-Player Turn-')
            print('You begin to use your {0} to summon a powerful spell.'.format(
                  inv_system.equipped['weapon']))
            if dodge in range(monsters.monster.evad, 250):
                print('Using the power of "{0}", you deal {1} damage to the {2}!'.format(
                      self.name, attk_pwr, monsters.monster.name))
                monsters.monster.hp -= attk_pwr
            else:
                print('The {0} dodges your attack!'.format(monsters.monster.name))
            return True
        else:
            print(out_of_mana)
            return False

class Buff(Spell): # Buffs are spells that temporarily raise the player's stats
                   # during battle. They last until the battle is over, at which
                   # point the player's stats will return to normal.
    def __init__(self, name, desc, mana, req_lvl, incre, stat):
        Spell.__init__(self, name, desc, mana, req_lvl)
        self.incre = incre
        self.stat = stat
    def __str__(self):
        return self.name
    def use_magic(self):
        if main.player.mp >= self.mana:
            print()
            Spell.use_mana(self)
            print('-Player Turn-')
            print('Using the power of {0}, your {1} increases temporarily by {2}!'.format(
                  self.name, self.stat, self.incre))
            if self.stat == 'Defense':
                battle.temp_stats['dfns'] += self.incre
            elif self.stat == 'Magic Defense':
                battle.temp_stats['m_dfns'] += self.incre
            elif self.stat == 'Speed':
                battle.temp_stats['spd'] += self.incre
            elif self.stat == 'Evasion':
                battle.temp_stats['evad'] += self.incre
            elif self.stat == 'Attack':
                battle.temp_stats['attk'] += self.incre
            elif self.stat == 'Magic Attack':
                battle.temp_stats['m_attk'] += self.incre
            return True
        else:
            print(out_of_mana)
            return False

w_flame = Damaging('Weak Flame', "Summon a weak fireball to destroy your foes.", 3, 2, 4, "fire")
f_blaze = Damaging('Fierce Blaze', "Summon a powerful flame to destroy your foes.", 9, 8, 12, "fire")
g_infer = Damaging('Grand Inferno', "Summon a monsterous blaze destroy your foes.", 18, 18, 23, "fire")

in_spark = Damaging('Inferior Spark', "Summon a weak spark to destroy your foes.", 3, 2, 4, "electric")
pwr_jolt = Damaging('Powerful Jolt', "Summon a powerful jolt of energy to destroy your foes.", 10, 8, 12, "electric")
sp_storm = Damaging('Superior Storm', "Summon a devastating lightning storm to destroy your foes.", 19, 18, 23, "electric")

mi_heal = Healing('Minor Healing', "Restore a small amount of HP by using magic.", 3, 2, 20)
ad_heal = Healing('Advanced Healing', "Restore a large amount of HP by using magic.", 10, 9, 60)
dv_heal = Healing('Divine Healing', "Call upon the arcane arts to greatly restore your HP.", 25, 20, 125)

m_quick = Buff('Minor Quickness', "Temporarily raise your speed by a small amount.", 2, 4, 3, "Speed")
m_evade = Buff('Minor Evade', "Temporarily raise your evasion by a small amount.", 2, 4, 3, "Evasion")

m_defend = Buff('Minor Defend', "Temporarily raise your defense by a small amount.", 2, 5, 2, "Defense")
m_shield = Buff('Minor Shield', "Temporarily raise your magic defense by a small amount.", 2, 5, 2, "Magic Defense")

m_stren = Buff('Minor Strengthen', "Temporarily raise your attack by a small amount.", 2, 6, 2, "Attack")
m_power = Buff('Minor Empower', "Temporarily raise your magic attack by a small amount.", 2, 6, 2, "Magic Attack")

a_defend = Buff('Adept Defend', "Temporarily raise your defense by a large amount.", 7, 12, 5, "Defense")
a_shield = Buff('Adept Shield', "Temporarily raise your magic defense by a small amount.", 7, 12, 5, "Magic Defense")

a_stren = Buff('Adept Strengthen', "Temporarily raise your attack by a large amount.", 7, 10, 5, "Attack")
a_power = Buff('Adept Empower', "Temporarily raise your magic attack by a large amount.", 7, 10, 5, "Magic Attack")

spells = [
         w_flame,            # Level 1
         in_spark, mi_heal,  # Level 2
         m_quick, m_evade,   # Level 4
         m_defend, m_shield, # Level 5
         m_stren, m_power,   # Level 6
         f_blaze,            # Level 7
         pwr_jolt,           # Level 8
         ad_heal,            # Level 9
         a_stren, a_power,   # Level 10
         a_defend, a_shield, # Level 12
         g_infer,            # Level 17
         sp_storm,           # Level 18
         dv_heal             # Level 20
    ]

def eval_element(p_elem='None', m_elem='None', m_dmg=0, p_dmg=0):
    element_list = ['Fire', 'Water', 'Electric', 'Earth',
                    'Grass', 'Wind', 'Ice']
    for x, y in enumerate(element_list):
        if p_elem == y:
            player = x
    else:
        return [p_dmg, m_dmg]
    for a, b in enumerate(element_list):
        if m_elem == b:
            monster = a
    else:
        return [p_dmg, m_dmg]
    try:
        if m_elem == element_list[player + 1]:
            p_dmg /= 1.5
            p_dmg = int(p_dmg)
        elif m_elem == element_list[player - 1]:
            p_dmg *= 1.5
            p_dmg = int(p_dmg)
    except IndexError:
        m_elem = 'Fire'
        if p_elem == 'Ice':
            p_dmg /= 1.5
            p_dmg = int(p_dmg)
        elif p_elem == 'Water':
            p_dmg *= 1.5
            p_dmg = int(p_dmg)
    try:
        if p_elem == element_list[monster + 1]:
            m_dmg /= 1.5
            m_dmg = int(m_dmg)
        elif p_elem == element_list[monster - 1]:
            m_dmg *= 1.5
            m_dmg = int(m_dmg)
    except IndexError:
        p_elem = 'Fire'
        if m_elem == 'Ice':
            m_dmg /= 1.5
            m_dmg = int(m_dmg)
        elif m_elem == 'Water':
            m_dmg *= 1.5
            m_dmg = int(m_dmg)
    return [p_dmg, m_dmg]


spellbook = {'Healing':[], 'Damaging':[w_flame], 'Buffs':[]}

def pick_cat(var, dodge):
    while True:
        cat = input('Spellbook: ' +
                    ', '.join(['"' + x + '"' for x in spellbook]) +
                     ' | Input category: ')
        try:
            cat = cat.title()
        except AttributeError:
            continue
        for i in spellbook:
            if cat == i:
                break
        else:
            continue
        if not spellbook[cat]:
            print('-'*25)
            print('You do not yet have any spells in the {0} category.'.format(cat))
            print('-'*25)
            continue
        if pick_spell(cat, var, dodge):
            return True

def pick_spell(cat, var, dodge):
    print('-'*25)
    while True:
        spell = input(cat + ': ' + ', '.join(
            ['"' + str(x) + '" (' + str(x.mana) + ' MP)' for x in spellbook[cat]]
            ) + ' | Input spell (or type "back"): ')
        if spell == '':
            continue
        try:
            spell = spell.title()
        except AttributeError:
            continue
        if spell == 'Back':
            return False
        for i in spellbook[cat]:
            if spell == str(i):
                spell = i
                break
        else:
            continue
        print('-'*25)
        print(''.join([str(spell), ': ', spell.desc, ' | ', str(spell.mana), ' MP']))
        print('-'*25)
        while True:
            y_n = input('Use {0}? | Yes or No: '.format(str(spell)))
            if y_n == '':
                continue
            try:
                y_n = y_n.lower()
            except AttributeError:
                continue
            if y_n in ['yes', 'y']:
                if isinstance(spell, Damaging):
                    if spell.use_magic(var, dodge):
                        return True
                    else:
                        return False
                else:
                    if spell.use_magic():
                        return True
                    else:
                        return False
            elif y_n in ['no', 'n']:
                break

def new_spells():
    global spellbook
    for spell in spells:
        if isinstance(spell, Damaging):
            cat = 'Damaging'
        elif isinstance(spell, Healing):
            cat = 'Healing'
        elif isinstance(spell, Buff):
            cat = 'Buffs'
        if main.player.lvl >= spell.req_lvl:
            for x in spellbook[cat]:
                if x.name == spell.name:
                    break
            else:
                spellbook[cat].append(spell)
                print('You have learned "{0}", a new {1} spell!'.format(
                      str(spell), cat if not cat.endswith('s'
                      ) else cat[0:len(cat) - 1]))

def serialize_sb(path):
    j_spellbook = {}
    for cat in spellbook:
        j_spellbook[cat] = []
        for spell in spellbook[cat]:
            j_spellbook[cat].append(spell.__dict__)
    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_spellbook, f, indent=4, separators=(', ', ': '))

def deserialize_sb(path):
    global spellbook
    norm_sb = {}
    with open(path, mode='r', encoding='utf-8') as f:
        j_spellbook = json.load(f)
    for category in j_spellbook:
        norm_sb[category] = []
        for spell in j_spellbook[category]:
            if category == 'Damaging':
                x = Damaging('', '', '', '', '', '')
            elif category == 'Healing':
                x = Healing('', '', '', '', '')
            elif category == 'Buffs':
                x = Buff('', '', '', '', '', '')
            x.__dict__ = spell
            norm_sb[category].append(x)
    spellbook = norm_sb