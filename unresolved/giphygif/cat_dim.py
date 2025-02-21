from PIL import Image, ImageSequence
stego_gif = Image.open('cat.gif')
    
first_frame = stego_gif.convert("P")  
pixels = first_frame.load()
width, height = first_frame.size
print("width = ",width)
print("height = ",height)
