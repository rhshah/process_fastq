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

import os
import logging
from collections import defaultdict
import pathlib

try:
    import pandas as pd
except ImportError as e:
    print(
        "process_fastq: pandas is not installed, please install pandas as it is one of the requirements."
    )
    exit(1)
try:
    import process_fastq.helper as hp
except ImportError as e:
    print(
        "process_fastq: helper module could not be loaded, please install package correctly to get this running."
    )
    exit(1)
try:
    import process_fastq.get_directory_paths as gdp
except ImportError as e:
    print(
        "process_fastq: get_directory_paths module could not be loaded, please install package correctly to get this running."
    )
    exit(1)
try:
    import process_fastq.get_fastq_information as gfi
except ImportError as e:
    print(
        "process_fastq: get_fastq_information module could not be loaded, please install package correctly to get this running."
    )
    exit(1)
try:
    import process_fastq.run_cutadapt as rc
except ImportError as e:
    print(
        "process_fastq: run_cutadapt module could not be loaded, please install package correctly to get this running."
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
    if hp.is_empty(request_id):
        request_id = None
    if hp.is_empty(run_id):
        run_id = None
    logger.info("procees_fastq: run: sample id: %s", sample_id)
    logger.info("procees_fastq: run: run id: %s", run_id)
    logger.info("procees_fastq: run: request id: %s", request_id)
    logger.info("procees_fastq: run: fastq path: %s", fastq_path)
    logger.info("procees_fastq: run: expected read length: %d", expected_read_length)
    logger.info("procees_fastq: run: output path: %s", output_path)
    logger.info("procees_fastq: run: cutadapt path: %s", cutadapt_path)
    run_dict = defaultdict(dict)
    if run_id and request_id:
        if len(run_id) == 1:
            glob_file_path, target_path_to_link, fastq_list, read_length_list = get_sample_level_information(
                fastq_path, output_path, sample_id, run_id[0], request_id
            )
            run_dict[run_id]["path"] = glob_file_path
            run_dict[run_id]["fastq_list"] = fastq_list
            run_dict[run_id]["read_length"] = read_length_list
            check_value = compare_read_length(read_length_list, expected_read_length, glob_file_path, fastq_path, fastq_list):
                if check_value:
                    try:
                        os.symlink(os.path.join(glob_file_path,"*"), os.path.join(target_path_to_link , "/")
                    except OSError as e:
                        logger.info("procees_fastq: run: cannot create symlink")
                        exit(1)
                else:
                    logger.info("procees_fastq: run: running cutadapt")
        else:
            for r_id in run_id:
                glob_file_path, target_path_to_link, fastq_list, read_length_list = get_sample_level_information(
                    fastq_path, output_path, sample_id, r_id, request_id
                )
                run_dict[r_id]["path"] = glob_file_path
                run_dict[r_id]["fastq_list"] = fastq_list
                run_dict[r_id]["read_length"] = read_length_list
                compare_read_length(
                    read_length_list,
                    expected_read_length,
                    glob_file_path,
                    fastq_path,
                    fastq_list,
                )

    elif run_id and request_id is None:
        if len(run_id) == 1:
            glob_file_path, target_path_to_link, fastq_list, read_length_list = get_sample_level_information(
                fastq_path, output_path, sample_id, run_id[0], request_id
            )
            run_dict[run_id]["path"] = glob_file_path
            run_dict[run_id]["fastq_list"] = fastq_list
            run_dict[run_id]["read_length"] = read_length_list
            compare_read_length(
                read_length_list,
                expected_read_length,
                glob_file_path,
                fastq_path,
                fastq_list,
            )
        else:
            for r_id in run_id:
                glob_file_path, target_path_to_link, fastq_list, read_length_list = get_sample_level_information(
                    fastq_path, output_path, sample_id, r_id, request_id
                )
                run_dict[r_id]["path"] = glob_file_path
                run_dict[r_id]["fastq_list"] = fastq_list
                run_dict[r_id]["read_length"] = read_length_list
                compare_read_length(
                    read_length_list,
                    expected_read_length,
                    glob_file_path,
                    fastq_path,
                    fastq_list,
                )

    else:
        glob_file_path = gdp.make_path(fastq_path, sample_id, run_id, request_id)
        logger.info("process_fastq: run: the path to search for files: %s", glob_file_path)
        for m_path in glob_file_path:
            p_path = pathlib.Path(m_path)
            p_sample_id = p_path.name
            p_run_id = p_path.parent.parent.name
            target_path_to_link = hp.make_directory(p_sample_id, output_path)
            fastq_list = gfi.get_fastq(m_path)
            logger.info("process_fastq: run: the fastq path files: %s", fastq_list)
            read_length_list = gfi.get_fastq_read_length(fastq_list)
            run_dict[p_run_id]["path"] = m_path
            run_dict[p_run_id]["fastq_list"] = fastq_list
            run_dict[p_run_id]["read_length"] = read_length_list
            compare_read_length(
                read_length_list,
                expected_read_length,
                m_path,
                fastq_path,
                fastq_list,
            )

    return 0


def get_sample_level_information(fastq_path, output_path, sample_id, r_id, request_id):
    glob_file_path = gdp.make_path(fastq_path, sample_id, r_id, request_id)
    logger.info("process_fastq: get_sample_level_information: the path to search for files: %s", glob_file_path)
    if isinstance(glob_file_path, list):
        glob_file_path = "".join(glob_file_path)
    p_path = pathlib.Path(glob_file_path)
    p_sample_id = p_path.name
    target_path_to_link = hp.make_directory(p_sample_id, output_path)
    fastq_list = gfi.get_fastq(glob_file_path)
    logger.info("process_fastq: get_sample_level_information: the fastq path files: %s", fastq_list)
    read_length_list = gfi.get_fastq_read_length(fastq_list)
    return [glob_file_path, target_path_to_link, fastq_list, read_length_list]


def compare_read_length(
    read_length_list, expected_read_length, glob_file_path, fastq_path, fastq_list
):
    if hp.all_same(read_length_list):
        if read_length_list[0] == expected_read_length:
            value = True
            logger.info(
                "process_fastq: compare_read_length:  length for %s matches expected read length",
                glob_file_path,
            )
        elif read_length_list[0] < expected_read_length:
            value = True
            logger.critical(
                "process_fastq: compare_read_length:  length for %s does not match the expected read length",
                glob_file_path,
            )
            logger.warning(
                "process_fastq: compare_read_length: read length for %s is less then expected read length",
                glob_file_path,
            )
        else:
            value = False
            logger.critical(
                "process_fastq: compare_read_length:  length for %s does not match the expected read length",
                glob_file_path,
            )
            logger.critical(
                "process_fastq: compare_read_length:  length for %s is more then expected read length",
                glob_file_path,
            )
            logger.critical(
                "process_fastq:compare_read_length: trimming with cutadapt will be ran to make the read length match expected read length"
            )

    else:
        logger.error(
            "process_fastq: compare_read_length: length for read1 (R1) and read2 (R2) with %s does not match this is not expected",
            fastq_list,
        )
        exit(1)
    return value
