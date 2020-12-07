---
title: "Download ViroMatch"
date: 2020-11-10T23:11:59-06:00
draft: false
weight: 3
---

## ViroMatch Docker Image

Once you've installed Docker Desktop (and the Docker service is running on your system) you will be able to download the ViroMatch Docker image. To test that Docker Desktop is installed and running correctly on your computer, you may type the following in a terminal.

```bash
docker --version
```

Results:

```plaintext
Docker version 19.03.12, build 48a66213fe
```

The latest version of ViroMatch is provided via [DockerHub](https://hub.docker.com). Once you've installed Docker Desktop (and the Docker service is running on your system) you will be able to download and run the ViroMatch Docker image. Specifically, you want the `viromatch:latest` image.

{{< button href="https://hub.docker.com/r/twylie/viromatch/tags" >}}Download ViroMatch{{< /button >}}

Alternatively, to download and install ViroMatch into Docker service, type the following in your terminal.

```bash
docker pull twylie/viromatch:latest
```
Results:

```plaintext
latest: Pulling from twylie/viromatch
Digest: sha256:71547c20dbdd6c14f67b661f3c88b4b902675df642004a1a90c57f1223fdabb2
Status: Image is up to date for twylie/viromatch:latest
docker.io/twylie/viromatch:latest
```

The command above will contact DockerHub to download and register the ViroMatch image on your system. This process can take several minutes. Once installed, you will be able to run ViroMatch pipeline containers on your computer. Type the following to see if your download was successful.

```bash
docker images twylie/virmatch:latest
```

Results:

```plaintext
REPOSITORY        TAG      IMAGE ID       CREATED     SIZE
twylie/viromatch   latest   de2636b2ff1e   3 days ago  1.56GB
```

If you see something that looks similar to the above output, you've downloaded and registered the ViroMatch docker image on your system.
