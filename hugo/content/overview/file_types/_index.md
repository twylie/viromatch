---
title: "Input File Types"
date: 2020-11-11T13:22:23-06:00
draft: false
weight: 5
---

## Pipeline Input Files

| Argument | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:--------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--input`  | file path(s) | Path to the input read file(s). A user may provide either (1) a single input uBAM file or (2) paired FASTQ files. If a uBAM file is provided, it will be converted to paired FASTQ files for downstream processing. If paired FASTQ files are provided, the R1-file should be first followed by the R2-file, space delimited. |

## FASTQ Files

[FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) is an extension of the veneral [FASTA](https://en.wikipedia.org/wiki/FASTA_format) sequence format first described by [P. Cock, et al](https://academic.oup.com/nar/article/38/6/1767/3112533). FASTQ combines sequence and quality information in the same file format. ViroMatch accepts paired FASTQ files --- i.e. two FASTQ files from the same sample with read-1 and read-2 pairs broken out, ordered by corresponding read pair ids --- as `--input` when running the pipeline.

{{% notice note %}}
For FASTQ support, ViroMatch requires that you pass two FASTQ files whose order retains correspondiong read pair ids. For example, read_1/1 and read_1/2 should be the first entries in the FASTQ files, respectively.
{{% /notice %}}

Within the larger ViroMatch command, the `--input` argument for FASTQ files would look something like this.

```bash
viromatch --input example.r1.fastq example.r2.fastq
```

The first 2 entries of example.r1.fastq file:

```plaintext
@D00170:57:CA2R8ANXX:4:1101:10005:81687/1
GTTTCTACCATGTGTACTGGAATTCTTATAGTTCTAGCTTGATCTGCTATTGCTCTTGTAATAGCTTGTCTTATCCACCATGTTGCATAAGTACTAAATTTAAAACCTTTAGTATAATCAAACTTC
+
BBBBBF/<B/<FBFF<FF///<FB//BB/FFFFFFFBFF///<FF<FFF/FFFB/BFF<F/FF/FFFFFF<F<FFFF//<FFF<<FF/F//<FF//<BF/<<FFFFF/FFF/FFFFBF/FF<BB</
@D00170:57:CA2R8ANXX:4:1101:10024:71656/1
ACACTGCTTCACCCACTCCCACGGCTCCACCGTCCCATCTCCGTCCAAATCGGGGCTGAGGTCGCGGTGGCCGCATACACGGGCGTTCCGGAACTGTTGTAGCAGCTGGTACACCAGCAGGTGCAG
+
BBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
```

The first 2 entries of example.r2.fastq file:

```plaintext
@D00170:57:CA2R8ANXX:4:1101:10005:81687/2
AGAGGCTAAACAAAAATTAGCAGAGTCAAACTTAAGATTAGTTGTAAGTATTGCTAAAAAATATGTTGGAAGAGGAATGCTATTCTTAGATTTAATACAAGAAGGTAACATGGGTCTTATAAAAGC
+
BBBBBFFBFFFFFFFFFFFFFFBFFFFFFFF</FFFFFFF/<F<F/FBF<<FFF/FFFBF<<F<FBBBF/BBBBBFBBFFFFFFFF/B<BBFFFFFFFFBF/FFFBBFFFF/FFFFFF<FF/7<B/
@D00170:57:CA2R8ANXX:4:1101:10024:71656/2
GAAGGCGGGCTGGATGCCCGGGGAAATCCGAAGGATACCCGTACGCCGGAGCAGCATTCGGCCCTGCACCTGCTGGTGTACCAGCTGCTACAACAGTTCCGGAACGCCCGTGTATGCGGCCACCGC
+
BBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
```

Note in the example above that sequence `@D00170:57:CA2R8ANXX:4:1101:10005:81687` has read-1 ordered in the `example.r1.fastq` file corresponding to read-2 in the `example.r2.fastq` file, as indicated by the `/r1` and `/r2` suffixes, respectively.

## uBAM File

It is not uncommon for unmapped FASTQ files to be stored in the BAM format simply to take advantage of its file compression format and save disk space. If your started point is such an unmapped BAM (uBAM) file, where read pairs are stored in the BAM format, you may feed ViroMatch a single uBAM file as `--input` when running the pipeline. ViroMatch will automatically convert the BAM file into constituent FASTQ read files (R1 & R2) while executing the pipeline.

{{% notice note %}}
For those running ViroMatch at Washington University School of Medicine through the **compute1** high performance computing server, your input will almost always be the uBAM format.
{{% /notice %}}

For an in-depth overview of the SAM/BAM file specification please visit the [SAM/BAM and related specifications](http://samtools.github.io/hts-specs/) page or [samtools/hts-specs](https://github.com/samtools/hts-specs) repository.

Within the larger ViroMatch command, the `--input` argument for a BAM would look something like this.

```bash
viromatch --input example.bam
```

BAM files are not directly human-readable but can be viewed using [Samtools](http://www.htslib.org/) software.

## NCBI nt Files

| Argument   | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:----------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--nt`       | file path(s) | Space delimited list of paths to ViroMatch's split NCBI nt nucleotide indexed FASTA files. Alternatively, a file with paths to the files, one per line, can be supplied instead, provided the file has a _.fofn_ suffix --- e.g. NT.fofn file.                                                                                |

### Command Line List (nt)

The NCBI nt reference database is too large to pragmatically facilitate direct alignments without considerable computational resources. Therefore, we have split nt into multiple parts for iterative processing. The `--nt` argument points ViroMatch to where the split and indexed nt reference files reside on your system. File paths should be fully qualified and not rely on relative paths.

We may pass these files directly on the command line when running the pipeline, space-delimited. Within the larger ViroMatch command, the `--nt` argument for FASTQ files would look something like this.

