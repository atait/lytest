''' Store new references from command line
'''
import os
import argparse
from lytest import __version__, store_reference
import importlib.util

parser = argparse.ArgumentParser(description="lygadgets linkers between klayout and system namespaces")
parser.add_argument('testfile', type=argparse.FileType('r'),
                    help='the file in which the test resides')
parser.add_argument('testname', type=str,
                    help='name of the test')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s v{__version__}')


def cm_store_ref():
    args = parser.parse_args()
    import pdb; pdb.set_trace()

    # Import the module from the source of that file
    modulename = os.path.splitext(os.path.basename(args.testfile.name))[0]
    spec = importlib.util.spec_from_file_location(modulename, args.testfile.name)
    test_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(test_module)
    except Exception as err:
        raise ImportError('Error loading ' + str(testfile.name))
    test_function = getattr(test_module, args.testname)
    store_reference(test_function)
    print('Success')