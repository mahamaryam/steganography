#!/usr/bin/python3

from PIL import Image, ImageSequence
import numpy as np
gif = Image.open('encoded.gif')

decoded_bytes = []
byte_accumulator=""
binary_message =''

for frame in ImageSequence.Iterator(gif):
    frame = frame.convert('P')  
    pixels = frame.load()  
    width, height = frame.size

    for x in range(width):
        for y in range(height):
            palette_index = pixels[x, y]

            bit = palette_index & 1
            byte_accumulator += f"{bit:01b}"  
            
            if len(byte_accumulator) == 8:
                byte_value = int(byte_accumulator, 2)  
                if byte_value == 0:
                	break
                decoded_bytes.append(byte_value) 
                byte_accumulator = '' 

decoded_array = np.array(decoded_bytes, dtype=np.uint8)
decoded_image_array = decoded_array[:512 * 512 * 3].reshape((512, 512, 3))

decoded_image = Image.fromarray(decoded_image_array, 'RGB')

decoded_image.save('reconstructed_image.png', 'PNG')

print("image is reconstructed and saved as 'reconstructed_image.png'.")



