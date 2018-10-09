# quickplotters so you can debug more easily
try:
    import lyipc.client as ipc
    kqp = ipc.generate_display_function(None, 'debugging.gds')
except ImportError:
    def kqp(*args, **kwargs):
        print('klayout quickplot is not available.\nPlease install lyipc.')

try:
    from phidl import quickplot2 as qp
except ImportError:
    def qp(*args, **kwargs):
        print('phidl does not seem to be installed, so you cannot use qp')


from lytest.kdb_xor import *
from lytest.utest_buds import *
from lytest.nonvisual import *
