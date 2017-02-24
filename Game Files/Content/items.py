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

from ItemClass import *
import json

# Potions -- Health
s_potion = Consumable('Weak Potion',
                      'A small potion that restores 15 HP when consumed.',
                      15, 5, heal=15)
m_potion = Consumable('Basic Potion',
                      'A regular potion that restores 45 HP when consumed.',
                      30, 10, heal=45)
l_potion = Consumable('Strong Potion',
                      'A powerful potion that restores 100 HP when consumed.',
                      60, 20, heal=100)
x_potion = Consumable('Super Potion',
                      'A super powerful potion that restores 200 HP when consumed.',
                      120, 40, heal=200)

# Potions -- Mana
s_elixir = Consumable('Basic Elixir',
                      'A generic elixir that restores 15 MP when consumed.',
                      10, 3, mana=10, ascart='Elixir')
m_elixir = Consumable('Enhanced Elixir',
                      'A more potent elixir that restores 45 MP when consumed.',
                      25, 8, mana=35, ascart='Elixir')
l_elixir = Consumable('Grand Elixir',
                      'A powerful elixir that restores 100 MP when consumed.',
                      50, 17, mana=75, ascart='Elixir')
x_elixir = Consumable('Extreme Elixir',
                      'A super powerful elixir that restores 175 MP when consumed.',
                      100, 35, mana=175, ascart='Elixir')

# Potions -- Both
s_rejuv = Consumable('Minor Rejuvenation Potion',
                     'A basic mixture that restores 15 HP and 15 MP when consumed.',
                     35, 12, heal=15, mana=15, ascart='Rejuv')

m_rejuv = Consumable('Refined Rejuvenation Potion',
                     'A higher quality mixture that restores 45 HP and 45 MP when consumed.',
                     65, 22, heal=45, mana=45, ascart='Rejuv')

l_rejuv = Consumable('Mighty Rejuvenation Potion',
                     'A super powerful mixture that restores 100 HP and 100 MP when consumed.',
                     225, 80, heal=100, mana=100, ascart='Rejuv')

# Potions - Status
silence_potion = StatusPotion('Potion of Allowing Speech',
                              "A potion designed to enable the usage of damaged vocal chords.",
                              50, 25, 'silenced', ascart='Status')
poison_potion = StatusPotion('Potion of Curing Disease',
                             'A potion designed to cure even the most deadly of illnesses.',
                             50, 25, 'poisoned', ascart='Status')
weakness_potion = StatusPotion('Potion of Regaining Strength',
                               'A potion designed to help regain lost muscle-mass and stamina.',
                               50, 25, 'weakened', ascart='Status')
blindness_potion = StatusPotion('Potion of Enabling Sight',
                                'A potion designed to help the blind regain their eyesight.',
                                50, 25, 'blinded', ascart='Status')
paralyzation_potion = StatusPotion('Potion of Inducing Motion',
                                   'A potion designed to cure minor paralysis in most of the body.',
                                   50, 25, 'paralyzed', ascart='Status')


# Fists exist to prevent bugs caused by not having any weapon equipped. Also the starting
# weapon for the Monk.
fists = Weapon('Fists',
               """Nothing beats good ol' fashioned hand-to-hand combat (No damage bonus)""",
               0, 0, 0, 'melee', 'none', 'Fists')

# Weapons -- Warrior
wdn_sht = Weapon('Wooden Shortsword',
                 'A small sword carved from an oak branch (+5% Damage)',
                 10, 5, 0.05, 'melee', 'warrior', 'Short Sword')

bnz_swd = Weapon('Bronze Sword',
                 'A light yet sturdy sword smelted from a bronze alloy (+10% Damage)',
                 50, 15, 0.1, 'melee', 'warrior', 'Sword')
en_bnz_swd = Weapon('Enhanced Bronze Sword',
                    'An enhanced version of your typical Bronze Sword (+25% Damage)',
                    100, 25, 0.25, 'melee', 'warrior', 'Sword')

stl_spr = Weapon('Steel Spear',
                 'A fair-sized spear crafted from well made steel (+40% Damage)',
                 225, 75, 0.4, 'melee', 'warrior', 'Spear')
en_stl_spr = Weapon('Enhanced Steel Spear',
                    'An enhanced version of your typical Steel Spear (+60% Damage)',
                    350, 125, 0.6, 'melee', 'warrior', 'Spear')

durs_axe = Weapon('Durasteel Battleaxe',
                  'A heavy and powerful axe made with high quality durasteel ore (+80% Damage)',
                  500, 225, 0.8, 'melee', 'warrior', 'Axe')
en_durs_axe = Weapon('Enhanced Durasteel Battleaxe',
                     'An enhanced version of your typical Durasteel Battleaxe (+100% Damage)',
                     750, 325, 1, 'melee', 'warrior', 'Axe')

# Weapons -- Assassin
stn_dag = Weapon('Stone Dagger',
                 'A crude yet effective knife carved from a light stone (+5% Damage)',
                 10, 5, 0.05, 'melee', 'assassin', 'Dagger')

ser_knf = Weapon('Serrated Knife',
                 'A durable knife made of iron, with one side made jagged (+10% Damage)',
                 50, 15, 0.1, 'melee', 'assassin', 'Dagger')
