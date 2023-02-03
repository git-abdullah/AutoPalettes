import random as ra
from PIL import Image
import numpy as np
import datetime


# constants for images
PALETTE_W = 500
PALETTE_H = 200

COLOR_W = 100
COLOR_H = 200


class PaletteBuilder:
    def __int__(self) -> None:
        self.unique_img_data = []
        self.palette_colors = []
        self.palette_img = None

        # re-initialize the list, before using it
        self.palette_color_img_list = []

    def set_img(self, path_to_img: str) -> list:
        path = path_to_img
        opened_img = Image.open(fp=path).convert('RGBA')
        img_data = set(opened_img.getdata())  # to use for union
        self.unique_img_data = list(img_data.union(img_data))  # to use for random sample

        return [
            opened_img.size,
            opened_img.mode,
            opened_img.format,
        ]

    def new_palette(self) -> list | None:
        try:
            if self.unique_img_data is not None:

                # samples five random colors from the list
                palette_colors = ra.sample(self.unique_img_data, 5)
                palette_colors_hex = self._to_hex(palette_colors)
                self.palette_img = Image.new(size=(PALETTE_W, PALETTE_H), mode='RGBA', color=(0, 0, 0))
                self.palette_color_img_list = []

                # builds the palette_img anf
                count = 0
                for color in palette_colors:
                    color_img = Image.new(size=(COLOR_W, COLOR_H), mode='RGBA', color=color)
                    self.palette_color_img_list.append(np.asarray(color_img, dtype=float) / 255.0)
                    self.palette_img.paste(color_img, (count, 0))
                    count = count + COLOR_W

                return [
                    np.asarray(self.palette_img, dtype=float) / 255.0,
                    self.palette_color_img_list,
                    palette_colors,
                    palette_colors_hex
                ]
        except Exception as err:
            print(err)
            return None

    def export_as_png(self, path: str) -> None:
        now = datetime.datetime.now()
        path = f'{path}/{now}.png'
        try:
            self.palette_img.save(path, type='PNG')
        except Exception as err:
            print(err)

    def _to_hex(self, palette: list) -> list:
        hex_palette = []
        for color in palette:
            r, g, b, a = color    
            hex_col = '#%02x%02x%02x' % (r, g, b)
            hex_palette.append(hex_col)
        return hex_palette
