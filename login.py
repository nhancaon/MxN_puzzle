import pygame, sys
import math
import os
from hover import *

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Login Interface")

#load image
bg = pygame.image.load("images/background.png").convert()
bg_width = bg.get_width()

#define game variables
scroll = 0
tiles = math.ceil(SCREEN_WIDTH  / bg_width) + 1

button1 = Button('Play',200,40,(SCREEN_WIDTH / 2 - 100,200),5)
button2 = Button('Guide',200,40,(SCREEN_WIDTH / 2 - 100,250),5)
button3 = Button('Exit',200,40,(SCREEN_WIDTH / 2 - 100,300),5)

#center screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

#game loop
run = True
while run:
    #draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    #scroll background
    scroll -= 5

    #reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    buttons_draw()

    pygame.display.update()
    clock.tick(FPS)
