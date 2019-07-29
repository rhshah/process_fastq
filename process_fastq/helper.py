# -*- coding: utf-8 -*-

"""
helper
~~~~~~~~~~~~~~~
:Description: helper has many utilities for process_fastq
"""
"""
Created on July 26, 2019
Description: helper has many utilities for process_fastq
@author: Ronak H Shah
"""

import sys
import os
import logging
import glob

try:
    import pandas as pd
except ImportError as e:
    print(
        "helper: pandas is not installed, please install pandas as it is one of the requirements"
    )
    exit(1)

# Making logging possible
logger = logging.getLogger("process_fastq")


def read_excel(file):
    logger.info("helper: Reading the excel file: %s", file)
    pdataframe = pd.read_excel(file, sheet_name=0, keep_default_na="True", index_col=0)
    logger.info("helper: Finished reading excel file: %s", file)
    return pdataframe


def make_path(dir_path, run_id, request_id, sample_id):
    logger.info("helper: Making file path to search for files")
    glob_run_id = "*" + run_id + "*"
    glob_request_id = "*" + request_id + "*"
    glob_sample_id = "*" + sample_id + "*"
    glob_path = os.path.join(dir_path, glob_run_id, glob_request_id, glob_sample_id)
    glob_path = glob.glob(glob_path)
    logger.info("helper: Finished making file path to search for files")
    return glob_path


def get_fastq(dir_path):
    logger.info("helper: Globbing fastq.gz file")
    R1_pattern = "*R1*.gz"
    R2_pattern = "*R2*.gz"
    logger.debug("helper: Path to search for fastq: %s", dir_path)
    glob_path_R1 = os.path.join(dir_path, R1_pattern)
    glob_path_R2 = os.path.join(dir_path, R2_pattern)
    glob_path_R1 = glob.glob(glob_path_R1)
    glob_path_R2 = glob.glob(glob_path_R2)
    logger.info("helper: Done globbing fastq.gz file")
    return [glob_path_R1, glob_path_R2]


