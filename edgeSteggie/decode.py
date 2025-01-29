def decode_message(encoded_image_path):
    # Load the encoded image
    encoded_image = cv2.imread(encoded_image_path)
    gray = cv2.cvtColor(encoded_image, cv2.COLOR_BGR2GRAY)
    
    # Detect edges
    edges = cv2.Canny(gray, 100, 200)

    # Extract binary data from the edges
    secret_bin = ""
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i, j] == 255:  # Edge pixel
                secret_bin += str(encoded_image[i, j, 0] & 1)

    # Convert binary data to text
    secret_message = ""
    for i in range(0, len(secret_bin), 8):
        byte = secret_bin[i:i+8]
        if byte == "11111110":  # End marker
            break
        secret_message += chr(int(byte, 2))

    print("Decoded message:", secret_message)
    return secret_message

# Example usage
string = decode_message("encoded_image.png")
print(string)
