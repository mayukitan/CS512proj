import csv
import numpy
import pandas

import constants


def read_data(filename):
    return pandas.read_csv(
        constants.datapath + filename + '.txt',
        sep='\t', index_col=False)


def save_x(type_x, data):
    dropped = data.drop_duplicates(type_x)
    x = dropped[type_x]
    x.to_csv(constants.datapath + type_x + '.csv', index=False)

data = read_data('top_actor')
# print('data:', data)

save_x(constants.LANG, data)
save_x(constants.ACTOR, data)
save_x(constants.REPO, data)