en_ser_knf = Weapon('Enhanced Serrated Knife',
                    'An enhanced version of your typical Serrated Knife (+25% Damage)',
                    100, 25, 0.25, 'melee', 'assassin', 'Dagger')

stiletto = Weapon('Stiletto',
                  'A long, cross-shaped knife perfect for "removing" your enemies (+40% Damage)',
                  225, 75, 0.4, 'melee', 'assassin', 'Stiletto')
en_stiletto = Weapon('Enhanced Stiletto',
                     'An enhanced version of your typical Stiletto (+60% Damage)',
                     350, 125, 0.6, 'melee', 'assassin', 'Stiletto')

myth_sb = Weapon('Mythril Shortblade',
                 'A knife made of a rare and powerful material (+80% Damage)',
                 500, 225, 0.8, 'melee', 'assassin', 'Short Sword')
en_myth_sb = Weapon('Enhanced Mythril Shortblade',
                    'An enhanced version of your typical Mythril Shortblade (+100% Damage)',
                    750, 325, 1, 'melee', 'assassin', 'Short Sword')

# Weapons -- Ranger
slg_sht = Weapon('Sling Shot',
                 'A weapon that could scare even the mightiest of tin-cans (+5% Damage)',
                 10, 5, 0.05, 'ranged', 'ranger', 'Sling Shot')

sht_bow = Weapon('Short Bow',
                 "A bow of great craftsmanship. It's kinda small, though (+10% Damage)",
                 50, 15, 0.10, 'ranged', 'ranger', 'Bow')
en_sht_bow = Weapon('Enhanced Short Bow',
                    " An enhanced version of your typical Short Bow (+25% Damage)",
                    100, 25, 0.25, 'ranged', 'ranger', 'Bow')

lng_bow = Weapon('Long Bow',
                 'A much more impressive bow capable of accuracy at long distances (+40% Damage)',
                 225, 75, 0.4, 'ranged', 'ranger', 'Bow')
en_lng_bow = Weapon('Enhanced Long Bow',
                    'An enhanced version of your typical Long Bow (+60% Damage)',
                    350, 125, 0.6, 'ranged', 'ranger', 'Bow')

ash_cbow = Weapon('Ashen Crossbow',
                  'A beautifully-crafted crossbow made from the wood of an ash tree. (+80% Damage)',
                  500, 225, 0.8, 'ranged', 'ranger', 'Crossbow')
en_ash_cbow = Weapon('Enhanced Ashen Crossbow',
                     'An enhanced version of your typical Ashen Crossbow (+100% Damage)',
                     750, 325, 1, 'ranged', 'ranger', 'Crossbow')

# Weapons -- Mage
# Mage weapons deal around half that of other weapons, but their magic deals 2x damage so it
# for the most part balances it out
mag_twg = Weapon('Magical Twig',
                 'A small stick with basic magical properties (+5% Damage)',
                 10, 5, 0.05, 'ranged', 'mage', 'Twig')

oak_stf = Weapon('Oak Staff',
                 'A wooden staff imbued with weak magical abilities (+10% Damage)',
                 50, 15, 0.1, 'ranged', 'mage', 'Staff')
en_oak_stf = Weapon('Enhanced Oak Staff',
                    'An enhanced version of your typical Oak Staff (+15% Damage)',
                    100, 25, 0.15, 'ranged', 'mage', 'Staff')

arc_spb = Weapon('Arcane Spellbook',
                 'An intermediate spellbook for combat purposes (+20% Damage)',
                 225, 75, 0.2, 'ranged', 'mage', 'Book')
en_arc_spb = Weapon('Enhanced Arcane Spellbook',
                    'An enhanced version of your typical Arcane Spellbook (+30% Damage)',
                    350, 125, 0.3, 'ranged', 'mage', 'Book')

rnc_stf = Weapon('Runic Staff',
                 'A powerful staff enchanted with ancient magic (+40% Damage)',
                 500, 225, 0.4, 'ranged', 'mage', 'Staff')
en_rnc_stf = Weapon('Enhanced Runic Staff',
                    'An enhanced version of your typical Runic Staff (+50% Damage)',
                    750, 325, 0.5, 'ranged', 'mage', 'Staff')

# Weapons -- Paladin
rbr_mlt = Weapon('Rubber Mallet',
                 'This can barely hammer nails, what do you expect to kill with it? (+5% Damage)',
                 10, 5, 0.05, 'melee', 'paladin', 'Hammer')

holy_mace = Weapon('Holy Mace',
                   'An well-made iron mace imbued with the power of the heavens (+10% Damage)',
                   50, 15, 0.1, 'melee', 'paladin', 'Mace')
en_holy_mace = Weapon('Enhanced Holy Mace',
                      'An enhanced version of your typical Holy Mace (+25% Damage)',
                      100, 25, 0.25, 'melee', 'paladin', 'Mace')

hmr_of_mgt = Weapon('Hammer of Might',
                    'A hammer often used by holy warriors to smash their foes (+40% Damage)',
                    225, 75, 0.4, 'melee', 'paladin', 'Hammer')
en_hmr_of_mgt = Weapon('Enhanced Hammer of Might',
                       'An enhanced version of your typical Hammer of Might (+60% Damage)',
                       350, 125, 0.6, 'melee', 'paladin', 'Hammer')

