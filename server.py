from models.job_configuration import JobConfiguration
import datetime
from flask import Flask, jsonify, request, make_response

server = Flask(__name__)
FILE_PATH = './config.json'


@server.route('/')
def main():
    print(f'Main route accessed at {datetime.datetime.now()}')
    return 'ACK'


@server.get('/config')
def get_config():
    config = JobConfiguration.read(FILE_PATH)
    data = config.__dict__()
    json = jsonify(data)
    return json


@server.post('/config')
def save_config():
    if request.json is None:
        return make_response('Invalid JSON.', 400)

    json = request.get_json()
    config = JobConfiguration.from_json(json)
    config.write(FILE_PATH)
    res = make_response('', 204)
    print('config saved!')
    return res


@server.post('/job')
def immediate_job():
    if request.json is None:
        return make_response('Invalid JSON.', 400)

    json = request.get_json()

    if 'volume' not in json:
        return make_response('Missing required parameter: volume', 400)

    volume = json['volume']
    print(f'executing immediate job of {volume}mL')
    return make_response('', 204)


server.run(host='localhost', port=5000)
