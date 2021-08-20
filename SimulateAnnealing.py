from BasicMethods import *


class SimulateAnnealing(BasicMethods):
    def __init__(self, G, T, Tm):
        self.G = nx.Graph(G)  # 保存原始图数据
        self._G = nx.Graph(G)  # 保存迭代的中间图数据变量
        self.kshell = self.k_shell(G)
        self._kshell = self.k_shell(G)
        self.T = T
        self.Tm = Tm

    def annealingSimulate(self, attackNumber):
        _edges, acc, number = list(self._G.edges)[:], 1.0, 0
        rewiredResults, backResults = [[0, 1], [_edges[0], _edges[1]]], []
        for _ in range(attackNumber):
            _T, iteration = self.T, 0
            while _T > self.Tm:
                iteration += 1
                for __ in range(10):
                    tempEdges = _edges[:]
                    seeds = random.sample(range(len(tempEdges)), 2)
                    selectedEdges = [tempEdges[seeds[0]], tempEdges[seeds[1]]]
                    rewiredEdges = self.constraint(tempEdges, selectedEdges)
                    if rewiredEdges == 0:
                        __ -= 0 if __ == 0 else 1
                        continue
                    tempEdges[seeds[0]], tempEdges[seeds[1]] = rewiredEdges[0], rewiredEdges[1]
                    self._kshell = self.k_shell(tempEdges)
                    _acc = self.accuracy(self.kshell, self._kshell)
                    if _acc < acc or np.random.uniform(0, 1) < np.exp((acc - _acc) * 1000 / _T):
                        acc, rewiredResults, backResults = _acc, [seeds, rewiredEdges], [selectedEdges, rewiredEdges]
                _T = _T / (iteration + 1)
            _edges[rewiredResults[0][0]] = rewiredResults[1][0]
            _edges[rewiredResults[0][1]] = rewiredResults[1][1]
        for edge in _edges:
            number += 1 if self.edgeExists(self.G.edges, edge) else 0
        LCR = (len(_edges) - number) / len(_edges)
        ASR = 1.0 - acc
        return [ASR, LCR, nx.Graph(_edges), backResults] if acc < 1.0 else False



