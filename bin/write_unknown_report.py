#! /usr/bin/python3.7

import argparse
import pandas as pd
from datetime import date
import os
import sys

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Based on unknown taxa files, count lineages.',
        prog='write_unknown_report.py',
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
        '--report',
        metavar='FILE',
        action='store',
        help='Path to write count report.',
        required=True,
    )

    required_group.add_argument(
        '--unknown1',
        metavar='FILE',
        action='store',
        help='Path to R1 unknown file.',
        required=True
    )

    required_group.add_argument(
        '--unknown2',
        metavar='FILE',
        action='store',
        help='Path to R2 unknown file.',
        required=True
    )

    required_group.add_argument(
        '--mode',
        metavar='nuc|transnuc',
        action='store',
        help='Type of alignment for count file.',
        required=True
    )

    required_group.add_argument(
        '--sampleid',
        metavar='STR',
        action='store',
        help='Sample name, id, or label.',
        required=True,
        type=str
    )

    required_group.add_argument(
        '--config',
        metavar='STR',
        action='store',
        help='Path to runtime config file.',
        required=True,
        type=str
    )

    arguments = parser.parse_args()

    if arguments.mode != 'nuc' and arguments.mode != 'transnuc':
        msg = 'Unknown --mode value {} passed. Must be nuc|transnuc only.'.format(arguments.mode)
        parser.error(msg)

    return arguments


def write_lineage_counts(fh_out, df, pair_label):

    fh_out.write('LINEAGE ' + pair_label + '\n')
    fh_out.write('-' * 20 + '\n')
    fh_out.write('[1] hit count\n')
    fh_out.write('[2] percent\n')
    fh_out.write('[3] lineage\n')
    fh_out.write('-' * 20 + '\n')
    for lineage, count in df['lineage'].value_counts().items():
        total = df['lineage'].value_counts().sum()
        percent = round(count / total, 3)
        line = '\t'.join([str(count), str(percent), lineage])
        fh_out.write(line + '\n')
    fh_out.write('-' * 20 + '\n')
    fh_out.write(str(total) + '  TOTAL\n\n\n')

    return


def write_count_report(arguments):

    # Are the R1 and R2 groups populated?

    df1 = pd.read_csv(arguments.unknown1, sep='\t')
    df1['end'] = 'R1'
    df2 = pd.read_csv(arguments.unknown2, sep='\t')
    df2['end'] = 'R2'
    df = pd.concat([df1, df2])

    df_group_ids = df['end'].unique()
    df_r1_populated = 'R1' in df_group_ids
    df_r2_populated = 'R2' in df_group_ids

    if df_r1_populated is False and df_r2_populated is False:
        write_blank_report_file(arguments)

    fh_out = open(arguments.report, 'w')

    # Header.

    fh_out.write('-------------------\n')
    fh_out.write(' V I R O M A T C H\n')
    fh_out.write('-------------------\n\n')

    with open(arguments.config, 'r') as config_fh:
        for line in config_fh:
            fh_out.write('# ' + line)
        fh_out.write('\n')

    fh_out.write(':BEGIN:\n\n\n')

    fh_out.write('Sample ID: ' + arguments.sampleid + '\n')

    today = date.today()
    today_date = today.strftime("%B %d, %Y")
    fh_out.write('Date: ' + today_date + '\n\n')

    if arguments.mode == 'nuc':
        fh_out.write('=' * 75 + '\n')
        fh_out.write('NUCLEOTIDE UNKNOWN TAXA HIT COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')
    elif arguments.mode == 'transnuc':
        fh_out.write('=' * 75 + '\n')
        fh_out.write('TRANSLATED NUCLEOTIDE UNKNOWN TAXA HIT COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')

    # Combined (R1 + R2).

    pair_label = '(R1 + R2)'
    write_lineage_counts(fh_out=fh_out, df=df, pair_label=pair_label)
    fh_out.write(':' * 75 + '\n')
    fh_out.write(':' * 75 + '\n')
    fh_out.write(':' * 75 + '\n\n\n')

    # R1 only.

    if df_r1_populated is True:
        pair_label = '(R1)'
        write_lineage_counts(fh_out=fh_out, df=df1, pair_label=pair_label)
        fh_out.write(':' * 75 + '\n')
        fh_out.write(':' * 75 + '\n')
        fh_out.write(':' * 75 + '\n\n\n')
    else:
        fh_out.write('(R1) --- NO HITS TO REPORT\n\n\n')
        fh_out.write(':' * 75 + '\n')
        fh_out.write(':' * 75 + '\n')
        fh_out.write(':' * 75 + '\n\n\n')

    # R2 only.

    if df_r2_populated is True:
        pair_label = '(R2)'
        write_lineage_counts(fh_out=fh_out, df=df2, pair_label=pair_label)
    else:
        fh_out.write('(R2) --- NO HITS TO REPORT\n\n\n')

    fh_out.write(':END:\n\n')

    fh_out.close()

    return


def write_blank_report_file(arguments):
    # Write blank report file.

    fh_out = open(arguments.report, 'w')

    fh_out.write('-------------------\n')
    fh_out.write(' V I R O M A T C H\n')
    fh_out.write('-------------------\n\n')

    with open(arguments.config, 'r') as config_fh:
        for line in config_fh:
            fh_out.write('# ' + line)
        fh_out.write('\n')

    fh_out.write(':BEGIN:\n\n\n')

    fh_out.write('Sample ID: ' + arguments.sampleid + '\n')

    today = date.today()
    today_date = today.strftime("%B %d, %Y")
    fh_out.write('Date: ' + today_date + '\n\n')

    if arguments.mode == 'nuc':
        fh_out.write('=' * 75 + '\n')
        fh_out.write('NUCLEOTIDE UNKNOWN TAXA HIT COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')
    elif arguments.mode == 'transnuc':
        fh_out.write('=' * 75 + '\n')
        fh_out.write('TRANSLATED NUCLEOTIDE UNKNOWN TAXA HIT COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')

    fh_out.write('HITS FILE WAS BLANK --- NO HITS TO REPORT\n\n\n')
    fh_out.write(':END:\n\n')

    sys.exit()


if __name__ == '__main__':

    # We will calculate, and report on, unknown taxa lineage counts. Blank
    # input will produce blank output files.

    arguments = eval_cli_arguments()

    if os.stat(arguments.unknown1).st_size == 0 and os.stat(arguments.unknown2).st_size == 0:
        write_blank_report_file(arguments=arguments)
    else:
        write_count_report(arguments=arguments)


# __END__
