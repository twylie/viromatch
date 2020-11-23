#! /usr/bin/python3.7

import argparse
from viromatch.lib.taxonomy import Taxonomy
from viromatch.lib.hits import ReadBlockSam
from viromatch.lib.hits import CalcPercentVariationSam

version = '1.1'


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Filter a name sorted SAM file for best hits.',
        prog='best_hit_filter_sam.py',
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
        '--sam',
        metavar='FILE',
        action='store',
        help='Path to read name sorted SAM file.',
        required=True,
    )

    required_group.add_argument(
        '--out',
        metavar='FILE',
        action='store',
        help='Path to write filtered, best hit SAM file.',
        required=True
    )

    required_group.add_argument(
        '--log',
        metavar='FILE',
        action='store',
        help='Path to write pass/fail log file.',
        required=True
    )

    required_group.add_argument(
        '--unknown',
        metavar='FILE',
        action='store',
        help='Path to write unknown taxa log file.',
        required=True
    )

    required_group.add_argument(
        '--otherseq',
        metavar='FILE',
        action='store',
        help='Path to other sequences log file.',
        required=True
    )

    required_group.add_argument(
        '--taxid',
        metavar='FILE',
        action='store',
        help='Taxonomy ID lookup file.',
        required=True
    )

    required_group.add_argument(
        '--pid',
        metavar='FLOAT',
        action='store',
        type=float,
        help='Max percent identity variance for nucleotide hits.',
        required=True
    )

    required_group.add_argument(
        '--pidprox',
        metavar='FLOAT',
        action='store',
        type=float,
        help='Max proximal percent identity variance for nucleotide hits.',
        required=True
    )

    return parser.parse_args()


def filter_sam_hits(taxonomy, arguments):

    read_block = list()
    current_read_id = None
    best_score = None

    arguments.fh_log = open(arguments.log, 'w')
    arguments.fh_log_unknown = open(arguments.unknown, 'w')
    arguments.fh_log_other_seq = open(arguments.otherseq, 'w')
    fh_out = open(arguments.out, 'w')

    header = '\t'.join([
        '# pass|fail',
        'code',
        'read block size',
        'read id',
        'comment',
        'pidv',
        'acc id',
        'species',
        'lineage'
    ])
    arguments.fh_log.write(header + '\n')

    header = '\t'.join([
        '# status',
        'code',
        'read id',
        'comment',
        'acc id',
        'tax id',
        'lineage'
    ])
    arguments.fh_log_unknown.write(header + '\n')
    arguments.fh_log_other_seq.write(header + '\n')

    with open(arguments.sam, 'r') as fh_sam:

        # Collect the read id and percent identity value for each hit.

        for line in fh_sam:
            line = line.strip()
            fields = line.split('\t')
            read_id = fields[0]
            score = CalcPercentVariationSam(line).calc_percent_variation()

            # A read block is a list of alignment report lines, all having
            # the same read id. In this way, we evaluate a smaller chunk of
            # alignments at any one time.

            if current_read_id is None:
                current_read_id = read_id
                read_block.append([line, score])
                if best_score is None:
                    best_score = score
            elif read_id == current_read_id:
                read_block.append([line, score])
                if score < best_score:
                    best_score = score
            elif read_id != current_read_id:
                # Determine the best hit in the read block.
                rb = ReadBlockSam(arguments, current_read_id, best_score, taxonomy, read_block)
                best_hit, best_hit_lineage = rb.evaluate_read_block()
                if best_hit is not None:
                    fh_out.write(best_hit + '\n')
                best_score = score
                current_read_id = read_id
                del read_block[:]
                read_block.append([line, score])

        # Because of our evaluation loop, the last line in the read block
        # is a special case and needs to be evaluated on its own.

        rb = ReadBlockSam(arguments, current_read_id, best_score, taxonomy, read_block)
        best_hit, best_hit_lineage = rb.evaluate_read_block()

        if best_hit is not None:
            fh_out.write(best_hit + '\n')

    fh_out.close()
    arguments.fh_log.close()
    arguments.fh_log_unknown.close()
    arguments.fh_log_other_seq.close()

    return


if __name__ == '__main__':

    # We are passed a name-sorted SAM file as input. It is important that
    # the SAM file be read name sorted, as we will be evaluating best hits
    # per read for each read block; a read block is a block of hits with
    # the same read name. We will write a SAM file where each read name has
    # a single, chosen best hit.

    arguments = eval_cli_arguments()

    filter_sam_hits(
        taxonomy=Taxonomy(arguments.taxid),
        arguments=arguments
    )


# __END__
