import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import filedialog

check = False

def split(start_split):
    if start_split:
        try:
            #get image path
            def choose_image():
                root = tk.Tk()
                root.withdraw()  # Hide the main tkinter window
                file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
                return file_path

            path = choose_image()
            img = cv2.imread(path)
            # Use the os.path.basename() function to get the filename from the path
            file_name, file_tailname = os.path.splitext(os.path.basename(path))

            piece_width, piece_height = 384, 384
            img = cv2.resize(img, (piece_height, piece_width))

            grid_size = 3

            def img_to_grid(img, row, col):
                ww = [[i.min(), i.max()] for i in np.array_split(range(img.shape[0]), row)]
                hh = [[i.min(), i.max()] for i in np.array_split(range(img.shape[1]), col)]
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
                        filename = os.path.join(output_dir, f"{file_name}{c}{file_tailname}")
                        cv2.imwrite(filename, subimg_rgb)
                        c += 1
                        if c== grid_size**2:
                            c = 0

            row, col = grid_size, grid_size
            grid, r, c = img_to_grid(img, row, col)

            # Specify the directory where you want to save the subimages
            output_directory = 'output_images'
            save_grid_images(grid, r, c, output_directory)
        
            #done_split
            check = True 

        except Exception as e:
            print(f"Error: {e}")
            return None



