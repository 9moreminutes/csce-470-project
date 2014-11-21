Trackflix
=========

Group project for CSCE 470 - Information Storage and Retrieval

Python Dependencies
-------------------
- nltk
- simplejson
- stemming
- mrjob


Running test data
-----------------

To run a small test of the steps we take to process the data,

- Check  out the repo
- go to the processing/ folder
- make sure you have the python libraries installed
- run `python countwords.py sampledata.json > test.out` to calculate the tfidf vectors for each title in the sample data
- run `python find_similarity.py` to generate a json similarity matrix
