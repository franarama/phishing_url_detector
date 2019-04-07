from flask import Flask, render_template, request
from avoidmain import percentage
from feature_extraction import FeSingleURL
import pickle

url = ''

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def predict(to_check):

    model = pickle.load(open('model.pkl', 'rb'))

    if request.method == 'POST':
        fes = FeSingleURL(to_check)
        data = fes.main()
        # print("DATA=", data)
        # print("url to check: ", to_check)
        prediction = model.predict(data)
        return prediction



@app.route('/', methods=['POST', 'GET'])
def urltest():
    form = request.form
    if request.method == 'POST':
        url_to_check = request.form['url']
        print("got the url: " + url_to_check)
        prediction = predict(url_to_check)
        # 0 - not phishing, 1 - phishing
        print(prediction)
        return render_template('index.html', prediction=prediction)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


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
