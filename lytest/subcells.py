''' Here is the workflow of this file:

    The subcell decorator splits a function into two
    - One will be produced and registered for main layout if being_added is True
    - One is easily examined by a human with lyipc installed
'''
from functools import wraps

try:
    import lyipc.client as ipc
    kqp = ipc.generate_display_function(None, 'debugging.gds')
except ImportError:
    def kqp(*args, **kwargs):
        pass

# See the ports go through to the gds
# Comment if its breaking. Then update OLMAC PDK
from phidl import Port
from nc_constants import lys
# Port.port_layer = lys['ports']  # This line breaks stuff in gdspy, but only when run by pytest


# Put the subcells in a list so that they can be packed at the end
global all_cell_functions
all_cell_functions = []
def subcell(being_added=True, cell_function_list=None):
    ''' Magic patching.
        Old function is inserted into the list of things to put on chip (if being_added is True)

        Returned function will auto-quickplot when it is called by name. Debug it

        subcell must return a Device and have no arguments
    '''
    if cell_function_list is None:
        global all_cell_functions
        cell_function_list = all_cell_functions
    def subcell_inner(func):
        @wraps(func)
        def procedure_wrapper():
            device_out = func()
            # Cache stuff
            return device_out

        @wraps(func)
        def human_wrapper():
            device_out = func()
            kqp(device_out, fresh=True)
            return device_out

        if being_added:
            cell_function_list.append(procedure_wrapper)
        return human_wrapper
    return subcell_inner