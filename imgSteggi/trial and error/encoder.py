from PIL import Image
import numpy as np
import sys
import argparse

def encode_message(image_path, message):

    #convert message to binary, encoding it properly as UTF-8, why UTF-8? as it provides universality and is widely used. decimal ascii 65 for A and 0x41 for A. the things we've done already.
    #read it this way, that for every byte in message that we receievd in function paramters, encode it in utf-8, means if we have A in out message only then A.encode=65 in decimal or 0x41 in hex
    #after message encoding in utf-8, format it into bytes of 8 bits and then join all the bits together.
    #message.encode: Encodes the message string into a sequence of bytes using UTF-8 encoding.
    #format(byte,'08b'): Converts each byte into an 8-bit binary string. like A = 1000001
    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '00000000'  #add delimiter to mark end of message, can use other delimiters too such as # or $.
    
    #open image in RGB as we want to preserve image colours and convert to numpy array
    #shape of img will result in 3d array having height width and number of channels that will be 3(RGB).
    img = Image.open(image_path).convert('RGB')
    #here we have used np.asarray because it sort of becomes a pointer to the actual array that is img and no additional array is made. it references img. had we used np.array then a copy
    #of the array would've been made, changes made in the numpy array wouldn't have been visible in the original array, but with asarray, changes made in pixels will effect img too.
    #so it is a sort of pointer to an already exisiting array(img). this pointer is made using the np.asarray that also behaves exactly like an array. 
    pixels = np.asarray(img) 
    
    
    #this is purely optional 
    #check if image can hold the message
    max_bytes = pixels.size // 8
    message_size = len(binary_message)
    if message_size > max_bytes:
        raise ValueError(f"no way")
    
    #Pixel values in images are typically stored as 8-bit unsigned integers (uint8), representing values in the range [0, 255].
#Ensuring the data type explicitly with dtype=np.uint8 prevents issues during manipulation, such as overflow or invalid values.
#When modifying the least significant bit (LSB) of pixel values, it's crucial to stay within the valid range of 0–255.
#Specifying dtype=np.uint8 ensures that operations like bitwise manipulation (&, |) are applied correctly and remain valid for image data.
#Each channel's intensity is stored in an 8-bit (uint8) value. This ensures that the values for each channel are always in the [0, 255] range.
#If any operation results in a value outside the [0, 255] range (e.g., due to addition, subtraction, or bit manipulation), it's clamped back to the valid range using:
#pixel_value = np.clip(pixel_value, 0, 255). This ensures no overflow or underflow.
#The uint8 data type inherently enforces the [0, 255] range. Any value set outside this range automatically wraps around: -1 becomes 255 (underflow).  256 becomes 0 (overflow).
    encoded_pixels = np.array(pixels, dtype=np.uint8)
    
    for i in range(len(binary_message)):
        #THE REAL OG LOGIC
        pixel_index = i // 3  #getting the pixel index
        color_index = i % 3   #getting the color channel index 
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
        
        #store modified pixel value
        encoded_pixels[row, col, color_index] = pixel_value
    
    # Convert back to image and save
    encoded_image = Image.fromarray(encoded_pixels)
    encoded_image.save(image_path, 'PNG')

def decode_message(image_path):
    #open image and convert to numpy array
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
        print("use -help to see how to use")
        sys.exit(1)

    if sys.argv[1] == '-e' or sys.argv[1] == "--encode":
        if len(sys.argv) != 4:
            print("provide both an image path and a message.")
            print("python3 encoder.py -encode <image_path> <message>")
            sys.exit(1)

        image_path = sys.argv[2]
        message = sys.argv[3]
        encode_message(image_path, message)
        print("Message encoded")
    
    elif sys.argv[1] == '-d' or sys.argv[1] == "--decode":
        if len(sys.argv) != 3:
            print("You need to provide an image path for decoding.")
            print("python3 encoder.py -decode <image_path>")
            sys.exit(1)

        image_path = sys.argv[2]
        decoded_message = decode_message(image_path)
        print("decoded Message: ", decoded_message)
     
    elif sys.argv[1] == '-h' or sys.argv[1] == "--help":
    	print("python3 encoder.py --help or -h")
    	print("encode: python3 encoder.py --encode <image.png> <message> or -e")
    	print("decode: python3 encoder.py --decode <image.png> or -d")
    
    # If no valid option provided
    else:
        print("Invalid")
        print("python3 encoder.py -encode <image_path> <message> or -decode <image_path>")

if __name__ == '__main__':
    main()

