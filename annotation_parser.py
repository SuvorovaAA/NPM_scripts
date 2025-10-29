import json
import argparse

parser = argparse.ArgumentParser(description="""
    This script parses interproscan annotation, then 
    retrieves NPM-like domain sequences and writes to 
    fasta file, and also formats information about
    domains and disorder regions to load it into iTOL. 
    """)

parser.add_argument('in_file', help='input fasta file')
args = parser.parse_args()

tree_filename = args.in_file
path = '/'.join(args.in_file.split('/')[:-1]) + '/'

with open(path + 'interproscan_res/sequences_with_outgroup.faa.json') as file:
    annot = json.load(file)['results']

id_descr = {}
npms = {}

species_counter = {}
tmp_id_2_id = {}

with open(args.in_file) as file:
    for line in file:
        if line.startswith('>'):
            identifier = line[1:].split()[0]
            species = line.split('[')[1][:-1].split()
            short_name = species[0][:3] + species[1][:2]
            num = species_counter.get(short_name, 0)
            tmp_id = f'{short_name}{num:02d}'  # otherwise one id is a substring of another one
            species_counter[short_name] = num + 1
            species_str = ' '.join(species).replace(']', '')
            tmp_id_2_id[tmp_id] = species_str  + '-' + identifier

with open(path + '/tmp_id_2_id.json', "w") as file:
    json.dump(tmp_id_2_id, file, indent=4)

for res in annot:
    for val in tmp_id_2_id.values():
        if val.endswith(res['xref'][0]['id']):
            key = val
            break
    length = len(res['sequence'])
    id_descr[key] = str(length)
    for match in res['matches']:
        type_name = match['signature']['type']
        feature = ''
        if match['signature']['name'] is not None:
            feature = match['signature']['name']
        for loc in match['locations']:
            start = loc['start']
            end = loc['end']
            color = ''
            if type_name == 'REGION' and feature == 'disorder_prediction':
                color = '#F69697'      # red
            elif type_name == 'DOMAIN':
                color = '#8FD3FE'      # blue
                if 'NPM' in feature or 'NPL' in feature or 'Nucleoplasmin' in feature:
                    npms[key] = [res['sequence'][start - 1 : end], (start, end)]
            if color:
                id_descr[key] += f',RE|{start}|{end}|{color}|{feature}'   # RE for rectangle

with open(path + 'interproscan_domains_itol.txt', 'w') as outfile:
    print('''DATASET_DOMAINS
SEPARATOR COMMA
DATASET_LABEL,MobiDB and Secondary Structure
COLOR,#000000
LABEL_AUTO_COLOR,1
BACKBONE_COLOR,#aaaaaa
BACKBONE_HEIGHT,10
BORDER_WIDTH,0
GRADIENT_FILL,0
DATA''', file=outfile)
    for key, val in id_descr.items():
        print(f'{key},{val}', file=outfile)

with open(path + 'NPM_sequences.faa', 'w') as outfile:
    for key, val in npms.items():
        print(f'>{key}', file=outfile)
        print(val[0], file=outfile)

with open(path + 'NPM_coordinates.txt', 'w') as outfile:
    for key, val in npms.items():
        print(key, file=outfile)
        print(f'{val[1][0]}..{val[1][1]}', file=outfile)
