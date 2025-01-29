#!/usr/bin/python3

#modify this code to set the width and height of the image in the beginning so that decoding gets enabled.

from PIL import Image, ImageSequence
import numpy as np

img = Image.open('lena.png').convert('RGB')   
pixels = np.asarray(img)     
encoded_pixels = np.array(pixels, dtype=np.uint8)
binary_pixels = np.vectorize(np.binary_repr)(encoded_pixels, width=8)
bit_string = "".join("".join(pixel.flatten()) for pixel in binary_pixels)
bit_string += '00000000'

gif = Image.open('minnie.gif')
frames = []  # To store modified frames
print(f"Mode of the GIF: {gif.mode}")
i = 0  
binary_length = len(bit_string)

# Loop through each frame and access its pixels
for frame in ImageSequence.Iterator(gif):
    frame = frame.convert('P')  # Ensure the frame is in palette mode
    palette = frame.getpalette()  # Get the palette (list of RGB values)
    pixels = frame.load()  # Access pixel data
    width, height = frame.size

    # Create a copy of the frame to store modified pixel values
    modified_frame = frame.copy()
    modified_pixels = modified_frame.load()

    for x in range(width):
        for y in range(height):
            if i >= binary_length:
                break  # Stop if the entire message is encoded
            
            # Get the original pixel value (palette index)
            original_index = pixels[x, y]

            # Modify the least significant bit (LSB) of the index
            bit = int(bit_string[i])
            modified_index = (original_index & ~1) | bit  # Set LSB to the message bit

            # Save the modified pixel
            modified_pixels[x, y] = modified_index

            i += 1

        if i >= binary_length:
            break  # Stop if the entire message is encoded

    # Add the modified frame to the list, keeping the original palette
    modified_frame.putpalette(palette)  # Reapply the palette to the modified frame
    frames.append(modified_frame)

# Save the modified frames as a new GIF
frames[0].save(
    'encoded.gif',
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=gif.info.get('duration', 100),  # Preserve the original frame duration
    disposal=2  # Clear each frame before displaying the next
)

print("Message encoded and saved in 'encoded.gif'")

