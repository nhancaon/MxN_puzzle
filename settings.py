import pygame
# COLORS (r, g, b)
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGREY = (165, 253, 86)
LIGHTGREY =  (255,255,255)
BGCOLOUR = ( (DARKGREY[0] + 0) // 2,    # Average the red component
    (DARKGREY[1] + 0) // 2,    # Average the green component
    (DARKGREY[2] + 128) // 2  # Average the blue component with dark blue
)

# game settings
WIDTH = 1200
HEIGHT = 800
FPS = 60
title = "Sliding Puzzle Game"
TILESIZE = 128
GAME_SIZE_X = 3
GAME_SIZE_Y = 2
