import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime


sentences = []
fileWithData = 'Data/test.csv'

with open(fileWithData, 'rb') as csvfile:
    fileReader = csv.DictReader(csvfile)
    for row in fileReader:
        datetime_object = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
        sentences.append(row['text'])

score_sentence = []
analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    score_sentence.append(vs['compound'])
    print(vs['compound'])

