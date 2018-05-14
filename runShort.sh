#!/bin/bash

#This script is used to preform a sentiment analysis over a shorter time. Each sentiment for day can be shown. (not only average)
#OBS: Only works correctly if the result from one date is used.

#VARIABLES:
START_DATE="2016-05-07" #"2014-05-06"
START_DATE_GRAPH="2016-05-08" #"2014-05-06"

END_DATE="2016-05-12" #"2014-09-10" #format: YYYY-mm-dd

FILE_NAME="Activision_Blizzard_2018-04-10_VADER" #The file in which the tweets can be found.

DAT_FILE_NAME="acti_2016_Q1" #The name of the dat-file (that will be used to create the graph)

python sentiment_analysis_short.py $START_DATE $END_DATE $FILE_NAME > Data/${DAT_FILE_NAME}.dat


gnuplot << EOF
	set xdata time
	set timefmt "%Y-%m-%d_%H:%M:%S"
	set xrange["${START_DATE_GRAPH}_00:00:00": "${END_DATE}_00:00:00"]
  set xlabel "Time"
  set yrange[-1:1]
  set ylabel "Sentiment score (decimal)"
	set terminal png font arial 14 size 1500,800
	set output 'Plot/$DAT_FILE_NAME.png'
	plot "Data/${DAT_FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments" axes x1y1
EOF
