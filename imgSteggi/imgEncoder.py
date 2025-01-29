#!/usr/bin/python3

#modify this code to set the width and height of the image in the beginning so that decoding gets enabled.

from PIL import Image
import numpy as np
# Load the images
img = Image.open('parent.png').convert('RGB')   
parent_pixels = np.asarray(img)     
parent_encoded_pixels = np.array(parent_pixels, dtype=np.uint8)
img2 = Image.open('child.png').convert('RGB')   
child_pixels = np.asarray(img2)     
child_encoded_pixels = np.array(child_pixels, dtype=np.uint8)

# Convert child_encoded_pixels to binary strings
child_binary_pixels = np.vectorize(np.binary_repr)(child_encoded_pixels, width=8)

# Convert binary strings into a single sequence of characters without a delimiter
bit_string = "".join("".join(pixel.flatten()) for pixel in child_binary_pixels)

# Add termination sequence (e.g., '00000000') at the end
bit_string += '00000000'

j = 0
# Encode message bit by bit
while j*2 < len(bit_string):  # Changed condition to check bit_string bounds
    pixel_index = j // 3  # Get the pixel index
    color_index = j % 3   # Get the color channel index (R, G, B)
    row = pixel_index // parent_pixels.shape[1]
    col = pixel_index % parent_pixels.shape[1]
    
    # Get the bit to encode
    bit1 = int(bit_string[j*2])  # First bit, using j*2
    bit2 = int(bit_string[j*2 + 1]) if j*2 + 1 < len(bit_string) else 0  # Second bit, using j*2+1
    
    # Get current pixel value
    pixel_value = int(parent_encoded_pixels[row, col, color_index])
    
    # Clear last two bits and set new ones
    pixel_value = (pixel_value & 0b11111100) | (bit1 << 1) | bit2
            
    # Ensure value stays within uint8 range
    pixel_value = np.clip(pixel_value, 0, 255)
        
    # Store modified pixel value
    parent_encoded_pixels[row, col, color_index] = pixel_value
    
    j += 1
        
# Save the encoded image
parent_encoded_image = Image.fromarray(parent_encoded_pixels)
parent_encoded_image.save('output.png', 'PNG')
