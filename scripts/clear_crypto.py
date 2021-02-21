"""
This script deletes the data for crypto, using the the general metadata.json to
find folders to clear
"""

import shutil, json, os
from pathlib import Path

# Iterate over exchanges in overall cryptodata folder
crypto_dir = Path('../data/cryptodata')
crypto_meta = crypto_dir/'metadata.json'
with open(crypto_meta) as crypto_meta_file:
    crypto_meta_json = json.load(crypto_meta_file)

    # Iterate over all exchanges, deleting all currencies present
    for exchange in crypto_meta_json['exchanges']:
        if (exchange_dir:=crypto_dir/exchange).is_dir():
            for elem in os.listdir(exchange_dir):
                if (exchange_dir/elem).is_dir():
                    shutil.rmtree(exchange_dir/elem)
        else:
            raise Exception('{} does not have a folder'.format(exchange))