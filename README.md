# gsummarize

A command line tools to summarize files in a Google cloud S3 bucket. The `summary` command generates a tab-delimited summary of files, file types, and storage usage. The `dedup` command generates a tab-delimited list of duplicate files in a Google cloud S3 bucket. Note that given occasional comma's in filenames, tab-delimited output is by default -- use `--cd` to override and save outputs as comma-delimited files.

For proper usage, either run the module in a the Google Cloud Shell or set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the proper service account key. 

### Additional features

- After setting Google credentials, the output CSV can be specified as a `gsutil` URI to save the resulting file to a GCP bucket, e.g. `gs://path/to/bucket/summary.csv`.
- Users can also summarize or deduplicate sub-directories of buckets, e.g. `gs://path/to/bucket/sub/dir`.

## Installation

Download the most recent release [here](https://github.com/nashbio/gsummarize/releases/) and run the following command:

```python
pip install gsummarize-1.0.2.tar.gz
```

## `summary` example

The following command summarizes the bucket, `gs://path/to/bucket`, and outputs a detailed CSV in the `output.csv`. 


```bash
gsummarize summarize gs://path/to/bucket output.csv --detailed
```

This produces results that look like the following:

| **parent_directory** | **file_extension** | **count** | **size** |
| -------------------- | ------------------ | --------- | -------- |
| /path/to/dir1        | gz                 | 24        | 1.6GiB   |
| /path/to/dir2        | json               | 21        | 203.7MiB |
| /path/to/dir3        | docx               | 34        | 104.3MiB |
| /path/to/dir3        | pdf                | 31        | 85.7MiB  |
| /path/to/dir1        | txt                | 111       | 71.1MiB  |

And a non-detailed (e.g. without the `--detailed` flag) version groups just by the `parent_directory` and produces output like the following:

| **parent_directory** | **size** | **count** |
| -------------------- | -------- | --------- |
| /path/to/dir1        | 1.6GiB   | 33        |
| /path/to/dir2        | 203.7MiB | 28        |
| /path/to/dir3        | 104.3MiB | 16        |
| /path/to/dir3        | 85.7MiB  | 67        |
| /path/to/dir1        | 71.1MiB  | 11        |

---

## `dedup` exmaple

The following command lists the MD5 hashes of all blobs in the bucket, `gs://path/to/bucket`, determines duplicate hashes, and outputs the resulting table to `output.csv`. The `--include-dirs` flag will include directories when determining duplicates. To only output the duplicate files for a given bucket, use the `--only-dups` option.

```bash
gsummarize dedup gs://path/to/bucket output.csv --include-dirs
```

This produces results that look like the following:

| **blob**       | **parent_dir** | **file_extension** | **md5_hash** | **size** | **duplicated** |
| -------------- | -------------- | ------------------ | ------------ | -------- | -------------- |
| /path/to/dir1  | dir1           | NA                 | abcd1234     | 11       | FALSE          |
| /path/to/dir2  | dir2           | NA                 | abcd4231     | 11       | FALSE          |
| /path/to/file1 | dir1           | csv                | wxyz1234     | 240      | TRUE           |
| /path/to/file2 | dir1           | gz                 | abcd5678     | 38       | FALSE          |
| /path/to/file3 | dir2           | csv                | wxyz1234     | 167      | TRUE           |

