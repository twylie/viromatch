# VIROMATCH / Snakemake pipeline
# viromatch.smk
# T.N. Wylie  <twylie@wustl.edu>

import sys
import os

configfile: 'CONFIG.yaml'

nt_refs = dict()
for i, ref in enumerate(config['nt']):
    nt_refs.update({i: ref})

nr_refs = dict()
for i, ref in enumerate(config['nr']):
    nr_refs.update({i: ref})


# RULES:

# all
# prep_fastq_files
# trim_fastq_files
# blank_eval_filter_low_complexity
# filter_low_complexity_fastq_files
# host_screen_mapping
# host_screen_write_unmapped_bam
# host_screen_write_unmapped_fastq
# viral_nuc_mapping
# viral_nuc_write_unmapped_bam
# viral_nuc_write_unmapped_fastq
# viral_nuc_write_mapped_bam
# viral_nuc_write_mapped_fastq
# blank_eval_viral_trans_nuc
# viral_trans_nuc_mapping
# viral_trans_nuc_daa_to_tsv
# viral_trans_nuc_extract_mapped_ids
# viral_trans_nuc_write_mapped_fastq
# viral_mapped_fastq_merge
# validate_nuc_nt_mapping
# validate_nuc_nt_write_mapped_sam
# validate_nuc_nt_write_unmapped_sam
# validate_nuc_nt_merge_r1_mapped_sam
# validate_nuc_nt_merge_r2_mapped_sam
# validate_nuc_nt_write_r1_unmapped_ids
# validate_nuc_nt_write_r2_unmapped_ids
# validate_nuc_nt_write_merged_unmapped_fastq
# blank_eval_validate_trans_nuc_nr
# validate_trans_nuc_nr_mapping
# validate_trans_nuc_nr_mapping_daa_to_tsv
# validate_trans_nuc_nr_merge_r1_mapped_tsv
# validate_trans_nuc_nr_merge_r2_mapped_tsv
# nuc_nt_best_hit_filter_sam
# trans_nuc_nr_best_hit_filter_tsv
# nuc_nt_otherseq_hit_report
# nuc_nt_unknown_hit_report
# trans_nuc_nr_otherseq_hit_report
# trans_nuc_nr_unknown_hit_report
# nuc_nt_best_hit_count_prep
# trans_nuc_nr_best_hit_count_prep
# nuc_nt_best_hit_counts
# trans_nuc_nr_best_hit_counts
# copy_nuc_nt_report
# copy_trans_nuc_nr_report
# copy_nuc_ambiguous_report
# copy_trans_nuc_ambiguous_report


# :::::::
#  A L L
# :::::::

rule all:
    input:
        'REPORT.trans_nuc_counts.txt',
        'REPORT.nuc_counts.txt',
        'REPORT.nuc_ambiguous_counts.txt',
        'REPORT.trans_nuc_ambiguous_counts.txt',


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
        bam = temp('viromatch_results/host_screen_write_unmapped_bam/INPUT.{pair}.host.unmapped.bam'),
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
        fastq = temp('viromatch_results/host_screen_write_unmapped_fastq/INPUT.{pair}.host.unmapped.fastq'),
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


# :::::::::::::::::::::::::::::::::::
#  V I R A L   N U C   M A P P I N G
# :::::::::::::::::::::::::::::::::::

# Dependencies:
# + bwa
# + samtools
# + blank_fastq_eval.py

# We now will perform nuc-based mapping against our viral reference
# database, using the host-filtered FASTQ files from the previous step.

