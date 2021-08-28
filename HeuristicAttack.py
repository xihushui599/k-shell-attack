from BasicMethods import *


class HeuristicAttack(BasicMethods):
    def __init__(self, G):
        self.G = nx.Graph(G)  # 保存原始图数据
        self._G = nx.Graph(G)  # 保存迭代的中间图数据变量
        self.kshell = self.k_shell(self.G)
        self._kshell = self.k_shell(self._G)

    def selectLinks(self, edges):
        index = list(self._kshell.keys())
        seeds = random.sample(index, 2)
        while abs(self._kshell[seeds[0]] - self._kshell[seeds[1]]) < 1:
            seeds = random.sample(index, 2)
        neibors = [self.get_neigbors(nx.Graph(edges), seeds[0]), self.get_neigbors(nx.Graph(edges), seeds[1])]
        neibor = [random.sample(neibors[0], 1)[0], random.sample(neibors[1], 1)[0]]
        selectedEdges = [(seeds[0], neibor[0]), (seeds[1], neibor[1])]
        return selectedEdges

    def Attack(self, attackNumber):
        _edges, acc, number = list(self._G.edges)[:], 1.0, 0
        for _ in range(attackNumber):
            selectedEdges = self.selectLinks(_edges)
            rewiredEdges = self.constraint(_edges, selectedEdges)
            if rewiredEdges == 0:
                _ -= 0 if _ == 0 else 1
                continue
            for edge in selectedEdges:
                try:
                    _edges.remove(edge)
                except:
                    _edges.remove(edge[::-1])
            _edges.extend(rewiredEdges)
        self._kshell = self.k_shell(_edges)
        acc = self.accuracy(self.kshell, self._kshell)
        for edge in _edges:
            number += 1 if self.edgeExists(self.G.edges, edge) else 0
        LCR = (len(_edges) - number) / len(_edges)
        ASR = 1.0 - acc
        return [ASR, LCR, nx.Graph(_edges)]


if __name__ == "__main__":
    edges = pkl.load(open(data_path + "karate" + ".pkl", "rb"))
    G = nx.Graph(edges)
    HA = HeuristicAttack(G)
    result = HA.Attack(10)
    print(result)
