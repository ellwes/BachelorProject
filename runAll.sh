#!/bin/bash

#VARIABLES
SEARCH_QUERY="something to search for"
START_DATE="2017-10-07"
END_DATE="2018-01-07" #format: YYYY-mm-dd
OFFSET_MONTH=1 #number of month before endDate

ALGORITHM="VADAR"
SCRAPE_TWITTER=1


#SCRIPT

FILE_NAME="$(echo -e "${SEARCH_QUERY}" | tr -s '[:space:]' '_')${START_DATE}_$OFFSET_MONTH"


if [ $SCRAPE_TWITTER ]
then
	python getTweets.py $SEARCH_QUERY 'query_end' $END_DATE $OFFSET_MONTH $FILE_NAME
fi

python sentiment_analysis.py $SEARCH_QUERY 'query_end' $END_DATE $START_DATE > test.dat



#gnuplot << EOF
#	plot_quarter_data=0

#	set xdata time
#	set timefmt "%Y-%m-%d"
#	set xrange["2013-01-28": "2018-02-28"]
#	set terminal png font arial 14 size 1500,800
#	set output 'plot.png'
#	if (plot_quarter_data == 1) {
	#	plot "test.dat" using 1:2 with linespoints title "Sentiments", "test.dat" using 1:3 title "Quater Result"
	#} else {
	#    plot "test.dat" using 1:2 with linespoints title "Sentiments"
	#}
#EOF
