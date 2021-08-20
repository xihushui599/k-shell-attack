from BasicMethods import *


class HeuristicAttack(BasicMethods):
    def __init__(self, G):
        self.G = nx.Graph(G)  # 保存原始图数据
        self._G = nx.Graph(G)  # 保存迭代的中间图数据变量
        self.kshell = self.k_shell(self.G)
        self._kshell = self.k_shell(self._G)

    def findFurthestNodes(self, center):
        def judge(standrad):
            nodes = self.get_neigbors(self._G, center, standrad)
            return [True if nodes else False, nodes]

        standrad = int(nx.diameter(self._G) / 2)
        flag, record = judge(standrad)
        area = range(standrad, nx.diameter(self._G) + 2) if flag else range(standrad, 0, -1)
        for d in area:
            current, nodes = judge(d)
            if current ^ flag:
                return record
            record = nodes





    def selectLinks(self):
        def findMaxBatch(metricDict):
            sortedDict = dict(sorted(metricDict.items(), key=lambda x: x[1], reverse=True))
            maxValue, filter = list(sortedDict.values())[0], []
            for key in sortedDict.keys():
                if sortedDict[key] >= maxValue:
                    filter.append(key)
                else:
                    return filter
        self._kshell = self.k_shell(self._G)
        filterNodes = findMaxBatch(self._kshell)
        eadDict = findMaxBatch(self.calEAD(self._G, filterNodes))






    def heuristicAttack(self, attackNumber):
        _edges, acc, number = list(self._G.edges)[:], 1.0, 0
        rewiredResults, backResults = [[0, 1], [_edges[0], _edges[1]]], []
        for _ in range(attackNumber):
            tempEdges = _edges[:]
            seeds = random.sample(range(len(tempEdges)), 2)
            selectedEdges = [tempEdges[seeds[0]], tempEdges[seeds[1]]]
            rewiredEdges = self.constraint(tempEdges, selectedEdges)
            if rewiredEdges == 0:
                continue
            tempEdges[seeds[0]], tempEdges[seeds[1]] = rewiredEdges[0], rewiredEdges[1]
            self._kshell = self.k_shell(tempEdges)
            _acc = self.accuracy(self.kshell, self._kshell)
            acc, rewiredResults, backResults = _acc, [seeds, rewiredEdges], [selectedEdges, rewiredEdges]
        _edges[rewiredResults[0][0]] = rewiredResults[1][0]
        _edges[rewiredResults[0][1]] = rewiredResults[1][1]
        for edge in _edges:
            number += 1 if self.edgeExists(self.G.edges, edge) else 0
        LCR = (len(_edges) - number) / len(_edges)
        ASR = 1.0 - acc
        return [ASR, LCR, nx.Graph(_edges), backResults] if acc < 1.0 else False


if __name__ == "__main__":
    edges = pkl.load(open(data_path + "facebook" + ".pkl", "rb"))
    G = nx.Graph(edges)
    HA = HeuristicAttack(G)
    x = HA.findFurthestNodes(4)
    print(x)
