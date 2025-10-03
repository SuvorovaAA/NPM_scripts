import json
import argparse
import os
import configparser
import subprocess

parser = argparse.ArgumentParser(
    description="""
    This script launches local BLAST tool. I plan
    to use this one to launch lots of searches.
    """)

parser.add_argument('-evalue', help='E-value threshold to use, default=1e-5', default=1e-5)
parser.add_argument('-word', help='Word size to use, >= 4, default=6', default=6)
parser.add_argument('-max_target_seqs', help='Maximal number of sequences. Not the best ones. default=500', default=500)
parser.add_argument('-db', choices=['nucl', 'prot'], help='Choose which database to use')
parser.add_argument('-quiet', action='store_true', help='Hide progress bars')
parser.add_argument('-orgn_name', help='Organism name')

args = parser.parse_args()

with open("name_2_id.json", "r") as file:
    loaded_dict = json.load(file)

assembly_id = loaded_dict[args.orgn_name]

config = configparser.ConfigParser()
config.read('config.ini')
query_path = config.get('paths', 'query')

if not os.path.isdir('../blast_results'):
    subprocess.check_output(['mkdir', '../blast_results'])

path = f'../blast_results/{args.orgn_name}'
if not os.path.isdir(path):
    subprocess.check_output(['mkdir', path])

if args.db == 'nucl':
    db_path = f'../blast_dbs/{args.orgn_name}/genomic_db/{assembly_id}_genomic'
    out_path = f'../blast_results/{args.orgn_name}/{assembly_id}_genomic_blast.tsv'
else:
    db_path = f'../blast_dbs/{args.orgn_name}/proteome_db/{assembly_id}_proteome'
    out_path = f'../blast_results/{args.orgn_name}/{assembly_id}_proteome_blast.tsv'

if args.db == 'nucl':
    filename = f'{path}/{assembly_id}_tblastn_res.tsv'
    command = f'tblastn -query {query_path} -db {db_path} -out {filename} -outfmt 6 -evalue {args.evalue} -word_size {args.word}'
    subprocess.check_output(command.split())
    n_res = int(subprocess.check_output(['wc', '-l', filename]).split()[0])
    if n_res == 0:
        print('No results found')
    elif n_res == args.max_target_seqs:
        print('Reached maximum number of target sequences')
    else:
        print(f'Found {n_res} results')

else:
    filename = f'{path}/{assembly_id}_blastp_res.tsv'
    command = f'blastp -query {query_path} -db {db_path} -out {filename} -outfmt 6 -evalue {args.evalue} -word_size {args.word}'
    subprocess.check_output(command.split())
    n_res = int(subprocess.check_output(['wc', '-l', filename]).split()[0])
    if n_res == 0:
        print('No results found')
    elif n_res == args.max_target_seqs:
        print('Reached maximum number of target sequences')
    else:
        print(f'Found {n_res} results')