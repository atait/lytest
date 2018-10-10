import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pyalib

import lytest
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file

# Differencing
from lytest import difftest_it, store_reference
from lytest.nonvisual_pya import contained_geometry
test_root = os.path.join(os.path.dirname(pyalib.__file__), 'tests')
lytest.utest_buds.set_layout_dirbase(test_root)


# Begin actual device testing
@contained_geometry
def Boxypy(TOP, layout):
    pyalib.put_box(TOP, layout)
    1 + 1

def test_Boxypy(): difftest_it(Boxypy)()
