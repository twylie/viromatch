---
title: "Snakemake"
date: 2020-11-13T13:37:01-06:00
draft: false
weight: 2
---

## The Snakemake Pipeline

The ViroMatch pipeline uses [Snakemake](https://snakemake.readthedocs.io/en/stable/) to organize and run its steps.

_What is Snakemake?_

>The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language. They can be seamlessly scaled to server, cluster, grid and cloud environments, without the need to modify the workflow definition. Finally, Snakemake workflows can entail a description of required software, which will be automatically deployed to any execution environment. (Source: [Snakemake](https://snakemake.readthedocs.io/en/stable/))

>[Köster, Johannes and Rahmann, Sven. "Snakemake - A scalable bioinformatics workflow engine". Bioinformatics 2012.](https://bioinformatics.oxfordjournals.org/content/28/19/2520)

All of the steps (_rules_ in Snakemake terminology) in the pipeline are defined and run by Snakemake under-the-hood. That is, you will not have to write Snakemake code or run Snakemake directly; ViroMatch does all of that for you automatically based on the input parameters supplied to the `viromatch` command. 

When ViroMatch is run, the following Snakemake specific files are auto-generated in the `--output` directory.

```plaintext
cmd.sh
CONFIG.yaml
Snakefile
```

These files are the core input required to automatically run a Snakemake instance of the ViroMatch pipeline.

### cmd.sh

The `cmd.sh` file contains the shell commands that ViroMatch runs to automatically launch the Snakemake pipeline. You don't have to run this code manually since ViroMatch runs everything for you. However, if you launched ViroMatch using the `--dryrun` argument, executing this script will manually run the pipeline.

### CONFIG.yaml

The `CONFIG.yaml` file stores all of the parameters required to run the ViroMatch pipeline. The parameters passed to the `viromatch` command from the command line are stored here. Other internal variables for running the pipeline are also stored here. This is the configuration file used by Snakemake when running the pipeline. You should not directly edit the configuration file.

### Snakefile

The `Snakefile` is technically _the pipeline_ in terms of code that defines and executes all of the steps in a specific order. This file (along with the configuration file) are used by Snakemake to execute the pipeline. Please note that the Snakefile contains calls to other third-party executables --- e.g. BWA, Samtools, Diamond, etc. Also, ViroMatch specific code is also called in this manner. The Snakefile is essentially the _recipe_ or protocol for the ViroMatch pipeline.

Here is a list of all of the steps/rules in the Snakefile, ordered by occurrence. See [Steps (Snakemake Rules)](https://twylie.github.io/viromatch/overview/steps/#steps-snakemake-rules) for a detailed breakdown of all steps and their purpose.

+ prep_fastq_files
+ trim_fastq_files
+ blank_eval_filter_low_complexity
+ filter_low_complexity_fastq_files
+ host_screen_mapping
+ host_screen_write_unmapped_bam
+ host_screen_write_unmapped_fastq
+ viral_nuc_mapping
+ viral_nuc_write_unmapped_bam
+ viral_nuc_write_unmapped_fastq
+ viral_nuc_write_mapped_bam
+ viral_nuc_write_mapped_fastq
+ blank_eval_viral_trans_nuc
+ viral_trans_nuc_mapping
+ viral_trans_nuc_daa_to_tsv
+ viral_trans_nuc_extract_mapped_ids
+ viral_trans_nuc_write_mapped_fastq
+ viral_mapped_fastq_merge
+ validate_nuc_nt_mapping
+ validate_nuc_nt_write_mapped_sam
+ validate_nuc_nt_write_unmapped_sam
+ validate_nuc_nt_merge_r1_mapped_sam
+ validate_nuc_nt_merge_r2_mapped_sam
+ validate_nuc_nt_write_r1_unmapped_ids
+ validate_nuc_nt_write_r2_unmapped_ids
+ validate_nuc_nt_write_merged_unmapped_fastq
+ blank_eval_validate_trans_nuc_nr
+ validate_trans_nuc_nr_mapping
+ validate_trans_nuc_nr_mapping_daa_to_tsv
+ validate_trans_nuc_nr_merge_r1_mapped_tsv
+ validate_trans_nuc_nr_merge_r2_mapped_tsv
+ nuc_nt_best_hit_filter_sam
+ trans_nuc_nr_best_hit_filter_tsv
+ nuc_nt_otherseq_hit_report
+ nuc_nt_unknown_hit_report
+ trans_nuc_nr_otherseq_hit_report
+ trans_nuc_nr_unknown_hit_report
+ nuc_nt_best_hit_count_prep
+ trans_nuc_nr_best_hit_count_prep
+ nuc_nt_best_hit_counts
+ trans_nuc_nr_best_hit_counts
+ copy_nuc_nt_report
+ copy_trans_nuc_nr_report
+ copy_nuc_ambiguous_report
+ copy_trans_nuc_ambiguous_report
