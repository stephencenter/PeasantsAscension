using System.Collections.Generic;
using System.Media;

namespace Scripts
{
    public class SoundManager
    {
        // Sword Slash -- Played when you attempt to physically attack an enemy
        public readonly SoundPlayer sword_slash = new SoundPlayer("../../../Sound FX/sword_slash.wav");

        // Magical Attack -- Played when you attempt to use a magical attack
        public readonly SoundPlayer magic_attack = new SoundPlayer("../../../Sound FX/magic_attack.wav");

        // Magic Healing -- Played when you attempt to use a magical healing spell
        public readonly SoundPlayer magic_healing = new SoundPlayer("../../../Sound FX/magic_healing.wav");

        // Enemy-hit -- Played when the enemy is hit by a player attack
        public readonly SoundPlayer enemy_hit = new SoundPlayer("../../../Sound FX/enemy_hit.wav");

        // Foot-steps -- Played when you move on the overworld
        public readonly SoundPlayer foot_steps = new SoundPlayer("../../../Sound FX/foot_steps.wav");

        // Aim Weapon -- Played when attempting to attack with a ranged weapon
        public readonly SoundPlayer aim_weapon = new SoundPlayer("../../../Sound FX/aim_weapon.wav");

        // Attack Miss -- Played when attempting to attack and then failing
        public readonly SoundPlayer attack_miss = new SoundPlayer("../../../Sound FX/attack_miss.wav");

        // Got Item -- Played when you receive an item, GP, or XP
        public readonly SoundPlayer item_pickup = new SoundPlayer("../../../Sound FX/item_pickup.wav");

        // Low Health -- Played when you have low (less than 20%) health remaining
        public readonly SoundPlayer health_low = new SoundPlayer("../../../Sound FX/health_low.wav");

        // Poison Damage -- Played when the player or enemy take poison damage
        public readonly SoundPlayer poison_damage = new SoundPlayer("../../../Sound FX/poison_damage.wav");

        // Use Buff Spell -- Played when the player or enemy use a buff spell
        public readonly SoundPlayer buff_spell = new SoundPlayer("../../../Sound FX/buff_spell.wav");

        // Ally Death -- Played when a member of your party dies
        public readonly SoundPlayer ally_death = new SoundPlayer("../../../Sound FX/ally_death.wav");

        // Enemy Death -- Played when a member of the enemy team dies
        public readonly SoundPlayer enemy_death = new SoundPlayer("../../../Sound FX/enemy_death.wav");

        // Critical Hit -- Played when someone lands a critical hit
        public readonly SoundPlayer critical_hit = new SoundPlayer("../../../Sound FX/critical_hit.wav");

        // Lockpick Break -- Played when failing to pick a lock (Stolen from Oblivion)
        public readonly SoundPlayer lockpick_break = new SoundPlayer("../../../Sound FX/lockpick_break.wav");

        // Lockpicking -- Played when attempting to pick a lock
        public readonly SoundPlayer lockpicking = new SoundPlayer("../../../Sound FX/lockpicking.wav");

        // Unlock Chest -- Played when succeeding to pick a lock
        public readonly SoundPlayer unlock_chest = new SoundPlayer("../../../Sound FX/unlock_chest.wav");

        // Debuff -- Played when the player suffers from a debuff
        public readonly SoundPlayer debuff = new SoundPlayer(@"../../../Sound FX\debuff.wav");

        // Ability cast -- Used when non-magical abilities are casted
        public readonly SoundPlayer ability_cast = new SoundPlayer("../../../Sound FX/ability_cast.wav");

        // Potion Brew -- Used when brewing potions
        public readonly SoundPlayer potion_brew = new SoundPlayer("../../../Sound FX/potion_brew.wav");

        // Eerie Sound -- No current use
        public readonly SoundPlayer eerie_sound = new SoundPlayer("../../../Sound FX/eerie_sound.wav");

        // Random encounter -- No current use
        public readonly SoundPlayer random_enc = new SoundPlayer("../../../Sound FX/random_encounter.wav");

        public readonly Dictionary<string, SoundPlayer> bard_sounds = new Dictionary<string, SoundPlayer>()
        {
            { "snare_drum", new SoundPlayer("../../../Sound FX/Bard Sounds/snare_1.wav") },
            { "violin", new SoundPlayer("../../../Sound FX/Bard Sounds/violin_1.wav") },
            { "flute", new SoundPlayer("../../../Sound FX/Bard Sounds/flute_1.wav") },
            { "trumpet", new SoundPlayer("../../../Sound FX/Bard Sounds/trumpet_1.wav") },
            { "kazoo", new SoundPlayer("../../../Sound FX/Bard Sounds/kazoo_1.wav") },
            { "bagpipes", new SoundPlayer("../../../Sound FX/Bard Sounds/bagpipes_1.wav") }
        };
    }
}
