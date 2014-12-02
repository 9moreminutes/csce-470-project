import re
soundtracks = {}

with open('testdata.txt') as f:
	lines = f.readlines()

	# split lines into sublists by movie
	indices = [i for (i, x) in enumerate(lines) if x == '\n']
	ends = indices + [len(lines)]
	begins = [0] + [x + 1 for x in indices]
	raw_soundtracks = [lines[begin:end] for (begin, end) in zip(begins, ends)]

	for title in raw_soundtracks:
		soundtrack = []
		movie_title = title[0][2:].strip()

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
		soundtracks[movie_title] = soundtrack

for movie, soundtrack in soundtracks.iteritems():
	print movie
	print soundtrack
			