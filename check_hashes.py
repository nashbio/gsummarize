#!/usr/bin/python3
## imports and storage setup
from google.cloud import storage
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
	blobs = CS.list_blobs(bucket_name)
	hash_df = pd.DataFrame([{'blob': b.name,
							 'filetype':get_extension(b.name),
							 'md5_hash':b.md5_hash, 
							 'size': b.size} for b in blobs])
	return hash_df

nedr = get_hash_df(BUCKET1)
nbgr = get_hash_df(BUCKET2)

## subset to files and mark dups
nedr_files = nedr.loc[[x is not None for x in nedr['filetype']]]
nedr_files.loc[:,'duplicated'] = nedr_files['md5_hash'].duplicated()
nedr_summary = nedr_files.groupby("duplicated").sum()
nedr_summary['readable_size'] = [sizeof_fmt(int(s)) for s in nedr_summary.values]

## subset to files and mark dups
nbgr_files = nbgr.loc[[x is not None for x in nbgr['filetype']]]
nbgr_files.loc[:,'duplicated'] = nbgr_files['md5_hash'].duplicated()
nbgr_summary = nbgr_files.groupby("duplicated").sum()
nbgr_summary['readable_size'] = [sizeof_fmt(int(s)) for s in nbgr_summary.values]

