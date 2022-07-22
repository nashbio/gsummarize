from setuptools import setup, find_namespace_packages

setup (
 name = 'gsummarize',
 description = 'A simple command line tool to summarize Google cloud storage buckets.',
 version = '1.0.1',
 packages = ['src','src.gsummarize'],
 install_requires = ["pandas", "docopt", "google-cloud-storage"],
 author="Coleman Harris",
 entry_points={
        'console_scripts': [
            'gsummarize = src.gsummarize:run_gsummarize',
        ]
 }
)