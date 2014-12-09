import simplejson as json
# from time import sleep
import pymongo

conn = pymongo.Connection('localhost', 27017)
db = conn['imdb']
total = 12050
breakpoint = 600
print
with open('top6_over_2000_ratings.json') as f:
	count = 0
	for line in f:
		movie = json.loads(line)
		movie_title = movie['name'][1:-1]
		related = movie['similarities'].keys()
		related = map(lambda s: s[1:-1], related)
		query_dict = {'name': movie_title}
		update_dict = {'$set': {'related': related}}
		# print query_dict
		# print update_dict
		# print
		count += 1
		# if count > 5000: break
		if count > breakpoint:
			breakpoint += 600
		CURSOR_UP_ONE = '\x1b[1A'
		ERASE_LINE = '\x1b[2K'
		print CURSOR_UP_ONE + ERASE_LINE, '['+('='*(breakpoint/600-1))+(' '*(20-(breakpoint/600-1)))+']', count, '/', total
		db.movies.update(query_dict, update_dict)
		# sleep(0.0005)