ngt_bane = Weapon("Night's Bane",  # Reference to Terraria's "Light's Bane"
                  'A hammer used by countless paladins to stamp out unholy creatures (+80% Damage)',
                  500, 225, 0.8, 'melee', 'paladin', 'Hammer')
en_ngt_bane = Weapon("Enhanced Night's Bane",
                     "An enhanced version of your typical Night's Bane (+100% Damage)",
                     750, 325, 1, 'melee', 'paladin', 'Hammer')

# Weapon -- Monk
brass_kncls = Weapon('Brass Knuckles',
                     'A brass adornment for your knuckles providing extra punching power (+10% Damage)',
                     50, 15, 0.1, 'melee', 'monk', 'Knuckles')
en_brass_kncls = Weapon('Enhanced Brass Knuckles',
                        'An enhanced version of your typical Brass Knuckles (+25% Damage)',
                        100, 25, 0.25, 'melee', 'monk', 'Knuckles')

bladed_gloves = Weapon('Bladed Gloves',
                       'Leather gloves with sturdy steel blades protruding from them (+40% Damage)',
                       225, 75, 0.4, 'melee', 'monk', 'Gloves')
en_bladed_gloves = Weapon('Enhanced Bladed Gloves',
                          'An enhanced version of your typical Bladed Gloves (+60% Damage)',
                          350, 125, 0.6, 'melee', 'monk', 'Gloves')

lead_bg = Weapon('Lead-Weighted Boxing Gloves',
                 'Weighted with 5 pounds of lead and tipped with steel blades. Probably \n\
not allowed in standard matches (+80% Damage)',
                 500, 225, 0.8, 'melee', 'monk', 'Gloves')
en_lead_bg = Weapon('Enhanced Lead Gloves',
                    'An enhanced version of your typical Lead-Weighted Boxing Gloves (+100% Damage)',
                    750, 325, 1, 'melee', 'monk', 'Gloves')

# Starting Armor (Useless)
straw_hat = Armor('Straw Hat',
                  "Other than keep the sun out of your eyes, this doesn't do much.",
                  0, 2, 0, 'head', 'none', 'Hat')
cotton_shirt = Armor('Cotton Shirt',
                     "It's barely even worth the material it's made of.",
                     0, 2, 0, 'body', 'none', 'Shirt')
sunday_trousers = Armor('Sunday Trousers',
                        "At least they look nice... Wait, isn't it Thursday?",
                        0, 2, 0, 'legs', 'none', 'Pants')

# Armor -- Warrior + Paladin -- Weak
bnz_hlm = Armor('Bronze Helmet',
                'A simple helmet crafted from bronze (+5% ARMOR)',
                25, 10, 0.05, 'head', ['warrior', 'paladin'], 'Helmet')
bnz_cst = Armor('Bronze Chestpiece',
                'Simple chest armor crafted from bronze (+10% ARMOR)',
                25, 10, 0.1, 'body', ['warrior', 'paladin'], 'Shirt')
bnz_leg = Armor('Bronze Greaves',
                'Simple leg armor crafted from bronze (+5% ARMOR)',
                25, 10, 0.05, 'legs', ['warrior', 'paladin'], 'Pants')

en_bnz_hlm = Armor('Enhanced Bronze Helmet',
                   'An enhanced version of your typical Bronze Helmet (+10% ARMOR)',
                   75, 35, 0.1, 'head', ['warrior', 'paladin'], 'Helmet')
en_bnz_cst = Armor('Enhanced Bronze Chestpiece',
                   'An enhanced version of your typical Bronze Chestpiece (+15% ARMOR)',
                   75, 35, 0.15, 'body', ['warrior', 'paladin'], 'Shirt')
en_bnz_leg = Armor('Enhanced Bronze Greaves',
                   'An enhanced version of your typical Bronze Greaves (+10% ARMOR)',
                   75, 35, 0.1, 'legs', ['warrior', 'paladin'], 'Pants')

# Armor -- Mage + Monk -- Weak
wiz_hat = Armor('Silk Hat',
                'A silk hat woven with magic thread (+3% ARMOR)',
                25, 10, 0.03, 'head', ['mage', 'monk'], 'Wizard Hat')
wiz_rob = Armor('Silk Robe',
                'A silk robe woven with magic thread (+5% ARMOR)',
                25, 10, 0.05, 'body', ['mage', 'monk'], 'Robe')
wiz_gar = Armor('Silk Garments',
                'Silk garments woven with magic thread (+3% ARMOR)',
                25, 10, 0.03, 'legs', ['mage', 'monk'], 'Robe Pants')

en_wiz_hat = Armor('Enhanced Silk Hat',
                   'An enhanced version of your typical Wizard Hat (+5% ARMOR)',
                   75, 35, 0.05, 'head', ['mage', 'monk'], 'Wizard Hat')
en_wiz_rob = Armor('Enhanced Silk Robe',
                   'An enhanced version of your typical Wizard Robe (+10% ARMOR)',
                   75, 35, 0.1, 'body', ['mage', 'monk'], 'Robe')
en_wiz_gar = Armor('Enhanced Silk Garments',
                   'An enhanced version of your typical Wizard Garments (+5% ARMOR)',
                   75, 35, 0.05, 'legs', ['mage', 'monk'], 'Robe Pants')

