#!/usr/bin/env python3

'''
DESCRIPTION     : Custom function library.
USAGE           : from twitterfunc import tweet_clean
OUTPUT          : function return
AUTHOR          : Dr. Rohit Farmer
EMAIL           : rohit.farmer@gmail.com
'''

import re
import string

def tweet_clean(text):
    """Function to remove unwanted text/words from tweets. This is independent of nltk stopwords method."""
    # Remove hyperlinks
    text = re.sub('https://\S+', '', text)
    text = re.sub('http://\S+', '', text)
    # Remove &
    text = re.sub('&amp', '', text)
    # Remove hashtags
    text = re.sub('#\w+', '', text)
    text = re.sub('#', ' ', text)
    # Remove citations
    text = re.sub('@\w+', '', text)
    # Remove tickers
    text = re.sub('\$\w+', '', text)
    # Remove punctuation
    text = re.sub('[' + string.punctuation + ']+', '', text)
    # # Remove quotes
    text = re.sub('&*[amp]*;|gt+', '', text)
    # Remove RT and CT
    text = re.sub('rt\s+', '', text)
    text = re.sub('ct\s+', '', text)
    # Remove linebreak, tab, return
    text = re.sub('[\n\t\r]+', '', text)
    # Remove via with blank
    text = re.sub('via+\s', '', text)
    # Remove multiple whitespace
    text = re.sub('\s+\s+', ' ', text)
    # Remove anything that is not a unicode character
    text = re.sub('\W', ' ', text)
    # Remove digits
    text = re.sub('\d+', '', text)
    return text