#Prints out the a line for each day with format: YYYY-mm-dd calculated_sentiment ev_report_result
import sys
import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

start_date = sys.argv[1]
end_date = sys.argv[2]

file_with_data = "Data/" + sys.argv[3] + ".csv"
newFilePath = "Sentiments/" + sys.argv[3] + ".csv"

#Reads the date and the comments from file
sentences = []
with open(file_with_data, 'rb') as csvfile:
    fileReader = csv.DictReader(csvfile)
    read_data = False
    for row in fileReader:
        curr_date = str(datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
        if curr_date == end_date:
            read_data = True
        elif curr_date == start_date:
            read_data = False
        if read_data:
            sentences.insert(0, (row['date'], row['text']))


#Preformes the analysis
time_and_sentiments = []
analyzer = SentimentIntensityAnalyzer()
with open(newFilePath, 'w') as csvfile:
    fieldnames = ['date', 'sentiment_value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence[1])
        time_and_sentiments.append( (sentence[0], vs['compound']))
        writer.writerow({'date': sentence[0].replace(' ', '_'),  'sentiment_value': vs['compound']})
        print sentence[0].replace(' ', '_') + ' ' + str(vs['compound'])
