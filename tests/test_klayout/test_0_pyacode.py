from conftest import requires_pya

@requires_pya
def test_imports():
    ''' See if it imports '''
    import pyalib
