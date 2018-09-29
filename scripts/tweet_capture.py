#!/usr/bin/env python3

'''
DESCRIPTION     : Captures streaming tweets via Twitter OAuth authentication.
DEPENDENCIES    : tweepy, sqlite3
USAGE           : nohup python3 tweet_capture.py &
INPUT           : no command line input
OUTPUT          : Stores captured tweets in a SQLite3 database
                  Generates a log file "tweets_capture.log" 
AUTHOR          : Dr. Rohit Farmer
EMAIL           : rohit.farmer@gmail.com
'''

# Standard library
import logging
import datetime, time
import sqlite3
import pickle
import os

# External library
import tweepy

# Logging configuration
logging.basicConfig(filename='../.log/tweets_capture.log',level=logging.INFO)

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
#api.update_status('Start Streaming')

# # Get a list of the users that i am following.
# following = api.friends_ids('bioinfobot')

# Read following users list.
if os.path.isfile('following.pickle'):
    try:
        with open('following.pickle', 'rb') as fol:
            # The protocol version used is detected automatically, so we do not have to specify it.
            following = []
            following_dict = pickle.load(fol)
            for key, value in following_dict.items():
                following.append(value)
    except Exception as ex:
        logging.info("Exception occured in reading pickle!!")
        print(ex)
print(following[0:10])
following = following[0:10]

# Subclass for stream listener
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        if status.lang == 'en' and 'RT'.upper() not in status.text :
            stat = status.text
            stat = stat.replace('\n','')
            stat = stat.replace('\t','')
            user_id = status.user.id_str
            stat_id = status.id_str
            create = str(status.created_at)
            name = status.user.screen_name
            data = (create, name, user_id, stat_id, stat)
            #Connecting to SQLite3 database
            try:
                db_file = '../../db/bioinfotweet.db'
                conn = sqlite3.connect(db_file, isolation_level=None)
                conn.execute('PRAGMA journal_mode=wal') # This will let concurrent read and write to the database. 
                c = conn.cursor()
                c.execute("INSERT INTO tweetscapture (Date, ScreenName, UserID, TweetID, Text) values (?, ?, ?, ?, ?)", data)
                conn.commit()
                cdate="Tweet inserted at: "+str(datetime.datetime.now())
                logging.info(cdate)
                conn.close()
            except Exception as ex:
                exname = str(ex)
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.info("Sqlite3 database exception occurred.")
                logging.info(message)

    def on_error(self, status_code):
        if status_code == 420:
            cdate = "Error code 420 at:"+str(datetime.datetime.now())
            logging.info(cdate)
            logging.info("Sleeping for 15 mins")
            time.sleep(900)
        return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
cdate="Stream started at: "+str(datetime.datetime.now())
logging.info(cdate)

while True:
    try:
        #stream.userstream(encoding='utf8')
        stream.filter(follow=following)
    except Exception as ex:
        exname = str(ex)
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.info("Generic exception occurred.")
        logging.info(message)
        if "not defined" in exname:
            break
        else:
            logging.info("Sleeping for 60 sec")
            time.sleep(60)
            continue

cdate="Stream finished at: "+str(datetime.datetime.now())
logging.info(cdate)
