#!/usr/bin/python3

from PIL import Image
import numpy as np
import sys

def get_image_details(image_path):
    """Get the dimensions and total pixels of an image."""
    with Image.open(image_path) as img:
        width, height = img.size
        num_pixels = width * height
    return width, height, num_pixels

def check_image_compatibility(parent, child):
    """Verify the parent image has enough capacity for the child image."""
    _, _, pixels_parent = get_image_details(parent)
    _, _, pixels_child = get_image_details(child)

    if pixels_parent >= 2 * pixels_child:
        print("Parent image has sufficient capacity.")
        return True
    else:
        print("Parent image does not have sufficient capacity.")
        return False

def pixels_to_binary(image_array):
    """Convert pixel values to 8-bit binary strings."""
    return np.vectorize(lambda x: format(x, '08b'))(image_array)

def add_delimiter(binary_array):
    """Add delimiter '#' to the binary array."""
    delimiter_bin = format(ord('#'), '08b')
    # Flatten and append delimiter
    return np.append(binary_array.flatten(), delimiter_bin)

def get_last_two_bits(binary_array):
    """Extract the last two bits from each binary string."""
    bit_pairs = []
    for binary_string in binary_array.flatten():
        # Extract last two bits and convert to integers
        pair = binary_string[-2:]
        bit_pairs.extend([int(pair[0]), int(pair[1])])
    return np.array(bit_pairs)

def embed_bits(binary_pixels, bit_array):
    """Embed bit array into the least significant bits of binary pixels."""
    bit_index = 0
    flat_pixels = binary_pixels.flatten()
    new_pixels = []

    for binary_pixel in flat_pixels:
        if bit_index + 1 < len(bit_array):
            # Replace last two bits with bits from bit_array
            modified_pixel = binary_pixel[:-2] + str(bit_array[bit_index]) + str(bit_array[bit_index + 1])
            bit_index += 2
        else:
            modified_pixel = binary_pixel
        new_pixels.append(modified_pixel)
    
    return np.array(new_pixels).reshape(binary_pixels.shape)

def save_image(binary_pixels, output_path):
    """Convert binary pixels back to an image and save."""
    # Convert binary strings to integers
    pixel_array = np.vectorize(lambda x: int(x, 2))(binary_pixels)
    # Ensure valid pixel values
    pixel_array = np.clip(pixel_array, 0, 255).astype(np.uint8)
    # Save image
    Image.fromarray(pixel_array).save(output_path)

def encode_image(parent_path, child_path, output_path):
    """Main function to encode one image within another."""
    # Validate images
    if not check_image_compatibility(parent_path, child_path):
        sys.exit(1)

    # Load images
    parent_img = Image.open(parent_path)
    child_img = Image.open(child_path)
    
    # Convert to arrays
    parent_pixels = np.array(parent_img)
    child_pixels = np.array(child_img)

    # Convert to binary
    parent_binary = pixels_to_binary(parent_pixels)
    child_binary = pixels_to_binary(child_pixels)

    # Add delimiter to child image data
    child_binary_with_delimiter = add_delimiter(child_binary)

    # Get bit array to embed
    bits_to_embed = get_last_two_bits(child_binary_with_delimiter)

    # Embed bits
    embedded_image = embed_bits(parent_binary, bits_to_embed)

    # Save result
    save_image(embedded_image, output_path)
    print(f"Successfully encoded image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python encode.py parent_image child_image output_image")
        sys.exit(1)
    
    parent_image = sys.argv[1]
    child_image = sys.argv[2]
    output_image = sys.argv[3]
    
    encode_image(parent_image, child_image, output_image)

