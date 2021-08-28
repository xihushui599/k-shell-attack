from BasicMethods import *


class RandomAttack(BasicMethods):
    def __init__(self, G):
        self.G = nx.Graph(G)  # 保存原始图数据
        self._G = nx.Graph(G)  # 保存迭代的中间图数据变量
        self.kshell = self.k_shell(self.G)
        self._kshell = self.k_shell(self._G)

    def Delete(self, attackNumber):
        _edges, acc, number = list(self._G.edges)[:], 1.0, 0
        seeds = random.sample(_edges, attackNumber)
        for seed in seeds:
            _edges.remove(seed)
        self._kshell = self.k_shell(_edges)
        acc = self.accuracy(self.kshell, self._kshell)
        LCR = 1.0 - len(_edges) / len(self.G.edges)
        ASR = 1.0 - acc
        return [ASR, LCR, nx.Graph(_edges)]

    def Attack(self, attackNumber):
        _edges, acc, number = list(self._G.edges)[:], 1.0, 0
        for _ in range(attackNumber):
            seeds = random.sample(range(len(_edges)), 2)
            selectedEdges = [_edges[seeds[0]], _edges[seeds[1]]]
            rewiredEdges = self.constraint(_edges, selectedEdges)
            if rewiredEdges == 0:
                _ -= 0 if _ == 0 else 1
                continue
            rewiredResults = [seeds, rewiredEdges]
            _edges[rewiredResults[0][0]] = rewiredResults[1][0]
            _edges[rewiredResults[0][1]] = rewiredResults[1][1]
        self._kshell = self.k_shell(_edges)
        acc = self.accuracy(self.kshell, self._kshell)
        for edge in _edges:
            number += 1 if self.edgeExists(self.G.edges, edge) else 0
        LCR = (len(_edges) - number) / len(_edges)
        ASR = 1.0 - acc
        return [ASR, LCR, nx.Graph(_edges)]


# if __name__ == "__main__":
#     SA = pkl.load(open(cache_path + "netscience_graph_SA.pkl", "rb"))
#     RD = pkl.load(open(cache_path + "netscience_graph_RD.pkl", "rb"))
#     pdData = {"SA": [], "RD": []}
#     for graphs in SA:
#         SA_LC = []
#         for graph in graphs:
#             # SA_LC.append(len(max(nx.connected_components(graph), key=len)) / len(graph.nodes))
#             SA_LC.append(np.mean(list(BasicMethods().calEAD(graph).values())))
#         pdData["SA"].append(np.mean(SA_LC))
#         print(pdData["SA"][-1])
#     for graphs in RD:
#         RD_LC = []
#         for graph in graphs:
#             # RD_LC.append(len(max(nx.connected_components(graph), key=len)) / len(graph.nodes))
#             RD_LC.append(np.mean(list(BasicMethods().calEAD(graph).values())))
#         pdData["RD"].append(np.mean(RD_LC))
#         print(pdData["RD"][-1])
#     pdData = pd.DataFrame(pdData)
#     with pd.ExcelWriter(cache_path + "netscience_COM" + '.xlsx') as f:
#         pdData.to_excel(f, index=False, sheet_name="Sheet")


