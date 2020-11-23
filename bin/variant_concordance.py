#! /usr/bin/python3.7

import argparse
import pandas as pd
import vcfpy
import re

version = '1.0'


class _Concordance():

    def __init__(self, vardb, vcf, counts):

        self.vcf_positive_report = list()
        self.vcf_negative_report = list()
        self.vardb_report = pd.DataFrame()

        # Set the vardb data frame.

        self.vardb = df_vardb

        # Index the vcf file lines.

        self.vcf_index = dict()
        i = 1
        with open(vcf, 'r') as vcf_fh:
            for line in vcf_fh:
                line = line.strip()
                if line[0] == '#':
                    next
                else:
                    self.vcf_index.update({i: line})
                    i += 1

        # Parse and load the vcf information. EXAMPLE:

        # CHROM   | NC_001798.2
        # POS     | 10178
        # ID      | .
        # REF     | C
        # ALT     | T
        # QUAL    | .
        # FILTER  | PASS
        # INFO    | ADP=26;WT=0;HET=0;HOM=1;NC=0
        # FORMAT  | GT:GQ:SDP:DP:RD:AD:FREQ:PVAL:RBQ:ABQ:RDF:RDR:ADF:ADR
        # GENO    | 1/1:146:26:26:0:26:100%:2.0165E-15:0:39:0:0:12:14

        # ----------------------------------------------------------------------
        # FIELDS
        # ----------------------------------------------------------------------
        # CHROM              | Chromosome.
        # POS                | Reference position.
        # ID                 | Identifiers, semicolon separated.
        # REF                | Reference base call.
        # ALT                | Alternative base call(s).
        # QUAL               | Quality score.
        # FILTER             | Pass or fail status.
        # INFO        : ADP  | Average per-sample depth of bases with Phred score >= 20.
        # INFO        : WT   | Number of samples called reference (wild-type).
        # INFO        : HET  |  Number of samples called heterozygous-variant.
        # INFO        : HOM  | Number of samples called homozygous-variant.
        # INFO        : NC   | Number of samples not called.
        # FORMAT/GENO : GT   | Genotype  (1/1: Homozygous ; 0/1 : Heterozygous).
        # FORMAT/GENO : GQ   | Genotype quality.
        # FORMAT/GENO : SDP  | Raw Read Depth as reported by SAMtools.
        # FORMAT/GENO : DP   | Quality Read Depth of bases withPhred score >= 20.
        # FORMAT/GENO : RD   | Depth of reference-supporting bases.
        # FORMAT/GENO : AD   | Depth of variant-supporting bases.
        # FORMAT/GENO : FREQ | Variant allelefrequency.
        # FORMAT/GENO : PVAL | P-value from Fisher's Exact Test (not computed here : default value).
        # FORMAT/GENO : RBQ  | Average quality of reference-supporting bases.
        # FORMAT/GENO : ABQ  | Average quality of variant-supporting bases.
        # FORMAT/GENO : RDF  | Depth of reference-supporting bases on forward strand.
        # FORMAT/GENO : RDR  | Depth of reference-supporting bases on reverse strand.
        # FORMAT/GENO : ADF  | Depth of variant-supporting bases on forward strand.
        # FORMAT/GENO : ADR  | Depth of variant-supporting bases on reverse strand.
        # ----------------------------------------------------------------------

        self.vcf = dict()
        reader = vcfpy.Reader.from_path(vcf)
        for i, vcf_record in enumerate(reader, 1):
            pos = vcf_record.POS - 1

            self.vcf.update({
                pos: {
                    'vcf line': self.vcf_index[i],
                    'record id': i,
                    'chrom': vcf_record.CHROM,
                    'id': vcf_record.ID,
                    'ref': vcf_record.REF,
                    'qual': vcf_record.QUAL,
                    'filter': vcf_record.FILTER,
                    'info': {
                        'adp': vcf_record.INFO.get('ADP'),
                        'wt': vcf_record.INFO.get('WT'),
                        'het': vcf_record.INFO.get('HET'),
                        'hom': vcf_record.INFO.get('HOM'),
                        'nc': vcf_record.INFO.get('NC')
                    }
                }
            })

            for j, alt in enumerate(vcf_record.ALT):
                if 'alt' not in self.vcf[pos].keys():
                    self.vcf[pos]['alt'] = {
                        j: {
                            'type': alt.type,
                            'alt': alt.value
                        }
                    }

            # NOTE: The following code expects only a single sample in the VCF
            # --- i.e. there will only be a single FORMAT/GENO section for
            # a "Sample1".

            for call in vcf_record.calls:
                self.vcf[pos]['geno'] = {
                    'sample': call.sample,
                    'gt': call.data.get('GT'),
                    'gq': call.data.get('GQ'),
                    'sdp': call.data.get('SDP'),
                    'dp': call.data.get('DP'),
                    'rd': call.data.get('RD'),
                    'ad': call.data.get('AD'),
                    'freq': call.data.get('FREQ'),
                    'pval': call.data.get('PVAL'),
                    'rbq': call.data.get('RBQ'),
                    'abq': call.data.get('ABQ'),
                    'rdf': call.data.get('RDF'),
                    'rdr': call.data.get('RDR'),
                    'adf': call.data.get('ADF'),
                    'adr': call.data.get('ADR')
                }

        # Parse the read counts file and save this information in
        # context of only the possible vardb positions.

        # ----------------------------------------------------------------------
        # FIELDS
        # ----------------------------------------------------------------------
        # chrom	position
        # ref_base
        # depth
        # q20_depth
        # base:reads:strands:avg_qual:map_qual:plus_reads:minus_reads
        # ----------------------------------------------------------------------

        self.read_counts = dict()
        with open(arguments.counts, 'r') as fh:
            for line in fh:
                if line[0:5] == 'chrom':
                    continue
                else:
                    line = line.strip()
                    chrom, position, ref, depth, *glob = line.split('\t')
                    self.read_counts.update({int(position): int(depth)})

        return

    def evaluate_concordance(self, refid, sampleid):

        # We will now evaluate the vardb variants in context of the vcf
        # information, updating the report information along the way. We
        # need only evaluate the specific reference indicated by the refid
        # argument. We will cast the variant string to a list context.

        df = self.vardb.groupby('Reference Genome Accession ID').get_group(refid)
        for id_ in df.index:
            variants = df.loc[id_]['Genomic Variant List']
            variants = variants[1:-1]
            variants = re.sub(' ', '', variants)
            variants = re.sub('\'', '', variants)
            variants = variants.split(',')

            # There can be multiple variants per vardb entry
            # (comma-separated). Some of the variants are mutually
            # exclusive (colon-separated). EXAMPLES:
            # SINGLES             | g.143605C>G
            # MULTIPLES (OR)      | g.80683G>C, g.80683G>T
            # MULTIPLES (AND, OR) | g.47370G>A:g.47371C>T, g.47371C>T

            vcf_positives = list()
            vcf_positive_positions = set()

            for var in variants:
                # Multiples.
                if re.search(':', var):
                    var_set = set(var.split(':'))
                    var_positives = set()
                    for variant in var_set:
                        variant_position = int(variant[2:-3])  # 0-based
                        # variant_ref = variant[-3]
                        variant_alt = variant[-1]
                        if variant_position in self.vcf.keys():
                            vcf_alternatives = set()
                            for i in self.vcf[variant_position]['alt'].keys():
                                vcf_alternatives.add(
                                    self.vcf[variant_position]['alt'][i]['alt'].upper()
                                )
                            if variant_alt.upper() in vcf_alternatives:
                                var_positives.add(variant)
                                vcf_positive_positions.add(variant_position)
                    if var_set == var_positives:
                        vcf_positives.append(var)
                else:
                    # Singles.
                    variant_position = int(var[2:-3])  # 0-based
                    # variant_ref = var[-3]
                    variant_alt = var[-1]
                    if variant_position in self.vcf.keys():
                        vcf_alternatives = set()
                        for i in self.vcf[variant_position]['alt'].keys():
                            vcf_alternatives.add(
                                self.vcf[variant_position]['alt'][i]['alt'].upper()
                            )
                        if variant_alt.upper() in vcf_alternatives:
                            vcf_positives.append(var)
                            vcf_positive_positions.add(variant_position)

            if len(vcf_positives) >= 1:
                # Update vardb report --- POSITIVE.
                refs = list()
                adps = list()
                filters = list()
                alternates = list()
                geno_gt = list()
                geno_sdp = list()
                geno_dp = list()
                geno_freq = list()
                vcf_lines = list()
                for pos in vcf_positive_positions:
                    geno_gt.append(self.vcf[pos]['geno']['gt'])
                    geno_sdp.append(self.vcf[pos]['geno']['sdp'])
                    geno_dp.append(self.vcf[pos]['geno']['dp'])
                    geno_freq.append(self.vcf[pos]['geno']['freq'])
                    vcf_lines.append(self.vcf[pos]['vcf line'])
                    refs.append(self.vcf[pos]['ref'])
                    adps.append(self.vcf[pos]['info']['adp'])
                    alt_glob = str()
                    for alt in self.vcf[pos]['alt']:
                        alt_glob += self.vcf[pos]['alt'][alt]['alt']
                    alternates.append(alt_glob)
                    filter_glob = str()
                    for filter_ in self.vcf[pos]['filter']:
                        filter_glob += filter_
                    filters.append(filter_glob)
                df.at[id_, 'VCF Filter'] = filters
                df.at[id_, 'VCF Positives'] = vcf_positives
                df.at[id_, 'VCF ADP'] = adps
                df.at[id_, 'VCF Ref'] = refs
                df.at[id_, 'VCF Alt'] = alternates
                df.at[id_, 'VCF GT'] = geno_gt
                df.at[id_, 'VCF Freq'] = geno_freq
                df.at[id_, 'VCF SDP'] = geno_sdp
                df.at[id_, 'VCF DP'] = geno_dp
                df.at[id_, 'VCF Lines'] = vcf_lines
            else:
                # Update vardb report --- NEGATIVE.
                negative_vardb_series = df.loc[id_]
                # Need (1) failed SNPs and (2) non-SNP entries in vardb matrix.

        # VCF positives (intersect).
        for pos in sorted(vcf_positive_positions):
            self.vcf_positive_report.append(self.vcf[pos]['vcf line'])

        # VCF negatives (difference).
        for pos in sorted(set(self.vcf.keys()).difference(vcf_positive_positions)):
            self.vcf_negative_report.append(self.vcf[pos]['vcf line'])

        return

    def populate_vardb_read_counts(self, refid):

        # Update the 'Read Counts' field for all possible Genomic Variant
        # positions in the vardb entries.

        df = self.vardb.groupby('Reference Genome Accession ID').get_group(refid)
        for id_ in df.index:
            variants = df.loc[id_]['Genomic Variant List']
            variants = variants[1:-1]
            variants = re.sub(' ', '', variants)
            variants = re.sub('\'', '', variants)
            variants = variants.split(',')

            read_counts = list()

            for var in variants:
                # Multiples.
                if re.search(':', var):
                    var_set = var.split(':')
                    for variant in var_set:
                        variant_position = int(variant[2:-3])  # 0-based
                        if variant_position in self.read_counts.keys():
                            read_counts.append(self.read_counts[variant_position + 1])
                        else:
                            read_counts.append('0')
                else:
                    # Singles.
                    variant_position = int(var[2:-3])  # 0-based
                    if variant_position in self.read_counts.keys():
                        read_counts.append(self.read_counts[variant_position + 1])
                    else:
                        read_counts.append('0')

            self.vardb.at[id_, 'Read Counts'] = read_counts

        return


