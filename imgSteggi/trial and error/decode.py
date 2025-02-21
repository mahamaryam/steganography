#!/usr/bin/python3

from PIL import Image
import numpy as np

def pixels_to_binary(image_array):
    binary_array = np.vectorize(lambda x: format(x, '08b'))(image_array)
    return binary_array

def extract_message(binary_pixels):
    bit_stream = [] 
    to_return = []
    message = ""   
    
    flat_binary_pixels = binary_pixels.flatten()
    
    for binary_pixel in flat_binary_pixels:
        lsb = binary_pixel[-2:]  
        bit_stream.append(lsb)
        to_return.append(lsb)        
        if len(bit_stream) % 8==0:
            byte = ''.join(bit_stream)         
            char = chr(int(byte, 2))           
            if char == "#":                    
                break
            message += char                   
            bit_stream = []                     
    
    return to_return

image = Image.open('output.png') 
image_array = np.array(image)
binary_pixels = pixels_to_binary(image_array)
hidden_message = extract_message(binary_pixels)
bit_array = np.array(hidden_message, dtype=np.uint8)
result_image = Image.fromarray(bit_array)
result_image.save('res.png')

