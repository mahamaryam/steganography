import cv2
import numpy as np

image_path = "image.png" 
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    print("Error: Could not load image.")
    exit()

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(image, low_threshold, high_threshold)
edges_array = np.array(edges)

print("Edges Array:")
print(edges_array)
