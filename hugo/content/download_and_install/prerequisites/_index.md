---
title: "Prerequisites"
date: 2020-11-10T22:36:09-06:00
draft: false
weight: 1
---

## System Resources

In terms of disk space and memory, requirements vary depending on the size of the samples you are processing. We have run ViroMatch on thousands of samples, ranging from 1 million reads to over 200 million reads processed. At lower boundary single core processing, we have processed 30 million reads using 8 GB of memory and 105 GB of disk space and 17:04 runtime. The same data set was parallel processed using 100 cores and 16 GB memory in under 5 hours, same disk space.

As a general rule of thumb, we use 16 GB of memory.

Disk space needed for ViroMatch processing can be considerable (potentially hundreds of gigabytes) depending on the number of reads processed per sample, especially if the `--keep` option is used to retain all temporary files.

{{% notice note %}}
General resources and benchmarks are outlined on this page as broad guidelines. It is not possible to give exact requirements for resources --- e.g. processing time, memory, disk space --- _a priori_, as these resources are highly dependent on the viral complexity of the sequencing reads being evaluated. If a very large portion of the reads are viral, then processing will likely take longer and use more resources when compared to a sample with fewer viral reads.
{{% /notice %}}

## Example Runtime Breakdown

In the table below, we processed 11,829,946 reads using a single core and 16 GB of RAM in a total of 8:00:06 runtime. Each step in the pipeline is broken down and shows how long the step took to complete. Note that some steps produce more output files than other and benefit from parallel processing. This same sample was parallel-processed on the WashU compute1 LSF server using 150 cores (16 GB RAM each) and finished in 2:35:45 runtime. Steps like `validate_nuc_nt_mapping` and `validate_trans_nuc_nr_mapping` benefit greatly from parallel-processing, as their processes are computationally intensive across multiple discrete iterations within the step. Results indicate <10K reads (0.008%) were viral in this sample.

