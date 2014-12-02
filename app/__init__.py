from flask import Flask
app = Flask(__name__)

@app.route("/trackflix")
def hello():
    return "Hello!"

@app.route("/trackflix/search")
def search():
	return "This is the search result"

if __name__ == "__main__":
    app.run()