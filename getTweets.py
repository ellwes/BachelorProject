    
import sys
sys.path.append('GetOldTweets-python/')

import got
import json
import csv

usernames = []
querySearch = ['nvidia stock']
newFilePath = 'Data/test.csv'


startDate = '2017-01-09' #str. "yyyy-mm-dd"
endDate = '2017-01-010' #str. "yyyy-mm-dd"

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

with open(newFilePath, 'w') as csvfile:
    fieldnames = ['username', 'date', 'text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for tweet in tweets:
        writer.writerow({'username': tweet.username.encode("utf-8"),  'date': tweet.date, 'text': tweet.text.encode("utf-8")})
