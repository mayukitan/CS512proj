import csv
import numpy
import pandas
import time
import argparse
import constants


def read_data(datafile):
    return pandas.read_csv(
        datafile, sep='\t', index_col=False)


def read_x(filename, savedir):
    return pandas.read_csv(
        savedir + '/' + filename + '.csv',
        sep='\t', index_col=0, header=None)


def create_matrixRX(repo, x):
    matrixRX = pandas.DataFrame(numpy.zeros(shape=(len(repo), len(x))))
    matrixRX = matrixRX.set_index(repo.index.values)
    matrixRX.columns = x.index.values
    return matrixRX


def set_relation(matrixRX, type_x, datafile):
    data = read_data(datafile)

    for index, row in data.iterrows():
        cur_repo = row[constants.REPO]
        cur_x = row[type_x]
        if type == constants.LANG:
            # make sure a repository gets one language only once
            matrixRX.loc[cur_repo][cur_x] = 1
        else:
            matrixRX.loc[cur_repo][cur_x] += 1


def create_matrices(actor, lang, repo, datafile):
    matrixRA = create_matrixRX(repo, actor)
    matrixRL = create_matrixRX(repo, lang)

    set_relation(matrixRA, constants.ACTOR, datafile)
    set_relation(matrixRL, constants.LANG, datafile)
    return matrixRA, matrixRL


def create_matrixARA(matrixRA, savedir):
    try:
        # load matrix from csv
        matrixARA = pandas.DataFrame.from_csv(
            savedir + '/' + 'matrixARA.csv')
    except IOError:
        matrixAR = matrixRA.transpose()
        matrixARA = matrixAR.dot(matrixRA)

        # save matrix to csv
        matrixARA.to_csv(savedir + '/' + 'matrixARA.csv')

    return matrixARA


def create_matrixARLRA(matrixRL, matrixRA, savedir):
    try:
        # load matrix from csv
        matrixARLRA = pandas.DataFrame.from_csv(
            savedir + '/' + 'matrixARLRA.csv')
    except IOError:
        matrixAR = matrixRA.transpose()
        matrixARL = matrixAR.dot(matrixRL)
        matrixLRA = matrixARL.transpose()
        matrixARLRA = matrixARL.dot(matrixLRA)

        # save matrix to csv
        matrixARLRA.to_csv(savedir + '/' + 'matrixARLRA.csv')
    return matrixARLRA


def top_k_similar(actor_name, k, matrix):
    similar = matrix.loc[actor_name].copy()
    for other_actor in similar.index:
        similar[other_actor] = (
            2 * matrix.loc[actor_name][other_actor] / (
                matrix.loc[actor_name][actor_name] +
                matrix.loc[other_actor][other_actor]))

    similar.sort_values(inplace=True, ascending=False)

    return similar[0:k]


parser = argparse.ArgumentParser()
parser.add_argument("datafile")
parser.add_argument("savedir")
args = parser.parse_args()

print(args.datafile)
print(args.savedir)

lang = read_x(constants.LANG, args.savedir)
actor = read_x(constants.ACTOR, args.savedir)
repo = read_x(constants.REPO, args.savedir)

matrixRA, matrixRL = create_matrices(actor, lang, repo, args.datafile)
# print('matrixRA:', matrixRA)
# print('matrixRL:', matrixRL)

matrixARA = create_matrixARA(matrixRA, args.savedir)

print('\nThe top similar actors to pombredanne using ARA are:\n')
result = top_k_similar('pombredanne', 10, matrixARA)
print('result:', result)

matrixARLRA = create_matrixARLRA(matrixRL, matrixRA, args.savedir)

print('\nThe top similar actors to pombredanne using ARLRA are:\n')
result = top_k_similar('pombredanne', 10, matrixARLRA)
print('result:', result)
