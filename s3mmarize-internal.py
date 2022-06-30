#!/usr/bin/python3
"""
Summarize a Google S3 bucket.

Usage:
  s3mmarize.py summarize <bucket_name> <names_file> <vals_file> <out_file> [--detailed]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --detailed    Use file extensions in grouped results.

"""

## necessary imports
import os
import pandas as pd
from docopt import docopt

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

## udf to retreive parent directory from name
def get_parent_dir(b_name):
    s = b_name.split("/")
    return "/".join(s[0:(len(s)-1)])

## udf to format results df
def setup_final_df(both_df):
    both_df = both_df.rename(columns={"exists":"count"})
    both_df['count'] = both_df['count'].astype(int)
    both_df = both_df.sort_values("size",ascending=False)
    both_df['size'] = [sizeof_fmt(x) for x in both_df['size']]

    return both_df

## udf to summarize
def make_summary(names,vals,bucket,detailed=False):
    ## read files
    x = pd.read_csv(names,header=None)
    y = pd.read_csv(vals,header=None)
    os.remove(names)
    os.remove(vals)

    ## combine into one df
    df1 = y.rename(columns={0:'size', 1:'timestamp'})
    df1['name'] = [b.replace(bucket,"") for b in x[0]]
    df1['parent_directory'] = [get_parent_dir(b) for b in df1['name']]
    df1['file_extension'] = [get_extension(b) for b in df1['name']]
    df1['exists'] = 1

    ## make grouped df
    if detailed:
        both_df = df1.groupby(['parent_directory','file_extension']).sum().reset_index()[['parent_directory', 'file_extension', 'exists', 'size']]
    else:
        both_df = df1.groupby(['parent_directory']).sum().reset_index()

    return setup_final_df(both_df)

if __name__ == '__main__':
    ## collect args
    args = docopt(__doc__, version="s3mmarize 1.0")
    ## get summaries
    df = make_summary(args["<names_file>"],args["<vals_file>"],args["<bucket_name>"],args["--detailed"])
    print("Printing summary:")
    print(df)
    df.to_csv(args["<out_file>"],index=False)
