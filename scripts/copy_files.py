#!/usr/bin/env python3

# Standard library.
import os
import shutil

path = '/home/r/rohit/projects/binf/pmc/uncompressed'

folders = []
files = []
 
for entry in os.scandir(path):
    if entry.is_dir():
        # folders.append(entry.path)
        for entry_sub in os.scandir(entry.path):
            if entry_sub.is_file():
                files.append(entry_sub.path)
    # elif entry.is_file():
    #     files.append(entry.path)
 
# print('Folders:')
# print(folders)

# print('Files')
# print(files)

outfile = '/home/r/rohit/projects/binf/pmc/all/pmc_all.txt'

outfile = open(outfile, 'a')

for file in files:
    with open(file, 'r') as f:
        for line in f:
            if line.rstrip().lower() == '   references':
                break
            else:
                outfile.write(line)

outfile.close()