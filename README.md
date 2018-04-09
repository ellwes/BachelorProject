# BachelorProject

## Setup
### Required dependencies
#### GetOldTweets
Get GetOldTweets from https://github.com/Jefferson-Henrique/GetOldTweets-python.  
Move to the directory GetOldTweets-python and run:  

Make sure following dependencies are installed by executing:
```
sudo apt-get update
sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo apt-get install libxml2-dev libxslt-dev python-dev lib32z1-dev
```

Now install requirements

```
pip install -r requirements.txt
```

#### VADER
Install VADER (Valence Aware Dictionary and sEntiment Reasoner):  

```
pip install vaderSentiment
```
#### SEC-Edgar-Crawler
Get GetOldTweets from https://github.com/rahulrrixe/sec-edgar.

```
git clone https://github.com/rahulrrixe/sec-edgar.git  
```

Stand in this repos root and move to the directory root of sec-edgar.
```
cd sec-edgar
```

Install requirements
```
pip install -r requirements.txt
```

Make sure requests version is atleast 2.6.0:
```
pip install requests==2.6.0
```
#### GnuPlot
```
sudo apt-get install gnuplot-qt rlwrap 
```

#### Setting up this repos dependencies
To setup internal imports: (TODO

```
pip install python-dateutil
```

