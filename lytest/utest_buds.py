from lytest.kdb_xor import GeometryDifference, run_xor
from functools import wraps
import os


from lytest import ipc_load


#: Set this attribute depending on where you want to do the testing
test_root = '.'

def get_ref_dir():
    ''' This does the path joining of course, and also creates the right setup if not present '''
    ref_layouts_dir = os.path.realpath(os.path.join(test_root, 'ref_layouts'))
    if not os.path.exists(ref_layouts_dir):
        os.mkdir(ref_layouts_dir)
        gitignore_file = os.path.join(ref_layouts_dir, '.gitignore')
        with open(gitignore_file, 'w') as fx:
            fx.write('!*.gds\n!*.oas')
    return ref_layouts_dir


def get_test_dir():
    ''' This does the path joining of course, and also creates the right setup if not present '''
    test_layouts_dir = os.path.realpath(os.path.join(test_root, 'run_layouts'))
    if not os.path.exists(test_layouts_dir):
        os.mkdir(test_layouts_dir)
    return test_layouts_dir


def store_reference(generator_func, extension='.gds'):
    basename = generator_func.__name__ + extension
    generator_func(out_file=os.path.join(get_ref_dir(), basename))


def difftest_it(func, file_ext='.gds'):
    ''' Decorator. Runs an XOR after the function runs.
        The decorated/wrapped function must take at least one argument that is a filename. It must save to it.
        Other arguments can be passed through the wrapper function.
        This wrapper does not return. Instead it raises GeometryDifference if there are differences
    '''
    testname = func.__name__
    if file_ext.lower() not in ['.gds', '.oas']:
        raise ValueError('Unrecognized layout format: {}'.format(file_ext))
    ref_file = os.path.join(get_ref_dir(), testname) + file_ext
    test_file = os.path.join(get_test_dir(), testname) + file_ext

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(ref_file):
            print('Warning reference does not exist. Creating it and an initial test')
            func(ref_file, *args, **kwargs)
        func(test_file, *args, **kwargs)
        try:
            run_xor(ref_file, test_file, tolerance=1, verbose=False)
        except GeometryDifference:
            ipc_load(ref_file, mode=1)
            ipc_load(test_file, mode=2)
            raise
    return wrapper

