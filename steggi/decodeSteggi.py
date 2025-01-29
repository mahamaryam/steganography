#!/usr/bin/python3

from PIL import Image
import numpy as np

# Function to convert the pixel array to binary
def pixels_to_binary(image_array):
    binary_array = np.vectorize(lambda x: format(x, '08b'))(image_array)
    return binary_array

# Function to extract hidden message
def extract_message(binary_pixels):
    bit_stream = []  # List to store extracted LSBs
    message = ""     # Final message
    
    # Flatten the binary pixel array for easy iteration
    flat_binary_pixels = binary_pixels.flatten()
    
    # Extract the LSBs
    for binary_pixel in flat_binary_pixels:
        lsb = binary_pixel[-1]  # Extract the least significant bit
        bit_stream.append(lsb) # Add LSB to the bit stream
        
        # Check if we have 8 bits (1 byte) to form a character
        if len(bit_stream) % 8==0:
            byte = ''.join(bit_stream)          # Join bits into a byte
            char = chr(int(byte, 2))            # Convert binary to ASCII character
            if char == "#":                     # Terminate at delimiter
                break
            message += char                     # Add character to the message
            bit_stream = []                     # Reset bit stream for next character
    
    return message

# Read the image
image = Image.open('modified_image.png')  # Replace with your image path

# Convert to a NumPy array
image_array = np.array(image)

# Convert the pixel array to binary
binary_pixels = pixels_to_binary(image_array)

# Extract the hidden message
hidden_message = extract_message(binary_pixels)

print(f"Hidden message: {hidden_message}")

