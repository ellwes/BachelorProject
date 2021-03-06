
import sys
sys.path.append('GetOldTweets-python/')

import got
import json
import csv
import os

from datetime import datetime, timedelta
import dateutil.relativedelta

i = 1
query = sys.argv[i]
i+=i
while sys.argv[i] != 'query_end':
	query = query + ' ' + sys.argv[i]
	i+=1


usernames = []
querySearch = [query]


endDate = sys.argv[i+1] #str. "yyyy-mm-dd"
offsetMonth = int(sys.argv[i+2]) #1 is 2 months. 2 is 3 months etc...

#newFilePath = 'Data/' + sys.argv[i+3] + '.csv'




#
# Functions
#

def scrapeMonth(eD, offsetMonth):

	startDate = (datetime.strptime(eD, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(months=offsetMonth+1)).strftime('%Y-%m-%d')
	endDate = (datetime.strptime(eD, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(months=offsetMonth)).strftime('%Y-%m-%d')

	#Fix precision
	#startDate = datetime.combine(startDate, datetime.time.min)
	#endDate = datetime.combine(endDate, datetime.time.max)

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

def scrapeWithRetry(eD, offsetMonth):
	scrapeSuccessful = False
	while not scrapeSuccessful:
		try:
			return scrapeMonth(eD, offsetMonth)
			scrapeSuccessful = True
			break
		except:
			print("Failed retrying again")

def get_lastday(current):
	_first_day = current.replace(day=1)
	prev_month_lastday = _first_day - datetime.timedelta(days=1)
	return prev_month_lastday.replace(day=1)



#
# The script
#
for x in range(offsetMonth):
	newFilePath = 'Data/' + sys.argv[i+3] + '-' + str(x) + '.csv'
	try:
	    os.remove(newFilePath)
	except OSError:
	    pass
	with open(newFilePath, 'w') as csvfile:
		fieldnames = ['username', 'date', 'text']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()


		print('Scraping month: ' + str(x+1) + ' of ' + str(offsetMonth))
		tweets = scrapeWithRetry(endDate, x)
		for tweet in tweets:
			writer.writerow({'username': tweet.username.encode("utf-8"),  'date': tweet.date, 'text': tweet.text.encode("utf-8")})
