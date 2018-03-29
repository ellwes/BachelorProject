#!/bin/bash
startDate = "2017-01-07" #format: 2017-01-

python sentiment_analysis.py > test.dat 

gnuplot << EOF
	set xdata time
	set timefmt "%Y-%m-%d"
	set xrange["2017-01-07": "2017-01-10"]
	set terminal png font arial 14 size 800,600
	set output 'plot.png'
	plot "test.dat" using 1:2 with linespoints title "Sentiments", "test.dat" using 1:3 title "Quater Result"

EOF