| Pipeline Steps                                |        Sub-Steps |   Total Time (seconds) |   Hours |   Minutes |   Seconds |
| :-------------------------------------------: | :--------------: | :--------------------: | :-----: | :-------: | :-------: |
| **prep_fastq_files**                            |                1 |            27.85244131 |       0 |         0 |        27 |
| **trim_fastq_files**                            |                2 |            5559.313289 |       1 |        32 |        39 |
| **blank_eval_filter_low_complexity**            |                2 |            12.54826808 |       0 |         0 |        12 |
| **filter_low_complexity_fastq_files**           |                2 |            212.6389837 |       0 |         3 |        32 |
| **host_screen_mapping**                         |                2 |            2385.155264 |       0 |        39 |        45 |
| **host_screen_write_unmapped_bam**              |                2 |            34.51873302 |       0 |         0 |        34 |
| **host_screen_write_unmapped_fastq**            |                2 |            10.13627338 |       0 |         0 |        10 |
| **viral_nuc_mapping**                           |                2 |            175.7005126 |       0 |         2 |        55 |
| **viral_nuc_write_unmapped_bam**                |                2 |            18.99056435 |       0 |         0 |        18 |
| **viral_nuc_write_unmapped_fastq**              |                2 |            18.39612222 |       0 |         0 |        18 |
| **viral_nuc_write_mapped_bam**                  |                2 |            24.41263771 |       0 |         0 |        24 |
| **viral_nuc_write_mapped_fastq**                |                2 |            25.48392177 |       0 |         0 |        25 |
| **blank_eval_viral_trans_nuc**                  |                2 |            7.917856216 |       0 |         0 |         7 |
| **viral_trans_nuc_mapping**                     |                2 |            280.4345899 |       0 |         4 |        40 |
| **viral_trans_nuc_daa_to_tsv**                  |                2 |            29.10870218 |       0 |         0 |        29 |
| **viral_trans_nuc_extract_mapped_ids**          |                2 |            26.77536488 |       0 |         0 |        26 |
| **viral_trans_nuc_write_mapped_fastq**          |                2 |            11.67773151 |       0 |         0 |        11 |
| **viral_mapped_fastq_merge**                    |                2 |            8.115232706 |       0 |         0 |         8 |
| **validate_nuc_nt_mapping**                     |              148 |            10271.54403 |       2 |        51 |        11 |
| **validate_nuc_nt_write_mapped_sam**            |              148 |            1164.741204 |       0 |        19 |        24 |
| **validate_nuc_nt_write_unmapped_sam**          |              148 |            1163.295703 |       0 |        19 |        23 |
| **validate_nuc_nt_merge_r1_mapped_sam**         |                1 |            191.6536033 |       0 |         3 |        11 |
| **validate_nuc_nt_merge_r2_mapped_sam**         |                1 |            8.467573881 |       0 |         0 |         8 |
| **validate_nuc_nt_write_r1_unmapped_ids**       |                1 |             22.6810627 |       0 |         0 |        22 |
| **validate_nuc_nt_write_r2_unmapped_ids**       |                1 |            6.817457676 |       0 |         0 |         6 |
| **validate_nuc_nt_write_merged_unmapped_fastq** |                2 |            3.277892351 |       0 |         0 |         3 |
| **blank_eval_validate_trans_nuc_nr**            |                2 |            3.754998446 |       0 |         0 |         3 |
| **validate_trans_nuc_nr_mapping**               |               80 |            5631.398906 |       1 |        33 |        51 |
| **validate_trans_nuc_nr_mapping_daa_to_tsv**    |               80 |            792.9289281 |       0 |        13 |        12 |
| **validate_trans_nuc_nr_merge_r1_mapped_tsv**   |                1 |             5.43210721 |       0 |         0 |         5 |
| **validate_trans_nuc_nr_merge_r2_mapped_tsv**   |                1 |            2.971903563 |       0 |         0 |         2 |
| **nuc_nt_best_hit_filter_sam**                  |                2 |            97.25468874 |       0 |         1 |        37 |
| **trans_nuc_nr_best_hit_filter_tsv**            |                2 |            84.00837421 |       0 |         1 |        24 |
| **nuc_nt_otherseq_hit_report**                  |                1 |            349.1610229 |       0 |         5 |        49 |
| **nuc_nt_unknown_hit_report**                   |                1 |            20.51718807 |       0 |         0 |        20 |
| **trans_nuc_nr_otherseq_hit_report**            |                1 |            23.29803538 |       0 |         0 |        23 |
| **trans_nuc_nr_unknown_hit_report**             |                1 |             10.5249989 |       0 |         0 |        10 |
| **nuc_nt_best_hit_count_prep**                  |                1 |             6.06182313 |       0 |         0 |         6 |
| **trans_nuc_nr_best_hit_count_prep**            |                1 |            10.92386746 |       0 |         0 |        10 |
| **nuc_nt_best_hit_counts**                      |                1 |            37.75414157 |       0 |         0 |        37 |
| **trans_nuc_nr_best_hit_counts**                |                1 |            3.687265873 |       0 |         0 |         3 |
| **copy_nuc_nt_report**                          |                1 |              8.1452775 |       0 |         0 |         8 |
| **copy_trans_nuc_nr_report**                    |                1 |            0.593919754 |       0 |         0 |         0 |
| **copy_nuc_ambiguous_report**                   |                1 |            13.35895181 |       0 |         0 |        13 |
| **copy_trans_nuc_ambiguous_report**             |                1 |            3.470051765 |       0 |         0 |         3 |
|                                               |            **665** |          **28806.90147** |     **8** |       **0** |       **6** |

## Downloads

While the ViroMatch code base is hosted at [https://github.com/twylie/viromatch](https://github.com/twylie/viromatch), we only support using the official Docker image. Docker Desktop is required on your computer in order to run ViroMatch containers. All required code and third party dependencies are included in the ViroMatch Docker image. You will also need to download required ViroMatch reference genome databases using Globus.

Checklist:

+ Docker Desktop software (download from Docker)
+ ViroMatch Docker image (download from DockerHub)
+ ViroMatch reference genome databases (download using Globus)

Download instructions for these items are outlined in the following pages.
