from .lib import Host
import yaml
import shutil


# This code will be executed when the top-most (/bin/viromatch_host) script
# is run. Goals for this function follow.
#
# 1. Collect and evaluate command line arguments.
# 2. Create a new processing/working directory.
# 3. Write an instance configuration file.
# 4. Choose the appropriate Snakefile (recipe) for processing and copy it into
#    the working directory.
# 5. Execute the Snakefile.


def main():

    viromatch = Host()

    # Evaluate command line arguments; convert argparse object to flat
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
