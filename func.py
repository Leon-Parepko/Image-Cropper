import os
import concurrent.futures
import numpy as np
import cv2


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # h, s, v = hue, saturation, value
    cmax = max(r, g, b)  # maximum of r, g, b
    cmin = min(r, g, b)  # minimum of r, g, b
    diff = cmax - cmin  # diff of cmax and cmin.

    if cmax == cmin:
        h = 0

    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360

    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360

    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    if cmax == 0:
        s = 0

    else:
        s = (diff / cmax) * 100

    v = cmax * 100
    return [h, s, v]



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


def block_preview(preview, border_size, split_param, RGB):
    splited_img_arr = split_img(preview, split_param)

    out_img = border(splited_img_arr[0], border_size, RGB)

    # Create horizontal slices from blocks and add them to arr
    horiz_slice_arr = []
    for i in range(0, split_param[0]):
        horiz_slice = border(splited_img_arr[i * split_param[1]], border_size, RGB)
        for j in range(1, split_param[1]):
            horiz_slice = np.concatenate(
                (horiz_slice, border(splited_img_arr[(i * split_param[1]) + j], border_size, RGB)), axis=1)
        horiz_slice_arr.append(horiz_slice)

    if horiz_slice_arr:
        out_img = horiz_slice_arr[0]

    # Combine all horizontal slices
    for i in range(1, len(horiz_slice_arr)):
        out_img = np.concatenate((out_img, horiz_slice_arr[i]), axis=0)

    return out_img


def process(border_param, split_param, color_rgb, in_wd, out_wd, multiproc):
    try:
        os.mkdir(out_wd)
        # GUIFunc.write_to_text_field(gui, f"New output directory was created in: {out_wd}", 'i')
        print(f"New output directory was created in: {out_wd}")

    except Exception:
        pass

    try:
        if not os.path.exists(in_wd):
            return "There is no such directory!"

        file_list = []
        for file in os.listdir(in_wd):
            if file.endswith(".jpg") or file.endswith(".png"):
                # Read file
                file_path = os.path.join(in_wd, file)
                if multiproc:
                    file_list.append([file, file_path])

                if not multiproc:
                    process_operations(file_path, file, border_param, split_param, color_rgb, out_wd)
                    print(f"{file} Done!")

        if multiproc:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = [executor.submit(process_operations, single_file_path[1], single_file_path[0], border_param, split_param, color_rgb, out_wd) for single_file_path in file_list]

                # Write Processing msg
                for f in concurrent.futures.as_completed(results):
                    if multiproc:
                        print(f"{f.result()} Done!")

    except Exception as e:
        return f"Can't process img due to: {e}"


def process_operations(in_file_path, file_name, border_param, split_param, color_rgb, out_wd):
    img = cv2.imread(in_file_path, 1)

    # Split img into the blocks
    splitted_img = split_img(img, split_param)

    # Process
    iter = 1
    for block in splitted_img:
        out_img = border(block, border_param, color_rgb)
        file_splitted = file_name.split(".")

        if len(splitted_img) == 1:
            cv2.imwrite(os.path.join(out_wd, f'{file_splitted[0]}_(res).{file_splitted[1]}'), out_img)
        else:
            cv2.imwrite(os.path.join(out_wd, f'{file_splitted[0]}_(res_{iter}).{file_splitted[1]}'), out_img)

        iter += 1

    return file_name


