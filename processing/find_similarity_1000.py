import math   
import simplejson as json 
import operator
import sys

def magnitude(tfidf_vector):
    total = 0
    for word, tfidf in tfidf_vector:
        total += tfidf**2
    mag = math.sqrt(total)
    return mag    

def dot(one, two):
    total = 0
    one_words = dict(one)
    two_words = dict(two)
    for term, value in one_words.iteritems():
        if term in two_words:
            total += one_words[term] * two_words[term]
    return total

def cosine_tfidf(one, two):
    mag_1 = magnitude(one)
    mag_2 = magnitude(two)
    one_dot_two = dot(one, two)
    cosine_value = one_dot_two/(mag_1*mag_2)
    return cosine_value

def main():
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    filename = 'filtered_data_2000.txt'
    tfidf_lists = {}
    titles = []
    with open(filename) as f:
        for line in f:
            title, raw_tfidf_list = line.split('\t')[:2]
            tfidf_list = json.loads(raw_tfidf_list)
            tfidf_lists[title] = tfidf_list
            titles.append(title)

# {
#     name: 'title1',
#     related: [
#         'title2',
#         'title2',
#         'title2',
#         'title2',
#         'title2',
#         'title2',
#     ]
# }
    count = start
    total = len(titles)
    print total
    outfile = "all_similarity_matrix_2000_" + str(start) + ".json" 
    with open(outfile, 'w') as f:
        my_title_block = titles[start:end]
        for title1 in my_title_block:
            # if '(TV)' in title1:
            #     print 'SKIPPING:', title1
            #     count+=1
            #     continue
            # if '(VG)' in title1:
            #     print 'SKIPPING:', title1
            #     count+=1
            #     continue
            json_dict = {}
            json_dict['name'] = title1
            similarities = {}
            for title2 in titles:
                if title1 == title2: continue
                # if '(TV)' in title2: continue
                # if '(VG)' in title2: continue
                cos_value = cosine_tfidf(tfidf_lists[title1], tfidf_lists[title2])
                similarities[title2] = cos_value
            top6_tuples = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)[:6]
            top_similarities = {}
            for movie, sim in top6_tuples:
                top_similarities[movie] = sim
            json_dict['similarities'] = top_similarities
            json.dump(json_dict, f)
            f.write('\n')
            count += 1
            print 'Done with', title1, count, 'of', total


if __name__ == '__main__':
    main()