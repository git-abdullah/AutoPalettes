import dearpygui.dearpygui as dpg
from palette_generator import Palette

dpg.create_context()
palette = Palette()


def img_pick_callback(user_data, app_data):
    """
    app_data contains: {'file_path_name': '/home/abdullah/repos/AutoPalette/assets/sample.png', 'file_name':
    'sample.png', 'current_path': '/home/abdullah/repos/AutoPalette/assets', 'current_filter': '.png', 'min_size': [
    100.0, 100.0], 'max_size': [30000.0, 30000.0], 'selections': {'sample.png':
    '/home/abdullah/repos/AutoPalette/assets/sample.png'}}
    """
    print(app_data)

    img_path = app_data.get('file_path_name')
    dpg.set_value(item='picked_img', value=app_data.get('file_name'))

    palette.set_path(img_path)
    info = palette.org_img_info()
    dpg.set_value(item='img_name', value=f"File: {app_data.get('file_name')}")
    dpg.set_value(item='info_format', value=f"Format: {info.get('format')}")
    dpg.set_value(item='info_mode', value=f"Mode: {info.get('mode')}")
    dpg.set_value(item='info_size', value=f"Size: {info.get('size')}")


def palette_generate_callback():
    palette.new_palette()
    palette_preview_array = palette.palette_img_array()
    dpg.set_value('preview-palette', palette_preview_array)

    palette_imgs = palette.palette_color_imgs
    palette_colors = palette.palette
    for i in range(0, 5):
        dpg.set_value(f'color-{i}', palette_imgs[i])
        dpg.set_value(f'color-{i}-value-rgb', f'rgb{palette_colors[i]}')


# textures
with dpg.texture_registry(show=False):
    # textures defined here, each for each color
    h, w = 100, 100
    img_format = dpg.mvFormat_Float_rgb
    dpg.add_raw_texture(width=w, height=h, default_value=[], format=img_format, tag='color-0')
    dpg.add_raw_texture(width=w, height=h, default_value=[], format=img_format, tag='color-1')
    dpg.add_raw_texture(width=w, height=h, default_value=[], format=img_format, tag='color-2')
    dpg.add_raw_texture(width=w, height=h, default_value=[], format=img_format, tag='color-3')
    dpg.add_raw_texture(width=w, height=h, default_value=[], format=img_format, tag='color-4')
# preview palette texture
    dpg.add_raw_texture(width=500, height=100, default_value=[], format=img_format, tag='preview-palette')

# File Picker dialog for images
with dpg.file_dialog(directory_selector=False, show=False, callback=img_pick_callback,
                     id='img_pick_dialog', height=400, width=400):
    dpg.add_file_extension('.png')
    dpg.add_file_extension('.jpg')
    dpg.add_file_extension('.jpeg')

# dir picker dialog for export dir
# TODO

# Main window
with dpg.window(tag='Auto Palettes'):

    # acts as top bar for pick_img button
    with dpg.group(horizontal=True):
        dpg.add_button(label='Pick Image', callback=lambda: dpg.show_item('img_pick_dialog'))
        dpg.add_text('None', tag='picked_img')

    # acts as a container for both cols
    with dpg.group(horizontal=True):

        # first col. for Image and info
        with dpg.child_window(border=True, width=200, use_internal_label=True):
            dpg.add_text('Info:')
            dpg.add_text('File: ...', tag='img_name')
            dpg.add_text('Format: ...', tag='info_format')
            dpg.add_text('Size: ...', tag='info_size')
            dpg.add_text('Mode: ...', tag='info_mode')
            dpg.add_text('')

            dpg.add_button(label='Generate', callback=palette_generate_callback)

        # second col. for palette and color fields
        with dpg.child_window(border=True):

            # builds fields and color image for each color
            with dpg.group(horizontal=True):
                for i in range(0, 5):
                    with dpg.group(horizontal=False):
                        dpg.add_image(texture_tag=f'color-{i}')
                        with dpg.group(horizontal=True):
                            dpg.add_input_text(label='rga', tag=f'color-{i}-value-rgb', width=80)
                            dpg.add_button(label='copy', tag=f'color-{i}-value-rgb-copy')

                        with dpg.group(horizontal=True):
                            dpg.add_input_text(label='hex', tag=f'color-{i}-value-hex', width=80)
                            dpg.add_button(label='copy', tag=f'color-{i}-value-hex-copy')

            # displays palette preview
            dpg.add_text('')
            dpg.add_text('Palette Preview')
            dpg.add_image('preview-palette')
            dpg.add_text('')

            # later, add a dir picker dialog callback
            dpg.add_button(label='Save as PNG')


dpg.create_viewport(title='Auto Palettes', width=1100, height=480, resizable=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Auto Palettes', True)
dpg.start_dearpygui()
dpg.destroy_context()
