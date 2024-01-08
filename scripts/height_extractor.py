import ee

ee.Authenticate()
# Initialize the Earth Engine module
ee.Initialize(project='ee-ssw03270')

# Define the coordinates of the bounding box (South-West, North-East)
sw_latitude = 33.4509  # 남서쪽 위도
sw_longitude = 126.40069  # 남서쪽 경도
ne_latitude = 33.4109  # 북동쪽 위도
ne_longitude = 126.36069  # 북동쪽 경도

# Create a rectangle for the bounding box
bbox = ee.Geometry.Rectangle([sw_longitude, sw_latitude, ne_longitude, ne_latitude])

# Load the elevation data
elevation = ee.Image('USGS/SRTMGL1_003')

# Clip the elevation data to the bounding box
elevation_clip = elevation.clip(bbox)

# Define visualization parameters for elevation in grayscale
vis_params = {
    'min': 0,  # 최소 높이 값 (조정 가능)
    'max': 3000,  # 최대 높이 값 (조정 가능)
    'palette': ['black', 'white']  # 흑백 팔레트
}

# Create a URL to the styled image for the specified region
url = elevation_clip.getThumbUrl({
    'min': 0, 'max': 3000, 'dimensions': 512, 'region': bbox,
    'palette': ['black', 'white']
})

print("URL to download the grayscale height map image:", url)