#! /usr/bin/python3.7

import argparse
from viromatch.lib.taxonomy import Taxonomy

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Based on filtered/passed Diamond TSV files, asscoiate taxonomy.',
        prog='tsv_taxonomy_count_prep.py',
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
        '--tsv1',
        metavar='FILE',
        action='store',
        help='Path to read name sorted TSV file.',
        required=True,
    )

    required_group.add_argument(
        '--tsv2',
        metavar='FILE',
        action='store',
        help='Path to read name sorted TSV file.',
        required=True,
    )

    required_group.add_argument(
        '--out',
        metavar='FILE',
        action='store',
        help='Path to write filtered, best hit TSV file.',
        required=True
    )

    required_group.add_argument(
        '--taxid',
        metavar='FILE',
        action='store',
        help='Taxonomy ID lookup file.',
        required=True
    )

    return parser.parse_args()


def write_taxonomy(fh_out, tsv, end, taxonomy):

    with open(tsv, 'r') as fh:
        for line in fh:
            line = line.strip()
            fields = line.split('\t')
            read_id = fields[0]
            acc_id, tax_id = fields[1].split('|')
            tax = taxonomy.lookup_lineage(tax_id)
            genus = tax.genus()
            species = tax.species()
            lineage = tax.flatten_lineage()

            line = '\t'.join([
                end,
                read_id,
                acc_id,
                genus,
                species,
                lineage
            ])

            fh_out.write(line + '\n')

    return


def associate_taxonomy_with_hits(taxonomy, arguments):

    fh_out = open(arguments.out, 'w')

    header = '\t'.join([
        '# pair end',
        'read id',
        'acc id',
        'genus',
        'species',
        'lineage'
    ])

    fh_out.write(header + '\n')

    write_taxonomy(fh_out=fh_out, tsv=arguments.tsv1, end='R1', taxonomy=taxonomy)
    write_taxonomy(fh_out=fh_out, tsv=arguments.tsv2, end='R2', taxonomy=taxonomy)

    fh_out.close()

    return


if __name__ == '__main__':

    # Provided R1 and R2 filtered/passed Diamond TSV files, we will
    # associate taxonomy for these best hits and prepare a file for
    # downstream read counting and reporting.

    arguments = eval_cli_arguments()

    associate_taxonomy_with_hits(
        taxonomy=Taxonomy(arguments.taxid),
        arguments=arguments
    )


# __END__
