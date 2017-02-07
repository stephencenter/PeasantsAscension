from MagicClass import *

# -- Damaging Spells -- #
# Neutral
magic_shot = Damaging('Magical Shot',
                      "Hurl a small ball of magical energy at your enemies! (Weak)",
                      3, 1, 0.25, "none",
                      a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))
magic_burst = Damaging('Magical Burst',
                       "Shatter your enemy's defenses with a burst of magical energy! (Moderate)",
                       9, 11, 0.5, "none",
                       a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))
magic_blast = Damaging('Magical Blast',
                       "Bomb your enemies with a detonating ball of magical energy! (Strong)",
                       18, 23, 1, "none",
                       a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))

# Fire
w_flame = Damaging('Weak Flame',
                   "Summon a weak fireball to destroy your foes. (Weak)",
                   3, 2, 0.25, "fire")
f_blaze = Damaging('Fierce Blaze',
                   "Summon a powerful flame to destroy your foes. (Moderate)",
                   10, 12, 0.5, "fire")
g_infer = Damaging('Grand Inferno',
                   "Unleash a monstrous blaze destroy your foes. (Strong)",
                   20, 24, 1, "fire")

# Grass
lef_blad = Damaging('Leaf Blade',
                    "Summon a weak blade of grass to destroy your foes. (Weak)",
                    3, 2, 0.25, "grass")
gra_gren = Damaging('Grass Grenade',
                    "Summon a small explosion to destroy your foes. (Moderate)",
                    10, 12, 0.5, "grass")
vin_strm = Damaging('Vine Storm',
                    "Unleash a frenzy of powerful vines to destroy your foes. (Strong)",
                    20, 24, 1, "grass")

# Electricity
in_spark = Damaging('Inferior Spark',
                    "Summon a weak spark to destroy your foes. (Weak)",
                    3, 3, 0.25, "electric")
pwr_jolt = Damaging('Powerful Jolt',
                    "Summon a powerful jolt of energy to destroy your foes. (Moderate)",
                    10, 13, 0.5, "electric")
sp_storm = Damaging('Superior Storm',
                    "Unleash a devastating lightning storm to destroy your foes. (Strong)",
                    20, 25, 1, "electric")

# Water
bub_splsh = Damaging('Bubble Splash',
                     "Summon a small wave of bubbles to destroy your foes. (Weak)",
                     3, 3, 0.25, "water")
wtr_blast = Damaging('Water Blast',
                     "Summon a large burst of water to destroy your foes. (Moderate)",
                     10, 13, 0.5, "water")
tsunami = Damaging('Tsunami',
                   "Unleash a terrifying barrage of waves upon your foes. (Strong)",
                   20, 25, 1, "water")

# Earth
mud_toss = Damaging('Mud Toss',
                    "Summon a small ball of mud to throw at your foes. (Weak)",
                    3, 4, 0.25, "earth")
rock_slam = Damaging('Rock Slam',
                     "Crush your enemies with a wall of solid rock. (Moderate)",
                     10, 13, 0.5, "earth")
earthquake = Damaging("Earthquake",
                      "Wreck havoc on your enemies with a powerful earthquake. (Strong)",
                      20, 25, 1, "earth")

# Ice
icicle_dagger = Damaging('Icicle Dagger',
                         "Hurl a volley of supercooled icicles at your enemies. (Weak)",
                         3, 4, 0.25, "ice")
hail_storm = Damaging('Hailstorm',
                      "Rain ice upon your enemies with unrelenting force! (Moderate)",
                      11, 14, 0.5, 'ice')
blizzard = Damaging('Blizzard',
                    "Devastate your enemies with a terrifying flurry of ice and wind. (Strong)",
                    23, 26, 1, 'ice')

# Wind
m_gust = Damaging('Minor Gust',
                  "Batter your enemies with powerful gusts and winds! (Weak)",
                  3, 4, 0.25, "wind")
microburst = Damaging('Microburst',
                      "Decimate your foes with a powerful blast of wind! (Moderate)",
                      11, 14, 0.5, "wind")
cyclone = Damaging('Cyclone',
                   "Demolish all that stand in your path with a terrifying tornado! (Strong)",
                   23, 26, 1, "wind")

# Life
purify = Damaging('Purify',  # Paladins start with this spell
                  "Call upon His Divinity to cast out evil creatures! (Weak)",
                  3, 5, 0.25, "life", a_c=('paladin', 'mage'))
smite = Damaging('Holy Smite',
                 "Strike down unholy beings using His Divinity's power! (Moderate)",
                 11, 15, 0.5, "life", a_c=('paladin', 'mage'))
