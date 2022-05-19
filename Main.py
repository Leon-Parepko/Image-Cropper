"""
------------------ Image-Cropper By LPM 05.17.2022 ------------------
------------------           V 1.6 alpha           ------------------

         This is a simple program, with graphical interface,
        which was constructed to prepare images for printing
        in separate paper lists. You could configure slice,
        border and color settings to print your pictures in
        higher (physical) resolution. The program supports
        operating on multiple files (in same directory) at
        the same time. Also, you could use console mode to
        perform operations faster and with higher performance.
"""
import tkinter as tk

import gui_components
import grid
import cmd


if __name__ == '__main__':

    MODE = "gui"

    if MODE == "gui":
        window = tk.Tk()
        window.title('Image-Cropper')

        gui = gui_components.Components(window)
        grid.construct_grid(gui)

        window.mainloop()

    elif MODE == "cmd":
        while cmd.start():
            pass