def eval_cli_arguments():

    parser = argparse.ArgumentParser(
        description='Reports concordance of variants of interest.',
        prog='variant_concordance.py',
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
        '--vardb',
        metavar='FILE',
        action='store',
        help='Path to variant database.',
        required=True,
    )

    required_group.add_argument(
        '--counts',
        metavar='FILE',
        action='store',
        help='Path to read counts file.',
        required=True,
    )

    required_group.add_argument(
        '--vcfreport',
        metavar='FILE',
        action='store',
        help='Path to write vcf report file.',
        required=True
    )

    required_group.add_argument(
        '--vardbreport',
        metavar='FILE',
        action='store',
        help='Path to write vardb report file.',
        required=True
    )

    required_group.add_argument(
        '--snpvcf',
        metavar='FILE',
        action='store',
        help='Path to snp VCF file.',
        required=True,
    )

    required_group.add_argument(
        '--indelvcf',
        metavar='FILE',
        action='store',
        help='Path to indel VCF file',
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
        '--refid',
        metavar='STR',
        action='store',
        help='Reference genome id associated with VCFs.',
        required=True,
        type=str
    )

    return parser.parse_args()


def populate_var_db(arguments):

    # We will be creating a dataframe for the database of important
    # known-variants.

    df = pd.read_csv(arguments.vardb, sep='\t', comment='#')

    # Placeholder for extended VCF-related fields.

    df['Sample ID'] = arguments.sampleid
    df['Read Counts'] = '[]'
    df['VCF Filter'] = '[]'
    df['VCF Positives'] = '[]'
    df['VCF ADP'] = '[]'
    df['VCF Ref'] = '[]'
    df['VCF Alt'] = '[]'
    df['VCF GT'] = '[]'
    df['VCF Freq'] = '[]'
    df['VCF SDP'] = '[]'
    df['VCF DP'] = '[]'
    df['VCF Lines'] = '[]'

    return df


