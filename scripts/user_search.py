#!/usr/bin/env python3
'''
Purpose: Search for new twitter users to follow with the selected keyword in their description.
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
logging.basicConfig(filename='../.log/usersearch.log',level=logging.INFO)

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

# Check the users that I am already following.
following = api.friends_ids('bioinfobot')

# Keyword to search for new users.
keywords =['Bioinformatics','Genomics','Metagenomics','Computational Biology','Structural Bioinformatics','Molecular Modelling','Next Generation Sequencing']

# Read/create skip users list.
if os.path.isfile('skip_users.pickle'):
    try:
        with open('skip_users.pickle', 'rb') as sup:
            # The protocol version used is detected automatically, so we do not have to specify it.
            skip_users = pickle.load(sup)
    except:
        logging.info("Exception occured in reading pickle!!")
else:
    try:
        skip_users=['bioinfobot']
        with open('skip_users.pickle', 'wb') as sup:
            # Pickle the 'skip_user' list using the highest protocol available.
            pickle.dump(skip_users, sup, pickle.HIGHEST_PROTOCOL)
    except:
        logging.info("Exception occured while creating pickle!!")

# Iterate over the keywords, search and add new users.
for keyword in keywords:
    logging.info('Searching for keyword: '+keyword)
    count = 0
    for i in range(1,40):
        try:
            users = api.search_users(q=keyword, count=20, page=i)
            for user in users:
                if user.id in following : # Continue if user is already being followed.
                    continue
                else:
                    count +=1
                    if user.screen_name not in skip_users:
                        logging.info('Following: '+ str(user.screen_name))
                        api.create_friendship(user.id) # Follow new user

        # Catch tweepy and connection related execptions.
        except tweepy.TweepError as te:
            logging.info("Tweepy exception occured!!")
            #logging.info(te.response.text) # This is to get the entire response as string.
            logging.info(str(te.args[0][0]['code']) + " " + te.args[0][0]['message'])
            if te.args[0][0]['code'] == 160: # Code 160 is for the users to whom follow request have been made.
                skip_member = te.args[0][0]['message'][35:-1]
                skip_users.append(skip_member)
            if te.args[0][0]['code'] == 162: # Code 162 is for the users who have blocked me.
                skip_member = str(user.screen_name)
                skip_users.append(skip_member)
            time.sleep(1)
        except ConnectionError as ce:
            logging.info("Connection error!!")
            logging.info(ce)
            time.sleep(10)

# Write the updated skip user list in the pickle.
try:
    with open('skip_users.pickle', 'wb') as sup:
        # Pickle the 'skip_user' list using the highest protocol available.
        pickle.dump(skip_users, sup, pickle.HIGHEST_PROTOCOL)
except:
    logging.info("Exception occured while writing pickle!!")

# Report the number of users found in the current run.
logging.info('No of new users found: '+str(count))
logging.info('//')
