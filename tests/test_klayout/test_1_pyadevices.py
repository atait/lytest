import os
from conftest import pya
import pytest

if pya is None:
    pytest.skip('Module import requires pya', allow_module_level=True)

import pyalib

# Differencing
import lytest
from lytest import difftest_it, store_reference
from lytest.containers import contained_pyaCell, contained_script
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file


# Begin actual device testing
@contained_pyaCell
def Boxypy(TOP):
    pyalib.put_box(TOP)


def test_Boxypy():
    lytest.utest_buds.test_root = os.path.dirname(__file__)
    difftest_it(Boxypy, file_ext='.oas')()

    # Now test that the fallback works
    lytest.utest_buds.run_xor = lytest.kdb_xor.run_xor_phidl
    difftest_it(Boxypy, file_ext='.oas')()
    lytest.utest_buds.run_xor = lytest.kdb_xor.run_xor


import subprocess
@contained_script
def Boxxx():
    script_file = os.path.join(os.path.dirname(__file__), 'make_somepya.py')
    subprocess.check_call(['klayout', '-b', '-r', script_file])
    return 'sample_layout.gds'


def test_Boxxx():
    lytest.utest_buds.test_root = os.path.dirname(__file__)
    # First lets check whether klayout is installed and aliased to command line
    try:
        subprocess.check_call(['klayout', '-b'])
    except:
        return  # if not, then don't try to run the test
    difftest_it(Boxxx, file_ext='.gds')()
