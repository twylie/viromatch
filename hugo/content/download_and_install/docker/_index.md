---
title: "Docker"
date: 2020-11-10T22:47:17-06:00
draft: false
weight: 2
---

## Docker Containers

The ViroMatch pipeline, and all of its underlying code dependencies, are provided as a [Docker](https://www.docker.com/) image. Once you've installed Docker on your computer and have downloaded the ViroMatch Docker image, you will be able to run pipeline containers.

_What are containers?_

> "A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. A Docker container image is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings."
> (Source: [What is a container?](https://www.docker.com/resources/what-container))

Docker containers are an easy, pragmatic way to package and deliver software, and have been widely adopted for local and cloud-bases computing. Using a Docker image means we've done all of the setup (dependency installation, environment variables, etc.) for you! However, you will need to install Docker on your system before taking advantage of the ViroMatch pipeline image.

To install Docker Desktop for your particular system, please visit:

{{% button href="https://www.docker.com/get-started" %}}Get started with Docker{{% /button %}}

and download the appropriate version for your computer. Follow Docker's instructions for installing and starting Docker Desktop. 

Docker's own tutorials are a good place to start familiarizing yourself with Docker and running Docker containers.

{{% button href="https://www.docker.com/play-with-docker" %}}Play with Docker{{% /button %}}

An in depth overview of Docker is beyond the scope of this documentation; however, there are many other resources, tutorials, and walk-throughs related to Docker online. We will cover Docker basics for running the ViroMatch pipeline throughout this documentation.


