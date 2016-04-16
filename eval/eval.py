import argparse
import pandas
import numpy


def get_actors(filename):
    return pandas.read_csv(
        filename,
        sep='\t', index_col=0, header=None)


def create_matrixTA(test_actors, actors):
    matrixTA = pandas.DataFrame(
        numpy.zeros(shape=(len(test_actors), len(actors))))
    matrixTA = matrixTA.set_index(test_actors.index.values)
    matrixTA.columns = actors.index.values
    return matrixTA


def read_data(datafile):
    return pandas.read_csv(
        datafile, sep='\t', index_col=False)


def set_relation(matrixTA, datafile):
    data = read_data(datafile)

    for index, row in data.iterrows():
        cur_repo = row[constants.REPO]
        cur_x = row[type_x]
        if type == constants.LANG:
            # make sure a repository gets one language only once
            matrixRX.loc[cur_repo][cur_x] = 1
        else:
            matrixRX.loc[cur_repo][cur_x] += 1

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("datafile")
parser.add_argument("test_actor_csv")
parser.add_argument("all_actor_csv")
args = parser.parse_args()

print(args.datafile)

test_actors = get_actors(args.test_actor_csv)
actors = get_actors(args.all_actor_csv)

matrixTA = create_matrixTA(test_actors, actors)
print(matrixTA)
