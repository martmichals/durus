"""
Script that combines .csv files for the same currency, in the same exchange into one .csv file
"""
import argparse, os
import pandas as pd
from pathlib import Path

def main(args):
    # Iterate over exchanges
    exchange_folder = Path('../../data/cryptodata/{}'.format(args.exchange.lower()))
    if exchange_folder.is_dir():
        for elem in os.listdir(exchange_folder):

            # Iterate over currencies, merging the csv files
            if (curr_dir:=exchange_folder/elem).is_dir():
                # TODO : This code is not working
                paths = [curr_dir/file for file in os.listdir(curr_dir)]
                data_frame_all = (pd.read_csv(f, sep=',', skiprows=[0], low_memory=False) for f in paths)
                data_frame_merged = pd.concat(data_frame_all, ignore_index=True)
                data_frame_merged.to_csv(curr_dir/'{}.csv'.format('merged'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to combine files representing multiple years into one file')

    parser.add_argument('--ex', dest='exchange', type=str, help='the exchange to combine files for in cryptodata')
    args = parser.parse_args()
    main(args)