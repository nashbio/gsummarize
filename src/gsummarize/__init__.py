#!/usr/bin/python3
"""
Summarize a Google S3 bucket.
Use `summary` to generate a tab-delimited summary for the number of files and storage in a Google S3 bucket.
Use `dedup` to generate a tab-delimited list of duplicate files in a Google S3 bucket.

Usage:
  gsummarize summarize <bucket_name> <out_file> [--cd] [--detailed]
  gsummarize dedup <bucket_name> <out_file> [--cd] [--include-dirs] [--only-dups]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --cd          Saves output file as a comma delimited CSV (tab-delimited recommended).
  --detailed    Use file extensions in grouped summary results (for use with `summarize`).
  --include-dirs  Include directories in dedup summaries (for use with `dedup`).
  --only-dups  Saves output file with only the duplicate files (for use with `dedup`).

"""

## necessary imports
import pandas as pd
from docopt import docopt
from google.cloud import storage

## udf to get out file delimiter
def get_delim(commas):
    if commas:
        return ","
    return "\t"

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

## udf to get blobs
def get_blobs(bucket_name):
    print("Getting blobs from Google...")
    CS = storage.Client()
    bucket_name = bucket_name.replace("gs://","")
    if "/" in bucket_name:
        blist = bucket_name.split("/")
        bname = blist.pop(0)
        prefix = "/".join(blist)
        return CS.list_blobs(bname, prefix=prefix)
    return CS.list_blobs(bucket_name)

## udf to create base_df
def create_base_df(blobs):
    print("Organizing bucket attributes...")
    return pd.DataFrame([{'blob': b.name,
                'parent_directory': get_parent_dir(b.name),
                 'file_extension': get_extension(b.name),
                 'hash': b.crc32c,
                 'size': b.size} for b in blobs])

## udf to format results df
def setup_summarize_df(both_df):
    both_df = both_df.rename(columns={"exists":"count"})
    both_df['count'] = both_df['count'].astype(int)
    both_df = both_df.sort_values("size",ascending=False)
    both_df['size'] = [sizeof_fmt(x) for x in both_df['size']]

    return both_df

## udf to summarize
def summarize(bucket_name, detailed=False):
    ## get blobs & base df
    blobs = get_blobs(bucket_name)
    df = create_base_df(blobs)

    ## setup for summarize
    df['exists'] = 1
    df = df.drop(columns=['hash'])

    ## make grouped df
    if detailed:
        both_df = df.groupby(['parent_directory','file_extension']).sum().reset_index()[['parent_directory', 'file_extension', 'size', 'exists']]
    else:
        both_df = df.groupby(['parent_directory']).sum().reset_index()

    return setup_summarize_df(both_df)

## function to get hashes and setup df
def dedup(bucket_name, include_dirs=False):
    blobs = get_blobs(bucket_name)
    df = create_base_df(blobs)

    if include_dirs is False:
        df = df.loc[[x is not None for x in df['file_extension']]]
    df.loc[:,'duplicated'] = df['hash'].duplicated(keep=False)

    return df

## udf to print summary, save csv
def finish_df(odf, out_file, sep):
    print("Printing summary...")
    print(odf.head().to_string(index=False))
    odf.to_csv(out_file,index=False,sep=sep)

## function to run module
def run_gsummarize():
    ## collect args
    args = docopt(__doc__, version="gsummarize 1.0.1")
    sep = get_delim(args['--cd'])
    ## get summaries
    if args['summarize']:
        ## summarize
        odf = summarize(args["<bucket_name>"], args['--detailed'])
        finish_df(odf, args["<out_file>"], sep)
        
    elif args['dedup']:
        ## dedup
        odf = dedup(args["<bucket_name>"], args['--include-dirs'])
        if(args['--only-dups']):
            odf = odf.loc[odf['duplicated']]
        finish_df(odf, args["<out_file>"], sep)
    print("Saved output to {}.".format(args["<out_file>"]))
