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


def run(sample_id, request_id, run_id, fastq_path, output_path, cutadapt_path):
    logger.info("procees_fastq: sample id: %s", sample_id)
    logger.info("procees_fastq: run id: %s", run_id)
    logger.info("procees_fastq: fastq_path: %s", fastq_path)
    logger.info("procees_fastq: output_path: %s", output_path)
    logger.info("procees_fastq: cutadapt_path: %s", cutadapt_path)
    run_dict = defaultdict(dict)
    store_read_length = []
    for id in run_id:
        glob_file_path = hp.make_path(fastq_path, id, request_id, sample_id)
        logger.info("process_fastq: the path to search for files: %s", glob_file_path)
        run_dict[id]["path"] = glob_file_path
        fastq_list = hp.get_fastq(glob_file_path)
        run_dict[id]["fastq_list"] = fastq_list
        logger.info("process_fastq: the fastq path files: %s", fastq_list)
        read_length_list = hp.get_fastq_read_length(fastq_list)
        run_dict[id]["read_length"] = read_length_list
        store_read_length.append(read_length_list)
    for a, b in itertools.combinations(store_read_length, 2):
        logger.info("Comparing read lengths: %s and %s", a, b)
        if a == b:
            pass
        else:
            logger.critical("Read length are not the same: %s and %s", a, b)
            logger.critical(
                "Cutadapt will be ran to make the read length match across runs"
            )

    # pprint.pprint(run_dict)
    return 0
