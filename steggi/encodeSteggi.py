#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np

def add_delimiter(string):
    string += "#"
    return string

def string_to_bits(input_string):
    binary_list = [format(ord(char), '08b') for char in input_string]
    bit_array = [bit for binary in binary_list for bit in binary]
    return bit_array

def pixels_to_binary(image_array):
    binary_array = np.vectorize(lambda x: format(x, '08b'))(image_array)
    return binary_array

def embed_bits(binary_pixels, bit_array):
    bit_index = 0
    flat_pixels = binary_pixels.flatten()  
    new_pixels = []

    for binary_pixel in flat_pixels:
        if bit_index < len(bit_array):
            modified_pixel = binary_pixel[:-1] + bit_array[bit_index]
            bit_index += 1
        else:
            modified_pixel = binary_pixel
        new_pixels.append(modified_pixel)
    
    new_pixels = np.array(new_pixels).reshape(binary_pixels.shape)
    return new_pixels

def save_binary_pixels(binary_pixels, output_path):
    pixel_array = np.vectorize(lambda x: int(x, 2))(binary_pixels)
    pixel_array = np.clip(pixel_array, 0, 255).astype(np.uint8)
    new_image = Image.fromarray(pixel_array)
    new_image.save(output_path)

def main():
    if len(sys.argv) != 4:
        print("python3 script.py <input_image_path> <output_image_path> <message>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]
    message = sys.argv[3]

    image = Image.open(input_image_path)
    image_array = np.array(image)
    binary_pixels = pixels_to_binary(image_array)
    message_with_delimiter = add_delimiter(message)
    bit_array = string_to_bits(message_with_delimiter)
    new_binary_pixels = embed_bits(binary_pixels, bit_array)
    save_binary_pixels(new_binary_pixels, output_image_path)

    print(f"message saved in '{output_image_path}'")

if __name__ == "__main__":
    main()

