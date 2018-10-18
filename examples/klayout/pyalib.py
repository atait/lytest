from lygadgets import pya as kdb

layers_temp = [kdb.LayerInfo(1, 0), kdb.LayerInfo(2, 0)]

def put_box(cell):
    all_layer_refs = []
    for layerspec in layers_temp:
        all_layer_refs.append(cell.layout().insert_layer(layerspec))
    box = kdb.DBox(kdb.DPoint(0, 0), kdb.DPoint(50, 30))
    cell.shapes(all_layer_refs[0]).insert(box)
