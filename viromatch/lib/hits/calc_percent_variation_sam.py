import re
import sys


class CalcPercentVariationSam():

    # Given a SAM line, we may reconstruct the sequence alignment and
    # calculate the percent variation, query-to-subject.

    def __init__(self, sam_line):

        # |--------+-------------------------------------------|
        # | CODE   | DESCRIPTION                               |
        # |--------+-------------------------------------------|
        # | NM     | edit distance (mismatches + I + D )       |
        # | H      | hard clipping (excised in query sequence) |
        # | S      | soft clipping (masked in query sequence)  |
        # | M      | match or mismatch at locus                |
        # | I      | insertion (query-side)                    |
        # | D      | deletion (query-side)                     |
        # |--------+-------------------------------------------|

        self.sam_line = sam_line
        self.read_id = None
        self.ref_id = None
        self.cigar = None
        self.variant_bases = None
        self.alignment_length = None
        self.percent_variation = None
        self.md = None              # MD
        self.nm = None              # NM
        self.hard_clipping = 0      # H
        self.soft_clipping = 0      # S
        self.match_or_mismatch = 0  # M
        self.insertion = 0          # I
        self.deletion = 0           # D

        return

    def calc_percent_variation(self):

        f = self.sam_line.split('\t')
        self.read_id = f[0]
        self.ref_id = f[2]
        self.cigar = f[5]
        self.nm = int(f[11].split(':')[2])
        self.md = f[12].split(':')[2]

        # We can walk through the CIGAR string and collect the associated
        # position categories. These designations will help us determine
        # sequence alignment specifics downstream.

        categories = list(filter(None, re.split(r'(\d+)', self.cigar)))
        pairs = list()
        for i in range(0, len(categories), 2):
            pairs.append([categories[i], categories[i + 1]])

        for [count, code] in pairs:
            if code == 'H':
                self.hard_clipping += int(count)
            elif code == 'S':
                self.soft_clipping += int(count)
            elif code == 'M':
                self.match_or_mismatch += int(count)
            elif code == 'I':
                self.insertion += int(count)
            elif code == 'D':
                self.deletion += int(count)
            else:
                print('ERROR: Unknown CIGAR string category of type {} encountered!'.format(code))
                sys.exit()

        # |------------------+-------------------|
        # | DESCRIPTION      | CALCULATION       |
        # |------------------+-------------------|
        # | variant bases    | NM + H + S        |
        # | alignment length | S + H + M + I + D |
        # |------------------+-------------------|

        self.variant_bases = self.nm + self.hard_clipping + self.soft_clipping
        self.alignment_length = self.soft_clipping + self.hard_clipping + self.match_or_mismatch + \
            self.insertion + self.deletion
        self.percent_variation = round(self.variant_bases / self.alignment_length, 4)

        return self.percent_variation


# __END__
