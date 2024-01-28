''' This is not run by pytest. It is run as a contained script in test_1_pyadevices.py '''
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import pya
import pyalib

layout = pya.Layout()
TOP = layout.create_cell('TOP')

pyalib.put_box(TOP, w=100)

layout.write('sample_layout.gds')
