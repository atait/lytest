import os
import sys
import pytest

# See what can be tested
try:
    from lygadgets import pya
except ImportError:
    pya = None

try:
    import phidl
    import lygadgets
except ImportError:
    phidl = None

try:
    from kigadgets import pcbnew_bare as pcbnew
except ImportError:
    pcbnew = None

requires_pya = pytest.mark.skipif(pya is None, reason='pya not present')
requires_phidl = pytest.mark.skipif(phidl is None, reason='phidl not present')
requires_pcbnew = pytest.mark.skipif(pcbnew is None, reason='kigadgets not present')


# Add paths
test_dir = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(test_dir, 'test_klayout'))
sys.path.insert(0, os.path.join(test_dir, 'test_phidl'))
sys.path.insert(0, os.path.join(test_dir, 'test_kicad'))
