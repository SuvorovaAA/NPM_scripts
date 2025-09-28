import argparse
import os
import configparser

parser = argparse.ArgumentParser(
    description="""
    This script creates a configuration file. You may
    specify path to query files not to specify them 
    every time. This might be a dumb decision of mine, 
    but that's the only one I came up with so far.
    """)

parser.add_argument('-query_path', help="Path to the query file")

args = parser.parse_args()

if not os.path.exists(args.query_path):
    raise FileNotFoundError('Query file not found')


config = configparser.ConfigParser()
config['paths'] = {'query': args.query_path}
# Write the configuration to a file
with open('config.ini', 'w') as configfile:
    config.write(configfile)