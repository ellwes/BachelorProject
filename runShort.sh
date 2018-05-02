#!/bin/bash

#This script is used to preform a sentiment analysis over a shorter time. Each sentiment for day can be shown. (not only average)
#OBS: Only works correctly if the result from one date is used.

#VARIABLES:
START_DATE="2015-07-22" #"2014-05-06"
END_DATE="2015-07-26" #"2014-09-10" #format: YYYY-mm-dd

FILE_NAME="SIMPLE_nvidia_2015-07-22_2015-07-26" #The file in which the tweets can be found.
RESULT_FILE="NVDA-Q-10" #The file in which result can be found. Format: COMPANY_CODE-Q-10

DAT_FILE_NAME="SIMPLE_nvidia_2015-07-22_2015-07-26" #The name of the dat-file (that will be used to create the graph)

python sentiment_analysis_short.py $START_DATE $END_DATE $FILE_NAME $RESULT_FILE > Data/${DAT_FILE_NAME}.dat


gnuplot << EOF
	set xdata time
	set timefmt "%Y-%m-%d_%H:%M:%S"
	set xrange["${START_DATE}_00:00:00": "${END_DATE}_00:00:00"]
  set xlabel "Time"
  set yrange[-1:1]
  set ylabel "Sentiment score (decimal)"
  set y2range[-2:2]
  set y2label "Procentual changes (decimal)"
  set ytics nomirror
  set y2tics
	set terminal png font arial 14 size 1500,800
	set output 'Plot/$DAT_FILE_NAME.png'
	plot "Data/${DAT_FILE_NAME}.dat" using 1:2 with linespoints title "Sentiments" axes x1y1
EOF
