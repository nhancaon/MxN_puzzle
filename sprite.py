import pygame
from settings import *

pygame.font.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text=None, image=None):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if image == None:
            if self.text != "empty":
                self.font = pygame.font.SysFont("Consolas", 50)
                font_surface = self.font.render(self.text, True, WHITE)
                self.image.fill(BLACK)
                self.font_size = self.font.size(self.text)
                draw_x = (TILE_SIZE / 2) - self.font_size[0] / 2
                draw_y = (TILE_SIZE / 2) - self.font_size[1] / 2
                self.image.blit(font_surface, (draw_x, draw_y))
            else:
                self.image.fill(BG_COLOR)
        else:
            if self.text == None:
                self.image = image
            elif self.text == "empty":
                self.font = pygame.font.SysFont("Consolas", 50)
                font_surface = self.font.render(self.text, True, WHITE)

                self.font_size = self.font.size(self.text)
                draw_x = (TILE_SIZE / 2) - self.font_size[0] / 2
                draw_y = (TILE_SIZE / 2) - self.font_size[1] / 2
                self.image.blit(font_surface, (draw_x, draw_y))
                self.image = image
            # else:
            #     self.image.fill(BG_COLOR)

    def update(self):
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + TILE_SIZE < GAME_SIZE_X * TILE_SIZE

    def left(self):
        return self.rect.x - TILE_SIZE >= 0

    def up(self):
        return self.rect.y - TILE_SIZE >= 0

    def down(self):
        return self.rect.y + TILE_SIZE < GAME_SIZE_Y * TILE_SIZE

class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))
        
class UIE:
    def __init__(self, x, y, text_list, max_chars=35):
        self.x, self.y = x, y
        self.text_list = self.format_text(text_list, max_chars)

    def format_text(self,text_list, max_chars):
        formatted_text = []
        current_line = ""
        for char in text_list:
            if len(current_line + char) <= max_chars:
                current_line += char
            else:
                formatted_text.append(current_line)
                current_line = char
        formatted_text.append(current_line)

        return formatted_text


    def draw(self, screen):
        pygame.init()
        font = pygame.font.SysFont("Consolas", 30)
        y_offset = 0  

        for text in self.text_list:
            text_surface = font.render(text, True, (255, 255, 255))  # White color for text
            text_rect = text_surface.get_rect(topleft=(self.x, self.y + y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += text_rect.height

class Picture:
    def __init__(self, x, y, width, height, image):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.image = image # Set the image directly
        self.rect = self.image.get_rect()

    def draw(self, screen):
        # Update the picture's rect position
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)  # Blit the image onto the screen

    def resize(self):
        self.image = pygame.transform.scale(self.image, (self.width/3, self.height/3))
        self.width, self.height = self.width/3, self.width/3