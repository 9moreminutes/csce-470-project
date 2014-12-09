import re
import pymongo
soundtracks = {}

filename = 'sample_ratings.txt'
valid_movies=[]
with open(filename) as f:
	for line in f:
		split_line = line.split()
		num_ratings = int(split_line[1])
		name = ' '.join(split_line[3:])
		if num_ratings > 2000:
			valid_movies.append(name)

conn = pymongo.Connection('localhost', 27017)
db = conn['imdb']

with open('soundtracks.txt') as f:
	lines = f.readlines()

	# split lines into sublists by movie
	indices = [i for (i, x) in enumerate(lines) if x == '\n']
	ends = indices + [len(lines)]
	begins = [0] + [x + 1 for x in indices]
	raw_soundtracks = [lines[begin:end] for (begin, end) in zip(begins, ends)]
	count = 0
	total = len(raw_soundtracks)
	for title in raw_soundtracks:

		soundtrack = []
		movie_title = title[0][2:].strip()
		if movie_title not in valid_movies: continue
		if '(TV)' in movie_title: continue
		if '(VG)' in movie_title: continue
		count += 1
		# split list into sublists of song info
		songs_raw = title[1:]
		song_indices = [i for (i, x) in enumerate(songs_raw) if x.startswith('-')]
		song_ends = song_indices + [len(songs_raw)]
		if song_ends[0] == 0:
			del song_ends[0]
		song_begins = []
		if 0 not in song_indices:
			song_begins.append(0)
		song_begins = song_begins + [x for x in song_indices]
		songs = [songs_raw[begin:end] for (begin, end) in zip(song_begins, song_ends)]

		for raw_song in songs:
			song = {}
			song['name'] = raw_song[0][2:].strip().strip('"\'')
			# print song['name']
			song_data = raw_song[1:]
			for data_line in song_data:
				data = data_line.split('by')
				# Get what the person/people did
				action = data[0].strip()

				# process the names
				info = "".join(data[1:]).strip()
				info = info.replace('(qv)', '').strip()
				info = info.strip('"\'')
				info = re.split(",|&", info)
				info = [i.strip().strip('"\'') for i in info]

				# add the names to our song dict
				if 'written' in action.lower(): song['writers'] = info
				elif 'performed' in action.lower(): song['performers'] = info
				elif 'published' in action.lower(): song['publishers'] = info
				elif 'lyrics' in action.lower(): song['lyricists'] = info
				elif 'music' in action.lower(): song['artists'] = info
				elif 'composed' in action.lower(): song['composers'] = info
				elif 'sung' in action.lower(): song['singers'] = info

			# put the song in the soundtrack list for this movie
			soundtrack.append(song)

		# add the soundtrack for this movie to our full dict of soundtracks

		query_dict = {'name': movie_title}
		update_dict = {'$set': {'soundtrack': soundtrack}}
		print query_dict
		print update_dict
		db.movies.update(query_dict, update_dict, True)
		soundtracks[movie_title] = soundtrack
		print 'Done with', count, 'of', total