# Armor -- Assassin + Ranger -- Weak
lth_cap = Armor('Leather Cap',
                'A simple leather cap providing equally simple protection (+2% ARMOR)',
                25, 10, 0.02, 'head', ['assassin', 'ranger'], 'Cap')
lth_bdy = Armor('Leather Bodyarmor',
                'Simple body armor providing equally simple protection (+4% ARMOR)',
                25, 10, 0.04, 'body', ['assassin', 'ranger'], 'Shirt')
lth_leg = Armor('Leather Leggings',
                'Simple leggings providing equally simple protection (+2% ARMOR)',
                25, 10, 0.02, 'legs', ['assassin', 'ranger'], 'Pants')

en_lth_cap = Armor('Enhanced Leather Cap',
                   'An enhanced version of your typical Leather Cap (+7% ARMOR)',
                   75, 35, 0.07, 'head', ['assassin', 'ranger'], 'Cap')
en_lth_bdy = Armor('Enhanced Leather Bodyarmor',
                   'An enhanced version of your typical Leather Bodyarmor (+12% ARMOR)',
                   75, 35, 0.12, 'body', ['assassin', 'ranger'], 'Shirt')
en_lth_leg = Armor('Enhanced Leather Leggings',
                   'An enhanced version of your typical Leather Leggings (+7% ARMOR)',
                   75, 35, 0.07, 'legs', ['assassin', 'ranger'], 'Pants')

# Armor -- Warrior + Paladin -- Mid
stl_hlm = Armor('Steel Helmet',
                'A decent helmet created from a solid metal (+15% ARMOR)',
                200, 100, 0.15, 'head', ['warrior', 'paladin'], 'Helmet')
stl_cst = Armor('Steel Chestpiece',
                'Decent body armor made from a solid metal (+20% ARMOR)',
                200, 100, 0.20, 'body', ['warrior', 'paladin'], 'Shirt')
stl_leg = Armor('Steel Greaves',
                'Decent greaves made from a solid metal (+15% ARMOR)',
                200, 100, 0.15, 'legs', ['warrior', 'paladin'], 'Pants')

en_stl_hlm = Armor('Enhanced Steel Helmet',
                   'An enhanced version of your typical Steel Helmet (+20% ARMOR)',
                   325, 150, 0.20, 'head', ['warrior', 'paladin'], 'Helmet')
en_stl_cst = Armor('Enhanced Steel Chestpiece',
                   'An enhanced version of your typical Steel Chestpiece (+25% ARMOR)',
                   325, 150, 0.25, 'body', ['warrior', 'paladin'], 'Shirt')
en_stl_leg = Armor('Enhanced Steel Leggings',
                   'An enhanced version of your typical Steel Greaves (+20% ARMOR)',
                   325, 150, 0.20, 'legs', ['warrior', 'paladin'], 'Pants')


# Armor -- Mage + Monk -- Mid
myst_hat = Armor('Mystical Hood',
                 'A mysterious hood with strange symbols sewn into it (+8% ARMOR)',
                 200, 100, 0.08, 'head', ['mage', 'monk'], 'Wizard Hat')
myst_rob = Armor('Mystical Robe',
                 'A mysterious robe with strange symbols sewn into it (+12% ARMOR)',
                 200, 100, 0.12, 'body', ['mage', 'monk'], 'Robe')
myst_gar = Armor('Mystical Garments',
                 'Mysterious garments with strange symbols sewn into it (+8% ARMOR)',
                 200, 100, 0.08, 'legs', ['mage', 'monk'], 'Robe Pants')

en_myst_hat = Armor('Enhanced Mystical Hood',
                    'An enhanced version of your typical Mystical Hood (+15% ARMOR)',
                    325, 150, 0.15, 'head', ['mage', 'monk'], 'Wizard Hat')
en_myst_rob = Armor('Enhanced Mystical Robe',
                    'An enhanced version of your typical Mystical Robe (+20% ARMOR)',
                    325, 150, 0.2, 'body', ['mage', 'monk'], 'Robe')
en_myst_gar = Armor('Enhanced Mystical Garments',
                    'An enhanced version of your typical Mystical Garments (+15% ARMOR)',
                    325, 150, 0.15, 'legs', ['mage', 'monk'], 'Robe Pants')

# Armor -- Assassin + Ranger -- Mid
std_cwl = Armor('Studded Cowl',
                'A soft leather cap studded with steel pieces (+12% ARMOR)',
                200, 100, 0.12, 'head', ['assassin', 'ranger'], 'Cap')
std_bdy = Armor('Studded Body-armor',
                'Soft leather body armor studded with steel pieces (+18% ARMOR)',
                200, 100, 0.18, 'body', ['assassin', 'ranger'], 'Shirt')
std_leg = Armor('Studded Leggings',
                'Soft leather leggings studded with steel pieces (+12% ARMOR)',
                200, 100, 0.12, 'legs', ['assassin', 'ranger'], 'Pants')

en_std_cwl = Armor('Enhanced Studded Cowl',
                   'An enhanced version of your typical Studded Hood (+17% ARMOR)',
                   325, 150, 0.17, 'head', ['assassin', 'ranger'], 'Cap')
