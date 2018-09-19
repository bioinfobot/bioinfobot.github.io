# Bioinfobot
## https://rohitfarmer.github.io/bioinfobot/
## Introduction

Bioinformatics Bot is an automated tool that captures trends in the bioinformatics industry by analysing tweets posted by bioinformaticians from all over the world. Tweets are captured in real time, tweeted by the users followed by @bioinfobot twitter account. This bot consists of a collection of scripts written in python that apart from capturing Twitter data in real time also periodically search and follow new Twitter users who have bioinformatics, genomics, metagenomics, computational biology, structural bioinformatics, molecular modelling or next-generation sequencing in their Twitter bio. Many of the well-known bioinformaticians/computational biologist that might be missed by the automated search and follow procedure are also manually selected and followed by the creator and maintainer of this service (Rohit Farmer, PhD). The analysis presented here is the result of the analysis of last month's tweets.

The bot scripts are running in a Google Cloud Platform instance and the website is hosted via GitHub pages. Tweepy is the main module that is being used to follow people, collect streaming tweets and fetch tweet related metadata. The captured tweet data is stored in an Sqlite3 database. Natural Language Toolkit (NLTK) is used for analysing tweets. At the moment tweet analysis consists of producing a list of "Top 20 Words", "Top 20 Tweeters", "Top 20 Hashtags" and "Popular Programming Languages & Frameworks". The processed results per month are presented and stored in the form of a word cloud image and a JSON file respectively. Word cloud is generated using wordcloud python module. All the data provided on this website is copyleft and free to use.

In the future, utilizing and manually labelling a set of randomly selected tweets into bioinformatics related and unrelated will be used to build a deep learning predictive model. The predictive model will be used to filter tweets that are bioinformatics related and re-tweet them by the @bioinfobot twitter account. Thus, by following just @bioinfobot, users will be able to receive bioinformatics related tweets from thousands of bioinformaticians worldwide. Collecting and analysing data over the years would eventually give us a view of how bioinformatics industry has grown over time. A list of diseases will also be included in the analysis procedure.

** This project has been a fun way of learning Python, database connection with python, natural language processing, deep learning, JavaScript and Google Cloud Platform. Anyone interested in collaborating and learning along the way is most welcomed. For any queries or collaborations please contact Dr. Rohit Farmer at rohit [dot] farmer [at] gmail [dot] com.

## Scripts Used

**tweet_capture.py:** Captures streaming tweets via Twitter OAuth authentication.  
*Usage: nohup python3 tweet_capture.py &  # to keep it running at the background*

**bioinfotweet.db:** An SQLite3 database to store captured tweets by tweet_capture.py script.  
*Database schema:*  
```sqlite
sqlite> .schema
CREATE TABLE "tweetscapture" (
    "Date" TEXT NOT NULL,
    "ScreenName" TEXT NOT NULL,
    "UserID" TEXT NOT NULL,
    "TweetID" TEXT NOT NULL,
    "Text" TEXT NOT NULL
)
```

**tweet_analyse.py:** Analyse tweet database and generate wordcloud and stats in a JSON file.  
*Usage: python3 tweet_analyse.py*  
*Note: might need to change path where the wordcloud and JSON file be sent.*

**twitterfunc.py:** Collection of functions.  
*Usage: from twitterfunc import*  

**user_search.py:** Search for new twitter users to follow with the selected keyword in their description.  
*Usage: python3 user_search.py*  
*Note: Change keywords (e.g. bioinformatics, computational biology, structural bioinformatics)*
