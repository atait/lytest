from lygadgets import pya


def put_box(cell, w=50):
    if pya is None:
        return  # skip it hard
    layers_temp = [pya.LayerInfo(1, 0), pya.LayerInfo(2, 0)]
    all_layer_refs = []
    for layerspec in layers_temp:
        all_layer_refs.append(cell.layout().insert_layer(layerspec))
    box = pya.DBox(pya.DPoint(0, 0), pya.DPoint(w, 30))
    cell.shapes(all_layer_refs[0]).insert(box)
