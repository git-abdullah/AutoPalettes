import random as ra
from PIL import Image


class Palette:
    def __init__(self, path_to_img) -> None:
        self.path = path_to_img
        self.img = Image.open(fp=self.path)
        self.img_pixels = set(self.img.getdata())
        self.unique_pixels = list(self.img_pixels.union(self.img_pixels))
        # picks 5 random color from unique pixel data
        self.palette = ra.sample(self.unique_pixels, 5)

        self.palette_image = Image.new(size=(1000, 500), mode='RGB', color=(0, 0, 0))
        self._get_palette_img()

    def _get_palette_img(self) -> None:

        count = 0
        for color in self.palette:
            color_img = Image.new(size=(200, 500), mode='RGB', color=color)
            self.palette_image.paste(color_img, (count, 0))
            count = count + 200

    def palette_img_array(self) -> list:
        return list(self.palette_image.getdata())

    def palette_color_values(self) -> list:
        return self.palette

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
