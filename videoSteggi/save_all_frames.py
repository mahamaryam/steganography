import cv2
import os

def extract_frames(video_path, output_dir):
    # Check if the output directory exists, create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    if not video_capture.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    frame_number = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break  # Exit the loop if no more frames are available
        
        # Save the frame as an image
        frame_filename = os.path.join(output_dir, f"frame_{frame_number:04d}.png")
        cv2.imwrite(frame_filename, frame)
        print(f"Saved: {frame_filename}")
        
        frame_number += 1

    # Release the video capture object
    video_capture.release()
    print(f"All frames extracted and saved to {output_dir}")

# Usage example
video_path = "v1.mp4"  # Replace with your video file path
output_dir = "frames_output"   # Replace with your desired output directory
extract_frames(video_path, output_dir)

