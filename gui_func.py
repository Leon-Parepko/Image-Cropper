
import os
import re
import cv2
import numpy as np
import concurrent.futures
import tkinter as tk

from tkinter import filedialog, INSERT
from PIL import Image, ImageTk

from gui_components import *
import func


class GUIFunc:

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
            pass


    def process(gui):
        border_param = gui.border_slider.get()
        split_param = gui.get_split()
        color_rgb = gui.get_RGB()
        cwd = gui.dir_entry.get()
        out_wd = os.path.join(cwd, 'out')

        try:
            os.mkdir(out_wd)
            GUIFunc.write_to_text_field(gui, f"New output directory was created in: {out_wd}", 'i')
        except:
            pass

        try:
            if not os.path.exists(cwd):
                GUIFunc.write_to_text_field(gui, "There is no such directory!", type="e")
                return

            file_list = []
            for file in os.listdir(cwd):
                if file.endswith(".jpg") or file.endswith(".png"):

                    # Read file
                    file_path = os.path.join(cwd, file)
                    file_list.append([file, file_path])

                    # img = cv2.imread(file_path, 1)
                    #
                    # # Write Processing msg
                    # GUIFunc.write_to_text_field(gui, f"Processing {file_path}", type="i")

                    # Split img into the blocks
                    # splitted_img = func.split_img(img, split_param)
                    #
                    # # Process
                    # iter = 1
                    # for block in splitted_img:
                    #     out_img = func.border(block, border, color_rgb)
                    #     file_splitted = file.split(".")
                    #
                    #     if len(splitted_img) == 1:
                    #         cv2.imwrite(os.path.join(out_wd, f'{file_splitted[0]}_(res).{file_splitted[1]}'), out_img)
                    #     else:
                    #         cv2.imwrite(os.path.join(out_wd, f'{file_splitted[0]}_(res_{iter}).{file_splitted[1]}'), out_img)
                    #
                    #     iter += 1

                    # func.process_operations(file_path, file, border_param, split_param, color_rgb, out_wd)

            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = [executor.submit(func.process_operations, single_file_path[1], single_file_path[0], border_param, split_param, color_rgb, out_wd) for single_file_path in file_list]

                # Write Processing msg
                for f in concurrent.futures.as_completed(results):
                    GUIFunc.write_to_text_field(gui, f"{f.result()} Done!", 'i')

        except Exception as e:
            GUIFunc.write_to_text_field(gui, f"Can't process img due to: {e}", 'e')


    def preprocess(gui, preview):
        try:
            # Get some variables
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
            GUIFunc.write_to_text_field(gui, f"Can't preprocess banner due to: {e}", 'e')


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

        # else:
        #     GUIFunc.write_to_text_field(gui, "Wrong RGB format: 'R: <int 255>  G: <int 255>  B: <int 255>'", 'w')


    def chose_dir(gui):
        path = filedialog.askdirectory()
        gui.dir_entry.insert(0, path)

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


    def write_to_text_field(gui, arg, type=''):
        if type == 'i':
            gui.text_field.insert(tk.END, f'Info:    {arg}\n')

        elif type == 'e':
            gui.text_field.insert(tk.END, f'Error:   {arg}\n')

        elif type == 'w':
            gui.text_field.insert(tk.END, f'Warning: {arg}\n')

        elif type == '':
            gui.text_field.insert(tk.END, f'{arg}\n')
