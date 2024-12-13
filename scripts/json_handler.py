import json

def get_json_data(json_path):
    with open(json_path, 'r') as file:
            data = json.load(file)
    return data


def write_json_file(json_path_updated, data):
    
    with open(json_path_updated, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"json file: '{json_path_updated}' successfully created.")