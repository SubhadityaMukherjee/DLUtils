import concurrent
import os
import time
from concurrent.futures import ProcessPoolExecutor
from types import SimpleNamespace
from typing import *

from tqdm import tqdm


def num_cpus():
    """
    Get number of cpus
    """
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count()


def ifnone(a, b):
    """
    Return if None
    """
    return b if a is None else a
