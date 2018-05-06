#Simple script to retrive Tweets. Can only search on one query.

import sys
sys.path.append('GetOldTweets-python/')

import got
import json
import csv
import os

from datetime import datetime, timedelta
import dateutil.relativedelta


query = "wells fargo"

startDateArg = "2018-01-08" #str. "yyyy-mm-dd"
endDateArg = "2018-01-20" #str. "yyyy-mm-dd"

newFilePath = 'Data/SIMPLE_' + query.replace(' ', '_') + '_' + startDateArg + '_' + endDateArg  + '.csv'

startDate = datetime.strptime(startDateArg, '%Y-%m-%d').strftime('%Y-%m-%d')
endDate = datetime.strptime(endDateArg, '%Y-%m-%d').strftime('%Y-%m-%d')
tweets = []

#Prep first day
startScrapeDay = (datetime.strptime(endDate, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
endScrapeDay = endDate
#Loop
while (datetime.strptime(startDate, '%Y-%m-%d')).strftime('%Y-%m-%d') != startScrapeDay:
	print("Scraping" + endScrapeDay + "   Target:" + startDate)

	tweetCriteria = got.manager.TweetCriteria().setSince(startScrapeDay).setUntil(endScrapeDay).setQuerySearch(query)
	tweetsWithCriteria = got.manager.TweetManager.getTweets(tweetCriteria)
	for tweet in tweetsWithCriteria:
	    tweets.append(tweet)

	#Change day
	startScrapeDay = (datetime.strptime(startScrapeDay, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
	endScrapeDay = (datetime.strptime(endScrapeDay, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')

with open(newFilePath, 'w') as csvfile:
	fieldnames = ['username', 'date', 'text']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	for tweet in tweets:
		writer.writerow({'username': tweet.username.encode("utf-8"),  'date': tweet.date, 'text': tweet.text.encode("utf-8")})


