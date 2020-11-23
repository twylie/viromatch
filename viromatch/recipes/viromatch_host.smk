# VIROMATCH HOST / Snakemake pipeline
# viromatch_host.smk
# T.N. Wylie  <twylie@wustl.edu>

import sys
import os

configfile: 'CONFIG.yaml'


# RULES:

# all
# prep_fastq_files
# trim_fastq_files
# blank_eval_filter_low_complexity
# filter_low_complexity_fastq_files
# host_screen_mapping
# host_screen_write_unmapped_bam
# host_screen_write_unmapped_fastq


# :::::::
#  A L L
# :::::::

rule all:
    input:
        'viromatch_results/host_screen_write_unmapped_fastq/INPUT.r1.host.unmapped.fastq',
        'viromatch_results/host_screen_write_unmapped_fastq/INPUT.r2.host.unmapped.fastq'


# :::::::::::::::::::::::::::::::::
#  P R E P   F A S T Q   F I L E S
# :::::::::::::::::::::::::::::::::

# Dependencies:
# + ln
# + samtools

rule prep_fastq_files:
    input:
        config['input']
    output:
        'viromatch_results/prep_fastq_files/INPUT.r1.fastq',
        'viromatch_results/prep_fastq_files/INPUT.r2.fastq',
        cmd = 'viromatch_results/prep_fastq_files/INPUT.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.fastq.benchmark'
    run:
        if config['bam'] is False:
            cmd_link_r1 = ' '.join([
                'ln',
                '-s',
                config['input'][0],
                'viromatch_results/prep_fastq_files/INPUT.r1.fastq'
            ])

            cmd_link_r2 = ' '.join([
                'ln',
                '-s',
                config['input'][1],
                'viromatch_results/prep_fastq_files/INPUT.r2.fastq'
            ])
            shell('echo "' + cmd_link_r1 + '" > {output.cmd}')
            shell('echo "' + cmd_link_r2 + '" >> {output.cmd}')
            shell(cmd_link_r1)
            shell(cmd_link_r2)
        else:
            cmd_link_bam = ' '.join([
                'ln',
                '-s',
                config['input'][0],
                ' viromatch_results/prep_fastq_files/INPUT.bam'
            ])

            cmd_bam_to_fastq = ' '.join([
                'samtools',
                'fastq',
                '-N',
                '-1',
                'viromatch_results/prep_fastq_files/INPUT.r1.fastq',
                '-2',
                'viromatch_results/prep_fastq_files/INPUT.r2.fastq',
                config['input'][0]
            ])
            shell('echo "' + cmd_link_bam + '" > {output.cmd}')
            shell('echo "' + cmd_bam_to_fastq + '" >> {output.cmd}')
            shell(cmd_link_bam)
            shell(cmd_bam_to_fastq)


# :::::::::::::::::::::::::::::::::
#  T R I M   F A S T Q   F I L E S
# :::::::::::::::::::::::::::::::::

# Dependencies:
# + fqtrim

# The phred value may have been altered in the config file; update
# accordingly for fqtrim processing.

if int(config['phred']) == 33:
    phred = '-P33'
elif int(config['phred']) == 64:
    phred = '-P64'

# We use fqtrim to trim adaptor sequences, revise end quality, and filter
# out too-short reads.

rule trim_fastq_files:
    input:
        'viromatch_results/prep_fastq_files/INPUT.{pair}.fastq'
    output:
        fqtrim = temp('viromatch_results/trim_fastq_files/INPUT.{pair}.fqtrim.fastq'),
        fqreport = 'viromatch_results/trim_fastq_files/INPUT.{pair}.fqtrim.report.fastq',
        cmd = 'viromatch_results/trim_fastq_files/INPUT.{pair}.fqtrim.fastq.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.fqtrim.fastq.benchmark'
    run:
        cmd = ' '.join([
            'fqtrim',
            '-f', config['adaptor'],
            '-r {output.fqreport}',
            '-q', str(config['endqual']),
            '-l', str(config['readlen']),
            '-m', str(config['minn']),
            phred,
            '{input} > {output.fqtrim}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule blank_eval_filter_low_complexity:
    input:
        'viromatch_results/trim_fastq_files/INPUT.{pair}.fqtrim.fastq'
    output:
        check = 'viromatch_results/blank_eval_filter_low_complexity/INPUT.{pair}.fqtrim.fastq.blank.eval',
        cmd = 'viromatch_results/blank_eval_filter_low_complexity/INPUT.{pair}.fqtrim.fastq.blank.eval.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.fqtrim.fastq.blank.eval.benchmark'
    run:
        cmd = ' '.join([
            'blank_fastq_eval.py',
            '--fastq {input}',
            '--log {output.check}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#  F I L T E R   L O W   C O M P L E X I T Y  F A S T Q   F I L E S
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + vsearch

rule filter_low_complexity_fastq_files:
    input:
        fastq = 'viromatch_results/trim_fastq_files/INPUT.{pair}.fqtrim.fastq',
        log = 'viromatch_results/blank_eval_filter_low_complexity/INPUT.{pair}.fqtrim.fastq.blank.eval'
    output:
        fastq = temp('viromatch_results/filter_low_complexity_fastq_files/INPUT.{pair}.dusted.fastq'),
        cmd = 'viromatch_results/filter_low_complexity_fastq_files/INPUT.{pair}.dusted.fastq.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.dusted.fastq.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.dusted.fastq.benchmark'
    run:
        cmd = ' '.join([
            'vsearch',
            '--fastx_mask {input.fastq}',
            '--min_unmasked_pct', str(config['minn']),
            '--fastqout {output.fastq}',
            '--hardmask',
            '2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::
#  H O S T   S C R E E N   F A S T Q   R E A D S
# :::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + bwa
# + samtools

# We we align our prepared FASTQ files against a host reference genome and
# prepare the unmapped reads for downstream processing.

rule host_screen_mapping:
    input:
        'viromatch_results/filter_low_complexity_fastq_files/INPUT.{pair}.dusted.fastq'
    output:
        sam = temp('viromatch_results/host_screen_mapping/INPUT.{pair}.host.sam'),
        cmd = 'viromatch_results/host_screen_mapping/INPUT.{pair}.host.sam.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.host.sam.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.host.sam.benchmark'
    run:
        cmd = ' '.join([
            'bwa',
            'mem',
            config['host'],
            '{input} > {output.sam} 2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule host_screen_write_unmapped_bam:
    input:
        'viromatch_results/host_screen_mapping/INPUT.{pair}.host.sam'
    output:
        bam = 'viromatch_results/host_screen_write_unmapped_bam/INPUT.{pair}.host.unmapped.bam',
        cmd = 'viromatch_results/host_screen_write_unmapped_bam/INPUT.{pair}.host.unmapped.bam.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.host.unmapped.bam.benchmark'
    run:
        cmd = ' '.join([
            'samtools',
            'view',
            '-b {input}',
            '-f',
            '0x4',
            '-o {output.bam}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule host_screen_write_unmapped_fastq:
    input:
        'viromatch_results/host_screen_write_unmapped_bam/INPUT.{pair}.host.unmapped.bam'
    output:
        fastq = 'viromatch_results/host_screen_write_unmapped_fastq/INPUT.{pair}.host.unmapped.fastq',
        cmd = 'viromatch_results/host_screen_write_unmapped_fastq/INPUT.{pair}.host.unmapped.fastq.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.host.unmapped.fastq.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.host.unmapped.fastq.benchmark'
    run:
        cmd = ' '.join([
            'samtools',
            'fastq',
            '{input} > {output.fastq} 2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# __END__
