import ee

# Initialize the Earth Engine module
ee.Initialize()

def get_data():
    # Example of retrieving specific dataset (modify as needed)
    dataset = ee.ImageCollection('MODIS/006/MOD13A2').select('NDVI')

    # Example: Specify a region of interest (modify coordinates as needed)
    roi = ee.Geometry.Rectangle([-122.6, 37.6, -122.3, 37.8])

    # Fetching the data
    image = dataset.mean().clip(roi)

    # Return the URL for visualization
    url = image.getThumbUrl({'min': 0, 'max': 9000, 'dimensions': '512x512'})
    return {'url': url}
import ee

# Initialize the Earth Engine module
ee.Initialize()

def get_data(dataset):
    # Set up a region of interest based on coordinates from IP location
    # Example: Change this to handle specific datasets
    roi = ee.Geometry.Rectangle([-122.6, 37.6, -122.3, 37.8])  # Example coordinates

    
    if dataset == 'cloud':
        collection = ee.ImageCollection('COPERNICUS/S2').filterBounds(roi).first()
    elif dataset == 'land_use':
        collection = ee.ImageCollection('USDA/NASS/CDL').first()
    elif dataset == 'topography':
        collection = ee.Image('USGS/SRTMGL1_003')
    elif dataset == 'soil_moisture':
        collection = ee.ImageCollection('NASA/SMAP/SPL3SMP_E/V4')
    elif dataset == 'earthquakes':
        # Example earthquake dataset (modify based on actual dataset)
        collection = ee.FeatureCollection('USGS/earthquakes')
    else:
        return {'error': 'Dataset not found'}

    # Fetch the data
    image_json = collection.getThumbUrl({'min': 0, 'max': 9000, 'dimensions': '512x512'})
    return {'url': image_json}
