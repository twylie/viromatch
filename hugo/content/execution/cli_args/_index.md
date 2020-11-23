---
title: "Command Line Arguments"
date: 2020-11-11T11:52:44-06:00
draft: false
weight: 4
---

## Terse Usage Statement

Typing `viromatch` from the command line will display a terse usage statement.

```bash
docker container run twylie/viromatch:latest viromatch
```

Results:

```plaintext
usage: viromatch [-h] [--version] [--keep] [--dryrun] [--smkcores INT]
                 [--endqual INT] [--minn INT] [--phred 33|64] [--readlen INT]
                 [--pid FLOAT] [--pidprox FLOAT] [--bsize INT] [--bitprox INT]
                 [--mts INT] [--evalue FLOAT] --sampleid STR --input FILE
                 [FILE ...] --outdir DIR --nt FILE [FILE ...] --nr FILE
                 [FILE ...] --viralfna FILE --viralfaa FILE --host FILE
                 --adaptor FILE --taxid FILE [--wustlconfig FILE]
viromatch: error: the following arguments are required: --sampleid, --input, --outdir, --nt, --nr, --viralfna, --viralfaa, --host, --adaptor, --taxid
```

## Detailed Usage Statement

You may get a detailed list of command line options using the `--help` switch from the command line.

```plaintext
docker container run twylie/viromatch:latest viromatch --help
```

Results:

```plaintext
usage: viromatch [-h] [--version] [--keep] [--dryrun] [--smkcores INT]
                 [--endqual INT] [--minn INT] [--phred 33|64] [--readlen INT]
                 [--pid FLOAT] [--pidprox FLOAT] [--bsize INT] [--bitprox INT]
                 [--mts INT] [--evalue FLOAT] --sampleid STR --input FILE
                 [FILE ...] --outdir DIR --nt FILE [FILE ...] --nr FILE
                 [FILE ...] --viralfna FILE --viralfaa FILE --host FILE
                 --adaptor FILE --taxid FILE [--wustlconfig FILE]

Read-based virome characterization pipeline.

optional arguments:
  -h, --help            Display the extended usage statement.
  --version             Display the software version number.
  --keep                Retain intermediate files.
  --dryrun              Preps pipeline but no execution.
  --smkcores INT        Number of CPU cores for Snakemake. [1]
  --endqual INT         Trim 3'-end when quality drops below value. [10]
  --minn INT            Max percent of Ns allowed post-trimming. [50]
  --phred 33|64         Choose phred-33 or phred-64 quality encoding. [33]
  --readlen INT         Minimum read length after trimming. [50]
  --pid FLOAT           Max percent id variance for nucleotide hits. [0.15]
  --pidprox FLOAT       Max proximal percent id variance for nucleotide hits.
                        [0.04]
  --bsize INT           Buffer size for sorting (Gb). [1]
  --bitprox INT         Max proximal bitscore for translated hits. [1]
  --mts INT             Translated nucleotide max-target-seqs. [5]
  --evalue FLOAT        Translated nucleotide max-expect-value. [0.001]

required:
  --sampleid STR        Label or id for sample.
  --input FILE [FILE ...]
                        Path to single input BAM or paired FASTQ file(s).
  --outdir DIR          Path to directory for writing output.
  --nt FILE [FILE ...]  NCBI nt nucleotide FASTA file(s) or NT.fofn file.
  --nr FILE [FILE ...]  NCBI nr protein FASTA file(s) or NR.fofn file.
  --viralfna FILE       Viral identity (indexed) nucleotide FASTA file.
  --viralfaa FILE       Viral identity (indexed) translated FASTA file.
  --host FILE           Host (indexed) FASTA file for host screening.
  --adaptor FILE        File with adapter sequences to trim.
  --taxid FILE          Taxonomy ID lookup file.

Washington University only (LSF cluster submission):
  --wustlconfig FILE    Path to config file for WUSTL LSF parallel processing.
```

## Command Line Options

Details for the command line options are outlined below. Some arguments are required while others are optional.

### Required Arguments

