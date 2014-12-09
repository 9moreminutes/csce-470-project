from flask import Flask
from flask import render_template
from flask import request
import pymongo
app = Flask(__name__)

@app.route("/trackflix")
def hello():
    return render_template('index.html')


# http://matthewh.net/trackflix/search?q=TheBeatles
@app.route("/trackflix/search")
def search():
        search_term = str(request.args.get('q'))
        conn = pymongo.Connection('localhost', 27017)
        db = conn['imdb']
        related_search_dict = { '$or': [ { 'soundtrack': { '$elemMatch': { 'singers': {'$regex': '.*' + search_term + '.*'}} } }, { 'soundtrack': { '$elemMatch': { 'artists': {'$regex': '.*' + search_term + '.*'}} } }, { 'soundtrack': { '$elemMatch': { 'lyricists': {'$regex': '.*' + search_term + '.*'}} } }, { 'soundtrack': { '$elemMatch': { 'performers': {'$regex': '.*' + search_term + '.*'}} } }, { 'soundtrack': { '$elemMatch': { 'writers': {'$regex': '/.*' + search_term + '.*/'}} } }, { 'soundtrack': { '$elemMatch': { 'composers': {'$regex': '/.*' + search_term + '.*/'}} } }]}
        projection_dict = {'name': 1, 'image_url': 1, 'related': 1, '_id': 0}
        docs = db.movies.find(related_search_dict, projection_dict).limit(10)
        results_dict = {}
        for doc in docs:
                image = '/static/images/cav.png'
                if 'image_url' in doc:
                        image = doc['image_url'].encode('utf-8')
                result_key = (doc['name'].encode('utf-8'), image)
                result_array = []
                if 'related' not in doc:
                        continue
                for related_movie in doc['related']:
                        related_image = '/static/images/cav.png'
                        curs = db.movies.find({'name': related_movie.encode('utf-8')}, projection_dict).limit(1)
                        for db_result in curs:
                                if 'image_url' in db_result:
                                        related_image = db_result['image_url'].encode('utf-8')
                        result_value = (related_movie.encode('utf-8'), related_image)
                        result_array.append(result_value)
                results_dict[result_key] = result_array

        return render_template('search_results.html', results = results_dict)

if __name__ == "__main__":
    app.run()