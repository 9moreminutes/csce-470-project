Trackflix
=========

Group project for CSCE 470 - Information Storage and Retrieval
Finds movies with queried artist/composer, then recommends movies similar to each one returned.

Python Dependencies
-------------------
- Processing
  - nltk
  - simplejson
  - stemming
  - mrjob

- Web Dependencies
  - flask
  - requests


Running test data
-----------------

To run a small test of the steps we take to process the data,

- Check  out the repo
- go to the processing/ folder
- make sure you have the python libraries installed
- run `python countwords.py sampledata.json > test.out` to calculate the tfidf vectors for each title in the sample data
- run `python find_similarity.py` to generate a json similarity matrix

Firefox Config
--------------

Images will only work when the referer header is blank because IMDB disallows hotlinking. This is a changeable setting in Firefox:
network.http.sendRefererHeader = 0
