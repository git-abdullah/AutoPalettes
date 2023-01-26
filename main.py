from PIL import Image
import random as ra

sample_img = Image.open(fp='assets/sample.png')
pixel_set = set(sample_img.getdata())

# using union of sets, same pixels are removed (all pixels are unique)
unique_pixel = list(pixel_set.union(pixel_set))

# picks 5 random color from unique pixel data
palettes = ra.sample(unique_pixel, 5)

palette_image = Image.new(size=(1000, 200), mode='RGB', color=(0, 0, 0))

count = 0
for color in palettes:
    color_img = Image.new(size=(200, 200), mode='RGB', color=color)
    palette_image.paste(color_img, (count, 0))
    count = count + 200

palette_image.show(title="Color Palette")
