import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pyalib


# Differencing
import lytest
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file
from lytest import difftest_it, store_reference
from lytest.nonvisual_pya import contained_geometry
test_root = os.path.join(os.path.dirname(pyalib.__file__), 'tests')
lytest.utest_buds.set_layout_dirbase(test_root)


# Begin actual device testing
@contained_geometry
def Boxy(TOP, layout):
    pyalib.put_box(TOP, layout)

def test_Boxy(): difftest_it(Boxy)()
