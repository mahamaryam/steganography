#!/usr/bin/python3

from PIL import Image
import sys

# Open the GIF file
string = input("Enter text to encode: ")
binary_message = ''.join(format(byte, '08b') for byte in string.encode('utf-8'))
binary_message += '00000000'  # Add delimiter to mark end of message, can use other delimiters too such as # or $.

gif = Image.open('kermit.gif')
mode = gif.mode
# GIF mode is palette

i = 0
# Loop through each frame and access its pixels
for frame_index in range(gif.n_frames):
    gif.seek(frame_index)  # Go to the current frame

    # Convert frame to 'P' mode if necessary
    if gif.mode != 'P':
        frame = gif.convert('P')
    else:
        frame = gif.copy()  # Copy the current frame to modify

    pixels = frame.load()  # Access pixel data
    width, height = frame.size

    # Modify pixels to encode the message
    for x in range(width):
        for y in range(height):
            if i >= len(binary_message):
                break
            pixel = pixels[x, y]
            bit = int(binary_message[i])
            if bit == 1:
                pixels[x, y] = pixel | 1  # Set LSB to 1
            else:
                pixels[x, y] = pixel & ~1  # Set LSB to 0
            i += 1
        if i >= len(binary_message):
            break

    # Replace the modified frame in the original GIF
    gif.paste(frame)

# Save the modified GIF
gif.save('encodedKermit.gif', save_all=True, loop=0, duration=gif.info.get('duration', 100))

print("Message encoded directly in the original file 'kermit.gif'")

