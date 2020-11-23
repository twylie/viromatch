#! /usr/bin/python3.7

import argparse
from viromatch.lib.taxonomy import Taxonomy
import os

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Resolve lineage given taxid.',
        prog='taxid2lineage.py',
        add_help=False
    )

    # Optional arguments.

    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='Display the extended usage statement.'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=version,
        help='Display the software version number.'
    )

    # Required arguments.

    required_group = parser.add_argument_group('required')

    required_group.add_argument(
        '--taxonomy',
        metavar='FILE',
        action='store',
        help='Path to taxonomy file.',
        required=True,
    )

    required_group.add_argument(
        '--taxid',
        metavar='INT',
        action='store',
        help='Tax ids.',
        required=True,
        nargs='+'
    )

    arguments = parser.parse_args()

    for arg in arguments.taxid:
        if arg.isnumeric() is not True:
            msg = 'Taxid must be numeric.'
            parser.error(msg)

    if os.path.isfile(arguments.taxonomy) is not True:
        msg = 'You must supply a taxonomy file [--taxonomy].'
        parser.error(msg)

    return arguments


if __name__ == '__main__':

    # Given a list of NCBI tax ids, we will look-up and return the
    # corresponding taxonomic lineages. By default, we return the YAML
    # representation and the flattened lineage views.

    arguments = eval_cli_arguments()

    tax = Taxonomy(arguments.taxonomy)

    for id_ in arguments.taxid:
        tax.lookup_lineage(id_)
        print('# [{}] {}'.format(id_, tax.flatten_lineage()))
        tax.lineage_yaml()
        print('---')


# __END__
