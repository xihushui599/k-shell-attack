import numpy as np
# import os
import pandas as pd
# import math
import networkx as nx
import random
import pickle as pkl
import argparse
import matplotlib.pyplot as plt
# from tqdm import tqdm
# import xlsxwriter as xw
# import openpyxl
# from openpyxl.styles import Alignment

data_path = "./datasets/"
cache_path = "./cache/"


def get_cmd_para():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', dest='dataset', type=str, default='karate', help='select dataset')
    parser.add_argument('-e', '--episode', dest='episode', type=int, default=1000, help='attack episode')
    args = parser.parse_args()
    try:
        file = open(data_path + args.dataset + ".pkl", "rb")
    except:
        raise ValueError("Unexpected filename " + str(args.dataset) + " received.")
    return args, file


if __name__ == "__main__":
    file = open(data_path + "hybrid" + ".pkl", "rb")
    edges = pkl.load(file)
    G = nx.Graph(edges)
    x = {(a, b): c for a, b, c in list(nx.common_neighbor_centrality(G))}
    print(len(x))
    print(x)
