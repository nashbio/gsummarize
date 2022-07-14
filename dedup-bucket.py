#!/usr/bin/python3
"""
Generate list of deduped files (tab-delimited output).

Usage:
  dedup-bucket-internal.py <path_to_bucket> <out_file> [--include-dirs]

Options:
  --include-dirs  Include directories in deduplication summaries.
  -h --help  Show this screen.
  --version  Show version.


"""

## imports and storage setup
from google.cloud import storage
from docopt import docopt
import pandas as pd
CS = storage.Client()

## udf to generate file extension
def get_extension(x):
    spl = x.split(".")
    spl_len = len(spl)
    if(spl_len > 1):
      return spl[len(spl)-1]
    return None

## udf to convert bytes into human readable format
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

## function to get hashes and setup df
def get_hash_df(bucket_name):
    if "gs" in bucket_name:
        bucket_name = bucket_name.replace("gs://","")
    blobs = CS.list_blobs(bucket_name)
    hash_df = pd.DataFrame([{'blob': b.name,
			     'filetype':get_extension(b.name),
			     'md5_hash':b.md5_hash,
			     'size': b.size} for b in blobs])
    return hash_df


if __name__ == '__main__':
    ## collect args
    args = docopt(__doc__, version="get_dups 1.0")
    ## get summaries
    df = get_hash_df(args["<path_to_bucket>"])
    if args['--include-dirs'] is False:
        df = df.loc[[x is not None for x in df['filetype']]]
    df.loc[:,'duplicated'] = df['md5_hash'].duplicated()
    df.to_csv(args["<out_file>"],index=False,sep="\t")
