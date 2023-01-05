import re
import json
import code
import argparse
from os import listdir, getcwd, mkdir
from shutil import copyfile
from os.path import isfile, join, exists


def init_parser():
    parser = argparse.ArgumentParser(description="Create genesis file which allocates Ether for existing accounts")
    parser.add_argument("--genesis", type=str, default="genesis.json", help="Genesis file to update with new Accounts")
    parser.add_argument("keystore", type=str, help="Path to keystore containing accounts")

    return parser

def copy_keystore(path, files):
    dirname = join(getcwd(), 'keystore')
    if not exists(dirname):
        mkdir(dirname)
    for file in files:
        copyfile(join(path, file), join(dirname, file))

def read_keystore_addresses(keystore_path):
    addresses = []
    files = [f for f in listdir(keystore_path) if isfile(join(keystore_path, f)) and re.match('^UTC.*', f)]
    for file in files:
        with open(join(keystore_path, file)) as f:
            data = json.load(f)
            addresses.append(data['address'])
    # copy_keystore(keystore_path, files)
    return addresses


def read_genesis_file(genesis_file):
    with open(genesis_file) as file:
        genesis_dict = json.load(file)
    return genesis_dict


def fill_genesis_file(genesis, addresses):
    for address in addresses:
        genesis.get('alloc')[address] = {'balance': '100000000000000000000000000000000000'}
    with open("_genesis.json", "w") as f:
        f.write(json.dumps(genesis))

def main():
    parser = init_parser()
    args = parser.parse_args()
    if hasattr(args, 'genesis') and hasattr(args, 'keystore'):
        genesis = read_genesis_file(args.genesis)
        addresses = read_keystore_addresses(args.keystore)
        fill_genesis_file(genesis, addresses)

if __name__ == '__main__':
    main()
            
