# Set color based on RGB
BLACK = (0,0,0)
WHITE = (255,255,255)
DARK_GREY = (165, 253, 86)
LIGHTGREY = (255,255,255)
BG_COLOR = ((DARK_GREY[0] + 0) // 2,    # Average the red component
            (DARK_GREY[1] + 0) // 2,    # Average the green component
            (DARK_GREY[2] + 128) // 2  # Average the blue component with dark blue
)

# Game Settings
title = "MxN Puzzle Game"
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 128
GAME_SIZE_Y = 3
GAME_SIZE_X = 3
