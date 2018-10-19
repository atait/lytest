import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pyalib

import pya

layout = pya.Layout()
TOP = layout.create_cell('TOP')

pyalib.put_box(TOP, w=100)

layout.write('sample_layout.gds')