```bash
viromatch --nt /databases/ncbi/nt/nt-1.fna /databases/ncbi/nt/nt-2.fna /databases/ncbi/nt/nt-3.fna /databases/ncbi/nt/nt-4.fna /databases/ncbi/nt/nt-5.fna /databases/ncbi/nt/nt-6.fna /databases/ncbi/nt/nt-7.fna /databases/ncbi/nt/nt-8.fna /databases/ncbi/nt/nt-9.fna /databases/ncbi/nt/nt-10.fna /databases/ncbi/nt/nt-11.fna /databases/ncbi/nt/nt-12.fna /databases/ncbi/nt/nt-13.fna /databases/ncbi/nt/nt-14.fna /databases/ncbi/nt/nt-15.fna /databases/ncbi/nt/nt-16.fna /databases/ncbi/nt/nt-17.fna /databases/ncbi/nt/nt-18.fna /databases/ncbi/nt/nt-19.fna /databases/ncbi/nt/nt-20.fna /databases/ncbi/nt/nt-21.fna /databases/ncbi/nt/nt-22.fna /databases/ncbi/nt/nt-23.fna /databases/ncbi/nt/nt-24.fna /databases/ncbi/nt/nt-25.fna /databases/ncbi/nt/nt-26.fna /databases/ncbi/nt/nt-27.fna /databases/ncbi/nt/nt-28.fna /databases/ncbi/nt/nt-29.fna /databases/ncbi/nt/nt-30.fna /databases/ncbi/nt/nt-31.fna /databases/ncbi/nt/nt-32.fna /databases/ncbi/nt/nt-33.fna /databases/ncbi/nt/nt-34.fna /databases/ncbi/nt/nt-35.fna /databases/ncbi/nt/nt-36.fna /databases/ncbi/nt/nt-37.fna /databases/ncbi/nt/nt-38.fna /databases/ncbi/nt/nt-39.fna /databases/ncbi/nt/nt-40.fna /databases/ncbi/nt/nt-41.fna /databases/ncbi/nt/nt-42.fna /databases/ncbi/nt/nt-43.fna /databases/ncbi/nt/nt-44.fna /databases/ncbi/nt/nt-45.fna /databases/ncbi/nt/nt-46.fna /databases/ncbi/nt/nt-47.fna /databases/ncbi/nt/nt-48.fna /databases/ncbi/nt/nt-49.fna /databases/ncbi/nt/nt-50.fna /databases/ncbi/nt/nt-51.fna /databases/ncbi/nt/nt-52.fna /databases/ncbi/nt/nt-53.fna /databases/ncbi/nt/nt-54.fna /databases/ncbi/nt/nt-55.fna /databases/ncbi/nt/nt-56.fna /databases/ncbi/nt/nt-57.fna /databases/ncbi/nt/nt-58.fna /databases/ncbi/nt/nt-59.fna /databases/ncbi/nt/nt-60.fna /databases/ncbi/nt/nt-61.fna /databases/ncbi/nt/nt-62.fna /databases/ncbi/nt/nt-63.fna /databases/ncbi/nt/nt-64.fna /databases/ncbi/nt/nt-65.fna /databases/ncbi/nt/nt-66.fna /databases/ncbi/nt/nt-67.fna /databases/ncbi/nt/nt-68.fna /databases/ncbi/nt/nt-69.fna /databases/ncbi/nt/nt-70.fna /databases/ncbi/nt/nt-71.fna /databases/ncbi/nt/nt-72.fna /databases/ncbi/nt/nt-73.fna /databases/ncbi/nt/nt-74.fna
```

Although we are pointing to the FASTA files in the above command, the corresponding indexed files should also be present on your system. For example, `/databases/ncbi/nt/nt-1.fna` should have the following files located along with the FASTA file.

```plaintext
/databases/ncbi/nt/nt-1.fna
/databases/ncbi/nt/nt-1.fna.amb
/databases/ncbi/nt/nt-1.fna.ann
/databases/ncbi/nt/nt-1.fna.bwt
/databases/ncbi/nt/nt-1.fna.pac
/databases/ncbi/nt/nt-1.fna.sa
```

### File of File Names (nt)

In the above command line example, we passed all of the split and indexed nt database files on the command line as a list. As there are many split files, using this method makes the command line statement hard to read, and invites user error (e.g. accidentally omitting a split file). Therefore it is recommended that you supply the `--nt` argument a file of file names where each line is a fully qualified path to the nt FASTA files.

{{% notice warning %}}
Your file of file names file must end in a `.fofn` suffix.
{{% /notice %}}

Although we are pointing to the FASTA files in the _fofn_ file, the corresponding indexed files should also be present on your system as outlined above.

Within the larger ViroMatch command, the `--nt` argument for the file of file names would look something like this.

```bash
viromatch --nt /databases/ncbi/nt/nt.fofn
```

The `nt.fofn` file will contain the paths to all of the split NCBI nt files, like so.

