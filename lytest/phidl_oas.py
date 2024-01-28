""" Adds OASIS functionality to phidl. Uses klayout to convert gds to oas and back
"""

import os

try:
    from phidl import geometry as pg
except ImportError:
    # This will error if you call the functions, not when you import the module
    class Warner:
        def __getattr__(self, att):
            raise ImportError('phidl was not found, so import/write OAS will not work')
    pg = Warner()


def import_oas(filename, cellname=None, flatten=False):
    if filename.lower().endswith(".gds"):
        # you are looking for import_gds
        retval = pg.import_gds(filename, cellname=cellname, flatten=flatten)
        return retval
    try:
        import pya
    except ImportError as err:
        err.args = (
            "[PHIDL] klayout package needed to import OASIS. pip install klayout\n"
            + err.args[0],
        ) + err.args[1:]
        raise
    if not filename.lower().endswith(".oas"):
        filename += ".oas"
    fileroot = os.path.splitext(filename)[0]
    tempfilename = f"{fileroot}-tmp.gds"

    layout = pya.Layout()
    layout.read(filename)
    # We want to end up with one Device. If the imported layout has multiple top cells,
    # a new toplevel is created, and they go into the second level
    if len(layout.top_cells()) > 1:
        topcell = layout.create_cell("toplevel")
        rot_DTrans = pya.DTrans.R0
        origin = pya.DPoint(0, 0)
        for childcell in layout.top_cells():
            if childcell == topcell:
                continue
            topcell.insert(
                pya.DCellInstArray(
                    childcell.cell_index(), pya.DTrans(rot_DTrans, origin)
                )
            )
    else:
        topcell = layout.top_cell()
    topcell.write(tempfilename)

    retval = pg.import_gds(tempfilename, cellname=cellname, flatten=flatten)
    os.remove(tempfilename)
    return retval


def write_oas(device, filename, **write_kwargs):
    if filename.lower().endswith(".gds"):
        # you are looking for write_gds
        device.write_gds(filename, **write_kwargs)
        return
    try:
        import pya
    except ImportError as err:
        err.args = (
            "[PHIDL] klayout package needed to write OASIS. pip install klayout\n"
            + err.args[0],
        ) + err.args[1:]
        raise
    if not filename.lower().endswith(".oas"):
        filename += ".oas"
    fileroot = os.path.splitext(filename)[0]
    tempfilename = f"{fileroot}-tmp.gds"

    device.write_gds(tempfilename, **write_kwargs)
    layout = pya.Layout()
    layout.read(tempfilename)
    # there can only be one top_cell because we only wrote one device
    topcell = layout.top_cell()
    topcell.write(filename)
    os.remove(tempfilename)
    return filename
