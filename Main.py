"""
--------------- By LPM 05.17.2022 ---------------
---------------    V 1.0 alpha    ---------------
"""
import tkinter as tk

import grid
import gui_components

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Image-Cropper')

    gui = gui_components.Components(window)
    grid.construct_grid(gui)

    window.mainloop()

