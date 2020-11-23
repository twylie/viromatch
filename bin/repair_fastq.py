#! /usr/bin/python3.7

import argparse
from Bio import SeqIO

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Repairs the pairing of FASTQ files.',
        prog='repair_fastq.py',
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
        '--fastq1',
        metavar='FILE',
        action='store',
        help='Path to R1 FASTQ file.',
        required=True,
    )

    required_group.add_argument(
        '--fastq2',
        metavar='FILE',
        action='store',
        help='Path to R2 FASTQ file.',
        required=True
    )

    required_group.add_argument(
        '--mate1',
        metavar='FILE',
        action='store',
        help='Path to write repaired R1 FASTQ file.',
        required=True,
    )

    required_group.add_argument(
        '--mate2',
        metavar='FILE',
        action='store',
        help='Path to write repaired R2 FASTQ file.',
        required=True
    )

    required_group.add_argument(
        '--orphans',
        metavar='FILE',
        action='store',
        help='Path to write orphans FASTQ file.',
        required=True
    )

    required_group.add_argument(
        '--summary',
        metavar='FILE',
        action='store',
        help='Path to write summary/report file.',
        required=True
    )

    return parser.parse_args()


def repair_fastq(arguments):

    # Create synchronized files, plus an "orphans" file. If we ignore
    # the orphaned reads, the reads should already be ordered, hence we
    # only need to stream through each file one time.

    # Collect the list of all ids that have mate pairs.

    r1_set = set()
    with open(arguments.fastq1, "r") as input_handle:
        for record in SeqIO.parse(input_handle, "fastq"):
            r1_set.add(record.id)

    r2_set = set()
    with open(arguments.fastq2, "r") as input_handle:
        for record in SeqIO.parse(input_handle, "fastq"):
            r2_set.add(record.id)

    mate_set = r1_set.intersection(r2_set)
    union_set = r1_set.union(r2_set)
    orphans_set = union_set.difference(mate_set)

    # Create synchronized files, plus an "orphans" file.

    with open(arguments.orphans, 'w') as fh_orphans:

        with open(arguments.mate1, 'w') as fh_r1:
            with open(arguments.fastq1, "r") as input_handle:
                for record in SeqIO.parse(input_handle, "fastq"):
                    if record.id in orphans_set:
                        fh_orphans.write(record.format("fastq"))
                    else:
                        record.id += '/1'
                        record.name = record.id
                        record.description = record.id
                        fh_r1.write(record.format("fastq"))

        with open(arguments.mate2, 'w') as fh_r2:
            with open(arguments.fastq2, "r") as input_handle:
                for record in SeqIO.parse(input_handle, "fastq"):
                    if record.id in orphans_set:
                        fh_orphans.write(record.format("fastq"))
                    else:
                        record.id += '/2'
                        record.name = record.id
                        record.description = record.id
                        fh_r2.write(record.format("fastq"))

    return (r1_set, r2_set, mate_set, orphans_set)


def report_summary(arguments, r1_set, r2_set, mate_set, orphans_set):

    # Summarize the read placement in a small report file.

    with open(arguments.summary, 'w') as fh_summary:
        fh_summary.write('\n')
        fh_summary.write('R1 input FASTQ: {}'.format(arguments.fastq1) + '\n')
        fh_summary.write('R2 input FASTQ: {}'.format(arguments.fastq2) + '\n')
        fh_summary.write('R1 reads: {}'.format(len(r1_set)) + '\n')
        fh_summary.write('R2 reads: {}'.format(len(r2_set)) + '\n')
        fh_summary.write('R1/R2 reads: {} ({} mate pairs)'.format(len(mate_set) * 2, len(mate_set)) + '\n')
        fh_summary.write('Orphaned reads: {}'.format(len(orphans_set)) + '\n')
        fh_summary.write('\n')

    return


if __name__ == '__main__':

    # The R1/R2 read pairs in the FASTQ files are out of synchronization,
    # as they were aligned independently. For variant calling, we are going
    # to use paired alignments, so we will need to run a repair script to
    # put mate pairs back together. Orphaned reads will be ignored
    # downstream.

    arguments = eval_cli_arguments()
    r1_set, r2_set, mate_set, orphans_set = repair_fastq(arguments)
    report_summary(arguments, r1_set, r2_set, mate_set, orphans_set)


# __END__
