import os

import numpy as np
import cv2
import tkinter as tk
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
    rgb_entry.delete(0,"end")
    rgb_entry.insert(0, f'R: {red.get()}  G: {green.get()}  B: {blue.get()}')


def set_rgb_sliders(content):
    print(content)
    #
    # red.set()
    # green.set()
    # blue.set()

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
border_label = tk.Label(window, text='Border:')
border = tk.Scale(window, from_=0, to=100,  orient='horizontal', command=preprocess)
border.set(20)

dir_label = tk.Label(window, text='Select working directory:')
dir_entry = tk.Entry(window)
dir_button = tk.Button(window, text='select', command=chose_dir)

color_label = tk.Label(window, text='COLOR:')
red_label = tk.Label(window, text='red:')
green_label = tk.Label(window, text='green:')
blue_label = tk.Label(window, text='blue:')
red = tk.Scale(window, from_=0, to=255,  orient='horizontal', command=set_rgb_entry)
green = tk.Scale(window, from_=0, to=255,  orient='horizontal', command=set_rgb_entry)
blue = tk.Scale(window, from_=0, to=255,  orient='horizontal', command=set_rgb_entry)
rgb_label = tk.Label(window, text='RGB')
hue_label = tk.Label(window, text='HUE')
rgb_entry_content = tk.StringVar()
rgb_entry_content.trace("w", lambda name, index, mode, rgb_entry_content=rgb_entry_content: set_rgb_sliders(rgb_entry_content))
rgb_entry = tk.Entry(window, textvariable=rgb_entry_content)
hue_entry = tk.Entry(window)

preview = tk.Label(window, image=imgtk)

text_field = tk.Text(window, height=10, width=45)

confirm_button = tk.Button(window, text='Process', width=25, command=lambda: process(dir_entry.get(), border.get(), [blue.get(), green.get(), red.get()]))








# Place components in grid
border_label.grid(column=0, row=0)
border.grid(column=1, row=0)

dir_label.grid(column=0, row=1)
dir_button.grid(column=1, row=1)
dir_entry.grid(column=2, row=1)

color_label.grid(column=1, row=2, sticky='w')
red_label.grid(column=0, row=3)
green_label.grid(column=0, row=4)
blue_label.grid(column=0, row=5)
red.grid(column=1, row=3)
green.grid(column=1, row=4)
blue.grid(column=1, row=5)
rgb_label.grid(column=0, row=6)
hue_label.grid(column=0, row=7)
rgb_entry.grid(column=1, row=6)
hue_entry.grid(column=1, row=7)
confirm_button.grid(column=3, row=10)

preview.grid(column=3, row=0)
text_field.grid(column=3, row=7)



window.mainloop()

