import json

def dump_data(file, data):
	with open(file, 'w') as out:
		json.dump(data, out, indent=4)

def read_data(file):
	with open(file, 'r') as f:
		return json.load(f)