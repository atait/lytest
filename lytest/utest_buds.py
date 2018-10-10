from lytest.kdb_xor import GeometryDifference, run_xor
from functools import wraps
import os


try:
    from lyipc.client import load as ipc_load
except ImportError:
    def ipc_load(*args, **kwargs):
        pass


#: set this to specify reference directory. Default is current working directory
_ref_layouts_dir = None
#: set this to specify test directory. Default is current working directory
_test_layouts_dir = None


def set_layout_dirbase(path='.'):
    ''' This determines what the folders are called.
        They are sisters with fixed names.
    '''
    path = os.path.realpath(path)
    global _ref_layouts_dir, _test_layouts_dir
    _ref_layouts_dir = os.path.join(path, 'ref_layouts')
    _test_layouts_dir = os.path.join(path, 'run_layouts')


set_layout_dirbase()


def get_ref_dir():
    if _ref_layouts_dir is None:
        return None
    if not os.path.exists(_ref_layouts_dir):
        os.mkdir(_ref_layouts_dir)
        gitignore_file = os.path.join(_ref_layouts_dir, '.gitignore')
        with open(gitignore_file, 'w') as fx:
            fx.write('!*.gds\n!*.oas')
    return ref_layouts_dir


def get_test_dir():
    if _test_layouts_dir is None:
        return None
    if not os.path.exists(_test_layouts_dir):
        os.mkdir(_test_layouts_dir)
    return _test_layouts_dir


def store_reference(generator_func, extension='.gds'):
    basename = generator_func.__name__ + extension
    generator_func(out_file=os.path.join(get_ref_dir(), basename))


def difftest_it(func, reftest_ext=('.gds','.gds')):
    ''' Decorator. Runs an XOR after the function runs.
        The decorated/wrapped function must take at least one argument that is a filename. It must save to it.
        Other arguments can be passed through the wrapper function.
        This wrapper does not return. Instead it raises GeometryDifference if there are differences
    '''
    if func.__name__.startswith('test_'):
        testname = func.__name__[5:]
    else:
        testname = func.__name__

    if type(reftest_ext) is str:
        reftest_ext = (reftest_ext, reftest_ext)
    for ext in reftest_ext:
        if ext.lower() not in ['.gds', '.oas']:
            raise ValueError('Unrecognized layout format: {}'.format(ext))
    ref_file = os.path.join(get_ref_dir(), testname) + reftest_ext[0]
    test_file = os.path.join(get_test_dir(), testname) + reftest_ext[1]

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

