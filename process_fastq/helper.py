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

import os
import logging
from functools import reduce

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
    logger.info("helper: make_path: Reading the excel file: %s", file)
    pdataframe = pd.read_excel(file, sheet_name=0, keep_default_na="True", index_col=0)
    logger.info("helper: make_path: Finished reading excel file: %s", file)
    return pdataframe


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def all_same(items):
    return all(x == items[0] for x in items)


def is_empty(any_structure):
    if any_structure:
        logger.info("helper: is_empty Structure is not empty.", any_structure)
        return False
    else:
        logger.info("helper: is_empty: Structure is empty.")
        return True


def make_directory(name, path):
    dirName = os.path.join(path, name)
    try:
        # Create target Directory
        os.mkdir(dirName)
        logger.info("helper: make_directory: Directory created: %s", dirName)
    except FileExistsError as e:
        logger.warning("helper: make_directory: Directory already exists: %s", dirName)
        logger.warning("helper: make_directory: ")
    return dirName
