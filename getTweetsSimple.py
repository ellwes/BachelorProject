#Simple script to retrive Tweets. Can only search on one query.

import sys
sys.path.append('GetOldTweets-python/')

import got
import json
import csv
import os

from datetime import datetime, timedelta
import dateutil.relativedelta


query = "nvidia"

startDate = "2015-07-22" #str. "yyyy-mm-dd"
endDate = "2015-07-26" #str. "yyyy-mm-dd"

newFilePath = 'Data/SIMPLE_' + query.replace(' ', '_') + '_' + startDate + '_' + endDate  + '.csv'


tweets = []
tweetCriteria = got.manager.TweetCriteria().setSince(startDate).setUntil(endDate).setQuerySearch(query)
tweetsWithCriteria = got.manager.TweetManager.getTweets(tweetCriteria)
for tweet in tweetsWithCriteria:
    tweets.append(tweet)



with open(newFilePath, 'w') as csvfile:
	fieldnames = ['username', 'date', 'text']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	for tweet in tweets:
		writer.writerow({'username': tweet.username.encode("utf-8"),  'date': tweet.date, 'text': tweet.text.encode("utf-8")})
