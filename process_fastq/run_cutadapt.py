# -*- coding: utf-8 -*-

"""
run_cutadapt
~~~~~~~~~~~~~~~
:Description: this function helps to run cutadapt to trim reads larger then expected read length
"""
"""
Created on July 26, 2019
Description: this function helps to run cutadapt to trim reads larger then expected read length
@author: Ronak H Shah
"""

import os
import logging
import glob
import subprocess
import re
import pathlib
from collections import defaultdict

# Making logging possible
logger = logging.getLogger("process_fastq")
