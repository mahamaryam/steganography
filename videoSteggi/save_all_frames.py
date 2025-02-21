import cv2
import os

def extract_frames(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_capture = cv2.VideoCapture(video_path)
    
    if not video_capture.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    frame_number = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break 
        frame_filename = os.path.join(output_dir, f"frame_{frame_number:04d}.png")
        cv2.imwrite(frame_filename, frame)
        print(f"Saved: {frame_filename}")
        
        frame_number += 1

    video_capture.release()
    print(f"All frames extracted and saved to {output_dir}")

video_path = "v1.mp4" 
output_dir = "frames_output"  
extract_frames(video_path, output_dir)

