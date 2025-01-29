#!/usr/bin/python3

from PIL import Image, ImageSequence

# Open the GIF file
string = input("Enter text to encode: ")
binary_message = ''.join(format(byte, '08b') for byte in string.encode('utf-8'))
binary_message += '00000000'  # Add delimiter to mark the end of the message

gif = Image.open('kermit.gif')
frames = []  # To store modified frames

i = 0  # To track the bit position in the binary message
binary_length = len(binary_message)

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
            bit = int(binary_message[i])
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
    'kermit_encoded.gif',
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=gif.info.get('duration', 100),  # Preserve the original frame duration
    disposal=2  # Clear each frame before displaying the next
)

print("Message encoded and saved in 'kermit_encoded.gif'")

