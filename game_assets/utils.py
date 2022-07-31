import requests
from PIL import Image
import PIL
import io
import numpy as np
from sklearn.cluster import MiniBatchKMeans


def reduce_img_colours(img_path, compression=1, num_colours=5):

    img = Image.open(img_path)

    new_size = (np.array(img.size) * compression).astype(int)

    img_array = np.array(img.resize(new_size))

    pixels = img_array.reshape((-1, 3))

    kmeans = MiniBatchKMeans(num_colours).fit(pixels)

    new_pixels = kmeans.cluster_centers_[kmeans.labels_]

    new_img = new_pixels.reshape((new_size[1], new_size[0], 3))

    print(f'# Old colours: {len(np.unique(pixels, axis = 0))}')
    print(f'# New colours: {num_colours}')

    return new_img


def square_image(pil_img):

    short_side = min(pil_img.size)

    img_width, img_height = pil_img.size
    return pil_img.crop(
        ((img_width - short_side) // 2, (img_height - short_side) // 2,
         (img_width + short_side) // 2, (img_height + short_side) // 2))


def simplify_image(pil_img, num_colors=8):

    img = pil_img.quantize(colors=num_colors, method=2)

    sq_img = square_image(img).resize((128, 128), Image.LANCZOS)

    return sq_img


def get_pil_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except requests.exceptions.RequestException:
        return None
    except PIL.UnidentifiedImageError:
        return None


def save_img(pil_img, caption, destination_folder):

    file_name = f"{destination_folder}/{caption.replace('.', '')}.png"

    pil_img.save(file_name)
