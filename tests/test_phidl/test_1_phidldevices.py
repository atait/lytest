import os
from conftest import requires_pya, phidl
import pytest

if phidl is None:
    pytest.skip('Module import requires phidl', allow_module_level=True)

from phidl import geometry as pg
import phidlib

# Differencing
import lytest
from lytest import difftest_it, store_reference, xor_polygons_phidl
from lytest.containers import contained_phidlDevice
from lytest.phidl_oas import write_oas, import_oas
from lytest import qp, kqp  # not used for testing. Used if you want to debug this file


# Begin actual device testing
@contained_phidlDevice
def Boxy(TOP):
    TOP << phidlib.box()


def test_Boxy():
    lytest.utest_buds.test_root = os.path.dirname(__file__)
    difftest_it(Boxy)()

    # Now test that the fallback works
    lytest.utest_buds.run_xor = lytest.kdb_xor.run_xor_phidl
    difftest_it(Boxy, file_ext='.gds')()
    lytest.utest_buds.run_xor = lytest.kdb_xor.run_xor


def test_phidlXOR():
    ref_file = os.path.join(os.path.dirname(__file__), 'ref_layouts', 'Boxy.gds')
    TOP1 = phidlib.box()
    TOP2 = pg.import_gds(ref_file)
    TOP_different = phidlib.box(width=100)
    for hash_geom in [True, False]:
        XOR = xor_polygons_phidl(TOP1, TOP2, hash_geom=hash_geom)
        if len(XOR.flatten().get_polygons()) > 0:
            raise GeometryDifference("Differences found between phidl Devices.")
        XOR_different = xor_polygons_phidl(TOP_different, TOP2, hash_geom=hash_geom)
        assert len(XOR_different.flatten().get_polygons()) > 0


@requires_pya
def test_OAS():
    TOP1 = phidlib.box()
    tempfilename = 'pytesting.oas'
    write_oas(TOP1, tempfilename)
    TOP2 = import_oas(tempfilename)
    XOR = xor_polygons_phidl(TOP1, TOP2)
    if len(XOR.flatten().get_polygons()) > 0:
        raise GeometryDifference("Differences found between phidl Devices.")
    os.remove(tempfilename)

