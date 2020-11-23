---
title: "Installation and Pipeline Execution"
date: 2020-11-10T21:53:53-06:00
draft: false
---

## Quick Start

While the ViroMatch code base is hosted at [https://github.com/twylie/viromatch](https://github.com/twylie/viromatch), we only support using the official Docker image. Instructions follow for installing and running ViroMatch using Docker.

------------

### Step 1: Input Sequences

Gather your input sequences for processing. You may provide either (1) a single input unmapped BAM (uBAM) file or (2) paired FASTQ files. If paired FASTQ files are provided, the R1-file should be first followed by the R2-file, space delimited.

------------

### Step 2: Download and Install Docker Desktop

The ViroMatch pipeline, and all of its underlying code dependencies, are provided as a Docker image. Once you've installed Docker Desktop on your computer and have downloaded the ViroMatch Docker image, you will be able to run the pipeline containers.

{{< button href="https://www.docker.com/get-started" >}}Download Docker{{< /button >}}

------------

### Step 3: Download ViroMatch Docker Image

Once you've installed Docker Desktop (and the Docker service is running on your system) you will be able to download and run the ViroMatch Docker image. Specifically, you want the `viromatch:latest` image.

{{< button href="https://hub.docker.com/r/twylie/viromatch/tags" >}}Download ViroMatch{{< /button >}}

------------

### Step 4: Download Required ViroMatch Databases

ViroMatch requires several specific databases (`--host`, `--viralfna`, `--viralfaa`, `--nt`, `--nr`) for processing. These databases have been pre-compiled and are available for download. 

Be aware the databases are quite large in cumulative size (~860 GB).

Databases are being hosting through [Globus Connect](https://www.globus.org/globus-connect). Globus Connect is free to install and use for users at non-profit research and education institutions. You will need to login to Globus to access the databases.

{{< button href="https://app.globus.org/file-manager?origin_id=b578a7a6-2cf1-11eb-b16b-0ee0d5d9299f&origin_path=%2F" >}}Download ViroMatch Databases Using Globus{{< /button >}}

<!-- We will be pointing to GLobus for database hosting. Update later. -->

------------

### Step 5: Run ViroMatch

We can run ViroMatch via a Docker container using the command line. From a terminal, we would type the following to call the Docker container and run ViroMatch. Arguments will need to reflect your file paths and personal settings in order to run properly on your system. 

```bash
docker \
container run \
-itd \
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
--taxid /taxonomy/taxonomy.tsv
```

------------

### Step 6: ViroMatch Report Review

Upon completion, ViroMatch will provide reports detailing viral taxonomic classification and quantification. All report files are at the top-level of the `--outdir` directory provided in the execution command.

Results:

```plaintext
REPORT.nuc_ambiguous_counts.txt
REPORT.nuc_counts.txt
REPORT.trans_nuc_ambiguous_counts.txt
REPORT.trans_nuc_counts.txt
```

------------
