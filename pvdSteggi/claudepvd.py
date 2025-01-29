from PIL import Image
import numpy as np

# Function to calculate range for a given difference
def calculate_range(diff):
    ranges = [(0, 7), (8, 15), (16, 31), (32, 63), (64, 127), (128, 255)]
    for i, (low, high) in enumerate(ranges):
        if low <= diff <= high:
            return i + 1, low, high  # i+1 determines the number of bits to embed
    return 0, 0, 0

# Encoding function
def pvd_encode(image_path, message, output_path):
    # Load the image
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    pixels = np.array(image)
    
    # Flatten the pixels for easier pair processing
    flat_pixels = pixels.flatten()
    
    # Convert message to binary and append a terminator
    binary_message = ''.join(f"{ord(c):08b}" for c in message) + "11111111"
    binary_index = 0
    
    # Encode binary data into pixel pairs
    for i in range(0, len(flat_pixels) - 1, 2):
        if binary_index >= len(binary_message):
            break
        
        p1, p2 = flat_pixels[i], flat_pixels[i + 1]
        diff = abs(p1 - p2)
        
        # Calculate the range for the difference
        num_bits, low, high = calculate_range(diff)
        if num_bits == 0:
            continue
        
        # Extract the bits to embed
        bits_to_embed = binary_message[binary_index:binary_index + num_bits]
        if len(bits_to_embed) < num_bits:
            bits_to_embed = bits_to_embed.ljust(num_bits, "0")
        
        binary_index += num_bits
        
        # Calculate new difference
        new_diff = low + int(bits_to_embed, 2)
        new_diff = max(low, min(new_diff, high))
        
        # Adjust pixel values to match the new difference
        if p1 > p2:
            p1 = p1 - (diff - new_diff)
        else:
            p2 = p2 - (diff - new_diff)
        
        # Update pixel values
        flat_pixels[i], flat_pixels[i + 1] = p1, p2
    
    # Reshape and save the encoded image
    encoded_pixels = flat_pixels.reshape(pixels.shape)
    encoded_image = Image.fromarray(encoded_pixels.astype(np.uint8))
    encoded_image.save(output_path)

# Decoding function
def pvd_decode(encoded_image_path):
    # Load the encoded image
    image = Image.open(encoded_image_path).convert("L")  # Convert to grayscale
    pixels = np.array(image)
    
    # Flatten the pixels for easier pair processing
    flat_pixels = pixels.flatten()
    
    binary_message = ""
    
    # Decode the binary data from pixel pairs
    for i in range(0, len(flat_pixels) - 1, 2):
        p1, p2 = flat_pixels[i], flat_pixels[i + 1]
        diff = abs(p1 - p2)
        
        # Calculate the range for the difference
        num_bits, low, high = calculate_range(diff)
        if num_bits == 0:
            continue
        
        # Extract the bits from the difference
        embedded_bits = bin(diff - low)[2:].zfill(num_bits)
        binary_message += embedded_bits
        
        # Check for the terminator
        if binary_message.endswith("11111111"):
            binary_message = binary_message[:-8]
            break
    
    # Convert binary message to text
    message = "".join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
    return message

# Example usage
if __name__ == "__main__":
    # Input and output paths
    input_image = "image.png"
    output_image = "encoded_image.png"
    hidden_message = "Hello, PVD!"
    
    # Encoding
    pvd_encode(input_image, hidden_message, output_image)
    print(f"Message encoded into {output_image}")
    
    # Decoding
    decoded_message = pvd_decode(output_image)
    print(f"Decoded message: {decoded_message}")

