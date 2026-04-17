import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Music Player")
tracks=["music\\track1.mp3", "music\\track2.mp3", "music\\track3.mp3"]
current_track=0
running = True
clock=pygame.time.Clock()
def play_music():
    pygame.mixer.music.load(tracks[current_track])
    pygame.mixer.music.play()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                play_music()
            elif event.key == K_s:
                pygame.mixer.music.stop()
            elif event.key == K_n:
                current_track = (current_track + 1) % len(tracks)
                play_music()
            elif event.key == K_b:
                current_track = (current_track - 1) % len(tracks)
                play_music()
            elif event.key == K_q:
                running = False
    clock.tick(20)
pygame.quit()