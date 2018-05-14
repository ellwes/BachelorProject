#Prints out the a line for each day with format: YYYY-mm-dd calculated_sentiment ev_report_result
import sys
import os
import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import dateutil.relativedelta

companyReports = "Reports/"
tweetsPath = "Data/"




def PNRatio(filePath, startInterval, endInterval):
	sentencePos = []
	sentenceNeg = []

	startInterval = startInterval.replace(hour=0, minute=0, second=0)
	endInterval = endInterval.replace(hour=23, minute=59, second=59)

	analyzer = SentimentIntensityAnalyzer()

	with open(filePath, 'rb') as csvfile:
		fileReader = csv.DictReader(csvfile)

		for row in fileReader:
			curr_date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
			if (startInterval <= curr_date <= endInterval):
				vs = analyzer.polarity_scores(row['text'])
				sentimentScore = vs['compound']
				if sentimentScore < 0:
					sentenceNeg.append(sentimentScore)
				elif 0 < sentimentScore:
					sentencePos.append(sentimentScore)
		#calculate PNRatio
		print str(sum(sentencePos)) + ' ' + str(sum(sentenceNeg))
		return abs(sum(sentencePos) / sum(sentenceNeg))

def ProcessCompanyReport(filePath, newFilePath):
	with open(filePath, 'r') as csvinput:
		with open(newFilePath, 'w') as csvoutput:
			fileReader = csv.DictReader(csvinput)

			writer = csv.writer(csvoutput, lineterminator='\n')
			reader = csv.reader(csvinput)

			all = []
			row = next(reader)
			row.append('PNRatio')
			all.append(row)

			for row in reader:
				print row[0];
				datePressRelease = row[1]
				#Offsetdates
				startInterval = datetime.strptime(datePressRelease, '%Y-%m-%d') - dateutil.relativedelta.relativedelta(days=0)
				endInterval = datetime.strptime(datePressRelease, '%Y-%m-%d') + dateutil.relativedelta.relativedelta(days=2)
				pnratio = PNRatio(tweetsPath + '/' + row[8], startInterval, endInterval)
				row.append(pnratio)
				all.append(row)

			writer.writerows(all)

#Process all files, append PNRatio based on their connected
for filename in os.listdir(companyReports):
	ProcessCompanyReport(companyReports + '/' + filename, filename + '_processed.csv')
