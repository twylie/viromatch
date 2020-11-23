import random
import re


class ReadBlockSam():

    # A read block is a list of alignment report lines, all having the same
    # read id. In this way, we evaluate a smaller chunk of alignments at
    # any one time. Although the alignment formats for nt and nr are
    # different, the concept is the same.

    def __init__(self, arguments, read_id, best_score, taxonomy, read_block):

        read_block_lines = [i[0] for i in read_block]

        self.arguments = arguments
        self.taxonomy = taxonomy
        self.read_id = read_id
        self.best_score = best_score
        self.read_block = read_block
        self.read_block_size = len(read_block_lines)
        self.passed_best_hits = list()
        self.failed_best_hits = list()
        self.passed_neighbors = list()
        self.failed_neighbors = list()
        self.secondary = list()
        self.best_hit = None
        self.best_hit_lineage = None
        self.best_hit_acc_id = None
        self.best_hit_tax_id = None
        self.best_hit_pid = None
        self.best_hit_species = None

        return

    def update_best_hit(self, line):

        line, pid = line
        self.best_hit = line
        fields = self.best_hit.split('\t')
        self.best_hit_acc_id, self.best_hit_tax_id = fields[2].split('|')[-2:]
        self.best_hit_pid = pid
        self.best_hit_lineage = self.taxonomy.lookup_lineage(self.best_hit_tax_id)
        self.best_hit_species = self.best_hit_lineage.species()

        return

    def print_secondary_nn_fail(self):

        for line in self.secondary:
            line, pid = line
            fields = line.split('\t')
            acc_id, tax_id = fields[2].split('|')[-2:]

            msg = '\t'.join([
                'FAIL',
                'SECONDARY NN',
                '{}'.format(self.read_block_size),
                self.read_id,
                'secondary, non-neighbor hit',
                str(pid),
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

        line, pid = line
        fields = line.split('\t')
        acc_id, tax_id = fields[2].split('|')[-2:]

        msg = '\t'.join([
            'FAIL',
            'TIED BEST HIT',
            '{}'.format(self.read_block_size),
            self.read_id,
            'failed best hit (tied)',
            str(pid),
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
            str(self.best_hit_pid),
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
            str(self.best_hit_pid),
            self.best_hit_acc_id,
            self.best_hit_species,
            self.best_hit_lineage.flatten_lineage()
        ])
        self.arguments.fh_log.write(msg + '\n')

        return

    def fail_read_block_pid(self):

        for line in self.read_block:
            line, pid = line
            fields = line.split('\t')
            acc_id, tax_id = fields[2].split('|')[-2:]

            msg = '\t'.join([
                'FAIL',
                'RB PID',
                '{}'.format(self.read_block_size),
                self.read_id,
                'best score {} > {}'.format(self.best_score, self.arguments.pid),
                str(pid),
                acc_id,
                self.taxonomy.lookup_lineage(tax_id).species(),
                self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
            ])
            self.arguments.fh_log.write(msg + '\n')

        return [self.best_hit, self.best_hit_lineage]

    def fail_read_block_ambiguous_superkingdom(self):

        for line in self.read_block:
            line, pid = line
            fields = line.split('\t')
            acc_id, tax_id = fields[2].split('|')[-2:]

            msg = '\t'.join([
                'FAIL',
                'RB AMBIGUITY',
                '{}'.format(self.read_block_size),
                self.read_id,
                'significant ambiguous, non-viral hit',
                str(pid),
                acc_id,
                self.taxonomy.lookup_lineage(tax_id).species(),
                self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
            ])
            self.arguments.fh_log.write(msg + '\n')

        return [self.best_hit, self.best_hit_lineage]

    def fail_viral_neighbor_reads(self):

        for line in self.passed_neighbors:
            line, pid = line
            fields = line.split('\t')
            acc_id, tax_id = fields[2].split('|')[-2:]

            msg = '\t'.join([
                'FAIL',
                'NEIGHBOR',
                '{}'.format(self.read_block_size),
                self.read_id,
                'viral neighbor hit',
                str(pid),
                acc_id,
                self.taxonomy.lookup_lineage(tax_id).species(),
                self.taxonomy.lookup_lineage(tax_id).flatten_lineage()
            ])
            self.arguments.fh_log.write(msg + '\n')

        return

    def evaluate_read_block(self):

        # NOTE: We may have been passed "blank" arguments during
        # initialization, so check for None types as needed.

        # We fail an entire read block if the block's best score is greater
        # than pid, which should be explicitly supplied to the class
        # instance under arguments.

        if self.best_score is not None:
            if self.best_score > self.arguments.pid:
                return self.fail_read_block_pid()

        for line in reversed(self.read_block):
            original_line = line
            line, pid = line
            line = line.strip()
            fields = line.split('\t')
            acc_id, tax_id = fields[2].split('|')[-2:]

            # If a hit's lineage matches the "other sequences" category, we are
            # going to ignore the hit, but we will quantify and report how many
            # hits are affected.

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

            # If a hit's superkingdom is "Unknown", we can't really evaluate if
            # the hit is a virus or non-viral, so we will ignore/skip the hit
            # however, we will quantify and report how many hits are affected.

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

            # If a hit's pid equals the best score, and superkingdom
            # taxonomy is equal to 'Viruses', then collect the hit as being
            # punitively passed. Else, if superkingdom is not 'Viruses',
            # fail the read.

            # If the hit's pid is within proximal range to the best pid
            # score, and superkingdom taxonomy is equal to 'Viruses', then
            # collect the read as being punitively passed. Else, if
            # superkingdom is not 'Viruses', fail the read.

            # Finally, any other condition will be a read failure, or
            # secondary hit that does not pass previous requirements.

            if pid == self.best_score:
                if superkingdom == 'Viruses':
                    self.passed_best_hits.append([line, pid])
                else:
                    self.failed_best_hits.append([line, pid])
            elif pid <= (self.best_score + self.arguments.pidprox):
                if superkingdom == 'Viruses':
                    self.passed_neighbors.append([line, pid])
                else:
                    self.failed_neighbors.append([line, pid])
            else:
                self.secondary.append([line, pid])

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
                line, pid = hit
                if line is not self.best_hit:
                    self.print_tied_best_hit_fail(hit)
        elif len(self.passed_best_hits) == 1:
            self.update_best_hit(self.passed_best_hits[0])
            self.print_best_hit_pass()

        return [self.best_hit, self.best_hit_lineage]


# __END__
