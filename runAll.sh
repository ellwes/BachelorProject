#!/bin/bash
#startDate = "2017-01-07" #format: 2017-01-

python sentiment_analysis.py > test.dat 

gnuplot << EOF
	plot_quarter_data=0

	set xdata time
	set timefmt "%Y-%m-%d"
	set xrange["2013-01-28": "2018-02-28"]
	set terminal png font arial 14 size 1500,800
	set output 'plot.png'
	if (plot_quarter_data == 1) {
		plot "test.dat" using 1:2 with linespoints title "Sentiments", "test.dat" using 1:3 title "Quater Result"
	} else {
	    plot "test.dat" using 1:2 with linespoints title "Sentiments"
	}
EOF