en_std_bdy = Armor('Enhanced Studded Body-armor',
                   'An enhanced version of your typical Studded Bodyarmor (+22% ARMOR)',
                   325, 150, 0.22, 'body', ['assassin', 'ranger'], 'Shirt')
en_std_leg = Armor('Enhanced Studded Leggings',
                   'An enhanced version of your typical Studded Leggings (+17% ARMOR)',
                   325, 150, 0.17, 'legs', ['assassin', 'ranger'], 'Pants')


# Armor -- Warrior + Paladin -- Pow
# 90% ARMOR
ori_hlm = Armor('Orichalcum Helmet',
                'A strong helmet smelted from rare mountain copper  (+25% ARMOR)',
                475, 225, 0.25, 'head', ['warrior', 'paladin'], 'Helmet')
ori_cst = Armor('Orichalcum Chestplate',
                'Strong chest armor smelted from rare mountain copper  (+35% ARMOR)',
                475, 225, 0.35, 'body', ['warrior', 'paladin'], 'Shirt')
ori_leg = Armor('Orichalcum Greaves',
                'Strong leg armor smelted from rare mountain copper (+25% ARMOR)',
                475, 225, 0.25, 'legs', ['warrior', 'paladin'], 'Pants')

# Armor -- Mage + Monk -- Pow
# 65% ARMOR
elem_hat = Armor('Armored Cloth Hat',
                 'A silk hat lined with chainmail in important parts (+20% ARMOR)',
                 475, 225, 0.20, 'head', ['mage', 'monk'], 'Wizard Hat')
elem_rob = Armor('Armored Cloth Robe',
                 'A silk robe lined with chainmail in important parts (+25% ARMOR)',
                 475, 225, 0.25, 'body', ['mage', 'monk'], 'Robe')
elem_gar = Armor('Armored Cloth Garments',
                 'Silk garments lined with chainmail in important parts (+20% ARMOR)',
                 475, 225, 0.20, 'legs', ['mage', 'monk'], 'Robe Pants')

# Armor -- Assassin + Ranger -- Pow
# 80% ARMOR
drg_cwl = Armor('Dragonhide Cowl',
                'A tough hood crafted from high-quality dragonskin (+25% ARMOR)',
                475, 225, 0.25, 'head', ['assassin', 'ranger'], 'Cap')
drg_bdy = Armor('Dragonhide Bodyarmor',
                'Tough bodyarmor crafted from high-quality dragonskin (+30% ARMOR)',
                475, 225, 0.3, 'body', ['assassin', 'ranger'], 'Shirt')
drg_leg = Armor('Dragonhide Leggings',
                'Tough leggings crafted from high-quality dragonskin (+25% ARMOR)',
                475, 225, 0.25, 'legs', ['assassin', 'ranger'], 'Pants')

# Accessories
# -- Elemental Accessories
water_amulet = ElementAccessory('Aquatic Amulet', 'An amulet that imbues its wearer with the power of WATER',
                                375, 175, 'Water')
fire_amulet = ElementAccessory('Infernal Amulet', 'An amulet that imbues its wearer with the power of FIRE',
                               375, 175, 'Fire')
earth_amulet = ElementAccessory('Ground Amulet', 'An amulet that imbues its wearer with the power of EARTH',
                                375, 175, 'Earth')
electric_amulet = ElementAccessory('Galvanic Amulet', 'An amulet that imbues its wearer with the power of ELECTRICITY',
                                   375, 175, 'Electric')
wind_amulet = ElementAccessory('Tempestuous Amulet', 'An amulet that imbues its wearer with the power of WIND',
                               375, 175, 'Wind')
grass_amulet = ElementAccessory('Verdant Amulet', 'An amulet that imbues its wearer with the power of GRASS',
                                375, 175, 'Grass')
ice_amulet = ElementAccessory('Glacial Amulet', 'An amulet that imbues its wearer with the power of ICE',
                              375, 175, 'Ice')
light_amulet = ElementAccessory('Divine Amulet', 'An amulet that imbues its wearer with the power of LIGHT',
                                375, 175, 'Light')
dark_amulet = ElementAccessory('Umbral Amulet', 'An amulet that imbues its wearer with the power of DARKNESS',
                               375, 175, 'Dark')

# Quest items
message_joseph = Misc('Message from Joseph', 'A neatly written message addressed to Philliard.',
                      0, 0, cat='q_items', imp=True)

message_philliard = Misc('Message from Philliard', 'A neatly written message addressed to Joseph.',
                         0, 0, cat='q_items', imp=True)

iSound = Misc('iSound', "You can't even begin to imagine how one would go about using this.",
              250, 75, cat='q_items', imp=False)


# Gems & Valuables
pearl_gem = Valuable('Pearl', 'A valuable pearl. This could probably be sold for quite a bit.',
                     0, 175)

ruby_gem = Valuable('Ruby', 'A valuable ruby. This could be sold for quite a bit.',
                    0, 175)

sapphire_gem = Valuable('Sapphire', 'A valuable sapphire. This could probably be sold for quite a bit.',
                        0, 175)

emerald_gem = Valuable('Emerald', 'A valuable emerald. This could probably be sold for quite a bit.',
                       0, 175)

