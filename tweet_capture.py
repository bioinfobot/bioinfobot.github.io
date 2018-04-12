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
LAST MODIFIED   : 11/04/2018
'''
import tweepy
import logging
import datetime, time
import sqlite3

# Logging configuration
logging.basicConfig(filename='tweets_capture.log',level=logging.INFO)

# Twitter OAuth authentication
# This is where your key and secrete for twitter login should go.
# More info at https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creating a tweepy object
api = tweepy.API(auth)

# Subclass for stream listener
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
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
            conn = sqlite3.connect('bioinfotweet.db', isolation_level=None)
            conn.execute('PRAGMA journal_mode=wal')
            c = conn.cursor()
            c.execute("INSERT INTO tweetscapture (Date, ScreenName, UserID, TweetID, Text) values (?, ?, ?, ?, ?)", data)
            conn.commit()
            cdate="Tweet inserted at: "+str(datetime.datetime.now())
            logging.info(cdate)
            conn.close()

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
        stream.userstream(encoding='utf8')
		#print("Trying",cool)
    except Exception as ex:
        exname = str(ex)
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.info("Generic exception occurred")
        logging.info(message)
        if "not defined" in exname:
            break
        else:
            logging.info("Sleeping for 60 sec")
            time.sleep(60)
            continue

cdate="Stream finished at: "+str(datetime.datetime.now())
logging.info(cdate)