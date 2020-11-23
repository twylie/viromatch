#! /usr/bin/python3.7

import argparse

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Write a list of unique unmapped FASTQ read ids.',
        prog='write_unmapped_fastq_ids.py',
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
        '--mapsam',
        metavar='FILE',
        action='store',
        help='List of mapped SAM paths.',
        required=True,
        nargs='+'
    )

    required_group.add_argument(
        '--unmapsam',
        metavar='FILE',
        action='store',
        help='List of unmapped SAM paths.',
        required=True,
        nargs='+'
    )

    required_group.add_argument(
        '--out',
        metavar='FILE',
        action='store',
        help='Path to write unmapped id file.',
        required=True
    )

    return parser.parse_args()


def write_unmapped_fastq_ids(arguments):

    # Merging mapped SAM read ids.

    mapsam_ids = set()
    for mapsam in arguments.mapsam:
        with open(mapsam, 'r') as fh:
            for line in fh:
                line = line.strip()
                mapsam_ids.add(line.split('\t')[0])

    # Merging mapped SAM read ids.

    unmapsam_ids = set()
    for unmapsam in arguments.unmapsam:
        with open(unmapsam, 'r') as fh:
            for line in fh:
                line = line.strip()
                unmapsam_ids.add(line.split('\t')[0])

    # A read id only has to be mapped once to be discounted, so the mapped
    # set of ids is canonical. Any id in the unmapped set, but not in the
    # mapped set, is considered unmapped.

    # Example read ids:
    #
    # D00170:57:CA2R8ANXX:4:1113:3715:56038
    # D00170:57:CA2R8ANXX:4:1114:1779:14299
    # D00170:57:CA2R8ANXX:4:1115:16070:70451
    # ...

    with open(arguments.out, 'w') as fh:
        for read_id in unmapsam_ids.difference(mapsam_ids):
            fh.write(read_id + '\n')

    return


if __name__ == '__main__':

    # We are passed a list of mapped and unmapped SAM files. We will
    # evaluate the union of read ids and resolve the list of (unique)
    # unmapped read ids. A file of unmapped read names will be written to
    # the indicated "out" file path.

    arguments = eval_cli_arguments()
    write_unmapped_fastq_ids(arguments)


# __END__
