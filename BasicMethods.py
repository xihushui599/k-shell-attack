from __init__ import *


class BasicMethods:
    # 该函数为k-shell分解算法
    def k_shell(self, edges):
        G = nx.Graph(edges)  # 用边集构建图
        kshell, k = dict(G.degree), 1
        while True:
            while min([x[1] for x in list(G.degree)]) <= k:
                for node in list(G.degree):
                    if node[1] <= k:
                        kshell[node[0]] = k
                        G.remove_node(node[0])
                if not G:
                    return kshell
            k = min([x[1] for x in list(G.degree)])

    # k-shell的分解精度
    def accuracy(self, k, k_):
        acc_absolute = 0
        for key in sorted(k_.keys()):
            if k_.get(key, []) == k.get(key, []):
                acc_absolute += 1
        acc_attack = acc_absolute / len(k_)
        return acc_attack

    def get_neigbors(self, G, node, depth=1):
        output = {}
        layers = dict(nx.bfs_successors(G, source=node, depth_limit=depth))
        nodes = [node]
        for i in range(1, depth + 1):
            output[i] = []
            for x in nodes:
                output[i].extend(layers.get(x, []))
            nodes = output[i]
        return output[depth]

    def edgeExists(self, edges, edge):
        if edge in edges or edge[::-1] in edges:
            return True
        else:
            return False

    def constraint(self, tempEdges, selectedEdges):
        nodes = [selectedEdges[0][0], selectedEdges[0][1], selectedEdges[1][0], selectedEdges[1][1]]
        if len(set(nodes)) < 4:
            return 0
        rewired_Direct = [(nodes[0], nodes[2]), (nodes[1], nodes[3])]
        rewired_Cross = [(nodes[0], nodes[3]), (nodes[1], nodes[2])]
        enableDirect = not (self.edgeExists(tempEdges, rewired_Direct[0]) or
                            self.edgeExists(tempEdges, rewired_Direct[1]))
        enableCross = not (self.edgeExists(tempEdges, rewired_Cross[0]) or
                           self.edgeExists(tempEdges, rewired_Cross[1]))
        if enableDirect ^ enableCross:
            rewiredEdges = rewired_Direct if enableDirect else rewired_Cross
        elif enableDirect and enableCross:
            rewiredEdges = rewired_Direct if random.random() < 0.5 else rewired_Cross
        else:
            return 0
        return rewiredEdges

    def calEAD(self, G, ebunch=None):
        """计算网络中每个节点的一阶邻居余平均度（Excess average degree）"""
        def applyFunction(func, ebunch):
            bunch = ebunch if ebunch else G.nodes
            return ((n, func(n)) for n in bunch)
        def predict(n):
            return np.mean([G.degree(x) for x in nx.neighbors(G, n)])
        return dict(applyFunction(predict, ebunch))

    def applyFunction(self, G, func):
        ebunch = nx.non_edges(G)
        return ((u, v, func(u, v)) for u, v in ebunch)

    def calHPI(self, G):
        def predict(u, v):
            return len(list(nx.common_neighbors(G, u, v))) / min(G.degree(u), G.degree(v))

        return {(a, b): c for a, b, c in list(self.applyFunction(G, predict))}

    def calHDI(self, G):
        def predict(u, v):
            return len(list(nx.common_neighbors(G, u, v))) / max(G.degree(u), G.degree(v))

        return {(a, b): c for a, b, c in list(self.applyFunction(G, predict))}

    def calRA(self, G):
        return {(a, b): c for a, b, c in list(nx.resource_allocation_index(G))}

    def calJaccard(self, G):
        return {(a, b): c for a, b, c in list(nx.jaccard_coefficient(G))}

    def calAA(self, G):
        return {(a, b): c for a, b, c in list(nx.adamic_adar_index(G))}

    def calPA(self, G):
        return {(a, b): c for a, b, c in list(nx.preferential_attachment(G))}

    def calCCPA(self, G):
        return {(a, b): c for a, b, c in list(nx.common_neighbor_centrality(G))}

    def calLinkMetrics(self, G):
        return [
            self.calRA(G), self.calJaccard(G), self.calAA(G), self.calPA(G), self.calCCPA(G),
            self.calHPI(G), self.calHDI(G)
        ]

    def calNodeMetrics(self, G):
        return [
            self.k_shell(G), self.calEAD(G), nx.closeness_centrality(G), nx.betweenness_centrality(G),
            dict(nx.all_pairs_shortest_path_length(G)), nx.diameter(G), nx.clustering(G),
        ]


# if __name__ == "__main__":
#     file = open(data_path + "hybrid" + ".pkl", "rb")
#     edges = pkl.load(file)
#     G = nx.Graph(edges)
#     kshell = BasicMethods().k_shell(G)
#     s = dict(sorted(kshell.items(), key=lambda x: x[1], reverse=True))
#     print(s.values())
