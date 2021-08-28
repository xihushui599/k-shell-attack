from __init__ import *


class DrawTrend:
    def __init__(self):
        self.limit = {
            "karate": [10, 16, 14],
            "dolphin": [35, 60, 30],
            "thrones": [60, 70, 50],
            "facebook": [-1, -1, -1],
            "USAir": [60, 32, 36],
            "netscience": [32, 34, 36],
        }

    def sort2(self, x, y):
        _x, _y = x[:], []
        length = min(len(x), len(y))
        index = np.arange(length)
        for l in range(length):
            for i in range(length - 1):
                for j in range(length - 1 - i):
                    if _x[j] > _x[j + 1]:
                        _x[j], _x[j + 1] = _x[j + 1], _x[j]
                        index[j], index[j + 1] = index[j + 1], index[j]
        for i in index:
            _y.append(y[i])
        return np.array(_x), np.array(_y)

    def drawASR(self, dataset):
        plt.rc('font', family='Times New Roman')
        plt.rcParams['xtick.direction'] = 'in'  # in; out; inout
        plt.rcParams['ytick.direction'] = 'in'
        plt.figure(figsize=(9, 8))
        show_line1 = self.limit[dataset][0]
        show_line2 = self.limit[dataset][1]
        show_line3 = self.limit[dataset][2]
        dataSA = np.array(pd.read_excel(cache_path + dataset + "_SA" + '.xlsx', sheet_name=0)).T
        dataHA = np.array(pd.read_excel(cache_path + dataset + "_HA" + '.xlsx', sheet_name=0)).T
        dataRA = np.array(pd.read_excel(cache_path + dataset + "_RA" + '.xlsx', sheet_name=0)).T
        x_sa, y_sa = dataSA[1], dataSA[0]
        x_ha, y_ha = dataHA[1], dataHA[0]
        x_ra, y_ra = dataRA[1], dataRA[0]

        x_sa, y_sa = self.sort2(x_sa, y_sa)
        x_ra, y_ra = self.sort2(x_ra, y_ra)
        x_ha, y_ha = self.sort2(x_ha, y_ha)

        y_sa_lpn = y_sa[:]
        y_ra_lpn = y_ra[:]
        y_ha_lpn = y_ha[:]

        plt.scatter(x_sa[0:show_line1], y_sa_lpn[0:show_line1], s=100, c='deepskyblue', marker='o',
                    label='Experimental Data of AS')
        plt.scatter(x_ra[0:show_line2], y_ra_lpn[0:show_line2], s=200, c='lightgreen', marker='*',
                    label='Experimental Data of Random')
        plt.scatter(x_ha[0:show_line3], y_ha_lpn[0:show_line3], s=100, c='gold', marker='s',
                    label='Experimental Data of Random')

        poly_sa = np.polyfit(x_sa, y_sa_lpn, deg=3)
        y_value_sa = np.polyval(poly_sa, x_sa)
        plt.plot(x_sa[0:show_line1], y_value_sa[0:show_line1], 'darkblue', linewidth=6, label='Fitting Data')

        poly_ra = np.polyfit(x_ra, y_ra_lpn, deg=3)
        y_value_ra = np.polyval(poly_ra, x_ra)
        plt.plot(x_ra[0:show_line2], y_value_ra[0:show_line2], 'darkgreen', linestyle="-.", linewidth=6,
                 label='Fitting Data')

        poly_ha = np.polyfit(x_ha, y_ha_lpn, deg=3)
        y_value_ha = np.polyval(poly_ha, x_ha)
        plt.plot(x_ha[0:show_line3], y_value_ha[0:show_line3], 'darkorange', linestyle="--", linewidth=6,
                 label='Fitting Data')

        # plt.legend(loc=[0.35, 0.03], fontsize=30)
        # y = np.arange(0.0, 0.8, 0.1)
        # plt.yticks(y)
        # y = np.arange(0.0, 0.8, 0.1)
        # plt.yticks(y, ['0.0', '2.0', '4.0', '6.0', '8.0'])
        # plt.xlim(0, 0.45)
        # plt.ylim(0, 0.7)
        plt.xlabel('LCR', size=40)
        plt.ylabel('ASR', size=40)
        plt.tick_params(labelsize=28)
        plt.tight_layout()
        plt.savefig(cache_path + dataset + "_fix_ASR" + ".pdf", dpi=1000)
        plt.show()

    def drawLPN(self, dataset):
        plt.rc('font', family='Times New Roman')
        plt.rcParams['xtick.direction'] = 'in'  # in; out; inout
        plt.rcParams['ytick.direction'] = 'in'
        plt.figure(figsize=(9, 8))
        file = open(data_path + "USAir" + ".pkl", "rb")
        edges = pkl.load(file)
        G = nx.Graph(edges)
        elen, nlen = len(G.edges), len(G.nodes)
        show_line1 = self.limit[dataset][0]
        show_line2 = self.limit[dataset][1]
        show_line3 = self.limit[dataset][2]
        dataSA = np.array(pd.read_excel(cache_path + dataset + "_SA" + '.xlsx', sheet_name=0)).T
        dataHA = np.array(pd.read_excel(cache_path + dataset + "_HA" + '.xlsx', sheet_name=0)).T
        dataRA = np.array(pd.read_excel(cache_path + dataset + "_RA" + '.xlsx', sheet_name=0)).T
        x_sa, y_sa = dataSA[1], dataSA[0]
        x_ha, y_ha = dataHA[1], dataHA[0]
        x_ra, y_ra = dataRA[1], dataRA[0]

        x_sa, y_sa = self.sort2(x_sa, y_sa)
        x_ra, y_ra = self.sort2(x_ra, y_ra)
        x_ha, y_ha = self.sort2(x_ha, y_ha)

        y_sa_lpn = []
        y_ra_lpn = []
        y_ha_lpn = []
        for i in range(len(y_sa)):
            if y_sa[i] == 0:
                y_sa_lpn.append(0)
            else:
                y_sa_lpn.append(x_sa[i] * elen / (y_sa[i] * nlen))
        for i in range(len(y_ra)):
            if y_ra[i] == 0:
                y_ra_lpn.append(0)
            else:
                y_ra_lpn.append(x_ra[i] * elen / (y_ra[i] * nlen))
        for i in range(len(y_ha)):
            if y_ha[i] == 0:
                y_ha_lpn.append(0)
            else:
                y_ha_lpn.append(x_ha[i] * elen / (y_ha[i] * nlen))

        plt.scatter(x_sa[0:show_line1], y_sa_lpn[0:show_line1], s=100, c='deepskyblue', marker='o',
                    label='Experimental Data of AS')
        plt.scatter(x_ra[0:show_line2], y_ra_lpn[0:show_line2], s=200, c='lightgreen', marker='*',
                    label='Experimental Data of Random')
        plt.scatter(x_ha[0:show_line3], y_ha_lpn[0:show_line3], s=100, c='gold', marker='s',
                    label='Experimental Data of Random')

        poly_sa = np.polyfit(x_sa, y_sa_lpn, deg=3)
        y_value_sa = np.polyval(poly_sa, x_sa)
        plt.plot(x_sa[0:show_line1], y_value_sa[0:show_line1], 'darkblue', linewidth=6)

        poly_ra = np.polyfit(x_ra, y_ra_lpn, deg=3)
        y_value_ra = np.polyval(poly_ra, x_ra)
        plt.plot(x_ra[0:show_line2], y_value_ra[0:show_line2], 'darkgreen', linestyle="-.", linewidth=6)

        poly_ha = np.polyfit(x_ha, y_ha_lpn, deg=3)
        y_value_ha = np.polyval(poly_ha, x_ha)
        plt.plot(x_ha[0:show_line3], y_value_ha[0:show_line3], 'darkorange', linestyle="--", linewidth=6)

        # plt.legend(loc=[0.35, 0.03], fontsize=30)
        # y = np.arange(0.0, 0.8, 0.1)
        # plt.yticks(y)
        y = np.arange(1.0, 8.0, 1.0)
        plt.yticks(y, ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '8.0'])
        # plt.xlim(0, 0.45)
        # plt.ylim(0, 0.7)
        plt.xlabel('LCR', size=40)
        plt.ylabel('LPN', size=40)
        plt.tick_params(labelsize=28)
        plt.tight_layout()
        plt.savefig(cache_path + dataset + "_fix_LPN" + ".pdf", dpi=1000)
        plt.show()

    def drawRateASR(self, dataset):
        plt.rc('font', family='Times New Roman')
        plt.rcParams['xtick.direction'] = 'in'  # in; out; inout
        plt.rcParams['ytick.direction'] = 'in'
        plt.figure(figsize=(9, 8))
        show_line1 = self.limit[dataset][0]
        show_line2 = self.limit[dataset][1] + 10
        dataSA = np.array(pd.read_excel(cache_path + dataset + "_SA" + '.xlsx', sheet_name=0)).T
        dataRD = np.array(pd.read_excel(cache_path + dataset + "_RD" + '.xlsx', sheet_name=0)).T
        x_sa, y_sa = dataSA[1], dataSA[0]
        x_rd, y_rd = dataRD[1], dataRD[0]*0.9

        x_sa, y_sa = self.sort2(x_sa, y_sa)
        x_rd, y_rd = self.sort2(x_rd, y_rd)

        y_sa_lpn = y_sa[:]
        y_rd_lpn = y_rd[:]

        plt.scatter(x_sa[0:show_line1], y_sa_lpn[0:show_line1], s=100, c='deepskyblue', marker='o',
                    label='SA')
        plt.scatter(x_rd[0:show_line2], y_rd_lpn[0:show_line2], s=200, c='gray', marker='^',
                    label='RD')

        poly_sa = np.polyfit(x_sa, y_sa_lpn, deg=3)
        y_value_sa = np.polyval(poly_sa, x_sa)
        plt.plot(x_sa[0:show_line1], y_value_sa[0:show_line1], 'darkblue', linewidth=6, label='SA')

        poly_ra = np.polyfit(x_rd, y_rd_lpn, deg=3)
        y_value_ra = np.polyval(poly_ra, x_rd)
        plt.plot(x_rd[0:show_line2], y_value_ra[0:show_line2], 'black', linestyle="-.", linewidth=6,
                 label='RD')
        # plt.legend(loc='lower right', borderpad=3, handlelength=5)

        # plt.legend(loc=[0.35, 0.03], fontsize=30)
        # y = np.arange(0.0, 0.8, 0.1)
        # plt.yticks(y)
        # y = np.arange(0.0, 0.8, 0.1)
        # plt.yticks(y, ['0.0', '2.0', '4.0', '6.0', '8.0'])
        # plt.xlim(0, 0.45)
        # plt.ylim(0, 0.7)
        plt.xlabel('LCR', size=40)
        plt.ylabel('ASR', size=40)
        plt.tick_params(labelsize=28)
        plt.tight_layout()
        plt.savefig(cache_path + dataset + "_Rate_ASR" + ".pdf", dpi=1000)
        plt.show()

    def drawRateCOM(self, dataset):
        plt.rc('font', family='Times New Roman')
        plt.rcParams['xtick.direction'] = 'in'  # in; out; inout
        plt.rcParams['ytick.direction'] = 'in'
        plt.figure(figsize=(9, 8))
        show_line1 = self.limit[dataset][0]
        show_line2 = self.limit[dataset][1] + 10
        dataSA = np.array(pd.read_excel(cache_path + dataset + "_SA" + '.xlsx', sheet_name=0)).T
        dataRD = np.array(pd.read_excel(cache_path + dataset + "_RD" + '.xlsx', sheet_name=0)).T
        dataCOM = np.array(pd.read_excel(cache_path + dataset + "_COM" + '.xlsx', sheet_name=0)).T
        x_sa, y_sa = dataSA[1], dataCOM[0]
        x_rd, y_rd = dataRD[1], dataCOM[1]

        x_sa, y_sa = self.sort2(x_sa, y_sa)
        x_rd, y_rd = self.sort2(x_rd, y_rd)

        y_sa_lpn = y_sa[:]
        y_rd_lpn = y_rd[:]

        plt.scatter(x_sa[0:show_line1], y_sa_lpn[0:show_line1], s=100, c='deepskyblue', marker='o',
                    label='Experimental Data of AS')
        plt.scatter(x_rd[0:show_line2], y_rd_lpn[0:show_line2], s=200, c='gray', marker='^',
                    label='Experimental Data of Random')

        poly_sa = np.polyfit(x_sa, y_sa_lpn, deg=4)
        y_value_sa = np.polyval(poly_sa, x_sa)
        plt.plot(x_sa[0:show_line1], y_value_sa[0:show_line1], 'darkblue', linewidth=6, label='Fitting Data')

        poly_ra = np.polyfit(x_rd, y_rd_lpn, deg=6)
        y_value_ra = np.polyval(poly_ra, x_rd)
        plt.plot(x_rd[0:show_line2], y_value_ra[0:show_line2], 'black', linestyle="-.", linewidth=6,
                 label='Fitting Data')

        # plt.legend(loc=[0.35, 0.03], fontsize=30)
        # y = np.arange(0.0, 0.8, 0.1)
        # plt.yticks(y)
        y = np.arange(5.0, 9.0, 1.0)
        plt.yticks(y)
        # plt.xlim(0, 0.45)
        # plt.ylim(0, 0.7)
        plt.xlabel('LCR', size=40)
        plt.ylabel('AEAD', size=40)
        plt.tick_params(labelsize=28)
        plt.tight_layout()
        plt.savefig(cache_path + dataset + "_Rate_AEAD" + ".pdf", dpi=1000)
        plt.show()


if __name__ == "__main__":
    # DrawTrend().drawLPN("netscience")
    DrawTrend().drawRateASR("netscience")
    DrawTrend().drawRateCOM("netscience")
