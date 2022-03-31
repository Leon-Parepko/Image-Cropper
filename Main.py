import numpy as np
import cv2
import tkinter as tk
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









def process ():
    pass




def set_rgb_entry(num):
    rgb_entry.delete(0,"end")
    rgb_entry.insert(0, f'R: {red.get()}  G:{green.get()}  B: {blue.get()}')







window = tk.Tk()

window.title('Counting Seconds')




img = cv2.imread(f'Test/1.jpg')
print(img.shape)
img_preview = resize_to_preview(img, 300)
print(img_preview.shape)
img_preview_b,img_preview_g,img_preview_r = cv2.split(img_preview)
img_preview = cv2.merge((img_preview_r,img_preview_g,img_preview_b))

# Convert the Image object into a TkPhoto object
im = Image.fromarray(img_preview)
imgtk = ImageTk.PhotoImage(image=im)





# Introduce window components
border_label = tk.Label(window, text='Border:')
border = tk.Scale(window, from_=0, to=100,  orient='horizontal')
border.set(20)

folder_label = tk.Label(window, text='Select working directory:')
folder_entry = tk.Entry(window)
folder_button = tk.Button(window, text='select')

color_label = tk.Label(window, text='COLOR:')
red_label = tk.Label(window, text='red:')
green_label = tk.Label(window, text='green:')
blue_label = tk.Label(window, text='blue:')
red = tk.Scale(window, from_=0, to=255,  orient='horizontal', command=set_rgb_entry)
green = tk.Scale(window, from_=0, to=255,  orient='horizontal', command=set_rgb_entry)
blue = tk.Scale(window, from_=0, to=255,  orient='horizontal', command=set_rgb_entry)
rgb_label = tk.Label(window, text='RGB')
hue_label = tk.Label(window, text='HUE')
rgb_entry = tk.Entry(window)
hue_entry = tk.Entry(window)

preview = tk.Label(window, image=imgtk)

confirm_button = tk.Button(window, text='Process', width=25, command=process)








# Place components in grid
border_label.grid(column=0, row=0)
border.grid(column=1, row=0)

folder_label.grid(column=0, row=1)
folder_button.grid(column=1, row=1)
folder_entry.grid(column=2, row=1)

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



window.mainloop()




# for i in range(0, 9):
#     img = cv2.imread(f'not_resized/{i}.jpg', 1)
#     img_s = resize(img, 90)
#
#     back = np.zeros(img.shape, dtype=np.uint8)
#     h, w = img.shape[:2]
#     h1, w1 = img_s.shape[:2]
#
#
#     cx, cy = (h - h1) // 2, (w - w1) // 2
#
#
#     # print(h, w)
#     # print(h1, w1)
#     # print(cx, cy)
#
#     back[cx:h1+cx, cy:w1+cy] = img_s
#
#
# # print(img)
# # # img_noised = img[np.where(img != 0)] - 2
# # # img_noised = img[np.where(img != 0)] + noise.astype(np.uint8)
# # # img_noised += img
# #
# # #
# # # print(img_noised)
#
#
#
#     cv2.imwrite(f'resized/{i}_res.jpg', back)
# # cv2.imshow("Test", back)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
#
# # print(img[0])

