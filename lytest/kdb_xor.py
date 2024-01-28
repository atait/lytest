import os

from lytest.phidl_oas import import_oas


class GeometryDifference(Exception):
    pass


def run_xor_pya(file1, file2, tolerance=1, hash_geom=False, verbose=False):
    """Returns nothing. Raises a GeometryDifference if there are differences detected
        hash_geom=True uses phidl's hash_geometry, avoiding a full XOR unless they are different
    """
    from lygadgets import pya
    if hash_geom or pya is None:
        run_xor_phidl(file1, file2, tolerance, hash_geom=True, verbose=verbose)

    l1 = pya.Layout()
    l1.read(file1)

    l2 = pya.Layout()
    l2.read(file2)

    # Check that same set of layers are present
    layer_pairs = []
    for ll1 in l1.layer_indices():
        li1 = l1.get_info(ll1)
        ll2 = l2.find_layer(l1.get_info(ll1))
        if ll2 is None:
            raise GeometryDifference(
                f"Layer {li1} of layout {file1} not present in layout {file2}."
            )

        layer_pairs.append((ll1, ll2))

    for ll2 in l2.layer_indices():
        li2 = l2.get_info(ll2)
        ll1 = l1.find_layer(l2.get_info(ll2))
        if ll1 is None:
            raise GeometryDifference(
                f"Layer {li2} of layout {file2} not present in layout {file1}."
            )

    # Check that topcells are the same
    tc1_names = [tc.name for tc in l1.top_cells()]
    tc2_names = [tc.name for tc in l2.top_cells()]
    tc1_names.sort()
    tc2_names.sort()
    if tc1_names != tc2_names:
        raise GeometryDifference(
            "Missing topcell on one of the layouts, or name differs:\n{}\n{}".format(
                tc1_names, tc2_names
            )
        )
    topcell_pairs = [(l1.cell(tc1_n), l2.cell(tc1_n)) for tc1_n in tc1_names]
    # Check that dbu are the same
    if (l1.dbu - l2.dbu) > 1e-6:
        raise GeometryDifference(
            f"Database unit of layout {file1} ({l1.dbu}) differs from that of layout {file2} ({l2.dbu})."
        )

    # Run the difftool
    diff = False
    for tc1, tc2 in topcell_pairs:
        for ll1, ll2 in layer_pairs:
            r1 = pya.Region(tc1.begin_shapes_rec(ll1))
            r2 = pya.Region(tc2.begin_shapes_rec(ll2))

            rxor = r1 ^ r2

            if tolerance > 0:
                rxor.size(-tolerance)

            if not rxor.is_empty():
                diff = True
                if verbose:
                    print(
                        f"{rxor.size()} differences found in {tc1.name} on layer {l1.get_info(ll1)}."
                    )

            elif verbose:
                print(
                    f"No differences found in {tc1.name} on layer {l1.get_info(ll1)}."
                )

    if diff:
        fn_abgd = []
        for fn in [file1, file2]:
            head, tail = os.path.split(fn)
            abgd = os.path.join(os.path.basename(head), tail)
            fn_abgd.append(abgd)
        raise GeometryDifference(
            "Differences found between layouts {} and {}".format(*fn_abgd)
        )


def xor_polygons_phidl(A, B, hash_geom=True):
    """Given two devices A and B, performs a layer-by-layer XOR diff between
    A and B, and returns polygons representing the differences between A and B.
    """
    from phidl import Device
    import gdspy

    # first do a geometry hash to vastly speed up if they are equal
    if hash_geom and (A.hash_geometry() == B.hash_geometry()):
        return Device()

    D = Device()
    A_polys = A.get_polygons(by_spec=True)
    B_polys = B.get_polygons(by_spec=True)
    A_layers = A_polys.keys()
    B_layers = B_polys.keys()
    all_layers = set()
    all_layers.update(A_layers)
    all_layers.update(B_layers)
    for layer in all_layers:
        if (layer in A_layers) and (layer in B_layers):
            p = gdspy.fast_boolean(
                A_polys[layer],
                B_polys[layer],
                operation="xor",
                precision=0.001,
                max_points=4000,
                layer=layer[0],
                datatype=layer[1],
            )
        elif layer in A_layers:
            p = A_polys[layer]
        elif layer in B_layers:
            p = B_polys[layer]
        if p is not None:
            D.add_polygon(p, layer=layer)
    return D


def run_xor_phidl(file1, file2, tolerance=1, verbose=False, hash_geom=True):
    TOP1, TOP2 = [import_oas(fn) for fn in [file1, file2]]
    XOR = xor_polygons_phidl(TOP1, TOP2, hash_geom=True)
    if len(XOR.flatten().get_polygons()) > 0:
        raise GeometryDifference(
            f"Differences found between layouts {file1} and {file2}"
        )


run_xor = run_xor_pya


if __name__ == "__main__":
    """For command line argument usage, run ``python kdb_xor.py --help``

    If there is a difference found, this script will return a non-zero exit code.

    Typical usage from a bash script::

        python kdb_xor.py a.gds b.gds || failed=true
        # alternatively:
        if !(python kdb_xor.py a.gds b.gds); then
          failed=true
        fi
    """
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Run a klayout XOR to check yes/no for differences."
    )
    parser.add_argument("file1", help="first .gds (or .oas) file")
    parser.add_argument("file2", help="second .gds (or .oas) file")
    parser.add_argument(
        "--tol", type=int, default=1, help="tolerance in database units (default = 1)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print out status layer by layer"
    )
    args = parser.parse_args()

    try:
        run_xor(args.file1, args.file2, args.tol, verbose=args.verbose)
    except GeometryDifference as err:
        print(err)
        sys.exit(1)
