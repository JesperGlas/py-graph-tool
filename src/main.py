import dearpygui.dearpygui as dpg
from typing import Dict, Tuple
from Graph import Graph

# global variables
GRAPH   = Graph()
PADDING = 10
VIEW_WIDTH = 800
VIEW_HEIGHT = 600
ITEMS: Dict[str, set[str]] = {
    "vertices": set(),
    "edges": set(),
    "selected": set()
}

# help variables
LEFT_CLICK = 0
RIGHT_CLICK = 1

def init():
    dpg.create_context()
    __init_view()
    __init_values()
    __init_handlers()

def __init_view():
    dpg.create_viewport(title="Graph Tool", width=VIEW_WIDTH, height=VIEW_HEIGHT)
    
    with dpg.window(
        tag="win:main",
        width=VIEW_WIDTH,
        height=VIEW_HEIGHT,
        no_move=True,
        no_resize=True,
        no_title_bar=True,
        no_collapse=True,
        no_close=True,
    ):
        with dpg.menu_bar():
            dpg.add_menu(tag="menu:vertices", label="Vertices")
            dpg.add_button(label="Connect", callback=__connect_btn_callback)
            dpg.add_button(label="Remove", callback=__remove_btn_callback)
            dpg.add_button(label="Reset", callback=__reset_graph_callback)
            dpg.add_menu(tag="menu:edges", label="Edges")
        dpg.add_drawlist(
            tag="canvas:main",
            pos=[PADDING]*2,
            width=VIEW_WIDTH - PADDING*2,
            height=VIEW_HEIGHT - PADDING*4
        ) 
        dpg.draw_circle([0, 0], 5, color=(0, 0, 255, 255), tag="draw:selection")
        
    dpg.setup_dearpygui()
    dpg.show_viewport()

def __init_values():
    with dpg.value_registry():
        dpg.add_float4_value(tag="val:mouse_position", default_value=[0, 0, 0, 0])
        dpg.add_string_value(tag="val:", default_value=None)

def __init_handlers():
    with dpg.handler_registry():
        dpg.add_mouse_move_handler(callback=__mouse_move_callback)
        dpg.add_mouse_click_handler(callback=__mouse_click_callback)
    
def __mouse_move_callback(sender, data):
    # adjusting mouse position to padding
    dpg.set_value("val:mouse_position", list(map(lambda x: x-PADDING, dpg.get_mouse_pos())))
    dpg.configure_item("draw:selection", center=dpg.get_value("val:mouse_position")[:2])

def __mouse_click_callback(sender: str, data):
    print(f"[Mouse Click] Sender: {sender}, Data: {data}")
    if data == RIGHT_CLICK:
        GRAPH.add_vert(dpg.get_value("val:mouse_position")[:2])
        __load_graph()

def __vert_btn_callback(sender: str, data):
    print(f"[Vert Btn] Sender: {sender}, Data: {data}")
    if (selected := sender.split(":")[1]) not in list(ITEMS["selected"]):
        ITEMS["selected"].add(selected)
    else:
        ITEMS["selected"].remove(selected)
    __load_graph()

def __reset_graph_callback(sender, data):
    GRAPH.clear()
    __load_graph()

def __remove_btn_callback(sender: str, data):
    print(f"[Remove Btn] Sender: {sender}, Data: {data}")
    if len(selection := ITEMS["selected"]) > 0:
        for vert_key in selection:
            GRAPH.remove_vert(vert_key)
        __load_graph()

def __connect_btn_callback(sender: str, data):
    print(f"[Connect Btn] Sender: {sender}, Data: {data}")
    if len(ITEMS["selected"]) >= 2:
        for i, src in enumerate(ITEMS["selected"]):
            for dst in list(ITEMS["selected"])[i:]:
                GRAPH.add_edge(src, dst)
    print(GRAPH)
    __load_edges()

def __load_graph():
    __load_vertices()

def __load_vertices():
    for vert_key in GRAPH.vertices.union(ITEMS["vertices"]):
        if vert_key in GRAPH.vertices and vert_key not in ITEMS["vertices"]:
            ITEMS["vertices"].add(vert_key)
            dpg.draw_circle(tag=f"vert:{vert_key}", parent="canvas:main", center=dpg.get_value("val:mouse_position")[:2], radius=5, fill=(0, 255, 0, 255))
            dpg.add_checkbox(tag=f"btn:{vert_key}", label=vert_key, parent="menu:vertices", callback=__vert_btn_callback)
        if vert_key not in GRAPH.vertices and vert_key in ITEMS["vertices"]:
            dpg.delete_item(f"vert:{vert_key}")
            dpg.delete_item(f"btn:{vert_key}")
            ITEMS["vertices"].remove(vert_key)
            if vert_key in ITEMS["selected"]: ITEMS["selected"].remove(vert_key)
        if vert_key in ITEMS["selected"]:
            dpg.configure_item(f"vert:{vert_key}", fill=(255, 0, 0, 255))

def __load_edges():
    for src_key, adjacent in GRAPH.edge_data.items():
        for dst_key in adjacent:
            if (edge_key := GRAPH.edge_key(src_key, dst_key)) not in ITEMS["edges"] and GRAPH.edge_key(dst_key, src_key) not in ITEMS["edges"]:
                ITEMS["edges"].add(edge_key)
                src = GRAPH.get_pos(src_key)
                dst = GRAPH.get_pos(dst_key)
                dpg.draw_line(src, dst, color=(0, 0, 255, 255), thickness=1, parent="canvas:main")
            

def run():
    dpg.start_dearpygui()
    dpg.destroy_context()

def main():
    init()
    run()
    
if __name__ == "__main__":
    main()
