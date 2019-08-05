# -*- coding: utf-8 -*-

"""
link_fastq_juno
~~~~~~~~~~~~~~~
:Description: console script for running process_fastq on manifest level on juno
"""
"""
Created on August 05, 2019
Description: console script for running process_fastq on manifest level on juno
@author: Ronak H Shah
"""


import sys
import logging
import time
import subprocess
import shlex

try:
    import click
except ImportError as e:
    print(
        "cli: click is not installed, please install pandas as it is one of \
            the requirements."
    )
    exit(1)
try:
    import click_log
except ImportError as e:
    print(
        "cli: click-log is not installed, please install pandas as it is one \
            of the requirements."
    )
    exit(1)
try:
    import pandas as pd
except ImportError as e:
    print(
        "helper: pandas is not installed, please install pandas as it is one of the requirements"
    )
    exit(1)


__all__ = []
__version_info__ = ("0", "1", "0")
__version__ = ".".join(__version_info__)
__date__ = "2019-08-05"
__updated__ = "2019-08-05"


# Making logging possible
logger = logging.getLogger("link_fastq")
click_log.basic_config(logger)
click_log.ColorFormatter.colors["info"] = dict(fg="green")


@click.command()
@click.option(
    "--manifest-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="Manifest file having information about run id and sample id to get the fastq files (eg: -m Project_05500_GB_manifest.xslx)",
)
@click.option(
    "--request-id",
    "-p",
    required=True,
    default=None,
    type=click.STRING,
    help="IGO request id to get the fastq files. (eg:-p Project_05500_GB or -p 05500_GB)",
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
@click.option(
    "--process-fastq-path",
    "-pfp",
    required=True,
    type=click.Path(exists=True),
    help="Full path to location of cutadapt executable",
)
@click.option(
    "--expected-read-length",
    "-l",
    required=False,
    default=101,
    type=click.INT,
    help="Expected read length from the fastq file",
)
@click.version_option(version=__version__, prog_name="link_fastq_juno")
@click_log.simple_verbosity_option(logger)
def main(
    manifest_file,
    fastq_path,
    expected_read_length,
    output_path,
    cutadapt_path,
    process_fastq_path,
    request_id,
):
    logger_output = output_path + "link_fastq.log"
    fh = logging.FileHandler(logger_output)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("==================================================")
    logger.info(">>> Running link_fastq for: %s <<<", request_id)
    logger.info("==================================================")
    t1_start = time.perf_counter()
    t2_start = time.process_time()
    # Code to traverse all samples
    p_dataframe = read_excel(manifest_file)
    for index, row in p_dataframe.iterrows():
        sample_id = row["INVESTIGATOR_SAMPLE_ID"]
        if ";" in row["INCLUDE_RUN_ID"]:
            run_id = row["INCLUDE_RUN_ID"].split(";")
        else:
            run_id = row["INCLUDE_RUN_ID"]
        logger.info(
            "link_fastq_juno: run: processing %s, on follwoing runs: %s",
            sample_id,
            run_id,
        )
        if len(run_id) > 1:
            process_fastq_cmd = (
                process_fastq_path
                + " -l "
                + str(expected_read_length)
                + " -s "
                + sample_id
                + " -r "
                + " -r ".join(run_id)
                + " "
                + " -p "
                + request_id
                + " -fp "
                + fastq_path
                + " -op "
                + output_path
                + " -cp "
                + cutadapt_path
                + " --verbosity DEBUG"
            )
        else:
            process_fastq_cmd = (
                process_fastq_path
                + " -l "
                + str(expected_read_length)
                + " -s "
                + sample_id
                + " -r "
                + run_id
                + " -p "
                + request_id
                + " -fp "
                + fastq_path
                + " -op "
                + output_path
                + " -cp "
                + cutadapt_path
                + " --verbosity DEBUG"
            )
        bsub_cmd = (
            "bsub -cwd . "
            + "-J "
            + "link_fastq_"
            + sample_id
            + " -g "
            + request_id
            + " -app anyOS"
            + " -R select[mem > 12]"
            + " -R rusage[mem=12]"
            + " -R select[type==CentOS7]"
            + " -M 12"
            + " -n 1"
            + ' -W 360 "'
            + process_fastq_cmd
            + '"'
        )
        logger.debug(
            "link_fastq: run: the commandline is %s",
            bsub_cmd.encode("unicode_escape").decode("utf-8"),
        )
        lsf_job_id = bsub(shlex.split(bsub_cmd))
        logger.info(
            "Job submitted to lsf for sample %s, job id:%s", sample_id, lsf_job_id
        )
    # Code done
    t1_stop = time.perf_counter()
    t2_stop = time.process_time()
    logger.info("--------------------------------------------------")
    logger.info("Elapsed time: %.1f [min]" % ((t1_stop - t1_start) / 60))
    logger.info("CPU process time: %.1f [min]" % ((t2_stop - t2_start) / 60))
    logger.info("--------------------------------------------------")
    return 0


def read_excel(file):
    logger.info("link_fastq: read_excel: Reading the excel file: %s", file)
    pdataframe = pd.read_excel(file, sheet_name=0, keep_default_na="True", index_col=0)
    logger.info("link_fastq: read_excel: Finished reading excel file: %s", file)
    return pdataframe


def bsub(args):
    """
    Execute lsf bsub
    :param bsubline:
    :return:
    """
    try:
        proc = Popen(args)
        proc.wait()
        retcode = proc.returncode
        if retcode >= 0:
            pass
    except IOError as e:
        e = sys.exc_info()[0]
        logging.info(
            "Running of bsub command: %s \n has failed. The exception produced is %s Thus we will exit",
            cmd,
            e,
        )
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
