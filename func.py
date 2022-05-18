
import numpy as np
import cv2


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


def border(img, border, color):
    img_b = resize(img, 100 + border)

    back = np.full(img_b.shape, color, dtype=np.uint8)
    h, w = img_b.shape[:2]
    h1, w1 = img.shape[:2]

    cx, cy = (h - h1) // 2, (w - w1) // 2

    back[cx:h1 + cx, cy:w1 + cy] = img

    return back




