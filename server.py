import waitress
import os
import logging
from flask import Flask, jsonify, request, make_response

from models.job_configuration import JobConfiguration

server = Flask(__name__)
FILE_PATH = './config.json'


@server.route('/')
def main():
    logging.info(f'Main route accessed.')
    return 'ACK'


@server.get('/config')
def get_config():
    logging.info('Request for config data.')

    try:
        config = JobConfiguration.read(FILE_PATH)
        data = config.__dict__()
        json = jsonify(data)
        return json
    except IOError as e:
        logging.error('Failed to read configuration file.')
        logging.debug('Error:')
        logging.debug(e)

        return make_response('Unable to read config data.', 500)


@server.post('/config')
def save_config():
    logging.info('Request to save config data.')
    if request.json is None:
        logging.error('JSON data not found in request body.')
        return make_response('Invalid JSON.', 400)

    json = request.get_json()

    try:
        config = JobConfiguration.from_json(json)
    except:
        logging.error('Unable to parse JSON into JobConfiguration')
        logging.debug(json)
        return make_response('Error: Unable to read JSON data.', 500)

    try:
        config.write(FILE_PATH)
        res = make_response('', 204)
        logging.info('New config saved!')
        return res
    except IOError as e:
        logging.error('Failed to write new config to file.')
        logging.debug('Error data:')
        logging.debug(e)
        return make_response('Error: Could not save JobConfiguration data.', 500)


@server.post('/job')
def immediate_job():
    logging.info('Request for immediate job.')
    if request.json is None:
        logging.error('JSON data not found in request body.')
        return make_response('Invalid JSON.', 400)

    json = request.get_json()

    if 'volume' not in json:
        logging.error('JSON missing "volume" key.')
        logging.debug(json)
        return make_response('Missing required parameter: volume', 400)

    volume = json['volume']
    logging.info(f'Executing immediate job of {volume}mL')
    return make_response('', 204)


if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG')
    if debug is not None and debug.lower() == 'true':
        logging.basicConfig(filename='pi-dispense.log', level=logging.DEBUG)
        logging.debug('Running in debug')
        server.run(host='localhost', port=5001, debug=True)
    else:
        logging.basicConfig(filename='pi-dispense.log', level=logging.INFO)
        logging.debug('Running in production')
        waitress.serve(server, host='0.0.0.0', port=5001)
