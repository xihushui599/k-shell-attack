from SimulateAnnealing import *


def regularLinks(links):
    for i in range(len(links)):
        if links[i][0] > links[i][1]:
            links[i] = (links[i][1], links[i][0])


def getNodes(dict, links):
    return [dict[links[0][0]], dict[links[0][1]], dict[links[1][0]], dict[links[1][1]]]


def getLinks(dict, links):
    return [dict.get(links[0], -1), dict.get(links[1], -1)]


def attack(SA):
    max, results = 0, []
    for _ in range(10):
        _results = SA.annealingSimulate(1)
        if _results == False:
            continue
        elif _results[0] > max:
            results, max = _results, _results[0]
    return results


def SAProcess(SA, attack_number=100):
    sheet_names = ['ASR', 'LCR', 'kshell', '余平均度', '聚类系数', '接近中心性', '介数中心性', '最短距离',
                   '资源分配指数', 'Jaccard', 'AA', 'PA', 'CCPA', 'HPI', 'HDI']
    pdData = dict([(k, []) for k in sheet_names])
    cacheGraph = []
    for n in range(attack_number):
        print('当前第', n + 1, '轮')
        """获取攻击前的节点指标"""
        [k, ead, cc, bc, distance, diameter, cluster] = SA.calNodeMetrics(SA._G)
        """获取攻击前的链路指标"""
        [ra, ja, aa, pa, ccpa, hpi, hdi] = SA.calLinkMetrics(SA._G)
        """对网络进行攻击"""
        [ASR, LCR, SA._G, links] = attack(SA)
        """获取攻击后的节点指标"""
        [_k, _ead, _cc, _bc, _distance, _diameter, _cluster] = SA.calNodeMetrics(SA._G)
        """获取攻击后的链路指标"""
        [_ra, _ja, _aa, _pa, _ccpa, _hpi, _hdi] = SA.calLinkMetrics(SA._G)

        cacheGraph.append([ASR, LCR, SA._G, links])
        pdData['ASR'].append(ASR)
        pdData['LCR'].append(LCR)
        pdData['kshell'].append(np.round([getNodes(k, links[0]), getNodes(k, links[1])], 1))
        pdData['余平均度'].append(np.round([getNodes(ead, links[0]), getNodes(ead, links[1])], 1))
        pdData['接近中心性'].append(np.round([getNodes(cc, links[0]), getNodes(_cc, links[1])], 1))
        pdData['介数中心性'].append(np.round([getNodes(bc, links[0]), getNodes(bc, links[1])], 1))
        pdData['最短距离'].append(np.round([distance[links[1][0][0]][links[1][0][1]],
                                           distance[links[1][1][0]][links[1][1][1]], diameter], 1))
        pdData['聚类系数'].append(np.round([getNodes(cluster, links[0]), getNodes(cluster, links[1])], 1))
        regularLinks(links[0])
        regularLinks(links[1])
        pdData['资源分配指数'].append(np.round([getLinks(ra, links[1]), getLinks(_ra, links[0])], 1))
        pdData['Jaccard'].append(np.round([getLinks(ja, links[1]), getLinks(_ja, links[0])], 1))
        pdData['AA'].append(np.round([getLinks(aa, links[1]), getLinks(_aa, links[0])], 1))
        pdData['PA'].append(np.round([getLinks(pa, links[1]), getLinks(_pa, links[0])], 1))
        pdData['CCPA'].append(np.round([getLinks(ccpa, links[1]), getLinks(_ccpa, links[0])], 1))
        pdData['HPI'].append(np.round([getLinks(hpi, links[1]), getLinks(_hpi, links[0])], 1))
        pdData['HDI'].append(np.round([getLinks(hdi, links[1]), getLinks(_hdi, links[0])], 1))
        print(links)
        if LCR > 0.3:
            break
    return pd.DataFrame(pdData), cacheGraph


if __name__ == "__main__":
    args, file = get_cmd_para()
    tem_cache = {
        "hybrid": [210, 1],
        "karate": [850, 1],
        "dolphin": [760, 1],
        "tortoise": [200, 1],
        "thrones": [160, 1],
        "facebook": [150, 1],
    }
    T, Tmin = tem_cache.get(args.dataset, [210, 1])[0], tem_cache.get(args.dataset, [210, 1])[1]
    SA = SimulateAnnealing(pkl.load(file), T, Tmin)
    print('当前数据集为：', args.dataset)
    print("节点数:连边数为 ", len(SA.G.nodes), ":", len(SA.G.edges))
    print('设定的攻击轮次为：', args.episode)
    print('温度设置为：', T, Tmin)

    pdData, cacheGraph = SAProcess(SA, args.episode)

    with pd.ExcelWriter(cache_path + str(args.dataset) + '.xlsx') as f:
        pdData.to_excel(f, index=False, sheet_name="单列数据")
        sheet = f.sheets["单列数据"]
        sheet.set_column("A:Z", 25)
        print('save data successed')
    file = open(cache_path + str(args.dataset) + "_graph.pkl", "wb")
    pkl.dump(cacheGraph, file)

    # def formulateTable():
    #     wb = openpyxl.Workbook()
    #     sheet = wb.active
    #     sheet.merge_cells("A1:A2")
    #     sheet.merge_cells("B1:B2")
    #     cell = sheet.cell(row=1, column=1)
    #     cell.value = "ASR"
    #     cell.alignment = Alignment(horizontal='center', vertical='center')
    #     cell = sheet.cell(row=1, column=2)
    #     cell.value = "LCR"
    #     cell.alignment = Alignment(horizontal='center', vertical='center')
    #     index_names = ['ASR', 'LCR', '平均余平均度', '接近中心性', '介数中心性', '度同配性', 'kshell-余度', 'kshell-接近中心性', 'kshell-介数中心性']
    #     for i in range(len(index_names) - 2):
    #         sheet.merge_cells(start_row=1, end_row=1, start_column=3 + i * 4, end_column=6 + i * 4)
    #         cell = sheet.cell(row=1, column=3 + i * 4)
    #         cell.value = index_names[i+2]
    #         cell.alignment = Alignment(horizontal='center', vertical='center')
    #         for j in range(4):
    #             cell = sheet.cell(row=2, column=3 + i * 4 + j)
    #             cell.value = "n" + str(j+1)
    #             cell.alignment = Alignment(horizontal='center', vertical='center')
    #     return wb
    #
    #
    # wb = formulateTable()
    # wb.save(cache_path + "test" + ".xlsx")
    # wb.close()
