import cv2
import numpy as np

def encode_message(image_path, secret_message, output_path):
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Image at {image_path} not found.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    secret_bin = ''.join(format(ord(c), '08b') for c in secret_message) + '1111111111111110'  # End marker
    binary_index = 0
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i, j] == 255:  
                if binary_index < len(secret_bin):
                    blue_pixel_value = image[i, j, 0]
                    new_blue_value = (blue_pixel_value & ~1) | int(secret_bin[binary_index])
                    new_blue_value = max(0, min(255, new_blue_value))  # Clamp to uint8 range
                    image[i, j, 0] = new_blue_value
                    binary_index += 1

    cv2.imwrite(output_path, image)
    print(f"Message encoded in {output_path}")

encode_message("image.png", "mm is a brilliant girl", "encoded_image.png")
