from mutagen.mp4 import MP4
import base64
import shutil
import os
from PIL import Image
import numpy as np

def hide_image(mp4_path, image_path, output_path):
    img = Image.open(image_path).convert('RGB')
    pixels = np.asarray(img, dtype=np.uint8)
    height, width, channels = pixels.shape
    flattened_pixels = pixels.flatten()

    header = f"{height}.{width}.{channels}#"
    pixel_data = ",".join(map(str, flattened_pixels))
    image_data = header + pixel_data

    base64_data = base64.b64encode(image_data.encode('utf-8')).decode('utf-8')

    shutil.copy2(mp4_path, output_path)

    try:
        video = MP4(output_path)
        video["\xa9day"] = base64_data
        video.save()
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        raise Exception(f"fail")

def retrieve_image(mp4_path):
    if not os.path.exists(mp4_path):
        raise FileNotFoundError(f"file not found")

    video = MP4(mp4_path)

    if "\xa9day" not in video:
        raise ValueError("No hidden image found")

    encoded_data = video["\xa9day"][0]
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    header, pixel_data = decoded_data.split("#", 1)
    height, width, channels = map(int, header.split("."))
    pixel_values = np.fromstring(pixel_data, dtype=np.uint8, sep=",")

    image_array = pixel_values.reshape((height, width, channels))
    return Image.fromarray(image_array)

hide_image('v1.mp4', 'image.jpeg', 'output.mp4')
retrieved_image = retrieve_image('output.mp4')
retrieved_image.show() 

