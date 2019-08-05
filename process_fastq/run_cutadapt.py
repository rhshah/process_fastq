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
import subprocess
import pathlib
import tempfile
from collections import defaultdict

# Making logging possible
logger = logging.getLogger("process_fastq")


def run(cutadapt_path, output_path, fastq_list, trim_length):
    trimmed_fastq = []
    for fastq_file in fastq_list:
        p_path = pathlib.Path(fastq_file)
        sample_id = p_path.name
        tmp_fo = tempfile.TemporaryDirectory(dir=output_path, prefix="cutadapt_")
        out_file_path = os.path.join(tmp_fo.name, sample_id)
        cmd = cutadapt_path + " -l " + str(trim_length) + " " + out_file_path + fastq_file
        logger.debug(
            "run_cutadapt: run: the commandline is %s",
            cmd.encode("unicode_escape").decode("utf-8"),
        )
        out = subprocess.Popen(
            (cmd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        stdout, stderr = out.communicate()
        if stderr is None:
            logger.debug("run_cutadapt: run: Read: %s", stdout.decode("utf-8"))
        else:
            logger.error("run_cutadapt: run: could not run cutadapt for: %s", sample_id)
            exit(1)
        trimmed_fastq.append(out_file_path)
    return trimmed_fastq
