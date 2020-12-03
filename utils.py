import pickle
from indexer import Indexer
import os

def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_inverted_index():
    return None
def load_inverted_index(path):
    file = open(path + "\\inverted_index_dic.txt", "r")
    inverted_index = {}
    line = file.readline()
    while line:
        splited_line = line.split(":")
        term = splited_line[0]
        inverted_index[term] = {}
        values = splited_line[1].split(" ")
        inverted_index[term]['tf'] = values[0]
        line = file.readline()
    file.close()
    return inverted_index

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path
    else:
        return path

