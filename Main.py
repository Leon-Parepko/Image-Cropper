"""
--------------- By LPM 05.17.2022 ---------------
---------------    V 1.0 alpha    ---------------
"""

import cv2

import tkinter as tk

import grid
import gui_components
from func import resize_to_preview
from PIL import Image, ImageTk

if __name__ == '__main__':
    window = tk.Tk()

    window.title('Image-Cropper')


    img = cv2.imread(f'Test/T/4.jpg')


    # img_preview = resize_to_preview(img, 300)
    # img_preview_b, img_preview_g, img_preview_r = cv2.split(img_preview)
    # img_preview = cv2.merge((img_preview_r, img_preview_g, img_preview_b))
    #
    # # Convert the Image object into a TkPhoto object
    # im = Image.fromarray(img_preview)
    # imgtk = ImageTk.PhotoImage(image=im)

    gui = gui_components.Components(window)
    grid.construct_grid(gui)

    window.mainloop()

