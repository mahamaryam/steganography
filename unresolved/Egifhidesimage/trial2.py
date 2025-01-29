#!/usr/bin/python3

from PIL import Image, ImageSequence
import numpy as np

def encode_image_in_gif(image_path, gif_path, output_path):
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS) # Resize to reduce data
        pixels = np.asarray(img)
        encoded_pixels = np.array(pixels, dtype=np.uint8)
        binary_pixels = np.vectorize(np.binary_repr)(encoded_pixels, width=8)
        bit_string = "".join("".join(pixel.flatten()) for pixel in binary_pixels)
        bit_string += '00000000' # Add a small terminator

        gif = Image.open(gif_path)
        frames = []
        i = 0
        binary_length = len(bit_string)

        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('P')
            palette = frame.getpalette()
            width, height = frame.size

            modified_frame = frame.copy()
            modified_pixels = modified_frame.load()

            for x in range(width):
                for y in range(height):
                    if i >= binary_length:
                        break

                    original_index = frame.getpixel((x, y)) # Use getpixel for palettes
                    bit = int(bit_string[i])
                    modified_index = (original_index & ~1) | bit

                    modified_pixels[x, y] = modified_index
                    i += 1
                if i >= binary_length:
                    break

            modified_frame.putpalette(palette)
            frames.append(modified_frame)

        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=gif.info.get('duration', 100),
            disposal=2
        )
        print(f"Message encoded and saved in '{output_path}'")

    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
encode_image_in_gif('lena.png', 'baby.gif', 'encoded.gif')

