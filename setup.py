from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup (
 name = 'gsummarize',
 description = 'A simple command line tool to summarize Google cloud storage buckets.',
 version = '1.0.1',
 packages = find_packages(), # list of all packages
 install_requires = ["pandas", "docopt", "google-cloud-storage"],
 python_requires='>=2.7', # any python greater than 2.7
 author="Coleman Harris",
 keyword="google, cloud, storage, bucket, gsutil",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
 url='https://github.com/nashbio/gsummarize',
 author_email='coleman@nashvillebiosciences.com',
)