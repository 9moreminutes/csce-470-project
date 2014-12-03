from __future__ import division
import simplejson as json
from mrjob.job import MRJob
import re
import math
#import nltk
from stemming.porter2 import stem

class TfidfCalculator(MRJob):
    
    def __init__(self, *args, **kwargs):
        super(TfidfCalculator, self).__init__(*args, **kwargs)
        #self.stop = nltk.corpus.stopwords.words('english')

    def counter(self, _, line):
        # load the data from json
        data = json.loads(line)

        # don't have a plot for this title so skipping
        if not data['plot']:

            return
        plots = data['plot']
        title = data['name']

        for plot in plots:
            for word in re.findall(r'\w+',plot['text'].lower()):
                #if word in self.stop:
                    #continue
                yield (title, stem(word)), 1

    def sum_words(self, key, counts):
        total = 0
        for count in counts:
            total += count

        yield key, total

    def flip_title_and_count(self, key, count):
        title, word = key
        yield title, (word, count)

    def get_doc_word_count(self, title, word_counts):
        doc_word_count = 0
        word_counts = list(word_counts)
        for word_count in word_counts:
            _, count = word_count
            doc_word_count += count
        for word_count in word_counts:
            word, count = word_count
            yield (title, word), (count, doc_word_count)

    def extract_word(self, title_and_word, count_and_doc_count):
        title, word = title_and_word
        count, doc_word_count = count_and_doc_count
        yield word, (title, count, doc_word_count, 1)

    def get_doc_freq(self, word, infos):
        infos = list(infos)
        doc_freq = len(infos)
        for info in infos:
            title, count, doc_word_count = info[:3]
            yield (title, word), (count, doc_word_count, doc_freq)

    def calc_tfidf(self, title_and_word, counts):
        title, word = title_and_word
        count, doc_word_count, doc_freq = counts
        tf = 1 + math.log(count)
        if doc_freq == 0:
            idf = 0
        else:
            # idf = math.log( 395101 / doc_freq )
            idf = math.log( 20 / doc_freq )
        # found this number with the following query in mongo
        #   db.movies.find({"plot": { "$exists": true}}).count()
        yield title, (word, tf, idf)

    def combine_tfidfs(self, title, word_tfidf_list):
        tfidf_list = []
        for word_tfidf in word_tfidf_list:
            word, tf, idf = word_tfidf
            tfidf = tf * idf
            tfidf_list.append((word, tfidf))

        magnitude = 0
        for word_tfidf in tfidf_list:
            _, tfidf = word_tfidf
            magnitude += tfidf**2
        magnitude = math.sqrt(magnitude)

        normalized_list = []
        for word_tfidf in tfidf_list:
            normalized_list.append((word_tfidf[0], word_tfidf[1] / magnitude))

        yield title, normalized_list
        

    def steps(self):
        return [self.mr(mapper = self.counter, reducer = self.sum_words),
            self.mr(mapper = self.flip_title_and_count, reducer = self.get_doc_word_count),
            self.mr(mapper = self.extract_word, reducer = self.get_doc_freq),
            self.mr(mapper = self.calc_tfidf, reducer = self.combine_tfidfs)]

if __name__ == '__main__':
    TfidfCalculator.run()