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
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creating a tweepy object
api = tweepy.API(auth)

timestamp = datetime.datetime.now()
logging.info(timestamp)
logging.info('Extracting following ids')

following = api.friends_ids('bioinfobot')

# Keyword to search
keyword ='Computational Biology'

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