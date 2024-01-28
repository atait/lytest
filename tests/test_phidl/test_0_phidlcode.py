import os
import sys
from conftest import requires_phidl

@requires_phidl
def test_imports():
    ''' See if it imports '''
    import phidlib
