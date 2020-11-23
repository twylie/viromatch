from .lib import ViroMatch
import yaml
import shutil

# This code will be executed when the top-most (/bin/viromatch) script is
# run. Goals for this function follow.
#
# 1. Collect and evaluate command line arguments.
# 2. Create a new processing/working directory.
# 3. Write an instance configuration file.
# 4. Choose the appropriate Snakefile (recipe) for processing and copy it into
#    the working directory.
# 5. Execute the Snakefile.


def main():

    """
    ViroMatch is a lightweight computational pipeline for detection of viral
    reads from complex metagenomic sequencing data. The ViroMatch framework is
    implemented as a class of methods and also a standalone executable. To run
    the pipeline directly, see:

            viromatch --help

    A command line interface (CLI) provides a menu of choices for running
    ViroMatch. Input sequence association and processing parameters are passed
    using the CLI. A single, reproducible analysis instruction set is defined
    per sample/process. ViroMatch utilizes several current, core NGS software
    packages (e.g. BWA, SAMtools, Diamond) for sequence alignment and
    manipulation and supports BAM or paired FASTQ files as sequence input.
    Pipeline methods are included for pre-processing (low-complexity filtering,
    adaptor removal, quality trimming, etc.) and human/host sequence removal.
    Metagenomic reads are aligned against comprehensive viral databases in an
    iterative, increasingly sensitive fashion. Primary identities are
    determined using BWA-MEM, followed by secondary translated nucleotide
    alignments using Diamond. Finally, putative viral reads are screened
    against all NCBI nt/nr entries before being classified as viral to improve
    specificity of viral assignment. Reports are generated for viral genome
    identities and associated read counts.
    """

    viromatch = ViroMatch()

    # evaluate command line arguments; convert argparse object to flat
    # dictionary.

    viromatch.evaluate_cli_arguments()
    arguments = vars(viromatch.arguments)
    arguments.update({'version': viromatch.version})

    # Based on the instance arguments, choose the appropriate Snakefile
    # pipeline recipe. Copy the Snakefile into the working directory. All
    # that is needed to run the pipeline will be (1) CONFIG.yaml and (2)
    # the Snakefile.

    snakefile = viromatch.select_snakefile_recipe()
    shutil.copy(snakefile, arguments['outdir'] + 'Snakefile')
    arguments.update({'snakefile': snakefile})

    # Write the arguments to a YAML config file for Snakemake.

    arguments.update({'config': arguments['outdir'] + 'CONFIG.yaml'})
    with open(arguments['config'], 'w') as outfile:
        yaml.dump(arguments, outfile)

    # Execute the Snakemake pipeline in the processing directory.

    viromatch.execute_snakemake_pipeline()

    return


# __END__
