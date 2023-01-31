import random as ra
from PIL import Image
import numpy as np


class Palette:
    def __init__(self) -> None:
        self.path = None
        self.img = None
        self.img_pixels = None
        self.unique_pixels = None
        self.palette = None

        self.palette_image = None
        self.palette_color_imgs = []

    def set_path(self, path) -> None:
        self.path = path
        self.img = Image.open(fp=self.path)
        self.img_pixels = set(self.img.getdata())
        self.unique_pixels = list(self.img_pixels.union(self.img_pixels))

    def new_palette(self) -> None:
        # picks 5 random color from unique pixel data
        self.palette = ra.sample(self.unique_pixels, 5)
        self.palette_image = Image.new(size=(500, 100), mode='RGB', color=(0, 0, 0))
        self.palette_color_imgs = []
        self._get_palette_img()

    def _get_palette_img(self) -> None:
        count = 0
        for color in self.palette:
            color_img = Image.new(size=(100, 100), mode='RGB', color=color)
            self.palette_color_imgs.append(np.asarray(color_img, dtype='float') / 255.0)
            self.palette_image.paste(color_img, (count, 0))
            count = count + 100

    def palette_img_array(self) -> np.array:
        # I had to divide values by 255 since PIL uses 0 to 255 and dearpygui seems
        # to use 0.0 to 1.0
        # dpg_image = numpy.frombuffer(image.tobytes(), dtype=numpy.uint8) / 255.0
        # just for self note:
        # LINK https://stackoverflow.com/questions/65880271/how-to-draw-a-pil-image-to-a-dearpygui-canvas

        return np.asarray(self.palette_image, dtype='float') / 255.0

    def export_palette_img(self, export_path) -> None:
        try:
            self.palette_image.save(fp=export_path, type='PNG')

        except Exception as err:
            raise Exception(err)

    def org_img_info(self) -> dict:
        size = self.img.size
        mode = self.img.mode
        img_format = self.img.format

        return {'size': size, 'mode': mode, 'format': img_format}
