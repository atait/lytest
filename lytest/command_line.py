''' Store new references from command line
'''
import os
import argparse
from lytest import __version__, store_reference, ipc_load
from lytest.kdb_xor import run_xor, GeometryDifference
import importlib.util


_loaded_modules = dict()
def load_attribute_fromfile(filename, attr):
    # Import the module from the source of that file, then get an attribute
    modulename = os.path.splitext(os.path.basename(filename))[0]
    if modulename not in _loaded_modules:
        spec = importlib.util.spec_from_file_location(modulename, filename)
        the_module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(the_module)
        except Exception as err:
            raise ImportError('Error loading ' + str(testfile.name))
        _loaded_modules[modulename] = the_module
    the_module = _loaded_modules[modulename]
    return getattr(the_module, attr)



parser = argparse.ArgumentParser(description="lytest entry points for storing references and running difftest_it")
parser.add_argument('testfile', type=argparse.FileType('r'),
                    help='the file in which the test resides')
parser.add_argument('testname', type=str,
                    help='name of the test')
parser.add_argument('-v', '--version', action='version', version='%(prog)s v{}'.format(__version__))


def cm_store_ref():
    args = parser.parse_args()
    test_function = load_attribute_fromfile(args.testfile.name, args.testname)
    store_reference(test_function)
    print('Success')


def cm_xor_test():
    args = parser.parse_args()
    # make sure we get the difftest_it kind
    func_name = args.testname
    if func_name.startswith('test_') or func_name.endswith('_test'):
        pass  # good to go
    else:
        for func_name_try in ['test_' + func_name, func_name + '_test']:
            try:
                load_attribute_fromfile(args.testfile.name, func_name_try)
                break
            except AttributeError:
                pass
        else:
            raise AttributeError('No pytest-able version of this attribute was found')
        func_name = func_name_try

    difftesting_function = load_attribute_fromfile(args.testfile.name, func_name)
    difftesting_function()
    print('Success')


# File based diff
filebased_parser = argparse.ArgumentParser(description="file-based diff integrated with klayout")
filebased_parser.add_argument('lyfile1', type=argparse.FileType('r'),
                    help='First layout file (GDS or OAS)')
filebased_parser.add_argument('lyfile2', type=argparse.FileType('r'),
                    help='Second layout file (GDS or OAS)')
filebased_parser.add_argument('-v', '--version', action='version', version='%(prog)s v{}'.format(__version__))


def cm_diff():
    args = filebased_parser.parse_args()
    for file in [args.lyfile1, args.lyfile2]:
        file_ext = os.path.splitext(file.name)[1]
        if file_ext.lower() not in ['.gds', '.oas']:
            raise ValueError('Unrecognized layout format: {}'.format(file_ext))
    ref_file = args.lyfile1.name
    test_file = args.lyfile2.name
    try:
        run_xor(ref_file, test_file, tolerance=1, verbose=False)
    except GeometryDifference:
        print('These layouts are different.')
        ipc_load(ref_file, mode=1)
        ipc_load(test_file, mode=2)

