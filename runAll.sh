#!/bin/bash

#VARIABLES
SEARCH_QUERY="nvidia stock"
START_DATE="2017-12-07"
END_DATE="2018-01-07" #format: YYYY-mm-dd
OFFSET_MONTH=1 #number of month before endDate

ALGORITHM="VADER"
SCRAPE_TWITTER=true


#SCRIPT

FILE_NAME="$(echo -e "${SEARCH_QUERY}" | tr -s '[:space:]' '_')${END_DATE}_$OFFSET_MONTH_$ALGORITHM"


if $SCRAPE_TWITTER
then
	python getTweets.py $SEARCH_QUERY 'query_end' $END_DATE $OFFSET_MONTH $FILE_NAME
fi

python sentiment_analysis.py $FILE_NAME > Data/$FILE_NAME.dat


gnuplot << EOF
	plot_quarter_data=0

	set xdata time
	set timefmt "%Y-%m-%d"
	set xrange["$START_DATE": "$END_DATE"]
	set terminal png font arial 14 size 1500,800
	set output 'Plot/$FILE_NAME.png'
	if (plot_quarter_data == 1) {
		plot "Data/${FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments", "$FILE_NAME.dat" using 1:3 title "Quater Result"
	} else {
	    plot "Data/${FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments"
	}
EOF