citrine_gem = Valuable('Citrine', 'A valuable citrine. This could probably be sold for quite a bit.',
                       0, 175)

jade_gem = Valuable('Jade', 'A valuable jade. This could probably be sold for quite a bit.',
                    0, 175)

opal_gem = Valuable('Opal', 'A valuable opal. This could probably be sold for quite a bit.',
                    0, 175)

onyx_gem = Valuable('Onyx', 'A valuable onyx. This could probably be sold for quite a bit.',
                    0, 175)

diamond_gem = Valuable('Diamond', 'A valuable diamond. This could probably be sold for quite a bit.',
                                  0, 175)

amethyst_gem = Valuable('Amethyst', 'A valuable amethyst. This could probably be sold for quite a bit.',
                                    0, 175)

topaz_gem = Valuable('Topaz', 'A valuable topaz. This could probably be sold for quite a bit.',
                              0, 175)

garnet_gem = Valuable('Garnet', 'A valuable garnet. This could probably be sold for quite a bit.',
                                0, 175)

quartz_gem = Valuable('Quartz', 'A valuable quartz. This could probably be sold for quite a bit.',
                                0, 175)

zircon_gem = Valuable('Zircon', 'A valuable zircon. This could probably be sold for quite a bit.',
                                0, 175)

agate_gem = Valuable('Agate', 'A valuable agate. This could probably be sold for quite a bit.',
                              0, 175)

aquamarine_gem = Valuable('Aquamarine', 'A valuable aquamarine. This could probably be sold for quite a bit.',
                          0, 175)

valuable_list = [pearl_gem, ruby_gem, sapphire_gem, emerald_gem, citrine_gem, jade_gem, opal_gem, onyx_gem, diamond_gem,
                 amethyst_gem, topaz_gem, garnet_gem, quartz_gem, zircon_gem, agate_gem, aquamarine_gem]

# Tools
magic_compass = MagicCompass('Magical Compass', 'A compass capable of detecting nearby towns.', 0, 0, imp=True)
divining_rod = DiviningRod('Divining Rod', 'A magical stick capable of detecting nearby ores and gems.', 300, 150)
shovel = Shovel('Shovel', 'A simple shovel used to excavate for hidden gems and minerals.', 200, 100)
map_of_fast_travel = TownTeleporter('Map of Fast Travel', 'Allows traveling to previously visited towns.', 2000, 100)

# Tools -- Lockpicks
wood_lckpck = LockpickKit('Wooden Lockpick Kit',
                          'A wooden lockpick kit with a 30% chance to open chests.', 30, 15, 30)
copper_lckpck = LockpickKit('Copper Lockpick Kit',
                            'A copper lockpick kit with a 45% chance to open chests.', 200, 100, 45)
iron_lckpck = LockpickKit('Iron Lockpick Kit',
                          'An iron lockpick kit with a 60% chance to open chests.', 300, 150, 60)
steel_lckpck = LockpickKit('Steel Lockpick Kit',
                           'A steel lockpick kit with a 75% chance to open chests.', 500, 250, 75)
mythril_lckpck = LockpickKit('Mythril Lockpick Kit',
                             'A mythril lockpick kit with a 90% chance to open chests.', 750, 375, 90)

# Monster Drops
shell_fragment = Misc('Shell Fragment', "A broken fragment of a once-beautiful sea-creature's shell [JUNK]", 0, 5)
crab_claw = Misc('Crab Claw', 'A reddish claw from a giant crab [JUNK]', 0, 5)
fairy_dust = Misc('Fairy Dust', 'Dust from a fairy. It has strange, magical properties [JUNK]', 0, 5)
serpent_scale = Misc('Serpent Scale', 'A rough scale from an unknown reptile [JUNK]', 0, 5)
ink_sack = Misc('Ink Sack', 'A small pouch full of an inky substance [JUNK]', 0, 5)
bone_bag = Misc('Bag of Bones', 'A bag full of various bones from a now deceased creature [JUNK]', 0, 5)
monster_skull = Misc('Monster Skull', 'A broken skull from a strange creature [JUNK]', 0, 5)
living_bark = Misc('Living Bark', 'This bark has a fleshy texture to it [JUNK]', 0, 5)
ripped_cloth = Misc('Ripped Cloth', 'A thick, torn cloth made out of an unknown fabric [JUNK]', 0, 5)
beetle_shell = Misc('Beetle Shell', 'A bluish shell from a large beetle [JUNK]', 0, 5)
wing_piece = Misc('Wing Piece', 'A piece of wing from a flying creature [JUNK]', 0, 5)
monster_fang = Misc('Monster Fang', 'The sharp fang of a frightening creature [JUNK]', 0, 5)
animal_fur = Misc('Animal Fur', 'A wet clump of fur from a strange animal [JUNK]', 0, 5)
golem_rock = Misc('Golem Rock', 'A small rock that seems to glow slightly [JUNK]', 0, 5)
burnt_ash = Misc('Burnt Ash', 'The ashy remains of a once-living creature [JUNK]', 0, 5)
antennae = Misc('Gooey Antennae', 'A pair of antennae from a massive, slimy insect [JUNK]', 0, 5)
ectoplasm = Misc('Ectoplasm', 'The gooey remains from a terrifying apparition [JUNK]', 0, 5)
chain_link = Misc('Chain links', 'A couple joined links of chain made from steel [JUNK]', 0, 5)
unicorn_horn = Misc('Unicorn Horn', 'A tough and shiny horn from a mythical creature [JUNK]', 0, 5)
demonic_essence = Misc('Demonic Essence', 'A strange orb that exudes a terrifying aura [JUNK]', 0, 5)
angelic_essence = Misc('Angelic Essence', 'A strange orb that radiates an incredible aura [JUNK]', 0, 5)
eye_balls = Misc('Eyeballs', 'The visual receptors of some disgusting creature [JUNK]', 0, 5)
mysterious_runes = Misc('Mysterious Runestone', 'Strange stones with even stranger symbols on it [JUNK]', 0, 5)
rodent_tail = Misc('Rodent Tail', 'The detached tail of a hideous rodent [JUNK]', 0, 5)
serpent_tongue = Misc('Serpent Tongue', 'A dried-up tongue from a slithery serpent [JUNK]', 0, 5)
feathers = Misc('Feathers', 'A veiny feather from an unknown avian creature [JUNK]', 0, 5)
broken_crystal = Misc('Broken Crystal', 'A chunk of crystal too powdery to be of any value [JUNK]', 0, 5)
slime_vial = Misc('Vial of Slime', 'A small glass vial filled with gooey slime [JUNK]', 0, 5)
blood_vial = Misc('Vial of Blood', 'A small glass vial filled with the blood of an evil creature [JUNK]', 0, 5)
water_vial = Misc('Vial of Water', 'A small glass vial filled with enchanted water [JUNK]', 0, 5)

