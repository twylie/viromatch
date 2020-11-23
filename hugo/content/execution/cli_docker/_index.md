---
title: "Command Line Docker"
date: 2020-11-11T00:02:01-06:00
draft: false
weight: 3
---

## Command Line Docker Execution

We can run ViroMatch from an interactive container as a [two-step process](https://twylie.github.io/viromatch/execution/interactive_docker/). Here, we outline how to do both steps at once.

Let's take a look at the execution command and then we'll breakdown what's going on. From a terminal, we would type the following to call the Docker container and run ViroMatch.

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

All of the arguments are the same as detailed in [Interactive Docker Session](https://twylie.github.io/viromatch/execution/interactive_docker/#interactive-docker-sessions), but we've essentially combined the two steps. Running the above command still produces standard output as the pipeline progresses, but is now displayed in our terminal shell and not an interactive Docker shell. Once the pipeline has finished, Docker will discretely terminate the underlying container shell.

{{% notice tip %}}
It is also possible to execute a Docker job from the command line and run it completely in the background. Just add the `-d` switch to your docker command to detach the job. You will be given a job ID to monitor the job. This is the preferred method for long-running ViroMatch jobs on a local system.
{{% /notice %}}
