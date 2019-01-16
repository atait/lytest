import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pyalib

import lytest
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file

# Differencing
from lytest import difftest_it, store_reference
from lytest.containers import contained_pyaCell, contained_script

from test_0_pyacode import working_pya

# Begin actual device testing
@contained_pyaCell
def Boxypy(TOP):
    pyalib.put_box(TOP)


@working_pya
def test_Boxypy():
    lytest.utest_buds.test_root = os.path.join(os.path.dirname(pyalib.__file__), 'test_klayout')
    difftest_it(Boxypy, file_ext='.oas')()


import subprocess
@contained_script
def Boxxx():
    script_file = os.path.join(os.path.dirname(__file__), 'make_somepya.py')
    subprocess.check_call(['klayout', '-b', '-r', script_file])
    produced_file = 'sample_layout.gds'
    return produced_file

@working_pya
def test_Boxxx():
    lytest.utest_buds.test_root = os.path.join(os.path.dirname(pyalib.__file__), 'test_klayout')
    # First lets check whether klayout is installed and aliased to command line
    try:
        subprocess.check_call(['klayout', '-b'])
    except:
        return  # if not, then don't try to run the test
    difftest_it(Boxxx, file_ext='.gds')()
