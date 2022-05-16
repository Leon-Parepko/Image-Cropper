import os
import re
import numpy as np
import cv2

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

from func import resize
from gui_components import *


class Func:

    def split_img(img, split):

        out_arr = []
        block_dim = [img.shape[0] // split[0], img.shape[1] // split[1]]

        for h in range(0, split[0]):
            h_slice = img[h * block_dim[0]:(h + 1) * block_dim[0]]
            h_slice = cv2.rotate(h_slice, cv2.ROTATE_90_CLOCKWISE)
            for w in range(0, split[1]):
                v_slice = h_slice[w * block_dim[1]:(w + 1) * block_dim[1]]
                v_slice = cv2.rotate(v_slice, cv2.ROTATE_90_COUNTERCLOCKWISE)
                out_arr.append(v_slice)

        return out_arr




    def process(gui, cwd, border, color_rgb, split):

        if not os.path.exists(cwd):
            Func.write_to_text_field(gui, "There is no such directory!", type="e")
            return 0

        for file in os.listdir(cwd):
            if file.endswith(".jpg") or file.endswith(".png"):
                # Read file
                file_path = os.path.join(cwd, file)
                img = cv2.imread(file_path, 1)

                # Write Processing msg
                Func.write_to_text_field(gui, f"Processing {file_path}", type="i")

                # Split img into the blocks
                splitted_img = Func.split_img(img, split)

                # Process
                iter = 1
                for block in splitted_img:
                    img_b = resize(block, 100 + border)

                    back = np.full(img_b.shape, color_rgb, dtype=np.uint8)
                    h, w = img_b.shape[:2]
                    h1, w1 = block.shape[:2]

                    cx, cy = (h - h1) // 2, (w - w1) // 2

                    back[cx:h1+cx, cy:w1+cy] = block

                    file_splitted = file.split(".")
                    if len(splitted_img) == 1:
                        cv2.imwrite(os.path.join(cwd, f'{file_splitted[0]}_(res).{file_splitted[1]}'), back)
                    else:
                        cv2.imwrite(os.path.join(cwd, f'{file_splitted[0]}_(res_{iter}).{file_splitted[1]}'), back)

                    iter += 1


    def preprocess(gui, border):
        global img_preview
        back = np.full(img_preview.shape, [255, 255, 0], dtype=np.uint8)
        im = Image.fromarray(back)
        imgtk = ImageTk.PhotoImage(image=im)
        # preview.configure(image=imgtk)


    def set_rgb_entry(gui, event):
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