def df_vardb_add_mock_positives(df_vardb):

    # We will be adding a couple of mock positive variants for testing
    # purposes. These tests will be added to the vardb dataframe. We
    # will add entries for a positive SNV (single) and a MNV
    # (multiple, mutually exclusive) cases. NOTE: The majority of info
    # in these entries is not accurate, but rather placeholder
    # information.

    # NC_001798 : g.10178C>T
    # NC_001798 : g.154371C>T:g.154372G>A

    mock_snv = df_vardb.loc[0].to_dict()
    mock_snv['Genomic Variant List'] = "['g.10177C>T', 'g.154370C>T:g.154371G>A']"
    mock_snv['Virus'] = 'MOCK'
    mock_snv['Reference Genome Accession ID'] = 'NC_001798'
    mock_snv['Comment'] = 'Mock virus for testing.'
    mock_snv = {0: mock_snv}
    df_mock_snv = pd.DataFrame.from_dict(mock_snv, 'index')
    df_vardb = pd.concat([df_vardb, df_mock_snv]).reset_index(drop=True)

    return df_vardb


if __name__ == '__main__':

    # Given a database of variants of interest, we will be intersecting
    # with variants in supplied VCF files. The ultimate purpose of this
    # code is to generate a report highlighting concordance of sample
    # variants with the database of important known-variants.

    arguments = eval_cli_arguments()
    df_vardb = populate_var_db(arguments)
    df_vardb = df_vardb_add_mock_positives(df_vardb)  # optional

    concordance = _Concordance(
        vardb=df_vardb,
        vcf=arguments.snpvcf,
        counts=arguments.counts
    )
    concordance.populate_vardb_read_counts(refid=arguments.refid)
    concordance.evaluate_concordance(refid=arguments.refid, sampleid=arguments.sampleid)
    # concordance.write_vardb_report(arguments.vardbreport)
    # concordance.write_vcf_report(arguments.vcfreport)
    # pprint(concordance.vcf_positive_report)
    # pprint(concordance.vcf)

# __END__
