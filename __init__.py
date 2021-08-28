import numpy as np
import pandas as pd
import networkx as nx
import random
import pickle as pkl
import argparse
import matplotlib.pyplot as plt
import time


data_path = "./datasets/"
cache_path = "./cache/"


def get_cmd_para():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', dest='dataset', type=str, default='karate', help='select dataset')
    parser.add_argument('-r', '--round', dest='round', type=int, default=1000, help='attack round')
    args = parser.parse_args()
    try:
        file = open(data_path + args.dataset + ".pkl", "rb")
    except:
        raise ValueError("Unexpected filename " + str(args.dataset) + " received.")
    return args, file


# if __name__ == "__main__":
#     edges = []
#     with open(data_path + "CA.txt", "r") as f:  # 打开文件
#         lines = f.readlines()  # 读取文件
#         for line in lines:
#             data = line.split("\t")
#             data[1] = data[1].split("\n")
#             edges.append((int(data[0]), int(data[1][0])))
#     print(edges)
#     file = open(data_path + 'CA' + ".pkl", "wb")
#     pkl.dump(edges, file)


