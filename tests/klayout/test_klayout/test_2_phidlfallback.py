import os
import lytest
import pyalib
from lytest.containers import contained_pyaCell

@contained_pyaCell
def Boxypy(TOP):
    pyalib.put_box(TOP)


# def test_Boxypy():
#     # In the previous test (test_1_pyadevices.py), run_layouts/Boxypy.oas was regenerated
#     # We will reuse that and just do a XOR on the files
#     # xor_filename = 'Boxypy.gds'
#     xor_filename = 'Boxypy.oas'  # switch to this one once phidl supports OASIS
#     ref_file = os.path.join(os.path.dirname(__file__), 'ref_layouts', xor_filename)
#     run_file = os.path.join(os.path.dirname(__file__), 'run_layouts', xor_filename)

#     # make it look like klayout is not installed
#     # import lygadgets
#     # lygadgets.environment.pya = None
#     # lygadgets.pya = None

#     # Do the XOR, which should trigger the phidl implementation
#     from lytest.kdb_xor import run_xor_phidl
#     run_xor_phidl(ref_file, run_file)

def test_Boxypy():
    lytest.utest_buds.test_root = os.path.join(os.path.dirname(pyalib.__file__), 'test_klayout')
    lytest.kdb_xor.run_xor = lytest.kdb_xor.run_xor_phidl
    lytest.difftest_it(Boxypy, file_ext='.oas')()
