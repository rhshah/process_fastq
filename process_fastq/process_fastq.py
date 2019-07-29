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
import json

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
    run_json = {}
    for id in run_id:
        glob_file_path = hp.make_path(fastq_path, id, request_id, sample_id)
        logger.info("process_fastq: the path to search for files: %s",
                    glob_file_path)
        run_json['run_id_path'] = glob_file_path
        fastq_list = hp.get_fastq(glob_file_path)
        run_json['fastq_list'] = fastq_list
        logger.info("process_fastq: the fastq path files: %s",
                    fastq_list)
    print(json.dump(run_json), sort_keys=True, indent=4)
    return 0
