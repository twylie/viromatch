
FROM ubuntu:bionic
MAINTAINER T.N. Wylie <twylie@wustl.edu>

LABEL \
description = "Read-based virome characterization pipeline."

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
    build-essential \
    bzip2 \
    cmake \
    git \
    libnss-sss \
    libtbb2 \
    libtbb-dev \
    liblzma-dev \
    ncurses-dev \
    nodejs \
    python3.7-dev \
    python3-pip \
    unzip \
    wget \
    zlib1g \
    zlib1g-dev \
    curl \
    zsh \
    libbz2-dev \
    autoconf \
    automake \
    zile \
    default-jre \
    varscan \
    bcftools

# Installing BioPython.
RUN \
python3.7 -m pip install biopython && \
python3.7 -m pip install pip

# Install BWA for sequence alignments.

RUN \
git clone https://github.com/lh3/bwa.git viromatch_install/bwa && \
cd viromatch_install/bwa && \
make && \
cp bwa /usr/bin

# Install SAMTOOLS for SAM/BAM handling.

RUN \
curl -L https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2 > viromatch_install/samtools-1.9.tar.bz2 && \
bzip2 -d viromatch_install/samtools-1.9.tar.bz2 && \
tar xvf viromatch_install/samtools-1.9.tar -C viromatch_install/ && \
cd viromatch_install/samtools-1.9 && \
./configure --without-curses --disable-lzma && \
make && \
cp samtools /usr/bin

# Install seqtk for sequence handling.

RUN \
git clone https://github.com/lh3/seqtk.git viromatch_install/seqtk && \
cd viromatch_install/seqtk && \
make && \
cp seqtk /usr/bin

# Install Diamond for sequence alignments.

RUN \
wget -O viromatch_install/diamond-linux64.tar.gz http://github.com/bbuchfink/diamond/releases/download/v0.9.29/diamond-linux64.tar.gz && \
cd viromatch_install/ && \
tar xvfz diamond-linux64.tar.gz && \
cp diamond /usr/bin

# Install VSEARCH for low-complexity filter methods.

RUN \
git clone https://github.com/torognes/vsearch.git viromatch_install/vsearch && \
cd viromatch_install/vsearch && \
./autogen.sh && \
./configure && \
make && \
make install

# Install FQTRIM for sequence trimming.

RUN \
wget -O viromatch_install/fqtrim-0.9.7.Linux_x86_64.tar.gz http://ccb.jhu.edu/software/fqtrim/dl/fqtrim-0.9.7.Linux_x86_64.tar.gz && \
cd viromatch_install/ && \
tar xvfz fqtrim-0.9.7.Linux_x86_64.tar.gz && \
cp fqtrim-0.9.7.Linux_x86_64/fqtrim /usr/bin

# Install Snakemake for pipeline development.

RUN \
python3.7 -m pip install snakemake==5.25.0

# File clean-up.

RUN \
cd / && \
\rm -rf viromatch_install

# Installing ViroMatch pipeline and associated code.

RUN \
python3.7 -m pip install --upgrade pip setuptools wheel && \
pip install pandas && \
pip install pyyaml && \
pip install pysam && \
pip install vcfpy

RUN mkdir /usr/lib/python3.7/viromatch/
ADD viromatch /usr/lib/python3.7/viromatch/
COPY bin /usr/bin

RUN mkdir /usr/share/viromatch/
COPY db /usr/share/viromatch/


# __END__
