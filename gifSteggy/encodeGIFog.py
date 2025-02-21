#!/usr/bin/python3

from PIL import Image, ImageSequence

string = input("Enter text to encode: ")
binary_message = ''.join(format(byte, '08b') for byte in string.encode('utf-8'))
binary_message += '00000000'  

gif = Image.open('kermit.gif')
frames = []  
i = 0 
binary_length = len(binary_message)
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
            bit = int(binary_message[i])
            modified_index = (original_index & ~1) | bit  
            modified_pixels[x, y] = modified_index

            i += 1

        if i >= binary_length:
            break 

    modified_frame.putpalette(palette)  
    frames.append(modified_frame)

frames[0].save(
    'kermit_encoded.gif',
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=gif.info.get('duration', 100), 
    disposal=2 
)
