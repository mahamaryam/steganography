from PIL import Image, ImageSequence
stego_gif = Image.open('cat.gif')
    
    # Extract width, height, and number of frames from the first 48 bits of the first frame
first_frame = stego_gif.convert("P")  # Ensure it's in P mode
pixels = first_frame.load()
width, height = first_frame.size
print("width = ",width)
print("height = ",height)
