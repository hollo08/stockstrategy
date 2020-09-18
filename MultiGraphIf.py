from MplVisualIf import MplTypesDraw, DefTypesPool
import matplotlib.gridspec as gridspec  # 分割子图
import matplotlib.pyplot as plt
import numpy as np

class MultiGraphIf(MplTypesDraw):
    app = DefTypesPool()

    ##########################行情分析界面###############################
    @app.route_types(u"ochl")
    def ochl_graph(stock_dat, sub_graph, df_dat=None):  # prepare data
        type_dict = {'Open': stock_dat.Open,
                     'Close': stock_dat.Close,
                     'High': stock_dat.High,
                     'Low': stock_dat.Low
                     }
        view_function = MplTypesDraw.mpl.route_output(u"ochl")
        view_function(stock_dat.index, type_dict, sub_graph)

    @app.route_types(u"sma")
    def sma_graph(stock_dat, sub_graph, periods):  # prepare data
        for val in periods:
            type_dict = {'SMA' + str(val): stock_dat.Close.rolling(window=val).mean()}
            view_function = MplTypesDraw.mpl.route_output(u"line")
            view_function(stock_dat.index, type_dict, sub_graph)

    @app.route_types(u"vol")
    def vol_graph(stock_dat, sub_graph, df_dat=None):  # prepare data
        type_dict = {'bar_red': np.where(stock_dat.Open < stock_dat.Close, stock_dat.Volume, 0),  # 绘制BAR>0 柱状图
                     'bar_green': np.where(stock_dat.Open > stock_dat.Close, stock_dat.Volume, 0)  # 绘制BAR<0 柱状图
                     }
        view_function = MplTypesDraw.mpl.route_output(u"bar")
        view_function(stock_dat.index, type_dict, sub_graph)

    @app.route_types(u"macd")
    def macd_graph(stock_dat, sub_graph, df_dat=None):  # prepare data

        macd_dif = stock_dat['Close'].ewm(span=12, adjust=False).mean() - stock_dat['Close'].ewm(span=26,
                                                                                                 adjust=False).mean()
        macd_dea = macd_dif.ewm(span=9, adjust=False).mean()
        macd_bar = 2 * (macd_dif - macd_dea)

        type_dict = {'bar_red': np.where(macd_bar > 0, macd_bar, 0),  # 绘制BAR>0 柱状图
                     'bar_green': np.where(macd_bar < 0, macd_bar, 0)  # 绘制BAR<0 柱状图
                     }
        view_function = MplTypesDraw.mpl.route_output(u"bar")
        view_function(stock_dat.index, type_dict, sub_graph)

        type_dict = {'macd dif': macd_dif,
                     'macd dea': macd_dea
                     }
        view_function = MplTypesDraw.mpl.route_output(u"line")
        view_function(stock_dat.index, type_dict, sub_graph)

    @app.route_types(u"kdj")
    def kdj_graph(stock_dat, sub_graph, df_dat=None):  # prepare data

        low_list = stock_dat['Low'].rolling(9, min_periods=1).min()
        high_list = stock_dat['High'].rolling(9, min_periods=1).max()
        rsv = (stock_dat['Close'] - low_list) / (high_list - low_list) * 100
        stock_dat['K'] = rsv.ewm(com=2, adjust=False).mean()
        stock_dat['D'] = stock_dat['K'].ewm(com=2, adjust=False).mean()
        stock_dat['J'] = 3 * stock_dat['K'] - 2 * stock_dat['D']

        type_dict = {'K': stock_dat.K,
                     'D': stock_dat.D,
                     'J': stock_dat.J
                     }
        view_function = MplTypesDraw.mpl.route_output(u"line")
        view_function(stock_dat.index, type_dict, sub_graph)

    def __init__(self, **kwargs):
        MplTypesDraw.__init__(self)
        self.fig = plt.figure(figsize=kwargs['figsize'], dpi=100, facecolor="white")  # 创建fig对象
        self.graph_dict = {}
        self.graph_curr = []

        try:
            gs = gridspec.GridSpec(kwargs['nrows'], kwargs['ncols'],
                                   left=kwargs['left'], bottom=kwargs['bottom'], right=kwargs['right'],
                                   top=kwargs['top'],
                                   wspace=kwargs['wspace'], hspace=kwargs['hspace'],
                                   height_ratios=kwargs['height_ratios'])
        except:
            raise Exception("para error")
        else:
            for i in range(0, kwargs['nrows'], 1):
                self.graph_dict[kwargs['subplots'][i]] = self.fig.add_subplot(gs[i, :])

    def graph_run(self, stock_data, **kwargs):
        # 绘制子图
        self.df_ohlc = stock_data
        for key in kwargs:
            self.graph_curr = self.graph_dict[kwargs[key]['graph_name']]
            for path, val in kwargs[key]['graph_type'].items():
                view_function = MultiGraphIf.app.route_output(path)
                view_function(self.df_ohlc, self.graph_curr, val)
            self.graph_attr(**kwargs[key])
        plt.show()

        """
        print("kwargs %s-->%s" % (key, kwargs[key]))
        #globals().get('self.%s' % key)(**kwargs[key])
        eval('self.%s' % key)()
        #self.kline_draw(**kwargs[key])
        """

    def graph_attr(self, **kwargs):

        if 'title' in kwargs.keys():
            self.graph_curr.set_title(kwargs['title'])

        if 'legend' in kwargs.keys():
            self.graph_curr.legend(loc=kwargs['legend'], shadow=True)

        if 'xlabel' in kwargs.keys():
            self.graph_curr.set_xlabel(kwargs['xlabel'])

        self.graph_curr.set_ylabel(kwargs['ylabel'])
        self.graph_curr.set_xlim(0, len(self.df_ohlc.index))  # 设置一下x轴的范围
        self.graph_curr.set_xticks(range(0, len(self.df_ohlc.index), kwargs['xticks']))  # X轴刻度设定 每15天标一个日期

        if 'xticklabels' in kwargs.keys():
            self.graph_curr.set_xticklabels(
                [self.df_ohlc.index.strftime(kwargs['xticklabels'])[index] for index in
                 self.graph_curr.get_xticks()])  # 标签设置为日期

            # X-轴每个ticker标签都向右倾斜45度
            for label in self.graph_curr.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_fontsize(10)  # 设置标签字体
        else:
            for label in self.graph_curr.xaxis.get_ticklabels():
                label.set_visible(False)