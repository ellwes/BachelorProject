#!/bin/bash

#VARIABLES
#For scraping twitter
SEARCH_QUERY="Activision Blizzard"
START_DATE="2014-05-06"
END_DATE="2018-04-10" #format: YYYY-mm-dd
OFFSET_MONTH=48 #number of month before endDate

#For scraping reports
COMPANY_CODE='ATVI'    # company code for apple

#For the rest
ALGORITHM="VADER"
SCRAPE_TWITTER=false
FILE_NAME="$(echo -e "${SEARCH_QUERY}" | tr -s '[:space:]' '_')${END_DATE}_$OFFSET_MONTH_$ALGORITHM"


#SCRIPT
if $SCRAPE_TWITTER
then
	python getTweets.py $SEARCH_QUERY 'query_end' $END_DATE $OFFSET_MONTH $FILE_NAME
fi



python sentiment_analysis.py $FILE_NAME $COMPANY_CODE > Data/$FILE_NAME.dat

gnuplot << EOF
	plot_quarter_data=1

	set xdata time
	set timefmt "%Y-%m-%d"
	set xrange["$START_DATE": "$END_DATE"]
	set terminal png font arial 14 size 1500,800
	set output 'Plot/$FILE_NAME.png'
	if (plot_quarter_data == 1) {
		plot "Data/${FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments", "Data/${FILE_NAME}.dat" using 1:3 title "Total net revenues", "Data/${FILE_NAME}.dat" using 1:4 title "Net income"
	} else {
	    plot "Data/${FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments"
	}
EOF
