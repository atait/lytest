import phidl
from phidl import geometry as pg
from phidl.device_layout import LayerSet

lys = LayerSet()
lys.add_layer(gds_layer=1, gds_datatype=0,
              name='l1', description='Layer 1')
lys.add_layer(gds_layer=2, gds_datatype=0,
              name='l2', description='Layer 2')


def box():
    return pg.rectangle(size=(10, 20), layer=lys['l1'])