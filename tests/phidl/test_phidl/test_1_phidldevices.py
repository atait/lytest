import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import phidlib

import lytest
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file

# Differencing
from lytest import difftest_it, store_reference
from lytest.containers import contained_phidlDevice


# Begin actual device testing
@contained_phidlDevice
def Boxy(TOP):
    TOP << phidlib.box()


def test_Boxy():
    lytest.utest_buds.test_root = os.path.join(os.path.dirname(phidlib.__file__), 'test_phidl')
    difftest_it(Boxy)()

    # Now test that the fallback works
    lytest.utest_buds.run_xor = lytest.kdb_xor.run_xor_phidl
    difftest_it(Boxy, file_ext='.gds')()
    lytest.utest_buds.run_xor = lytest.kdb_xor.run_xor