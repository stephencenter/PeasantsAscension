import sys
import json
import monsters
import inv_system

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

out_of_mana = """\
-------------------------
You don't have enough mana to cast this spell!
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
    def __init__(self, name, desc, mana, req_lvl, health):
        Spell.__init__(self, name, desc, mana, req_lvl)
        self.health = health
    def __str__(self):
        return self.name
    def use_magic(self):
        if main.player.mp >= self.mana:
            print()
            Spell.use_mana(self)
            main.player.hp += self.heal
            if main.player.hp > main.static['hp_p']:
                main.player.hp -= (main.player.hp - main.static['hp_p'])
            print('-Player Turn-')
            print('Using "%s", you are healed by %s HP!' % (self.name, self.health))
        else:
            print(out_of_mana)
            return False

class Damaging(Spell):
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
            attk_pwr = int(self.damage + (main.player.m_attk/3) - (monsters.monster.m_dfns/2) + var)
            print('-Player Turn-')
            print('You begin to use your %s to summon a powerful spell.' % (inv_system.equipped['weapon']))
            if dodge in range(monsters.monster.evad, 250):
                print('Using the power of "%s", you deal %s damage to the %s!' % (self.name, attk_pwr, monsters.monster.name))
                monsters.monster.hp -= attk_pwr
            else:
                print('The %s dodges your attack!' % (monsters.monster.name))
            return True
        else:
            print(out_of_mana)
            return False

w_flame = Damaging('Weak Flame', "Summon a weak fireball to destroy your foes.", 3, 1, 3, "fire")
f_blaze = Damaging('Fierce Blaze', "Summon a powerful flame to destroy your foes.", 9, 7, 11, "fire")
g_infer = Damaging('Grand Inferno', "Summon a monsterous blaze destroy your foes.", 18, 17, 22, "fire")

mi_heal = Healing('Minor Healing', "Restore a small amount of HP by using magic.", 2, 2, 15)
ad_heal = Healing('Advanced Healing', "Restore a decent amount of HP by using magic.", 10, 9, 45)
dv_heal = Healing('Divine Healing', "Call upon the arcane arts to restore your HP.", 25, 20, 115)

spells = [w_flame, mi_heal, f_blaze, ad_heal, g_infer, dv_heal]
spellbook = {'Healing':[], 'Damaging':[w_flame]}

def pick_cat(var, dodge):
    while True:
        cat = input('Spellbook: ' + ', '.join(['"' + x + '"' for x in spellbook]) + ' | Input catagory (or type "exit"): ')
        try:
            cat = cat.title()
        except AttributeError:
            continue
        if cat == 'Exit':
            return False
        for i in spellbook:
            if cat == i:
                break
        else:
            continue
        if not spellbook[cat]:
            print('-'*25)
            print('You do not yet have any spells in the %s catagory.' % (cat))
            print('-'*25)
            continue
        if pick_spell(cat, var, dodge):
            return True

def pick_spell(cat, var, dodge):
    print('-'*25)
    while True:
        spell = input(cat + ': ' + ', '.join(['"' + str(x) + '" (' + str(x.mana) + ' MP)' for x in spellbook[cat]]) + ' | Input spell (or type "back"): ')
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

def new_spells():
    global spellbook
    for spell in spells:
        if isinstance(spell, Damaging):
            cat = 'Damaging'
        elif isinstance(spell, Healing):
            cat = 'Healing'
        if main.player.lvl == spell.req_lvl:
            spellbook[cat].append(spell)
            print('You have learned "%s", a new %s spell!' % (str(spell), cat))

def serialize_sb(path):
    j_spellbook = {}
    for cat in spellbook:
        j_spellbook[cat] = []
        for spell in spellbook[cat]:
            j_spellbook[cat].append(spell.__dict__)
    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_spellbook, f)

def deserialize_sb(path):
    global spellbook
    norm_sb = {}
    with open(path, mode='r', encoding='utf-8') as f:
        j_spellbook = json.load(f)
    for catagory in j_spellbook:
        norm_sb[catagory] = []
        for spell in j_spellbook[catagory]:
            if catagory == 'Damaging':
                x = Damaging('', '', '', '', '', '')
            elif catagory == 'Healing':
                x = Healing('', '', '', '', '')
            x.__dict__ = spell
            norm_sb[catagory].append(x)
    spellbook = norm_sb