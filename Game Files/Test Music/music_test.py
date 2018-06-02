import pygame
import threading
import random

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

songs = ['1.ogg', '2.ogg', '3.ogg']
song_num = 0
SONG_END = pygame.USEREVENT + 1


def playlist():
    for song in songs:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        music_sound = pygame.mixer.Sound(song)

        while 0 <= (pygame.mixer.music.get_pos()/1000)/music_sound.get_length() < 1:
            pass


music_thread = threading.Thread(target=playlist)
music_thread.start()

input("Yo!")
input("Woah!")
