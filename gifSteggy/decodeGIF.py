#!/usr/bin/python3

from PIL import Image, ImageSequence

gif = Image.open('kermit_encoded.gif')
binary_message = ""

for frame in ImageSequence.Iterator(gif):
    frame = frame.convert('P') 
    pixels = frame.load()  
    width, height = frame.size

    for x in range(width):
        for y in range(height):
            palette_index = pixels[x, y]
            bit = palette_index & 1
            binary_message += str(bit)

bytes_list = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
decoded_message = ""
for byte in bytes_list:
    if byte == "00000000": 
        break
    decoded_message += chr(int(byte, 2))

print("Decoded Message:", decoded_message)

