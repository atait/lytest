# lytest
Unit-testing tools for integrated circuit layout

Uses klayout's standalone python modules

Uses pytest (`pip install pytest`). Run all tests with `pytest tests`.

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
