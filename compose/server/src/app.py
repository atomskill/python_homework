import os
from flask import Flask

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/', methods=['GET'])
def foo():
	return {'text':'ok'}

app.run('0.0.0.0', int(os.environ['port']))
