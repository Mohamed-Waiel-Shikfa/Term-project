import os
import numpy as np
from PIL import Image

# Image dimensions
width = 800
height = 580

# Create a subfolder named 'images' if it doesn't exist
if not os.path.exists('noise_image'):
    os.makedirs('noise_image')

# Generate and save 51 images
for i in range(0, 51):
    # Generate random noise with a black to transparent ratio of 10:1
    noise = np.random.choice([0, 255], size=(height, width), p=[1/11, 10/11])

    # Create a PIL image from the noise array
    image = Image.fromarray(np.uint8(noise))

    # Convert the image to RGBA and make white (also noise) pixels transparent
    image = image.convert("RGBA")
    datas = image.getdata()

    newData = []
    for item in datas:
        # change all white (also shades of whites)
        # pixels to transparent
        if item[0] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    image.putdata(newData)

    # Save the image in the 'images' subfolder
    image.save(f'noise_image/{i}.png')
