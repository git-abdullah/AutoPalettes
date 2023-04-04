import dearpygui.dearpygui as dpg
from palette_generator import PaletteBuilder
import pyperclip

dpg.create_context()
palette = PaletteBuilder()


def img_pick_callback(user_data, app_data):
    img_path = app_data.get('file_path_name')
    dpg.set_value(item='picked_img', value=app_data.get('file_name'))

    info = palette.set_img(path_to_img=img_path)
    dpg.set_value(item='img_name', value=f"File: {app_data.get('file_name')}")
    dpg.set_value(item='info_format', value=f"Format: {info[2]}")
    dpg.set_value(item='info_mode', value=f"Mode: {info[1]}")
    dpg.set_value(item='info_size', value=f"Size: {info[0]}")


def palette_generate_callback():
    palette_preview_array, palette_color_img_list, palette_colors, colors_hex = palette.new_palette()
    dpg.set_value('preview-palette', palette_preview_array)

    for i in range(0, 5):
        dpg.set_value(f'color-{i}', palette_color_img_list[i])
        dpg.set_value(f'color-{i}-value-rgb', f'rgb{palette_colors[i]}')
        dpg.set_value(f'color-{i}-value-hex', colors_hex[i])


def color_copy_callback(sender):
    tag = sender.split('#')[0]
    color = dpg.get_value(tag)
    if color != '':
        try:
            pyperclip.copy(color)
        except Exception as err:
            print(err)


def export_png_callback(user_data, app_data):
    export_path = app_data.get('file_path_name')
    palette.export_as_png(path=export_path)


# textures
with dpg.texture_registry(show=False):
    # textures defined here, each for each color
    h, w = 200, 100
    img_format = dpg.mvFormat_Float_rgb
    dpg.add_dynamic_texture(width=w, height=h, default_value=[], tag='color-0')
    dpg.add_dynamic_texture(width=w, height=h, default_value=[], tag='color-1')
    dpg.add_dynamic_texture(width=w, height=h, default_value=[], tag='color-2')
    dpg.add_dynamic_texture(width=w, height=h, default_value=[], tag='color-3')
    dpg.add_dynamic_texture(width=w, height=h, default_value=[], tag='color-4')
    # preview palette texture
    dpg.add_dynamic_texture(width=500, height=200, default_value=[], tag='preview-palette')

# File Picker dialog for images
with dpg.file_dialog(directory_selector=False, show=False, callback=img_pick_callback,
                     tag='img_pick_dialog', height=400, width=400):
    dpg.add_file_extension('.png')
    dpg.add_file_extension('.jpg')
    dpg.add_file_extension('.jpeg')

# dir picker dialog for export dir
dpg.add_file_dialog(
    directory_selector=True, show=False, callback=export_png_callback, tag='export-dir', height=400, width=400)

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
                            dpg.add_input_text(label='rga', tag=f'color-{i}-value-rgb', width=90)
                            dpg.add_button(label='copy', tag=f'color-{i}-value-rgb#-copy', callback=color_copy_callback)

                        with dpg.group(horizontal=True):
                            dpg.add_input_text(label='hex', tag=f'color-{i}-value-hex', width=90)
                            dpg.add_button(label='copy', tag=f'color-{i}-value-hex#-copy', callback=color_copy_callback)

            # displays palette preview
            dpg.add_text('')
            dpg.add_text('Palette Preview')
            dpg.add_image('preview-palette')
            dpg.add_text('')

            # later, add a dir picker dialog callback
            dpg.add_button(label='Save as PNG', callback=lambda: dpg.show_item('export-dir'))


dpg.create_viewport(title='Auto Palettes', width=1100, height=600, resizable=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Auto Palettes', True)
dpg.start_dearpygui()
dpg.destroy_context()
