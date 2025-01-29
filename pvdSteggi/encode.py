from PIL import Image
import numpy as np
import sys
import argparse

def encode_message(image_path, message):

    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '00000000'  

    img = Image.open(image_path).convert('RGB')
    pixels = np.asarray(img) 
       
    encoded_pixels = np.array(pixels, dtype=np.uint8)
    
    string_index = 0

    for i in range(len(binary_message)):
        pixel_index = i // 3  
        color_index = i % 3   
        row = pixel_index // pixels.shape[1]
        col = pixel_index % pixels.shape[1]
        
        pixel_value1 = int(encoded_pixels[row, col, color_index])
        
        i += 1
        pixel_index = i // 3  
        pixel_value2 = int(encoded_pixels[row, col, color_index])
        
        #now we have a pair of pixels ready.
        
        diff = abs(pixel_value1 - pixel_value2)
        #now we have the difference, now we need to find the range into which this difference falls so that we can calculate the number of bits of message to be embedded.
        
        if diff in range(0,8): #range is exclusive of the upper bound
        	string = binary_messagep[string_index:string_index+3]
        	string_index+=3
        	
        elif diff in range(8,16):
        	string = binary_messagep[string_index:string_index+3]
        	string_index+=3
        	
        elif diff in range(16,32): #4
        	string = binary_messagep[string_index:string_index+4]
        	string_index+=4
        	
        elif diff in range(32,64): #5
        	string = binary_messagep[string_index:string_index+5]
        	string_index+=5
        	
        elif diff in range(64,128): #6
        	string = binary_messagep[string_index:string_index+6]
        	string_index+=6
        	
        elif diff in rnage(128,256): #7
        	string = binary_messagep[string_index:string_index+7]
        	string_index+=7
        
        val = int(string,2)
        
        #pixels are already positive
        
        if (abs(pixel_value1 - pixel_value2)) < val:
        	 while True:
        	 	
        	 	
        
            
        pixel_value = np.clip(pixel_value, 0, 255)
        
        encoded_pixels[row, col, 0] = pixel_value
        
        i+=1
    
    encoded_image = Image.fromarray(encoded_pixels)
    encoded_image.save(image_path, 'PNG')
