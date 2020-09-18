import mpl_finance as mpf  # 替换 import matplotlib.finance as mpf
import numpy as np
import matplotlib.pyplot as plt


class DefTypesPool():

    def __init__(self):
        self.routes = {}

    def route_types(self, types_str):
        def decorator(f):
            self.routes[types_str] = f
            return f

        return decorator

    def route_output(self, path):
        # print(u"output [%s] function:" % path)
        function_val = self.routes.get(path)
        if function_val:
            return function_val
        else:
            raise ValueError('Route "{}"" has not been registered'.format(path))


class MplTypesDraw():
    mpl = DefTypesPool()

    @mpl.route_types(u"line")
    def line_plot(df_index, df_dat, graph):
        # 绘制line图
        for key, val in df_dat.items():
            graph.plot(np.arange(0, len(val)), val, label=key, lw=1.0)

    @mpl.route_types(u"ochl")
    def ochl_plot(df_index, df_dat, graph):
        # 绘制ochl图——Kline
        # 方案一
        mpf.candlestick2_ochl(graph, df_dat['Open'], df_dat['Close'], df_dat['High'], df_dat['Low'], width=0.5,
                              colorup='r', colordown='g')  # 绘制K线走势
        # 方案二
        ohlc = list(zip(np.arange(0, len(df_index)), df_dat['Open'], df_dat['Close'], df_dat['High'],
                        df_dat['Low']))  # 使用zip方法生成数据列表
        mpf.candlestick_ochl(graph, ohlc, width=0.2, colorup='r', colordown='g', alpha=1.0)  # 绘制K线走势

    @mpl.route_types(u"bar")
    def bar_plot(df_index, df_dat, graph):
        # 绘制bar图——Volume
        # graph.bar(np.arange(0, len(df_index)), df_dat['Volume'], \
        #     color=['g' if df_dat['Open'][x] > df_dat['Close'][x] else 'r' for x in range(0,len(df_index))])

        graph.bar(np.arange(0, len(df_index)), df_dat['bar_red'], facecolor='red')
        graph.bar(np.arange(0, len(df_index)), df_dat['bar_green'], facecolor='green')

    @mpl.route_types(u"hline")
    def hline_plot(df_index, df_dat, graph):
        # 绘制hline图
        for key, val in df_dat.items():
            graph.axhline(val['pos'], c=val['c'], label=key)

    @mpl.route_types(u"annotate")
    def annotate_plot(df_index, df_dat, graph):
        # 绘制annotate图
        for key, val in df_dat.items():
            for kl_index, today in val['andata'].iterrows():
                x_posit = df_index.get_loc(kl_index)
                graph.annotate(u"{}\n{}".format(key, today.name.strftime("%m.%d")),
                               xy=(x_posit, today[val['xy_y']]),
                               xycoords='data',
                               xytext=(val['xytext'][0], val['xytext'][1]),
                               va=val['va'],  # 点在标注下方
                               textcoords='offset points',
                               fontsize=val['fontsize'],
                               arrowprops=val['arrow'])

    @mpl.route_types(u"filltrade")
    def filltrade_plot(df_index, df_dat, graph):
        # 绘制filltrade图
        signal_shift = df_dat['signal'].shift(1)
        signal_shift.fillna(value=-1, inplace=True)  # 序列最前面的NaN值用-1填充
        list_signal = np.sign(df_dat['signal'] - signal_shift)
        bs_singal = list_signal[list_signal != 0]

        skip_days = False
        for kl_index, value in bs_singal.iteritems():  # iteritems以迭代器形式返回
            if (value == 1) and (skip_days == False):
                start = df_index.get_loc(kl_index)
                skip_days = True
            elif (value == -1) and (skip_days == True):
                end = df_index.get_loc(kl_index) + 1  # 加1用于匹配[start:end]选取到end值
                skip_days = False

                if df_dat['jdval'][end - 1] < df_dat['jdval'][start]:  # 赔钱显示绿色
                    graph.fill_between(np.arange(start, end), 0, df_dat['jdval'][start:end], color='green', alpha=0.38)
                    is_win = False
                else:  # 赚钱显示红色
                    graph.fill_between(np.arange(start, end), 0, df_dat['jdval'][start:end], color='red', alpha=0.38)
                    is_win = True
                graph.annotate('获利\n' if is_win else '亏损\n',
                               xy=(end, df_dat['jdval'].asof(kl_index)),
                               xytext=(df_dat['xytext'][0], df_dat['xytext'][1]),
                               xycoords='data',
                               va=df_dat['va'],  # 点在标注下方
                               textcoords='offset points',
                               fontsize=df_dat['fontsize'],
                               arrowprops=df_dat['arrow'])
        # 整个时间序列填充为底色blue 透明度alpha小于后标注区间颜色
        graph.fill_between(np.arange(0, len(df_index)), 0, df_dat['jdval'], color='blue', alpha=.08)


class MplVisualIf(MplTypesDraw):  # matplotlib Visualization interface

    def __init__(self):
        MplTypesDraw.__init__(self)

    def fig_creat(self, **kwargs):
        if 'figsize' in kwargs.keys():  # 创建fig对象
            self.fig = plt.figure(figsize=kwargs['figsize'], dpi=100, facecolor="white")
        else:
            self.fig = plt.figure(figsize=(14, 7), dpi=100, facecolor="white")
        self.graph = self.fig.add_subplot(1, 1, 1)  # 创建子图
        self.fig.autofmt_xdate(rotation=45)  # 避免x轴日期刻度标签的重叠 将每个ticker标签倾斜45度

    def fig_config(self, **kwargs):
        if 'legend' in kwargs.keys():
            self.graph.legend(loc=kwargs['legend'], shadow=True)
        if 'xlabel' in kwargs.keys():
            self.graph.set_xlabel(kwargs['xlabel'])
        else:
            self.graph.set_xlabel(u"日期")
        self.graph.set_title(kwargs['title'])
        self.graph.set_ylabel(kwargs['ylabel'])
        self.graph.set_xlim(0, len(self.index))  # 设置x轴的范围

        if 'ylim' in kwargs.keys():  # 设置y轴的范围
            bottom_lim = self.graph.get_ylim()[0]
            top_lim = self.graph.get_ylim()[1]
            range_lim = top_lim - bottom_lim
            self.graph.set_ylim(bottom_lim + range_lim * kwargs['ylim'][0],
                                top_lim + range_lim * kwargs['ylim'][1])

        if 'xticks' in kwargs.keys():  # X轴刻度设定
            self.graph.set_xticks(range(0, len(self.index), kwargs['xticks']))
        else:
            self.graph.set_xticks(range(0, len(self.index), 15))  # 默认每15天标一个日期
        if 'xticklabels' in kwargs.keys():  # 标签设置为日期
            self.graph.set_xticklabels([self.index.strftime(kwargs['xticklabels'])[index] \
                                        for index in self.graph.get_xticks()])
        else:
            self.graph.set_xticklabels([self.index.strftime('%Y-%m-%d')[index] \
                                        for index in self.graph.get_xticks()])

    def fig_show(self, **kwargs):
        plt.show()

    def fig_output(self, **kwargs):
        self.index = kwargs['index']
        self.fig_creat(**kwargs)
        for path, val in kwargs['draw_kind'].items():
            print(u"输出[%s]可视化图表:" % path)
            view_function = self.mpl.route_output(path)
            view_function(self.index, val, self.graph)
        self.fig_config(**kwargs)
        self.fig_show(**kwargs)