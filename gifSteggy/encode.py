#!/usr/bin/python3

from PIL import Image
import sys

string = input("Enter text to encode: ")
binary_message = ''.join(format(byte, '08b') for byte in string.encode('utf-8'))
binary_message += '00000000'

gif = Image.open('kermit.gif')
mode = gif.mode
i = 0
for frame_index in range(gif.n_frames):
    gif.seek(frame_index) 

    if gif.mode != 'P':
        frame = gif.convert('P')
    else:
        frame = gif.copy()  

    pixels = frame.load()  
    width, height = frame.size

    for x in range(width):
        for y in range(height):
            if i >= len(binary_message):
                break
            pixel = pixels[x, y]
            bit = int(binary_message[i])
            if bit == 1:
                pixels[x, y] = pixel | 1  
            else:
                pixels[x, y] = pixel & ~1  
            i += 1
        if i >= len(binary_message):
            break

    gif.paste(frame)

gif.save('encodedKermit.gif', save_all=True, loop=0, duration=gif.info.get('duration', 100))
print("message encoded in 'kermit.gif'")

