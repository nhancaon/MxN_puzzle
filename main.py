import pygame
import random
import time
import os
import copy

from sprite import *
from settings import *
from algo import *
from split_img import *
from hover import *
import tkinter as tk
from tkinter import scrolledtext

# block open Add image many times
icheck = 0

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.step = ""
        self.shuffle_time = 0
        self.start_shuffle = False
        self.start_DFS = False
        self.start_IDS = False
        self.start_BFS = False
        self.start_UCS = False
        self.start_A_STAR = False
        self.start_GREEDY = False
        self.start_HILL = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])
        self.pieces = []
        self.start_add_image = False
        multi = None
        self.problem = [[x + y * GAME_SIZE_X for x in range(1, GAME_SIZE_X + 1)] for y in range(GAME_SIZE_Y)]
        self.problem[-1][-1] = 0
        self.searched_state_bfs = [0]
        self.searched_state_dfs = [0]
        self.searched_state_ids = [0]
        self.searched_state_ucs = [0]
        self.searched_state_astar = [0]
        self.searched_state_greedy = [0]
        self.searched_state_hill = [0]
        self.steps_bfs = 0
        self.steps_dfs = 0
        self.steps_ids = 0
        self.steps_ucs = 0
        self.steps_astar = 0
        self.steps_greedy = 0
        self.steps_hill = 0
        self.moves = []

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [[x + y * GAME_SIZE_X for x in range(1, GAME_SIZE_X + 1)] for y in range(GAME_SIZE_Y)]
        grid[-1][-1] = 0
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("R")
                    if tile.left():
                        possible_moves.append("L")
                    if tile.up():
                        possible_moves.append("U")
                    if tile.down():
                        possible_moves.append("D")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "R":
            possible_moves.remove("L") if "L" in possible_moves else possible_moves
        elif self.previous_choice == "L":
            possible_moves.remove("R") if "R" in possible_moves else possible_moves
        elif self.previous_choice == "U":
            possible_moves.remove("D") if "D" in possible_moves else possible_moves
        elif self.previous_choice == "D":
            possible_moves.remove("U") if "U" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "R":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                self.tiles_grid[row][col]
        elif choice == "L":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                self.tiles_grid[row][col]
        elif choice == "U":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                self.tiles_grid[row][col]
        elif choice == "D":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                self.tiles_grid[row][col]

    #region Algorithms
    def BFS(self):
        solution_path = bfs(self.initial_state, self.goal_state,self.searched_state_bfs)
        if solution_path:
            self.steps_bfs = len(solution_path)
        self.draw()
        return solution_path

    def DFS(self):
        solution_path = dfs(self.initial_state, self.goal_state,self.searched_state_dfs)
        if solution_path:
            self.steps_dfs=len(solution_path)
        return solution_path

    def IDS(self):
        solution_path = ids(
            self.initial_state, self.goal_state,self.searched_state_ids)
        if solution_path:
            self.steps_ids=len(solution_path)
        return solution_path

    def UCS(self):
        solution_path = ucs(self.initial_state, self.goal_state,self.searched_state_ucs)
        if solution_path:
            self.steps_ucs=len(solution_path)
        return solution_path

    def A_STAR(self):
        solution_path = a_star(self.initial_state, self.goal_state,self.searched_state_astar)
        if solution_path:
            self.steps_astar=len(solution_path)
        return solution_path

    def GREEDY(self):
        solution_path = greedy(
            self.initial_state, self.goal_state,self.searched_state_greedy)
        if solution_path:
            self.steps_greedy=len(solution_path)
        return solution_path
    
    def HILL(self):
        solution_path = hill_climbing(
            self.initial_state, self.goal_state,self.searched_state_hill)
        if solution_path:
            self.steps_hill=len(solution_path)
        return solution_path
    #endregion

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_second = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.picture_list = []
        self.size_x = len(self.tiles_grid)
        self.size_y = len(self.tiles_grid[0])
        self.goal_state = [[x + y * self.size_y for x in range(1, self.size_y + 1)] for y in range(self.size_x)]
        self.goal_state[-1][-1] = 0
        self.initial_state = copy.deepcopy(self.goal_state)

        #region Button creation
        button4 = Button("Clear image",200,50,(700,25),5)
        button5 = Button("Add image",200,50,(700,100),5)
        button6 = Button("Reset",200,50,(700,170),5)
        button7 = Button("Shuffle",200,50,(950,25),5)
        button8 = Button("SOLVE",100,50,(1000,100),5)
        button9 = Button("Quit Game",200,50,(950,240),5)
        button10 = Button("New Game",200,50,(700,240),5)

        name_button = ["BFS", "DFS", "IDS", "UCS", "A_STAR", "GREEDY","HILL CLIMBING"]
        multi_btn = MultiOptionButton(name_button, "Algorithm", 200, 50, (950, 170), 5)
        #endregion

        self.draw_tiles()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 30:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True
                self.problem=copy.deepcopy(self.tiles_grid)
                self.searched_state_bfs = [0]
                self.searched_state_dfs = [0]
                self.searched_state_ids = [0]
                self.searched_state_ucs = [0]
                self.searched_state_astar = [0]
                self.searched_state_greedy = [0]
                self.searched_state_hill = [0]
                self.steps_bfs = 0
                self.steps_dfs = 0
                self.steps_ids = 0
                self.steps_ucs = 0
                self.steps_astar = 0
                self.steps_greedy = 0
                self.steps_hill = 0
                self.moves = []
                self.draw()
        if self.start_DFS:
            solution_path = self.DFS()

            if solution_path:
                self.moves=[]
                self.moves=copy.deepcopy(solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_DFS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_DFS = False
                self.start_game = True
                self.start_timer = True
        if self.start_BFS == True:
            solution_path = self.BFS()
            if solution_path:
                self.moves=[]
                self.moves=copy.deepcopy(solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_BFS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_BFS = False
                self.start_game = True
                self.start_timer = True
        if self.start_UCS:
            solution_path = self.UCS()

            if solution_path:
                self.moves=[]
                self.moves=copy.deepcopy(solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_UCS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_UCS = False
                self.start_game = True
                self.start_timer = True
        if self.start_A_STAR:
            solution_path = self.A_STAR()

            if solution_path:
                self.moves=[]
                self.moves=copy.deepcopy(solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_A_STAR = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_A_STAR = False
                self.start_game = True
                self.start_timer = True
        if self.start_GREEDY:
            
            solution_path = self.GREEDY()
            if solution_path:
                self.moves=[]
                self.moves=copy.deepcopy(solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_GREEDY = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_GREEDY = False
                self.start_game = True
                self.start_timer = True
        if self.start_HILL:
            solution_path = self.HILL()
            
            if solution_path:
                self.moves=[]
                self.moves=copy.deepcopy(solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_HILL = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_HILL = False
                self.start_game = True
                self.start_timer = True
        if self.start_IDS:
            solution_path = self.IDS()

            if solution_path:
                self.moves=copy.deepcopy(solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_IDS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_IDS = False
                self.start_game = True
                self.start_timer = True            
        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE_X * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0),
                             (row, GAME_SIZE_Y * TILESIZE))
        for col in range(-1, GAME_SIZE_Y * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col),
                             (GAME_SIZE_X * TILESIZE, col))

    def draw(self):
        #set background
        bg = pygame.image.load("images/bgmain.jpg").convert()
        self.screen.blit(bg,(0,0))

        #draw buttons
        buttons_draw()

        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for pic in self.picture_list:
            pic.draw(self.screen)
        UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(430, 300, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        UIElement(430, 350, "BFS Searched : %.0f" %
                  (self.searched_state_bfs[0])).draw(self.screen)
        UIElement(800, 350, "Steps : %.0f" %
                  (self.steps_bfs)).draw(self.screen)
        UIElement(430, 400, "DFS Searched : %.0f" %
                  (self.searched_state_dfs[0])).draw(self.screen)
        UIElement(800, 400, "Steps : %.0f" %
                  (self.steps_dfs)).draw(self.screen)
        UIElement(430, 450, "IDS Searched : %.0f" %
                  (self.searched_state_ids[0])).draw(self.screen)
        UIElement(800, 450, "Steps : %.0f" %
                  (self.steps_ids)).draw(self.screen)
        UIElement(430, 500, "UCS Searched : %.0f" %
                  (self.searched_state_ucs[0])).draw(self.screen)
        UIElement(800, 500, "Steps : %.0f" %
                  (self.steps_ucs)).draw(self.screen)
        UIElement(430, 550, "GREEDY Searched : %.0f" %
                  (self.searched_state_greedy[0])).draw(self.screen)
        UIElement(800, 550, "Steps : %.0f" %
                  (self.steps_greedy)).draw(self.screen)
        UIElement(430, 600, "A* Searched : %.0f" %
                  (self.searched_state_astar[0])).draw(self.screen)
        UIElement(800, 600, "Steps : %.0f" %
                  (self.steps_astar)).draw(self.screen)
        UIElement(430, 650, "Hill climbing Searched : %.0f" %
                  (self.searched_state_hill[0])).draw(self.screen)
        UIElement(950, 650, "Steps : %.0f" %
                  (self.steps_hill)).draw(self.screen)
        UIE(50, 450, self.moves).draw(self.screen)
        pygame.display.flip()
    

    def draw_tiles(self):
        self.tiles = []
        if self.start_add_image:
            for row, x in enumerate(self.tiles_grid):
                self.tiles.append([])
                for col, tile in enumerate(x):
                    i = tile
                    if i == 0:
                        i = GAME_SIZE_X*GAME_SIZE_Y-1
                    else:
                        i -= 1
                    if tile != 0:
                        self.tiles[row].append(Tile(self, col, row, None, self.pieces[i]))
                    else:
                        self.tiles[row].append(Tile(self, col, row, "empty", self.pieces[i]))

        else:
            for row, x in enumerate(self.tiles_grid):
                self.tiles.append([])
                for col, tile in enumerate(x):
                    if tile != 0:
                        self.tiles[row].append(Tile(self, col, row, str(tile)))
                    else:
                        self.tiles[row].append(Tile(self, col, row, "empty"))

    def move_tile(self, path):
        initial_state = [row[:] for row in self.tiles_grid]
        # Find the position of the empty tile (0)
        row, col = None, None
        for i in range(GAME_SIZE_Y):
            for j in range(GAME_SIZE_X):
                if initial_state[i][j] == 0:
                    row, col = i, j
        if path == "D":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

        elif path == "U":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

        elif path == "R":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

        elif path == "L":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

        else:
            print("Invalid move: Unknown direction")
        self.draw()
        self.draw_tiles()
        self.all_sprites.update()
        pygame.time.delay(150)

    def return_picture_list(self):
        # Use a list comprehension to filter files with .png extension
        directory_path = "D:/UNIVERSITY/3rd/Semester 1/Artificial Intelligence/FINAL PROJECT/8-Puzzle/output_images/"
        picture_list_save = [f"output_images/{file}" for file in os.listdir(directory_path) if file.endswith(f".jpg")]
        return picture_list_save

    def events(self):
        global output_images_path
        output_images_path = 'output_images/'
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

        global icheck #limit the auto press of button Add image avoid error
        clicked_button_text = get_clicked_button_text()
        multi = get_clicked_button_text_multi()

        if clicked_button_text == "Shuffle":
            self.shuffle_time = 0
            self.start_shuffle = True

        if clicked_button_text == "New Game":
            self.new()
            self.searched_state_bfs = [0]
            self.searched_state_dfs = [0]
            self.searched_state_ids = [0]
            self.searched_state_ucs = [0]
            self.searched_state_astar = [0]
            self.searched_state_greedy = [0]
            self.searched_state_hill = [0]
            self.steps_bfs = 0
            self.steps_dfs = 0
            self.steps_ids = 0
            self.steps_ucs = 0
            self.steps_astar = 0
            self.steps_greedy = 0
            self.steps_hill = 0
            self.moves = []
            
        if clicked_button_text == "Reset":
            self.tiles_grid=copy.deepcopy(self.problem)
            self.draw_tiles()

        if clicked_button_text == "Add image":
            if icheck == 0:
                icheck = 1
                self.start_add_image = True
                selected_image_path = split(self.start_add_image)
                if self.start_add_image:  
                    # Convert pictures to surfaces
                    image_surfaces = self.return_picture_list()
                    self.pieces = [pygame.image.load(image_path).convert_alpha() for image_path in image_surfaces]

                    self.draw_tiles()

        if clicked_button_text == "Clear image":
            icheck = 0
            self.picture_list = []
            self.start_add_image = False
            # Delete images in folder output_images
            delete_files_in_directory(output_images_path)
            self.draw_tiles()
        if clicked_button_text == "SOLVE":
            self.initial_state = copy.deepcopy(self.tiles_grid)
            if multi == "BFS":
                self.shuffle_time = 0
                self.start_BFS = True 
            elif multi == "DFS":
                self.shuffle_time = 0
                self.start_DFS = True
            elif multi == "IDS":
                self.shuffle_time = 0
                self.start_IDS = True
            elif multi == "UCS":
                self.shuffle_time = 0
                self.start_UCS = True
            elif multi == "A_STAR":
                self.shuffle_time = 0
                self.start_A_STAR = True
            elif multi == "GREEDY":
                self.shuffle_time = 0
                self.start_GREEDY = True
            elif multi == "HILL CLIMBING":
                self.shuffle_time = 0
                self.start_HILL = True

        if clicked_button_text == "Quit Game":
            delete_files_in_directory(output_images_path)
            pygame.quit()
            quit(0)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
def delete_files_in_directory(directory):
    # Get the list of files in the directory
    file_list = os.listdir(directory)

    # Iterate over the files and delete each one
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Not a file: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


game = Game()

while True:
    game.new()
    game.run()
    delete_files_in_directory(output_images_path)
