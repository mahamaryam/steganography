#!/usr/bin/python3

from PIL import Image
import numpy as np 

img = Image.open('gif_frames/frame_0001.png')
pixels = np.asarray(img)     
encoded_pixels = np.array(pixels, dtype=np.uint8)
width, height, channel = encoded_pixels.shape
print(width,"    ", height)
