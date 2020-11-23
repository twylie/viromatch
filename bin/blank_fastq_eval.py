#! /usr/bin/python3.7

import argparse
import os

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Evaluate and fix blank FASTQ files for downstream input.',
        prog='blank_fastq_eval.py',
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
        '--fastq',
        metavar='FILE',
        action='store',
        help='Path to input FASTQ file.',
        required=True,
    )

    required_group.add_argument(
        '--log',
        metavar='FILE',
        action='store',
        help='Path to touch eval log file.',
        required=True
    )

    return parser.parse_args()


if __name__ == '__main__':

    # Some applications will error-out if given a blank/empty FASTQ file as
    # input. Therefore, we will evaluate a given FASTQ file for zero-byte
    # size. If a FASTQ is blank, we will write a "null" placeholder file so
    # applications will not error-out.

    arguments = eval_cli_arguments()

    if os.stat(arguments.fastq).st_size == 0:
        with open(arguments.fastq, 'w') as fh_out:
            fh_out.write('@null\n')
            fh_out.write('NNNNNNNNNNNN\n')
            fh_out.write('+\n')
            fh_out.write('BBBBBBBBBBBB\n')
            with open(arguments.log, 'w') as log_out:
                log_out.write('BLANK EVAL FAILED (touched a null file)\n')
    else:
        with open(arguments.log, 'w') as log_out:
            log_out.write('BLANK EVAL PASSED\n')


# __END__
