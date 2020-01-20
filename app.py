from flask import Flask, request, render_template, url_for, redirect
import senAnaly
from senAnaly import TwitterClient

app = Flask(__name__)

@app.route('/', methods = ["GET","POST"])
def index():
	if request.method == "POST":
		query = request.form['content']
		queryObject = TwitterClient()
		results = queryObject.main(query)

		return render_template('result.html', results = results)

	else:
		return render_template('index.html')
