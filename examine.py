# call this with klayout -r examine.py -rd comp=Bragg_gratings

''' New idea for this file

    It seems hard to launch the rdb from command line.

    What if instead, it looked in the run and ref directories looking for everything that had a match.
    It then goes in klayout and opens every pair in a different layout view.
    Easy to examine, one button away from a full diff being done in RDB.
'''

import pya

def gui_read(filename):
    ''' Gets a layout from a file and returns it top cell

        Also opens it in the main window
    '''
    main = pya.Application.instance().main_window()
    view = main.load_layout(filename, 2)
    top = view.cell
    return top


def run_diff(file1='allDevices_reference.gds', file2='allDevices_trial.gds'):
    topcell_ref = gui_read(file1)
    topcell_trial = gui_read(file2)
    difftool = pya.LayoutDiff()
    retval = difftool.compare(topcell_ref, topcell_trial, difftool.Verbose, 10)
    pya.Application.execute(pya.Application.instance())


if __name__ == '__main__':
    global comp
    ref_file = 'ref_layouts/' + comp + '.gds'
    test_file = 'run_layouts/' + comp + '.gds'
    ret = run_diff(ref_file, test_file)
    pya.Application.execute(pya.Application.instance())
