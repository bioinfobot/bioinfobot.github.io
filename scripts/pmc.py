#!/usr/bin/env python3

# Standard library.
import tarfile
import os

# External library.
import wget

# List of files in pmc as of 27 Sep 2018
links = ['ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/manuscript/PMC001XXXXXX.txt.tar.gz',
         'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/manuscript/PMC002XXXXXX.txt.tar.gz',
         'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/manuscript/PMC003XXXXXX.txt.tar.gz',
         'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/manuscript/PMC004XXXXXX.txt.tar.gz',
         'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/manuscript/PMC005XXXXXX.txt.tar.gz',
         'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/manuscript/PMC006XXXXXX.txt.tar.gz']

for link in links:
    wget.download(link)


# Untar files in the current directory.
files = os.listdir()
for file in files:
    if 'tar.gz' in file:
        tar = tarfile.open(file, "r:gz")
        tar.extractall()
        tar.close()