moonbeam = Damaging('Moonbeam',
                    "Utterly destroy evil creatures with holy rays from the moon! (Strong)",
                    23, 27, 1, "life", a_c=('paladin', 'mage'))


# Death
curse = Damaging('Evil Curse',
                 "Call upon His Wickedness to harm holy creatures! (Weak)",
                 3, 5, 0.25, "death")
desecration = Damaging('Desecration',
                       "Defile holy spirits with an evil aura! (Moderate)",
                       11, 15, 0.5, "death")
unholy_rend = Damaging('Unholy Rend',
                       "Annihilate holy creatures with a searing blow! (Strong)",
                       23, 27, 1, "death")

# -- Healing -- #
pit_heal = Healing('Pitiful Healing',  # Every character starts with this spell
                   """Restore a downright pitiful amount of HP by using magic.
Heals 10 HP or 5% of the target's max HP, whichever is more (Tier 1: Pitiful)""",
                   1, 1, 10, 0.05)

min_heal = Healing('Minor Healing',  # The Paladin also starts with this spell
                   """Restore a small amount of HP by using magic.
Heals 25 HP or 20% of the target's max HP, whichever is more (Tier 2: Weak)""",
                   3, 3, 25, 0.2, a_c=('assassin', 'monk', 'paladin', 'mage', 'warrior', 'ranger'))

adv_heal = Healing('Advanced Healing',  # This tier and up can only be learned by Paladins and Mages
                   """Restore a large amount of HP by using magic.
Heals 70 HP, or 50% of the target's max HP, whichever is more (Tier 3: Moderate)""",
                   10, 15, 70, 0.5, a_c=('paladin', 'mage'))

div_heal = Healing('Divine Healing',
                   """Call upon the arcane arts to greatly restore your HP.
Heals 100% of the target's HP (Tier 4: Strong)""",
                   25, 28, 0, 1, a_c=('paladin', 'mage'))

# -- Buffs -- #

# Movement Buffs
m_quick = Buff('Minor Quickness',
               "Temporarily raise your speed by a small amount. (Weak)",
               3, 1, 0.25, "spd", a_c=('mage', 'monk', 'ranger', 'assassin'))
m_evade = Buff('Minor Evade',
               "Temporarily raise your evasion by a small amount. (Weak)",
               3, 1, 0.25, "evad", a_c=('mage', 'monk', 'ranger', 'assassin'))

a_quick = Buff('Adept Quickness',
               "Temporarily raise your speed by a large amount. (Moderate)",
               6, 10, 0.5, "spd", a_c=('mage', 'monk', 'ranger', 'assassin'))
a_evade = Buff('Adept Evade',
               "Temporarily raise your evasion by a large amount. (Moderate)",
               6, 10, 0.5, "evad", a_c=('mage', 'monk', 'ranger', 'assassin'))

