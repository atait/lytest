import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import phidlib
import numpy as np


# quickplotters so you can debug this file more easily
try:
    import lyipc.client as ipc
    kqp = ipc.generate_display_function(None, 'debugging.gds')
except ImportError:
    def kqp(*args, **kwargs):
        raise RuntimeError('klayout quickplot is not available.\nPlease install lyipc.')
from phidl import quickplot2 as qp


# Differencing
import lytest
from lytest import contained_geometry, difftest_it, store_reference
test_root = os.path.join(os.path.dirname(phidlib.__file__), 'tests')
lytest.utest_buds.set_layout_dirbase(test_root)


# Begin actual device testing
@contained_geometry
def Boxy(TOP):
    TOP << phidlib.box()

def test_Boxy(): difftest_it(Boxy)()
