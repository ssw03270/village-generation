import numpy as np
from shapely.geometry import Polygon
from skimage import io, color
from skimage.measure import find_contours, approximate_polygon


def get_road_polygons(center_latitude, center_longitude, api_key, map_zoom=20, map_size=(600, 600)):
    # Google Static Maps URL 설정
    map_center = f"{center_latitude},{center_longitude}"
    map_zoom = str(map_zoom)
    map_size_str = f"{map_size[0]}x{map_size[1]}"

    style = "feature:road|element:geometry.stroke|visibility:on|color:0xffffff|weight:1"

    url = f"http://maps.googleapis.com/maps/api/staticmap?center={map_center}&zoom={map_zoom}&size={map_size_str}&maptype=roadmap&style=visibility:off&style={style}&key={api_key}"

    # 이미지 처리
    img = io.imread(url)
    gray_img = color.rgb2gray(img)
    binary_image = np.where(gray_img < np.mean(gray_img), 0.0, 1.0)  # 도로는 어두운 색
    contours = find_contours(binary_image, 0.1)

    # 도로 폴리곤 추출
    road_polygons = [approximate_polygon(contour, tolerance=2) for contour in contours if len(contour) > 100]
    return road_polygons


def get_building_polygons(center_latitude, center_longitude, api_key, map_zoom=20, map_size=(600, 600)):
    # Google Static Maps URL 설정
    map_center = f"{center_latitude},{center_longitude}"
    map_zoom = str(map_zoom)
    map_size_str = f"{map_size[0]}x{map_size[1]}"
    style = "feature:landscape.man_made|element:geometry.stroke|visibility:on|color:0xffffff|weight:1"

    url = f"http://maps.googleapis.com/maps/api/staticmap?center={map_center}&zoom={map_zoom}&size={map_size_str}&maptype=roadmap&style=visibility:off&style={style}&key={api_key}"

    # 이미지 로드 및 처리
    img = io.imread(url)
    gray_img = color.rgb2gray(img)
    binary_image = np.where(gray_img > np.mean(gray_img), 0.0, 1.0)
    contours = find_contours(binary_image, 0.1)

    # 폴리곤 추출
    polygons = []
    for contour in contours:
        if len(contour) > 10:  # 폴리곤 최소 길이 필터
            polygon = approximate_polygon(contour, tolerance=2)
            polygons.append(polygon)

    return polygons


def filter_overlapping_polygons(polygons):
    filtered_polygons = []
    for i, polygon1 in enumerate(polygons):
        poly1 = Polygon(polygon1)
        overlap = False
        for j, polygon2 in enumerate(polygons):
            if i != j:
                poly2 = Polygon(polygon2)
                if poly1.intersects(poly2):
                    # 두 폴리곤의 교차 면적이 더 작은 폴리곤의 면적의 50% 이상인지 확인
                    intersection_area = poly1.intersection(poly2).area

                    if intersection_area > 0.5 * min(poly1.area, poly2.area):
                        # 더 큰 폴리곤을 필터링 목록에서 제거
                        if poly1.area > poly2.area:
                            overlap = True
                            break
        if not overlap:
            filtered_polygons.append(polygon1)
    return filtered_polygons


def remove_invalid_polygons(polygons):
    valid_polygons = []
    for polygon in polygons:
        if len(polygon) < 3:
            continue

        # Polygon 객체로 변환
        poly = Polygon(polygon)
        # 폴리곤의 유효성 검사
        if poly.is_valid:
            valid_polygons.append(polygon)
    return valid_polygons


def get_chunk_centers_within_bbox(bbox, chunk_size, zoom):
    north, south, west, east = bbox

    meters_per_pixel = 156543.03392 * np.cos(north * np.pi / 180) / (2 ** zoom)
    meters_per_chunk = chunk_size * meters_per_pixel

    # bbox를 덮는 청크의 시작 및 종료 좌표 계산
    start_x = int(north * 111320 // meters_per_chunk)
    end_x = int(south * 111320 // meters_per_chunk) - 1
    start_y = int(west * 111320 * np.cos(north * np.pi / 180) // meters_per_chunk)
    end_y = int(east * 111320 * np.cos(north * np.pi / 180) // meters_per_chunk) + 1

    centers = []
    coords = []
    coord_x = 0
    coord_y = 0
    for y in range(start_y - 1, end_y + 1):
        for x in range(start_x + 1, end_x - 1, -1): # 북쪽에서 남쪽으로 이동
            center_lat = x * meters_per_chunk / 111320
            center_lng = y * meters_per_chunk / (111320 * np.cos(north * np.pi / 180))
            centers.append((center_lat, center_lng))
            coords.append([coord_x, coord_y])
            coord_x += 1
        coord_y += 1
        coord_x = 0

    return centers, start_x - end_x, end_y - start_y, coords

def get_valid_polygons(polygons, start_point, end_point):
    _polygons = []
    for polygon in polygons:
        if np.all(polygon[:, 0] > start_point[0]) and np.all(polygon[:, 1] > start_point[1]):
            if np.all(polygon[:, 0] < end_point[0]) and np.all(polygon[:, 1] < end_point[1]):
                continue
        _polygons.append(polygon)
    return _polygons
