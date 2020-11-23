---
title: "Databases"
date: 2020-11-22T13:24:32-06:00
draft: false
weight: 4
---

## Downloading Required ViroMatch Databases

As outlined in [Input File Types](https://twylie.github.io/viromatch/overview/file_types/), you will need to supply required reference genome databases in order to run the ViroMatch pipeline. These resources have already been indexed and are ready for processing, but you will need to download all of the files first. 

We provide file access and transfer through [Globus Connenct](https://www.globus.org/globus-connect).

_What is Globus?_

> Globus Connect enables your system to use the Globus file transfer and sharing service. It makes it simple to create a Globus endpoint on practically any system, from a personal laptop to a national supercomputer. Globus Connect is free to install and use for users at non-profit research and education institutions.
> Globus Connect Versions (Source: [Globus Connect](https://www.globus.org/globus-connect))

[Globus Connect Personal](https://www.globus.org/globus-connect-personal) is designed for use by a single user on a personal machine and is free for users at non-profit research and education institutions. Once Globus Connect Personal is installed and you are logged in, you may click on the link below to download the ViroMatch databases.

{{< button href="https://app.globus.org/file-manager?origin_id=b578a7a6-2cf1-11eb-b16b-0ee0d5d9299f&origin_path=%2F" >}}Download ViroMatch Databases Using Globus{{< /button >}}

The main sub-directories for download are listed below, organized by database type. For detailed information on each sub-directory's files, see the corresponding Input File Type.

| Sub-Directory             | Input File Type                                                                        |
| :-----------------------: | -----------------                                                                      |
| `adaptor/`                | [Adaptor File](https://twylie.github.io/viromatch/overview/file_types/#adaptor-file)   |
| `host/`                   | [Host File](https://twylie.github.io/viromatch/overview/file_types/#host-file)         |
| `ncbi/nr/`                | [NCBI nr Files](https://twylie.github.io/viromatch/overview/file_types/#ncbi-nr-files) |
| `ncbi/nt/`                | [NCBI nt Files](https://twylie.github.io/viromatch/overview/file_types/#ncbi-nt-files) |
| `taxonomy/`               | [Taxid File](https://twylie.github.io/viromatch/overview/file_types/#taxid-file)       |
| `viral-only/nuc/`         | [Viralfna File](https://twylie.github.io/viromatch/overview/file_types/#viralfna-file) |
| `viral-only/trans_nuc/`   | [Viralfaa File](https://twylie.github.io/viromatch/overview/file_types/#viralfaa-file) |

You will need all of the underlying database files in these sub-directories in order to run the pipeline. Be aware the databases are quite large in cumulative size (~860 GB).
