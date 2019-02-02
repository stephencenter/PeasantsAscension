using System;
using System.Collections.Generic;
using System.Media;
using System.Windows.Media;

namespace Scripts
{
    public static class SoundManager
    {
        // =========================== //
        //        SOUND EFFECTS        //
        // =========================== //
        // Sword Slash -- Played when you attempt to physically attack an enemy
        public static readonly MediaWrapper sword_slash = new MediaWrapper("Sound FX/sword_slash.wav");

        // Magical Attack -- Played when you attempt to use a magical attack
        public static readonly MediaWrapper magic_attack = new MediaWrapper("Sound FX/magic_attack.wav");

        // Magic Healing -- Played when you attempt to use a magical healing spell
        public static readonly MediaWrapper magic_healing = new MediaWrapper("Sound FX/magic_healing.wav");

        // Enemy-hit -- Played when the enemy is hit by a player attack
        public static readonly MediaWrapper enemy_hit = new MediaWrapper("Sound FX/enemy_hit.wav");

        // Foot-steps -- Played when you move on the overworld
        public static readonly MediaWrapper foot_steps = new MediaWrapper("Sound FX/foot_steps.wav");

        // Aim Weapon -- Played when attempting to attack with a ranged weapon
        public static readonly MediaWrapper aim_weapon = new MediaWrapper("Sound FX/aim_weapon.wav");

        // Attack Miss -- Played when attempting to attack and then failing
        public static readonly MediaWrapper attack_miss = new MediaWrapper("Sound FX/attack_miss.wav");

        // Got Item -- Played when you receive an item, GP, or XP
        public static readonly MediaWrapper item_pickup = new MediaWrapper("Sound FX/item_pickup.wav");

        // Low Health -- Played when you have low (less than 20%) health remaining
        public static readonly MediaWrapper health_low = new MediaWrapper("Sound FX/health_low.wav");

        // Poison Damage -- Played when the player or enemy take poison damage
        public static readonly MediaWrapper poison_damage = new MediaWrapper("Sound FX/poison_damage.wav");

        // Use Buff Spell -- Played when the player or enemy use a buff spell
        public static readonly MediaWrapper buff_spell = new MediaWrapper("Sound FX/buff_spell.wav");

        // Ally Death -- Played when a member of your party dies
        public static readonly MediaWrapper ally_death = new MediaWrapper("Sound FX/ally_death.wav");

        // Enemy Death -- Played when a member of the enemy team dies
        public static readonly MediaWrapper enemy_death = new MediaWrapper("Sound FX/enemy_death.wav");

        // Critical Hit -- Played when someone lands a critical hit
        public static readonly MediaWrapper critical_hit = new MediaWrapper("Sound FX/critical_hit.wav");

        // Lockpick Break -- Played when failing to pick a lock
        public static readonly MediaWrapper lockpick_break = new MediaWrapper("Sound FX/lockpick_break.wav");

        // Lockpicking -- Played when attempting to pick a lock
        public static readonly MediaWrapper lockpicking = new MediaWrapper("Sound FX/lockpicking.wav");

        // Unlock Chest -- Played when succeeding to pick a lock
        public static readonly MediaWrapper unlock_chest = new MediaWrapper("Sound FX/unlock_chest.wav");

        // Debuff -- Played when the player suffers from a debuff
        public static readonly MediaWrapper debuff = new MediaWrapper("Sound FX/debuff.wav");

        // Ability cast -- Used when non-magical abilities are casted
        public static readonly MediaWrapper ability_cast = new MediaWrapper("Sound FX/ability_cast.wav");

        // Potion Brew -- Used when brewing potions
        public static readonly MediaWrapper potion_brew = new MediaWrapper("Sound FX/potion_brew.wav");

        // Eerie Sound -- No current use
        public static readonly MediaWrapper eerie_sound = new MediaWrapper("Sound FX/eerie_sound.wav");

        // Random encounter -- No current use
        public static readonly MediaWrapper random_enc = new MediaWrapper("Sound FX/random_encounter.wav");

        public static readonly Dictionary<string, MediaWrapper> bard_sounds = new Dictionary<string, MediaWrapper>()
        {
            { "snare_drum", new MediaWrapper("Sound FX/Bard Sounds/snare_1.wav") },
            { "violin", new MediaWrapper("Sound FX/Bard Sounds/violin_1.wav") },
            { "flute", new MediaWrapper("Sound FX/Bard Sounds/flute_1.wav") },
            { "trumpet", new MediaWrapper("Sound FX/Bard Sounds/trumpet_1.wav") },
            { "kazoo", new MediaWrapper("Sound FX/Bard Sounds/kazoo_1.wav") },
            { "bagpipes", new MediaWrapper("Sound FX/Bard Sounds/bagpipes_1.wav") }
        };

        // =========================== //
        //            MUSIC            //
        // =========================== //

        // Music that plays when you level up
        public static readonly SoundPlayer levelup_music = new SoundPlayer("Music/Adventures in Pixels.wav");

        // Music that plays inside a castle
        public static readonly SoundPlayer castle_music = new SoundPlayer("Music/Castle.wav");

        // Music that plays inside a town
        public static readonly SoundPlayer town_music = new SoundPlayer("Music/Chickens (going peck peck peck).wav");

        // Music that plays during the credits
        public static readonly SoundPlayer credits_music = new SoundPlayer("Music/Credits Music for an 8-Bit RPG.wav");

        // Music that plays inside a dungeon
        public static readonly SoundPlayer dungeon_music = new SoundPlayer("Music/Eight_Bit_Dungeon_Monster_Stomp.wav");

        // Music that plays while talking to NPCs
        public static readonly SoundPlayer npc_music = new SoundPlayer("Music/Mayhem in the Village.wav");

        // Music that plays in mountainous areas
        public static readonly SoundPlayer mountain_music = new SoundPlayer("Music/Mountain.wav");

        // Music that plays when your party loses a battle
        public static readonly SoundPlayer gameover_music = new SoundPlayer("Music/Power-Up.wav");

        // Music that plays when your party wins a battle
        public static readonly SoundPlayer victory_music = new SoundPlayer("Music/Python_RM.wav");

        // Music that plays during a normal monster battle
        public static readonly SoundPlayer battle_music = new SoundPlayer("Music/Ruari 8-bit Battle.wav");

        // Music that plays in haunted areas
        public static readonly SoundPlayer haunted_music = new SoundPlayer("Music/song17_02.wav");

        // Music that plays when sneaking inside a house
        public static readonly SoundPlayer sneaking_music = new SoundPlayer("Music/song21_02.wav");

        // Music that plays during a boss battle
        public static readonly SoundPlayer boss_music = new SoundPlayer("Music/Terrible Tarantuloid.wav");

        // Music that plays in forested areas
        public static readonly SoundPlayer forest_music = new SoundPlayer("Music/Through the Forest.wav");

        // Music that plays on the title screen
        public static readonly SoundPlayer title_music = new SoundPlayer("Music/Title Screen.wav");

        public static void PlayCellMusic()
        {
            // Plays the music from the current cell
            TileManager.FindCellWithTileID(CInfo.CurrentTile).Music.PlayLooping();
        }
    }

    public class MediaWrapper : MediaPlayer
    {         
        public void SmartPlay()
        {
            if (Position > TimeSpan.Zero)
            {
                Position = TimeSpan.Zero;
            }

            Play();
        }

        // Using this class, I can assign the MediaPlayer a URI inside the constructor
        public MediaWrapper(string uri) : base()
        {
            Open(new Uri(uri, UriKind.Relative));
        }
    }
}
