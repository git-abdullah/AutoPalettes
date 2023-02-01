import random as ra
from PIL import Image
import numpy as np

# constants for images
PALETTE_W = 500
PALETTE_H = 200

COLOR_W = 100
COLOR_H = 200


class PaletteBuilder:
    def __int__(self) -> None:
        self.opened_img = None
        self.unique_img_data = []
        self.palette_colors = []

        # re-initialize the list, before using it
        self.palette_color_img_list = []

    def set_img(self, path_to_img: str) -> None:
        path = path_to_img
        self.opened_img = Image.open(fp=path).convert('RGBA')
        img_data = set(self.opened_img.getdata())  # to use for union
        self.unique_img_data = list(img_data.union(img_data))  # to use for random sample

    def new_palette(self) -> list:
        if self.unique_img_data is not None:

            # samples five random colors from the list
            palette_colors = ra.sample(self.unique_img_data, 5)
            palette_img = Image.new(size=(PALETTE_W, PALETTE_H), mode='RGBA', color=(0, 0, 0))
            self.palette_color_img_list = []

            # builds the palette_img anf
            count = 0
            for color in palette_colors:
                color_img = Image.new(size=(COLOR_W, COLOR_H), mode='RGBA', color=color)
                self.palette_color_img_list.append(np.asarray(color_img, dtype=float) / 255.0)
                palette_img.paste(color_img, (count, 0))
                count = count + COLOR_W

            return [np.asarray(palette_img, dtype=float) / 255.0, self.palette_color_img_list, palette_colors]

    def org_img_info(self) -> dict:
        size = self.opened_img.size
        mode = self.opened_img.mode
        img_format = self.opened_img.format

        return {'size': size, 'mode': mode, 'format': img_format}
