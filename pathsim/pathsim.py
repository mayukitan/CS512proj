import csv
import numpy
import pandas
import time

import constants


def read_data(filename):
    return pandas.read_csv(
        constants.datapath + filename + '.txt',
        sep='\t', index_col=False)


def read_x(filename):
    return pandas.read_csv(
        constants.datapath + filename + '.csv',
        sep='\t', index_col=0, header=None)


def create_matrixRX(repo, x):
    matrixRX = pandas.DataFrame(numpy.zeros(shape=(len(repo), len(x))))
    matrixRX = matrixRX.set_index(repo.index.values)
    matrixRX.columns = x.index.values
    return matrixRX


def set_relation(matrixRX, type_x):
    data = read_data('top_actor')

    for index, row in data.iterrows():
        cur_repo = row[constants.REPO]
        cur_x = row[type_x]
        if type == constants.LANG:
            # make sure a repository gets one language only once
            matrixRX.loc[cur_repo][cur_x] = 1
        else:
            matrixRX.loc[cur_repo][cur_x] += 1


def create_matrices(actor, lang, repo):
    matrixRA = create_matrixRX(repo, actor)
    matrixRL = create_matrixRX(repo, lang)

    set_relation(matrixRA, constants.ACTOR)
    set_relation(matrixRL, constants.LANG)
    return matrixRA, matrixRL


def create_matrixARA(matrixRA):
    try:
        # load matrix from csv
        matrixARA = pandas.DataFrame.from_csv(
            constants.datapath + 'matrixARA.csv')
    except IOError:
        matrixAR = matrixRA.transpose()
        matrixARA = matrixAR.dot(matrixRA)

        # save matrix to csv
        matrixARA.to_csv(constants.datapath + 'matrixARA.csv')

    return matrixARA


def create_matrixARLRA(matrixRL, matrixRA):
    try:
        # load matrix from csv
        matrixARLRA = pandas.DataFrame.from_csv(
            constants.datapath + 'matrixARLRA.csv')
    except IOError:
        matrixAR = matrixRA.transpose()
        matrixARL = matrixAR.dot(matrixRL)
        matrixLRA = matrixARL.transpose()
        matrixARLRA = matrixARL.dot(matrixLRA)

        # save matrix to csv
        matrixARLRA.to_csv(constants.datapath + 'matrixARLRA.csv')
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


lang = read_x(constants.LANG)
actor = read_x(constants.ACTOR)
repo = read_x(constants.REPO)

matrixRA, matrixRL = create_matrices(actor, lang, repo)
# print('matrixRA:', matrixRA)
# print('matrixRL:', matrixRL)

matrixARA = create_matrixARA(matrixRA)

print('\nThe top similar actors to pombredanne using ARA are:\n')
result = top_k_similar('pombredanne', 10, matrixARA)
print('result:', result)

matrixARLRA = create_matrixARLRA(matrixRL, matrixRA)

print('\nThe top similar actors to pombredanne using ARLRA are:\n')
result = top_k_similar('pombredanne', 10, matrixARLRA)
print('result:', result)
