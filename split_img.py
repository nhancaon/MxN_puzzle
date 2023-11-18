import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import filedialog

from unidecode import unidecode
import shutil

from settings import *

def strange_characters(file_path):
    return any(ord(char) > 127 for char in file_path)

check = False

def split(start_split):
    global path
    if start_split:
        #get image path
        def choose_image():
            root = tk.Tk()
            root.withdraw()  # Hide the main tkinter window
            file_path = filedialog.askopenfilename(title="Selecting Image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
                
            if strange_characters(file_path):
                # Extract the file name and extension
                file_name_temp, file_ext = os.path.splitext(os.path.basename(file_path))

                # Transliterate Vietnamese characters in the file name
                new_file_name = unidecode(file_name_temp)

                if not os.path.exists("NonEnglish_images"):
                    os.makedirs("NonEnglish_images")

                # Create a new file path with the updated file name
                new_file_path = os.path.join(os.path.dirname("NonEnglish_images/"), f"{new_file_name}{file_ext}")

                # Copy the original file to the new location with the updated name
                shutil.copyfile(file_path, new_file_path)

                # Return the updated file path
                return new_file_path
            else:
                return file_path

        path = choose_image()
        img = cv2.imread(path)
        # Use the os.path.basename() function to get the filename from the path
        file_name, file_tailname = os.path.splitext(os.path.basename(path))

        piece_width, piece_height = TILESIZE * GAME_SIZE_Y, TILESIZE * GAME_SIZE_X
        img = cv2.resize(img, (piece_height, piece_width))

        # grid_size = 3

        def img_to_grid(img, row, col):
            ww = [[i.min(), i.max()] for i in np.array_split(range(img.shape[0]), col)]
            hh = [[i.min(), i.max()] for i in np.array_split(range(img.shape[1]), row)]
            grid = [img[j:jj, i:ii, :] for j, jj in ww for i, ii in hh]
            return grid, len(ww), len(hh)


        def save_grid_images(grid, rows, cols, output_dir):
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            c = 1
            for row in range(rows):
                for col in range(cols):
                    subimg = np.flip(grid[c], axis =- 1)
                    subimg_rgb = cv2.cvtColor(subimg, cv2.COLOR_BGR2RGB)
                    if c == rows * cols - 1:
                        subimg_rgb = cv2.medianBlur(subimg_rgb,5)
                    filename = os.path.join(output_dir, f"{file_name}{c}{file_tailname}")
                    cv2.imwrite(filename, subimg_rgb)
                    c += 1
                    if c == rows * cols:
                        c = 0

        row, col = GAME_SIZE_X, GAME_SIZE_Y
        grid, r, c = img_to_grid(img, row, col)

        # Specify the directory where you want to save the subimages
        output_directory = 'output_images'
        save_grid_images(grid, r, c, output_directory)
        
        #done_split
        check = True 

def origin_path():
    return path


