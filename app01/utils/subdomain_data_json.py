import json


def text_to_json(text_path):
    # Load JSON data from file
    with open(text_path, 'r') as f:
        data = json.load(f)

    # Create a new array of objects with key-value pairs
    new_data = [{'subdomain': item} for item in data]

    # Convert the new array to JSON and print it
    new_json = json.dumps(new_data)
    # print(new_json)
    return new_json


if __name__ == '__main__':
    text_to_json()
