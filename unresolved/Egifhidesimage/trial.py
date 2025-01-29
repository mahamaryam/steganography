from PIL import Image
import os

# Open the GIF file
gif_path = 'minnie.gif'  # Replace with your GIF file path
output_folder = 'frames'  # Folder to save frames

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Open the GIF
with Image.open(gif_path) as gif:
    frame_count = 0
    
    # Loop through each frame in the GIF
    while True:
        frame_path = os.path.join(output_folder, f"frame_{frame_count:03d}.png")
        
        # Save the current frame as an image
        gif.save(frame_path, format='PNG')
        frame_count += 1
        
        try:
            # Move to the next frame
            gif.seek(gif.tell() + 1)
        except EOFError:
            # Break the loop if we reach the end of the GIF
            break

print(f"Extracted {frame_count} frames to the folder '{output_folder}'.")

