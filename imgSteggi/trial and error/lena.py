#!/usr/bin/python3

from PIL import Image
import numpy as np

img = Image.open('child.png').convert('RGB')
 
pixels = np.asarray(img) 

print(pixels.shape)
