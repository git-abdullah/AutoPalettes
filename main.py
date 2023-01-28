import dearpygui.dearpygui as dpg
from palette_generator import Palette

dpg.create_context()


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

    info = Palette(img_path).org_img_info()
    dpg.set_value(item='img_name', value=f"File: {app_data.get('file_name')}")
    dpg.set_value(item='info_format', value=f"Format: {info.get('format')}")
    dpg.set_value(item='info_mode', value=f"Mode: {info.get('mode')}")
    dpg.set_value(item='info_size', value=f"Size: {info.get('size')}")


with dpg.window(tag='Auto Palettes'):
    # acts as top bar for pick_img button
    with dpg.group(horizontal=True):
        dpg.add_button(label='Pick Image', callback=lambda: dpg.show_item('img_pick_dialog'))
        dpg.add_text('None', tag='picked_img')

    with dpg.group(horizontal=True):

        # first col. for Image and info
        with dpg.child_window(border=True, width=200, use_internal_label=True):

            # file picker dialog for image path
            with dpg.file_dialog(directory_selector=False, show=False, callback=img_pick_callback,
                                 id='img_pick_dialog', height=400, width=400):
                dpg.add_file_extension('.png')
                dpg.add_file_extension('.jpg')
                dpg.add_file_extension('.jpeg')

            dpg.add_text('Info:')
            dpg.add_text('File: ...', tag='img_name')
            dpg.add_text('Format: ...', tag='info_format')
            dpg.add_text('Size: ...', tag='info_size')
            dpg.add_text('Mode: ...', tag='info_mode')
            dpg.add_text('')

            dpg.add_button(label='Generate')

        # second col. for palette and color fields
        with dpg.child_window(border=True):
            dpg.add_text('Palette Image here')
            dpg.add_text('and other widgets and color values')


dpg.create_viewport(title='Auto Palettes', width=900, height=480, resizable=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Auto Palettes', True)
dpg.start_dearpygui()
dpg.destroy_context()
