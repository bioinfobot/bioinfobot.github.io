#!/usr/bin/env python3

'''
Purpose: Testing script.
External Dependencies: Tweepy
Author: Rohit Farmer
'''

# Standard library
import logging
import datetime, time
import os
import pickle
from ftplib import FTP

# External library
import tweepy


# OAuth authentication
with open('../../cred/bioinfobotmain.txt', 'r') as f: # Reading the credentials from a text file.
    creds = f.readlines()
    consumer_key = creds[0].rstrip()
    consumer_secret = creds[1].rstrip()
    access_token = creds[2].rstrip()
    access_token_secret = creds[3].rstrip()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

# Creating a tweepy object
api = tweepy.API(auth)

# To get the rate limit status on various api calls.
print(api.rate_limit_status()['resources']['users']['/users/show/:id'])

# Check the users that I am already following.
# following = api.friends_ids('bioinfobot')
# print ("Type: {}".format(type(following)))
# print (following)

# following_screen_names = []
# count = 0
# for id in following:
#     count +=1
#     print (count,"\n")
#     user_info = api.get_user(id)
#     name = user_info.screen_name
#     #print("Type: {}".format(type(name)))
#     print("Name: {}".format(name))
#     following_screen_names.append(name)
# print ("Total no of users: {}".format(len(following_screen_names)))

# Check pubmed ftp
ftp = FTP('ftp.ncbi.nlm.nih.gov')
ftp.login()
ftp.cwd('pub/pmc/manuscript/')
files = ftp.nlst()
files.sort()
files_to_download = []
for file in files:
    if '.txt.tar.gz' in file:
        files_to_download.append(file)
print(files_to_download)

ftp.retrbinary("RETR " + files_to_download[0] ,open("/home/rohit/Downloads/" + files_to_download[0], 'wb').write)