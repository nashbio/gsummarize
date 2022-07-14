## s3mmarize

A bash script to summarize files in a GCP S3 cloud bucket. It recursively organizes all files in a cloud bucket by their parent directory and file extension, and tallies the number of that file type and the size of that file for each directory & file extension pair.

For proper usage, either run the module in a the Google Cloud Shell or set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the proper service account key.

Note that after setting these credentials, the output CSV can be specified as a `gsutil` URI (e.g., a user can save the resulting file to a GCP bucket).


### Example

The following command summarizes the bucket, `gs://path/to/bucket`, and outputs a detailed CSV in the `output.csv`. 


```{bash}
s3mmarize "gs://path/to/bucket" "output.csv" --detailed
```

This produces results that look like the following:

|         | **parent_directory** | **file_extension** | **count** | **size** |
| ------- | -------------------- | ------------------ | --------- | -------- |
| **23**  | /path/to/dir1        | gz                 | 24        | 1.6GiB   |
| **36**  | /path/to/dir2        | json               | 21        | 203.7MiB |
| **30**  | /path/to/dir3        | docx               | 34        | 104.3MiB |
| **19**  | /path/to/dir3        | pdf                | 31        | 85.7MiB  |
| **43**  | /path/to/dir1        | txt                | 111       | 71.1MiB  |

And a non-detailed (e.g. without the `--detailed` flag) version groups just by the `parent_directory` and produces output like the following:

|        | **parent_directory** | **size** | **count** |
| ------ | -------------------- | -------- | --------- |
| **23** | /path/to/dir1        | 1.6GiB   | 33        |
| **36** | /path/to/dir2        | 203.7MiB | 28        |
| **30** | /path/to/dir3        | 104.3MiB | 16        |
| **19** | /path/to/dir3        | 85.7MiB  | 67        |
| **43** | /path/to/dir1        | 71.1MiB  | 11        |

---

---

# dedup-bucket

A Python script that creates a table for duplicate files in a GCP S3 bucket based on their MD5 hashes. Note also that the script determines the filetype and size (in bytes) of the file. 

For proper usage, either run the module in a the Google Cloud Shell or set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the proper service account key.

Note that after setting these credentials, the output CSV can be specified as a `gsutil` URI (e.g., a user can save the resulting file to a GCP bucket).

### Example

The following command lists the MD5 hashes of all blobs in the bucket, `lorem`, determines duplicate hashes, and outputs the resulting table to `output.csv`. The `--include-dirs` flag will include directories when determining duplicates. 

```bash
<<<<<<< HEAD
<<<<<<< HEAD
dedup-bucket.py "gs://path/to/bucket" "output.csv" --include-dirs
=======
dedup-bucket "gs://path/to/bucket" "output.csv" --include-dirs
>>>>>>> 92bcac3 (reformat dedup script)
=======
dedup-bucket.py "gs://path/to/bucket" "output.csv" --include-dirs
>>>>>>> 644ec6d (Update README)
```

This produces results that look like the following:

| **blob**       | filetype | **md5_hash** | size | **duplicated** |
| -------------- | -------- | ------------ | ---- | -------------- |
| /path/to/dir1  | NA       | abcd1234     | 11   | FALSE          |
| /path/to/dir2  | NA       | abcd4231     | 11   | FALSE          |
| /path/to/file1 | csv      | wxyz1234     | 240  | TRUE           |
| /path/to/file2 | gz       | abcd5678     | 38   | FALSE          |
| /path/to/file3 | csv      | wxyz1234     | 167  | TRUE           |

