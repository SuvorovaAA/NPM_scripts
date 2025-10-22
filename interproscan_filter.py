import json
import argparse
import pandas as pd
from tqdm import tqdm
import os
import subprocess

parser = argparse.ArgumentParser(
    description="""
    This script takes in a tsv file containing organism
    name and assembly ID, then launches interproscan that
    filters blast results and outputs those containing 
    nucleoplasmin or NPM-like domain.
    """)

parser.add_argument('in_file', help='tsv table name')
parser.add_argument('-quiet', action='store_true', help='Not to display summary')

args = parser.parse_args()

summary = []

df = pd.read_csv(args.in_file, sep='\t')

os.chdir('../blast_results')

for index, row in tqdm(df.iterrows()):
    orgn_name = '_'.join(row['Species'].split())

    blast_res = f'{orgn_name}/unique_blastp_res.faa'
    out_dir = f'{orgn_name}/interproscan_res'

    os.makedirs(out_dir, exist_ok=True)
    command = f'docker run --rm -v /home/sasha_suvorova/interproscan-5.76-107.0/data:/opt/interproscan/data -v {os.getcwd()}:/work interpro/interproscan:5.76-107.0 --input /work/{blast_res} --output-dir /work/{out_dir} --cpu 8'
    subprocess.check_output(command.split())

    out_path = out_dir + '/' + 'unique_blastp_res.faa.json'
    with open(out_path) as f:
        data = json.load(f)

    res_counter = [0, 0]
    with open(f'{orgn_name}/blastp_res_filtered.faa', 'w') as outfile:
        for res in data['results']:
            res_counter[0] += 1
            for match in res['matches']:
                feature = match['signature']['name']
                if feature is not None and 'nucleoplasmin' in feature.lower():
                    res_counter[1] += 1
                    loc = match['locations'][0]
                    print('>' + res['xref'][0]['name'], file=outfile)
                    print(res['sequence'], file=outfile)
                    break
    summary.append(f'{orgn_name.ljust(20)} {res_counter[0]}->{res_counter[1]}')

if not args.quiet:
    print(*summary, sep='\n')