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

try:
    import pandas as pd
except ImportError as e:
    print(
        "process_fastq: pandas is not installed, please install pandas as it is one of the requirements."
    )
    exit(1)
try:
    import helper as hp
except ImportError as e:
    print(
        "process_fastq: helper module could not be loaded, please install package correctly to get this running."
    )
    exit(1)

# Making logging possible
logger = logging.getLogger("pf.log")


def run(filename, fastq_path, output_path, cutadapt_path):
    logger.info("Filename: %s", filename)
    logger.info("fastq_path: %s", fastq_path)
    logger.info("output_path: %s", output_path)
    logger.info("cutadapt_path: %s", cutadapt_path)
    hp.read_excel(filename)
    return 0
