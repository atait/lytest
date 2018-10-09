# import klayout.db as kdb
import pya as kdb


layers_temp = [kdb.LayerInfo(1, 0), kdb.LayerInfo(2, 0)]


# goes in library
# Write and tell Klayout GUI to open the file
layout.write(gdsname)
ipc.load(gdsname)
kqp = ipc.generate_display_function(TOP, 'box.gds')


def put_box(cell, layout):
    l1 = layout.insert_layer(pya.LayerInfo(1, 0))\
    box = pya.DBox(pya.DPoint(0, 0), pya.DPoint(20, 20))
    cell.shapes(l1).insert(box)


# class Box(pya.PCell):

# box = kdb.DBox(kdb.DPoint(0, 0), kdb.DPoint(20, 40))
# TOP.shapes(l1).insert(box)
