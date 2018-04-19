#Prints out the a line for each day with format: YYYY-mm-dd calculated_sentiment ev_report_result
import sys
import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from itertools import groupby

sentences = []
file_with_data = 'Data/' + sys.argv[1] + '.csv'
file_with_result = 'Results/' + sys.argv[2] + '-Q-10.txt'
day_precision = 5 #1 means its x-interval will be 1 day between 2 points, n means its x-interval will be n days between 2 points

results = [] #Holds the results from the quater reports
descriptor1 = 'Total revenues'
descriptor2 = 'Net income'
descriptor3 = 'Diluted'


#functions
def extractNumbers(s):
    s = re.findall("\(?\d*\.?\d+\)?" , s)[0]
    if s[0] == '(':
        s = '-' + s[1:]
    return s


#reads the result from a file
date = ''
result1 = '?'
result2 = '?'
result3 = '?'

result_file = open(file_with_result, 'r')
for line in result_file:
    if line.rstrip().isdigit():
        #Add result to resutls-list
        if result1 != '?' or result2 != '?' or result3 != '?':
            results.append((date, result1, result2, result3));
            date = ''
            result1 = '?'
            result2 = '?'
            result3 = '?'
        #Update date
        date = line[0:4] + '-' + line[4:6] + '-' + line[6:8]
    elif line[0] == "'":
        descriptor = re.findall("('.+')", line)[0][1:-1]
        thisQuater = extractNumbers(re.findall("('\s*\(?\d*\.?\d+\)?\s)" , line)[0])
        lastQuater = extractNumbers(re.findall("(\(?\d*\.?\d+\)?\s*\n)" , line)[0])
        if descriptor == descriptor1:
            result1 = (float(thisQuater) - float(lastQuater))/float(lastQuater)
        elif descriptor == descriptor2:
            result2 = (float(thisQuater) - float(lastQuater))/float(lastQuater)
        elif descriptor == descriptor3:
            result3 = (float(thisQuater) - float(lastQuater))/float(lastQuater)

if result1 != '?' or result2 != '?' or result3 != '?':
    results.append((date, result1, result2, result3))



#Reads the date and the comments from file
with open(file_with_data, 'rb') as csvfile:
    fileReader = csv.DictReader(csvfile)
    for row in fileReader:
        datetime_object = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
        sentences.insert(0, (datetime_object,row['text']))


#Preformes the analysis
dates_and_sentiments = []
analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence[1])
    dates_and_sentiments.append( (sentence[0], vs['compound']))



#Calculates the average per day
score_avg_sentence_per_day = [] #date is on format 'Y-m-d'
for key, group in groupby(dates_and_sentiments, lambda x: str(x[0].strftime('%Y-%m-%d'))):
    score_sentence_per_day = []
    for thing in group:
        score_sentence_per_day.append(thing[1]) #print "A %s is a %s." % (thing, key)
    avg = sum(score_sentence_per_day) / len(score_sentence_per_day)
    score_avg_sentence_per_day.append((key, avg))



#Puts all data in a csv-file in order to find the correlation c oefficient.
newFilePath = 'Correlation/' + sys.argv[1] + '_correlation.csv'
with open(newFilePath, 'w') as csvfile:
    fieldnames = ['date', 'sentiment_value', descriptor1, descriptor2, descriptor3]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for score_day in score_avg_sentence_per_day:
        res1 = ''
        res2 = ''
        res3 = ''
        for res in results:
            if res[0] == score_day[0]:
                res1 = res[1]
                res2 = res[2]
                res3 = res[3]
        writer.writerow({'date': score_day[0],  'sentiment_value': score_day[1], descriptor1: res1, descriptor2: res2, descriptor3: res3})



#Calculates the average per chosen number of days and prints the avg on first day, ? on the rest of the days
i = 0
curSum = 0
for score_day in score_avg_sentence_per_day:
    result_to_print1 = '?'
    result_to_print2 = '?'
    result_to_print3 = '?'
    for res in results:
        if res[0] == score_day[0]:
            result_to_print1 = str(res[1])
            result_to_print2 = str(res[2])
            result_to_print3 = str(res[3])
    curSum = curSum + score_day[1]
    if i % day_precision == day_precision-1:
    	print str(score_day[0]) + ' ' +  str(curSum / day_precision) + ' ' + result_to_print1 + ' ' + result_to_print2+ ' ' + result_to_print3
    	curSum = 0
    else:
	print str(score_day[0]) + ' ' +  '?' + ' ' + result_to_print1 + ' ' + result_to_print2+ ' ' + result_to_print3
    i = i + 1
