import json
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='read a tf json state file and search for a value')
parser.add_argument("--file", help="path to the json file to read", type=str, required=True)
parser.add_argument("--value", help="the image tag value to search for", type=str, required=True)
args = parser.parse_args()

with open(args.file, 'r') as f:
    data = json.loads(f.read())

print(data['values']['outputs'][f'{args.value}_image_tag']['value'])
