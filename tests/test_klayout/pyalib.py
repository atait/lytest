from lygadgets import pya


def put_box(cell, w=50):
    if pya is None:
        return  # skip it hard
    layers_temp = [pya.LayerInfo(1, 0), pya.LayerInfo(2, 0)]
    all_layer_refs = [cell.layout().insert_layer(layerspec) for layerspec in layers_temp]

    box = pya.DBox(pya.DPoint(0, 0), pya.DPoint(w, 30))
    cell.shapes(all_layer_refs[0]).insert(box)