| Argument   | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:----------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--sampleid` | string       | User defined text for sample identification. This text is used in the reports to help identify/track the sample.                                                                                                                                                                                                            |
| `--input`    | file path(s) | Path to the input read file(s). A user may provide either (1) a single input uBAM file or (2) paired FASTQ files. If a uBAM file is provided, it will be converted to paired FASTQ files for downstream processing. If paired FASTQ files are provided, the R1-file should be first followed by the R2-file, space delimited. |
| `--outdir`   | dir path     | Path to the directory for writing output. All ViroMatch ouput will be written here for a given instance of the pipeline.                                                                                                                                                                                                    |
| `--nt`       | file path(s) | Space delimited list of paths to ViroMatch's split NCBI nt nucleotide indexed FASTA files. Alternatively, a file with paths to the files, one per line, can be supplied instead, provided the file has a _.fofn_ suffix --- e.g. NT.fofn file.                                                                                |
| `--nr`       | file path(s) | Space delimited list of paths to ViroMatch's split NCBI nr nucleotide indexed FASTA files. Alternatively, a file with paths to the files, one per line, can be supplied instead, provided the file has a _.fofn_ suffix --- e.g. NR.fofn file.                                                                                |
| `--viralfna` | file path    | Path to ViroMatch's viral identity nucleotide indexed FASTA file. Putative viral identities come from this database prior to extended validation alignments.                                                                                                                                                                |
| `--viralfaa` | file path    | Path to ViroMatch's viral identity translated nucleotide indexed FASTA file. Putative viral identities come from this database prior to extended validation alignments.                                                                                                                                                     |
| `--host`     | file path    | Path to ViroMatch's host indexed FASTA file used for host screening. By default we provide an indexed version of the human reference genome.                                                                                                                                                                                |
| `--adaptor`  | file path    | Path to a file with adapter sequences, one per line, used for read trimming.                                                                                                                                                                                                                                                |
| `--taxid`    | file path    | Path to ViroMatch's taxonomy database. This file provides NCBI-based taxonomy and lineages based on NCBI taxon ids.                                                                                                                                                                                                         |

### Optional Arguments

| Argument   | Type    | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|:----------:|:-------:|:-------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--help`     | switch  |         | This switch will display the extended usage statement for ViroMatch command line parameters. Using this switch obviates pipeline execution.                                                                                                                                                                                                                                                                                                                                   |
| `--version`  | switch  |         | This switch will print the version id of the ViroMatch software being run. Using this switch obviates pipeline execution.                                                                                                                                                                                                                                                                                                                                                     |
| `--keep`     | switch  |         | ViroMatch generates many intermediate files that are marked as _temporary_ in the pipeline. By default, these files are deleted on the file system once they are no longer required for generating downstream output. Using the `--keep` switch will retain all of the temporary files produced by the pipeline. Please note, keeping these files will increase overall disk space consumption.                                                                                   |
| `--dryrun`   | switch  |         | Running this switch will create the ViroMatch output directory and write all of the files needed to run the pipeline; however, using this switch obviates pipeline execution. This can be useful for troubleshooting or reviewing setup prior to running the pipeline. The pipeline can still be executed by manually running the `cmd.sh` script in the output directory.                                                                                                      |
| `--smkcores` | integer |       1 | For systems with multiple processors, this value tells ViroMatch how many CPU cores to use in parallel, when possible. ViroMatch uses Snakemake for pipeline execution, which will automatically handle parallel steps. This value directly feeds Snakemake's `--cores` option. Note: This is *not* the same as parallel processing by submitting jobs to a compute cluster --- e.g. LSF jobs.                                                                                    |
| `--endqual`  | integer |      10 | During the adaptor trimming portion of the pipeline, we also trim the 3'-end of reads when base quality values drop below the `--endqual` value.                                                                                                                                                                                                                                                                                                                                |
| `--minn`     | integer |      50 | After trimming and low-complexity masking, a read is evaluated for the maximum percent of N's allowed across the read. If the percent of N's is greater than the `--minn` value then the read is _failed_ and not used downstream. Default is 50% of a read's length.                                                                                                                                                                                                               |
| `--phred`    | 33, 64  |      33 | This value tells the pipeline what encoding the input FASTQ files uses. You may choose phred-33 [33] or phred-64 [64] quality encoding. Default is phred-33 encoding.                                                                                                                                                                                                                                                                                                         |
| `--readlen`  | integer |      50 | After trimming, a read is evaluated for post-processed read length. The minimum read length (in basepairs) allowable after trimming is set by the `--readlen` value. Default is 50 bp or greater to use a read downstream, else the read is _failed_.                                                                                                                                                                                                                             |
| `--pid`      | float   |    0.15 | During the best-hit filter logic step of the pipeline, a nucleotide alignment is evaluated for the percent nucleotide variance a read (query) has compared to its reference (subject). The `--pid` value sets the maximum percent id variance allowable for a hit. Default is any hit with over 15% variance is considered _failed_.                                                                                                                                              |
| `--pidprox`  | float   |    0.04 | During the best-hit filter logic step of the pipeline, secondary (non-best-hit) nucleotide alignments are evaluated for their percent nucleotide variance when compared to the best hit for a read. The `--pidprox` value sets the maximum percent id variance allowable for a secondary hit. Default is any secondary/proximal hit with over 4% variance is considered _failed_.                                                                                                 |
| `--bsize`    | integer |       1 | During the best-hit filter logic step of the pipeline, reads are evaluated in a read block based on alignments sorted by read id. The `--bsize` option sets the maximum buffer size (Gb) for sorting in memory, before an external sort buffers to disk. If the sort exceeds the `--bsize` limit, it will buffer to disk. As the sort size will almost always be larger than convential memory, we can enforce disk buffering by setting `--bsize` low, such as the default of 1 GB. |
| `--bitprox`  | integer |       1 | During the best-hit filter logic step of the pipeline, secondary (non-best-hit) translated nucleotide alignments are evaluated for their bitscore when compared to the best hit for a read. The `--bitprox` value sets the maximum btiscore distance allowable for a secondary hit. Default is any secondary/proximal hit with a bitscore over 1 is considered _failed_.                                                                                                          |
| `--mts`      | integer |       5 | For translated nucleotide alignments, the maximum number of target sequences per read to report alignments. Reads are evaluated in a /read-block/ based on alignments sorted by read id. Default is top 5 alignments per read.                                                                                                                                                                                                                                                  |
| `--evalue`   | float   |   0.001 | For translated nucleotide alignments, the maximum expected value (e-value) to report an alignment. Default e-value is very conservative (0.001); increasing the e-value reports more questionable alignments.                                                                                                                                                                                                                                                                 |
|            |         |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

### Washington University Specific Arguments

{{% notice warning %}}
These options are only available to those running ViroMatch at Washington University School of Medicine through the **compute1** high performance computing server.
{{% /notice %}}

| Argument      | Type      | Description                                                                                                                                                             |
|:-------------:|:---------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--wustlconfig` | file path | Path to a YAML configuration file used for WUSTL LSF job parallel processing. Variables provided in this file are used for LSF job submission configuration. See [Wustlconfig File](https://twylie.github.io/viromatch/overview/file_types/#wustlconfig-file) for more details on configuration file format. |

------------

