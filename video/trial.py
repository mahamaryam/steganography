from PIL import Image
import numpy as np

# Load the image
img = Image.open('lena.png').convert('RGB')   
parent_pixels = np.asarray(img)     
x = np.array(parent_pixels, dtype=np.uint8)

height, width, channels = x.shape
print(x.shape)



# Flatten the array
flattened_x = x.flatten()
i = 0
image_to_encode = str(height) +"." + str(width)
while i < len(flattened_x):
	image_to_encode += "." + str(i)
	i +=1

image_to_encode += "#"
