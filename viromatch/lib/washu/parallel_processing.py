import yaml
import sys
import os


class ParallelProcessing():

    def __init__(self, arguments):

        self.arguments = arguments

        return

    def generate_wustl_cmd(self):

        # We will generate a command specific for the LSF queue at Washington
        # University School of Medicine, St. Louis. We will also copy the
        # information from the --wustlconfig file to out processing directory.

        # Possible entries are as follows. All but "ignore hosts" are mandatory.

        # docker:
        #   image: 'twylie/vm:41'
        #   volumes:
        #     - '/storage1/fs1/tnwylie_lab/Active/viroMatchDatabases:/db'
        #     - '/storage1/fs1/kwylie/Active/2020_09_21_AHA:/pwd'
        # lsf:
        #   memory: '16G'
        #   cores: '100'
        #   local cores: '1'
        #   compute group: 'compute-kwylie'
        #   queue: 'general'
        #   restart times: '3'
        #   latency wait: '100'
        #   ignore hosts:
        #     - 'compute1-exec-67.ris.wustl.edu'
        #     - 'compute1-exec-117.ris.wustl.edu'
        #     - 'compute1-exec-102.ris.wustl.edu'

        with open(self.arguments.wustlconfig, 'r') as fh:
            args = yaml.load(fh, Loader=yaml.FullLoader)

        # Minimal field checking.

        if 'docker' not in args.keys():
            error = '\nError: --wustlconfig requires {}\n'.format('[docker:]')
            print(error)
            sys.exit()

        if 'lsf' not in args.keys():
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf:]')
            print(error)
            sys.exit()

        if 'image' not in args['docker'].keys():
            error = '\nError: --wustlconfig requires {}\n'.format('[docker: image]')
            print(error)
            sys.exit()

        if 'volumes' not in args['docker'].keys():
            error = '\nError: --wustlconfig requires {}\n'.format('[docker: volumes]')
            print(error)
            sys.exit()

        if 'memory' not in args['lsf'].keys():
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf: memory]')
            print(error)
            sys.exit()

        if 'cores' not in args['lsf'].keys():
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf: cores]')
            print(error)
            sys.exit()

        if 'local cores' not in args['lsf'].keys():
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf: local cores]')
            print(error)
            sys.exit()

        if 'compute group' not in args['lsf']:
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf: compute group]')
            print(error)
            sys.exit()

        if 'queue' not in args['lsf']:
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf: queue]')
            print(error)
            sys.exit()

        if 'restart times' not in args['lsf']:
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf: restart times]')
            print(error)
            sys.exit()

        if 'latency wait' not in args['lsf']:
            error = '\nError: --wustlconfig requires {}\n'.format('[lsf: latency wait]')
            print(error)
            sys.exit()

        # Add the lsf submitter configuration information to our arguments.

        self.arguments.docker_image = args['docker']['image']
        self.arguments.docker_volumes = args['docker']['volumes']
        self.arguments.lsf_memory = args['lsf']['memory']
        self.arguments.lsf_cores = args['lsf']['cores']
        self.arguments.lsf_local_cores = args['lsf']['local cores']
        self.arguments.lsf_compute_group = args['lsf']['compute group']
        self.arguments.lsf_queue = args['lsf']['queue']
        self.arguments.lsf_restart_times = args['lsf']['restart times']
        self.arguments.lsf_latency_wait = args['lsf']['latency wait']
        self.arguments.docker_submitter = self.arguments.outdir + 'lsf_submitter.py'
        self.arguments.lsf_logdir = self.arguments.outdir + 'lsf_logs/'

        if os.path.isdir(self.arguments.lsf_logdir) is False:
            os.mkdir(self.arguments.lsf_logdir, 0o755)

        # Passed, so cat the LSF config file to the main Snakemake config file.

        args['lsf']['log directory'] = self.arguments.lsf_logdir

        with open(self.arguments.config, 'a') as config_fh:
            yaml.dump(args, config_fh)

        # Maybe the user passed the ignore hosts list?

        if 'ignore hosts' in args['lsf']:
            self.arguments.lsf_ignore_hosts = args['lsf']['ignore hosts']
        else:
            self.arguments.lsf_ignore_hosts = None

        # Now we can actually build the LSF/Snakemake command.

        cmd = [
            'snakemake',
            '--directory',
            self.arguments.outdir,
            '--snakefile',
            self.arguments.outdir + 'Snakefile',
            '--stats',
            self.arguments.outdir + 'stats.log',
            '--cluster',
            self.arguments.docker_submitter,
            '--cores',
            self.arguments.lsf_cores,
            '--local-cores',
            self.arguments.lsf_local_cores,
            '--restart-times',
            self.arguments.lsf_restart_times,
            '--latency-wait',
            self.arguments.lsf_latency_wait,
            '-p',
            '--rerun-incomplete'
        ]

        return self.arguments, cmd

    def generate_lsf_submitter_script(self):

        # We will generate a LSF submitter script specific for the LSF queue at
        # Washington University School of Medicine, St. Louis. Snakemake, in
        # --cluster mode, will submit sub-preocess (child) jobs to this script,
        # while the parent job keeps track of all children.

        with open(self.arguments.docker_submitter, 'w') as submitter_fh:

            submitter_fh.write('#!/usr/bin/python3.7\n\n')
            submitter_fh.write('# == AUTO-GENERATED CODE ==\n\n')
            submitter_fh.write('# ------------------------------------------------------------------------------\n')
            submitter_fh.write('# Washington University School of Medicine\n')
            submitter_fh.write('# High Performance Computing (LSF)\n')
            submitter_fh.write('# ------------------------------------------------------------------------------\n\n')
            submitter_fh.write('# This script may be used by Snakemake to submit sub-processing to the WashU LSF\n')
            submitter_fh.write('# system in parallel. We will be using Docker instances of the ViroMatch Docker\n')
            submitter_fh.write('# container to run these processes. The master Snakemake job will poll to see\n')
            submitter_fh.write('# when the sub-processes are finished also keep track of jobs based on the\n')
            submitter_fh.write('# original DAG.\n\n')
            submitter_fh.write('import os\n')
            submitter_fh.write('import sys\n')
            submitter_fh.write('from snakemake.utils import read_job_properties\n\n')
            submitter_fh.write('jobscript = sys.argv[-1]\n')
            submitter_fh.write('props = read_job_properties(jobscript)\n')
            submitter_fh.write("job_id = props['jobid']\n\n")

            docker_volumes = ' '.join(self.arguments.docker_volumes)

            err_log = self.arguments.lsf_logdir + 'LSF.err.{}'
            out_log = self.arguments.lsf_logdir + 'LSF.out.{}'

            if self.arguments.lsf_ignore_hosts:
                ignore_hosts = list()
                for host in self.arguments.lsf_ignore_hosts:
                    host = 'hname!=\'' + host + '\''
                    ignore_hosts.append(host)
                ignore_hosts = ' && '.join(ignore_hosts)
                cmd = ' '.join([
                    r'LSF_DOCKER_VOLUMES=\"{}\"'.format(docker_volumes),
                    'bsub',
                    r'-R \"select[{}]\"'.format(ignore_hosts)
                ])
            else:
                cmd = ' '.join([
                    r'LSF_DOCKER_VOLUMES=\"{}\"'.format(docker_volumes),
                    'bsub',
                ])

            cmd += ' '.join([
                ' -M {}'.format(self.arguments.lsf_memory),
                r'-R \"select[mem>{}] rusage[mem={}]\"'.format(self.arguments.lsf_memory, self.arguments.lsf_memory),
                '-G {}'.format(self.arguments.lsf_compute_group),
                '-q {}'.format(self.arguments.lsf_queue),
                '-e {}'.format(err_log),
                '-o {}'.format(out_log),
                "-a 'docker({})'".format(self.arguments.docker_image),
                '{}'
            ])

            submitter_fh.write('cmd = "' + cmd + '".format(job_id, job_id, jobscript)' + '\n\n')

            submitter_fh.write('print(cmd)\n')
            submitter_fh.write('os.system(cmd)\n\n')
            submitter_fh.write('# __END__\n')

            # Make executable.

        os.chmod(self.arguments.docker_submitter, 0o777)

        return