rule viral_nuc_mapping:
    input:
        'viromatch_results/host_screen_write_unmapped_fastq/INPUT.{pair}.host.unmapped.fastq'
    output:
        sam = temp('viromatch_results/viral_nuc_mapping/INPUT.{pair}.viral.sam'),
        cmd = 'viromatch_results/viral_nuc_mapping/INPUT.{pair}.viral.sam.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.viral.sam.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.sam.benchmark'
    run:
        cmd = ' '.join([
            'bwa',
            'mem',
            config['viralfna'],
            '{input} > {output.sam} 2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule viral_nuc_write_unmapped_bam:
    input:
        'viromatch_results/viral_nuc_mapping/INPUT.{pair}.viral.sam'
    output:
        bam = temp('viromatch_results/viral_nuc_write_unmapped_bam/INPUT.{pair}.viral.unmapped.bam'),
        cmd = 'viromatch_results/viral_nuc_write_unmapped_bam/INPUT.{pair}.viral.unmapped.bam.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.unmapped.bam.benchmark'
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

rule viral_nuc_write_unmapped_fastq:
    input:
        'viromatch_results/viral_nuc_write_unmapped_bam/INPUT.{pair}.viral.unmapped.bam'
    output:
        fastq = temp('viromatch_results/viral_nuc_write_unmapped_fastq/INPUT.{pair}.viral.unmapped.fastq'),
        cmd = 'viromatch_results/viral_nuc_write_unmapped_fastq/INPUT.{pair}.viral.unmapped.fastq.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.viral.unmapped.fastq.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.unmapped.fastq.benchmark'
    run:
        cmd = ' '.join([
            'samtools',
            'fastq',
            '{input} > {output.fastq} 2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule viral_nuc_write_mapped_bam:
    input:
        'viromatch_results/viral_nuc_mapping/INPUT.{pair}.viral.sam'
    output:
        bam = temp('viromatch_results/viral_nuc_write_mapped_bam/INPUT.{pair}.viral.mapped.bam'),
        cmd = 'viromatch_results/viral_nuc_write_mapped_bam/INPUT.{pair}.viral.mapped.bam.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.mapped.bam.benchmark'
    run:
        cmd = ' '.join([
            'samtools',
            'view',
            '-b {input}',
            '-F',
            '0X4',
            '-o {output.bam}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule viral_nuc_write_mapped_fastq:
    input:
        'viromatch_results/viral_nuc_write_mapped_bam/INPUT.{pair}.viral.mapped.bam'
    output:
        fastq = temp('viromatch_results/viral_nuc_write_mapped_fastq/INPUT.{pair}.viral.mapped.fastq'),
        cmd = 'viromatch_results/viral_nuc_write_mapped_fastq/INPUT.{pair}.viral.mapped.fastq.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.viral.mapped.fastq.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.mapped.fastq.benchmark'
    run:
        cmd = ' '.join([
            'samtools',
            'fastq',
            '{input} > {output.fastq} 2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


rule blank_eval_viral_trans_nuc:
    input:
        'viromatch_results/viral_nuc_write_unmapped_fastq/INPUT.{pair}.viral.unmapped.fastq'
    output:
        check = 'viromatch_results/blank_eval_viral_trans_nuc/INPUT.{pair}.viral.unmapped.fastq.blank.eval',
        cmd = 'viromatch_results/blank_eval_viral_trans_nuc/INPUT.{pair}.viral.unmapped.fastq.blank.eval.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.unmapped.fastq.blank.eval.benchmark'
    run:
        cmd = ' '.join([
            'blank_fastq_eval.py',
            '--fastq {input}',
            '--log {output.check}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::
#  V I R A L   T R A N S   N U C   M A P P I N G
# :::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + diamond
# + cut
# + sort
# + seqtk

# We now will perform translated nuc mapping against our viral reference
# database, using the unmapped FASTQ files from the previous nuc mapping
# step.

rule viral_trans_nuc_mapping:
    input:
        fastq = 'viromatch_results/viral_nuc_write_unmapped_fastq/INPUT.{pair}.viral.unmapped.fastq',
        log = 'viromatch_results/blank_eval_viral_trans_nuc/INPUT.{pair}.viral.unmapped.fastq.blank.eval'
    output:
        daa = temp('viromatch_results/viral_trans_nuc_mapping/INPUT.{pair}.viral.trans.daa'),
        cmd = 'viromatch_results/viral_trans_nuc_mapping/INPUT.{pair}.viral.trans.daa.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.viral.trans.daa.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.trans.daa.benchmark'
    run:
        cmd = ' '.join([
            'diamond',
            'blastx',
            '-d',
            config['viralfaa'],
            '-q {input.fastq}',
            '-a {output.daa}',
            '-t',
            'viromatch_results/viral_trans_nuc_mapping',
            '--max-target-seqs ' + str(config['mts']),
            '--evalue ' + str(config['evalue']),
            '2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule viral_trans_nuc_daa_to_tsv:
    input:
        'viromatch_results/viral_trans_nuc_mapping/INPUT.{pair}.viral.trans.daa'
    output:
        tsv = temp('viromatch_results/viral_trans_nuc_daa_to_tsv/INPUT.{pair}.viral.trans.daa.tsv'),
        cmd = 'viromatch_results/viral_trans_nuc_daa_to_tsv/INPUT.{pair}.viral.trans.daa.tsv.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.viral.trans.daa.tsv.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.trans.daa.tsv.benchmark'
    run:
        cmd = ' '.join([
            'diamond',
            'view',
            '-a {input}',
            '-o {output.tsv}',
            '-f',
            'tab',
            '2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule viral_trans_nuc_extract_mapped_ids:
    input:
        'viromatch_results/viral_trans_nuc_daa_to_tsv/INPUT.{pair}.viral.trans.daa.tsv'
    output:
        txt = temp('viromatch_results/viral_trans_nuc_extract_mapped_ids/INPUT.{pair}.viral.trans.daa.tsv.ids.txt'),
        cmd = 'viromatch_results/viral_trans_nuc_extract_mapped_ids/INPUT.{pair}.viral.trans.daa.tsv.ids.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.trans.daa.tsv.ids.txt.benchmark'
    run:
        cmd = ' '.join([
            'cut',
            '-f',
            '1 {input}',
            '|',
            'sort',
            '-u',
            '-S',
            str(config['bsize']) + 'G',
            '-T',
            'viromatch_results/viral_trans_nuc_extract_mapped_ids/',
            '> {output.txt}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule viral_trans_nuc_write_mapped_fastq:
    input:
        fastq = 'viromatch_results/viral_nuc_write_unmapped_fastq/INPUT.{pair}.viral.unmapped.fastq',
        ids = 'viromatch_results/viral_trans_nuc_extract_mapped_ids/INPUT.{pair}.viral.trans.daa.tsv.ids.txt'
    output:
        fastq = temp('viromatch_results/viral_trans_nuc_write_mapped_fastq/INPUT.{pair}.viral.trans.mapped.fastq'),
        cmd = 'viromatch_results/viral_trans_nuc_write_mapped_fastq/INPUT.{pair}.viral.trans.mapped.fastq.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.trans.mapped.fastq.benchmark'
    run:
        cmd = ' '.join([
            'seqtk',
            'subseq {input.fastq} {input.ids}',
            '> {output.fastq}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::
#  V I R A L   M A P P E D   F A S T Q   M E R G E
# :::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + cat

# For downstream validation steps, we will want the mapped reads from both
# nuc and translated nuc alignments merged into a single FASTQ file ---
# i.e. one FASTQ per read pair.

rule viral_mapped_fastq_merge:
    input:
        nuc = 'viromatch_results/viral_nuc_write_mapped_fastq/INPUT.{pair}.viral.mapped.fastq',
        transnuc = 'viromatch_results/viral_trans_nuc_write_mapped_fastq/INPUT.{pair}.viral.trans.mapped.fastq'
    output:
        fastq = temp('viromatch_results/viral_mapped_fastq_merge/INPUT.{pair}.viral.mapped.merged.fastq'),
        cmd = 'viromatch_results/viral_mapped_fastq_merge/INPUT.{pair}.viral.mapped.merged.fastq.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.mapped.merged.fastq.benchmark'
    run:
        cmd = 'cat {input.nuc} {input.transnuc} > {output.fastq}'
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::
#  V A L I D A T E   N U C   M A P P I N G
# :::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + bwa
# + samtools
# + seqtk
# + write_unmapped_fastq_ids.py

# Using the merged, mapped FASTQ files from the previous step, we will now
# iteratively map to all of the individual NCBI nt reference databases.

rule validate_nuc_nt_mapping:
    input:
        'viromatch_results/viral_mapped_fastq_merge/INPUT.{pair}.viral.mapped.merged.fastq'
    output:
        sam = temp('viromatch_results/validate_nuc_nt_mapping/INPUT.{pair}.validate.nuc.{nt}.sam'),
        cmd = 'viromatch_results/validate_nuc_nt_mapping/INPUT.{pair}.validate.nuc.{nt}.sam.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.validate.nuc.{nt}.sam.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.{nt}.sam.benchmark'
    run:
        cmd = ' '.join([
            'bwa',
            'mem',
            nt_refs[int(wildcards.nt)],
            '{input} > {output.sam} 2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_nuc_nt_write_mapped_sam:
    input:
        'viromatch_results/validate_nuc_nt_mapping/INPUT.{pair}.validate.nuc.{nt}.sam'
    output:
        sam = temp('viromatch_results/validate_nuc_nt_write_mapped_sam/INPUT.{pair}.validate.nuc.{nt}.mapped.sam'),
        cmd = 'viromatch_results/validate_nuc_nt_write_mapped_sam/INPUT.{pair}.validate.nuc.{nt}.mapped.sam.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.{nt}.mapped.sam.benchmark'
    run:
        cmd = ' '.join([
            'samtools',
            'view',
            '{input}',
            '-F',
            '0X4',
            '-o {output.sam}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_nuc_nt_write_unmapped_sam:
    input:
        'viromatch_results/validate_nuc_nt_mapping/INPUT.{pair}.validate.nuc.{nt}.sam'
    output:
        sam = temp('viromatch_results/validate_nuc_nt_write_unmapped_sam/INPUT.{pair}.validate.nuc.{nt}.unmapped.sam'),
        cmd = 'viromatch_results/validate_nuc_nt_write_unmapped_sam/INPUT.{pair}.validate.nuc.{nt}.unmapped.sam.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.{nt}.unmapped.sam.benchmark'
    run:
        cmd = ' '.join([
            'samtools',
            'view',
            '{input}',
            '-f',
            '0X4',
            '-o {output.sam}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_nuc_nt_merge_r1_mapped_sam:
    input:
        sam = expand(
            'viromatch_results/validate_nuc_nt_write_mapped_sam/INPUT.{pair}.validate.nuc.{nt}.mapped.sam',
            pair = 'r1',
            nt = nt_refs.keys()
        ),
    output:
        sam = temp('viromatch_results/validate_nuc_nt_merge_r1_mapped_sam/INPUT.{pair}.validate.nuc.mapped.merged.sam'),
        cmd = 'viromatch_results/validate_nuc_nt_merge_r1_mapped_sam/INPUT.{pair}.validate.nuc.mapped.merged.sam.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.mapped.merged.sam.benchmark'
    run:
        cmd = ' '.join([
            'sort',
            '-k',
            '1',
            '-S',
            str(config['bsize']) + 'G',
            '-T',
            'viromatch_results/validate_nuc_nt_merge_r1_mapped_sam/',
            '{input.sam} > {output.sam}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_nuc_nt_merge_r2_mapped_sam:
    input:
        sam = expand(
            'viromatch_results/validate_nuc_nt_write_mapped_sam/INPUT.{pair}.validate.nuc.{nt}.mapped.sam',
            pair = 'r2',
            nt = nt_refs.keys()
        ),
    output:
        sam = temp('viromatch_results/validate_nuc_nt_merge_r2_mapped_sam/INPUT.{pair}.validate.nuc.mapped.merged.sam'),
        cmd = 'viromatch_results/validate_nuc_nt_merge_r2_mapped_sam/INPUT.{pair}.validate.nuc.mapped.merged.sam.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.mapped.merged.sam.benchmark'
    run:
        cmd = ' '.join([
            'sort',
            '-k',
            '1',
            '-S',
            str(config['bsize']) + 'G',
            '-T',
            'viromatch_results/validate_nuc_nt_merge_r2_mapped_sam/',
            '{input.sam} > {output.sam}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_nuc_nt_write_r1_unmapped_ids:
    input:
        mapped = expand(
            'viromatch_results/validate_nuc_nt_write_mapped_sam/INPUT.{pair}.validate.nuc.{nt}.mapped.sam',
            pair = 'r1',
            nt = nt_refs.keys()
        ),
        unmapped = expand(
            'viromatch_results/validate_nuc_nt_write_unmapped_sam/INPUT.{pair}.validate.nuc.{nt}.unmapped.sam',
            pair = 'r1',
            nt = nt_refs.keys()
        )
    output:
        txt = temp('viromatch_results/validate_nuc_nt_write_r1_unmapped_ids/INPUT.{pair}.validate.nuc.unmapped.roi.ids.txt'),
        cmd = 'viromatch_results/validate_nuc_nt_write_r1_unmapped_ids/INPUT.{pair}.validate.nuc.unmapped.roi.ids.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.unmapped.roi.ids.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_unmapped_fastq_ids.py',
            '--mapsam {input.mapped}',
            '--unmapsam {input.unmapped}',
            '--out {output.txt}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_nuc_nt_write_r2_unmapped_ids:
    input:
        mapped = expand(
            'viromatch_results/validate_nuc_nt_write_mapped_sam/INPUT.{pair}.validate.nuc.{nt}.mapped.sam',
            pair = 'r2',
            nt = nt_refs.keys()
        ),
        unmapped = expand(
            'viromatch_results/validate_nuc_nt_write_unmapped_sam/INPUT.{pair}.validate.nuc.{nt}.unmapped.sam',
            pair = 'r2',
            nt = nt_refs.keys()
        )
    output:
        txt = temp('viromatch_results/validate_nuc_nt_write_r2_unmapped_ids/INPUT.{pair}.validate.nuc.unmapped.roi.ids.txt'),
        cmd = 'viromatch_results/validate_nuc_nt_write_r2_unmapped_ids/INPUT.{pair}.validate.nuc.unmapped.roi.ids.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.unmapped.roi.ids.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_unmapped_fastq_ids.py',
            '--mapsam {input.mapped}',
            '--unmapsam {input.unmapped}',
            '--out {output.txt}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


rule validate_nuc_nt_write_merged_unmapped_fastq:
    input:
        fastq = 'viromatch_results/viral_mapped_fastq_merge/INPUT.{pair}.viral.mapped.merged.fastq',
        ids = 'viromatch_results/validate_nuc_nt_write_{pair}_unmapped_ids/INPUT.{pair}.validate.nuc.unmapped.roi.ids.txt'
    output:
        fastq = temp('viromatch_results/validate_nuc_nt_write_merged_unmapped_fastq/INPUT.{pair}.viral.validate.merged.unmapped.fastq'),
        cmd = 'viromatch_results/validate_nuc_nt_write_merged_unmapped_fastq/INPUT.{pair}.viral.validate.merged.unmapped.fastq.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.validate.merged.unmapped.fastq.benchmark'
    run:
        cmd = ' '.join([
            'seqtk',
            'subseq {input.fastq} {input.ids}',
            '> {output.fastq}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


rule blank_eval_validate_trans_nuc_nr:
    input:
        'viromatch_results/validate_nuc_nt_write_merged_unmapped_fastq/INPUT.{pair}.viral.validate.merged.unmapped.fastq'
    output:
        check = 'viromatch_results/blank_eval_validate_trans_nuc_nr/INPUT.{pair}.viral.validate.merged.unmapped.fastq.blank.eval',
        cmd = 'viromatch_results/blank_eval_validate_trans_nuc_nr/INPUT.{pair}.viral.validate.merged.unmapped.fastq.blank.eval.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.viral.validate.merged.unmapped.fastq.blank.eval.benchmark'
    run:
        cmd = ' '.join([
            'blank_fastq_eval.py',
            '--fastq {input}',
            '--log {output.check}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::
#  V A L I D A T E   T R A N S   N U C   M A P P I N G
# :::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + diamond

# Using the merged, unmapped FASTQ files from the previous validation step,
# we will now iteratively map to all of the individual NCBI nr reference
# databases.

rule validate_trans_nuc_nr_mapping:
    input:
        fastq = 'viromatch_results/validate_nuc_nt_write_merged_unmapped_fastq/INPUT.{pair}.viral.validate.merged.unmapped.fastq',
        log = 'viromatch_results/blank_eval_validate_trans_nuc_nr/INPUT.{pair}.viral.validate.merged.unmapped.fastq.blank.eval'
    output:
        daa = temp('viromatch_results/validate_trans_nuc_nr_mapping/INPUT.{pair}.validate.trans.nuc.{nr}.daa'),
        cmd = 'viromatch_results/validate_trans_nuc_nr_mapping/INPUT.{pair}.validate.trans.nuc.{nr}.daa.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.validate.trans.nuc.{nr}.daa.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.trans.nuc.{nr}.daa.benchmark'
    run:
        cmd = ' '.join([
            'diamond',
            'blastx',
            '-d',
            nr_refs[int(wildcards.nr)],
            '-q {input.fastq}',
            '-a {output.daa}',
            '-t',
            'viromatch_results/validate_trans_nuc_nr_mapping',
            '--max-target-seqs ' + str(config['mts']),
            '--evalue ' + str(config['evalue']),
            '2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_trans_nuc_nr_mapping_daa_to_tsv:
    input:
        'viromatch_results/validate_trans_nuc_nr_mapping/INPUT.{pair}.validate.trans.nuc.{nr}.daa'
    output:
        tsv = temp('viromatch_results/validate_trans_nuc_nr_mapping_daa_to_tsv/INPUT.{pair}.validate.trans.nuc.{nr}.daa.tsv'),
        cmd ='viromatch_results/validate_trans_nuc_nr_mapping_daa_to_tsv/INPUT.{pair}.validate.trans.nuc.{nr}.daa.tsv.cmd'
    log:
        'viromatch_results/.viromatch/log/INPUT.{pair}.validate.trans.nuc.{nr}.daa.tsv.log'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.trans.nuc.{nr}.daa.benchmark'
    run:
        cmd = ' '.join([
            'diamond',
            'view',
            '-a {input}',
            '-o {output.tsv}',
            '-f',
            'tab',
            '2> {log}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_trans_nuc_nr_merge_r1_mapped_tsv:
    input:
        tsv = expand(
            'viromatch_results/validate_trans_nuc_nr_mapping_daa_to_tsv/INPUT.{pair}.validate.trans.nuc.{nr}.daa.tsv',
            pair = 'r1',
            nr = nr_refs.keys()
        ),
    output:
        tsv = 'viromatch_results/validate_trans_nuc_nr_merge_r1_mapped_tsv/INPUT.{pair}.validate.trans.nuc.mapped.merged.tsv',
        cmd = 'viromatch_results/validate_trans_nuc_nr_merge_r1_mapped_tsv/INPUT.{pair}.validate.trans.nuc.mapped.merged.tsv.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.trans.nuc.mapped.merged.tsv.benchmark'
    run:
        cmd = ' '.join([
            'sort',
            '-k',
            '1',
            '-S',
            str(config['bsize']) + 'G',
            '-T',
            'viromatch_results/validate_trans_nuc_nr_merge_r1_mapped_tsv/',
            '{input.tsv} > {output.tsv}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)

rule validate_trans_nuc_nr_merge_r2_mapped_tsv:
    input:
        tsv = expand(
            'viromatch_results/validate_trans_nuc_nr_mapping_daa_to_tsv/INPUT.{pair}.validate.trans.nuc.{nr}.daa.tsv',
            pair = 'r2',
            nr = nr_refs.keys()
        ),
    output:
        tsv = 'viromatch_results/validate_trans_nuc_nr_merge_r2_mapped_tsv/INPUT.{pair}.validate.trans.nuc.mapped.merged.tsv',
        cmd = 'viromatch_results/validate_trans_nuc_nr_merge_r2_mapped_tsv/INPUT.{pair}.validate.trans.nuc.mapped.merged.tsv.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.trans.nuc.mapped.merged.tsv.benchmark'
    run:
        cmd = ' '.join([
            'sort',
            '-k',
            '1',
            '-S',
            str(config['bsize']) + 'G',
            '-T',
            'viromatch_results/validate_trans_nuc_nr_merge_r2_mapped_tsv/',
            '{input.tsv} > {output.tsv}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::
#  N U C   N T   B E S T   H I T   F I L T E R   S A M
# :::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + best_hit_filter_sam.py

rule nuc_nt_best_hit_filter_sam:
    input:
        sam = 'viromatch_results/validate_nuc_nt_merge_{pair}_mapped_sam/INPUT.{pair}.validate.nuc.mapped.merged.sam'
    output:
        sam = temp('viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.{pair}.validate.nuc.mapped.filter.pass.sam'),
        cmd = 'viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.{pair}.validate.nuc.mapped.filter.pass.sam.cmd',
        log = temp('viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.{pair}.validate.nuc.mapped.filter.pass.sam.log'),
        unknown_log = temp('viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.{pair}.validate.nuc.mapped.filter.pass.sam.log.unknown'),
        otherseq_log = temp('viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.{pair}.validate.nuc.mapped.filter.pass.sam.log.otherseq')
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.nuc.mapped.filter.pass.sam.benchmark'
    run:
        cmd = ' '.join([
            'best_hit_filter_sam.py',
            '--sam {input.sam}',
            '--out {output.sam}',
            '--log {output.log}',
            '--unknown {output.unknown_log}',
            '--otherseq {output.otherseq_log}',
            '--taxid ' + config['taxid'],
            '--pid ' + str(config['pid']),
            '--pidprox ' + str(config['pidprox'])
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#  T R A N S   N U C   N R   B E S T   H I T   F I L T E R   T S V
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + best_hit_filter_tsv.py

rule trans_nuc_nr_best_hit_filter_tsv:
    input:
        tsv = 'viromatch_results/validate_trans_nuc_nr_merge_{pair}_mapped_tsv/INPUT.{pair}.validate.trans.nuc.mapped.merged.tsv'
    output:
        tsv = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.{pair}.validate.trans.nuc.mapped.filter.pass.tsv',
        cmd = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.{pair}.validate.trans.nuc.mapped.filter.pass.tsv.cmd',
        log = temp('viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.{pair}.validate.trans.nuc.mapped.filter.pass.tsv.log'),
        unknown_log = temp('viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.{pair}.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown'),
        otherseq_log = temp('viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.{pair}.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq')
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.{pair}.validate.trans.nuc.mapped.filter.pass.tsv.benchmark'
    run:
        cmd = ' '.join([
            'best_hit_filter_tsv.py',
            '--tsv {input.tsv}',
            '--out {output.tsv}',
            '--log {output.log}',
            '--unknown {output.unknown_log}',
            '--otherseq {output.otherseq_log}',
            '--taxid ' + config['taxid'],
            '--bitprox ' + str(config['bitprox']),
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::
#  N U C   N T   O T H E R S E Q   H I T   R E P O R T
# :::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + write_otherseq_report.py

rule nuc_nt_otherseq_hit_report:
    input:
        otherseq1 = 'viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r1.validate.nuc.mapped.filter.pass.sam.log.otherseq',
        otherseq2 = 'viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r2.validate.nuc.mapped.filter.pass.sam.log.otherseq'
    output:
        out = temp('viromatch_results/nuc_nt_otherseq_hit_report/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.otherseq.counts.txt'),
        cmd = 'viromatch_results/nuc_nt_otherseq_hit_report/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.otherseq.counts.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.otherseq.counts.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_otherseq_report.py',
            '--otherseq1 {input.otherseq1}',
            '--otherseq2 {input.otherseq2}',
            '--report {output.out}',
            '--mode nuc',
            '--sampleid ' + "'" + config['sampleid'] + "'",
            '--config ' + config['config']
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::
#  N U C   N T   U N K N O W N   H I T   R E P O R T
# :::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + write_unknown_report.py

rule nuc_nt_unknown_hit_report:
    input:
        unknown1 = 'viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r1.validate.nuc.mapped.filter.pass.sam.log.unknown',
        unknown2 = 'viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r2.validate.nuc.mapped.filter.pass.sam.log.unknown'
    output:
        out = temp('viromatch_results/nuc_nt_unknown_hit_report/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.unknown.counts.txt'),
        cmd = 'viromatch_results/nuc_nt_unknown_hit_report/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.unknown.counts.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.unknown.counts.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_unknown_report.py',
            '--unknown1 {input.unknown1}',
            '--unknown2 {input.unknown2}',
            '--report {output.out}',
            '--mode nuc',
            '--sampleid ' + "'" + config['sampleid'] + "'",
            '--config ' + config['config']            
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#  T R A N S   N U C   N T   O T H E R S E Q   H I T   R E P O R T
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + write_otherseq_report.py

rule trans_nuc_nr_otherseq_hit_report:
    input:
        otherseq1 = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r1.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq',
        otherseq2 = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r2.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq'
    output:
        out = temp('viromatch_results/trans_nuc_nr_otherseq_hit_report/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq.counts.txt'),
        cmd = 'viromatch_results/trans_nuc_nr_otherseq_hit_report/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq.counts.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq.counts.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_otherseq_report.py',
            '--otherseq1 {input.otherseq1}',
            '--otherseq2 {input.otherseq2}',
            '--report {output.out}',
            '--mode transnuc',
            '--sampleid ' + "'" + config['sampleid'] + "'",
            '--config ' + config['config'],
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#  T R A N S   N U C   N T   U N K N O W N   H I T   R E P O R T
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + write_unknown_report.py

rule trans_nuc_nr_unknown_hit_report:
    input:
        unknown1 = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r1.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown',
        unknown2 = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r2.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown'
    output:
        out = temp('viromatch_results/trans_nuc_nr_unknown_hit_report/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown.counts.txt'),
        cmd = 'viromatch_results/trans_nuc_nr_unknown_hit_report/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown.counts.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown.counts.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_unknown_report.py',
            '--unknown1 {input.unknown1}',
            '--unknown2 {input.unknown2}',
            '--report {output.out}',
            '--mode transnuc',
            '--sampleid ' + "'" + config['sampleid'] + "'",
            '--config ' + config['config']
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::
#  N U C   N T   B E S T   H I T   C O U N T   P R E P
# :::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + sam_taxonomy_count_prep.py

rule nuc_nt_best_hit_count_prep:
    input:
        sam1 = 'viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r1.validate.nuc.mapped.filter.pass.sam',
        sam2 = 'viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r2.validate.nuc.mapped.filter.pass.sam'
    output:
        tax = 'viromatch_results/nuc_nt_best_hit_count_prep/INPUT.merged.validate.nuc.mapped.filter.pass.tax',
        cmd = 'viromatch_results/nuc_nt_best_hit_count_prep/INPUT.merged.validate.nuc.mapped.filter.pass.tax.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.nuc.mapped.filter.pass.tax.benchmark'
    run:
        cmd = ' '.join([
            'sam_taxonomy_count_prep.py',
            '--sam1 {input.sam1}',
            '--sam2 {input.sam2}',
            '--out {output.tax}',
            '--taxid ' + config['taxid'],
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#  T R A N S   N U C   N R   B E S T   H I T   C O U N T   P R E P
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + tsv_taxonomy_count_prep.py

rule trans_nuc_nr_best_hit_count_prep:
    input:
       tsv1 = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r1.validate.trans.nuc.mapped.filter.pass.tsv',
       tsv2 = 'viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r2.validate.trans.nuc.mapped.filter.pass.tsv'
    output:
        tax = 'viromatch_results/trans_nuc_nr_best_hit_count_prep/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax',
        cmd = 'viromatch_results/trans_nuc_nr_best_hit_count_prep/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.benchmark'
    run:
        cmd = ' '.join([
            'tsv_taxonomy_count_prep.py',
            '--tsv1 {input.tsv1}',
            '--tsv2 {input.tsv2}',
            '--out {output.tax}',
            '--taxid ' + config['taxid'],
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::
#  N U C   N T   B E S T   H I T   C O U N T S
# :::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + write_count_report.py

rule nuc_nt_best_hit_counts:
    input:
        tax = 'viromatch_results/nuc_nt_best_hit_count_prep/INPUT.merged.validate.nuc.mapped.filter.pass.tax'
    output:
        counts = 'viromatch_results/nuc_nt_best_hit_counts/INPUT.merged.validate.nuc.mapped.filter.pass.tax.counts.txt',
        lineage = 'viromatch_results/nuc_nt_best_hit_counts/INPUT.merged.validate.nuc.mapped.filter.pass.tax.counts.lineage.tsv',
        genus = 'viromatch_results/nuc_nt_best_hit_counts/INPUT.merged.validate.nuc.mapped.filter.pass.tax.counts.genus.tsv',
        species = 'viromatch_results/nuc_nt_best_hit_counts/INPUT.merged.validate.nuc.mapped.filter.pass.tax.counts.species.tsv',
        cmd = 'viromatch_results/nuc_nt_best_hit_counts/INPUT.merged.validate.nuc.mapped.filter.pass.tax.counts.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.nuc.mapped.filter.pass.tax.counts.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_count_report.py',
            '--counts {input.tax}',
            '--mode nuc',
            '--report {output.counts}',
            '--lineage {output.lineage}',
            '--genus {output.genus}',
            '--species {output.species}',
            '--config ' + config['config'],
            '--sampleid ' + "'" + config['sampleid'] + "'"
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#  T R A N S   N U C   N R   B E S T   H I T   C O U N T S
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + write_count_report.py

rule trans_nuc_nr_best_hit_counts:
    input:
        tax = 'viromatch_results/trans_nuc_nr_best_hit_count_prep/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax'
    output:
        counts = 'viromatch_results/trans_nuc_nr_best_hit_counts/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.counts.txt',
        lineage = 'viromatch_results/trans_nuc_nr_best_hit_counts/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.counts.lineage.tsv',
        genus = 'viromatch_results/trans_nuc_nr_best_hit_counts/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.counts.genus.tsv',
        species = 'viromatch_results/trans_nuc_nr_best_hit_counts/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.counts.species.tsv',
        cmd = 'viromatch_results/trans_nuc_nr_best_hit_counts/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.counts.txt.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.counts.txt.benchmark'
    run:
        cmd = ' '.join([
            'write_count_report.py',
            '--counts {input.tax}',
            '--mode transnuc',
            '--report {output.counts}',
            '--lineage {output.lineage}',
            '--genus {output.genus}',
            '--species {output.species}',
            '--config ' + config['config'],
            '--sampleid ' + "'" + config['sampleid'] + "'"
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::
#  C O P Y   N U C   N T   R E P O R T
# :::::::::::::::::::::::::::::::::::::

# Dependencies:
# + cp

rule copy_nuc_nt_report:
    input:
        'viromatch_results/nuc_nt_best_hit_counts/INPUT.merged.validate.nuc.mapped.filter.pass.tax.counts.txt'
    output:
        nuc_nt_report = 'REPORT.nuc_counts.txt',
        cmd = 'viromatch_results/copy_nuc_nt_report/nuc_nt_copy_report.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/nuc_nt_copy_report.benchmark'
    run:
        cmd = ' '.join([
            'cp',
            '{input}',
            '{output.nuc_nt_report}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::
#  C O P Y   T R A N S   N U C   N T   R E P O R T
# :::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + cp

rule copy_trans_nuc_nr_report:
    input:
        'viromatch_results/trans_nuc_nr_best_hit_counts/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tax.counts.txt'
    output:
        trans_nuc_nr_report = 'REPORT.trans_nuc_counts.txt',
        cmd = 'viromatch_results/copy_trans_nuc_nr_report/trans_nuc_nr_copy_report.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/trans_nuc_nr_copy_report.benchmark'
    run:
        cmd = ' '.join([
            'cp',
            '{input}',
            '{output.trans_nuc_nr_report}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::
#  C O P Y   N U C   A M B I G U O U S   R E P O R T
# :::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + cat

rule copy_nuc_ambiguous_report:
    input:
        otherseq = 'viromatch_results/nuc_nt_otherseq_hit_report/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.otherseq.counts.txt',
        unknown = 'viromatch_results/nuc_nt_unknown_hit_report/INPUT.merged.validate.nuc.mapped.filter.pass.sam.log.unknown.counts.txt'
    output:
        nuc_ambiguous_report = 'REPORT.nuc_ambiguous_counts.txt',
        cmd = 'viromatch_results/copy_nuc_ambiguous_report/copy_nuc_ambiguous_report.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/copy_nuc_ambiguous_report.benchmark'
    run:
        cmd = ' '.join([
            'cat',
            '{input.otherseq}',
            '{input.unknown}',
            '>',
            '{output.nuc_ambiguous_report}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#  C O P Y   T R A N S   N U C   A M B I G U O U S   R E P O R T
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Dependencies:
# + cat

rule copy_trans_nuc_ambiguous_report:
    input:
        otherseq = 'viromatch_results/trans_nuc_nr_otherseq_hit_report/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq.counts.txt',
        unknown = 'viromatch_results/trans_nuc_nr_unknown_hit_report/INPUT.merged.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown.counts.txt'
    output:
        trans_nuc_ambiguous_report = 'REPORT.trans_nuc_ambiguous_counts.txt',
        cmd = 'viromatch_results/copy_trans_nuc_ambiguous_report/copy_trans_nuc_ambiguous_report.cmd'
    benchmark:
        'viromatch_results/.viromatch/benchmark/copy_trans_nuc_ambiguous_report.benchmark'
    run:
        cmd = ' '.join([
            'cat',
            '{input.otherseq}',
            '{input.unknown}',
            '>',
            '{output.trans_nuc_ambiguous_report}'
        ])
        shell('echo "' + cmd + '" > {output.cmd}')
        shell(cmd)


# __END__
