[![Build Status](https://travis-ci.org/atait/lytest.svg?branch=master)](https://travis-ci.org/atait/lytest)

# lytest

Test automation tools for integrated circuit layout using klayout and pytest.


## Code testing
We don't know by inspection what code does. Determining its behavior involves running it. Is this behavior what we want? There are three basic questions:

1. Does the code run
2. Is its behavior correct
3. Has its behavior changed

Ideally, we want all of these questions answered precisely for a whole range of tests immediately after any code change. But code changes constantly. This issue is excellently addressed by `pytest`, an automated unit testing framework. In a single command, it scrolls through a bunch of test functions, makes sure they run, and makes some programmer-defined checks on behavior.


### Code for layout
Code for layout is different from regular code in that its behavior is the geometry it produces. It is difficult to state as text what the correct behavior is, so layouts must be reviewed by eye. This process takes a lot of time for even one complex layout; it is only as good as the reviewer's eyes and knowledge; and it cannot practically be done without hundreds of commits since the last review (from multiple collaborators), making it very hard to localize the origin of bugs.


### What lytest does
`lytest` addresses the layout behavior testing problem by fully automating a key part of layout review process: change detection. It combines the `pytest` automated testing framework with the `klayout` XOR differencing engine. If stored GDS reference files are deemed correct, then change detection is as good as answering the question of correctness.

A test consists of a fixed block of code that produces a GDSII (or OASIS) file. An initial run produces a reference layout. After review by a human, this file is then marked as the "correct" behavior for that block of code. When the tests are executed, the block runs again, producing a new "run" GDS. Differences in geometry (i.e. non-empty XORs) will raise an exception to the attention of whoever is conducting the test.


## Installation
```
pip install lytest
```
The first time you do this, it will take about 10 minutes to build klayout. Installation depends on pytest, klayout, and lygadgets -- these are automatically installed as dependencies via pip.


## Usage
There are three main parts: write the test, save the answer, run the test repeatedly.

### Write a test
A simple code test that is compatible with `pytest` looks like this.

```python
def test_addition():
    assert 1 + 1 == 2
```

There are two magic parts of `lytest` that make XOR testing about as simple: layout containers like `contained_XXX` and the XOR test decorator: `difftest_it`. Here is a complete test file in which we test the `waveguide` device from `my_library` (phidl language version).
```python
from lytest import contained_phidlDevice, difftest_it
import my_library as lib
@contained_phidlDevice
def BasicWaveguides(TOP):
    TOP.add_reference(lib.waveguide(width=0.5, length=20))

def test_BasicWaveguides(): difftest_it(BasicWaveguides)()
```

The "contained" function (BasicWaveguides) is *not* a pytest function. It takes an (empty) cell, modifies that cell, and returns nothing. Optional arguments are allowed. They cannot start with "test_" or end with "\_test". There is a bit of a magic associated with declaring and debugging contained layouts, discussed below. For now, just go with that way of thinking about it.

The pytest function (`test_BasicWaveguides`) is essentially just a renaming of `difftest_it` wrapping your contained geometry function. Difftest it implements compiling the test layout, the XOR test, and error reporting. All of these second functions have the exact same format, which is why they are written as one-liners. If you want to disable a test from running automatically with pytest, just comment out this second function.

Why two functions? The first is a normal-ish function. It can be called, examined, used to save to file. It is useful beyond being a test (see below). The second is run automatically and has a whole bunch of other things happening, such as the XOR testing itself.

#### Making it a better test
Put in a few permutations of arguments. Check corner cases. Maybe intentionally break it using `pytest.raises`.
```python
def BasicWaveguides(TOP):
    TOP.add_reference(lib.waveguide(width=0.5, length=20))
    wg2 = lib.waveguide(width=0.5, length=50)
    TOP.add_reference(wg2.rotate(90))
    with pytest.raises(ValueError):
        wg3 = lib.waveguide(width=-0.5, length=50)
```

### Save the answer
Reference layouts are stored in the "ref_layouts" directory. The first time you run a new test, it will put its result in ref_layouts, where it will be fixed. If that code changes and you run test again, it will raise a geometry difference error. So if you deem the new behavior to be correct, update the reference. This is done from command line:
```bash
lytest store test_geometries.py BasicWaveguides
```
replacing "test_geometries.py" with the filename and "BasicWaveguides" with whatever yours is called.

#### OASIS (optional)
This model necessitates tracking references layouts. They are large binaries that change often, which is a bad combination for version control schemes. The OASIS format is much more memory efficient. It is supported since v0.0.4 and can be selected in the `difftest_it` call (see klayout examples).


### Run the test
The terminal command `pytest [target]` will run the file target (a .py file). If target is a directory, it crawls through automatically running .py files that start with `test_` or end with `_test`. Within a file, pytest automatically calls every function starting with `test_` or ending with `_test`. If an exception is raised, it prints the stack trace but keeps going on to the next function.

You can also pick out a single test and run it with
```bash
lytest run test_geometries.py BasicWaveguides
```

#### Visualizing errors (optional)
[lyipc](https://github.com/atait/klayout-ipc) stands for klayout inter-process control, but it is essentially a visual debug tool. `lytest` and `lyipc` are designed to work together to give more visual information. During development, the contained geometry result is sent automatically to the GUI. During testing, failed tests are prepped for XOR in the GUI. Get it through the klayout salt Package Manager

### Continuous Integration (optional)
Continuous integration (CI) is when tests are run in an automated way in connection with a version control system. Every time a push is made to any branch, the branch is pulled into a virtual machine (located at travis-ci.org), and a predefined test suite is run. After a few minutes, github displays whether that branch is passing. lytest has CI and an example of how to set it up can be found in `.travis.yml`. Since klayout standalone takes a long time to build, it is recommended to turn on the caching option for pip.


## git integration
GDS and OASIS are binary formats, so they cannot be compared meaningfully by typical text diffs. This is really an issue with version control approaches because they rely on diffing across commits, staging areas, and branches. `lytest` effectively gives a way to diff layouts, so it can help. It only matters if it pops up the two files in klayout, so you need to have `lyipc` server active. This is cool, trust me.

### Setup
You need to configure your own git system to enable it. This is simply done by
```bash
lytest git-config
```
You can also do this project-by-project using the `--local` flag.

And then you can do things like
```bash
git diff feature-branch tests/ref_layouts/
```
to see all the differences go over to the klayout GUI.

# The lytest/lyipc/ipython test-driven workflow
I currently use this workflow when developing new device cells (as opposed to system-level cells - a different workflow). It is a graphical layout version of test-driven design. It is enabled by some of the tools in lytest.

Whenever you write a new function, you call it with various options in order to develop it and understand what its doing. You come up with a mixture of library behavior and usgage calls that you like. If you save those calls in the right place, you have made a *test*!

### Tools and setup
[lyipc](https://github.com/atait/klayout-ipc) (klayout inter-process control)
- like quickplot for the klayout window, hence "kqp"
- kqp sends intermediate layouts at run time from the debugger to the klayout GUI
- lyipc is also used to automatically bring up failed XOR tests so that XOR results can be visualized

[pdb](https://docs.python.org/3/library/pdb.html) (python debugger)
- terminal-based, as lightweight as it gets
- set breakpoint with `import pdb; pdb.set_trace()`
- you can call quickplot or kqp (`klayout_quickplot`) from it
- recommended: [pdb++](https://pypi.org/project/pdbpp/)

ipython (interactive python)
- an upgraded command line shell
- close interaction with changing code, autoreloading
- turn autoreload on by default by putting
```python
print('autoreload is on')
%load_ext autoreload
%autoreload 2
```
in `~/.ipython/profile_default/startup/auto_reloader.ipy`

### The process
Let's say you want to design a qubit. After setting out your goals on paper, start by making a container function with some basic behavior
```python
# test_qubits.py
from lytest import contained_phidlDevice, difftest_it
import my_library as lib

@contained_phidlDevice
def SomeQubits(TOP):
    TOP << lib.qubit()

# def test_SomeQubits(): difftest_it(SomeQubits)()
```
and the corresponding library function
```python
# my_library.py
...
def qubit():
    D = Device('qubit')
    # geometry goes here
    return D
...
```

Activate the lyIPC server in klayout GUI. Open up an ipython shell (with autoreload on). Add some behavior to the library function. To see what this did,
```python
[1] %load_ext autoreload
[2] %autoreload 2
[3] from test_qubits import SomeQubits
[4] SomeQubits()
```
voila. Your contained layout has appeared in your klayout GUI.

Change the library behavior. Call it again
```python
[3] SomeQubits()
```
voila! The *new* behavior appears. No reloading all of the overhead or dealing with layout boilerplate. This call can be repeated every time you save the library.

As you are developing, there might be some call combinations that are very relevant. Keep those. You might end up with
```python
# test_qubits.py
...
@contained_phidlDevice
def SomeQubits(TOP):
    TOP << lib.qubit()
    TOP << lib.qubit(detuing=100e6).movey(100)
    TOP << lib.qubit(local_realistic=True).movex(100)
...
```

Finally, when you are satisfied with the library behavior, turn it into a test that is run automatically, telling all your collaborators - hey, don't change anything that ends up breaking the `SomeQubits` container. To do this, just uncomment the line above that has difftest_it.

## What is this container thing?
A layout "container" appears different from the outside vs. the inside. From the outside, it is a function. It has one optional argument that is a filename. When called, it makes a layout and saves it to that file. From the outside, containers are not language specific. The caller does not know if phidl, pya, or some other geometry language is being used.

The container can be used in different ways. Sometimes that layout gets saved to a file, otherwise it is sent for quickplotting or used in a XOR test. The critical thing is that the geometry code inside of the container remains identical no matter how we want to use it.

From the inside, the container looks completely different. It appears to receive – not a filename – but python objecs: a Cell (pya) or Device (phidl). So the container is also a wrapper that takes care of the set up and tear down associated with turning geometry commands into a complete layout. Script containers are not pya or phidl specific. They contain arbitrary code that produces a file and must return that filename to be found by the container.


## Todo
- use PCell in the pya examples
- warn when that extra parentheses is not there after difftest_it


#### Authors: Alex Tait, Adam McCaughan, Sonia Buckley, Jeff Chiles, Jeff Shainline, Rich Mirin, Sae Woo Nam
#### National Institute of Standards and Technology, Boulder, CO, USA
