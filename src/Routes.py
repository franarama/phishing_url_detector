from flask import Flask, render_template, request
from avoidmain import percentage

url = ''

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def urltest():
    form = request.form
    if request.method == 'POST':
        url = request.form['url']
        print("got the url: " + url)
        print("the percentage ", percentage(url))
        percent = percentage(url)
        return render_template('index.html', percent=percent)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()


    # CODE OFF PYTHONANYWHERE
    # from flask import Flask, render_template, request
    # from src.avoidmain import percentage
    # url = ''


    # app = Flask(__name__)

    # @app.route('/', methods = ['POST', 'GET'])
    # def urltest():
    # 	form = request.form
    # 	if request.method == 'POST':
    # 		form = request.form
    # 		url = request.form['url']
    # 		print("got the url: " + url)
    # 		print("the percentage ", percentage(url))
    # 		percent= percentage(url)
    # 		return render_template('index.html', percent = percent)
    # 	return render_template('index.html', form = form)
    # if __name__ == '__main__':
    # 	app.run()
