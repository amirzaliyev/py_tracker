import json
import os

DATA_FILE = 'data.json'

def load_data():
    """Load data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {
            "branches": {},
            "employees": {},
            "products": {}
        }

    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    """Save data to the JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