# Easter egg for my friend
calculus_homework = Misc('Calculus Homework', 'A load of random symbols and gibberish [FUNKY]', 0, 25)
graph_paper = Misc('Graph Paper', 'Useful paper for graphing points and lines [FUNKY]', 0, 25)
ruler = Misc('Ruler', 'A piece of wood with lines on it. Neat! [FUNKY]', 0, 25)
protractor = Misc('Protractor and Compass', 'Instruments used to make shapes and angles [FUNKY]', 0, 25)
textbook = Misc('AtW Textbook', 'More like Algebra that sucks amiright? [FUNKY)', 0, 25)

# Each monster can drop two different items, with the exception of the Calculator which is an easter egg monster
monster_drop_list = {'Shell Mimic': [shell_fragment, water_vial],
                     'Giant Crab': [crab_claw, shell_fragment],
                     'Naiad': [fairy_dust, water_vial],
                     'Squid': [ink_sack, slime_vial],
                     'Bog Slime': [slime_vial, water_vial],
                     'Moss Ogre': [bone_bag, ripped_cloth],
                     'Sludge Rat': [monster_skull, rodent_tail],
                     'Spriggan': [living_bark, fairy_dust],
                     'Vine Lizard': [serpent_scale, living_bark],
                     'Goblin Archer': [ripped_cloth, eye_balls],
                     'Beetle': [beetle_shell, antennae],
                     'Corrupt Thaumaturge': [ripped_cloth, mysterious_runes],
                     'Minor Yeti': [animal_fur, monster_fang],
                     'Fire Ant': [antennae, burnt_ash],
                     'Necromancer': [ripped_cloth, demonic_essence],
                     'Wraith': [ectoplasm, demonic_essence],
                     'Ghoul': [ectoplasm, demonic_essence],
                     "Will-o'-the-wisp": [fairy_dust, burnt_ash],
                     'Imp': [wing_piece, fairy_dust],
                     'Bat': [monster_fang, wing_piece],
                     'Skeleton': [bone_bag, demonic_essence],
                     'Undead Archer': [chain_link, bone_bag],
                     'Frost Bat': [monster_fang, wing_piece],
                     'Alicorn': [unicorn_horn, angelic_essence],
                     'Mummy': [burnt_ash, ripped_cloth],
                     'Giant Worm': [monster_fang, slime_vial],
                     'Griffin': [animal_fur, wing_piece],
                     'Anubis': [animal_fur, burnt_ash],
                     'Sea Serpent': [serpent_scale, serpent_tongue],
                     'Flying Serpent': [serpent_scale, serpent_tongue],
                     'Harpy': [wing_piece, feathers],
                     'Troll': [monster_skull, eye_balls],
                     'Sand Golem': [golem_rock, broken_crystal],
                     'Naga': [serpent_scale, eye_balls],
                     'Rock Giant': [golem_rock, broken_crystal],
                     'Ice Soldier': [chain_link, blood_vial],
                     'Arctic Wolf': [animal_fur, monster_fang],
                     'Oread': [fairy_dust, eye_balls],
                     'Tengu': [wing_piece, feathers],
                     'Zombie': [monster_skull, blood_vial],
                     'Calculator': [calculus_homework, graph_paper, protractor, ruler, textbook]
                     }

# "gs_stock" is a list of all items in the General Store's stock. The GS's level determines
# what items are in its stock via: [category[self.gs_level - 1] for category in gs_stock]

