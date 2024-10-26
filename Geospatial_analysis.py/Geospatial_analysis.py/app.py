import ee
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

service_account = 'minetech@minetech-438118.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'service_account.json')
ee.Initialize(credentials)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_ip_location', methods=['GET'])
def get_ip_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_gee_data', methods=['POST'])
def get_gee_data():
    data = request.json
    dataset = data['dataset']
    bounds = data['bounds']
    zoom = data['zoom']

    # Convert bounds to ee.Geometry
    roi = ee.Geometry.Rectangle(bounds)

    # Get the appropriate dataset
    if dataset == 'cloud':
        collection = ee.ImageCollection('COPERNICUS/S2_SR').filterBounds(roi).sort('CLOUDY_PIXEL_PERCENTAGE').first()
        vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}
    elif dataset == 'land_use':
        collection = ee.ImageCollection('MODIS/006/MCD12Q1').sort('system:time_start', False).first().select('LC_Type1')
        vis_params = {'min': 1, 'max': 17, 'palette': [
            '05450a', '086a10', '54a708', '78d203', '009900', 'c6b044', 'dcd159',
            'dade48', 'fbff13', 'b6ff05', '27ff87', 'c24f44', 'a5a5a5', 'ff6d4c',
            '69fff8', 'f9ffa4', '1c0dff'
        ]}
    elif dataset == 'topography':
        collection = ee.Image('USGS/SRTMGL1_003')
        vis_params = {'min': 0, 'max': 4000, 'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
    elif dataset == 'soil_moisture':
        collection = ee.ImageCollection('NASA_USDA/HSL/SMAP_soil_moisture').select('smp').filterBounds(roi).sort('system:time_start', False).first()
        vis_params = {'min': 0, 'max': 0.5, 'palette': ['ff0000', 'ffff00', '00ff00']}
    elif dataset == 'earthquakes':
        collection = ee.FeatureCollection('USGS/ANSS/Comcat').filterBounds(roi)
        vis_params = {'color': 'red'}
    else:
        return jsonify({'error': 'Invalid dataset'})

    # Adjust scale based on zoom level
    scale = 10000 // (2 ** (zoom - 3))  # Adjust this formula as needed

    # Create the image and set its projection
    if dataset != 'earthquakes':
        image = collection.reproject(crs='EPSG:3857', scale=scale)
        map_id = image.getMapId(vis_params)
        tile_url_template = map_id['tile_fetcher'].url_format
    else:
        image = ee.Image().paint(collection, 1, 3)
        map_id = image.getMapId(vis_params)
        tile_url_template = map_id['tile_fetcher'].url_format

    return jsonify({
        'tile_url': tile_url_template
    })

if __name__ == '__main__':
    app.run(debug=True)