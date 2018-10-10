# lytest
Unit-testing tools for integrated circuit layout

Uses klayout's standalone python modules and pytest.

## A big part of this is workflow
See test_1_components.py for an example.

There are functions that generate layouts of interest.
- They are NOT pytest functions. They cannot start with 'test_' or end with '_test'.
- Their first argument MUST be a filename. They must write some kind of layout to this file.
- They CAN take other arguments after the filename.

There are functions that perform the tests.
- These simply decorate the generating functions with a difference test
- They ARE pytest functions that will be run automatically

Why separate into two functions?
- First one is isolated, regular. Can be used to update references one-by-one.
- Second one can be run automatically with access to the unit-test goodies offered by pytest (e.g. coverage)

Why not put all diffs into one pytest function?
- Each pytest function stops on an exception, but different functions do not.
- Prevents one error in an early device shadow those happening in other devices.
- Can realistically only cover default arguments
- Does not document actual usage


## Recommended workflow for device/test development
When you write a new function, you call it with various options to make sure it's working. Testing more or less means saving those calls in the right place.

### Dependencies
pdb (python debugger)
- terminal-based, as lightweight as it gets
- set breakpoint with `import pdb; pdb.set_trace()`
- you can call quickplot or kqp (klayout_quickplot) from it
- documentation [here](https://docs.python.org/3/library/pdb.html)
- builtin

pdb++
- general upgrades to pdb. drops in seamlessly
- customize it to your liking with `~/.pdbrc.py`
- documentation [here](https://pypi.org/project/pdbpp/)
- `pip install pdbpp`

ipython
- an upgraded command line shell
- close interaction with changing code
- prevents unnecessary reloading
- `pip install ipython`
- turn autoreload on by default by putting
```python
print('autoreload is on')
%load_ext autoreload
%autoreload 2
```
in `~/.ipython/profile_default/startup/auto_reloader.ipy`

lyipc
- like quickplot for the klayout window
- technically quickplot is enough, but it's having trouble with ipython
- follow instructions on the [github page](https://github.com/atait/klayout-ipc)


## Goals of testing
1. Make sure code is not raising error
    - Just needs to run
2. See if code changes affected layout behavior
    - Needs XOR testing


## Writing tests
#### Minimal template
```python
import nc_library as lib
@contained_geometry
def N_tron(TOP):
    TOP << lib.ntron()

def test_N_tron(): difftest_it(N_tron)()
```

#### Developing a new test
1. Copy-paste this template into one of the test_*.py files
2. Replace `lib.ntron` with whatever device producing function you'd like to test
3. Rename `N_tron` and `test_N_tron`

#### Saving its reference
This is done automatically the first time that pytest encounters it.

#### Changing its reference
From command line:
```bash
python -c "from test_superconductor import *; store_reference(N_tron)"
```
but replace "test_superconductor" with the filename and "N_tron" with whatever yours is called.

#### Making it a better test
Put in a few permutations of arguments. Check corner cases. Maybe intentionally break it using `pytest.raises`.
```python
def N_tron(TOP):
    TOP << lib.ntron(layer=lys['m2_nw'])
    TOP << lib.ntron(channel_width=.5, gate_width=.3, layer=lys['m2_nw']).movex(20)
    with pytest.raises(ValueError):
        TOP << lib.ntron(channel_width=-50)
```

## Dependency
These will be installed automatically when you install lytest.

### pytest
The terminal command `pytest [target]` will run the file target (a .py file). If target is a directory, it crawls through automatically running .py files that start with `test_` or end with `_test`.

Within a file, pytest automatically calls every function starting with `test_` or ending with `_test`. If an exception is raised, it prints the stack trace but keeps going on to the next function.

### klayout
This is now on PyPI, so you have to have it now.

### lyipc (optional)
Gives more visual information. During development, the contained geometry result is sent automatically to the GUI. During testing, failed tests are prepped for XOR in the GUI.

Get it through the klayout salt Package Manager


## Todo

- command line entry points
    - done
- template for CI integration.
- OASIS
- what if you could `kdb_xor` across git commits/branches
- use PCell in the pya examples
- import pya from lygadgets. See if it detects the installed kdb.
    - done


#### Authors: Alex Tait, Adam McCaughan, Sonia Buckley, Jeff Chiles, Jeff Shainline, Rich Mirin, Sae Woo Nam
#### National Institute of Standards and Technology, Boulder, CO, USA
