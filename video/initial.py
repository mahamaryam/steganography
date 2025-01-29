from mutagen.mp4 import MP4, MP4Cover
import base64
import shutil
import os

def hide_text(mp4_path, text, output_path):
    """Hide text in MP4 metadata"""
    if not os.path.exists(mp4_path):
        raise FileNotFoundError(f"Input file not found: {mp4_path}")
        
    # Create a copy of the original file
    shutil.copy2(mp4_path, output_path)
    
    try:
        video = MP4(output_path)
        encoded_text = base64.b64encode(text.encode()).decode()
        video["\xa9cmt"] = encoded_text
        video.save()
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        raise Exception(f"Failed to hide text: {str(e)}")

def retrieve_text(mp4_path):
    """Extract hidden text from MP4 metadata"""
    if not os.path.exists(mp4_path):
        raise FileNotFoundError(f"File not found: {mp4_path}")
        
    video = MP4(mp4_path)
    
    if "\xa9cmt" not in video:
        raise ValueError("No hidden text found")
        
    encoded_text = video["\xa9cmt"][0]
    return base64.b64decode(encoded_text).decode()

string = ''
for i in range (1000000):
	string += "i am just a girl"
hide_text('v1.mp4',string,'v2.mp4')
print(retrieve_text('v2.mp4'))
