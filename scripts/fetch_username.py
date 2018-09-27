#!/usr/bin/env python3

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

# External library
import tweepy

# Create a log file.
logging.basicConfig(filename='../.log/fetchusername.log',level=logging.INFO)

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

# Print a timestamp in the log file.
timestamp = datetime.datetime.now()
logging.info(timestamp)

# Fetch the list of the users that I am already following.
following_ids = api.friends_ids('bioinfobot')

print("Total number of friends:", len(following_ids))

# Read/create skip users list.
if os.path.isfile('following.pickle'):
    try:
        with open('following.pickle', 'rb') as fol:
            # The protocol version used is detected automatically, so we do not have to specify it.
            following = pickle.load(fol)
    except:
        logging.info("Exception occured in reading pickle!!")
else:
    try:
        following={}
        following = following.fromkeys(following_ids)
        with open('following.pickle', 'wb') as fol:
            # Pickle the 'following' dicitonary using the highest protocol available.
            pickle.dump(following, fol, pickle.HIGHEST_PROTOCOL)
    except:
        logging.info("Exception occured while creating pickle!!")

limit = 830

keys = list(following.keys())

count = 0
for key in keys:
    if following[key] == None:
        count += 1
        user_info = api.get_user(key)
        name = user_info.screen_name
        following[key] = name
        if count == limit:
            break

# Print the total number of users with no screen names yet.
count_none = 0
for key in keys:
    if following[key] == None:
        count_none += 1
print("Total number of friend with no screen name yet:", count_none)

# Print the remaining number of api calls.
print("Number of api calls remainig:",api.rate_limit_status()['resources']['users']['/users/show/:id'])

# Write the updated following dictionary.
try:
    with open('following.pickle', 'wb') as fol:
        # Pickle the 'skip_user' list using the highest protocol available.
        pickle.dump(following, fol, pickle.HIGHEST_PROTOCOL)
except:
    logging.info("Exception occured while writing pickle!!")
