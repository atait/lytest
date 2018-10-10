import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import phidlib

import lytest
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file

# Differencing
from lytest import difftest_it, store_reference
from lytest.nonvisual import contained_geometry


# Begin actual device testing
@contained_geometry
def Boxy(TOP):
    TOP << phidlib.box()


def test_Boxy():
    lytest.utest_buds.test_root = os.path.join(os.path.dirname(phidlib.__file__), 'tests')
    difftest_it(Boxy)()
