import os
import sys
sys.path.append('sec-edgar/')
import re
import time
from itertools import groupby
from SECEdgar.crawler import SecCrawler
from lxml import etree
import pandas as pd
from html_tables import html_tables
import shutil
from bs4 import BeautifulSoup

sys.setrecursionlimit(3000)

qFilePath = 'sec-edgar/SEC-Edgar-Data/'
companyCode = 'NVDA'    		# company code for apple 
cik = '1045810'      		# cik code for nvidia
date = '20180101'       		# date from which filings should be downloaded
count = 4 * (2018-2014)          # no of filings, 201508
tableIndex = 6 #There is no implemented logic to automatically identify the right table

def scrapeFilings():
	#TODO wipe old files in directory!
	shutil.rmtree(qFilePath + '/' + companyCode + '/' + cik + '/10-Q')

	t1 = time.time()
	
	# create object
	seccrawler = SecCrawler()
	
	seccrawler.filing_10Q(str(companyCode), str(cik), str(date), str(count))

	t2 = time.time()
	print ("Total Time taken: "),
	print (t2-t1)

def testDisplayTable():
	for filename in os.listdir(finalPath):
		with open(finalPath + '/' + filename, 'r') as qReport:
			qReportContent = qReport.readlines()
			for line in qReportContent:
				if r'FILED AS OF DATE:' in line:
					filedAt = line.partition(r'FILED AS OF DATE:')[2] .strip()
					break
		print(filename + ' ' + filedAt)
		with open(finalPath + '/' + filename, 'r') as qReport:
			qReportContent = qReport.read()
			tables = pd.read_html(qReportContent) # Returns list of all tables on page
			print(tables[tableIndex])
			return

def getIncomeStatementData():
	finalPath = qFilePath + companyCode + '/' + cik + '/' + '10-Q'

	filedAt = ''
	incomeStatementEntries = []	

	for filename in os.listdir(finalPath):
		with open(finalPath + '/' + filename, 'r') as qReport:
			qReportContent = qReport.readlines()
			for line in qReportContent:
				if r'FILED AS OF DATE:' in line:
					filedAt = line.partition(r'FILED AS OF DATE:')[2] .strip()
					break
		print(filename + ' ' + filedAt)
		with open(finalPath + '/' + filename, 'r') as qReport:
			qReportContent = qReport.read()
			soup = BeautifulSoup(qReportContent, 'html5lib')
			table = soup.find_all('table')[tableIndex] 
			scrapedTable = pd.read_html(str(table)) # Returns list of all tables on page
			incomeStatementEntries = incomeStatementEntries + parseTable(scrapedTable[0], filedAt) # Select table of interest
	return incomeStatementEntries

def parseTable(table, filedAt):
	incomeStatementData = []
	for i in xrange(0, table.shape[0]):
		row = table.ix[i]
		rowStr = ''
		if is_number(row[0]):
			rowStr = u''.join((str(row[0]), '')).encode('utf-8').strip()
		else:
			rowStr = u''.join((row[0], '')).encode('utf-8').strip()
		if not "nan" in rowStr and 1 < len(rowStr.decode('utf-8')):
			colIndex = 0
			numericParseCount = 0
			statementEntry = [filedAt]
			print(rowStr)
			print(row[0])
			for col in row:
				colStr = ''
				if is_number(col):
					colStr = u' '.join((str(col), '')).encode('utf-8').strip()
				else:
					colStr = u' '.join((col, '')).encode('utf-8').strip()
				if colIndex == 0:
					statementEntry.append(colStr)
					colIndex = colIndex + 1
					continue
				match = re.search(r'\d'.decode('utf-8'), colStr.decode('utf-8'))
				#print("Looping")
				if match:
					statementEntry.append(colStr)
					numericParseCount = numericParseCount + 1
					if 2 <= numericParseCount:
						incomeStatementData.append(statementEntry)
						break
				colIndex = colIndex + 1
	print(incomeStatementData)
	return incomeStatementData

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def clearDataField(text, isDecimal):
	if not isDecimal:
		text = text.replace(".", "")
	if isDecimal:
		text = text.replace(" ", "")

	text = text.replace("-", "")
	text = text.replace("=", "")
	return text

scrapeFilings()
incomeStatementData = getIncomeStatementData()
#SaveToFIle
with open('Results/' + companyCode + '-Q10.txt', 'w') as the_file:
	for key, group in groupby(incomeStatementData, lambda x: str(x[0])):
		the_file.write(key + '\n')
		for thing in group:
			if  0 < len(clearDataField(thing[1], False)):
				the_file.write("'" + clearDataField(thing[1], False) + "' " + clearDataField(thing[2], True) + ' ' + clearDataField(thing[3], True) + '\n')








