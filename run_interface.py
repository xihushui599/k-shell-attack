from SimulateAnnealing import *
from HeuristicAttack import *
from RandomAttack import *


def attackProcess(obj, attack_number=100):
    index_names = ['ASR', 'LCR']
    pdData = dict([(k, []) for k in index_names])
    ASRList, LCRList, GraphList = [], [], []
    gap = int(np.ceil(len(obj.G.edges) / 50 / 2))
    for n in range(1, attack_number + 1, gap):
        print('No.', n, ' round begin...')
        ticks = time.time()
        ASR, LCR, graph, max = [], [], [], 0
        for _ in range(10):
            result = obj.Attack(n)
            if result[0] > 0:
                ASR.append(result[0])
                LCR.append(result[1])
                graph.append(result[2])
        print(time.time() - ticks)
        print(np.mean(ASR), np.mean(LCR))
        ASRList.append(np.mean(ASR))
        LCRList.append(np.mean(LCR))
        GraphList.append(graph)
    pdData['ASR'] = ASRList
    pdData['LCR'] = LCRList
    return pd.DataFrame(pdData), GraphList


if __name__ == "__main__":
    args, file = get_cmd_para()
    tem_cache = {
        "karate": [850, 1],
        "dolphin": [760, 1],
        "thrones": [160, 1],
        "facebook": [150, 1],
        "USAir": [420, 9],
        "netscience": [420, 1],
    }
    T, Tmin = tem_cache.get(args.dataset, [200, 1])[0], tem_cache.get(args.dataset, [200, 1])[1]
    edges = pkl.load(file)
    SA = SimulateAnnealing(edges, T, Tmin)
    HA = HeuristicAttack(edges)
    RA = RandomAttack(edges)
    print('Current Dataset：', args.dataset)
    print("Nodes, Edges: ", len(SA.G.nodes), ", ", len(SA.G.edges))
    print('Defined attack rounds：', args.round)
    print('Initial temperature and min temperature：', T, Tmin)

    pdData_SA, Graph_SA = attackProcess(SA, args.round)
    with pd.ExcelWriter(cache_path + str(args.dataset) + "_SA" + '.xlsx') as f:
        pdData_SA.to_excel(f, index=False, sheet_name="Sheet")
        print('save SA data successed')

    pdData_HA, Graph_HA = attackProcess(HA, args.round)
    with pd.ExcelWriter(cache_path + str(args.dataset) + "_HA" + '.xlsx') as f:
        pdData_HA.to_excel(f, index=False, sheet_name="Sheet")
        print('save HA data successed')

    pdData_RA, Graph_RA = attackProcess(RA, args.round)
    with pd.ExcelWriter(cache_path + str(args.dataset) + "_RA" + '.xlsx') as f:
        pdData_RA.to_excel(f, index=False, sheet_name="Sheet")
        print('save RA data successed')

    file1 = open(cache_path + str(args.dataset) + "_graph_SA" + ".pkl", "wb")
    pkl.dump(Graph_SA, file1)
    file2 = open(cache_path + str(args.dataset) + "_graph_HA" + ".pkl", "wb")
    pkl.dump(Graph_HA, file2)
    file3 = open(cache_path + str(args.dataset) + "_graph_RA" + ".pkl", "wb")
    pkl.dump(Graph_RA, file3)

