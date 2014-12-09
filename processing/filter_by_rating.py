

filename = 'sample_ratings.txt'
valid_movies=[]
with open(filename) as f:
	for line in f:
		split_line = line.split()
		num_ratings = int(split_line[1])
		name = ' '.join(split_line[3:])
		if num_ratings > 2000:
			valid_movies.append(name)

filename = 'all_tfidf.out'
with open(filename) as fin:
	with open('filtered_data_2000.txt', 'w') as fout:
		for line in fin:
			movie_title = line.split('\t')[0]
			if '(TV)' in movie_title: continue
			if '(VG)' in movie_title: continue
			# for x in valid_movies:
				#print movie_title, x
			if movie_title[1:-1] in valid_movies:
				fout.write(line)