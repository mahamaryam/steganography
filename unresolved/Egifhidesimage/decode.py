#!/usr/bin/python3

from PIL import Image, ImageSequence
import numpy as np
# Open the encoded GIF file
gif = Image.open('encoded.gif')

decoded_bytes = []
byte_accumulator=""
binary_message =''

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
            byte_accumulator += f"{bit:01b}"  # Append 2 bits as a string
            
            # If we have accumulated 8 bits, process them
            if len(byte_accumulator) == 8:
                byte_value = int(byte_accumulator, 2)  # Convert to an integer
                if byte_value == 0:
                	break
                decoded_bytes.append(byte_value)  # Add to the decoded bytes list
                byte_accumulator = ''  # Reset accumulator

# Convert the list of decoded bytes into a numpy array
decoded_array = np.array(decoded_bytes, dtype=np.uint8)


# Reshape the array into a 3D array (height, width, color channels)
decoded_image_array = decoded_array[:512 * 512 * 3].reshape((512, 512, 3))

# Create an image from the decoded array
decoded_image = Image.fromarray(decoded_image_array, 'RGB')

# Save the reconstructed image
decoded_image.save('reconstructed_image.png', 'PNG')

print("Image reconstructed and saved as 'reconstructed_image.png'.")



