import pygame
import sys
import os
from hover import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 300, 160
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,128)
pygame.display.set_caption("Creating Rectangle Puzzle")
font = pygame.font.SysFont("Consolas", 20)

button3 = Button("Start Game",180,40,(60, 110),5)

# Set up variables for the text entry
input_text_row = ""
input_text_col = ""
is_input_active_row = False
is_input_active_col = False

def write_row(row):
    # Update the settings.py file
    with open("settings.py", "r") as file:
        data = file.readlines()
        data[-2] = f"GAME_SIZE_Y = {row}\n"

    with open("settings.py", "w") as file:
        file.writelines(data)

def write_col(col):
    # Update the settings.py file
    with open("settings.py", "r") as file:
        data = file.readlines()
        data[-1] = f"GAME_SIZE_X = {col}\n"

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
            if 190 < event.pos[0] < 290 and 15 < event.pos[1] < 45:
                is_input_active_row = True
                is_input_active_col = False
            elif 190 < event.pos[0] < 290 and 65 < event.pos[1] < 95:
                is_input_active_row = False
                is_input_active_col = True
            else:
                is_input_active_row = False
                is_input_active_col = False
        elif event.type == pygame.KEYDOWN:
            # Check if the input is active and handle key events
            if is_input_active_row:
                if event.key == pygame.K_BACKSPACE:
                    input_text_row = input_text_row[:-1]
                else:
                    input_text_row += event.unicode
                    write_row(input_text_row)

            elif is_input_active_col:
                if event.key == pygame.K_BACKSPACE:
                    input_text_col = input_text_col[:-1]
                else:
                    input_text_col += event.unicode
                    write_col(input_text_col)
                    
    # Set the background
    SCREEN.blit(bg,(0,0))
    buttons_draw()

    # Render text
    text1 = font.render("Input row(s): ", True, WHITE)
    text2 = font.render("Input col(s): ", True, WHITE)
    
    # Get the text rectangle
    text_rect1 = text1.get_rect(topleft = (40, 20))
    text_rect2 = text2.get_rect(topleft = (40, 70))
    
    # Draw the text on the screen
    SCREEN.blit(text1, text_rect1)
    SCREEN.blit(text2, text_rect2)

	# Draw the text entry boxes
    pygame.draw.rect(SCREEN, pygame.Color(BLUE), (190, 15, 100, 30))
    pygame.draw.rect(SCREEN, pygame.Color(BLUE), (190, 65, 100, 30))
    if is_input_active_row:
        pygame.draw.rect(SCREEN, pygame.Color(BLUE), (190, 15, 100, 30), 2)
    elif is_input_active_col:
        pygame.draw.rect(SCREEN, pygame.Color(BLUE), (190, 65, 100, 30), 2)

    # Render and draw the entered text
    text_surface_row = font.render(input_text_row, True, WHITE)
    text_surface_col = font.render(input_text_col, True, WHITE)
    SCREEN.blit(text_surface_row, (230, 20))
    SCREEN.blit(text_surface_col, (230, 70))

    # Update the display
    pygame.display.flip()

    # Control the frame rate (optional)
    pygame.time.Clock().tick(60)


