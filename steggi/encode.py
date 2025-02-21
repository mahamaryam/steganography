#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np

image = Image.open('image.png')
image_array = np.array(image)
image_from_array = Image.fromarray(image_array)
image_from_array.save('modified_image.png')

