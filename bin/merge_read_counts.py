#! /usr/bin/python3.7

import argparse
import pandas as pd
import os
import sys

version = '1.0'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Merge multiple ViroMatch read count files.',
        prog='merge_read_counts.py',
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

    parser.add_argument(
        '--merge',
        metavar='nuc|trans|both',
        action='store',
        default='both',
        help='Merge read types. [both]',
    )

    # Required arguments.

    required_group = parser.add_argument_group('required')

    required_group.add_argument(
        '--reports',
        metavar='FILE',
        action='store',
        help='Path to file of report ids:paths.',
        required=True,
    )

    required_group.add_argument(
        '--reportdir',
        metavar='DIR',
        action='store',
        help='Directory to write report files.',
        required=True
    )

    return parser.parse_args()


def merge_read_counts(arguments):

    nuc_report = 'viromatch_results/nuc_nt_best_hit_count_prep/INPUT.merged.validate.nuc.mapped.filter.pass.tax'
    trans_nuc_report = 'viromatch_results/trans_nuc_nr_best_hit_count_prep/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax'

    # Load the ids:paths file.

    nuc_paths = dict()
    trans_nuc_paths = dict()

    with open(arguments.reports, 'r') as ids_fh:
        for line in ids_fh:
            line = line.strip()
            id_, path = line.split('\t')
            nuc_report_full = path + nuc_report
            trans_nuc_report_full = path + trans_nuc_report
            nuc_paths.update({nuc_report_full: id_})
            trans_nuc_paths.update({trans_nuc_report_full: id_})

    for i, report in enumerate(nuc_paths.keys()):
        if i == 0:
            df_cumulative_nuc = pd.read_csv(report, sep='\t')
            df_cumulative_nuc['sample name'] = nuc_paths[report]
        else:
            df_file = pd.read_csv(report, sep='\t')
            df_file['sample name'] = nuc_paths[report]
            df_cumulative_nuc = df_cumulative_nuc.append(df_file, ignore_index=True)

    for i, report in enumerate(trans_nuc_paths.keys()):
        if i == 0:
            df_cumulative_trans = pd.read_csv(report, sep='\t')
            df_cumulative_trans['sample name'] = trans_nuc_paths[report]
        else:
            df_file = pd.read_csv(report, sep='\t')
            df_file['sample name'] = trans_nuc_paths[report]
            df_cumulative_trans = df_cumulative_trans.append(df_file, ignore_index=True)

    df_cumulative_both = pd.concat([df_cumulative_nuc, df_cumulative_trans])

    if arguments.merge == 'both':
        df = df_cumulative_both
    elif arguments.merge == 'nuc':
        df = df_cumulative_nuc
    elif arguments.merge == 'trans':
        df = df_cumulative_trans

    for tax_level in ('lineage', 'genus', 'species'):
        write_report(arguments, df, tax_level)

    return


def write_report(arguments, df, tax_level):

    df_tax = df.groupby(tax_level)

    counts = dict()

    for group in df_tax.groups:
        df = df_tax.get_group(group)
        df_samples = df.groupby('sample name')[tax_level].count().to_dict()
        counts.update({group: df_samples})

    df_final = pd.DataFrame.from_dict(counts, orient='index').fillna(0).sort_index()
    df_final = df_final.reindex(sorted(df_final.columns), axis=1)

    df_report = arguments.reportdir + tax_level + '.df'
    df_final.to_csv(df_report, sep='\t')

    totals = df_final.T.sum().to_list()
    df_final['TOTAL'] = totals

    sample_totals = list()
    for sample in df_final.columns:
        sample_totals.append(df_final[sample].sum())
    df_final.loc['TOTAL'] = sample_totals

    report = arguments.reportdir + tax_level + '_merged_counts.tsv'

    df_final.to_csv(report, sep='\t')

    return


def make_report_directory(arguments):
    if arguments.reportdir[-1] != '/':
        arguments.reportdir += '/'
    if os.path.isdir(arguments.reportdir) is True:
        outdir_error = '\nThe --reportdir path "{}" already exists.\n'.format(arguments.reportdir)
        print(outdir_error)
        sys.exit()
    elif os.path.isdir(arguments.reportdir) is False:
        os.mkdir(arguments.reportdir, 0o755)
    return


if __name__ == '__main__':

    # Given a list of ViroMatch project directories and associated labels, we
    # may generate consolidated read count matrices for lineage, genus, and
    # species levels. Reports will include TSV files with and without totals.

    # The --reports file looks something like this (ids:paths).
    # FOO	/tmp/myTest/myTest/
    # FOO2	/tmp/myTest/myTest2/
    # ...

    arguments = eval_cli_arguments()
    make_report_directory(arguments)
    merge_read_counts(arguments)


# __END__
