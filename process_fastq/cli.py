# -*- coding: utf-8 -*-

"""
cli
~~~~~~~~~~~~~~~
:Description: console script for running process_fastq
"""
"""
Created on July 26, 2019
Description: console script for running process_fastq
@author: Ronak H Shah
"""
__all__ = []
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__date__ = '2019-07-27'
__updated__ = '2019-07-28'

import sys
import logging

try:
    import click
except ImportError as e:
    print(
        "cli: click is not installed, please install pandas as it is one of the requirements."
    )
    exit(1)
try:
    import click_log
except ImportError as e:
    print(
        "cli: click-log is not installed, please install pandas as it is one of the requirements."
    )
    exit(1)
try:
    import process_fastq as pf
except ImportError as e:
    print(
        "cli: process_fastq module could not be loaded, please install package correctly to get this running."
    )
    exit(1)
try:
    import helper as hp
except ImportError as e:
    print(
        "cli: helper module could not be loaded, please install package correctly to get this running."
    )
    exit(1)

# Making logging possible
logger = logging.getLogger("pf.log")
click_log.basic_config(logger)
click_log.ColorFormatter.colors["info"] = dict(fg="green")


@click.command()
@click.option(
    "--filename",
    "-f",
    required=True,
    type=click.Path(exists=True),
    help="Full path to the excel file",
)
@click.option(
    "--fastq-path",
    "-fp",
    required=True,
    type=click.Path(),
    help="Full path to fastq files",
)
@click.option(
    "--output-path",
    "-op",
    required=True,
    type=click.Path(),
    help="Full path to where we link the output files",
)
@click.option(
    "--cutadapt-path",
    "-cp",
    required=True,
    type=click.Path(exists=True),
    help="Full path to location of cutadapt executable",
)
@click.version_option(
    version=__version__,
    prog_name='process_fastq'
)
@click_log.simple_verbosity_option(logger)
def main(filename, fastq_path, output_path, cutadapt_path):
    # """Console script for process_fastq."""

    # click.echo("{}, {}".format(filename, fastq_path))
    # click.echo("Replace this message by putting your code into process_fastq.cli.main")
    pf.run(filename, fastq_path, output_path, cutadapt_path)

    # click.echo("See click documentation at http://click.pocoo.org/")
    return 0


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version 0.1.0")
    ctx.exit()


if __name__ == "__main__":
    sys.exit(main())
