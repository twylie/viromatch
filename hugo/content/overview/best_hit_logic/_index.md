---
title: "Best Hit Logic"
date: 2020-11-11T00:34:28-06:00
draft: false
weight: 6
---

## Determining a Read's Best Hit

As outlined in [NCBI nt Files](https://twylie.github.io/viromatch/overview/file_types/#ncbi-nt-files) and [NCBI nr Files](https://twylie.github.io/viromatch/overview/file_types/#ncbi-nr-files), the NCBI nt and nr reference databases are too large to index for alignment, so we split nt/nr into multiple indexed reference databases for independent alignment. Therefore, a candidate read will be aligned to _all_ of the split nt or nr databases and a best hit will be determined during the best hit logic portion of the pipeline. While a read may have a good hit to one of the split reference databases, it may have a better or equally good hit to another split reference database.

Having multiple hits per read requires choosing a single best, representative hit for a read. Also, it is during this validation step that a read may have a better non-viral hit as compared to the initial viral-only database hit that flagged the read as a candidate for viral identity. All of the hits for a given read are evaluated at the same time in a _read block_. A read block is a list of alignment report lines, all having the same read id. In this way, we evaluate a smaller chunk of alignments at any one time. Although the alignment formats for nt and nr hits are different, the concept is the same. A read will be given the status of PASS or FAIL based on the underlying hits being evaluated. See [Failure Codes](https://twylie.github.io/viromatch/overview/reports/#failure-codes) for more details on read pass/fail evaluation.

The general logic for choosing a best hit for a read follows.

1. In the first evaluation for nucleotide alignments, we fail an entire read block (and the read) if the block's best hit has a percent identity variance (pidv) score that is greater than `--pid`. For translated nucleotide alignments, we do not enforce a minimum percent identity score.

2. If the read block passes step #1 above, we then evaluate all of the hits in the read block. If a hit matches _unknown_ or _other sequences_ taxonomy, we ignore the hit, but quantify and report how many hits are affected. Other hits in the read block with known taxonomy are still evaluated.

3. The remaining hits are then placed into one of the following categories: 1) best hit score with viral-identity; 2) best hit score with non-viral-identity; 3) best hit neighbor with viral-identity; 4) best hit neighbor with non-viral-identity; 5) secondary, non-neighbor hits with any taxonomy.

4. We pool the best hit score with non-viral-identity and best hit neighbor with non-viral-identity hits and evaluate them. If there are any hits (>0 hits) in this pool, we fail the read block (and the read) because there are significant non-viral hits and the best viral-identity hit is therefore ambiguous. Neighbor reads are those hits that are within proximal range (`--pidprox` or `--bitprox`) to the best hit score.

5. If the read block passes step #4 above, we continue on with more hit evaluations. The best hit neighbor with viral-identity category was only used in separating viral and non-viral neighboring hits for evaluation. We make a note that these hits are viral neighbors in the sanity log files, but we fail these hits as they are not best hit candidates. We continue to evaluate the remaining hits in the read block.

6. The secondary, non-neighbor hits with any taxonomy are too distant from the best and neighboring hits, so these hits are failed. We continue to evaluate the remaining hits in the read block.

7. The remaining hit category in the read block is the best hit score with viral-identity hits. This may be a single hit or there may be multiple equally-scored hits in this pool of hits; however, they will all have viral taxonomy and be candidates for the best viral hit. If the hits are tied, a randomly selected representative hit will be chosen as the best viral hit. If there is a single best viral hit, it will be chosen by default.

8. At this point, the read block has been assessed and a _pass_ or _fail_ status is awarded to the parent read. A _pass_ means that a best viral-identity hit was chosen for the read and the read will be counted in the taxonomy/quantification reports. A _fail_ means that no significant viral-identity hit was chosen for the read and the read will not be included in the taxonomy/quantification reports.

9. The process continues (the next read block in the hits file is evaluated) iteratively until all of the reads and their hits have been evaluated.

For examples of evaluated reads, as well as a table of all possible pass/fail codes, see [Sanity files](https://twylie.github.io/viromatch/overview/reports/#sanity-files).

