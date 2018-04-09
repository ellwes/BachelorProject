import os
import sys
sys.path.append('sec-edgar/')
import re
import time
from itertools import groupby
from SECEdgar.crawler import SecCrawler

qFilePath = 'sec-edgar/SEC-Edgar-Data/'

companyCode = 'AAPL'    # company code for apple 
cik = '0000320193'      # cik code for apple
date = '20010101'       # date from which filings should be downloaded
count = '10'            # no of filings

def scrapeFilings():
	#TODO wipe old files in directory!
	t1 = time.time()
	
	# create object
	seccrawler = SecCrawler()
	
	seccrawler.filing_10Q(str(companyCode), str(cik), str(date), str(count))

	t2 = time.time()
	print ("Total Time taken: "),
	print (t2-t1)

def getIncomeStatementData():
	finalPath = qFilePath + companyCode + '/' + cik + '/' + '10-Q'

	filedAt = ''
	incomeStatementEntries = []	

	for filename in os.listdir(finalPath):
		foundIncomeStatement = False
		foundIncomeStatementTable = False
		foundIncomeStatementEndOfTable = False

		with open(finalPath + '/' + filename, 'r') as qReport:
			qReportContent = qReport.readlines()
			for line in qReportContent:
				if r'FILED AS OF DATE:' in line:
					filedAt = line.partition(r'FILED AS OF DATE:')[2] .strip()
				if r'CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS (Unaudited)' in line:
					foundIncomeStatement = True
					continue
				if foundIncomeStatement and r'<S>' in line:
					foundIncomeStatementTable = True
					continue
				if foundIncomeStatement and foundIncomeStatementTable and r'</TABLE>' in line:
					break
				if foundIncomeStatement and foundIncomeStatementTable:
					match = re.search(r'(?P<type>([\S(),]+([(\s)(\s\n)(\n\s)(\s\s)][\S(),]+)*))(\s){4}\s+(?P<thisYearsQ>(\$\s*(\S+))|(\S+))\s+(?P<prevYearsQ>(\$\s*(\S+))|(\S+)).*'.decode('utf-8'), line.decode('utf-8'))
					if match:
						_type = match.group('type')
						_curData = match.group('thisYearsQ')
						_prevData = match.group('prevYearsQ')
						incomeStatementEntries.append([filedAt, _type, _curData, _prevData])
	return incomeStatementEntries

def clearDataField(text, isDecimal):
	if not isDecimal:
		text = text.replace(".", "")
	if isDecimal:
		text = text.replace(" ", "")

	text = text.replace("-", "")
	text = text.replace("=", "")
	return text
#scrapeFilings()
incomeStatementData = getIncomeStatementData()
#SaveToFIle
with open('Results/' + companyCode + '-Q10.txt', 'w') as the_file:
	for key, group in groupby(incomeStatementData, lambda x: str(x[0])):
		the_file.write(key + '\n')
		for thing in group:
			if  0 < len(clearDataField(thing[1], False)):
				the_file.write("'" + clearDataField(thing[1], False) + "' " + clearDataField(thing[2], True) + ' ' + clearDataField(thing[3], True) + '\n')









