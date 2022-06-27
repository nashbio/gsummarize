## s3mmarize

A Python module to summarize files in a GCP S3 cloud bucket. It recursively organizes all files in a cloud bucket by their parent directory and file extension, and tallies the number of that file type and the size of that file for each directory & file extension pair.

For proper usage, either run the module in a the Google Cloud Shell or set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the proper service account key.


### Example

The following command summarizes the bucket, `gs://path/to/bucket`, and outputs a detailed CSV in the `gs://path/to/output.csv`. 


```{bash}
s3mmarize.py summarize gs://path/to/bucket --output-file=gs://path/to/output.csv --detailed
```

This produces results that look like the following:

|         | **parent_directory** | **file_extension** | **count** | **size** |
| ------- | -------------------- | ------------------ | --------- | -------- |
| **23**  | /path/to/dir1        | gz                 | 24        | 1.6GiB   |
| **36**  | /path/to/dir2        | json               | 21        | 203.7MiB |
| **30**  | /path/to/dir3        | docx               | 34        | 104.3MiB |
| **19**  | /path/to/dir3        | pdf                | 31        | 85.7MiB  |
| **43**  | /path/to/dir1        | txt                | 111       | 71.1MiB  |