
import os
import re
import cv2
import numpy as np
import tkinter as tk

from tkinter import filedialog, INSERT
from PIL import Image, ImageTk

from gui_components import *
import func

"""
 This class is implementing base 
functional of graphical interface.
It contains only functions.
Also, The instance of one is
inherited in 'gui_components'. 
"""
class GUIFunc:
    """
     This one loads default img
    as preview
    """
    def get_default_preview(gui):
        try:
            img = cv2.imread('content/default_banner.jpg')
            img_preview = func.resize_to_preview(img, 250)
            img_preview_b, img_preview_g, img_preview_r = cv2.split(img_preview)
            preview = cv2.merge((img_preview_r, img_preview_g, img_preview_b))
            return preview

        except Exception as e:
            # GUIFunc.write_to_text_field(gui, f"Can't load default banner due to:\n {e}", 'e')
            return np.zeros((250, 250, 3))


    """
    It seems to be look like gui adapter
    """
    def process_gui(gui):
        border_param = gui.border_slider.get()
        split_param = gui.get_split()
        color_rgb = gui.get_rgb()
        cwd = gui.dir_entry.get()
        out_wd = os.path.join(cwd, 'out')
        multiproc = gui.mult_check_box_var.get()

        # Perform operations and check for possible errors
        error = func.process(border_param, split_param, color_rgb, cwd, out_wd, multiproc=multiproc)
        if error is not None:
            GUIFunc.write_to_text_field(gui, error, 'e')
        else:
            GUIFunc.write_to_text_field(gui, "Finished!", 'i')


    """
    Returns a preprocessed img
    after performing all operations. 
    """
    def preprocess(gui, preview):
        try:
            # Get some variables from gui
            RGB = [gui.red_slider.get(), gui.green_slider.get(), gui.blue_slider.get()]
            split_param = [gui.split_H_slider.get(), gui.split_V_slider.get()]

            # Perform all operations
            out_img = func.block_preview(preview, gui.border_slider.get(), split_param, RGB)
            out_img = func.resize_to_preview(out_img, 250)

            # Convert to tkinter img Object
            im = Image.fromarray(out_img)
            imgtk = ImageTk.PhotoImage(image=im)

            # Update preview
            gui.preview.configure(image=imgtk)
            gui.preview.image = imgtk

        except Exception as e:
            GUIFunc.write_to_text_field(gui, f"Can't preprocess banner due to: '{e}'", 'e')


    """
     This one change the value
    of rgb and hue entry fields
    due to sliders(rgb) parameters.
    """
    def set_color_entry(gui):
        # Get some variables from gui
        rgb_cursor_pos = gui.rgb_entry.index(INSERT)
        hsv_cursor_pos = gui.hsv_entry.index(INSERT)
        r = gui.red_slider.get()
        g = gui.green_slider.get()
        b = gui.blue_slider.get()

        # Convert RGB to HSV
        h, s, v = func.rgb_to_hsv(r, g, b)

        # Update entry fields
        gui.rgb_entry.delete(0, "end")
        gui.rgb_entry.insert(0, f'R: {r}  G: {g}  B: {b}')
        gui.rgb_entry.icursor(rgb_cursor_pos)

        gui.hsv_entry.delete(0, "end")
        gui.hsv_entry.insert(0, f'H: {round(h)}  S: {round(s)}  V: {round(v)}')
        gui.hsv_entry.icursor(hsv_cursor_pos)


    """
     This function updates the
    value of rgb sliders, depending
    on entry field state.
    """
    def set_rgb_sliders(gui, content):
        #  Check if entry field format is correct
        if re.match("R: [0-9]+  G: [0-9]+  B: [0-9]+", content):
            content = content.split("  ")
            content = list(map(lambda x: x.split(" ")[1], content))

            # Update sliders
            gui.red_slider.set(content[0])
            gui.green_slider.set(content[1])
            gui.blue_slider.set(content[2])

        # else:
        #     GUIFunc.write_to_text_field(gui, "Wrong RGB format: 'R: <int 255>  G: <int 255>  B: <int 255>'", 'w')


    """
     This function get usr defined 
    directory and update the preview img
    from chosen folder.
    """
    def chose_dir(gui):
        # Ask user for the directory path
        path = filedialog.askdirectory()
        gui.dir_entry.insert(0, path)

        if path == '':
            return

        # Load preview img from user sours
        for file in os.listdir(path):
            if file.endswith(".jpg") or file.endswith(".png"):
                file_path = os.path.join(path, file)
                img = cv2.imread(file_path)
                img_preview = func.resize_to_preview(img, 250)
                img_preview_b, img_preview_g, img_preview_r = cv2.split(img_preview)
                final_img_preview = cv2.merge((img_preview_r, img_preview_g, img_preview_b))
                gui.preview_img = final_img_preview
                GUIFunc.preprocess(gui, final_img_preview)
                GUIFunc.write_to_text_field(gui, f"Loaded '{file_path}' as banner", 'i')
                return
        GUIFunc.write_to_text_field(gui, "Can't find any images!", 'w')


    """
     Simply write some types
    of information to the
    output text field.
    """
    def write_to_text_field(gui, arg, type=''):
        if type == 'i':
            gui.text_field.insert(tk.END, f'Info:    {arg}\n')

        elif type == 'e':
            gui.text_field.insert(tk.END, f'Error:   {arg}\n')

        elif type == 'w':
            gui.text_field.insert(tk.END, f'Warning: {arg}\n')

        elif type == '':
            gui.text_field.insert(tk.END, f'{arg}\n')
