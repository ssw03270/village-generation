import numpy as np
import matplotlib.pyplot as plt

def visualize_building(building_polygons, original_size, crop_size):
    fig, ax = plt.subplots()

    # 원본 이미지 크기에서 중앙 부분의 좌표 계산
    start_x = (original_size[1] - crop_size[1]) // 2
    end_x = start_x + crop_size[1]
    start_y = (original_size[0] - crop_size[0]) // 2
    end_y = start_y + crop_size[0]

    # 배경 설정
    ax.imshow(np.zeros(original_size), cmap='gray')

    # 폴리곤 시각화
    for polygon in building_polygons:
        ax.plot(polygon[:, 1], polygon[:, 0], linewidth=2)

    # 시각화할 부분을 제한
    ax.set_xlim([start_x, end_x])
    ax.set_ylim([end_y, start_y])
    ax.set_title("Building Polygons")
    plt.show()

def visualize_road(road_polygons, original_size, crop_size):
    fig, ax = plt.subplots()

    # 원본 이미지 크기에서 중앙 부분의 좌표 계산
    start_x = (original_size[1] - crop_size[1]) // 2
    end_x = start_x + crop_size[1]
    start_y = (original_size[0] - crop_size[0]) // 2
    end_y = start_y + crop_size[0]

    # 배경 설정
    ax.imshow(np.zeros(original_size), cmap='gray')

    # 폴리곤 시각화
    for polygon in road_polygons:
        ax.plot(polygon[:, 1], polygon[:, 0], linewidth=2)

    # 시각화할 부분을 제한
    ax.set_xlim([start_x, end_x])
    ax.set_ylim([end_y, start_y])
    ax.set_title("Road Polygons (Cropped)")
    plt.show()

def visualize_road_and_building(road_polygons, building_polygons, original_size, file_name):
    fig, ax = plt.subplots(figsize=(original_size[1] // 100, original_size[0] // 100))

    # 배경 설정
    ax.imshow(np.zeros(original_size), cmap='gray')

    # 도로 폴리곤 시각화
    for polygon in road_polygons:
        ax.plot(polygon[:, 1], polygon[:, 0], color='white', linewidth=2)

    # 건물 폴리곤 시각화
    for polygon in building_polygons:
        ax.plot(polygon[:, 1], polygon[:, 0], color='white', linewidth=2)

    # 시각화 설정
    ax.set_xlim([0, original_size[1]])
    ax.set_ylim([original_size[0], 0])
    ax.set_title("Road and Building Polygons")

    # 이미지 저장
    save_path = f'../output/{file_name}.png'
    plt.savefig(save_path, pad_inches=0)
    plt.close()