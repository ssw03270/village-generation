import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from geo_utils import get_building_polygons, get_road_polygons, filter_overlapping_polygons, remove_invalid_polygons, get_chunk_centers_within_bbox, get_valid_polygons
from plot_utils import visualize_building, visualize_road, visualize_road_and_building

data_path = '../output/all-settlements.json'
with open(data_path, "r", encoding="utf-8") as file:
    settlements = json.load(file)

    for idx, settlement in enumerate(tqdm(settlements[0:10])):
        display_name = settlement['display_name']
        location = [settlement['location'][1], settlement['location'][0]]
        bbox = [settlement['bbox'][3], settlement['bbox'][1], settlement['bbox'][0], settlement['bbox'][2]]
        print(idx, display_name, location, bbox)

        api_key = "AIzaSyCmCcz_ah9rqFNj4fK4b_MF1JaziBax27E"  # 여기에 Google API 키를 입력하세요
        map_size = (640, 640)
        chunk_size = 600
        map_zoom = 18

        centers, len_x, len_y, coords = get_chunk_centers_within_bbox(bbox, chunk_size, map_zoom)
        print(centers)
        building_polygons = []
        road_polygons = []
        for idxx, center in enumerate(centers):
            center_latitude, center_longitude = center

            _building_polygons = get_building_polygons(center_latitude, center_longitude, api_key, map_size=map_size,
                                                      map_zoom=map_zoom)
            _building_polygons = remove_invalid_polygons(_building_polygons)
            _building_polygons = filter_overlapping_polygons(_building_polygons)
            _building_polygons = get_valid_polygons(_building_polygons, (600, 0), (640, 100))
            _building_polygons = get_valid_polygons(_building_polygons, (600, 500), (640, 640))

            for i in range(len(_building_polygons)):
                _building_polygon = np.array(_building_polygons[i])
                _building_polygon[:, 0] += coords[idxx][0] * chunk_size
                _building_polygon[:, 1] += coords[idxx][1] * chunk_size
                _building_polygons[i] = _building_polygon

            building_polygons += _building_polygons
            # visualize_building(building_polygons, map_size, crop_size)

            # 도로 폴리곤 추출
            _road_polygons = get_road_polygons(center_latitude, center_longitude, api_key, map_size=map_size,
                                              map_zoom=map_zoom)
            _road_polygons = get_valid_polygons(_road_polygons, (600, 0), (640, 100))
            _road_polygons = get_valid_polygons(_road_polygons, (600, 500), (640, 640))

            for i in range(len(_road_polygons)):
                _road_polygon = np.array(_road_polygons[i])
                _road_polygon[:, 0] += coords[idxx][0] * chunk_size
                _road_polygon[:, 1] += coords[idxx][1] * chunk_size
                _road_polygons[i] = _road_polygon
            print(coords[idxx])
            road_polygons += _road_polygons
            # road_polygons = remove_invalid_polygons(road_polygons)
            # visualize_road(road_polygons, map_size, crop_size)

        new_map_size = (map_size[0] * (len_x + 2), map_size[1] * (len_y + 2))
        visualize_road_and_building(road_polygons, building_polygons, new_map_size, file_name=f'{idx}_{idxx}_{center_latitude}_{center_longitude}')
