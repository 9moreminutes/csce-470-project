import math   
import simplejson as json 

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
    filename = 'test.out'
    tfidf_lists = {}
    titles = []
    with open(filename) as f:
        for line in f:
            title, raw_tfidf_list = line.split('\t')[:2]
            tfidf_list = json.loads(raw_tfidf_list)
            tfidf_lists[title] = tfidf_list
            titles.append(title)

    cosine_matrix = {}
    for title1 in titles:
        for title2 in titles:
            if title1 == title2: continue
            cos_value = cosine_tfidf(tfidf_lists[title1], tfidf_lists[title2])
            if title1 in cosine_matrix:
                cosine_matrix[title1][title2] = cos_value
            else: 
                cosine_matrix[title1] = {title2: cos_value}
    with open("similarity_matrix.json", 'w') as f:
        print json.dump(cosine_matrix, f)


if __name__ == '__main__':
    main()