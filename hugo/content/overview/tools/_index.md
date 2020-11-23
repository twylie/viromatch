---
title: "Third-Party Tools"
date: 2020-11-13T15:29:39-06:00
draft: False
weight: 4
---

## Tools Used by ViroMatch

ViroMatch relies on third-party bioinformatics tools at various points in the pipeline. The table below lists the major third-party tools and how they are used.

| Software    | Version              | License                                                                      | Link                                                                         | ViroMatch Usage                                                        |
| :---------: | :-------:            | :---:                                                                        | ------                                                                       | -------                                                                |
| **BWA**       | 0.7.17-r1198-dirty   | GNU General Public License version 3.0 (GPLv3), MIT License                  | [http://bio-bwa.sourceforge.net/](http://bio-bwa.sourceforge.net/)           | Used for nucleotide alignments.                                        |
| **Biopython** | 1.78                 | Biopython License Agreement                                                  | [https://biopython.org/](https://biopython.org/)                             | Used for FASTA/FASTQ handling.                                         |
| **Diamond**   | diamond v0.9.29.130  | GPL-3.0 License                                                              | [http://www.diamondsearch.org/](http://www.diamondsearch.org/)               | Used for translated nucleotide alignments.                             |
| **Pandas**    | 1.1.2                | BSD-licensed library                                                         | [https://pandas.pydata.org/](https://pandas.pydata.org/)                     | Pandas used for data handling and reporting.                           |
| **Python**    | Python 3.7.5         | Python License Agreement (GPL-compatible)                                    | [https://www.python.org/](https://www.python.org/)                           | ViroMatch is written in Python.                                        |
| **Samtools**  | samtools 1.9         | The MIT License                                                              | [http://www.htslib.org/](http://www.htslib.org/)                             | Samtools is used for SAM/BAM handling.                                 |
| **Snakemake** | 5.25.0               | The MIT License                                                              | [https://snakemake.readthedocs.io/](https://snakemake.readthedocs.io/)       | Snakemake is used for pipeline organization and execution.             |
| **fqtrim**    | v0.9.7               | Artistic License 2.0                                                         | [https://ccb.jhu.edu/software/fqtrim/](https://ccb.jhu.edu/software/fqtrim/) | Used for adaptor and qaulity trimming; also, short read filtering.     |
| **seqtk**     | 1.3-r115-dirty       | The MIT License                                                              | [https://github.com/lh3/seqtk](https://github.com/lh3/seqtk)                 | The seqtk package is used to extract specific reads from FASTQ files.  |
| **vsearch**   | v2.15.0_linux_x86_64 | GNU General Public License version 3 or BSD 2-clause license (dual-licensed) | [https://github.com/torognes/vsearch](https://github.com/torognes/vsearch)   | The vsearch package is used for low-complexity read masking/filtering. |
