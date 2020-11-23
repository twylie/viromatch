import argparse
import os
import subprocess
import sys
from .. import version as ver
from .. washu import ParallelProcessing


class ViroMatch():

    """
    Provides a framework for creating the ViroMatch virome analysis
    pipeline.

    Args:
        None

    Attributes:
        distribution (dict): Info on code release/distribution.
        version (str): Revision and build info.
    """

    distribution = {
        'name': ver.name,
        'revision': ver.revision,
        'build': ver.build,
        'copyright holder': ver.copyright_holder,
        'copyright': ver.copyright_years,
        'authors': ver.authors,
    }

    version = '{} (Revision {} / Build {})'.format(
        distribution['name'],
        distribution['revision'],
        distribution['build'],
    )

    def __init__(self):

        """
        Constructs a ViroMatch object.

        Args:
            None
        """

        self.suffixes = ['r1', 'r2']
        self.arguments = None

        return

    def evaluate_cli_arguments(self):

        """
        The first step of the pipeline is to evaluate command line parameters.

        Optional and required arguments are evaluated in this method. Default
        values are set at this time. Any failures related to arguments are
        handled by this method.

        Args:
            None
        """

        parser = argparse.ArgumentParser(
            description='Read-based virome characterization pipeline.',
            prog=ViroMatch.distribution['name'].lower() + '.py',
            add_help=False
        )
        parser.prog = ver.name.lower()

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # O P T I O N A L   A R G U M E N T S
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        parser.add_argument(
            '-h',
            '--help',
            action='help',
            help='Display the extended usage statement.'
        )

        parser.add_argument(
            '--version',
            action='version',
            version=ViroMatch.version,
            help='Display the software version number.'
        )

        parser.add_argument(
            '--keep',
            action='store_true',
            help='Retain intermediate files.'
        )

        parser.add_argument(
            '--dryrun',
            action='store_true',
            help='Preps pipeline but no execution.'
        )

        parser.add_argument(
            '--variants',
            action='store_true',
            # help='Runs the extended variant calling pipeline.',
            help=argparse.SUPPRESS
        )

        parser.add_argument(
            '--smkcores',
            metavar='INT',
            action='store',
            default=1,
            type=int,
            help='Number of CPU cores for Snakemake. [1]',
        )

        parser.add_argument(
            '--endqual',
            metavar='INT',
            action='store',
            default=10,
            type=int,
            help='Trim 3\'-end when quality drops below value. [10]',
        )

        parser.add_argument(
            '--minn',
            metavar='INT',
            action='store',
            default=50,
            type=int,
            help='Max percent of Ns allowed post-trimming. [50]'
        )

        parser.add_argument(
            '--phred',
            metavar='33|64',
            action='store',
            default=33,
            type=int,
            help='Choose phred-33 or phred-64 quality encoding. [33]'
        )

        parser.add_argument(
            '--readlen',
            metavar='INT',
            action='store',
            default=50,
            type=int,
            help='Minimum read length after trimming. [50]'
        )

        parser.add_argument(
            '--pid',
            metavar='FLOAT',
            action='store',
            default=0.15,
            type=float,
            help='Max percent id variance for nucleotide hits. [0.15]'
        )

        parser.add_argument(
            '--pidprox',
            metavar='FLOAT',
            action='store',
            default=0.04,
            type=float,
            help='Max proximal percent id variance for nucleotide hits. [0.04]'
        )

        parser.add_argument(
            '--bsize',
            metavar='INT',
            action='store',
            default=1,
            type=int,
            help='Buffer size for sorting (Gb). [1]'
        )

        parser.add_argument(
            '--bitprox',
            metavar='INT',
            action='store',
            default=1,
            type=int,
            help='Max proximal bitscore for translated hits. [1]'
        )

        parser.add_argument(
            '--mts',
            metavar='INT',
            action='store',
            default=5,
            type=int,
            help='Translated nucleotide max-target-seqs. [5]'
        )

        parser.add_argument(
            '--evalue',
            metavar='FLOAT',
            action='store',
            default=0.001,
            type=float,
            help='Translated nucleotide max-expect-value. [0.001]'
        )

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # R E Q U I R E D   A R G U M E N T S
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        required_group = parser.add_argument_group('required')

        required_group.add_argument(
            '--sampleid',
            metavar='STR',
            action='store',
            help='Label or id for sample.',
            required=True,
        )

        required_group.add_argument(
            '--input',
            metavar='FILE',
            action='store',
            help='Path to single input BAM or paired FASTQ file(s).',
            required=True,
            nargs='+'
        )

        required_group.add_argument(
            '--outdir',
            metavar='DIR',
            action='store',
            help='Path to directory for writing output.',
            required=True
        )

        required_group.add_argument(
            '--nt',
            metavar='FILE',
            action='store',
            help='NCBI nt nucleotide FASTA file(s) or NT.fofn file.',
            required=True,
            nargs='+'
        )

        required_group.add_argument(
            '--nr',
            metavar='FILE',
            action='store',
            help='NCBI nr protein FASTA file(s) or NR.fofn file.',
            required=True,
            nargs='+'
        )

        required_group.add_argument(
            '--viralfna',
            metavar='FILE',
            action='store',
            help='Viral identity (indexed) nucleotide FASTA file.',
            required=True
        )

        required_group.add_argument(
            '--viralfaa',
            metavar='FILE',
            action='store',
            help='Viral identity (indexed) translated FASTA file.',
            required=True
        )

        required_group.add_argument(
            '--host',
            metavar='FILE',
            action='store',
            help='Host (indexed) FASTA file for host screening.',
            required=True
        )

        required_group.add_argument(
            '--adaptor',
            metavar='FILE',
            action='store',
            help='File with adapter sequences to trim.',
            required=True
        )

        required_group.add_argument(
            '--taxid',
            metavar='FILE',
            action='store',
            help='Taxonomy ID lookup file.',
            required=True,
        )

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # W U S T L   O N L Y
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        wustl_group = parser.add_argument_group('Washington University only (LSF cluster submission)')

        wustl_group.add_argument(
            '--wustlconfig',
            metavar='FILE',
            action='store',
            help='Path to config file for WUSTL LSF parallel processing.',
            type=str,
        )

        self.arguments = parser.parse_args()

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # E V A L U A T I O N   L O G I C
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        # Evaluate the outdir path; if needed, create the outdir directory.

        if self.arguments.outdir[-1:] != '/':
            self.arguments.outdir += '/'

        if os.path.isdir(self.arguments.outdir) is True:
            outdir_error = 'The --outdir path "{}" already exists.'.format(self.arguments.outdir)
            parser.error(outdir_error)
        elif os.path.isdir(self.arguments.outdir) is False:
            os.mkdir(self.arguments.outdir, 0o755)

        # Validate its existence of the adaptor file.

        if self.arguments.adaptor is not None:
            if os.path.isfile(self.arguments.adaptor) is False:
                adaptor_error = 'Adaptor file does not exist.'
                parser.error(adaptor_error)

        # Phred value can only be 33 or 64, no other value.

        if int(self.arguments.phred) != 33 and int(self.arguments.phred) != 64:
            phred_error = 'The --phred value is {}. Valid values are 33 or 64.'.format(self.arguments.phred)
            parser.error(phred_error)

        # Evaluate the percent identity variance values.

        if self.arguments.pid < 0.01 or self.arguments.pid > 0.99:
            pid_error = 'The --pid value is {}. Valid values are 0.01-0.99 in range.'.format(self.arguments.pid)
            parser.error(pid_error)

        if self.arguments.pidprox < 0.01 or self.arguments.pidprox > 0.99:
            pidprox_error = 'The --pidprox value is {}. Valid values are 0.01-0.99 in range.'.format(self.arguments.pidprox)
            parser.error(pidprox_error)

        # The user might pass FOFNs for the -nt argument, which must have
        # the "fofn" suffix.

        if len(self.arguments.nt) == 1:
            suffix = self.arguments.nt[0][-4:]
            if suffix != 'fofn' and suffix != 'FOFN':
                nt_error = 'The --nt file does not have a "fofn" suffix.'
                parser.error(nt_error)
            else:
                nt_tmp = list()
                with open(self.arguments.nt[0], 'r') as nt_fh:
                    for nt in nt_fh:
                        nt = nt.strip()
                        nt_tmp.append(nt)
                self.arguments.nt = nt_tmp

        # The user might pass FOFNs for the -nr argument, which must have
        # the "fofn" suffix.

        if len(self.arguments.nr) == 1:
            suffix = self.arguments.nr[0][-4:]
            if suffix != 'fofn' and suffix != 'FOFN':
                nr_error = 'The --nr file does not have a "fofn" suffix.'
                parser.error(nr_error)
            else:
                nr_tmp = list()
                with open(self.arguments.nr[0], 'r') as nr_fh:
                    for nr in nr_fh:
                        nr = nr.strip()
                        nr_tmp.append(nr)
                self.arguments.nr = nr_tmp

        # The user may pass a single BAM file as input, or paired (R1 & R2
        # FASTQ files.

        if len(self.arguments.input) == 1:
            self.arguments.bam = True
            if os.path.isfile(self.arguments.input[0]) is False:
                input_error = 'BAM file does not exist.'
                parser.error(input_error)
        elif len(self.arguments.input) == 2:
            self.arguments.bam = False
            fastq1_check = os.path.isfile(self.arguments.input[0])
            fastq2_check = os.path.isfile(self.arguments.input[1])
            if fastq1_check is False or fastq2_check is False:
                input_error = 'One or both of the FASTQ files does not exist.'
                parser.error(input_error)
        else:
            input_error = 'Incorrect (or too many) targets passed to the --input argument.'
            parser.error(input_error)

        return

    def select_snakefile_recipe(self):

        if self.arguments.variants is True:
            snakefile = '/usr/lib/python3.7/viromatch/recipes/viromatch_variants.smk'
        else:
            snakefile = '/usr/lib/python3.7/viromatch/recipes/viromatch.smk'

        return snakefile

    def execute_snakemake_pipeline(self):

        # EXAMPLE:
        # snakemake --directory <DIR> --snakefile <FILE> --notemp --stats <FILE>

        if self.arguments.wustlconfig:
            pp = ParallelProcessing(self.arguments)
            self.arguments, cmd = pp.generate_wustl_cmd()
            pp.generate_lsf_submitter_script()
        else:
            cmd = [
                'snakemake',
                '--directory',
                self.arguments.outdir,
                '--snakefile',
                self.arguments.outdir + 'Snakefile',
                '--stats',
                self.arguments.outdir + 'stats.log',
                '-p',
                '--cores',
                str(self.arguments.smkcores)
            ]

        if self.arguments.keep is True:
            cmd.append('--notemp')

        # Write the Snakemake command to the processing directory for
        # reference.

        cmd_file = self.arguments.outdir + 'cmd.sh'
        with open(cmd_file, 'w') as fh:
            cmd_line = ' '.join(cmd)
            fh.write(cmd_line + '\n')
        self.arguments.cmd_file = cmd_file

        # Write the pipeline steps to a log file.

        cmd_steps = [
            'snakemake',
            '--directory',
            self.arguments.outdir,
            '--snakefile',
            self.arguments.outdir + 'Snakefile',
            '-l',
        ]
        steps_file = self.arguments.outdir + 'steps.txt'
        steps_fh = open(steps_file, 'w')
        subprocess.call(cmd_steps, stdout=steps_fh)
        steps_fh.close()

        # Execute the Snakemake pipeline unless the user has chosen the
        # --dryrun option.

        if self.arguments.dryrun is True:
            print('\nPREPARED: ' + self.arguments.outdir + '\n')
            sys.exit()
        elif self.arguments.wustlconfig:
            docker_volumes = ' '.join(self.arguments.docker_volumes)
            if self.arguments.lsf_ignore_hosts:
                ignore_hosts = list()
                for host in self.arguments.lsf_ignore_hosts:
                    host = 'hname!=\'' + host + '\''
                    ignore_hosts.append(host)
                ignore_hosts = ' && '.join(ignore_hosts)
                cmd = ' '.join([
                    'LSF_DOCKER_VOLUMES="{}"'.format(docker_volumes),
                    'bsub',
                    '-R "select[{}]"'.format(ignore_hosts)
                ])
            else:
                cmd = ' '.join([
                    'LSF_DOCKER_VOLUMES="{}"'.format(docker_volumes),
                    'bsub',
                ])
            cmd += ' '.join([
                ' -M {}'.format(self.arguments.lsf_memory),
                '-R "select[mem>{}] rusage[mem={}]"'.format(self.arguments.lsf_memory, self.arguments.lsf_memory),
                '-G {}'.format(self.arguments.lsf_compute_group),
                '-q {}'.format(self.arguments.lsf_queue),
                '-e {}LSF.master.err'.format(self.arguments.outdir),
                '-o {}LSF.master.out'.format(self.arguments.outdir),
                "-a 'docker({})'".format(self.arguments.docker_image),
                'sh',
                '{}cmd.sh'.format(self.arguments.outdir)
            ])
            os.system(cmd)
        else:
            subprocess.call(cmd)

        return


# __END__
