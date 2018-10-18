import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pyalib

import lytest
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file

# Differencing
from lytest import difftest_it, store_reference
from lytest.nonvisual_pya import contained_geometry



# Begin actual device testing
@contained_geometry
def Boxypy(TOP):
    pyalib.put_box(TOP)


def test_Boxypy():
    lytest.utest_buds.test_root = os.path.join(os.path.dirname(pyalib.__file__), 'tests')
    difftest_it(Boxypy, file_ext='.oas')()
