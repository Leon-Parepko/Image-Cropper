import os
import re
import numpy as np
import cv2

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk



def noise(img):
    noised_image = img.copy()
    noise = np.random.randint(150, 255, size=(img[img >= 100].size), dtype=np.uint8)
    noised_image[noised_image >= 100] += noise
    return noised_image


def shift(img, r=0, l=0, u=0, d=0):
    shifted_image = img.copy()
    temp = shifted_image[u:img.shape[0] - d, l:img.shape[1] - r]
    shifted_image = cv2.copyMakeBorder(temp, d, u, r, l, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return shifted_image


def resize(img, scale_factor):
    width = int(img.shape[1] * scale_factor / 100)
    height = int(img.shape[0] * scale_factor / 100)
    dim = (width, height)
    resized = cv2.resize(img.copy(), dim, interpolation=cv2.INTER_AREA)
    return resized


def resize_to_preview(img, max_size):
    width = int(img.shape[1])
    height = int(img.shape[0])
    dim = (width, height)

    if max(dim) >= max_size:
        scale_factor = max(dim) / max_size
        new_dim = (int(width // scale_factor), int(height // scale_factor))

    else:
        scale_factor = (max_size / max(dim))
        new_dim = (int(width * scale_factor), int(height * scale_factor))


    resized = cv2.resize(img.copy(), new_dim, interpolation=cv2.INTER_AREA)
    return resized





def process(cwd, border, color_rgb):
    if not os.path.exists(cwd):
        write_to_text_field("There is no such directory!", type="e")
        return 0



    for file in os.listdir(cwd):
        if file.endswith(".jpg") or file.endswith(".png"):
            file_path = os.path.join(cwd, file)

            img = cv2.imread(file_path, 1)
            img_b = resize(img, 100 + border)

            back = np.full(img_b.shape, color_rgb, dtype=np.uint8)
            h, w = img_b.shape[:2]
            h1, w1 = img.shape[:2]

            cx, cy = (h - h1) // 2, (w - w1) // 2

            back[cx:h1+cx, cy:w1+cy] = img

            cv2.imwrite(os.path.join(cwd, f'(res)_{file}'), back)
            write_to_text_field(f"Processing {file_path}", type="i")


def preprocess(border):
    global img_preview
    back = np.full(img_preview.shape, [255, 255, 0], dtype=np.uint8)
    im = Image.fromarray(back)
    imgtk = ImageTk.PhotoImage(image=im)
    preview.configure(image=imgtk)




def set_rgb_entry(num):
    cursor_pos = rgb_entry.index(INSERT)
    rgb_entry.delete(0,"end")
    rgb_entry.insert(0, f'R: {red_slider.get()}  G: {green_slider.get()}  B: {blue_slider.get()}')
    rgb_entry.icursor(cursor_pos)


def set_rgb_sliders(content):
    if re.match("R: [0-9]+  G: [0-9]+  B: [0-9]+", content):

        content = content.split("  ")
        content = list(map(lambda x: x.split(" ")[1], content))

        red_slider.set(content[0])
        green_slider.set(content[1])
        blue_slider.set(content[2])
        


def chose_dir():
    path = filedialog.askdirectory()
    dir_entry.insert(0, path)


def write_to_text_field(arg, type=''):
    if type == 'i':
        text_field.insert(tk.END, f'Info:    {arg}\n')

    elif type == 'e':
        text_field.insert(tk.END, f'Error:   {arg}\n')

    elif type == 'w':
        text_field.insert(tk.END, f'Warning: {arg}\n')

    elif type == '':
        text_field.insert(tk.END, f'{arg}\n')

window = tk.Tk()

window.title('Counting Seconds')


img = cv2.imread(f'Test/T/4.jpg')


img_preview = resize_to_preview(img, 300)
img_preview_b, img_preview_g, img_preview_r = cv2.split(img_preview)
img_preview = cv2.merge((img_preview_r, img_preview_g, img_preview_b))

# Convert the Image object into a TkPhoto object
im = Image.fromarray(img_preview)
imgtk = ImageTk.PhotoImage(image=im)





# Introduce window components
border_label = tk.Label(window, text='BORDER')
border_slider = tk.Scale(window, from_=0, to=100, orient='horizontal', command=preprocess)
border_slider.set(20)

dir_label = tk.Label(window, text='Select working directory:')
dir_entry = tk.Entry(window)
dir_button = tk.Button(window, text='select', command=chose_dir)

color_label = tk.Label(window, text='COLOR:')
red_label = tk.Label(window, text='red:')
green_label = tk.Label(window, text='green:')
blue_label = tk.Label(window, text='blue:')
red_slider = tk.Scale(window, from_=0, to=255, orient='horizontal', command=set_rgb_entry)
green_slider = tk.Scale(window, from_=0, to=255, orient='horizontal', command=set_rgb_entry)
blue_slider = tk.Scale(window, from_=0, to=255, orient='horizontal', command=set_rgb_entry)
rgb_label = tk.Label(window, text='RGB')
hue_label = tk.Label(window, text='HUE')
rgb_entry_content = tk.StringVar()
rgb_entry_content.trace("w", lambda name, index, mode, rgb_entry_content=rgb_entry_content: set_rgb_sliders(rgb_entry.get()))
rgb_entry = tk.Entry(window, textvariable=rgb_entry_content)
hue_entry = tk.Entry(window)

split_lable = tk.Label(window, text='SPLIT')
split_H_label = tk.Label(window, text='Horizontally:')
split_V_label = tk.Label(window, text='Vertically:')
split_H_slider = tk.Scale(window, from_=1, to=10, orient='horizontal', command=preprocess)
split_V_slider = tk.Scale(window, from_=1, to=10, orient='horizontal', command=preprocess)

preview = tk.Label(window, image=imgtk)

text_field = tk.Text(window, height=10, width=45)

confirm_button = tk.Button(window, text='Process', width=25, command=lambda: process(dir_entry.get(), border_slider.get(), [blue_slider.get(), green_slider.get(), red_slider.get()]))








# Place components in grid

# BORDER
border_label.grid(column=1, row=0)
border_slider.grid(column=0, row=1)

dir_label.grid(column=0, row=2)
dir_button.grid(column=1, row=2)
dir_entry.grid(column=2, row=2)

color_label.grid(column=0, row=3)
red_label.grid(column=0, row=4)
green_label.grid(column=0, row=5)
blue_label.grid(column=0, row=6)
red_slider.grid(column=1, row=4)
green_slider.grid(column=1, row=5)
blue_slider.grid(column=1, row=6)
rgb_label.grid(column=0, row=7)
hue_label.grid(column=0, row=8)
rgb_entry.grid(column=1, row=7)
hue_entry.grid(column=1, row=8)

# SPLIT
split_lable.grid(column=1, row=9)
split_H_label.grid(column=0, row=10)
split_V_label.grid(column=0, row=11)
split_H_slider.grid(column=1, row=10)
split_V_slider.grid(column=1, row=11)

# PREVIEW
preview.grid(column=3, row=0)
text_field.grid(column=3, row=8)
confirm_button.grid(column=3, row=11)



window.mainloop()

