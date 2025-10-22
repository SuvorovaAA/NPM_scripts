import argparse
import pandas as pd
from tqdm import tqdm
import subprocess

parser = argparse.ArgumentParser(
    description="""
    This script takes in a tsv file containing organism
    name and assembly ID, then launches a script that
    performs blast search against dbs with ids from it
    using query file specified in config.ini, .
    """)

parser.add_argument('in_file', help='tsv table name')
parser.add_argument('-evalue', help='E-value threshold to use, default=1e-5', default=1e-5)
parser.add_argument('-word', help='Word size to use, >= 4, default=6', default=6)
parser.add_argument('-max_target_seqs', help='Maximal number of sequences. Not the best ones. default=500', default=500)
parser.add_argument('-db', choices=['nucl', 'prot'], help='Choose which database to use')
parser.add_argument('-quiet', action='store_true', help='Not to display summary')

args = parser.parse_args()

summary = []

df = pd.read_csv(args.in_file, sep='\t')
for index, row in tqdm(df.iterrows()):
    orgn_name = '_'.join(row['Species'].split())
    orgn_id = row["NCBI id"]
    command = f'python blasting.py -evalue {args.evalue} -word {args.word} -max_target_seqs {args.max_target_seqs} -db {args.db} -orgn_name {orgn_name} {"-quiet" if args.quiet else ""}'
    subprocess.check_output(command.split())
    path = f'../blast_results/{orgn_name}'
    filename = f'{path}/{orgn_id}_{"blastp" if args.db == "prot" else "tblastn"}_res.tsv'
    out_file = f'{path}/unique_{"blastp" if args.db == "prot" else "tblastn"}_res.faa'
    proteome = f'../data/{orgn_name}/ncbi_dataset/data/{orgn_id}/protein.faa'

    cut_process = subprocess.Popen(f'cut -f2 {filename}'.split(), stdout=subprocess.PIPE, text=True)
    sort_process = subprocess.Popen(['sort'], stdin=cut_process.stdout, stdout=subprocess.PIPE, text=True)
    cut_process.stdout.close()
    uniq_process = subprocess.Popen(['uniq'], stdin=sort_process.stdout, stdout=subprocess.PIPE, text=True)
    sort_process.stdout.close()

    output = uniq_process.stdout.read()
    uniq_process.stdout.close()

    summary.append([orgn_name, str(len(output.split()) + 1)])

    ids = output.split()
    with open(out_file, 'w') as out:
        with open(proteome) as file:
            is_needed = False
            for line in file:
                if line.startswith('>'):
                    if line.split()[0][1:] in ids:
                        is_needed = True
                        out.write(line)
                    else:
                        is_needed = False
                elif is_needed:
                    out.write(line)


    with open('summary.tmp', 'w') as out:
        for line in summary:
            print(*line, sep='\t', file=out)

if not args.quiet:
    for line in summary:
        print(line[0].ljust(30), line[1])