---
title: "Interactive Docker"
date: 2020-11-10T23:45:36-06:00
draft: false
weight: 2
---

## Interactive Docker Sessions

Docker will allow a user to enter an interactive session (shell) when running a container. In such a scenario, we first enter an interactive instance of the ViroMatch pipeline and _then_ execute our ViroMatch command. This approach can be very useful for interacting directly with the ViroMatch code base, running sub-commands manually, or troubleshooting. When running the pipeline using this method, we see standard output on the screen in real time. Since the session (and window) must remain open throughout pipeline processing, this method is not the best choice for long running jobs or if one is wanting to submit the job within a cluster (instead, see [Command Line Docker](https://twylie.github.io/viromatch/execution/cli_docker/)).

### Starting an Interactive Docker Session

Let's take a look at the command to get an interactive session and then we'll breakdown what is going on.

{{% notice tip %}}
For the command below, the `\` character at the end of each line is used to wrap the command for readability. You may also run the command below in your terminal as a single line sans `\` characters.
{{% /notice %}}

```bash
docker \
container run \
-it \
-v devViroMatchSMK/t/data:/data \
-v /tmp/myTest:/outdir \
-v devViroMatchSMK/t/ncbi/nt:/nt \
-v devViroMatchSMK/t/ncbi/nr:/nr \
-v devViroMatchSMK/t/viral/viralfna:/viralfna \
-v devViroMatchSMK/t/viral/viralfaa:/viralfaa \
-v devViroMatchSMK/t/host:/host \
-v devViroMatchSMK/t/adaptor:/adaptor \
-v devViroMatchSMK/t/taxonomy:/taxonomy \
twylie/viromatch:latest \
zsh
```

_Command Breakdown_

The `docker container run` invocation tells Docker that we are going to be running a container based on an image that is registered (has been pulled) and available on your system. The `-it` switch tells Docker that this will be an interactive session and we will be viewing standard output. All of the lines with a preceding `-v` are telling Docker that you are mapping volumes (disks). For example, in the above example, the local `/tmp/myTest` directory is accessible within the Docker container as `/outdir` directory. We map all of the directories we need in this manner. The `twylie/viromatch:latest` call tells Docker to use the ViroMatch image tagged _latest_ for the session. Finally, `zsh` runs a shell for our interactive session.

### Executing ViroMatch 

Running the above command drops us into an interactive Docker session with all of the ViroMatch code base at our disposal. We can now run the ViroMatch pipeline from the command line. A typical ViroMatch command would look like the following.

```bash
viromatch \
--sampleid 'Sample 1' \
--input /data/test.r1.fastq /data/test.r2.fastq \
--outdir /outdir/myTest \
--nt /nt/nt.fofn \
--nr /nr/nr.fofn \
--viralfna /viralfna/viral_genomes.fasta \
--viralfaa /viralfaa/viral_genomes.dmnd \
--host /host/human.fna \
--adaptor /adaptor/adaptor.fqtrim \
--taxid /taxonomy/taxonomy.tsv \
--keep
```

_Command Breakdown_

We call ViroMatch from the command line and pass required arguments (see [Command Line Options](https://twylie.github.io/viromatch/execution/cli_args/#command-line-options)) for running the pipeline. The `--sampleid` argument takes a text string which is used to label the sample during processing. The `--input` argument can take either a uBAM (unmapped BAM) file as input or, as shown here, paired FASTQ files. The `--outdir` path is where pipeline output will be written. The `--nt` and `--nr` arguments point to the paths for the split NCBI nt/nr reference sequence databases, here passed as file-of-filenames (see [Required Arguments](https://twylie.github.io/viromatch/execution/cli_args/#required-arguments)). Both `--viralfna` and `--viralfaa` point to viral-only databases, nucleotide and translated nucleotide respectively. For host screening, we provide `--host` with the human reference genome. The `--adaptor` argument provides the adaptor file used during adaptor trimming. The `--taxid` argument points to the taxonomy databases used for classifying reads. Finally, `--keep` is a switch that tells the pipeline to "keep" the temporary files generated during processing that would be otherwise deleted by default.

Note in the above command that we are pointing to directories that were originally mapped using Docker's `-v` argument when we initialized our interactive session. For example, when we ran the Docker command, we used:

`devViroMatchSMK/t/data:/data`

to map the local directory where our FASTQ files reside to a directory within the container instance called `/data`. Thus, when telling ViroMatch to look for `--input` we pointed to the `/data` directory path on the container side.

{{% notice warning %}}
Most errors encountered when running the pipeline stem from malformed volume mappings when executing the docker container run command. Make sure you are exact when providing volume mappings and use fully qualified paths to be explicit.
{{% /notice %}}

### ViroMatch Standard Output

After running the above commands, standard output from the pipeline begins to be displayed to the screen, describing pipeline progress. Here is a generic example, truncated for brevity.

```plaintext
Building DAG of jobs...
Using shell: /bin/bash
Provided cluster nodes: 150
Job counts:
	count	jobs
	1	all
	2	blank_eval_filter_low_complexity
	2	blank_eval_validate_trans_nuc_nr
	2	blank_eval_viral_trans_nuc
	1	copy_nuc_ambiguous_report
	1	copy_nuc_nt_report
	1	copy_trans_nuc_ambiguous_report
	1	copy_trans_nuc_nr_report
	2	filter_low_complexity_fastq_files
	2	host_screen_mapping
	2	host_screen_write_unmapped_bam
	2	host_screen_write_unmapped_fastq
	1	nuc_nt_best_hit_count_prep
	1	nuc_nt_best_hit_counts
	2	nuc_nt_best_hit_filter_sam
	1	nuc_nt_otherseq_hit_report
	1	nuc_nt_unknown_hit_report
	1	prep_fastq_files
	1	trans_nuc_nr_best_hit_count_prep
	1	trans_nuc_nr_best_hit_counts
	2	trans_nuc_nr_best_hit_filter_tsv
	1	trans_nuc_nr_otherseq_hit_report
	1	trans_nuc_nr_unknown_hit_report
	2	trim_fastq_files
	148	validate_nuc_nt_mapping
	1	validate_nuc_nt_merge_r1_mapped_sam
	1	validate_nuc_nt_merge_r2_mapped_sam
	148	validate_nuc_nt_write_mapped_sam
	2	validate_nuc_nt_write_merged_unmapped_fastq
	1	validate_nuc_nt_write_r1_unmapped_ids
	1	validate_nuc_nt_write_r2_unmapped_ids
	148	validate_nuc_nt_write_unmapped_sam
	80	validate_trans_nuc_nr_mapping
	80	validate_trans_nuc_nr_mapping_daa_to_tsv
	1	validate_trans_nuc_nr_merge_r1_mapped_tsv
	1	validate_trans_nuc_nr_merge_r2_mapped_tsv
	2	viral_mapped_fastq_merge
	2	viral_nuc_mapping
	2	viral_nuc_write_mapped_bam
	2	viral_nuc_write_mapped_fastq
	2	viral_nuc_write_unmapped_bam
	2	viral_nuc_write_unmapped_fastq
	2	viral_trans_nuc_daa_to_tsv
	2	viral_trans_nuc_extract_mapped_ids
	2	viral_trans_nuc_mapping
	2	viral_trans_nuc_write_mapped_fastq
	666

[Fri Oct 30 19:42:16 2020]
rule prep_fastq_files:
    input: /storage1/fs1/kwylie/Archive/2020_09_21_AHA_RAW_DATA_ONLY/RAW_DATA/gerald_HG3LNDSXY_4_GGTTGGAC-TACAGGAT.bam
    output: viromatch_results/prep_fastq_files/INPUT.r1.fastq, viromatch_results/prep_fastq_files/INPUT.r2.fastq, viromatch_results/prep_fastq_files/INPUT.cmd
    jobid: 665
    benchmark: viromatch_results/.viromatch/benchmark/INPUT.fastq.benchmark

Submitted job 665 with external jobid 'Job <207713> is submitted to queue <general>.'.
[Fri Oct 30 19:42:46 2020]
Finished job 665.
1 of 666 steps (0.15%) done

[Fri Oct 30 19:42:46 2020]
rule trim_fastq_files:
    input: viromatch_results/prep_fastq_files/INPUT.r1.fastq
    output: viromatch_results/trim_fastq_files/INPUT.r1.fqtrim.fastq, viromatch_results/trim_fastq_files/INPUT.r1.fqtrim.report.fastq, viromatch_results/trim_fastq_files/INPUT.r1.fqtrim.fastq.cmd
    jobid: 661
    benchmark: viromatch_results/.viromatch/benchmark/INPUT.r1.fqtrim.fastq.benchmark
    wildcards: pair=r1

...

```

For a detailed explanation of all command line arguments for ViroMatch, see [Command Line Docker](https://twylie.github.io/viromatch/execution/cli_docker/).
