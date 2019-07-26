# -*- coding: utf-8 -*-

"""
main
~~~~~~~~~~~~~~~
:Description: main module for process_fastq
"""
'''
Created on July 26, 2019
Description: main module for process_fastq
@author: Ronak H Shah
'''

import logging
try:
    import click
except ImportError as e:
    print("process_fastq: click is not installed, please install pandas as it is one of the requirements.")
    exit(1)
try:
    import click_log
except ImportError as e:
    print("process_fastq: click-log is not installed, please install pandas as it is one of the requirements.")
    exit(1)
try:
    import pandas as pd
except ImportError as e:
    print ("process_fastq: pandas is not installed, please install pandas as it is one of the requirements.")
    exit(1)
try:
    import helper
except ImportError as e:
    print ("process_fastq: helper moudle could not be loaded, please install package correctly to get this running.")
    exit(1)

#Making logging possible
logger = logging.getLogger('pf.log')
#click_log.basic_config(logger)
#click_log.ColorFormatter.colors['info'] = dict(fg="green")
#@click_log.simple_verbosity_option(logger)
def run(filename,fastq_path,output_path,cutadapt_path):
    logger.info("Filename: %s", filename)
    logger.info("fastq_path: %s", fastq_path)
    logger.info("output_path: %s", output_path)
    logger.info("cutadapt_path: %s", cutadapt_path)
    return 0