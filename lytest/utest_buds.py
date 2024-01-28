from lytest.kdb_xor import GeometryDifference, run_xor
from functools import wraps
import shutil
import os


from lytest import ipc_load


#: Set this attribute depending on where you want to do the testing
test_root = "."
default_file_ext = ".gds"


def get_ref_dir():
    """This does the path joining of course, and also creates the right setup if not present"""
    ref_layouts_dir = os.path.realpath(os.path.join(test_root, "ref_layouts"))
    if not os.path.exists(ref_layouts_dir):
        os.mkdir(ref_layouts_dir)
        gitignore_file = os.path.join(ref_layouts_dir, ".gitignore")
        with open(gitignore_file, "w") as fx:
            fx.write("!*.gds\n!*.oas\n*.kicad_*\n!*.kicad_pcb\n")
    return ref_layouts_dir


def get_src_dir():
    """ src_dir must be created manually """
    src_layouts_dir = os.path.realpath(os.path.join(test_root, "src_layouts"))
    if os.path.exists(src_layouts_dir):
        gitignore_file = os.path.join(src_layouts_dir, ".gitignore")
        if not os.path.exists(gitignore_file):
            with open(gitignore_file, "w") as fx:
                fx.write("!*.gds\n!*.oas\n*.kicad_*\n!*.kicad_pcb\n")
    return src_layouts_dir


def get_test_dir():
    """This does the path joining of course, and also creates the right setup if not present"""
    test_layouts_dir = os.path.realpath(os.path.join(test_root, "run_layouts"))
    if not os.path.exists(test_layouts_dir):
        os.mkdir(test_layouts_dir)
        gitignore_file = os.path.join(test_layouts_dir, ".gitignore")
        with open(gitignore_file, "w") as fx:
            fx.write("*.gds\n*.oas\n*.kicad_*\n")
    return test_layouts_dir


def store_reference(generator_func, extension=".gds"):
    basename = generator_func.__name__ + extension
    generator_func(out_file=os.path.join(get_ref_dir(), basename))


def difftest_it(func, file_ext=None):
    """Decorator. Runs an XOR after the function runs.
    The decorated/wrapped function must take at least one argument that is a filename. It must save to it.
    Other arguments can be passed through the wrapper function.
    This wrapper does not return. Instead it raises GeometryDifference if there are differences
    """
    testname = func.__name__
    if file_ext is None:
        file_ext = default_file_ext
    if file_ext.lower() not in [".gds", ".oas", ".kicad_pcb"]:
        raise ValueError("Unrecognized layout format: {}".format(file_ext))
    ref_file = os.path.join(get_ref_dir(), testname) + file_ext
    test_file = os.path.join(get_test_dir(), testname) + file_ext
    src_file = os.path.join(get_src_dir(), testname) + file_ext
    if not os.path.isfile(src_file):
        src_file = None

    @wraps(func)
    def wrapper(*args, **kwargs):
        func(test_file, *args, in_file=src_file, **kwargs)
        if not os.path.exists(ref_file):
            print("Warning reference does not exist. Creating it and an initial test")
            shutil.copyfile(test_file, ref_file)
        try:
            run_xor(ref_file, test_file, tolerance=1, hash_geom=True, verbose=False)
        except GeometryDifference:
            ipc_load(ref_file, mode=1)
            ipc_load(test_file, mode=2)
            raise

    return wrapper
