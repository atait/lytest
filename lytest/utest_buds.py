from lytest.kdb_xor import GeometryDifference, run_xor
from functools import wraps
import os

try:
    from lyipc.client import load as ipc_load
except ImportError:
    def ipc_load(*args, **kwargs):
        pass


#: set this to specify reference directory. Default is current working directory
ref_layouts_dir = None
#: set this to specify test directory. Default is current working directory
test_layouts_dir = None


def set_layout_dirbase(path='.'):
    path = os.path.realpath(path)
    global ref_layouts_dir, test_layouts_dir
    ref_layouts_dir = os.path.join(path, 'ref_layouts')
    test_layouts_dir = os.path.join(path, 'run_layouts')


set_layout_dirbase()


def get_reftest_filenames(testname):
    ''' Helps organize the typical testing setup where there are two directories
        with corresponding reference and test versions of the same files
    '''
    if not os.path.exists(ref_layouts_dir):
        raise RuntimeError('Reference directory does not exist.\n'
                           'Make {} and put in a .gitignore for !*.gds'.format(ref_layouts_dir))
    ref_file = os.path.join(ref_layouts_dir, testname)
    test_file = os.path.join(test_layouts_dir, testname)
    if ref_layouts_dir == test_layouts_dir:
        ref_file += '-ref.gds'
        test_file +=  '-run.gds'
    else:
        ref_file += '.gds'
        test_file += '.gds'
    return ref_file, test_file


def store_reference(generator_func):
    basename = generator_func.__name__ + '.gds'
    generator_func(out_file=os.path.join(ref_layouts_dir, basename))


def difftest_it(func):
    ''' Decorator. Runs an XOR after the function runs.
        The decorated/wrapped function must take at least one argument that is a filename. It must save to it.
        Other arguments can be passed through the wrapper function.
        This wrapper does not return. Instead it raises GeometryDifference if there are differences
    '''
    if func.__name__.startswith('test_'):
        testname = func.__name__[5:]
    else:
        testname = func.__name__
    @wraps(func)
    def wrapper(*args, **kwargs):
        ref_file, test_file = get_reftest_filenames(testname)
        if not os.path.exists(ref_file):
            print('Warning reference does not exist. Creating it')
            func(ref_file, *args, **kwargs)
            return
        func(test_file, *args, **kwargs)
        try:
            run_xor(ref_file, test_file, tolerance=10, verbose=False)
        except GeometryDifference:
            ipc_load(ref_file, mode=1)
            ipc_load(test_file, mode=2)
            raise
    return wrapper

