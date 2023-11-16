import pygame,sys
from subprocess import call

buttons = []
multi = []
multi_press = 0
# multi_check = False

class Button:
    def __init__(self, text, width, height, pos, elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text = text
        self.text_surf = gui_font.render(text, True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        buttons.append(self)

    def change_text(self, newtext):
        self.text_surf = gui_font.render(newtext, True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    print('click')
                    if self.text == "Play":
                        pygame.quit()
                        #open main.py and close login interface
                        open_py_file()
                        sys.exit()
                    if self.text == "Guide":
                        self.pressed = False
                    if self.text == "Exit":
                        pygame.quit()
                        sys.exit()
                    if self.text == "Clear image":
                        self.pressed = False
                        print(self.text)
                    if self.text == "Add image":
                        self.pressed = False
                        print(self.text)
                    if self.text == "Reset":
                        self.pressed = False
                        print(self.text)
                    if self.text == "Shuffle":
                        self.pressed = False
                        print(self.text)               
                    if self.text == "SOLVE":
                        self.pressed = False
                        print(self.text)
                    self.pressed = False
                    self.change_text(self.text)
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'

class MultiOptionButton(Button):
    def __init__(self, translations, text, width, height, pos, elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'
        self.translations = translations
        self.num_press = -1

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'

        #text
        self.text = text
        self.text_surf = gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        multi.append(self)

    def change_text(self, newtext):
        self.text_surf = gui_font.render(newtext, True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen, self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                # global multi_check
                self.dynamic_elevation = 0
                self.pressed = True
                # multi_check = True
                for i in range(len(self.translations)):
                    if self.num_press == i:
                        self.change_text(f"{self.translations[i]}")
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.num_press += 1
                    for i in range(len(self.translations)):
                        if self.num_press == i:
                            global multi_press
                            multi_press = f"{self.translations[i]}"
                            self.change_text(f"{self.translations[i]}")
                            print(self.translations[i])
                        if self.num_press > (len(self.translations) - 1):
                            self.change_text(self.text)
                            self.num_press = -1
                    # multi_check = False
                    self.pressed = False
                    
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'

def get_clicked_button_text():
    for button in buttons:
        if button.pressed:
            button.pressed = False  # Reset the pressed state
            return button.text
    return None

def get_clicked_button_text_multi():
    return multi_press

pygame.init()
screen = pygame.display.set_mode((1000,500))
pygame.display.set_caption('Login interface')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)

#draw buttons
def buttons_draw():
    for b in buttons:
        b.draw()
    for mul in multi:
        mul.draw()

#open other file
def open_py_file():
    call(["python3", "main.py"])


