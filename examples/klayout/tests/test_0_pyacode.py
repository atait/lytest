import os
import sys
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lygadgets import pya
working_pya = pytest.mark.skipif(pya is None,
                                 reason="There is something very wrong. Install of klayout failed, even though it is a requirement of this package")

@working_pya
def test_imports():
    ''' See if it imports '''
    import pyalib