import random as ra
from PIL import Image
import numpy as np
import dearpygui.dearpygui as dpg

dpg.create_context()


def palette_generate_callback():
    dpg.set_value('palette_img', palette_img_array('assets/sample.png'))
    print(dpg.get_value('input1'))


def palette_img_array(path):
    img = Image.open(fp=path).convert('RGB')
    img_pixels = set(img.getdata())
    unique_pixels = list(img_pixels.union(img_pixels))
    # picks 5 random color from unique pixel data
    palette = ra.sample(unique_pixels, 5)

    palette_image = Image.new(size=(500, 200), mode='RGBA', color=(0, 0, 0, 255))

    count = 0
    for color in palette:
        color_img = Image.new(size=(100, 200), mode='RGB', color=color)
        palette_image.paste(color_img, (count, 0))
        count = count + 100

    # palette_image.putalpha(255)
    arr_y = np.asarray(palette_image, dtype=float)
    return arr_y / 255.0


with dpg.window(tag='Auto Palettes'):
    dpg.add_button(label='Generate', callback=palette_generate_callback)
    with dpg.texture_registry(show=False):
        dpg.add_dynamic_texture(width=500, height=200, default_value=[], tag='palette_img')
    dpg.add_image('palette_img')
    dpg.add_input_text(tag='input1')

dpg.create_viewport(title='Auto Palettes', width=1100, height=480, resizable=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Auto Palettes', True)
dpg.start_dearpygui()
dpg.destroy_context()

