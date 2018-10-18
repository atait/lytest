import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pyalib

import lytest
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file

# Differencing
from lytest import difftest_it, store_reference
from lytest.containers import contained_pyaCell, contained_script



# Begin actual device testing
@contained_pyaCell
def Boxypy(TOP):
    pyalib.put_box(TOP)


def test_Boxypy():
    lytest.utest_buds.test_root = os.path.join(os.path.dirname(pyalib.__file__), 'tests')
    difftest_it(Boxypy, file_ext='.oas')()


import subprocess
@contained_script
def Boxxx():
    subprocess.call(['klayout', '-b', '-r', 'make_somepya.py'])
    return 'sample_layout.gds'
