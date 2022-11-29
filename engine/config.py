import json

# Simple load of dict from config JSON file
with open('config.json') as file:
    CONFIG = json.load(file)