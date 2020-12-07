---
title: "Reports and Output Files"
date: 2020-11-11T14:26:29-06:00
draft: false
weight: 7
---

## Top-Level Structure

When the ViroMatch pipeline finishes, all output will be in the directory specified by the `--output` argument. Contents of this area will look like the following.

```plaintext
CONFIG.yaml
REPORT.nuc_ambiguous_counts.txt
REPORT.nuc_counts.txt
REPORT.trans_nuc_ambiguous_counts.txt
REPORT.trans_nuc_counts.txt
Snakefile
cmd.sh
stats.log
steps.txt
viromatch_results/
```

Here is a breakdown of this area.

| File/Directory                          | Description                                                                                                                                                                                           |
| :-------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------               |
| .snakemake                              | This directory contains information written by Snakemake during its execution.                                                                                                                        |
| CONFIG.yaml                             | This file contains all of the configuration information required to run ViroMatch and is used directly by Snakmake to execute the pipeline. Command line parameters are captured here.                |
| REPORT.nuc_ambiguous_counts.txt         | Final virus read counts and taxonomy based on nucleotide reference mappings. [See below for detailed explanation.](https://twylie.github.io/viromatch/overview/reports/#ambiguous-counts)             |
| REPORT.nuc_counts.txt                   | Final virus read counts and taxonomy based on translated nucleotide reference mappings. [See below for detailed explanation.](https://twylie.github.io/viromatch/overview/reports/#nucleotide-counts) |
| REPORT.trans_nuc_ambiguous_counts.txt   | Rejected hits/taxonomy based on nucleotide reference mappings. [See below for detailed explanation](https://twylie.github.io/viromatch/overview/reports/#ambiguous-counts)                            |
| REPORT.trans_nuc_counts.txt             | Rejected hits/taxonomy based on translated nucleotide reference mappings. [See below for detailed explanation.](https://twylie.github.io/viromatch/overview/reports/#translated-nucleotide-counts)    |
| Snakefile                               | The Snakemake file that executes the steps in the ViroMatch pipeline. Can also be executed using Snakemake directly.                                                                                  |
| cmd.sh                                  | The shell script that ViroMatch uses to automatically execute the Snakemake pipeline.                                                                                                                 |
| stats.log                               | Upon completion of the pipeline, Snakemake will write a benchmark file outlining runtime per pipeline step.                                                                                           |
| steps.txt                               | The rules (steps) in the pipeline, as executed by Snakemake.                                                                                                                                          |
| viromatch_results/                      | This directory contains all of the ancillary directories and files ViroMatch writes during pipeline processing.                                                                                       |

## The viromatch_results/ Directory

This directory contains all of the ancillary directories and files ViroMatch writes during pipeline processing. Each rule (step) in the pipeline will have its own directory written here. The directory structure of a successful run will looks as follows.

```plaintext
viromatch_results/.viromatch/
viromatch_results/blank_eval_filter_low_complexity/
viromatch_results/blank_eval_validate_trans_nuc_nr/
viromatch_results/blank_eval_viral_trans_nuc/
viromatch_results/copy_nuc_ambiguous_report/
viromatch_results/copy_nuc_nt_report/
viromatch_results/copy_trans_nuc_ambiguous_report/
viromatch_results/copy_trans_nuc_nr_report/
viromatch_results/filter_low_complexity_fastq_files/
viromatch_results/host_screen_mapping/
viromatch_results/host_screen_write_unmapped_bam/
viromatch_results/host_screen_write_unmapped_fastq/
viromatch_results/nuc_nt_best_hit_count_prep/
viromatch_results/nuc_nt_best_hit_counts/
viromatch_results/nuc_nt_best_hit_filter_sam/
viromatch_results/nuc_nt_otherseq_hit_report/
viromatch_results/nuc_nt_unknown_hit_report/
viromatch_results/prep_fastq_files/
viromatch_results/trans_nuc_nr_best_hit_count_prep/
viromatch_results/trans_nuc_nr_best_hit_counts/
viromatch_results/trans_nuc_nr_best_hit_filter_tsv/
viromatch_results/trans_nuc_nr_otherseq_hit_report/
viromatch_results/trans_nuc_nr_unknown_hit_report/
viromatch_results/trim_fastq_files/
viromatch_results/validate_nuc_nt_mapping/
viromatch_results/validate_nuc_nt_merge_r1_mapped_sam/
viromatch_results/validate_nuc_nt_merge_r2_mapped_sam/
viromatch_results/validate_nuc_nt_write_mapped_sam/
viromatch_results/validate_nuc_nt_write_merged_unmapped_fastq/
viromatch_results/validate_nuc_nt_write_r1_unmapped_ids/
viromatch_results/validate_nuc_nt_write_r2_unmapped_ids/
viromatch_results/validate_nuc_nt_write_unmapped_sam/
viromatch_results/validate_trans_nuc_nr_mapping/
viromatch_results/validate_trans_nuc_nr_mapping_daa_to_tsv/
viromatch_results/validate_trans_nuc_nr_merge_r1_mapped_tsv/
viromatch_results/validate_trans_nuc_nr_merge_r2_mapped_tsv/
viromatch_results/viral_mapped_fastq_merge/
viromatch_results/viral_nuc_mapping/
viromatch_results/viral_nuc_write_mapped_bam/
viromatch_results/viral_nuc_write_mapped_fastq/
viromatch_results/viral_nuc_write_unmapped_bam/
viromatch_results/viral_nuc_write_unmapped_fastq/
viromatch_results/viral_trans_nuc_daa_to_tsv/
viromatch_results/viral_trans_nuc_extract_mapped_ids/
viromatch_results/viral_trans_nuc_mapping/
viromatch_results/viral_trans_nuc_write_mapped_fastq/
```

{{% notice tip %}}
ViroMatch writes several internal files in the `.viromatch` directory during processing. Information collected here includes benchmark files for individual steps and log files for steps that run executables that generate their own output.
{{% /notice %}}

As ViroMatch progresses through pipeline execution, each step will create an underlying directory based on the step's name and processing specific to the step will occur in this area. For example, if we wanted to see the exact commands related to the `viral_nuc_mapping` step, we would look in the `viromatch_results/viral_nuc_mapping/` directory.

```plaintext
viromatch_results/viral_nuc_mapping/INPUT.r1.viral.sam.cmd
viromatch_results/viral_nuc_mapping/INPUT.r2.viral.sam.cmd
```

There are two shell scripts, one for R1 reads and another for R2 reads, that run the specific commands to align FASTQ to the viral nucleotide reference database using BWA-MEM.

```bash
cat viromatch_results/viral_nuc_mapping/INPUT.r1.viral.sam.cmd
```

Results:

```plaintext
bwa mem /viralfna/2014_12_29_complete_viral_genomes.fasta viromatch_results/host_screen_write_unmapped_fastq/INPUT.r1.host.unmapped.fastq > viromatch_results/viral_nuc_mapping/INPUT.r1.viral.sam 2> viromatch_results/.viromatch/log/INPUT.r1.viral.sam.log
```

```bash
cat viromatch_results/viral_nuc_mapping/INPUT.r2.viral.sam.cmd
```

Results:

```plaintext
bwa mem /viralfna/2014_12_29_complete_viral_genomes.fasta viromatch_results/host_screen_write_unmapped_fastq/INPUT.r2.host.unmapped.fastq > viromatch_results/viral_nuc_mapping/INPUT.r2.viral.sam 2> viromatch_results/.viromatch/log/INPUT.r2.viral.sam.log
```

All ViroMatch processing is done by Snakemake executing individual shell scripts along the pipeline. Therefore, it is relatively easy to see exactly what commands are being run throughout the pipeline. Once a run is finished, you can list all of the underlying shell scripts with the following command.

```bash
find viromatch_results/* -type f | grep '.cmd$'
```

To see the order of execution for the shell commands, you will just need to look at the Snakemake log files that were generated during pipeline execution.

```bash
ls .snakemake/log/*
```

```plaintext
.snakemake/log/2020-10-27T183639.808528.snakemake.log
.snakemake/log/2020-10-27T183640.109481.snakemake.log
```

One of the logs simply lists the rules/steps in the pipeline in order of execution defined by Snakemake, the other log is written during actual pipeline line execution. You will see the order of execution here for each rule, the associated directory being writte under `viromatch_results/`, input and output files for the rule, and the specific shell script being used for execution.

## Sanity Files

{{% notice warning %}}
By default, ViroMatch removes temporary files generated during execution when they are no longer needed for downstream processing. This is done to save disk space, as many of the temporary files can be large in size. Therefore, not all of the files generated during processing will be under `viromatch_results/` unless the user specifies the `--keep` argument when executing the pipeline.
{{% /notice %}}

Using the `--keep` switch when executing the pipeline retains _all_ of the files generated during processing. There are several useful "sanity" files that are generated within the pipeline , but be warned they can be very large in size!

While retaining all of the pipeline files provides additional information for every command executed in the pipeline, some files are more important than others in reviewing pipeline decisions. Of particular interest are the pass/fail sanity files. These files provide the pass/fail status for every read evaluated in the pipeline, including the reason why a read might fail. While the read count report files provide viral hit/taxonomy counts, the pass/fail sanity files provide information on why or why not a read was counted.

The pass/fail sanity files are located here.

```plaintext
viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r1.validate.nuc.mapped.filter.pass.sam.log
viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r1.validate.nuc.mapped.filter.pass.sam.log.unknown
viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r1.validate.nuc.mapped.filter.pass.sam.log.otherseq

viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r2.validate.nuc.mapped.filter.pass.sam.log
viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r2.validate.nuc.mapped.filter.pass.sam.log.unknown
viromatch_results/nuc_nt_best_hit_filter_sam/INPUT.r2.validate.nuc.mapped.filter.pass.sam.log.otherseq

viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r1.validate.trans.nuc.mapped.filter.pass.tsv.log
viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r1.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown
viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r1.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq

viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r2.validate.trans.nuc.mapped.filter.pass.tsv.log
viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r2.validate.trans.nuc.mapped.filter.pass.tsv.log.unknown
viromatch_results/trans_nuc_nr_best_hit_filter_tsv/INPUT.r2.validate.trans.nuc.mapped.filter.pass.tsv.log.otherseq
```

There are sanity files for both nucleotide mapping and translated nucleotide mapping, both broken down into R1 and R2 reads.

The `*.unknown` and `*.otherseq` sanity files partition ambiguous hits that have been removed from consideration. See [Ambiguous Counts](https://twylie.github.io/viromatch/overview/reports/#ambiguous-counts) for more details.

### Sanity Examples

Using `INPUT.r1.validate.nuc.mapped.filter.pass.sam.log` as an example, the associated fields in the file are as follows.

| Field           | Description                                                                               |
|:---------------:|-------------------------------------------------------------------------------------------|
| pass/fail       | Pass/fail status for the hit. If passed, the read/hit was counted as a viral identity.    |
| code            | Discrete pass/fail code, associated with the best hit logic in the pipeline.              |
| read block size | How many hits per read were considered for the read.                                      |
| read id         | Associated sequence id for the read (from uBAM or FASTQ files).                           |
| comment         | Comment related to the pass/fail status.                                                  |
| pid             | Percent identity variance of the read (query) as compared to the reference hit (subject). |
| acc id          | Accession id of the reference hit.                                                        |
| species         | Species of the reference hit.                                                             |
| lineage         | Full lineage of the reference hit.                                                        |

An example of a single failed hit.

| Field            | Description                                                                              |
| :---------------:| ---------------------------------------------------------------------------------------- |
| pass/fail        | FAIL                                                                                     |
| code             | TIED BEST HIT                                                                            |
| read block size  | 2                                                                                        |
| read id          | D00170:57:CA2R8ANXX:4:2315:8200:2670                                                     |
| comment          | failed best hit (tied)                                                                   |
| pid              | 0.0397                                                                                   |
| acc id           | KF294862.1                                                                               |
| species          | Gyrovirus Tu789                                                                          |
| lineage          | Viruses --> Anelloviridae --> Gyrovirus --> unclassified Gyrovirus --> Gyrovirus Tu789   |

In the above example, the sequence read `D00170:57:CA2R8ANXX:4:2315:8200:2670` had a hit to the `KF294862.1` reference genome (Gyrovirus Tu789) with 3.97% variance. While this is an acceptable hit --- e.g. hits a known virus with acceptable percent identity --- there are 2 hits associated with this read. The other hit also was equally acceptable. In such cases, when hits are equivalent, the pipeline randomly chooses the best hit. As indicated, this hit was (randomly) failed and the other hit was the best hit for the read.

Let's look at a more complicated example. Here is a read block (i.e. all the hits being evaluated for a single read).

| Pass/Fail   | Code           |   Read Block Size | Read ID                                 | Comment                       |     PIDV | Accc ID      | Species             | Lineage                                                                          |
| :---------: | :------------: | :---------------: | :-------------------------------------: | :---------------------------: | :------: | :----------: | ------------------- | -------------------------------------------------------------------------------- |
| PASS        | BEST HIT       |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | best hit                      |   0.0066 | MH648893.1   | Anelloviridae sp.   | Viruses --> Anelloviridae --> unclassified Anelloviridae --> Anelloviridae sp.   |
| FAIL        | NEIGHBOR       |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | viral neighbor hit            |   0.0199 | KM593803.2   | SEN virus           | Viruses --> Anelloviridae --> unclassified Anelloviridae --> SEN virus           |
| FAIL        | SECONDARY NN   |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | secondary, non-neighbor hit   |   0.0993 | FM882010.1   | Torque teno virus   | Viruses --> Anelloviridae --> unclassified Anelloviridae --> Torque teno virus   |
| FAIL        | SECONDARY NN   |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | secondary, non-neighbor hit   |   0.1523 | AY206683.1   | SEN virus           | Viruses --> Anelloviridae --> unclassified Anelloviridae --> SEN virus           |
| FAIL        | SECONDARY NN   |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | secondary, non-neighbor hit   |   0.2914 | AB059353.1   | SEN virus           | Viruses --> Anelloviridae --> unclassified Anelloviridae --> SEN virus           |
| FAIL        | SECONDARY NN   |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | secondary, non-neighbor hit   |   0.5497 | GQ179972.1   | SEN virus           | Viruses --> Anelloviridae --> unclassified Anelloviridae --> SEN virus           |
| FAIL        | SECONDARY NN   |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | secondary, non-neighbor hit   |   0.5686 | MK820646.1   | Torque teno virus   | Viruses --> Anelloviridae --> unclassified Anelloviridae --> Torque teno virus   |
| FAIL        | SECONDARY NN   |                 8 | A00584:317:HG3LNDSXY:4:1404:2465:7639   | secondary, non-neighbor hit   |   0.6291 | AB856070.1   | SEN virus           | Viruses --> Anelloviridae --> unclassified Anelloviridae --> SEN virus           |

There are 8 total hits for the read, all hitting viral taxonomy; therefore, the best hit is chosen based on the best percent identity variance (pidv) value (0.0066 for `MH648893.1`). Note, the second best hit has a pidv value of 0.0199 to a viral identity, within the the default `--pidprox` value of 0.04 for "neighbor" status, so the failure code is labeled `NEIGHBOR`. The other viral hits are too distant from the `--pidprox` value, so their failure codes are `SECONDARY NN` for secondary, non-neighbor hits.

In the next example, we have a read block with 13 total hits.

| Pass/Fail   | Code           |   Read Block Size | Read ID                                  | Comment                                |     PIDV | Accc ID      | Species                                                  | Lineage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| :---------: | :------------: | :---------------: | :--------------------------------------: | :------------------------------------: | :------: | :----------: | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |    0.007 | LT908445.1   | Spodoptera aff. frugiperda 2 RZ-2014                     | cellular organisms --> Eukaryota --> Opisthokonta --> Metazoa --> Eumetazoa --> Bilateria --> Protostomia --> Ecdysozoa --> Panarthropoda --> Arthropoda --> Mandibulata --> Pancrustacea --> Hexapoda --> Insecta --> Dicondylia --> Pterygota --> Neoptera --> Holometabola --> Amphiesmenoptera --> Lepidoptera --> Glossata --> Neolepidoptera --> Heteroneura --> Ditrysia --> Obtectomera --> Noctuoidea --> Noctuidae --> Amphipyrinae --> Spodoptera --> Spodoptera aff. frugiperda 2 RZ-2014   |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |    0.007 | M63414.1     | Orgyia pseudotsugata single capsid nuclopolyhedrovirus   | Viruses --> Baculoviridae --> Alphabaculovirus --> unclassified Alphabaculovirus --> Orgyia pseudotsugata single capsid nuclopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                             |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |    0.007 | U75930.2     | Orgyia pseudotsugata multiple nucleopolyhedrovirus       | Viruses --> Baculoviridae --> Alphabaculovirus --> Orgyia pseudotsugata multiple nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                                                   |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.0141 | KP747440.1   | Dasychira pudibunda nucleopolyhedrovirus                 | Viruses --> Baculoviridae --> Alphabaculovirus --> Dasychira pudibunda nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                                                             |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.4859 | EF207986.1   | Antheraea pernyi nucleopolyhedrovirus                    | Viruses --> Baculoviridae --> Alphabaculovirus --> Antheraea pernyi nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                                                                |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.4859 | KY979487.1   | Antheraea pernyi nucleopolyhedrovirus                    | Viruses --> Baculoviridae --> Alphabaculovirus --> Antheraea pernyi nucleopolyhedrovirus --> Antheraea proylei nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                     |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.4859 | LC194889.1   | Antheraea pernyi nucleopolyhedrovirus                    | Viruses --> Baculoviridae --> Alphabaculovirus --> Antheraea pernyi nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                                                                |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.4859 | LC375537.1   | Antheraea yamamai nucleopolyhedrovirus                   | Viruses --> Baculoviridae --> unclassified Baculoviridae --> Antheraea yamamai nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                                                     |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.4859 | MH797002.1   | Antheraea pernyi nucleopolyhedrovirus                    | Viruses --> Baculoviridae --> Alphabaculovirus --> Antheraea pernyi nucleopolyhedrovirus --> Antheraea proylei nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                     |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.6831 | KJ631623.1   | Condylorrhiza vestigialis MNPV                           | Viruses --> Baculoviridae --> Alphabaculovirus --> unclassified Alphabaculovirus --> Condylorrhiza vestigialis MNPV                                                                                                                                                                                                                                                                                                                                                                                     |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.7746 | AF368905.1   | Anticarsia gemmatalis nucleopolyhedrovirus               | Viruses --> Baculoviridae --> Alphabaculovirus --> unclassified Alphabaculovirus --> Anticarsia gemmatalis nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                         |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.7746 | DQ813662.2   | Anticarsia gemmatalis multiple nucleopolyhedrovirus      | Viruses --> Baculoviridae --> Alphabaculovirus --> Anticarsia gemmatalis multiple nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                                                  |
| FAIL        | RB AMBIGUITY   |                13 | A00584:317:HG3LNDSXY:4:2646:2248:14935   | significant ambiguous, non-viral hit   |   0.7746 | MG746625.1   | Anticarsia gemmatalis multiple nucleopolyhedrovirus      | Viruses --> Baculoviridae --> Alphabaculovirus --> Anticarsia gemmatalis multiple nucleopolyhedrovirus                                                                                                                                                                                                                                                                                                                                                                                                  |

The hits above are a mixture of viral and non-viral identities. We have a tie for best pidv, namely 0.007 for hits to `LT908445.1`, `M63414.1`, and `U75930.2`. The `LT908445.1` hit is to a non-viral species, therefore the entire read block is failed and the failure code `RB AMBIGUITY` for significant ambiguous, non-viral hit is applied to all of the hits.

The above examples walk through some of the failure codes encountered in the sanity files. See the [Failure Codes](https://twylie.github.io/viromatch/overview/reports/#failure-codes) section below for details regarding other hit failures.

### Failure Codes

All possible pass/failure codes for the best hit logic portion of the pipeline are outlined below.

| Pass/Fail Status | Code            | Comment                                         | Description                                                                                                                                         |
|:----------------:|:---------------:|:-----------------------------------------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| FAIL             | NEIGHBOR        | viral neighbor hit                              | The hit was viral in nature, the score was within the `--pidprox` or `--bitprox` value range, but another viral hit was chosen based on a better score. |
| FAIL             | RB AMBIGUITY    | significant ambiguous, non-viral hit            | If the best hits (or any neighbor hits within the `--pidprox` or `--bitprox` value range) are not viruses, we fail the entire read block.               |
| FAIL             | RB PID          | best score X is > Y                             | The best score in the read block is greater than the `--pid` value; we fail the entire read block. Specific to nucleotide alignments.                 |
| FAIL             | SECONDARY NN    | secondary, non-neighbor hit                     | The hit is failed because it is greater than the `--pidprox` or `--bitprox` value.                                                                      |
| FAILED           | TIED BEST HIT   | failed best hit (tied)                          | The hit is viral and was tied for the best hit, but was not chosen during the random best hit selection.                                            |
| IGNORED          | OTHER SEQ       | taxonomy matches 'other sequences', investigate | If a hit's lineage matches NCBI's _other sequences_ category, we ignore the hit, but quantify and report how many hits are affected.                  |
| IGNORED          | UNKNOWN TAXA    | superkingdom is unknown, investigate            | If a hit's superkingdom is _unknown_ or unclassified, we ignore the hit, but quantify and report how many hits are affected.                          |
| PASS             | BEST HIT        | best hit                                        | The hit is viral and the single best (non-tied) hit.                                                                                                |
| PASS             | RANDOM BEST HIT | randomly chosen best hit (tied)                 | The hit is viral and was tied for the best hit, and was randomly chosen within the tied best hits.                                                  |

## Taxonomy/Quantification Reports

The ultimate purpose of the ViroMatch pipeline is to review metagenomic sequence reads and report hits to known viruses. Upon completion, ViroMatch will provide reports detailing viral taxonomic classification and quantification. All report files are at the top-level of the `--outdir` directory provided in the execution command, specifically:

```plaintext
REPORT.nuc_counts.txt
REPORT.trans_nuc_counts.txt
REPORT.nuc_ambiguous_counts.txt
REPORT.trans_nuc_ambiguous_counts.txt
```

These reports are discussed in more detail below.

### Nucleotide Counts

The `REPORT.nuc_counts.txt` file reports read identities to viruses as provided by the nucleotide mapping portions of the ViroMatch pipeline. Reads tallied in this report have been assessed by alignment to the viral-only reference database, validation of candidate viral reads against the NCBI nt reference database, taxonomic classification, and finally assessment by best hit logic. Only reads that have _passed_ all of these steps are considered viral identities.

{{% button href="REPORT.nuc_counts.txt" icon="fas fa-download" icon-position="right" %}}Download Example Nucleotide Counts Report{{% /button %}}

The nucleotide counts report file consists of the following sections:

| Section           | Description                                                                                                                                                                                                                                                                                                                                                                                             |
|:-----------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Header            | The header section captures the ViroMatch configuration for the process that produced the attached report information. Pipeline parameters are listed here.                                                                                                                                                                                                                                             |
| Lineage (R1 + R2) | The lineage section provides a breakdown of viral read counts at the full lineage level --- i.e. all taxonomic categories as provided by NCBI. Fields for this table are read count, percent of reads represented, and full lineage. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined.                                                   |
| Genus (R1 + R2)   | The genus section provides a breakdown of viral read counts at genus-level taxonomy. Fields for this table are read count, percent of reads represented, and genus. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined. This is the same cumulative total as listed in the lineage section, but broken down by genus.                    |
| Species (R1 + R2) | The species section provides a breakdown of viral read counts at species-level taxonomy. Fields for this table are read count, percent of reads represented, and species. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined. This is the same cumulative total as listed in the lineage and genus sections, but broken down by species. |
| Lineage (R1)      | The same information as outlined in the _Lineage (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                                                                                |
| Genus (R1)        | The same information as outlined in the _Genus (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                                                                                  |
| Species (R1)      | The same information as outlined in the _Species (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                                                                                |
| Lineage (R2)      | The same information as outlined in the _Lineage (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                                                                |
| Genus (R2)        | The same information as outlined in the _Genus (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                                                                  |
| Species (R2)      | The same information as outlined in the _Species (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                                                                |

### Translated Nucleotide Counts

The `REPORT.trans_nuc_counts.txt` file reports read identities to viruses as provided by the translated nucleotide mapping portions of the ViroMatch pipeline. Reads tallied in this report have been assessed by alignment to the viral-only translated reference database, validation of candidate viral reads against the NCBI nr reference database, taxonomic classification, and finally assessment by best hit logic. Only reads that have _passed_ all of these steps are considered viral identities.

{{% button href="REPORT.trans_nuc_counts.txt" icon="fas fa-download" icon-position="right" %}}Download Example Translated Nucleotide Counts Report{{% /button %}}

Translated nucleotide viral identities are reads that failed to map significantly during the nucleotide mapping sections of the pipeline but have identity to translated nucleotide viral references; therefore, these counts are separate and distinct from those listed in the `REPORT.trans_nuc_counts.txt` report. Adding together the counts in the `REPORT.nuc_counts.txt` and `REPORT.trans_nuc_counts.txt` files gives the total viral read counts for a given sample. As reads are given the opportunity to map to nucleotide references before translated nucleotide references, translated nucleotide counts are often much lower in count when compared to nucleotide reference counts.

The translated nucleotide counts report file consists of the following sections:

| Section           | Description                                                                                                                                                                                                                                                                                                                                                                                             |
|:-----------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Header            | The header section captures the ViroMatch configuration for the process that produced the attached report information. Pipeline parameters are listed here.                                                                                                                                                                                                                                             |
| Lineage (R1 + R2) | The lineage section provides a breakdown of viral translated read counts at the full lineage level --- i.e. all taxonomic categories as provided by NCBI. Fields for this table are read count, percent of reads represented, and full lineage. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined.                                        |
| Genus (R1 + R2)   | The genus section provides a breakdown of viral translated read counts at genus-level taxonomy. Fields for this table are read count, percent of reads represented, and genus. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined. This is the same cumulative total as listed in the lineage section, but broken down by genus.         |
| Species (R1 + R2) | The species section provides a breakdown of viral translated read counts at species-level taxonomy. Fields for this table are read count, percent of reads represented, and species. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined. This is the same cumulative total as listed in the lineage and genus sections, but broken down by species. |
| Lineage (R1)      | The same information as outlined in the _Lineage (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                                                                                |
| Genus (R1)        | The same information as outlined in the _Genus (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                                                                                  |
| Species (R1)      | The same information as outlined in the _Species (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                                                                                |
| Lineage (R2)      | The same information as outlined in the _Lineage (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                                                                |
| Genus (R2)        | The same information as outlined in the _Genus (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                                                                  |
| Species (R2)      | The same information as outlined in the _Species (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                                                                |

### Ambiguous Counts

The `REPORT.nuc_ambiguous_counts.txt` and `REPORT.trans_nuc_ambiguous_counts.txt` files report ambiguous hit identities encountered by the nucleotide and translated nucleotide mapping portions of the ViroMatch pipeline.

{{% button href="REPORT.nuc_ambiguous_counts.txt" icon="fas fa-download" icon-position="right" %}}Download Example Nucleotide Ambiguous Report{{% /button %}}

{{% button href="REPORT.trans_nuc_ambiguous_counts.txt" icon="fas fa-download" icon-position="right" %}}Download Example Translated Nucleotide Ambiguous Report{{% /button %}}

In early tests of ViroMatch, we noticed that NCBI had questionable taxonomic classifications for some of their reference sequences, leading to misleading identities. Some reads were aligning to references that were: 1) reference sequences that NCBI designates as _unclassified sequences_; 2) _other sequences_ consisting of cloning vector, synthetic constructs, or other artificial sequences.

When a read has a hit to a reference whose superkingdom is _Unknown_, we can't evaluate if the hit is a virus or non-viral, so we ignore/skip the hit; however, we quantify and report how many hits are affected in this manner from all of the reviewed sequences. The _other sequences_ category has reference entries with partial viral sequences submitted as part of cloning vectors etc., which can lead to false negatives during the best hit logic phase of the pipeline. If a hit's lineage matches NCBI's _other sequences_ category, we ignore the hit, but quantify and report how many hits are affected. These categories are now partitioned during ViroMatch classification reports as _uknown_ and _ambiguous_ hit counts, respectively.

Ambiguous hit counts are reported for reference, but are never considered in the pipeline past the point of their initial taxonomic identification.

{{% notice note %}}
It is important to note that a single read can have hits to multiple references. During the best hit logic portion of the pipeline, we evaluate all of the hits for a single read as a _read block_, or all of the hits for the read. Removing hits for either _other sequences_ or _unknown_ taxonomy removes only those hits from the read block and leaves the other hits for further evaluation; therefore, ambiguous hit removal does not necessarily mean the read has been failed.
{{% /notice %}}

The ambiguous nucleotide hit counts report files consist of the following sections:

| Section                           | Description                                                                                                                                                                                                                                                                                                                                                              |
|:---------------------------------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Other Sequences Header            | The header section captures the ViroMatch configuration for the process that produced the attached report information. Pipeline parameters are listed here.                                                                                                                                                                                                              |
| Other Sequences Lineage (R1 + R2) | The lineage section provides a breakdown of hit counts related to _other sequences_ at the full lineage level --- i.e. all taxonomic categories as provided by NCBI. Fields for this table are hit count, percent of reads represented, and full lineage. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined. |
| Other Sequences Lineage (R1)      | The same information as outlined in the _Other Sequences Lineage (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                                 |
| Other Sequences Lineage (R2)      | The same information as outlined in the _Other Sequences lineage (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                 |
| Unknown Header                    | The header section captures the ViroMatch configuration for the process that produced the attached report information. Pipeline parameters are listed here.                                                                                                                                                                                                              |
| Unknown Lineage (R1 + R2)         | The lineage section provides a breakdown of hit counts related to _unknown_ at the full lineage level --- i.e. all taxonomic categories as provided by NCBI. Fields for this table are hit count, percent of reads represented, and full lineage. A cumulative total is also provided. For this section, counts are derived from both read pairs (R1 & R2) combined.         |
| Unknown Lineage (R1)              | The same information as outlined in the _Unknown Lineage (R1 + R2)_ section, but representative of only the contributing R1 reads.                                                                                                                                                                                                                          |
| Unknown Lineage (R2)              | The same information as outlined in the _Unknown lineage (R1 + R2)_ section, but representative of only the contributing R2 reads.                                                                                                                                                                                                                                         |
