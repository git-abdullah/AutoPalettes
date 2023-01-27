import random as ra
from PIL import Image


class Palettes:
    def __init__(self, path_to_img) -> None:
        self.path = path_to_img

        img_pixels = set(Image.open(fp=self.path).getdata())
        self.unique_pixels = list(img_pixels.union(img_pixels))
        # picks 5 random color from unique pixel data
        self.palettes = ra.sample(self.unique_pixels, 5)

        self.palette_image = Image.new(size=(1000, 500), mode='RGB', color=(0, 0, 0))
        self._get_palette_img()

    def _get_palette_img(self) -> None:

        count = 0
        for color in self.palettes:
            color_img = Image.new(size=(200, 500), mode='RGB', color=color)
            self.palette_image.paste(color_img, (count, 0))
            count = count + 200

    def get_palette_img_bytes(self):
        return self.palette_image

    def color_values(self) -> list:
        return self.palettes

    def export_palette_img(self, export_path) -> None:
        try:
            self.palette_image.save(fp=export_path, type='PNG')

        except Exception as err:
            raise Exception(f'Unable to export image ERROR: {err} ...')