# Defense Buffs
m_defend = Buff('Minor Defend',
                "Temporarily raise your defense by a small amount. (Weak)",
                3, 3, 0.25, "dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
m_shield = Buff('Minor Shield',
                "Temporarily raise your magic defense by a small amount. (Weak)",
                3, 3, 0.25, "m_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
m_block = Buff('Minor Block',
               "Temporarily raise your pierce defense by a small amount. (Weak)",
               3, 7, 0.25, "p_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

a_defend = Buff('Adept Defend',
                "Temporarily raise your defense by a large amount. (Moderate)",
                6, 13, 0.5, "dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
a_shield = Buff('Adept Shield',
                "Temporarily raise your magic defense by a large amount. (Moderate)",
                6, 13, 0.5, "m_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))
a_block = Buff('Adept Block',
               "Temporarily raise your pierce defense by a large amount. (Moderate)",
               6, 17, 0.5, "p_dfns", a_c=('mage', 'monk', 'warrior', 'paladin'))

# Attack Buffs
m_stren = Buff('Minor Strengthen',
               "Temporarily raise your attack by a small amount. (Weak)",
               3, 6, 0.25, "attk", a_c=('mage', 'paladin', 'warrior', 'assassin', 'monk'))
m_power = Buff('Minor Empower',
               "Temporarily raise your magic attack by a small amount. (Weak)",
               3, 6, 0.25, "m_attk")
m_aim = Buff('Minor Aim',
             "Temporarily raise your pierce attack by a small amount. (Weak)",
             3, 7, 0.25, "p_attk", a_c=('ranger', 'mage', 'monk'))

a_stren = Buff('Adept Strengthen',
               "Temporarily raise your attack by a large amount. (Moderate)",
               6, 16, 0.5, "attk", a_c=('mage', 'paladin', 'warrior', 'assassin', 'monk'))
a_power = Buff('Adept Empower',
               "Temporarily raise your magic attack by a large amount. (Moderate)",
               6, 16, 0.5, "m_attk")
a_aim = Buff('Adept Aim',
             "Temporarily raise your pierce attack by a large amount. (Moderate)",
             6, 17, 0.5, "p_attk", a_c=('ranger', 'mage', 'monk'))

# -- Other Spells -- #
r_affliction = Spell('Relieve Affliction', 'Cure yourself of all status ailments, such as poison or weakness.', 4, 5)


def relieve_affliction(user, is_battle):
    if user.mp >= r_affliction.mana:
        if user.status_ail != 'none':

            Spell.use_mana(r_affliction, user)

            if is_battle:
                print(f"\n-{user.name}'s Turn-")
                print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

            print(f'Using the power of {r_affliction.name}, {user.name} is cured of their afflictions!')

            user.status_ail = 'none'
            sounds.buff_spell.play()

            return True

        else:
            print('-'*25)
            print("{0} doesn't have any status ailments.".format(user.name))
            print('-'*25)
            return False

    else:
        print(out_of_mana)
        return False


r_affliction.use_magic = relieve_affliction

all_spells = [
    pit_heal, min_heal, adv_heal, div_heal,  # Healing Spells (Level 1, 3, 15, 28)
    magic_shot, magic_burst, magic_blast,    # Neutral-typed Spells (Level 1, 11, 23)
    w_flame, f_blaze, g_infer,               # Fire Spells (Level 2, 12, 24)
    lef_blad, gra_gren, vin_strm,            # Grass Spells (Level 2, 12, 24)
    in_spark, pwr_jolt, sp_storm,            # Electric Spells (Level 3, 13, 25)
    bub_splsh, wtr_blast, tsunami,           # Water Spells (Level 3, 13, 25)
    mud_toss, rock_slam, earthquake,         # Earth Spells (Level 4, 14, 26)
    icicle_dagger, hail_storm, blizzard,     # Ice Spells (Level 4, 14, 26)
    m_gust, microburst, cyclone,             # Wind Spells (Level 4, 14, 26)
    purify, smite, moonbeam,                 # Life Spells (Level 5, 15, 27)
    curse, desecration, unholy_rend,         # Death Spells (Level 5, 15, 27)

    m_quick, m_evade, a_quick, a_evade,       # Movement Spells (Level 1, 10)
    m_defend, m_shield, a_defend, a_shield,   # Defense Spells (Level 3, 13)
    m_stren, m_power, a_stren, a_power,       # Attack Spells (Level 6, 16)
    m_aim, m_block, a_aim, a_block,           # Pierce Spells (Level 7, 17)

    r_affliction]  # Relieve Affliction (Level 5)

spellbook = {
    'player': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Solou': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Xoann': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Parsto': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    "Ran'af": {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Adorine': {
        'Healing': [pit_heal],
        'Damaging': [magic_shot],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    },

    'Chyme': {
        'Healing': [pit_heal, min_heal],
        'Damaging': [magic_shot, purify],
        'Buffs': [m_evade, m_quick],
        'Previous Spell': []
    }
}


def serialize_sb(path):
    j_spellbook = {}
    for user in spellbook:
        j_spellbook[user] = {}

        for cat in spellbook[user]:
            j_spellbook[user][cat] = []

            for spell in spellbook[user][cat]:
                spell_dict = {key: spell.__dict__[key] for key in spell.__dict__ if key != 'use_magic'}
                j_spellbook[user][cat].append(spell_dict)

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(j_spellbook, f, indent=4, separators=(', ', ': '))


def deserialize_sb(path):
    global spellbook
    norm_sb = {}

    with open(path, encoding='utf-8') as f:
        j_spellbook = json.load(f)

    for user in j_spellbook:
        norm_sb[user] = {}

        for category in j_spellbook[user]:
            norm_sb[user][category] = []

            for spell in j_spellbook[user][category]:

                if category == 'Damaging':
                    x = Damaging('', '', '', '', '', '')

                elif category == 'Healing':
                    if spell['name'] == 'Relieve Affliction':
                        x = Spell('', '', '', '')
                        x.__dict__ = spell
                        x.use_magic = relieve_affliction
                        norm_sb[user][category].append(x)

                        continue

                    x = Healing('', '', '', '', '', '')

                elif category == 'Buffs':
                    x = Buff('', '', '', '', '', '')

                elif category == 'Previous Spell':
                    continue

                x.__dict__ = spell
                norm_sb[user][category].append(x)

    spellbook = norm_sb
