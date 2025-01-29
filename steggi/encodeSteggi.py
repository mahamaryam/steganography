#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np

# Function to add a delimiter to a string
def add_delimiter(string):
    string += "#"
    return string

# Function to convert a string to bits
def string_to_bits(input_string):
    binary_list = [format(ord(char), '08b') for char in input_string]
    bit_array = [bit for binary in binary_list for bit in binary]
    return bit_array

# Function to convert the pixel array to binary
def pixels_to_binary(image_array):
    binary_array = np.vectorize(lambda x: format(x, '08b'))(image_array)
    return binary_array

# Function to embed the bit array into the binary pixels
def embed_bits(binary_pixels, bit_array):
    bit_index = 0
    flat_pixels = binary_pixels.flatten()  # Flatten to simplify iteration
    new_pixels = []

    for binary_pixel in flat_pixels:
        if bit_index < len(bit_array):
            # Replace the least significant bit with the next bit from bit_array
            modified_pixel = binary_pixel[:-1] + bit_array[bit_index]
            bit_index += 1
        else:
            modified_pixel = binary_pixel
        new_pixels.append(modified_pixel)
    
    # Reshape back to original shape
    new_pixels = np.array(new_pixels).reshape(binary_pixels.shape)
    return new_pixels

# Function to save binary pixel values using Pillow
def save_binary_pixels(binary_pixels, output_path):
    # Convert binary strings back to integers
    pixel_array = np.vectorize(lambda x: int(x, 2))(binary_pixels)

    # Ensure pixel values are valid for image formats (e.g., [0, 255])
    pixel_array = np.clip(pixel_array, 0, 255).astype(np.uint8)

    # Convert the NumPy array back to a Pillow image
    new_image = Image.fromarray(pixel_array)

    # Save the image using Pillow
    new_image.save(output_path)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <input_image_path> <output_image_path> <message>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]
    message = sys.argv[3]

    # Read the image
    image = Image.open(input_image_path)

    # Convert to a NumPy array
    image_array = np.array(image)

    # Convert the pixel array to binary
    binary_pixels = pixels_to_binary(image_array)

    # Add a delimiter to the string and convert it to bits
    message_with_delimiter = add_delimiter(message)
    bit_array = string_to_bits(message_with_delimiter)

    # Embed the bit array into the binary pixels
    new_binary_pixels = embed_bits(binary_pixels, bit_array)

    # Save the modified binary pixel array as an image
    save_binary_pixels(new_binary_pixels, output_image_path)

    print(f"Message encoded and saved in '{output_image_path}'")

if __name__ == "__main__":
    main()

