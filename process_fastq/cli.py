# -*- coding: utf-8 -*-

"""Console script for process_fastq."""
import sys
import logging
try:
    import click
except ImportError as e:
    print("cli: click is not installed, please install pandas as it is one of the requirements.")
    exit(1)
try:
    import click_log
except ImportError as e:
    print("cli: click-log is not installed, please install pandas as it is one of the requirements.")
    exit(1)
try:
    import pandas as pd
except ImportError as e:
    print ("cli: pandas is not installed, please install pandas as it is one of the requirements.")
    exit(1)
try:
    import main as pf
except ImportError as e:
    print ("cli: process_fastq moudle could not be loaded, please install package correctly to get this running.")
    exit(1)
try:
    import helper as hp
except ImportError as e:
    print ("cli: helper moudle could not be loaded, please install package correctly to get this running.")
    exit(1)

#Making logging possible
logger = logging.getLogger('pf.log')
click_log.basic_config(logger)
click_log.ColorFormatter.colors['info'] = dict(fg="green")


@click.command()
@click.option('--filename', '-f', type=click.Path(exists=True), help="Full path to the excel file")
@click.option('--fastq-path', '-fp', type=click.Path(), help="Full path to fastq files")
@click.option('--output-path', '-op', type=click.Path(), help="Full path to where we link the output files")
@click.option('--cutadapt-path', '-cp', type=click.Path(exists=True), help="Full path to location of cutadapt executable")
@click_log.simple_verbosity_option(logger)
def main(filename, fastq_path, output_path, cutadapt_path):
    #"""Console script for process_fastq."""
    
    #click.echo("{}, {}".format(filename, fastq_path))
    #click.echo("Replace this message by putting your code into process_fastq.cli.main")
    pf.run(filename,fastq_path,output_path,cutadapt_path)
    

    #click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    main()
