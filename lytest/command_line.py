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


top_parser = argparse.ArgumentParser(description='lytest main command-line entry point')
top_parser.add_argument('command', type=str, choices=['store', 'diff', 'test', 'git-config'],
                    metavar='<command>', help='Type "lytest <command> -h" for help on specific commands')
top_parser.add_argument('args', nargs=argparse.REMAINDER)
top_parser.add_argument('-v', '--version', action='version', version='%(prog)s v{}'.format(__version__))

def cm_main():
    args = top_parser.parse_args()
    if args.command == 'store':
        cm_store_ref(args.args)
    # elif args.command == 'diff':
    #     config_main(args.args)


store_parser = argparse.ArgumentParser(prog='lytest store', description="lytest entry points for storing references and running difftest_it")
store_parser.add_argument('testfile', type=argparse.FileType('r'),
                    help='the file in which the test resides')
store_parser.add_argument('testname', type=str,
                    help='name of the test')


def cm_store_ref(args):
    store_args = store_parser.parse_args(args)
    test_function = load_attribute_fromfile(store_args.testfile.name, store_args.testname)
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
            raise ValueError('Unrecognized layout format: {}'.format(file.name))
    ref_file = args.lyfile1.name
    test_file = args.lyfile2.name
    try:
        run_xor(ref_file, test_file, tolerance=1, verbose=False)
    except GeometryDifference:
        print('These layouts are different.')
        ipc_load(ref_file, mode=1)
        ipc_load(test_file, mode=2)


# git integration
git_parser = argparse.ArgumentParser(description="file-based diff integrated with klayout")
git_parser.add_argument('path')
git_parser.add_argument('lyfile1', type=argparse.FileType('r'),
                    help='First layout file (GDS or OAS)')
git_parser.add_argument('hash1')
git_parser.add_argument('mode1')
git_parser.add_argument('lyfile2', type=argparse.FileType('r'),
                    help='Second layout file (GDS or OAS)')
git_parser.add_argument('hash2')
git_parser.add_argument('mode2')
git_parser.add_argument('similarity', nargs='*')
git_parser.add_argument('-v', '--version', action='version', version='%(prog)s v{}'.format(__version__))

def cm_gitdiff():
    ''' This no longer has an entry point '''
    args = git_parser.parse_args()
    if len(args.similarity) > 0:
        print('Refusing to process similar files without the same name')
        print('\n'.join(args.similarity[1:]))
        return
    for file in [args.lyfile1, args.lyfile2]:
        if args.mode2 is None or file.name == '/dev/null':  # what is this on windows?
            print('File {} does not exist on both commits'.format([args.lyfile1.name, args.lyfile2.name]))
            return
        file_ext = os.path.splitext(file.name)[1]
        if file_ext.lower() not in ['.gds', '.oas']:
            raise ValueError('Unrecognized layout format: {}'.format(file.name))
    ref_file = args.lyfile1.name
    test_file = args.lyfile2.name
    try:
        run_xor(ref_file, test_file, tolerance=1, verbose=False)
    except GeometryDifference:
        print('Layouts differ:')
        print('  ', test_file)
        print('  ', ref_file)
        ipc_load(ref_file, mode=1)
        ipc_load(test_file, mode=2)

