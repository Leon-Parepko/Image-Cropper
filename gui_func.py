import os
import re
import numpy as np
import cv2

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

from gui_components import *
import func


class GUIFunc:
    def process(gui, cwd, border, color_rgb, split):
        if not os.path.exists(cwd):
            GUIFunc.write_to_text_field(gui, "There is no such directory!", type="e")
            return 0

        for file in os.listdir(cwd):
            if file.endswith(".jpg") or file.endswith(".png"):
                # Read file
                file_path = os.path.join(cwd, file)
                img = cv2.imread(file_path, 1)

                # Write Processing msg
                GUIFunc.write_to_text_field(gui, f"Processing {file_path}", type="i")

                # Split img into the blocks
                splitted_img = func.split_img(img, split)

                # Process
                iter = 1
                for block in splitted_img:

                    out_img = func.border(block, border, color_rgb)
                    file_splitted = file.split(".")
                    if len(splitted_img) == 1:
                        cv2.imwrite(os.path.join(cwd, f'{file_splitted[0]}_(res).{file_splitted[1]}'), out_img)
                    else:
                        cv2.imwrite(os.path.join(cwd, f'{file_splitted[0]}_(res_{iter}).{file_splitted[1]}'), out_img)

                    iter += 1


    def preprocess(gui, preview):

        # Perform all operations
        RGB = [gui.red_slider.get(), gui.green_slider.get(), gui.blue_slider.get()]
        split_param = [gui.split_H_slider.get(), gui.split_V_slider.get()]
        splited_img_arr = func.split_img(preview, split_param)

        out_img = func.border(splited_img_arr[0], gui.border_slider.get(), RGB)


        # Create horizontal slices from blocks and add them to arr
        horiz_slice_arr = []
        for i in range(0, split_param[0]):
            horiz_slice = func.border(splited_img_arr[i * split_param[1]], gui.border_slider.get(), RGB)
            for j in range(1, split_param[1]):
                horiz_slice = np.concatenate((horiz_slice, func.border(splited_img_arr[(i * split_param[1]) + j], gui.border_slider.get(), RGB)), axis=1)
            horiz_slice_arr.append(horiz_slice)

        if horiz_slice_arr:
            out_img = horiz_slice_arr[0]

        # Combine all horizontal slices
        for i in range(1, len(horiz_slice_arr)):
            out_img = np.concatenate((out_img, horiz_slice_arr[i]), axis=0)



        out_img = func.resize_to_preview(out_img, 250)

        # Convert to tkinter img Object
        im = Image.fromarray(out_img)
        imgtk = ImageTk.PhotoImage(image=im)

        # Update preview
        gui.preview.configure(image=imgtk)
        gui.preview.image = imgtk


    def set_rgb_entry(gui):
        cursor_pos = gui.rgb_entry.index(INSERT)
        gui.rgb_entry.delete(0, "end")
        gui.rgb_entry.insert(0, f'R: {gui.red_slider.get()}  G: {gui.green_slider.get()}  B: {gui.blue_slider.get()}')
        gui.rgb_entry.icursor(cursor_pos)


    def set_rgb_sliders(gui, content):
        if re.match("R: [0-9]+  G: [0-9]+  B: [0-9]+", content):
            content = content.split("  ")
            content = list(map(lambda x: x.split(" ")[1], content))

            gui.red_slider.set(content[0])
            gui.green_slider.set(content[1])
            gui.blue_slider.set(content[2])



    def chose_dir(gui):
        path = filedialog.askdirectory()
        gui.dir_entry.insert(0, path)


    def write_to_text_field(gui, arg, type=''):
        if type == 'i':
            gui.text_field.insert(tk.END, f'Info:    {arg}\n')

        elif type == 'e':
            gui.text_field.insert(tk.END, f'Error:   {arg}\n')

        elif type == 'w':
            gui.text_field.insert(tk.END, f'Warning: {arg}\n')

        elif type == '':
            gui.text_field.insert(tk.END, f'{arg}\n')


