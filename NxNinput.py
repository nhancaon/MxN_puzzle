import pygame
import sys
from hover import *
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 300, 160
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creating Square Puzzle")

# Set up colors and font
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,128)
font = pygame.font.SysFont("Consolas", 20)

button3 = Button("Start Game", 180, 40, (60, 100), 5)
# Set up variables for the text entry
input_text = ""
is_input_active = False

def write_square(n):
    # Update the settings.py file
    with open("settings.py", "r") as file:
        data = file.readlines()
        data[-1] = f"GAME_SIZE_X = {n}\n"
        data[-2] = f"GAME_SIZE_Y = {n}\n"

    with open("settings.py", "w") as file:
        file.writelines(data)

# Main game loop
while True:
    #set background
    bg = pygame.image.load("images/bgmain.jpg").convert()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is clicked in the text box areas
            if 150 < event.pos[0] < 270 and 35 < event.pos[1] < 65:
                is_input_active = True
            else:
                is_input_active = False
        elif event.type == pygame.KEYDOWN:
            # Check if the input is active and handle key events
            if is_input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
                    write_square(input_text)
		
    # Set the background
    SCREEN.blit(bg,(0,0))
    buttons_draw()

    # Render text
    text_N = font.render("Input N: ", True, WHITE)
    
    # Get the text rectangle
    text_rect_N = text_N.get_rect(topleft = (45, 45))
    
    # Draw the text on the screen
    SCREEN.blit(text_N, text_rect_N)

    # Draw the text entry boxes
    pygame.draw.rect(SCREEN, pygame.Color(BLUE), (150, 35, 120, 30))
    if is_input_active:
        pygame.draw.rect(SCREEN, pygame.Color(BLUE), (150, 35, 120, 30), 2)
        
    # Render and draw the entered text
    text_surface_row = font.render(input_text, True, WHITE)
    SCREEN.blit(text_surface_row, (190, 40))

    # Update the display
    pygame.display.flip()

    # Control the frame rate (optional)
    pygame.time.Clock().tick(60)