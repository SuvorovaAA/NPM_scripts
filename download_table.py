import argparse
import pandas as pd
from tqdm import tqdm
import subprocess

parser = argparse.ArgumentParser(
    description="""
    This script takes in a tsv file containing organism
    name and assembly ID, then launches a script that
    downloads data from NCBI database, then creates 
    blast database.
    """)

parser.add_argument('in_file', help='tsv table name')
parser.add_argument('-quiet', action='store_true', help='Hide progress bars')
parser.add_argument('-max_retries', type=int, help='Number of retries on error', default=5)

args = parser.parse_args()

df = pd.read_csv(args.in_file, sep='\t')
for index, row in tqdm(df.iterrows()):
    orgn_name = '_'.join(row['Species'].split())
    orgn_id = row['NCBI id']
    command = f'python downloading_data.py -orgn_name {orgn_name} {orgn_id} {"-quiet" if args.quiet else ""}'
    for attempt in range(args.max_retries):
        try:
            subprocess.check_output(command.split(), stderr=subprocess.STDOUT, text=True)
            break
        except subprocess.CalledProcessError as e:
            print(f"Command failed on attempt {attempt + 1} with error: {e.returncode}")
            print(f"Error output: {e.output.strip()}")
            if attempt == args.max_retries:
                print(f"Max retries reached. Command failed.")