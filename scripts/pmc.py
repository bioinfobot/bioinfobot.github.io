#!/usr/bin/python3

# Standard library.
import tarfile
import os
from ftplib import FTP
import sys
import shutil


# Capture the root path where the data will be downloaded.
root_path = sys.argv[1]

if root_path[-1] == '/':
    compressed_file_dir = root_path + 'compressed/'
    os.mkdir(compressed_file_dir)
    uncompressed_file_dir = root_path + 'uncompressed/'
    os.mkdir(uncompressed_file_dir)
    all_file_dir = root_path + 'all/'
    os.mkdir(all_file_dir)
else:
    compressed_file_dir = root_path + '/compressed/'
    os.mkdir(compressed_file_dir)
    uncompressed_file_dir = root_path + '/uncompressed/'
    os.mkdir(uncompressed_file_dir)
    all_file_dir = root_path + '/all/'
    os.mkdir(all_file_dir)

ftp = FTP('ftp.ncbi.nlm.nih.gov')
ftp.login()
ftp.cwd('pub/pmc/manuscript/')
files = ftp.nlst()
files.sort()
files_to_download = []
for file in files:
    if '.txt.tar.gz' in file:
        files_to_download.append(file)

#files_to_download = [files_to_download[0]]

for file in files_to_download:
    print('Downloading: {} \n'.format(file))
    ftp.retrbinary("RETR " + file ,open(compressed_file_dir + file, 'wb').write)

# Untar files in the compressed folder to the uncompressed folder.
for file in files_to_download:
    file_path = compressed_file_dir + file
    tar = tarfile.open(file_path, "r:gz")
    print("Extracting: {}\n".format(file))
    tar.extractall(path=uncompressed_file_dir)
    tar.close()

# Recursively remove compressed file directory.
shutil.rmtree(compressed_file_dir)

# Recursively scan uncompressed directory and make a list of file paths. 
files = []
for entry in os.scandir(uncompressed_file_dir):
    if entry.is_dir():
        for entry_sub in os.scandir(entry.path):
            if entry_sub.is_file():
                files.append(entry_sub.path)
 
# Concatenate all the uncompressed text files into one.
all_file_name = all_file_dir + 'pmc_all.txt'
outfile = open(all_file_name, 'a')
print("Concatinating files.")
for file in files:
    with open(file, 'r') as f:
        for line in f:
            if line.rstrip().lower() == '   references':
                break
            else:
                outfile.write(line)
outfile.close()

# Recursively remove uncompressed file directory.
shutil.rmtree(uncompressed_file_dir)

# Tar and gz pmc_all file.
print("Compressing final file.")
os.chdir(all_file_dir)
tar_file = 'pmc_all.txt.tar.gz'
tar = tarfile.open(tar_file, "w:gz")
tar.add('pmc_all.txt', recursive=False)

# Remove uncompressed all file.
os.remove('pmc_all.txt')
