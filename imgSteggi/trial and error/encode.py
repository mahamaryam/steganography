#!/usr/bin/python3

from PIL import Image
import numpy as np
import sys

def get_image_details(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        num_pixels = width * height
    return width, height, num_pixels

def check_image_compatibility(parent, child):
    _, _, pixels_parent = get_image_details(parent)
    _, _, pixels_child = get_image_details(child)

    if pixels_parent >= 2 * pixels_child:
        print("ok")
        return True
    else:
        print("not ok")
        return False

def pixels_to_binary(image_array):
    return np.vectorize(lambda x: format(x, '08b'))(image_array)

def add_delimiter(binary_array):
    delimiter_bin = format(ord('#'), '08b')
    return np.append(binary_array.flatten(), delimiter_bin)

def get_last_two_bits(binary_array):
    bit_pairs = []
    for binary_string in binary_array.flatten():
        pair = binary_string[-2:]
        bit_pairs.extend([int(pair[0]), int(pair[1])])
    return np.array(bit_pairs)

def embed_bits(binary_pixels, bit_array):
    bit_index = 0
    flat_pixels = binary_pixels.flatten()
    new_pixels = []

    for binary_pixel in flat_pixels:
        if bit_index + 1 < len(bit_array):
            modified_pixel = binary_pixel[:-2] + str(bit_array[bit_index]) + str(bit_array[bit_index + 1])
            bit_index += 2
        else:
            modified_pixel = binary_pixel
        new_pixels.append(modified_pixel)
    
    return np.array(new_pixels).reshape(binary_pixels.shape)

def save_image(binary_pixels, output_path):
    pixel_array = np.vectorize(lambda x: int(x, 2))(binary_pixels)
    pixel_array = np.clip(pixel_array, 0, 255).astype(np.uint8)
    Image.fromarray(pixel_array).save(output_path)

def encode_image(parent_path, child_path, output_path):
    if not check_image_compatibility(parent_path, child_path):
        sys.exit(1)

    parent_img = Image.open(parent_path)
    child_img = Image.open(child_path)
    parent_pixels = np.array(parent_img)
    child_pixels = np.array(child_img)
    parent_binary = pixels_to_binary(parent_pixels)
    child_binary = pixels_to_binary(child_pixels)
    child_binary_with_delimiter = add_delimiter(child_binary)
    bits_to_embed = get_last_two_bits(child_binary_with_delimiter)
    embedded_image = embed_bits(parent_binary, bits_to_embed)

    save_image(embedded_image, output_path)
    print("its a successs")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python encode.py parent_image child_image output_image")
        sys.exit(1)
    
    parent_image = sys.argv[1]
    child_image = sys.argv[2]
    output_image = sys.argv[3]
    
    encode_image(parent_image, child_image, output_image)

