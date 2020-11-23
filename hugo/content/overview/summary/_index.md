---
title: "Pipeline Summary"
date: 2020-11-11T11:28:11-06:00
draft: false
weight: 1
---


## Abstract

Next-generation sequencing (NGS) is a powerful tool for detecting viruses. However, automated interpretation of metagenomic sequences has proven challenging for virus classification due the heterogeneous nature of virus genomics. While software pipelines exist for viral detection, many rely on prohibitive memory and CPU requirements and are not meant for localized computing; others rely on perfect _k_-mer hashing identities that lack sensitivity. We have produced software in the form of an automated pipeline, called ViroMatch, that takes raw sequencing reads as input and identifies/quantifies viral taxonomy; additionally, we have targeted specific viral species for extended analyses (e.g. variant interpretation). The pipeline is written in Python and is mediated as a DAG (Directed Acyclic Graph) workflow using [Snakemake](https://snakemake.readthedocs.io/en/stable/), and supports single or multi-core processing. It can perform iterative nucleotide ([BWA-MEM](http://bio-bwa.sourceforge.net/)) and translated nucleotide ([Diamond](http://www.diamondsearch.org/index.php)) sequence alignments for all known viral reference genomes and can assign viral taxonomy with quantified results. Additionally, we have pre-compiled local viral sequences from [NCBI](https://www.ncbi.nlm.nih.gov/) (RefSeq, nt & nr) and associated annotation. For select viruses (e.g. HSV, CMV, EBV), we have implemented downstream viral interpretation steps (e.g. sub-typing, drug resistance), which involves SNV (single nucleotide variant) characterization comparison to known variants we have culled from literature and existing databases. Our databases and companion tools are extensible, and we anticipate periodic updates based on new virus data. ViroMatch is a staple on our work involving genomics-based detection/evaluation of viruses, and we anticipate this resource will be of great interest to others in the scientific and medical community. We provide a [Docker](https://www.docker.com/) image (DockerHub) for ViroMatch, so users will not have to install dependencies.

>T.N. Wylie, K.M. Wylie.      
>"ViroMatch: a computational pipeline for detection of viral reads from complex metagenomic data."     
>ASM Conference on Rapid Applied Microbial Next-Generation Sequencing and Bioinformatic Pipelines     
>December 7--11, 2020.
