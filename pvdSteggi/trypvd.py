from PIL import Image
import numpy as np

#function to calculate range for a given difference
def calculate_range(diff):
    ranges = [(0, 7), (8, 15), (16, 31), (32, 63), (64, 127), (128, 255)]
    for i, (low, high) in enumerate(ranges):
        if low <= diff <= high:
            return i + 1, low, high 
    return 0, 0, 0

def pvd_encode(image_path, message, output_path):
    image = Image.open(image_path).convert("L") 
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    binary_message = ''.join(f"{ord(c):08b}" for c in message) + "11111111"
    binary_index = 0
    
    for i in range(0, len(flat_pixels) - 1, 2):
        if binary_index >= len(binary_message):
            break
        
        p1, p2 = flat_pixels[i], flat_pixels[i + 1]
        diff = abs(p1 - p2)
        
        num_bits, low, high = calculate_range(diff)
        if num_bits == 0:
            continue
        
        bits_to_embed = binary_message[binary_index:binary_index + num_bits]
        if len(bits_to_embed) < num_bits:
            bits_to_embed = bits_to_embed.ljust(num_bits, "0")
        
        binary_index += num_bits
        
        new_diff = low + int(bits_to_embed, 2)
        new_diff = max(low, min(new_diff, high))
        
        if p1 > p2:
            p1 = p1 - (diff - new_diff)
        else:
            p2 = p2 - (diff - new_diff)
        
        flat_pixels[i], flat_pixels[i + 1] = p1, p2
    
    encoded_pixels = flat_pixels.reshape(pixels.shape)
    encoded_image = Image.fromarray(encoded_pixels.astype(np.uint8))
    encoded_image.save(output_path)

def pvd_decode(encoded_image_path):
    image = Image.open(encoded_image_path).convert("L") 
    pixels = np.array(image)
    
    flat_pixels = pixels.flatten()
    
    binary_message = ""
    
    for i in range(0, len(flat_pixels) - 1, 2):
        p1, p2 = flat_pixels[i], flat_pixels[i + 1]
        diff = abs(p1 - p2)
        
        num_bits, low, high = calculate_range(diff)
        if num_bits == 0:
            continue
        
        embedded_bits = bin(diff - low)[2:].zfill(num_bits)
        binary_message += embedded_bits
        
        if binary_message.endswith("11111111"):
            binary_message = binary_message[:-8]
            break
    
    message = "".join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
    return message

if __name__ == "__main__":
    input_image = "image.png"
    output_image = "encoded_image.png"
    hidden_message = "hello world"
    
    pvd_encode(input_image, hidden_message, output_image)
    print(f"message is encoded into {output_image}")
    
    decoded_message = pvd_decode(output_image)
    print(f"decoded message: {decoded_message}")

