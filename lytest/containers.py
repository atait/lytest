from functools import wraps
from contextlib import contextmanager
from shutil import copyfile

from lytest import kqp, ipc_load


@contextmanager
def phidl_context(device_name=None, out_file=None):
    ''' Handles a conditional write to file or send over lyipc connection.
        The context manager yields a new empty Device.
        The context block then modifies that device by adding references to it. It does not need to return anything.
        Back to the context manager, the Device is saved if out_file is not None, or it is sent over ipc

        Example::

            with phidl_context(out_file='my_box.gds') as D:
                r = D << phidl.geometry.rectangle(size=(10, 10), layer=1)
                r.movex(20)

        will write the device with a rectangle to a file called 'my_box.gds' and do nothing with lyipc.
        By changing out_file to None, it will send an ipc load command instead of writing to a permanent file,
        (Although ipc does write a file to be loaded by klayout, it's name or persistence is not guaranteed.)
    '''
    from phidl import Device
    TOP = Device('TOP')
    yield TOP
    if out_file is None:
        kqp(TOP, fresh=True)
    else:
        TOP.write_gds(out_file)


@contextmanager
def pya_context(cell_name=None, out_file=None):
    ''' Handles a conditional write to file or send over lyipc connection.
        See phidl_context above.
    '''
    from lygadgets import pya
    layout = pya.Layout()
    TOP = layout.create_cell('TOP')
    yield TOP
    if out_file is None:
        kqp(TOP, fresh=True)
    else:
        layout.write(out_file)


def contained_arbitrary(func, layout_context):
    '''
        Converts a function that takes a Device argument to one that takes a filename argument.
        This is used to develop fixed geometry creation blocks and then save them as reference files.
        Bad idea to try to use this in a library or call it from other functions.

        func should take *only one* argument that is a Device, modify that Device, and return nothing.

        It's sort of a decorator version of save_or_visualize.
        When called with a None argument, it will use klayout_quickplot.

        Example::

            @contained_geometry
            def boxer(D):
                r = D << phidl.geometry.rectangle(size=(10, 10), layer=1)
                r.movex(20)

        Usage::

            boxer()  # displays in klayout over ipc
            boxer('temp.gds')  # saves to file instead
    '''
    @wraps(func)
    def geometry_container(out_file=None):
        with layout_context(out_file=out_file) as TOP:
            func(TOP)
    return geometry_container


contained_phidlDevice = lambda func: contained_arbitrary(func, phidl_context)
contained_pyaCell = lambda func: contained_arbitrary(func, pya_context)


def contained_script(func):
    @wraps(func)
    def script_container(out_file=None):
        produced_file = func()
        if out_file is None:
            ipc_load(produced_file)
        else:
            copyfile(produced_file, out_file)
    return script_container
