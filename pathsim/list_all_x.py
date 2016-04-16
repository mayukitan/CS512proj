import csv
import numpy
import pandas
import argparse

import constants


def read_data(datapath):
    return pandas.read_csv(
        datapath, sep='\t', index_col=False)


def save_x(type_x, data, savedir):
    dropped = data.drop_duplicates(type_x)
    x = dropped[type_x]
    x.to_csv(savedir + '/' + type_x + '.csv', index=False)


parser = argparse.ArgumentParser()
parser.add_argument("datafile")
parser.add_argument("savedir")
args = parser.parse_args()

data = read_data(args.datafile)
# print('data:', data)


save_x(constants.LANG, data, args.savedir)
save_x(constants.ACTOR, data, args.savedir)
save_x(constants.REPO, data, args.savedir)
