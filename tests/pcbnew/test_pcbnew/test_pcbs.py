import os
import lytest
from lytest import contained_pcbnewBoard, difftest_it
lytest.utest_buds.test_root = os.path.dirname(__file__)

@contained_pcbnewBoard
def simple_track(pcb):
    pcb.add_track([(1, 1), (2, 2)], layer='B.Cu')

def test_simple_track(): difftest_it(simple_track, file_ext='.kicad_pcb')()
