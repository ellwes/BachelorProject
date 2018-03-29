    
import sys
sys.path.append('GetOldTweets-python/')

import got
import json
import csv

from datetime import datetime, timedelta
import dateutil.relativedelta

usernames = []
querySearch = ['nvidia stock']
newFilePath = 'Data/test.csv'


offsetMonth = 12*4 #0 is 1 month. 2 is 3 months etc...
endDate = '2017-01-10' #str. "yyyy-mm-dd"

#
# Functions
#

def scrapeMonth(eD, offsetMonth):
	startDate = (datetime.strptime(eD, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(months=offsetMonth+1)).strftime('%Y-%m-%d')
	endDate = (datetime.strptime(eD, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(months=offsetMonth)).strftime('%Y-%m-%d')
	tweets = []
	if usernames:
	    for username in usernames:
		for query in querySearch:
		    tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(startDate).setUntil(endDate).setQuerySearch(query)
		    tweetsWithCriteria = got.manager.TweetManager.getTweets(tweetCriteria)
		    for tweet in tweetsWithCriteria:
		        tweets.append(tweet)
	else:
		for query in querySearch:
		tweetCriteria = got.manager.TweetCriteria().setSince(startDate).setUntil(endDate).setQuerySearch(query)
		tweetsWithCriteria = got.manager.TweetManager.getTweets(tweetCriteria)
		for tweet in tweetsWithCriteria:
		    tweets.append(tweet)
	return tweets

def get_lastday(current):
	_first_day = current.replace(day=1)
	prev_month_lastday = _first_day - datetime.timedelta(days=1)
	return prev_month_lastday.replace(day=1)



#
# The script
#
with open(newFilePath, 'w') as csvfile:
	fieldnames = ['username', 'date', 'text']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()

	for x in range(offsetMonth):
		print('Scraping month: ' + str(x+1) + ' of ' + str(offsetMonth))
		tweets = scrapeMonth(endDate, x)
		for tweet in tweets:
			writer.writerow({'username': tweet.username.encode("utf-8"),  'date': tweet.date, 'text': tweet.text.encode("utf-8")})
