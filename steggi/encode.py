#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np

# Open the image
image = Image.open('image.png')

# Convert the image to a NumPy array
image_array = np.array(image)

# Convert the NumPy array back to a Pillow image
image_from_array = Image.fromarray(image_array)

# Save the image
image_from_array.save('modified_image.png')

