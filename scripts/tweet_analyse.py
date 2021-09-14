#!/usr/bin/env python3

'''
DESCRIPTION     : Analyse tweet database and generate wordcloud.
DEPENDENCIES    : nltk, wordcloud
USAGE           : python3 tweet_analyse.py
OUTPUT          : Generates a data file in JSON format
                  Generates a wordcloud image in jpg format
'''
# Standard library.
import re
from twitterfunc import tweet_clean
import datetime
import sqlite3
from collections import OrderedDict

# External library.
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk import FreqDist
from wordcloud import WordCloud
import json

# Establish connection to Sqlite3 database.
conn = sqlite3.connect('../../db/bioinfotweet.db')
c = conn.cursor()

# Extract tweets' text from the database followed by filtering and tokenizing.
filteredText = []
rowCount = 0
totalHash = []
totalUsers = []
totalTweetID = []
prog_lang = []
total_lang = {}

# Calculate date.
current_utc = str(datetime.datetime.now(datetime.timezone.utc))
year = current_utc[0:4]
month = current_utc[5:7]

if month == 1: # This is to check for the year change (January month)
    month = 12
    year = int(year) - 1
else:
    month = int(month) - 1

name = "{0}-{1}".format(year, str(month).zfill(2)) # name here means yyyy-mm

for row in c.execute('SELECT * FROM tweetscapture ORDER BY Date DESC'):
    creationDate = row[0]
    creation_month = int(creationDate[5:7])
    if name in creationDate:
        rowCount += 1
        screenName = row[1]
        totalUsers.append(screenName)
        userID = row[2]
        tweetID = row[3]
        tweetText = tweet_clean(row[4].lower())
        stopWords = list(stopwords.words("english"))
        myStopWords = ['also', 'bad', 'cant', 'could', 'dont', 'day', 'great', 'get', 'good', 'hear',
                       'here', 'ive', 'im', 'like', 'latest', 'new', 'news', 'oh', 'people', 'see',
                       'today', 'top', 'the', 'twitter', 'thats', 'thanks', 'us', 'using', 'work',
                       'would','x']
        stopWords = stopWords + myStopWords
        words = word_tokenize(tweetText)
        tagged = pos_tag(words)
        filteredSentence = [w for w in words if w not in stopWords]
        filteredText += filteredSentence
        hashMatch = re.findall('#\w+', row[4].lower())
        if not hashMatch:
            continue
        else:
            totalHash += hashMatch
    # elif creation_month < month:
    #     break
    elif month == 12:
        print("Analysis Month: {}".format(month))
        if creation_month == 11:
            print("Creation Month: {}".format(creation_month))
            break
    else:
        if creation_month < month:
            print("Analysis Month: {}".format(month))
            print("Creation Month: {}".format(creation_month))
            break

# Open txt file with the list of programming languages
file_prog = open("programminglang.txt", "r")
for i in file_prog:
    prog_lang.append(i.rstrip())
    tempdict = {i.rstrip(): 0}
    total_lang.update(tempdict)

for ha in totalHash:
    for pro in prog_lang:
        if "#"+pro.lower() == ha:
            total_lang[pro] += 1

totalWords = len(filteredText)
freq = FreqDist(filteredText)
uniqueWords = len(freq)
del filteredText

stopHash = ['#twitter', '#tweeted']  # Hastags of no interest
totalHash[:] = [h for h in totalHash if h not in stopHash]  # Get ride of any cell with stop hashtags
hashFreq = FreqDist(totalHash)
usersFreq = FreqDist(totalUsers)
lang_freq = FreqDist(total_lang)

# Generate a word cloud image.
wordcloud = WordCloud(font_path='Actor-Regular.ttf', width=1500, height=500,
                      max_words=500, stopwords=None, background_color='whitesmoke',
                      max_font_size=None, font_step=1, mode='RGB',
                      collocations=True, colormap=None, normalize_plurals=True).generate_from_frequencies(freq)
imagePath = "/home/bioinformaticsbot/bioinfobot.github.io/images/" + name + '.png'  # Put the actual path of the word cloud image produced in the previous step
wordcloud.to_file(imagePath)
imageUrl = "https://bioinfobot.github.io/images/" + name + '.png'


def dict_value_sort_return_top(frquency_dict, maxreturn):
    """Sort the dictionary according to values and return a list of top n elements"""
    dictionary_sorted = OrderedDict(sorted(frquency_dict.items(), key=lambda t: t[1], reverse=True))
    # Store top values in an array
    # Change maxCount value to extract top n elements
    count = 0
    top_elements = []
    for k, v in dictionary_sorted.items():
        # Key and value pairs are stored in the form of a tuple in the topWords array
        # Another dictionary is not created here in order to preserve the sorted order
        top_elements.append((k, v))
        count += 1
        if count >= maxreturn:
            break
    return top_elements


# Sort and store top n elements in an array
topWords = dict_value_sort_return_top(freq, 20)
del freq  # Delete freq variable to free memory space
hashFreqSorted = dict_value_sort_return_top(hashFreq, 20)
del hashFreq
usersFreqSorted = dict_value_sort_return_top(usersFreq, 20)
del usersFreq
lang_freq_sorted = dict_value_sort_return_top(lang_freq, 20)
del lang_freq
lang_nonzero = []
for l in range(len(lang_freq_sorted)):
    if lang_freq_sorted[l][1] > 0:
        lang_nonzero.append(lang_freq_sorted[l])

# Create a json file
# The top level data structure of a json file or object is a dictionary
# Variable to store data for json dump
mainJsonDump = {"ImageURL": imageUrl, "TopWords": topWords, "TweetCount": rowCount, "TotalWords": totalWords,
                "UniqueWords": uniqueWords, 'HashFreq': hashFreqSorted, 'UsersFreq': usersFreqSorted,
                'PopularLanguages': lang_nonzero}
# ImageURL contains the path to the wordcloud image produced in the previous block in string format
# TopWords contains the top words arranged in descending order in
# an array. Each array element is a tuple/array with two entries, word (index 0) and frequency (index 1)
# TweetCount contains the total no of tweets read from the database
# TotalWords contains the total no of filtered words used in the analysis
# UniqueWords contains the total no of unique words in the frequency dictionary
# HashFreq contains top n hashtags
# UsersFreq contains top n users

# Write a json file
jsonPath = '/home/bioinformaticsbot/bioinfobot.github.io/data/' + name + '.json'
with open(jsonPath, 'w') as wcd:
    json.dump(mainJsonDump, wcd)

# Load the above created json file and read the elements from dictionary and arrays
# This code is a template to reproduce it in JavaScript for the website
# It shows how the elements are stored in the json file
# with open(jsonPath, 'r') as rwcd:
#     obj = json.load(rwcd)
#     print(json.dumps(obj, indent='\t'))
# print('ImageURL:',obj['ImageURL'])
# print('TopWords:')
# for i in range(0,19):
# 	print(obj['TopWords'][i][0],'(',obj['TopWords'][i][1],')')
# print('TweetCount:',obj['TweetCount'])
# print('TotalWords:',obj['TotalWords'])
# print('UniqueWords:',obj['UniqueWords'])
