__version__ = '0.0.5'

# quickplotters so you can debug more easily
try:
    import lyipc.client as ipc
    kqp = ipc.generate_display_function(None, 'debugging.gds')
except ImportError:
    def kqp(*args, **kwargs):
        print('klayout quickplot is not available.\nPlease install lyipc.')
try:
    from lyipc.client import load as ipc_load
except ImportError:
    def ipc_load(*args, **kwargs):
        pass

try:
    from phidl import quickplot2 as qp
except ImportError:
    def qp(*args, **kwargs):
        print('phidl does not seem to be installed, so you cannot use qp')


from lytest.kdb_xor import GeometryDifference, run_xor
from lytest.utest_buds import store_reference, difftest_it
from lytest.containers import contained_phidlDevice, contained_pyaCell, contained_script
import lytest.command_line