```plain
/databases/ncbi/nt/nt-1.fna
/databases/ncbi/nt/nt-2.fna
/databases/ncbi/nt/nt-3.fna
/databases/ncbi/nt/nt-4.fna
/databases/ncbi/nt/nt-5.fna
/databases/ncbi/nt/nt-6.fna
/databases/ncbi/nt/nt-7.fna
/databases/ncbi/nt/nt-8.fna
/databases/ncbi/nt/nt-9.fna
/databases/ncbi/nt/nt-10.fna
/databases/ncbi/nt/nt-11.fna
/databases/ncbi/nt/nt-12.fna
/databases/ncbi/nt/nt-13.fna
/databases/ncbi/nt/nt-14.fna
/databases/ncbi/nt/nt-15.fna
/databases/ncbi/nt/nt-16.fna
/databases/ncbi/nt/nt-17.fna
/databases/ncbi/nt/nt-18.fna
/databases/ncbi/nt/nt-19.fna
/databases/ncbi/nt/nt-20.fna
/databases/ncbi/nt/nt-21.fna
/databases/ncbi/nt/nt-22.fna
/databases/ncbi/nt/nt-23.fna
/databases/ncbi/nt/nt-24.fna
/databases/ncbi/nt/nt-25.fna
/databases/ncbi/nt/nt-26.fna
/databases/ncbi/nt/nt-27.fna
/databases/ncbi/nt/nt-28.fna
/databases/ncbi/nt/nt-29.fna
/databases/ncbi/nt/nt-30.fna
/databases/ncbi/nt/nt-31.fna
/databases/ncbi/nt/nt-32.fna
/databases/ncbi/nt/nt-33.fna
/databases/ncbi/nt/nt-34.fna
/databases/ncbi/nt/nt-35.fna
/databases/ncbi/nt/nt-36.fna
/databases/ncbi/nt/nt-37.fna
/databases/ncbi/nt/nt-38.fna
/databases/ncbi/nt/nt-39.fna
/databases/ncbi/nt/nt-40.fna
/databases/ncbi/nt/nt-41.fna
/databases/ncbi/nt/nt-42.fna
/databases/ncbi/nt/nt-43.fna
/databases/ncbi/nt/nt-44.fna
/databases/ncbi/nt/nt-45.fna
/databases/ncbi/nt/nt-46.fna
/databases/ncbi/nt/nt-47.fna
/databases/ncbi/nt/nt-48.fna
/databases/ncbi/nt/nt-49.fna
/databases/ncbi/nt/nt-50.fna
/databases/ncbi/nt/nt-51.fna
/databases/ncbi/nt/nt-52.fna
/databases/ncbi/nt/nt-53.fna
/databases/ncbi/nt/nt-54.fna
/databases/ncbi/nt/nt-55.fna
/databases/ncbi/nt/nt-56.fna
/databases/ncbi/nt/nt-57.fna
/databases/ncbi/nt/nt-58.fna
/databases/ncbi/nt/nt-59.fna
/databases/ncbi/nt/nt-60.fna
/databases/ncbi/nt/nt-61.fna
/databases/ncbi/nt/nt-62.fna
/databases/ncbi/nt/nt-63.fna
/databases/ncbi/nt/nt-64.fna
/databases/ncbi/nt/nt-65.fna
/databases/ncbi/nt/nt-66.fna
/databases/ncbi/nt/nt-67.fna
/databases/ncbi/nt/nt-68.fna
/databases/ncbi/nt/nt-69.fna
/databases/ncbi/nt/nt-70.fna
/databases/ncbi/nt/nt-71.fna
/databases/ncbi/nt/nt-72.fna
/databases/ncbi/nt/nt-73.fna
/databases/ncbi/nt/nt-74.fna
```

## NCBI nr Files

| Argument   | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:----------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--nr`       | file path(s) | Space delimited list of paths to ViroMatch's split NCBI nr nucleotide indexed FASTA files. Alternatively, a file with paths to the files, one per line, can be supplied instead, provided the file has a _.fofn_ suffix --- e.g. NR.fofn file.                                                                                |

### Command Line List (nr)

The NCBI nr reference database is too large to pragmatically facilitate direct alignments without considerable computational resources. Therefore, we have split nt into multiple parts for iterative processing. The `--nr` argument points ViroMatch to where the split and indexed nr reference files reside on your system. File paths should be fully qualified and not rely on relative paths.

We may pass these files directly on the command line when running the pipeline, space-delimited. Within the larger ViroMatch command, the `--nr` argument for FASTQ files would look something like this.

```bash
viromatch --nr /databases/ncbi/nr/nr-1.dmnd /databases/ncbi/nr/nr-2.dmnd /databases/ncbi/nr/nr-3.dmnd /databases/ncbi/nr/nr-4.dmnd /databases/ncbi/nr/nr-5.dmnd /databases/ncbi/nr/nr-6.dmnd /databases/ncbi/nr/nr-7.dmnd /databases/ncbi/nr/nr-8.dmnd /databases/ncbi/nr/nr-9.dmnd /databases/ncbi/nr/nr-10.dmnd /databases/ncbi/nr/nr-11.dmnd /databases/ncbi/nr/nr-12.dmnd /databases/ncbi/nr/nr-13.dmnd /databases/ncbi/nr/nr-14.dmnd /databases/ncbi/nr/nr-15.dmnd /databases/ncbi/nr/nr-16.dmnd /databases/ncbi/nr/nr-17.dmnd /databases/ncbi/nr/nr-18.dmnd /databases/ncbi/nr/nr-19.dmnd /databases/ncbi/nr/nr-20.dmnd /databases/ncbi/nr/nr-21.dmnd /databases/ncbi/nr/nr-22.dmnd /databases/ncbi/nr/nr-23.dmnd /databases/ncbi/nr/nr-24.dmnd /databases/ncbi/nr/nr-25.dmnd /databases/ncbi/nr/nr-26.dmnd /databases/ncbi/nr/nr-27.dmnd /databases/ncbi/nr/nr-28.dmnd /databases/ncbi/nr/nr-29.dmnd /databases/ncbi/nr/nr-30.dmnd /databases/ncbi/nr/nr-31.dmnd /databases/ncbi/nr/nr-32.dmnd /databases/ncbi/nr/nr-33.dmnd /databases/ncbi/nr/nr-34.dmnd /databases/ncbi/nr/nr-35.dmnd /databases/ncbi/nr/nr-36.dmnd /databases/ncbi/nr/nr-37.dmnd /databases/ncbi/nr/nr-38.dmnd /databases/ncbi/nr/nr-39.dmnd /databases/ncbi/nr/nr-40.dmnd
```

### File of File Names (nr)

In the above command line example, we passed all of the split and indexed nr database files on the command line as a list. As there are many split files, using this method makes the command line statement hard to read, and invites user error (e.g. accidentally omitting a split file). Therefore it is recommended that you supply the `--nr` argument a file of file names where each line is a fully qualified path to the nt FASTA files.

{{% notice warning %}}
Your file of file names file must end in a `.fofn` suffix.
{{% /notice %}}

Within the larger ViroMatch command, the `--nr` argument for the file of file names would look something like this.

```bash
viromatch --nr /databases/ncbi/nr/nr.fofn
```

The `nr.fofn` file will contain the paths to all of the split NCBI nr files, like so.

```plaintext
/databases/ncbi/nr/nr-1.dmnd
/databases/ncbi/nr/nr-2.dmnd
/databases/ncbi/nr/nr-3.dmnd
/databases/ncbi/nr/nr-4.dmnd
/databases/ncbi/nr/nr-5.dmnd
/databases/ncbi/nr/nr-6.dmnd
/databases/ncbi/nr/nr-7.dmnd
/databases/ncbi/nr/nr-8.dmnd
/databases/ncbi/nr/nr-9.dmnd
/databases/ncbi/nr/nr-10.dmnd
/databases/ncbi/nr/nr-11.dmnd
/databases/ncbi/nr/nr-12.dmnd
/databases/ncbi/nr/nr-13.dmnd
/databases/ncbi/nr/nr-14.dmnd
/databases/ncbi/nr/nr-15.dmnd
/databases/ncbi/nr/nr-16.dmnd
/databases/ncbi/nr/nr-17.dmnd
/databases/ncbi/nr/nr-18.dmnd
/databases/ncbi/nr/nr-19.dmnd
/databases/ncbi/nr/nr-20.dmnd
/databases/ncbi/nr/nr-21.dmnd
/databases/ncbi/nr/nr-22.dmnd
/databases/ncbi/nr/nr-23.dmnd
/databases/ncbi/nr/nr-24.dmnd
/databases/ncbi/nr/nr-25.dmnd
/databases/ncbi/nr/nr-26.dmnd
/databases/ncbi/nr/nr-27.dmnd
/databases/ncbi/nr/nr-28.dmnd
/databases/ncbi/nr/nr-29.dmnd
/databases/ncbi/nr/nr-30.dmnd
/databases/ncbi/nr/nr-31.dmnd
/databases/ncbi/nr/nr-32.dmnd
/databases/ncbi/nr/nr-33.dmnd
/databases/ncbi/nr/nr-34.dmnd
/databases/ncbi/nr/nr-35.dmnd
/databases/ncbi/nr/nr-36.dmnd
/databases/ncbi/nr/nr-37.dmnd
/databases/ncbi/nr/nr-38.dmnd
/databases/ncbi/nr/nr-39.dmnd
/databases/ncbi/nr/nr-40.dmnd
```

## Viralfna File

| Argument   | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:----------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--viralfna` | file path    | Path to ViroMatch's viral identity nucleotide indexed FASTA file. Putative viral identities come from this database prior to extended validation alignments.                                                                                                                                                                |

