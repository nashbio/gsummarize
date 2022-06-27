#!/usr/bin/python3
"""
Summarize a Google S3 bucket.

Usage:
  s3mmarize.py summarize <bucket_name> [--output-file=<out> --detailed]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --output-file=<out>  Path to save result file (can be URI, e.g. gs://) [default: None].
  --detailed      Output results with extra detail.



"""

## necessary imports
from google.cloud import storage
import re
import pandas as pd
from docopt import docopt

## setup
storage_client = storage.Client()

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

## udf to get dictionary summary of blob
def get_blob_dict(in_blob, bucket):
    ## load blob
    b_name = in_blob.name
    blob = bucket.get_blob(b_name)
    ## check if directory & set file extension
    file_ext = get_extension(b_name)
    ## get parent dir
    s = b_name.split("/")
    parent_dir = "/".join(s[0:(len(s)-1)])
    #parent_dir = s[0:(len(s)-1)]
    blob_dict = {
        "name": b_name,
        "exists": blob.exists(),
        "size": blob.size,
        "storage_class": blob.storage_class,
        "is_directory": file_ext is None,
        "file_extension": file_ext,
        "parent_directory": parent_dir
    }
    return blob_dict

## udf to summarize all blobs in a bucket
def s3mmarize_bucket(bucket_name):
  ## remove URI if included
  if "gs" in bucket_name:
    bucket_name = bucket_name.replace("gs://","")
  ## load gcp storage client and bucket
  bucket = storage_client.get_bucket(bucket_name)
  ## retreive all blobs
  blobs = storage_client.list_blobs(bucket_name)
  ## iterate blobs (exhausted) and save names
  #blob_list = [get_blob_dict(b, bucket) for b in blobs]
  blob_list = map(lambda x: get_blob_dict(x, bucket), blobs)
  ## collect metadata from blob
  return blob_list

## udf to create summary table
def get_s3mmary_table(df1, detailed = True):
  if detailed:
    ## groupby and create results
    both_df = df1.groupby(['parent_directory','file_extension']).sum().reset_index()[['parent_directory', 'file_extension', 'exists', 'size']]
    both_df = both_df.rename(columns={"exists":"count"})
    both_df['count'] = both_df['count'].astype(int)
    ## [optional] sort by directory size
    #both_df.parent_directory = both_df.parent_directory.astype("category")
    #both_df.parent_directory.cat.set_categories(list(size_df['parent_directory']),inplace=True)
    #both_df.sort_values("parent_directory")
    ## sort by file size
    both_df = both_df.sort_values("size",ascending=False)
    ## change to human readable sizes
    both_df['size'] = [sizeof_fmt(x) for x in both_df['size']]
    return both_df
  else:
    ## groupby and create results
    size_df = pd.DataFrame(df1.groupby('parent_directory').sum()['size'])
    ## sort by dir size
    size_df = size_df.sort_values('size',ascending=False)
    ## change to human readable sizes
    size_df['size'] = [sizeof_fmt(x) for x in size_df['size']]
    size_df = size_df.reset_index()
    return size_df


if __name__ == '__main__':
  ## collect args
  args = docopt(__doc__, version="s3mmarize 1.0")
  ## get summaries
  all_data = s3mmarize_bucket(args['<bucket_name>'])
  all_data = pd.DataFrame(all_data)
  s3mm = get_s3mmary_table(all_data, detailed = args['--detailed'])
  if args['--output-file'] == 'None':
    print(s3mm)
  else:
    s3mm.to_csv(args['--output-file'])
