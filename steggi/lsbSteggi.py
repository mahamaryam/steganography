from PIL import Image
import numpy as np
import sys
import argparse

def encode_message(image_path, message):

    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '00000000' 
    img = Image.open(image_path).convert('RGB')
    pixels = np.asarray(img) 
    max_bytes = pixels.size // 8
    encoded_pixels = np.array(pixels, dtype=np.uint8)
    
    for i in range(len(binary_message)):
        pixel_index = i // 3  
        color_index = i % 3  
        row = pixel_index // pixels.shape[1]
        col = pixel_index % pixels.shape[1]
        
        bit = int(binary_message[i])
        
        pixel_value = int(encoded_pixels[row, col, color_index])
        
        if bit == 1:
            pixel_value = pixel_value | 1  
        else:
            pixel_value = pixel_value & ~1 
            
        #ensure value stays within uint8 range... wraps around in case of underflow or overflow. (modulus logic).
        pixel_value = np.clip(pixel_value, 0, 255)
        
        encoded_pixels[row, col, color_index] = pixel_value
    
    encoded_image = Image.fromarray(encoded_pixels)
    encoded_image.save(image_path, 'PNG')

def decode_message(image_path):
  
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    
    binary_message = ''
    byte_accumulator = ''
    decoded_bytes = bytearray()
    
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for color_channel in range(3):
                bit = pixels[row, col, color_channel] & 1
                byte_accumulator += str(bit)
                
                if len(byte_accumulator) == 8:
                    byte_value = int(byte_accumulator, 2)
                    if byte_value == 0:  
                        if decoded_bytes: 
                            return decoded_bytes.decode('utf-8')
                        return ""
                    decoded_bytes.append(byte_value)
                    byte_accumulator = ''
    
    if decoded_bytes:
        return decoded_bytes.decode('utf-8')
    return ""

def main():
    if len(sys.argv) < 2:
        print("use -help to see how to use this beauty")
        sys.exit(1)

    if sys.argv[1] == '-e' or sys.argv[1] == "--encode":
        if len(sys.argv) != 4:
            print("Error!!!!!! You need to provide both an image path and a message.")
            print("use like this: python3 lsbSteggi.py -encode <image_path> <message>")
            sys.exit(1)

        image_path = sys.argv[2]
        message = sys.argv[3]
        encode_message(image_path, message)
        print("message encoding is done")

    elif sys.argv[1] == '-d' or sys.argv[1] == "--decode":
        if len(sys.argv) != 3:
            print("Error!!!!! You need to provide an image path for decoding.")
            print("use this wayy:  python3 lsbSteggi.py -decode <image_path>")
            sys.exit(1)

        image_path = sys.argv[2]
        decoded_message = decode_message(image_path)
        print("decoded: ", decoded_message)
     
    elif sys.argv[1] == '-h' or sys.argv[1] == "--help":
    	print("help: python3 claudeSteggi.py --help or -h")
    	print("encode: python3 lsbSteggi.py --encode <image.png> <message> or -e")
    	print("decode: python3 lsbSteggi.py --decode <image.png> or -d")
    
    else:
        print("Invalid-_-")
        print("use this way: python3 lsbSteggi.py -encode <image_path> <message> or -decode <image_path>")

if __name__ == '__main__':
    main()

