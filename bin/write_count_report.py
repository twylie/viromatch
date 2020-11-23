#! /usr/bin/python3.7

import argparse
import pandas as pd
from datetime import date
import os
import sys

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Based on filtered/passed SAM files, asscoiate taxonomy.',
        prog='write_count_report.py',
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
        '--counts',
        metavar='FILE',
        action='store',
        help='Path to read count tax file.',
        required=True,
    )

    required_group.add_argument(
        '--report',
        metavar='FILE',
        action='store',
        help='Path to write read count report.',
        required=True
    )

    required_group.add_argument(
        '--genus',
        metavar='FILE',
        action='store',
        help='Path to write genus read count TSV.',
        required=True
    )

    required_group.add_argument(
        '--species',
        metavar='FILE',
        action='store',
        help='Path to write species read count TSV.',
        required=True
    )

    required_group.add_argument(
        '--lineage',
        metavar='FILE',
        action='store',
        help='Path to write lineage read count TSV',
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


def write_genus_counts(fh_out, df, pair_label):

    fh_out.write('GENUS ' + pair_label + '\n')
    fh_out.write('-' * 20 + '\n')
    fh_out.write('[1] read count\n')
    fh_out.write('[2] percent\n')
    fh_out.write('[3] genus\n')
    fh_out.write('-' * 20 + '\n')
    for genus, count in df['genus'].value_counts().items():
        total = df['genus'].value_counts().sum()
        percent = round(count / total, 3)
        line = '\t'.join([str(count), str(percent), genus])
        fh_out.write(line + '\n')
    fh_out.write('-' * 20 + '\n')
    fh_out.write(str(total) + '  TOTAL\n\n\n')

    return


def write_species_counts(fh_out, df, pair_label):

    fh_out.write('SPECIES ' + pair_label + '\n')
    fh_out.write('-' * 20 + '\n')
    fh_out.write('[1] read count\n')
    fh_out.write('[2] percent\n')
    fh_out.write('[3] species\n')
    fh_out.write('-' * 20 + '\n')
    for species, count in df['species'].value_counts().items():
        total = df['species'].value_counts().sum()
        percent = round(count / total, 3)
        line = '\t'.join([str(count), str(percent), species])
        fh_out.write(line + '\n')
    fh_out.write('-' * 20 + '\n')
    fh_out.write(str(total) + '  TOTAL\n\n\n')

    return


def write_lineage_counts(fh_out, df, pair_label):

    fh_out.write('LINEAGE ' + pair_label + '\n')
    fh_out.write('-' * 20 + '\n')
    fh_out.write('[1] read count\n')
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

    df = pd.read_csv(arguments.counts, sep='\t')
    df_group_ids = df['# pair end'].unique()
    df_r1_populated = 'R1' in df_group_ids
    df_r2_populated = 'R2' in df_group_ids

    if df_r1_populated is False and df_r2_populated is False:
        write_blank_report_file(arguments)

    # Make count dataframes.

    if df_r1_populated is True:
        df_r1 = df.groupby('# pair end').get_group('R1')

    if df_r2_populated is True:
        df_r2 = df.groupby('# pair end').get_group('R2')

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
        fh_out.write('NUCLEOTIDE ALIGNMENT READ COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')
    elif arguments.mode == 'transnuc':
        fh_out.write('=' * 75 + '\n')
        fh_out.write('TRANSLATED NUCLEOTIDE ALIGNMENT READ COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')

    # Combined (R1 + R2).

    pair_label = '(R1 + R2)'
    write_lineage_counts(fh_out=fh_out, df=df, pair_label=pair_label)
    write_genus_counts(fh_out=fh_out, df=df, pair_label=pair_label)
    write_species_counts(fh_out=fh_out, df=df, pair_label=pair_label)
    fh_out.write(':' * 75 + '\n')
    fh_out.write(':' * 75 + '\n')
    fh_out.write(':' * 75 + '\n\n\n')

    # R1 only.

    if df_r1_populated is True:
        pair_label = '(R1)'
        write_lineage_counts(fh_out=fh_out, df=df_r1, pair_label=pair_label)
        write_genus_counts(fh_out=fh_out, df=df_r1, pair_label=pair_label)
        write_species_counts(fh_out=fh_out, df=df_r1, pair_label=pair_label)
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
        write_lineage_counts(fh_out=fh_out, df=df_r2, pair_label=pair_label)
        write_genus_counts(fh_out=fh_out, df=df_r2, pair_label=pair_label)
        write_species_counts(fh_out=fh_out, df=df_r2, pair_label=pair_label)
    else:
        fh_out.write('(R2) --- NO HITS TO REPORT\n\n\n')

    fh_out.write(':END:\n\n')

    fh_out.close()

    return df


def write_lineage_tsv(df, arguments):

    with open(arguments.lineage, 'w') as fh_out:
        header = '\t'.join(['sample id', 'tax level', 'taxonomy', 'read count'])
        fh_out.write(header + '\n')
        for lineage, count in df['lineage'].value_counts().items():
            line = '\t'.join([arguments.sampleid, 'lineage', lineage, str(count)])
            fh_out.write(line + '\n')

    return


def write_genus_tsv(df, arguments):

    with open(arguments.genus, 'w') as fh_out:
        header = '\t'.join(['sample id', 'tax level', 'taxonomy', 'read count'])
        fh_out.write(header + '\n')
        for genus, count in df['genus'].value_counts().items():
            line = '\t'.join([arguments.sampleid, 'genus', genus, str(count)])
            fh_out.write(line + '\n')

    return


def write_species_tsv(df, arguments):

    with open(arguments.species, 'w') as fh_out:
        header = '\t'.join(['sample id', 'tax level', 'taxonomy', 'read count'])
        fh_out.write(header + '\n')
        for species, count in df['species'].value_counts().items():
            line = '\t'.join([arguments.sampleid, 'species', species, str(count)])
            fh_out.write(line + '\n')

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
        fh_out.write('NUCLEOTIDE ALIGNMENT READ COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')
    elif arguments.mode == 'transnuc':
        fh_out.write('=' * 75 + '\n')
        fh_out.write('TRANSLATED NUCLEOTIDE ALIGNMENT READ COUNTS\n')
        fh_out.write('=' * 75 + '\n\n')

    fh_out.write('COUNTS FILE WAS BLANK --- NO HITS TO REPORT\n\n\n')
    fh_out.write(':END:\n')

    fh_out.close()

    # Write blank lineage table.

    with open(arguments.lineage, 'w') as fh_out:
        header = '\t'.join(['sample id', 'tax level', 'taxonomy', 'read count'])
        fh_out.write(header + '\n')

    # Write blank genus table.

    with open(arguments.genus, 'w') as fh_out:
        header = '\t'.join(['sample id', 'tax level', 'taxonomy', 'read count'])
        fh_out.write(header + '\n')

    # Wrire blank species table.

    with open(arguments.species, 'w') as fh_out:
        header = '\t'.join(['sample id', 'tax level', 'taxonomy', 'read count'])
        fh_out.write(header + '\n')

    sys.exit()


if __name__ == '__main__':

    # We will calculate, and report on, read counts for several metadata
    # categories. Also, TSV tables of counts will be written. Blank input
    # will produce blank output files.

    arguments = eval_cli_arguments()

    if os.stat(arguments.counts).st_size == 0:
        write_blank_report_file(arguments=arguments)
    else:
        df = write_count_report(arguments=arguments)
        write_lineage_tsv(df=df, arguments=arguments)
        write_genus_tsv(df=df, arguments=arguments)
        write_species_tsv(df=df, arguments=arguments)


# __END__
