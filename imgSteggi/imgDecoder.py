#!/usr/bin/python3

#here we have hardcoded 512 as those were the dimensions of the lena image, but actually you can first save the dimesnions of the image in the stegoimage too

from PIL import Image
import numpy as np

img = Image.open('output.png').convert('RGB')
pixels = np.array(img, dtype=np.uint8)

decoded_bytes = []
byte_accumulator = ''

for row in range(pixels.shape[0]):
    for col in range(pixels.shape[1]):
        for color_channel in range(3):
            bit = pixels[row, col, color_channel] & 0b00000011
            byte_accumulator += f"{bit:02b}"  
            
            if len(byte_accumulator) == 8:
                byte_value = int(byte_accumulator, 2)  
                decoded_bytes.append(byte_value)  
                byte_accumulator = '' 

decoded_array = np.array(decoded_bytes, dtype=np.uint8)
if len(decoded_array) < 512 * 512 * 3:
    raise ValueError("Not enough data to construct a 512x512 RGB image.")

decoded_image_array = decoded_array[:512 * 512 * 3].reshape((512, 512, 3))
decoded_image = Image.fromarray(decoded_image_array, 'RGB')

decoded_image.save('reconstructed_image.png', 'PNG')

print("img saved as 'reconstructed_image.png'.")

