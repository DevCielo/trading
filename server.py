from flask import Flask, jsonify
from flask_cors import CORS
from scraping.investing_com import get_pair
from api.oanda_api import OandaApi
from api.web_options import get_options
import http

from scraping.bloomberg_com import bloomberg_com

app = Flask(__name__)
CORS(app)

def get_reponse(data):
    if data is None:
        return jsonify(dict(message='error getting data')), http.HTTPStatus.NOT_FOUND
    else:
        return jsonify(data)


@app.route('/api/test')
def test():
    return jsonify(dict(message='hello'))

@app.route("/api/headlines")
def headlines():
    return get_reponse(bloomberg_com())

@app.route("/api/account")
def account():
    return get_reponse(OandaApi().get_account_summary())

@app.route("/api/options")
def options():
    return get_reponse(get_options())

@app.route("/api/technicals/<pair>/<tf>")
def technicals(pair, tf):
    return get_reponse(get_pair(pair, tf))

@app.route("/api/prices/<pair>/<granularity>/<count>")
def prices(pair, granularity, count):
    return get_reponse(OandaApi().web_api_candles(pair, granularity, count))

if __name__ == '__main__':
    app.run(debug=True)