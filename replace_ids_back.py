import json
import argparse

parser = argparse.ArgumentParser(description="""
    This is a crutch script to return normal ids
    to the tree.
    """)

parser.add_argument('in_file', help='input alignment file')
args = parser.parse_args()

tree_filename = args.in_file
path = '/'.join(args.in_file.split('/')[:-1]) + '/'

with open(path + "tmp_id_2_id.json") as file:
    tmp_id_2_id = json.load(file)

with open(tree_filename) as file:
    tree = file.read()

for key, val in tmp_id_2_id.items():
    tree = tree.replace(key, val)

with open(path + 'tree_fixed.nwk', 'w') as file:
    file.write(tree)