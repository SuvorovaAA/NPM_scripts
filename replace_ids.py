import argparse
import json

parser = argparse.ArgumentParser(description="""
    This is a crutch script to make local FastME
    work properly.
    """)

parser.add_argument('in_file', help='input fasta file')

args = parser.parse_args()

path = '/'.join(args.in_file.split('/')[:-1]) + '/'

with open(path + "tmp_id_2_id.json") as file:
    tmp_id_2_id = json.load(file)

id_2_tmp_id = {id: tmp_id for tmp_id, id in tmp_id_2_id.items()}

out_path = path + '_out.'.join(args.in_file.split('/')[-1].split('.'))

with open(args.in_file) as file:
    with open(out_path, 'w') as out:
        for line in file:
            if line.startswith('>'):
                identifier = line[1:].rstrip()
                tmp_id = id_2_tmp_id[identifier]
                print(f'>{tmp_id}', file=out)
            else:
                print(line, end='', file=out)