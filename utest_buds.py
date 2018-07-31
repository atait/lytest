from . kdb_xor import GeometryDifference, run_xor
from functools import wraps
import os


#: set this to specify reference directory. Default is current working directory
ref_layouts_dir = os.path.realpath('.')
#: set this to specify test directory. Default is current working directory
test_layouts_dir = os.path.realpath('.')


def get_reftest_filenames(testname):
    ''' Helps organize the typical testing setup where there are two directories 
        with corresponding reference and test versions of the same files
    '''
    ref_file = os.path.join(ref_layouts_dir, testname)
    test_file = os.path.join(test_layouts_dir, testname)
    if ref_layouts_dir == test_layouts_dir:
        ref_file += '-ref.gds'
        test_file +=  '-run.gds'
    else:
        ref_file += '.gds'
        test_file += '.gds'
    if not os.path.exists(ref_file):
        raise RuntimeError('Reference file {} does not exist.'.format(ref_file))
    return ref_file, test_file


def difftest_it(func):
    ''' Decorator. Runs an XOR after the function runs.
        The decorated function must take one argument that is a filename. It must save to it.
        This wrapper does not return. Instead it raises GeometryDifference if there are differences
    '''
    if func.__name__.startswith('test_'):
        testname = func.__name__[5:]
    else:
        testname = func.__name__
    @wraps(func)
    def wrapper(*args, **kwargs):
        ref_file, test_file = get_reftest_filenames(testname)
        func(test_file, *args, **kwargs)
        run_xor(ref_file, test_file, tolerance=10, verbose=False)
    return wrapper

