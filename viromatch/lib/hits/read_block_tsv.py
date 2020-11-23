import random
import re


class ReadBlockTsv():

    # A read block is a list of alignment report lines, all having the same
    # read id. In this way, we evaluate a smaller chunk of alignments at
    # any one time. Although the alignment formats for nt and nr are
    # different, the concept is the same.

    def __init__(self, arguments, read_id, best_score, taxonomy, read_block):

        self.arguments = arguments
        self.taxonomy = taxonomy
        self.read_id = read_id
        self.best_score = best_score
        self.read_block = read_block
        self.read_block_size = len(read_block)
        self.passed_best_hits = list()
        self.failed_best_hits = list()
        self.passed_neighbors = list()
        self.failed_neighbors = list()
        self.secondary = list()
        self.best_hit = None
        self.best_hit_lineage = None
        self.best_hit_acc_id = None
        self.best_hit_tax_id = None
        self.best_hit_bitscore = None
        self.best_hit_species = None

        return

    def update_best_hit(self, line):

        self.best_hit = line
        fields = self.best_hit.split('\t')
        self.best_hit_acc_id, self.best_hit_tax_id = fields[1].split('|')[-2:]
        self.best_hit_bitscore = float(fields[11])
        self.best_hit_lineage = self.taxonomy.lookup_lineage(self.best_hit_tax_id)
        self.best_hit_species = self.best_hit_lineage.species()

        return

    def print_secondary_nn_fail(self):

        for line in self.secondary:
            fields = line.split('\t')
            acc_id, tax_id = fields[1].split('|')[-2:]
            bitscore = float(fields[11])

            msg = '\t'.join([
                'FAIL',
                'SECONDARY NN',
                '{}'.format(self.read_block_size),
                self.read_id,
                'secondary, non-neighbor hit',
                str(bitscore),
                acc_id,
                self.taxonomy.lookup_lineage(tax_id).species(),
                self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
            ])
            self.arguments.fh_log.write(msg + '\n')

        return

    def print_unknown(self, read_id, acc_id, tax_id, lineage):

        msg = '\t'.join([
            'IGNORED',
            'UNKNOWN TAXA',
            read_id,
            'superkingdom is unknown, investigate',
            acc_id,
            tax_id,
            lineage
        ])
        self.arguments.fh_log_unknown.write(msg + '\n')

        return

    def print_other_sequences(self, read_id, acc_id, tax_id, lineage):

        msg = '\t'.join([
            'IGNORED',
            'OTHER SEQ',
            read_id,
            'taxonomy matches \'other sequences\', investigate',
            acc_id,
            tax_id,
            lineage
        ])
        self.arguments.fh_log_other_seq.write(msg + '\n')

        return

    def print_tied_best_hit_fail(self, line):

        fields = line.split('\t')
        acc_id, tax_id = fields[1].split('|')[-2:]
        bitscore = float(fields[11])

        msg = '\t'.join([
            'FAIL',
            'TIED BEST HIT',
            '{}'.format(self.read_block_size),
            self.read_id,
            'failed best hit (tied)',
            str(bitscore),
            acc_id,
            self.taxonomy.lookup_lineage(tax_id).species(),
            self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
        ])
        self.arguments.fh_log.write(msg + '\n')

        return

    def print_random_best_hit_pass(self):

        msg = '\t'.join([
            'PASS',
            'RANDOM BEST HIT',
            '{}'.format(self.read_block_size),
            self.read_id,
            'randomly chosen best hit (tied)',
            str(self.best_hit_bitscore),
            self.best_hit_acc_id,
            self.best_hit_species,
            self.best_hit_lineage.flatten_lineage()
        ])
        self.arguments.fh_log.write(msg + '\n')

        return

    def print_best_hit_pass(self):

        msg = '\t'.join([
            'PASS',
            'BEST HIT',
            '{}'.format(self.read_block_size),
            self.read_id,
            'best hit',
            str(self.best_hit_bitscore),
            self.best_hit_acc_id,
            self.best_hit_species,
            self.best_hit_lineage.flatten_lineage()
        ])
        self.arguments.fh_log.write(msg + '\n')

        return

    def fail_read_block_ambiguous_superkingdom(self):

        for line in self.read_block:
            fields = line.split('\t')
            acc_id, tax_id = fields[1].split('|')[-2:]
            bitscore = float(fields[11])

            msg = '\t'.join([
                'FAIL',
                'RB AMBIGUITY',
                '{}'.format(self.read_block_size),
                self.read_id,
                'significant ambiguous, non-viral hit',
                str(bitscore),
                acc_id,
                self.taxonomy.lookup_lineage(tax_id).species(),
                self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
            ])
            self.arguments.fh_log.write(msg + '\n')

        return [self.best_hit, self.best_hit_lineage]

    def fail_viral_neighbor_reads(self):

        for line in self.passed_neighbors:
            fields = line.split('\t')
            acc_id, tax_id = fields[1].split('|')[-2:]
            bitscore = float(fields[11])

            msg = '\t'.join([
                'FAIL',
                'NEIGHBOR',
                '{}'.format(self.read_block_size),
                self.read_id,
                'viral neighbor hit',
                str(bitscore),
                acc_id,
                self.taxonomy.lookup_lineage(tax_id).species(),
                self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
            ])
            self.arguments.fh_log.write(msg + '\n')

        return

    def evaluate_read_block(self):

        for line in reversed(self.read_block):
            original_line = line
            line = line.strip()
            fields = line.split('\t')
            acc_id, tax_id = fields[1].split('|')[-2:]
            bitscore = float(fields[11])

            # If a read's lineage matches the "other sequences" category,
            # we are going to ignore the read, but we will quantify and
            # report how many reads are affected.

            lineage = self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
            if re.search('other sequences', lineage):
                self.print_other_sequences(
                    self.read_id,
                    acc_id,
                    tax_id,
                    lineage
                )
                self.read_block.remove(original_line)
                self.read_block_size -= 1
                continue

            # If a read's superkingdom is "Unknown", we can't really
            # evaluate if the read is a virus or non-viral, so we will
            # ignore/skip the read; however, we will quantify and report
            # how many reads are affected.

            superkingdom = self.taxonomy.lookup_lineage(tax_id).superkingdom()
            if superkingdom == 'Unknown':
                self.print_unknown(
                    self.read_id,
                    acc_id,
                    tax_id,
                    lineage
                )
                self.read_block.remove(original_line)
                self.read_block_size -= 1
                continue

            # If a hit's BITSCORE value equals the best score, and
            # superkingdom taxonomy is equal to 'Viruses', then collect the
            # hit as being punitively passed. Else, if superkingdom is not
            # 'Viruses', fail the read.

            # If the nr hit's BITSCORE value is within proximal range to
            # the best BITSCORE, and superkingdom taxonomy is equal to
            # 'Viruses', then collect the read as being passed. Else, if
            # superkingdom is not 'Viruses', fail the read.

            # Finally, any other condition will be a read failure, or
            # secondary hit that does not pass previous requirements.

            if bitscore == self.best_score:
                if superkingdom == 'Viruses':
                    self.passed_best_hits.append(line)
                else:
                    self.failed_best_hits.append(line)
            elif bitscore >= (self.best_score - self.arguments.bitprox) and bitscore < self.best_score:
                if superkingdom == 'Viruses':
                    self.passed_neighbors.append(line)
                else:
                    self.failed_neighbors.append(line)
            else:
                self.secondary.append(line)

        # If any significant hit in a read block fails because superkingdom
        # taxonomy does not match 'Viruses', then fail all of the read
        # block reads.

        if len(self.failed_best_hits + self.failed_neighbors) > 0:
            return self.fail_read_block_ambiguous_superkingdom()

        # Read block has passed taxonomy evaluation at this point.
        # Neighboring secondary hits were only used to evaluate
        # superkingdom taxonomy for the read block. We still fail those
        # that matched 'Viruses', as we are now looking for a best hit for
        # the read block.

        self.fail_viral_neighbor_reads()
        self.print_secondary_nn_fail()

        # If the best score has tied hits, randomly choose a best hit
        # representative; the other tied-hits will be failed.

        if len(self.passed_best_hits) > 1:
            self.update_best_hit(random.choice(self.passed_best_hits))
            self.print_random_best_hit_pass()
            for hit in self.passed_best_hits:
                if hit is not self.best_hit:
                    self.print_tied_best_hit_fail(hit)
        elif len(self.passed_best_hits) == 1:
            self.update_best_hit(self.passed_best_hits[0])
            self.print_best_hit_pass()

        return [self.best_hit, self.best_hit_lineage]


# __END__
