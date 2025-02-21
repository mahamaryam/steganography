def decode_message(encoded_image_path):
    encoded_image = cv2.imread(encoded_image_path)
    gray = cv2.cvtColor(encoded_image, cv2.COLOR_BGR2GRAY)
    # using inbuilt canny edge detection algo
    edges = cv2.Canny(gray, 100, 200)
    secret_bin = ""
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i, j] == 255:  # Edge pixel
                secret_bin += str(encoded_image[i, j, 0] & 1)

    secret_message = ""
    for i in range(0, len(secret_bin), 8):
        byte = secret_bin[i:i+8]
        if byte == "11111110":
            break
        secret_message += chr(int(byte, 2))

    print("Decoded message:", secret_message)
    return secret_message
string = decode_message("encoded_image.png")
print(string)
