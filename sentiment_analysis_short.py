#Prints out the a line for each day with format: YYYY-mm-dd calculated_sentiment ev_report_result
import sys
import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

start_date = sys.argv[1]
end_date = sys.argv[2]

file_with_data = "Data/" + sys.argv[3] + ".csv"
file_with_result = "Results/" + sys.argv[4] + ".txt"


#reads the result from a file
date = ''
result1 = '?'
result2 = '?'
result3 = '?'

results = [] #Holds the results from the quater reports
descriptor1 = 'Total net sales'
descriptor2 = 'Net income (loss)'
descriptor3 = 'Diluted'

def extractNumbers(s):
    s = re.findall("\(?\d*\.?\d+\)?" , s)[0]
    if s[0] == '(':
        s = '-' + s[1:]
    return s

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
        date = line[0:4] + '-' + line[4:6] + '-' + line[6:8] + '_08:00'

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
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence[1])
    time_and_sentiments.append( (sentence[0], vs['compound']))
    printed = False
    for res in results: #looks for resluts to print that day
        if sentence[0][0:10] == res[0]:
            print sentence[0].replace(' ', '_') + ' ' + str(vs['compound']) + res[1] + ' ' + res[2] + ' ' + res[3]
            printed = True
            break;
    if not printed:
        print sentence[0].replace(' ', '_') + ' ' + str(vs['compound']) + ' ? ? ?' 
    printed = False
