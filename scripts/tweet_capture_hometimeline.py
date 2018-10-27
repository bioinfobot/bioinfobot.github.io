#!/usr/bin/env python3

'''
DESCRIPTION     : Captures tweets from the user timeline.
DEPENDENCIES    : tweepy, sqlite3
OUTPUT          : Stores captured tweets in a SQLite3 database
                  Generates a log file "tweets_capture_hometimeline.log" 
AUTHOR          : Dr. Rohit Farmer
EMAIL           : rohit.farmer@gmail.com
'''

# Standard library
import logging
import datetime, time
import sqlite3

# External library
import tweepy

# Logging configuration
logging.basicConfig(filename='../.log/tweets_capture_hometimeline.log',level=logging.INFO)

# Twitter OAuth authentication
# This is where your key and secrete for twitter login should go.
# More info at https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/
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

db_file = '../../db/bioinfotweet.db'
conn = sqlite3.connect(db_file, isolation_level=None)
conn.execute('PRAGMA journal_mode=wal') # This will let concurrent read and write to the database. 
c = conn.cursor()
c.execute("SELECT * FROM tweetscapture ORDER BY Date DESC LIMIT 1")
tweet_id = c.fetchone()[3]

# Fetch recent tweets 
for status in api.home_timeline(since_id=tweet_id, tweet_mode='extended'):
    if status.lang == 'en' and 'RT'.upper() not in status.full_text :
        stat = status.full_text
        stat = stat.replace('\n','')
        stat = stat.replace('\t','')
        user_id = status.user.id_str
        stat_id = status.id_str
        create = str(status.created_at)
        name = status.user.screen_name
        data = (create, name, user_id, stat_id, stat)
        #Connecting to SQLite3 database
        try:
            # db_file = '../../db/bioinfotweet.db'
            # conn = sqlite3.connect(db_file, isolation_level=None)
            # conn.execute('PRAGMA journal_mode=wal') # This will let concurrent read and write to the database. 
            # c = conn.cursor()
            c.execute("INSERT INTO tweetscapture (Date, ScreenName, UserID, TweetID, Text) values (?, ?, ?, ?, ?)", data)
            conn.commit()
            cdate="Tweet inserted at: "+str(datetime.datetime.now())
            logging.info(cdate)
            # conn.close()
        except Exception as ex:
            exname = str(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.info("Sqlite3 database exception occurred.")
            logging.info(message)

conn.close()
