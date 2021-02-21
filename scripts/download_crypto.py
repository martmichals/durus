"""
This script downloads data for crypto, using the metdata.json folders in each 
directory to generate urls, as well as run the necessary data formatting scripts after download
"""

import requests
import json, os
from pathlib import Path

def launch_exchange_download(base_url, exchange_dir):
    """Downloads and saves data for an exchange

    Args:
        base_url (string): the base of the url to download from
        exchange_dir (string): directory for the exchange data, must contain metadata.json

    Raises:
        Exception: No metadata
    """
    exchange_meta = exchange_dir/'metadata.json'
    if exchange_meta.exists():

        # Open the exchange metadata
        with open(exchange_meta) as exchange_meta_file:
            exchange_meta_json = json.load(exchange_meta_file)

            # Iterate over currencies, download relevant files
            for curr in exchange_meta_json['links']:

                # Clear existing data
                curr_folder = exchange_dir/curr
                if curr_folder.exists():
                    for file in os.listdir(curr_folder):
                        os.remove(curr_folder/file)
                else:
                    os.mkdir(curr_folder)

                # Download and write data to files in currency directory
                for link in exchange_meta_json['links'][curr]:
                    download_link = base_url+link
                    req = requests.get(download_link)
                    if req.status_code != 200:
                        print('{} [\033[91mX\033[0m]'.format(link.split('/')[-1]))
                    else:
                        with open(curr_folder/download_link.split('/')[-1], 'wb') as f:
                            f.write(req.content)
                        print('{} [\033[92m✓\033[0m]'.format(link.split('/')[-1]))
                
                # TODO : Run cleanup scripts here
                # TODO : Look into USDT, is it diff than USD
    else:
        raise Exception('{} does not have metadata to facilitate downloads'.format(exchange_dir))

# Iterate over exchanges in overall cryptodata folder
crypto_dir = Path('../data/cryptodata')
crypto_meta = crypto_dir/'metadata.json'
with open(crypto_meta) as crypto_meta_file:
    crypto_meta_json = json.load(crypto_meta_file)

    # Iterate over all exchanges, launching download function
    for exchange in crypto_meta_json['exchanges']:
        if (exchange_dir:=crypto_dir/exchange).is_dir():
            launch_exchange_download(crypto_meta_json['url'], exchange_dir)
        else:
            raise Exception('{} does not have a folder'.format(exchange))
