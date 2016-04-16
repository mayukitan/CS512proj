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
