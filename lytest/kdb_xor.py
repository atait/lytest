import os


class GeometryDifference(Exception):
    pass


def run_xor(file1, file2, tolerance=1, verbose=False):
    ''' Returns nothing. Raises a GeometryDifference if there are differences detected
    '''
    from lygadgets import pya as kdb

    l1 = kdb.Layout()
    l1.read(file1)

    l2 = kdb.Layout()
    l2.read(file2)

    # Check that same set of layers are present
    layer_pairs = []
    for ll1 in l1.layer_indices():
        li1 = l1.get_info(ll1)
        ll2 = l2.find_layer(l1.get_info(ll1))
        if ll2 is None:
            raise GeometryDifference("Layer {} of layout {} not present in layout {}.".format(li1, file1, file2))
        layer_pairs.append((ll1, ll2))

    for ll2 in l2.layer_indices():
        li2 = l2.get_info(ll2)
        ll1 = l1.find_layer(l2.get_info(ll2))
        if ll1 is None:
            raise GeometryDifference("Layer {} of layout {} not present in layout {}.".format(li2, file2, file1))

    # Check that topcells are the same
    tc1_names = [tc.name for tc in l1.top_cells()]
    tc2_names = [tc.name for tc in l2.top_cells()]
    tc1_names.sort()
    tc2_names.sort()
    if not tc1_names == tc2_names:
        raise GeometryDifference("Missing topcell on one of the layouts, or name differs:\n{}\n{}".format(tc1_names, tc2_names))
    topcell_pairs = []
    for tc1_n in tc1_names:
        topcell_pairs.append((l1.cell(tc1_n), l2.cell(tc1_n)))

    # Check that dbu are the same
    if (l1.dbu - l2.dbu) > 1e-6:
        raise GeometryDifference("Database unit of layout {} ({}) differs from that of layout {} ({}).".format(file1, l1.dbu, file2, l2.dbu))

    # Run the difftool
    diff = False
    for tc1, tc2 in topcell_pairs:
        for ll1, ll2 in layer_pairs:
            r1 = kdb.Region(tc1.begin_shapes_rec(ll1))
            r2 = kdb.Region(tc2.begin_shapes_rec(ll2))

            rxor = r1 ^ r2

            if tolerance > 0:
                rxor.size(-tolerance)

            if not rxor.is_empty():
                diff = True
                if verbose:
                    print("{} differences found in {} on layer {}.".format(rxor.size(), tc1.name, l1.get_info(ll1)))
            else:
                if verbose:
                    print("No differences found in {} on layer {}.".format(tc1.name, l1.get_info(ll1)))

    if diff:
        fn_abgd = []
        for fn in [file1, file2]:
            head, tail = os.path.split(fn)
            abgd = os.path.join(os.path.basename(head), tail)
            fn_abgd.append(abgd)
        raise GeometryDifference("Differences found between layouts {} and {}".format(*fn_abgd))


if __name__ == "__main__":
    ''' For command line argument usage, run ``python kdb_xor.py --help``

        If there is a difference found, this script will return a non-zero exit code.

        Typical usage from a bash script::

            python kdb_xor.py a.gds b.gds || failed=true
            # alternatively:
            if !(python kdb_xor.py a.gds b.gds); then
              failed=true
            fi
    '''
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Run a klayout XOR to check yes/no for differences.')
    parser.add_argument('file1', help='first .gds (or .oas) file')
    parser.add_argument('file2', help='second .gds (or .oas) file')
    parser.add_argument('--tol', type=int, default=1, help='tolerance in database units (default = 1)')
    parser.add_argument('-v', '--verbose', action='store_true', help='print out status layer by layer')
    args = parser.parse_args()

    try:
        run_xor(args.file1, args.file2, args.tol, verbose=args.verbose)
    except GeometryDifference as err:
        print(err)
        sys.exit(1)

