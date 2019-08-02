# -*- coding: utf-8 -*-

"""
process_fastq
~~~~~~~~~~~~~~~
:Description: main module for process_fastq
"""
"""
Created on July 26, 2019
Description: main module for process_fastq
@author: Ronak H Shah
"""
import sys
import os
import logging
import glob
from collections import defaultdict
import pprint
import itertools

try:
    import pandas as pd
except ImportError as e:
    print(
        "process_fastq: pandas is not installed, please install pandas as it \
            is one of the requirements."
    )
    exit(1)
try:
    import helper as hp
except ImportError as e:
    print(
        "process_fastq: helper module could not be loaded, please install \
            package correctly to get this running."
    )
    exit(1)

# Making logging possible
logger = logging.getLogger("process_fastq")


def run(
    sample_id,
    fastq_path,
    expected_read_length,
    output_path,
    cutadapt_path,
    request_id=None,
    run_id=None,
):
    logger.info("procees_fastq: sample id: %s", sample_id)
    logger.info("procees_fastq: run id: %s", run_id)
    logger.info("procees_fastq: request id: %s", request_id)
    logger.info("procees_fastq: fastq_path: %s", fastq_path)
    logger.info("procees_fastq: expected read length: %d", expected_read_length)
    logger.info("procees_fastq: output path: %s", output_path)
    logger.info("procees_fastq: cutadapt path: %s", cutadapt_path)
    run_dict = defaultdict(dict)
    store_read_length = []
    if run_id and request_id:
        for id in run_id:
            glob_file_path = hp.make_path(fastq_path, sample_id ,id, request_id)
            logger.info(
                "process_fastq: the path to search for files: %s", glob_file_path
            )
            run_dict[id]["path"] = glob_file_path
            fastq_list = hp.get_fastq(glob_file_path)
            run_dict[id]["fastq_list"] = fastq_list
            logger.info("process_fastq: the fastq path files: %s", fastq_list)
            read_length_list = hp.get_fastq_read_length(fastq_list)
            run_dict[id]["read_length"] = read_length_list
            store_read_length.append(read_length_list)
            if hp.all_same(read_length_list):
                if read_length_list[0] == expected_read_length:
                    logger.info(
                        "process_fastq: read length for %s matches expected read length",
                        glob_file_path,
                    )
                elif read_length_list[0] < expected_read_length:
                    logger.critical(
                        "process_fastq: read length for %s does not match the expected read length",
                        glob_file_path,
                    )
                    logger.warning(
                        "process_fastq: read length for %s is less then expected read length",
                        glob_file_path,
                    )
                else:
                    logger.critical(
                        "process_fastq: read length for %s does not match the expected read length",
                        glob_file_path,
                    )
                    logger.critical(
                        "process_fastq: read length for %s is more then expected read length",
                        glob_file_path,
                    )
                    logger.critical(
                        "process_fastq: trimming with cutadapt will be ran to make the read length match expected read length"
                    )
            else:
                logger.error(
                    "process_fastq: read length for read1 (R1) and read2 (R2) with %s does not match this is not expected",
                    fastq_list,
                )
                exit(1)
    elif run_id and request_id is None:
        for id in run_id:
            glob_file_path = hp.make_path(fastq_path, sample_id, id, request_id)
            logger.info(
                "process_fastq: the path to search for files: %s", glob_file_path
            )
            run_dict[id]["path"] = glob_file_path
            fastq_list = hp.get_fastq(glob_file_path)
            run_dict[id]["fastq_list"] = fastq_list
            logger.info("process_fastq: the fastq path files: %s", fastq_list)
            read_length_list = hp.get_fastq_read_length(fastq_list)
            run_dict[id]["read_length"] = read_length_list
            store_read_length.append(read_length_list)
            if hp.all_same(read_length_list):
                if read_length_list[0] == expected_read_length:
                    logger.info(
                        "process_fastq: read length for %s matches expected read length",
                        glob_file_path,
                    )
                elif read_length_list[0] < expected_read_length:
                    logger.critical(
                        "process_fastq: read length for %s does not match the expected read length",
                        glob_file_path,
                    )
                    logger.warning(
                        "process_fastq: read length for %s is less then expected read length",
                        glob_file_path,
                    )
                else:
                    logger.critical(
                        "process_fastq: read length for %s does not match the expected read length",
                        glob_file_path,
                    )
                    logger.critical(
                        "process_fastq: read length for %s is more then expected read length",
                        glob_file_path,
                    )
                    logger.critical(
                        "process_fastq: trimming with cutadapt will be ran to make the read length match expected read length"
                    )
            else:
                logger.error(
                    "process_fastq: read length for read1 (R1) and read2 (R2) with %s does not match this is not expected",
                    fastq_list,
                )
                exit(1)
    else:
        glob_file_path = hp.make_path(fastq_path, sample_id, run_id, request_id)
        logger.info("process_fastq: the path to search for files: %s", glob_file_path)
        for m_path in glob_file_path:
            fastq_list = hp.get_fastq(m_path)
            logger.info("process_fastq: the fastq path files: %s", fastq_list)
            read_length_list = hp.get_fastq_read_length(fastq_list)
            if hp.all_same(read_length_list):
                if read_length_list[0] == expected_read_length:
                    logger.info(
                        "process_fastq: read length for %s matches expected read length",
                        glob_file_path,
                    )
                elif read_length_list[0] < expected_read_length:
                    logger.critical(
                        "process_fastq: read length for %s does not match the expected read length",
                        glob_file_path,
                    )
                    logger.warning(
                        "process_fastq: read length for %s is less then expected read length",
                        glob_file_path,
                    )
                else:
                    logger.critical(
                        "process_fastq: read length for %s does not match the expected read length",
                        glob_file_path,
                    )
                    logger.critical(
                        "process_fastq: read length for %s is more then expected read length",
                        glob_file_path,
                    )
                    logger.critical(
                        "process_fastq: trimming with cutadapt will be ran to make the read length match expected read length"
                    )
            else:
                logger.error(
                    "process_fastq: read length for read1 (R1) and read2 (R2) with %s does not match this is not expected",
                    fastq_list,
                )
                exit(1)

    return 0
