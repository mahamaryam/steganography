import cv2
import numpy as np

def encode_message(image_path, secret_message, output_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Image at {image_path} not found.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect edges using Canny
    edges = cv2.Canny(gray, 100, 200)
    
    # Convert secret message to binary
    secret_bin = ''.join(format(ord(c), '08b') for c in secret_message) + '1111111111111110'  # End marker
    binary_index = 0

    # Encode secret message in the edges
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i, j] == 255:  # Edge pixel
                if binary_index < len(secret_bin):
                    # Get the blue channel pixel value
                    blue_pixel_value = image[i, j, 0]
                    # Ensure the value is within 0 to 255
                    new_blue_value = (blue_pixel_value & ~1) | int(secret_bin[binary_index])
                    new_blue_value = max(0, min(255, new_blue_value))  # Clamp to uint8 range
                    # Assign the modified blue value
                    image[i, j, 0] = new_blue_value
                    binary_index += 1

    # Save the image with the hidden message
    cv2.imwrite(output_path, image)
    print(f"Message encoded in {output_path}")

# Example usage
encode_message("image.png", "SecretMessage", "encoded_image.png")

