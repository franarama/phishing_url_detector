from flask import Flask, render_template, request
from avoidmain import percentage
url = ''


app = Flask(__name__)

@app.route('/', methods = ['POST'])
def urltest():
	if request.method == 'POST':
		form = request.form
		url = request.form['url']
		print("got the url: " + url)
		print("the percentage ", percentage(url))
		percent= percentage(url)
		return render_template('index.html', percent = percent)
if __name__ == '__main__':
	app.run(debug = True)