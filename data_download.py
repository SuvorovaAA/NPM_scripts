import argparse
import os
import subprocess

parser = argparse.ArgumentParser(
    description="""
    This script takes in a given genome assembly ID, 
    downloads data from NCBI database, then creates 
    blast database.
    """)

parser.add_argument('id')                # assembly ID
parser.add_argument('-common_name')      # common name that will be used
parser.add_argument('-quiet', action='store_true')

args = parser.parse_args()

if not os.path.isdir('../data'):
    subprocess.check_output(['mkdir', '../data'])

path = f'../data/{args.common_name}'
if not os.path.isdir(path):
    subprocess.check_output(['mkdir', path])

if not args.quiet:
    print('Downloading data from NCBI...')
command = f'datasets download genome accession {args.id} --filename {path}/{args.common_name}.zip --include cds,gbff,genome,gff3,gtf,protein,rna,seq-report'
if args.quiet:
    command += ' --no-progressbar'
subprocess.check_output(command.split())

if not args.quiet:
    print('Unzipping...')
subprocess.check_output(['unzip', f'{path}/{args.common_name}.zip', '-d', path])

# Creating blast database
if not os.path.isdir('../blast_dbs'):
    subprocess.check_output(['mkdir', '../blast_dbs'])

db_path = path = f'../blast_dbs/{args.common_name}'
data_path = f'../data/{args.common_name}/ncbi_dataset/data/{args.id}'

if not args.quiet:
    print('Creating genomic database...')
title = f'"{args.common_name}_genomic_database_{args.id}"'

filename = [name for name in os.listdir(data_path) if name.startswith(args.id)][0]

command = f'makeblastdb -dbtype nucl -in {data_path}/{filename} -title {title} -out {db_path}/genomic_db/{args.id}_genomic'
subprocess.check_output(command.split())

if not args.quiet:
    print('Creating proteome database...')
title = f'"{args.common_name}_proteome_database_{args.id}"'
command = f'makeblastdb -dbtype prot -in {data_path}/protein.faa -title {title} -out {db_path}/proteome_db/{args.id}_proteome'
output = subprocess.check_output(command.split())

if not args.quiet:
    print('All done!')