import os
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ['API_KEY']
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path!= "" and os.path.exists("static/" + path):
        return send_from_directory('static', path)
    else:
        return "Not Found", 404

@app.route('/location1', methods=['GET'])
def get_locations():
    place = request.args.get('text')
    country_code_filter = request.args.get('filter', 'in')
    url = f'https://api.geoapify.com/v1/geocode/search?text={place}&filter=countrycode:{country_code_filter}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch places'}), response.status_code

@app.route('/places', methods=['GET'])
def get_places():
    categories = 'tourism.attraction'
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    radius = 5000
    limit = 20
    url = f'https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},{radius}&bias=proximity:{lon},{lat}&limit={limit}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch places'}), response.status_code

@app.route('/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Please provide latitude and longitude'}), 400
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            app.logger.error('Failed to fetch weather data: %s', response.text)
            return jsonify({'error': 'Failed to fetch weather data'}), response.status_code
    except Exception as e:
        app.logger.exception('An error occurred while fetching weather data')
        return jsonify({'error': 'Internal Server Error'}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=5090)
