# import klayout.db as kdb
import pya as kdb


def put_box(cell, layout):
    l1 = layout.insert_layer(kdb.LayerInfo(1, 0))
    box = kdb.DBox(kdb.DPoint(0, 0), kdb.DPoint(20, 30))
    cell.shapes(l1).insert(box)


# class Box(pya.PCell):

# box = kdb.DBox(kdb.DPoint(0, 0), kdb.DPoint(20, 40))
# TOP.shapes(l1).insert(box)
