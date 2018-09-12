#!/usr/bin/env python3
'''
Purpose: Search for new twitter users to follow with the selected keyword in their description.
External Dependencies: Tweepy
Author: Rohit Farmer
Last updated: 9 March 2018
'''

import tweepy
import logging
import datetime, time

logging.basicConfig(filename='usersearch.log',level=logging.INFO)

# OAuth authentication
with open('../cred/bioinfobotmain.txt', 'r') as f:
    creds = f.readlines()
    consumer_key = creds[0].rstrip()
    consumer_secret = creds[1].rstrip()
    access_token = creds[2].rstrip()
    access_token_secret = creds[3].rstrip()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

# Creating a tweepy object
api = tweepy.API(auth)

timestamp = datetime.datetime.now()
logging.info(timestamp)
logging.info('Extracting following ids')

following = api.friends_ids('bioinfobot')

# Keyword to search
keyword ='Bioinformatics'

count = 0
for i in range(1,40):
    try:
        users = api.search_users(q=keyword, count=20, page=i)
        for user in users:
            if user.id in following : # Continue if user is already being followed
                continue
            else:
                count +=1
                if user.screen_name != 'PootBlog' and user.screen_name != 'fourmodern': # Filter/skip users
                    logging.info('Following: '+ str(user.screen_name))
                    api.create_friendship(user.id) # Follow new user

    # Catch execptions
    except tweepy.TweepError:
        print("Tweepy exception occured!!")
        time.sleep(1)
    except ConnectionError:
        print("Connection error!!")
        time.sleep(10)

logging.info('No of new users found: '+str(count))
logging.info('//')
