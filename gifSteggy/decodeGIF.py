#!/usr/bin/python3

from PIL import Image, ImageSequence

# Open the encoded GIF file
gif = Image.open('kermit_encoded.gif')

binary_message = ""

# Loop through each frame and extract the LSBs of the pixel indices
for frame in ImageSequence.Iterator(gif):
    frame = frame.convert('P')  # Ensure the frame is in palette mode
    pixels = frame.load()  # Access pixel data
    width, height = frame.size

    for x in range(width):
        for y in range(height):
            # Get the palette index (pixel value)
            palette_index = pixels[x, y]

            # Extract the LSB of the palette index
            bit = palette_index & 1
            binary_message += str(bit)

# Split the binary message into 8-bit chunks
bytes_list = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]

# Convert each 8-bit chunk into a character and stop at the delimiter (00000000)
decoded_message = ""
for byte in bytes_list:
    if byte == "00000000":  # Delimiter for the end of the message
        break
    decoded_message += chr(int(byte, 2))

print("Decoded Message:", decoded_message)

