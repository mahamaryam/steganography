from PIL import Image
import numpy as np
img = Image.open('child.png').convert('RGB')   
parent_pixels = np.asarray(img)   
print(parent_pixels.shape)
