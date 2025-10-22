import json
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description="""
    This script takes in an interproscan output json file and
    gets consensus IDRs that are >= 30 nucleotides long.
    """)

parser.add_argument('in_file', help='json interproscan output file')
parser.add_argument('-O', default='IDR_sequences.faa', help='output fasta file')
parser.add_argument('-quiet', action='store_true', help='Not to display summary')

args = parser.parse_args()

with open(args.in_file) as f:
    data = json.load(f)

prot_counter = 0
IDR_counter = 0

with open(args.O, 'w') as outfile:
    for res in data['results']:
        prot_counter += 1
        for match in res['matches']:
            if match['signature']['description'] == 'consensus disorder prediction':
                for loc in match['locations']:
                    start = loc['start'] - 1   #for enumeration shift
                    end = loc['end'] - 1
                    if end - start > 30:
                        IDR_counter += 1
                        print(f'> {res["xref"][0]["name"]} {start}..{end}', file=outfile)
                        print(res['sequence'][start:end + 1], file=outfile)
                break

if not args.quiet:
    print(f'Retrieved {IDR_counter} IDRs form {prot_counter} protein sequences')