gs_stock = {'Potions': [[s_potion, s_potion, m_potion,
                         l_potion, l_potion, x_potion],  # Health Potions

            [s_elixir, s_elixir, m_elixir,
             l_elixir, l_elixir, x_elixir],  # Mana Potions

            [s_rejuv, s_rejuv, m_rejuv,
             m_rejuv, l_rejuv, l_rejuv],  # HP + MP Potions

            [poison_potion, poison_potion, poison_potion,
             poison_potion, poison_potion, poison_potion],  # Poison Potion

            [silence_potion, silence_potion, silence_potion,
             silence_potion, silence_potion, silence_potion],  # Silence Potion

            [blindness_potion, blindness_potion, blindness_potion,
             blindness_potion, blindness_potion, blindness_potion],  # Blindness Potion

            [paralyzation_potion, paralyzation_potion, paralyzation_potion,
             paralyzation_potion, paralyzation_potion, paralyzation_potion],  # Para. Potion

            [weakness_potion, weakness_potion, weakness_potion,
             weakness_potion, weakness_potion, weakness_potion]],  # Weakness Potion

            'Weapons': [[bnz_swd, en_bnz_swd, stl_spr,
                         en_stl_spr, durs_axe, en_durs_axe],  # Warrior Weapons

                        [oak_stf, en_oak_stf, arc_spb,
                         en_arc_spb, rnc_stf, en_rnc_stf],  # Mage Weapons

                        [ser_knf, en_ser_knf, stiletto,
                         en_stiletto, myth_sb, en_myth_sb],  # Assassin Weapons

                        [sht_bow, en_sht_bow, lng_bow,
                         en_lng_bow, ash_cbow, en_ash_cbow],  # Ranger Weapons

                        [holy_mace, en_holy_mace, hmr_of_mgt,
                         en_hmr_of_mgt, ngt_bane, en_ngt_bane],  # Paladin Weapons

                        [brass_kncls, en_brass_kncls, bladed_gloves,
                         en_bladed_gloves, lead_bg, en_lead_bg]],  # Monk Weapons

            'Armor': [[bnz_hlm, en_bnz_hlm, stl_hlm,
                       en_stl_hlm, ori_hlm, ori_hlm],  # Warrior Armor -- Head

                      [bnz_cst, en_bnz_cst, stl_cst,
                       en_stl_cst, ori_cst, ori_cst],  # Warrior Armor -- Body

                      [bnz_leg, en_bnz_leg, stl_leg,
                       en_stl_leg, ori_leg, ori_leg],  # Warrior Armor -- Legs

                      [wiz_hat, en_wiz_hat, myst_hat,
                       en_myst_hat, elem_hat, elem_hat],  # Mage Armor -- Head

                      [wiz_rob, en_wiz_rob, myst_rob,
                       en_myst_rob, elem_rob, elem_rob],  # Mage Armor -- Body

                      [wiz_gar, en_wiz_gar, myst_gar,
                       en_myst_gar, elem_gar, elem_gar],  # Mage Armor -- Legs

                      [lth_cap, en_lth_cap, std_cwl,
                       en_std_cwl, drg_cwl, drg_cwl],  # Assassin + Ranged Armor -- Head

                      [lth_bdy, en_lth_bdy, std_bdy,
                       en_std_bdy, drg_bdy, drg_bdy],  # Assassin + Ranged Armor -- Body

                      [lth_leg, en_lth_leg, std_leg,
                       en_std_leg, drg_leg]],  # Assassin + Ranged Armor -- Legs

            'Accessories': [[water_amulet, water_amulet, water_amulet,
                             water_amulet, water_amulet, water_amulet],

                            [fire_amulet, fire_amulet, fire_amulet,
                             fire_amulet, fire_amulet, fire_amulet],

                            [earth_amulet, earth_amulet, earth_amulet,
                             earth_amulet, earth_amulet, earth_amulet],

                            [electric_amulet, electric_amulet, electric_amulet,
                             electric_amulet, electric_amulet, electric_amulet],

                            [wind_amulet, wind_amulet, wind_amulet,
                             wind_amulet, wind_amulet, wind_amulet],

                            [grass_amulet, grass_amulet, grass_amulet,
                             grass_amulet, grass_amulet, grass_amulet],

                            [ice_amulet, ice_amulet, ice_amulet,
                             ice_amulet, ice_amulet, ice_amulet],

                            [light_amulet, light_amulet, light_amulet,
                             light_amulet, light_amulet, light_amulet],

                            [dark_amulet, dark_amulet, dark_amulet,
                             dark_amulet, dark_amulet, dark_amulet]],

            'Tools': [[divining_rod, divining_rod, divining_rod,
                       divining_rod, divining_rod, divining_rod],

                      [shovel, shovel, shovel,
                       shovel, shovel, shovel],

                      [map_of_fast_travel, map_of_fast_travel, map_of_fast_travel,
                       map_of_fast_travel, map_of_fast_travel, map_of_fast_travel],

                      [wood_lckpck, copper_lckpck, iron_lckpck, steel_lckpck,
                       mythril_lckpck, mythril_lckpck]]}


def serialize_gems(path):
    with open(path, mode='w') as j:
        json.dump([gem.name for gem in valuable_list if gem.acquired],
                  j, indent=4, separators=(', ', ': '))


def deserialize_gems(path):
    global valuable_list

    with open(path) as j:
        gems = json.load(j)

    for name in gems:
        for gem in valuable_list:
            if gem.name == name:
                gem.acquired = True