The `--viralfna` argument points to the path where ViroMatch's viral nucleotide database is installed on your system. File paths should be fully qualified and not rely on relative PATHS.

Within the larger ViroMatch command, the `--viralfna` argument for the viral nucleotide database would look something like this.

```bash
viromatch --viralfna /databases/viral-only/nuc/ncbi_viral.fna
```

Although we are pointing to the FASTA files in the above command, the corresponding indexed files should also be present on your system. For example, `/databases/viral-only/nuc/ncbi_viral.fna` should have the following files located along with the FASTA file.

```plaintext
/databases/viral-only/nuc/ncbi_viral.fna
/databases/viral-only/nuc/ncbi_viral.fna.amb
/databases/viral-only/nuc/ncbi_viral.fna.ann
/databases/viral-only/nuc/ncbi_viral.fna.bwt
/databases/viral-only/nuc/ncbi_viral.fna.pac
/databases/viral-only/nuc/ncbi_viral.fna.sa
```

The viral nucleotide database ViroMatch uses has been formatted in a manner to expedite processing time. Reference sequences have had their associated NCBI taxon ids annotated on each reference's FASTA header. Pre-associating the taxon ids speeds up taxonomy association within the pipeline considerably.

In the following reference example, the taxon id [1868221](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=1868221) can be used to lookup the full lineage for [MK746103.1](https://www.ncbi.nlm.nih.gov/nuccore/MK746103.1) accession id.

```plaintext
>MK746103.1|1868221 Porcine circovirus 3 strain PCV3/CNF/Xinjiang-160/2018, complete genome
TAGTATTACCCGGCACCTCGGAACCCGGATCCACGGAGGTCTGTAGGGAGAAAAAGTGGTATCCCATTATGGATGCTCCG
CACCGTGTGAGTGGATATACCGGGCAGTGGATGATGAAGCGGCCTCGTGTTTTGATGCCGCAGGACGGGGACTGGATAAC
TGAGTTTTTGTGGTGCTACGAGTGTCCTGAAGATAAGGACTTTTATTGTCATCCTATTCTAGGTCCGGAGGGAAAGCCCG
AAACACAGGTGGTGTTTTACGATAAACAACTGGACCCCGACCGAGTGGGAATCTATTGTGGAGTGTGGAGGCAGTATAGC
GAGATACCTTATTATCGGCAAAGAGGTTGGAAAAAGCGGTACCCCACACTTGCAAGGGTACGTGAATTTCAAGAACAAAA
GGCGACTCAGCTCGGTGAAGCGCTTACCCGGATTTGGTCGGGCCCATCTGGAGCCGGCGAGGGGGAGCCACAAAGAGGCC
AGCGAGTATTGCAAGAAAGAGGGGGATTACCTCGAGATTGGCGAAGATTCCTCTTCGGGTACCAGATCGGATCTTCAAGC
AGCAGCTCGGATTCTGACGGAGACGGCGGGAAATCTGACTGAAGTTGCGGAGAAGATGCCTGCAGTATTTATACGCTATG
GGCGGGGTTTGCGTGATTTTTGCGGGGTGATGGGGTTGGGTAAACCGCGTGATTTTAAAACTGAAGTTTATGTTTTTATT
GGTCCTCCAGGATGCGGGAAAACGCGGGAAGCTTGTGCGGATGCGGCTGCGCGGGAATTGCAGTTGTATTTCAAGCCACG
GGGGCCTTGGTGGGATGGTTATAATGGGGAGGGTGCTGTTATTTTGGATGATTTTTATGGGTGGGTTCCATTTGATGAAT
TGCTGAGAATTGGGGACAGGTACCCTCTGAGGGTTCCTGTTAAGGGTGGGTTTGTTAATTTTGTGGCTAAGGTATTATAT
ATTACTAGTAATGTTGTACCGGAGGAGTGGTATTCATCGGAGAATATTCGTGGAAAGTTGGAGGCCTTGTTTAGGAGGTT
CACTAAGGTTGTTTGTTGGGGGGAGGGGGGGGTAAAGAAAGACATGGAGACAGTGTATCCAATAAACTATTGATTTTATT
TGCACTTGTGTACAATTATTGCGTTGGGGTGGGGGTATTTATTGGGAGGGTGGGTGGGCAGCCCCCTAGCCACGGCTTGT
CGCCCCCACCGAAGCATGTGGGGGATGGGGTCCCCACATGCGAGGGCGTTTACCTGTGCCCGCACCCGAAGCGCAGCGGG
AGCGCGCGCGAGGGGACACGGCTTGTCGCCACCGGAGGGGTCAGATTTATATTTATTGTCACTTAGAGAACGGACTTGTA
ACGAATCCAAACTTCTTTGGTGCCGTAGAAGTCTGTCATTCCAGTTTTTTCCGGGACATAAATGCTCCAAAGCAGTGCTC
CCCATTGAACGGTGGGGTCATATGTGTTGAGCCATGGGGTGGGTCTGGAGAAAAAGAAGAGGCTTTGTCCTGGGTGAGTG
CTGGTAGTTCCCGCCAGAATTGGTTTGGGGGTGAAGTAAAGGCTGTGTTTTCTTTTAGAAGTCATAACTTTACGAGTGGA
ACTTTCCGCATAAGGGTCGTCTTGGAGCCAAGTGTTTGTGGTCCAGGCGCCGTCTAGATCTATGGCTGTGTGCCCGAACA
TAGTTTTTGTTTGCTGAGCCGGAGAAATTACAGGGCTGAGTGTAACTTTCATCTTTAGTATCTTATAATATTCAAAGGTA
ATTGCAGTTTCCCATTCGTTTAGGCGGGTAATGAAGTGGTTGGCGTGCCAGGGCTTGTTATTCTGAGGGGTTCCAACGGA
TATGACGTTCATGGTGGAGTATTTCTTTGTGTAGTATGTGCCAGCTGTGGGCCTCCTAATGAATAGTCTTCTTCTGGCAT
AGCGCCTTCTGTGGCGTCGTCGTCTCCTTGGGCGGGGTCTTCTTCTGAATATAGCTCTGTGTCTCATTTTGGTGCCGGGC
```
## Viralfaa File

| Argument   | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:----------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--viralfaa` | file path    | Path to ViroMatch's viral identity translated nucleotide indexed FASTA file. Putative viral identities come from this database prior to extended validation alignments.                                                                                                                                                     |

The `--viralfaa` argument points to the path where ViroMatch's viral translated nucleotide database is installed on your system. File paths should be fully qualified and not rely on relative paths.

Within the larger ViroMatch command, the `--viralfaa` argument for the viral nucleotide database would look something like this.

```bash
viromatch --viralfna /databases/viral-only/trans_nuc/ncbi_viral.dmnd
```

The translated viral nucleotide database ViroMatch uses is the exact same reference used in the `--viralfna`, but has been six-frame translated and indexed for translated alignments.

The translated viral nucleotide database ViroMatch uses has been formatted in a manner to expedite processing time. Reference sequences have had their associated NCBI taxon ids annotated on each reference's FASTA header. Pre-associating the taxon ids speeds up taxonomy association within the pipeline considerably.

In the following reference example, the taxon id [1868221](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=1868221) can be used to lookup the full lineage for [MK746103.1](https://www.ncbi.nlm.nih.gov/nuccore/MK746103.1) accession id. Also, note there are now six entries due to six-frame translation.

```plaintext
>MK746103.1|1868221|7_1 Porcine circovirus 3 strain PCV3/CNF/Xinjiang-160/2018, complete genome
*YYPAPRNPDPRRSVGRKSGIPLWMLRTV*VDIPGSG**SGLVF*CRRTGTG*LSFCGAT
SVLKIRTFIVILF*VRRESPKHRWCFTINNWTPTEWESIVECGGSIARYLIIGKEVGKSG
TPHLQGYVNFKNKRRLSSVKRLPGFGRAHLEPARGSHKEASEYCKKEGDYLEIGEDSSSG
TRSDLQAAARILTETAGNLTEVAEKMPAVFIRYGRGLRDFCGVMGLGKPRDFKTEVYVFI
GPPGCGKTREACADAAARELQLYFKPRGPWWDGYNGEGAVILDDFYGWVPFDELLRIGDR
YPLRVPVKGGFVNFVAKVLYITSNVVPEEWYSSENIRGKLEALFRRFTKVVCWGEGGVKK
DMETVYPINY*FYLHLCTIIALGWGYLLGGWVGSPLATACRPHRSMWGMGSPHARAFTCA
RTRSAAGARARGHGLSPPEGSDLYLLSLRERTCNESKLLWCRRSLSFQFFPGHKCSKAVL
PIERWGHMC*AMGWVWRKRRGFVLGECW*FPPELVWG*SKGCVFF*KS*LYEWNFPHKGR
LGAKCLWSRRRLDLWLCART*FLFAEPEKLQG*V*LSSLVSYNIQR*LQFPIRLGG**SG
WRARACYSEGFQRI*RSWWSISLCSMCQLWAS**IVFFWHSAFCGVVVSLGGVFF*I*LC
VSFWCRA
>MK746103.1|1868221|7_2 Porcine circovirus 3 strain PCV3/CNF/Xinjiang-160/2018, complete genome
SITRHLGTRIHGGL*GEKVVSHYGCSAPCEWIYRAVDDEAASCFDAAGRGLDN*VFVVLR
VS*R*GLLLSSYSRSGGKARNTGGVLR*TTGPRPSGNLLWSVEAV*RDTLLSAKRLEKAV
PHTCKGT*ISRTKGDSAR*SAYPDLVGPIWSRRGGATKRPASIARKRGITSRLAKIPLRV
PDRIFKQQLGF*RRRREI*LKLRRRCLQYLYAMGGVCVIFAG*WGWVNRVILKLKFMFLL
VLQDAGKRGKLVRMRLRGNCSCISSHGGLGGMVIMGRVLLFWMIFMGGFHLMNC*ELGTG
TL*GFLLRVGLLILWLRYYILLVMLYRRSGIHRRIFVESWRPCLGGSLRLFVGGRGG*RK
TWRQCIQ*TIDFICTCVQLLRWGGGIYWEGGWAAP*PRLVAPTEACGGWGPHMRGRLPVP
APEAQRERARGDTACRHRRGQIYIYCHLENGLVTNPNFFGAVEVCHSSFFRDINAPKQCS
PLNGGVICVEPWGGSGEKEEALSWVSAGSSRQNWFGGEVKAVFSFRSHNFTSGTFRIRVV
LEPSVCGPGAV*IYGCVPEHSFCLLSRRNYRAECNFHL*YLIIFKGNCSFPFV*AGNEVV
GVPGLVILRGSNGYDVHGGVFLCVVCASCGPPNE*SSSGIAPSVASSSPWAGSSSEYSSV
SHFGAG
>MK746103.1|1868221|7_3 Porcine circovirus 3 strain PCV3/CNF/Xinjiang-160/2018, complete genome
VLPGTSEPGSTEVCREKKWYPIMDAPHRVSGYTGQWMMKRPRVLMPQDGDWITEFLWCYE
CPEDKDFYCHPILGPEGKPETQVVFYDKQLDPDRVGIYCGVWRQYSEIPYYRQRGWKKRY
PTLARVREFQEQKATQLGEALTRIWSGPSGAGEGEPQRGQRVLQERGGLPRDWRRFLFGY
QIGSSSSSSDSDGDGGKSD*SCGEDACSIYTLWAGFA*FLRGDGVG*TA*F*N*SLCFYW
SSRMRENAGSLCGCGCAGIAVVFQATGALVGWL*WGGCCYFG*FLWVGSI**IAENWGQV
PSEGSC*GWVC*FCG*GIIYY**CCTGGVVFIGEYSWKVGGLV*EVH*GCLLGGGGGKER
HGDSVSNKLLILFALVYNYCVGVGVFIGRVGGQPPSHGLSPPPKHVGDGVPTCEGVYLCP
HPKRSGSAREGTRLVATGGVRFIFIVT*RTDL*RIQTSLVP*KSVIPVFSGT*MLQSSAP
H*TVGSYVLSHGVGLEKKKRLCPG*VLVVPARIGLGVK*RLCFLLEVITLRVELSA*GSS
WSQVFVVQAPSRSMAVCPNIVFVC*AGEITGLSVTFIFSIL*YSKVIAVSHSFRRVMKWL
ACQGLLF*GVPTDMTFMVEYFFV*YVPAVGLLMNSLLLA*RLLWRRRLLGRGLLLNIALC
LILVPG
>MK746103.1|1868221|7_4 Porcine circovirus 3 strain PCV3/CNF/Xinjiang-160/2018, complete genome
PAPK*DTELYSEEDPAQGDDDATEGAMPEEDYSLGGPQLAHTTQRNTPP*TSYPLEPLRI
TSPGTPTTSLPA*TNGKLQLPLNIIRY*R*KLHSAL*FLRLSKQKLCSGTQP*I*TAPGP
QTLGSKTTLMRKVPLVKL*LLKENTAFTSPPNQFWRELPALTQDKASSFSPDPPHGSTHM
TPPFNGEHCFGAFMSRKKLE*QTSTAPKKFGFVTSPFSK*Q*I*I*PLRWRQAVSPRARS
RCASGAGTGKRPRMWGPHPPHASVGATSRG*GAAHPPSQ*IPPPQRNNCTQVQIKSIVYW
IHCLHVFLYPPLPPTNNLSEPPKQGLQLSTNILR*IPLLRYNITSNI*YLSHKINKPTLN
RNPQRVPVPNSQQFIKWNPPIKIIQNNSTLPIITIPPRPPWLEIQLQFPRSRIRTSFPRF
PASWRTNKNINFSFKITRFTQPHHPAKITQTPPIAYKYCRHLLRNFSQISRRLRQNPSCC
LKIRSGTRRGIFANLEVIPLFLAILAGLFVAPPRRLQMGPTKSG*ALHRAESPFVLEIHV
PLQVWGTAFSNLFADNKVSRYTASTLHNRFPLGRGPVVYRKTPPVFRAFPPDLE*DDNKS
PYLQDTRSTTKTQLSSPRPAASKHEAASSSTARYIHSHGAEHP*WDTTFSPYRPPWIRVP
RCRVIL
>MK746103.1|1868221|7_5 Porcine circovirus 3 strain PCV3/CNF/Xinjiang-160/2018, complete genome
PGTKMRHRAIFRRRPRPRRRRRHRRRYARRRLFIRRPTAGTYYTKKYSTMNVISVGTPQN
NKPWHANHFITRLNEWETAITFEYYKILKMKVTLSPVISPAQQTKTMFGHTAIDLDGAWT
TNTWLQDDPYAESSTRKVMTSKRKHSLYFTPKPILAGTTSTHPGQSLFFFSRPTPWLNTY
DPTVQWGALLWSIYVPEKTGMTDFYGTKEVWIRYKSVL*VTININLTPPVATSRVPSRAL
PLRFGCGHR*TPSHVGTPSPTCFGGGDKPWLGGCPPTLPINTPTPTQ*LYTSANKINSLL
DTLSPCLSLPPPPPNKQP**TS*TRPPTFHEYSPMNTTPPVQHY**YIIP*PQN*QTHP*
QEPSEGTCPQFSAIHQMEPTHKNHPK*QHPPHYNHPTKAPVA*NTTAIPAQPHPHKLPAF
SRILEDQ*KHKLQF*NHAVYPTPSPRKNHANPAHSV*ILQASSPQLQSDFPPSPSESELL
LEDPIWYPKRNLRQSRGNPPLSCNTRWPLCGSPSPAPDGPDQIRVSASPS*VAFCS*NSR
TLASVGYRFFQPLCR**GISLYCLHTPQ*IPTRSGSSCLS*NTTCVSGFPSGPRIG*Q*K
SLSSGHS*HHKNSVIQSPSCGIKTRGRFIIHCPVYPLTRCGASIMGYHFFSLQTSVDPGS
EVPGNT
>MK746103.1|1868221|7_6 Porcine circovirus 3 strain PCV3/CNF/Xinjiang-160/2018, complete genome
ARHQNETQSYIQKKTPPKETTTPQKALCQKKTIH*EAHSWHILHKEILHHERHIRWNPSE
*QALARQPLHYPPKRMGNCNYL*IL*DTKDESYTQPCNFSGSANKNYVRAHSHRSRRRLD
HKHLAPRRPLCGKFHS*SYDF*KKTQPLLHPQTNSGGNYQHSPRTKPLLFLQTHPMAQHI
*PHRSMGSTALEHLCPGKNWNDRLLRHQRSLDSLQVRSLSDNKYKSDPSGGDKPCPLARA
PAALRVRAQVNALACGDPIPHMLRWGRQAVARGLPTHPPNKYPHPNAIIVHKCK*NQ*FI
GYTVSMSFFTPPSPQQTTLVNLLNKASNFPRIFSDEYHSSGTTLLVIYNTLATKLTNPPL
TGTLRGYLSPILSNSSNGTHP*KSSKITAPSPL*PSHQGPRGLKYNCNSRAAASAQASRV
FPHPGGPIKT*TSVLKSRGLPNPITPQKSRKPRP*RINTAGIFSATSVRFPAVSVRIRAA
A*RSDLVPEEESSPISR*SPSFLQYSLASLWLPLAGSRWARPNPGKRFTELSRLLFLKFT
YPCKCGVPLFPTSLPIIRYLAILPPHSTIDSHSVGVQLFIVKHHLCFGLSLRT*NRMTIK
VLIFRTLVAPQKLSYPVPVLRHQNTRPLHHPLPGISTHTVRSIHNGIPLFLPTDLRGSGF
RGAG*Y
```

## Host File

| Argument | Type      | Description                                                                                                                                  |
|:--------:|:---------:|----------------------------------------------------------------------------------------------------------------------------------------------|
| `--host`   | file path | Path to ViroMatch's host indexed FASTA file used for host screening. By default we provide an indexed version of the human reference genome. |

The ViroMatch pipeline performs host screening --- i.e. filters out reads based on identity to a reference host genome. All reads are host screened prior to viral (viralfna/viralfaa) assessment and NCBI nt/nr validation. If one read in a read-pair maps to a virus and the other maps to the host (e.g. an integrated virus), we want to remove the host read but not the viral hit; therefore, reads are aligned in single-end mode to the host genome.

The `--host` argument points to the path where ViroMatch's host genome is installed on your system. ViroMatch provides an indexed version of the human genome.

Within the larger ViroMatch command, the `--host` argument for the host reference would look something like this.

```bash
viromatch --host /databases/host/GRCh38_latest_genomic.fna
```

Although we are pointing to the FASTA file in the above command, the corresponding indexed files should also be present on your system. For example, `/databases/host/GRCh38_latest_genomic.fna` should have the following files located along with the FASTA file.

```plaintext
/databases/host/GRCh38_latest_genomic.fna
/databases/host/GRCh38_latest_genomic.fna.amb
/databases/host/GRCh38_latest_genomic.fna.ann
/databases/host/GRCh38_latest_genomic.fna.bwt
/databases/host/GRCh38_latest_genomic.fna.pac
/databases/host/GRCh38_latest_genomic.fna.sa
```

If you are not screening human but rather a different host genome, you will need to index the reference genome FASTA file yourself using the version of [BWA-MEM](http://bio-bwa.sourceforge.net/) included in the ViroMatch Docker image.

First, create an interactive session using the ViroMatch Docker image. You will want to map the volume that contains your reference FASTA so Docker can see it. On your computer, change directory to where your reference FASTA file resides, then open the interactive session like so.

```bash
docker \
container \
run \
-it \
-v ${PWD}:/reference \
twylie/viromatch:latest \
zsh
```

Once inside the interactive session, change to the directory where the reference FASTA file resides and index the reference FASTA using BWA.

```bash
cd /reference
bwa index example_reference.fasta
```

Finally, you will pass `--host` the full path to the newly indexed reference FASTA file.

{{% notice note %}}
If you are going to index your own host genome, make sure to use the version of BWA in the ViroMatch Docker image, as that is the version used for mapping within the pipeline. Using different versions of BWA to index and map can result in odd behavior.
{{% /notice %}}

## Adaptor File

| Argument   | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:----------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--adaptor`  | file path    | Path to a file with adapter sequences, one per line, used for read trimming.                                                                                                                                                                                                                                                |

The `--adaptor` argument takes a qualified path to an adaptor file which will be used during the trimming phase of ViroMatch.

Within the larger ViroMatch command, the `--adaptor` argument for the adaptor file would look something like this.

```bash
viromatch --adaptor /databases/adaptor/adaptor.fqtrim
```

The adaptor file is simply a text file listing the adaptor sequences you wish to use for trimming.

```plaintext
AGATCGGAAGAGCACA
TGCTCTTCCGATCT
GTTTCCCAGTCACGATA
TATCGTGACTGGGAAAC
```

ViroMatch uses `fqtrim` for trimming and the `--adaptor` file is passed directly to `fqtrim`. To learn more about `fqtrim` and its adaptor file format, take a look [here](https://ccb.jhu.edu/software/fqtrim/), specifically the `-f <filename>` usage statement.

{{% notice note %}}
You will need to replace the adaptor file included in the Globus database download with a version specific for your sequence data and how it was produced --- e.g. library prep, adaptors, etc.
{{% /notice %}}

## Taxid File

| Argument   | Type         | Description                                                                                                                                                                                                                                                                                                                 |
|:----------:|:------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--taxid`    | file path    | Path to ViroMatch's taxonomy database. This file provides NCBI-based taxonomy and lineages based on NCBI taxon ids.                                                                                                                                                                                                         |

The `--taxid` argument takes a qualified path to ViroMatch's taxonomy file which will be used to define taxonomies for reads.

Within the larger ViroMatch command, the `--taxid` argument for the adaptor file would look something like this.

```bash
viromatch --taxid /databases/taxonomy/taxonomy.tsv
```

The `--taxid` file is a tab-delimited file that has mappings among NCBI taxon ids. Given a taxon id, we may recursively walk through all associated ids and construct the lineage for a given taxon id.

For example, take the following refernce genome:

[Pseudomonas sp. SNU WT1 chromosome, complete genome](https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP035952.1)

which has `2518644` as the taxon id. Resolving this taxon id through the `taxonomy.tsv` file gives us the full lineage of this reference genome.

```plaintext
cellular organisms --> Bacteria --> Proteobacteria --> Gammaproteobacteria --> Pseudomonadales --> Pseudomonadaceae --> Pseudomonas --> unclassified Pseudomonas --> Pseudomonas sp. SNU WT1
```

ViroMatch performs automatic taxonomic lookup for all candidate viral reads throughout the pipeline.

## Wustlconfig File

{{% notice warning %}}
These options are only available to those running ViroMatch at Washington University School of Medicine through the **compute1** high performance computing server.
{{% /notice %}}

| Argument      | Type      | Description                                                                                                                                                             |
|:-------------:|:---------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--wustlconfig` | file path | Path to a YAML configuration file used for WUSTL LSF job parallel processing. Variables provided in this file are used for LSF job submission configuration. |

We provide `--wustlconfig` the full path to a YAML configuration file.

Within the larger ViroMatch command, the `--wustlconfig` argument for the YAML file would look something like this.

```bash
viromatch --wustlconfig run.yaml
```

The configuration file contains several parameters related to running parallel jobs on the WashU **compute1** server. A single configuration file may be used to launch many instances of the ViroMatch pipeline, provided all of the sequence files are within directories covered by the Docker volumes list. A typical configuration file looks like this.

```bash
docker:
  image: 'twylie/viromatch:latest'
  volumes:
    - '/storage1/fs1/tnwylie_lab/Active/viroMatchDatabases:/storage1/fs1/tnwylie_lab/Active/viroMatchDatabases'
    - '/storage1/fs1/twylie/Active/redoPP:/storage1/fs1/twylie/Active/redoPP'
    - '/storage1/fs1/twylie/RAW_DATA:/storage1/fs1/twylie/RAW_DATA'
lsf:
  memory: '16G'
  cores: '150'
  local cores: '1'
  compute group: 'compute-kwylie'
  queue: 'general'
  latency wait: '100'
  restart times: '3'
  ignore hosts:
    - 'compute1-exec-67.ris.wustl.edu'
    - 'compute1-exec-117.ris.wustl.edu'
    - 'compute1-exec-102.ris.wustl.edu'
```

The configuration file is used only for sub-process (children) jobs submitted to LSF from the parent ViroMatch job.

| Parameter         | Type     | Description                                                                                                           |
|:-----------------:|:--------:|-----------------------------------------------------------------------------------------------------------------------|
| docker/image      | Required | Name of the ViroMatch Docker image to use for sub-processing.                                                         |
| docker/volumes    | Required | A list of all of the Docker volume mappings that will be needed for sub-processing.                                   |
| lsf/memory        | Required | Request the minimum amount of memory required for sub-processing.                                                     |
| lsf/cores         | Required | How many cores to use at one time for parallel sub-processing.                                                        |
| lsf/local cores   | Required | How many local cores to address per each individual LSF sub-process job.                                              |
| lsf/compute group | Required | LSF compute group name.                                                                                               |
| lsf/queue         | Required | LSF submission queue name.                                                                                            |
| lsf/latency wait  | Required | Time in seconds for how long Snakemake should wait for latent files. Useful for high latency cluster systems.         |
| lsf/restart times | Required | How many times Snakemake should attempt to restart a failed sub-process.                                              |
| lsf/ignore hosts  | Optional | Some LSF execution nodes may be problematic. This list tells LSF to ignore these hosts when submitting sub-processes. |
