#Prints out the a line for each day with format: YYYY-mm-dd calculated_sentiment ev_report_result

import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from itertools import groupby

sentences = []
file_with_data = 'Data/test.csv'

with open(file_with_data, 'rb') as csvfile:
    fileReader = csv.DictReader(csvfile)
    for row in fileReader:
        datetime_object = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
        sentences.insert(0, (datetime_object,row['text']))


dates_and_sentiments = []

analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence[1])
    dates_and_sentiments.append( (sentence[0], vs['compound']) )




score_avg_sentence_per_day = [] #date is on format 'Y-m-d'

for key, group in groupby(dates_and_sentiments, lambda x: str(x[0].strftime('%Y-%m-%d'))):
    score_sentence_per_day = []
    for thing in group:
        score_sentence_per_day.append(thing[1]) #print "A %s is a %s." % (thing, key)
    avg = sum(score_sentence_per_day) / len(score_sentence_per_day)
    score_avg_sentence_per_day.append((key, avg))


results = [('2017-01-08', 90.5)] #Placeholder: will later be real result, list. Format: ('YYYY-mm-dd', result)

for score_day in score_avg_sentence_per_day:
    result_to_print = ''

    for res in results:
        if res[0] == score_day[0]:
            result_to_print = str(res[1])

    print str(score_day[0]) + ' ' +  str(score_day[1]) + ' ' + result_to_print
