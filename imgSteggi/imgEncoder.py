#!/usr/bin/python3

#modify this code to set the width and height of the image in the beginning so that decoding gets enabled.

from PIL import Image
import numpy as np
img = Image.open('parent.png').convert('RGB')   
parent_pixels = np.asarray(img)     
parent_encoded_pixels = np.array(parent_pixels, dtype=np.uint8)
img2 = Image.open('child.png').convert('RGB')   
child_pixels = np.asarray(img2)     
child_encoded_pixels = np.array(child_pixels, dtype=np.uint8)

child_binary_pixels = np.vectorize(np.binary_repr)(child_encoded_pixels, width=8)
bit_string = "".join("".join(pixel.flatten()) for pixel in child_binary_pixels)
bit_string += '00000000'

j = 0
while j*2 < len(bit_string):  
    pixel_index = j // 3  
    color_index = j % 3   
    row = pixel_index // parent_pixels.shape[1]
    col = pixel_index % parent_pixels.shape[1]
    
    bit1 = int(bit_string[j*2])  
    bit2 = int(bit_string[j*2 + 1]) if j*2 + 1 < len(bit_string) else 0  
    
    pixel_value = int(parent_encoded_pixels[row, col, color_index])
    pixel_value = (pixel_value & 0b11111100) | (bit1 << 1) | bit2
    pixel_value = np.clip(pixel_value, 0, 255)
    parent_encoded_pixels[row, col, color_index] = pixel_value
    
    j += 1
        
parent_encoded_image = Image.fromarray(parent_encoded_pixels)
parent_encoded_image.save('output.png', 'PNG')
