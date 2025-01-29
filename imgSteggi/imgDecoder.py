#!/usr/bin/python3

#here we have hardcoded 512 as those were the dimensions of the lena image, but actually you can first save the dimesnions of the image in the stegoimage too

from PIL import Image
import numpy as np

# Load the image and convert it to numpy array
img = Image.open('output.png').convert('RGB')
pixels = np.array(img, dtype=np.uint8)

# Initialize an empty list to store the decoded bytes
decoded_bytes = []
byte_accumulator = ''

# Iterate over the pixels and extract 2 LSBs from each color channel
for row in range(pixels.shape[0]):
    for col in range(pixels.shape[1]):
        for color_channel in range(3):
            # Extract 2 LSBs
            bit = pixels[row, col, color_channel] & 0b00000011
            byte_accumulator += f"{bit:02b}"  # Append 2 bits as a string
            
            # If we have accumulated 8 bits, process them
            if len(byte_accumulator) == 8:
                byte_value = int(byte_accumulator, 2)  # Convert to an integer
                decoded_bytes.append(byte_value)  # Add to the decoded bytes list
                byte_accumulator = ''  # Reset accumulator

# Convert the list of decoded bytes into a numpy array
decoded_array = np.array(decoded_bytes, dtype=np.uint8)

# Ensure the array has enough bytes to form a 512x512 RGB image
if len(decoded_array) < 512 * 512 * 3:
    raise ValueError("Not enough data to construct a 512x512 RGB image.")

# Reshape the array into a 3D array (height, width, color channels)
decoded_image_array = decoded_array[:512 * 512 * 3].reshape((512, 512, 3))

# Create an image from the decoded array
decoded_image = Image.fromarray(decoded_image_array, 'RGB')

# Save the reconstructed image
decoded_image.save('reconstructed_image.png', 'PNG')

print("Image reconstructed and saved as 'reconstructed_image.png'.")

