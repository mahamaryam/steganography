from PIL import Image
import os

def extract_frames_from_gif(gif_path, output_dir):
    # Open the GIF file
    with Image.open(gif_path) as gif:
        # Check if output directory exists, if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        frame_number = 0
        while True:
            # Save the current frame as an image
            frame_filename = os.path.join(output_dir, f"frame_{frame_number:04d}.png")
            gif.save(frame_filename, format="PNG")
            print(f"Saved: {frame_filename}")
            
            frame_number += 1

            # Move to the next frame
            try:
                gif.seek(frame_number)
            except EOFError:
                break  # No more frames to process

    print(f"All frames extracted and saved to {output_dir}")

# Usage example
gif_path = "cat.gif"         # Replace with your GIF file path
output_dir = "gif_frames"      # Replace with your desired output directory
extract_frames_from_gif(gif_path, output_dir)

