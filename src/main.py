import dearpygui.dearpygui as dpg
from typing import Dict

_CTX: Dict = {
    "padding": 10,
    "viewWidth": 800,
    "viewHeight": 600
}

def init():
    dpg.create_context()
    __init_view()
    __init_values()
    __init_input()

def __init_view():
    dpg.create_viewport(title="Graph Tool", width=_CTX["viewWidth"], height=_CTX["viewHeight"])
    
    with dpg.window(
        tag="win:main",
        width=_CTX["viewWidth"],
        height=_CTX["viewWidth"],
        no_move=True,
        no_resize=True,
        no_title_bar=True,
        no_collapse=True,
        no_close=True,
        menubar=True
    ):
        with dpg.menu_bar():
            dpg.add_menu(tag="menu:main", label="Vertices")
        dpg.add_drawlist(
            tag="canvas:main",
            pos=[_CTX["padding"]]*2,
            width=_CTX["viewWidth"] - _CTX["padding"]*2,
            height=_CTX["viewHeight"] - _CTX["padding"]*2
        ) 
        
    dpg.setup_dearpygui()
    dpg.show_viewport()

def __init_values():
    with dpg.value_registry():
        dpg.add_float4_value(tag="val:mouse_position")

def __init_input():
    with dpg.handler_registry():
        dpg.add_mouse_move_handler(callback=__mouse_move_callback)
    
def __mouse_move_callback():
    dpg.set_value("val:mouse_position", dpg.get_mouse_pos())
    print(f"Mouse moved: {dpg.get_value('val:mouse_position')}")

def run():
    dpg.start_dearpygui()
    dpg.destroy_context()

def main():
    init()
    run()
    
if __name__ == "__main__":
    main()