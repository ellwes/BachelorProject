#!/bin/bash

#VARIABLES
#For scraping twitter
SEARCH_QUERY="under armour" #"under armour"
START_DATE="2014-09-10" #"2014-05-06"
END_DATE="2018-04-01" #"2014-09-10" #format: YYYY-mm-dd
OFFSET_MONTH=12 #number of month before endDate

#For scraping reports
COMPANY_CODE='UA'    # company code for apple


#For the rest
ALGORITHM="VADER"
SCRAPE_TWITTER=false
CORRELATION=false
S_A=true
FILE_NAME="$(echo -e "${SEARCH_QUERY}" | tr -s '[:space:]' '_')${END_DATE}_$ALGORITHM"

#Zooming in graph
START_DATE_ZOOM="2014-09-10" #"2014-05-06"
END_DATE_ZOOM="2018-04-01" #"2014-09-10" #format: YYYY-mm-dd

#SCRIPT
if $SCRAPE_TWITTER
then
	python getTweets.py $SEARCH_QUERY 'query_end' $END_DATE $OFFSET_MONTH $FILE_NAME
fi



if $S_A
then
	python sentiment_analysis.py $FILE_NAME $COMPANY_CODE $CORRELATION > Data/$FILE_NAME.dat
fi

gnuplot << EOF
	plot_quarter_data=1

	set xdata time
	set timefmt "%Y-%m-%d"
	set xrange["$START_DATE_ZOOM": "$END_DATE_ZOOM"]
	set xlabel "Day"
	set yrange[-1:1]
	set ylabel "Sentiment score (decimal)"
	set y2range[-2:2]
	set y2label "Procentual changes (decimal)"
	set ytics nomirror
	set y2tics
	set terminal png font arial 14 size 1500,800
	set output 'Plot/$FILE_NAME.png'
	if (plot_quarter_data == 1) {
		plot "Data/${FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments" axes x1y1, "Data/${FILE_NAME}.dat" using 1:3 title "Total net revenues" lt rgb "#0E4D2A" axes x1y2, "Data/${FILE_NAME}.dat" using 1:4 title "Net income" axes x1y2, "Data/${FILE_NAME}.dat" using 1:5 title "Diluted" axes x1y2
	} else {
	    plot "Data/${FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments"
	}
EOF
