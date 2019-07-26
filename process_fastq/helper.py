# -*- coding: utf-8 -*-

"""
helper
~~~~~~~~~~~~~~~
:Description: helper has many utilities for process_fastq
"""
'''
Created on July 26, 2019
Description: helper has many utilities for process_fastq
@author: Ronak H Shah
'''

import logging
try:
    import click_log
except ImportError as e:
    print("helper: click-log is not installed, please install pandas as it is one of the requirements")
    exit(1)
try:
    import pandas as pd
except ImportError as e:
    print ("helper: pandas is not installed, please install pandas as it is one of the requirements")
    exit(1)

#Making logging possible
logger = logging.getLogger(__name__)
click_log.basic_config(logger)
click_log.ColorFormatter.colors['info'] = dict(fg="green")

#Read excel file
def read_excel(file):
    logger.info("helper: Reading the excel file: %s", file)
    pdataframe = pd.read_excel(file,sheet_name=0, keep_default_na='True',index_col=0)
    logger.info("helper: Finished reading excel file: %s", file) 
    return pdataframe