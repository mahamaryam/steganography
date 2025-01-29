from mutagen.mp4 import MP4
import base64
import shutil
import os
from PIL import Image
import numpy as np

def hide_image(mp4_path, image_path, output_path):
    """Hide image data in MP4 metadata."""
    # Load and process the image
    img = Image.open(image_path).convert('RGB')
    pixels = np.asarray(img, dtype=np.uint8)
    height, width, channels = pixels.shape
    flattened_pixels = pixels.flatten()

    # Prepare the data string
    header = f"{height}.{width}.{channels}#"
    pixel_data = ",".join(map(str, flattened_pixels))
    image_data = header + pixel_data
    image_data += image_data
    image_data += image_data
    image_data += image_data
    image_data += image_data
    image_data += image_data
    image_data += image_data
    image_data += image_data #8.

    # Convert to Base64
    base64_data = base64.b64encode(image_data.encode('utf-8')).decode('utf-8')

    # Copy the MP4 file
    shutil.copy2(mp4_path, output_path)

    # Embed the Base64 data into the MP4 metadata
    try:
        video = MP4(output_path)
        video["\xa9cmt"] = base64_data
        video.save()
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        raise Exception(f"Failed to hide image: {str(e)}")

def retrieve_image(mp4_path):
    """Extract hidden image data from MP4 metadata."""
    if not os.path.exists(mp4_path):
        raise FileNotFoundError(f"File not found: {mp4_path}")

    video = MP4(mp4_path)

    if "\xa9cmt" not in video:
        raise ValueError("No hidden image found")

    encoded_data = video["\xa9cmt"][0]
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')

    # Extract header and pixel data
    header, pixel_data = decoded_data.split("#", 1)
    height, width, channels = map(int, header.split("."))
    pixel_values = np.fromstring(pixel_data, dtype=np.uint8, sep=",")

    # Reshape into the original image dimensions
    image_array = pixel_values.reshape((height, width, channels))
    return Image.fromarray(image_array)

# Example usage
hide_image('v1.mp4', 'lena.png', 'v3.mp4')


