---
title: "Mapping Docker Volumes"
date: 2020-11-10T23:39:49-06:00
draft: false
weight: 1
---

## Docker Needs to See Your Files

Regardless of whether you use an interactive session or command line execution, you will need to map your local directories to the Docker container. Once inside a container, Docker doesn't understand your local file system unless you explicitly tell it how things are mapped. The volume mapping convention is of the form `/local:/container` --- i.e. we are mapping a local directory to an alias that will point to the directory within the Docker container, as passed on the command line using the `-v` option.

{{% notice note %}}
All local directories that you wish Docker to see must be mapped in this way. See the interactive and command line examples that follow for how Docker `-v` volume mapping is accomplished.
{{% /notice %}}




