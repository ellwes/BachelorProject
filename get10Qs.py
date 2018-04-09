import sys
sys.path.append('GetOldTweets-python/')

import time
from SECEdgar.crawler import SecCrawler

def get_filings():
	t1 = time.time()
	
	# create object
	seccrawler = SecCrawler()

	companyCode = 'AAPL'    # company code for apple 
	cik = '0000320193'      # cik code for apple
	date = '20010101'       # date from which filings should be downloaded
	count = '10'            # no of filings
	
	seccrawler.filing_10Q(str(companyCode), str(cik), str(date), str(count))

	t2 = time.time()
	print ("Total Time taken: "),
	print (t2-t1)


get_filings()
