import json
from tqdm import tqdm

def get_locations_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        source_data = file.read()
        data = source_data.replace("}\n{", "},{")
        json_arr = json.loads("[" + data + "]")
        json_arr = remove_duplicates(json_arr)
        return json_arr


def remove_duplicates(arr):
    arr_no_dup = []
    checked = []

    for index, value in enumerate(tqdm(arr)):
        if index in checked:
            continue

        duplicates = []
        for possible_duplicate_index, possible_duplicate in enumerate(arr):
            if ((possible_duplicate.get('name') == value.get('name') and possible_duplicate.get(
                    'population') == value.get('population')) or
                    possible_duplicate['display_name'] == value['display_name'] or
                    (possible_duplicate.get('name') == value.get('name') and possible_duplicate['address'].get(
                        'county') == value['address'].get('county') and possible_duplicate['address'].get('state') ==
                     value['address'].get('state'))):
                duplicates.append(possible_duplicate)

        for possible_duplicate_index, possible_duplicate in enumerate(duplicates):
            if possible_duplicate_index != index:
                checked.append(possible_duplicate_index)

        # get the largest
        largest = max(duplicates, key=lambda x: (abs(x['bbox'][0] - x['bbox'][2]) * abs(x['bbox'][1] - x['bbox'][3])))

        arr_no_dup.append(largest)

    return arr_no_dup


def main():
    # cities = get_locations_data("resources/kr/place-city.ndjson")
    # towns = get_locations_data("resources/kr/place-town.ndjson")
    # villages = get_locations_data("../resources/gb/place-village.ndjson")
    hamlets = get_locations_data("../resources/gb/place-hamlet.ndjson")

    # all_data = cities + towns + villages + hamlets
    all_data = hamlets

    with open("../output/all-settlements.json", 'w', encoding='utf-8') as file:
        json.dump(all_data, file, indent=4)


if __name__ == "__main__":
    main()