from flask import Flask
app = Flask(__name__)

@app.route("/trackflix")
def hello():
    return render_template('index.html')

@app.route("/trackflix/search")
def search():
	#connect to mongo
	# get the top 10 movies for the searhc
	# get the image url for each movie
	# {("Title", "image url"): [("Title", "image url"), ("Title", "image url"), ("Title", "image url"), ("Title", "image url")]}
	return "This is the search result"

if __name__ == "__main__":
    app.run()