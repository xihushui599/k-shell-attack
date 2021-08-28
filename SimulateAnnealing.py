from BasicMethods import *


class SimulateAnnealing(BasicMethods):
    def __init__(self, G, T, Tm):
        self.G = nx.Graph(G)  # 保存原始图数据
        self._G = nx.Graph(G)  # 保存迭代的中间图数据变量
        self.kshell = self.k_shell(G)
        self._kshell = self.k_shell(G)
        self.T = T
        self.Tm = Tm

    def Attack(self, attackNumber):
        _edges, acc, number = list(self._G.edges)[:], 1.0, 0
        rewiredResults = [[0, 1], [_edges[0], _edges[1]]]
        # Attack iteration
        for _ in range(attackNumber):
            _T, iteration = self.T, 0
            # Annealing iteration
            while _T > self.Tm:
                iteration += 1
                _T = _T / iteration
                for __ in range(10):
                    # Random select candidate edges and judge if they satisfy our constraint or not
                    tempEdges = _edges[:]
                    seeds = random.sample(range(len(tempEdges)), 2)
                    selectedEdges = [tempEdges[seeds[0]], tempEdges[seeds[1]]]
                    rewiredEdges = self.constraint(tempEdges, selectedEdges)
                    if rewiredEdges == 0:
                        __ -= 0 if __ == 0 else 1
                        continue
                    # Attack graph and calculate attack accuracy
                    tempEdges[seeds[0]], tempEdges[seeds[1]] = rewiredEdges[0], rewiredEdges[1]
                    self._kshell = self.k_shell(tempEdges)
                    _acc = self.accuracy(self.kshell, self._kshell)
                    # Judge whether this attack is accepted or not
                    if _acc < acc or np.random.uniform(0, 1) < np.exp((acc - _acc) * 1000 / _T):
                        acc, rewiredResults = _acc, [seeds, rewiredEdges]
                # Update temperature
            _edges[rewiredResults[0][0]] = rewiredResults[1][0]
            _edges[rewiredResults[0][1]] = rewiredResults[1][1]
        for edge in _edges:
            number += 1 if self.edgeExists(self.G.edges, edge) else 0
        LCR = (len(_edges) - number) / len(_edges)
        ASR = 1.0 - acc
        return [ASR, LCR, nx.Graph(_edges)]


# if __name__ == "__main__":
#     file = open(data_path + "netscience" + ".pkl", "rb")
#     edges = pkl.load(file)
#     G = nx.Graph(edges)
#     print(len(G.nodes), len(G.edges))
#     round = 0
#     scores = np.zeros(3)
#     for t in range(100, 1000, 20):
#         for tm in range(1, 20, 2):
#             ticks = time.time()
#             SA = SimulateAnnealing(G, t, tm)
#             result, score_new = [], 0
#             for _ in range(10):
#                 result = SA.Attack(10)
#                 score_new += result[0] / result[1]
#             print(time.time() - ticks, t, tm)
#             if score_new > scores[0]:
#                 scores[0] = score_new
#                 scores[1] = t
#                 scores[2] = tm
#                 print(result[0], result[1])
#                 print(str(round) + ".Upgrade data to:", scores)
#             else:
#                 print(result[0], result[1])
#                 print(str(round) + ".Not upgrade from:", scores)
#     print(scores)
