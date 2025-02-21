#!/usr/bin/python3

#modify this code to set the width and height of the image in the beginning so that decoding gets enabled.
#doesn't work yete
from PIL import Image, ImageSequence
import numpy as np

img = Image.open('lena.png').convert('RGB')   
pixels = np.asarray(img)     
encoded_pixels = np.array(pixels, dtype=np.uint8)
binary_pixels = np.vectorize(np.binary_repr)(encoded_pixels, width=8)
bit_string = "".join("".join(pixel.flatten()) for pixel in binary_pixels)
bit_string += '00000000'

gif = Image.open('minnie.gif')
frames = []  
print(f"Mode of the GIF: {gif.mode}")
i = 0  
binary_length = len(bit_string)

for frame in ImageSequence.Iterator(gif):
    frame = frame.convert('P') 
    palette = frame.getpalette()  
    pixels = frame.load()  
    width, height = frame.size

    modified_frame = frame.copy()
    modified_pixels = modified_frame.load()

    for x in range(width):
        for y in range(height):
            if i >= binary_length:
                break 
            
            original_index = pixels[x, y]

            bit = int(bit_string[i])
            modified_index = (original_index & ~1) | bit 

            modified_pixels[x, y] = modified_index

            i += 1

        if i >= binary_length:
            break

    modified_frame.putpalette(palette)  
    frames.append(modified_frame)

frames[0].save(
    'encoded.gif',
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=gif.info.get('duration', 100),  # Preserve the original frame duration
    disposal=2  # Clear each frame before displaying the next
)

print("encoded and saved in 'encoded.gif'")

