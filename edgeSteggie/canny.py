import cv2
import numpy as np

# Load the input image in grayscale
image_path = "image.png"  # Replace with your image path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded correctly
if image is None:
    print("Error: Could not load image.")
    exit()

# Apply Canny edge detection
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(image, low_threshold, high_threshold)

# Store the edges in a NumPy array
edges_array = np.array(edges)

# Display the original image and the edges
#cv2.imshow("Original Image", image)
#cv2.imshow("Detected Edges", edges)

# Wait for a key press and close the windows
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Print the edges array (optional)
print("Edges Array:")
print(edges_array)
