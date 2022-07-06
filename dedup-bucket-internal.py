#!/usr/bin/python3
"""
Generate list of deduped files.

Usage:
  dedup-bucket-internal.py <path_to_file> <out_file>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""


## python code
import pandas as pd
import numpy as np
from docopt import docopt

## udf to generate file extension
def get_extension(x):
    spl = x.split(".")
    spl_len = len(spl)
    if(spl_len > 1):
      return spl[len(spl)-1]
    return None

## udf to create dup table
def make_dup_table(path_to_file):
  ## load file and setup
  x1 = pd.read_csv(path_to_file, header=None, names=['blob','hash'])
  x1['filetype'] = [get_extension(x) for x in x1.blob]
  ## get dups and file types
  dups = np.array(x1['hash'].duplicated(keep=False).values)
  ndirs = np.array((x1['filetype'].values == None) == False)
  x1['duplicate_files'] = np.logical_and(dups, ndirs)
  return x1

if __name__ == '__main__':
    ## collect args
    args = docopt(__doc__, version="get_dups 1.0")
    ## get summaries
    df = make_dup_table(args["<path_to_file>"])
    df.to_csv(args["<out_file>"],index=False)
