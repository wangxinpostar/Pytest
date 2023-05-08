
import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.commons.utils import JsCode
import matplotlib.font_manager as fm
from namemap import namemap
from sklearn.tree import export_graphviz
from IPython.display import Image
from pylab import *
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
mpl.rcParams['font.sans-serif'] = ['SimHei']



# 数据存放在列表里
datas = []
# 遍历十页数据
for k in range(10):
    print("正在抓取第{}页数据...".format(k + 1))
    url = 'https://movie.douban.com/top250?start=' + str(k * 25)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    # 查找电影链接
    lists = soup.find_all('div', {'class': 'hd'})

    # 遍历每条电影链接
    for item in lists:
        href = item.a['href']
        # 休息一下，防止被封
        time.sleep(5)
        # 请求每条电影，获得详细信息
        response = requests.get(href, headers=headers)
        # 把获取好的电影数据打包成BeautifulSoup对象
        movie_soup = BeautifulSoup(response.text, 'lxml')

        # 获取电影星级评分
        star = []
        rating_items = movie_soup.find(
            'div', {'class': 'ratings-on-weight'}).find_all('div', {'class': 'item'})
        for rating_item in rating_items:
            rating_per = rating_item.find(
                'span', {'class': 'rating_per'}).get_text()
            star.append(rating_per)

        # 解析每条电影数据
        # 片名
        name = movie_soup.find(
            'span', {'property': 'v:itemreviewed'}).text.split(' ')[0]
        # 上映年份
        year = movie_soup.find('span', {'class': 'year'}).text.replace(
            '(', '').replace(')', '')
        # 评分
        score = movie_soup.find('strong', {'property': 'v:average'}).text
        # 评价人数
        votes = movie_soup.find('span', {'property': 'v:votes'}).text
        infos = movie_soup.find('div', {'id': 'info'}).text.split('\n')[1:11]
        # infos返回的是一个列表，我们只需要索引提取就好了
        # 导演
        director = infos[0].split(': ')[1]
        # 编剧
        scriptwriter = infos[1].split(': ')[1]
        # 主演
        actor = infos[2].split(': ')[1]
        # 类型
        filmtype = infos[3].split(': ')[1]
        # 国家/地区
        area = infos[4].split(': ')[1]

        # 数据清洗一下
        if '.' in area:
            area = infos[5].split(': ')[1].split(' / ')[0]
            # 语言
            language = infos[6].split(': ')[1].split(' / ')[0]
        else:
            area = infos[4].split(': ')[1].split(' / ')[0]
            # 语言
            language = infos[5].split(': ')[1].split(' / ')[0]
        if '大陆' in area or '中国香港' in area or '台湾' in area:
            area = '中国'
        if '戛纳' in area:
            area = '法国'
        # 时长
        times0 = movie_soup.find(attrs={'property': 'v:runtime'}).text
        times = re.findall('\d+', times0)[0]

        # 将数据写入列表
        datas.append({
            '片名': name,
            '上映年份': year,
            '评分': score,
            '评价人数': votes,
            '导演': director,
            '编剧': scriptwriter,
            '主演': actor,
            '类型': filmtype,
            '国家/地区': area,
            '语言': language,
            '时长(分钟)': times,
            '五星': star[0],
            '四星': star[1],
            '三星': star[2],
            '二星': star[3],
            '一星': star[4]
        })
        print("电影《{0}》已爬取完成...".format(name))



# 写入到文件
df = pd.DataFrame(datas)
df.to_csv("豆瓣电影top250.csv", index=False, header=True, encoding='utf_8_sig')



data = pd.read_csv('豆瓣电影top250.csv')
year_counts = data['上映年份'].value_counts()
year_counts.columns = ['上映年份', '数量']
year_counts = year_counts.sort_index()
c = (
    Bar()
    .add_xaxis(list(year_counts.index))
    .add_yaxis('上映数量', year_counts.values.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title='各年份上映电影数量'),
        yaxis_opts=opts.AxisOpts(name='上映数量'),
        xaxis_opts=opts.AxisOpts(name='上映年份'),
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_='inside')], )
)
c.render_notebook()



data = pd.read_csv('豆瓣电影top250.csv')
y1 = len(data[data['电影年份'] == '20世纪30年代'])
y2 = len(data[data['电影年份'] == '20世纪40年代'])
y3 = len(data[data['电影年份'] == '20世纪50年代'])
y4 = len(data[data['电影年份'] == '20世纪60年代'])
y5 = len(data[data['电影年份'] == '20世纪70年代'])
y6 = len(data[data['电影年份'] == '20世纪80年代'])
y7 = len(data[data['电影年份'] == '20世纪90年代'])
y8 = len(data[data['电影年份'] == '21世纪00年代'])
y9 = len(data[data['电影年份'] == '21世纪10年代'])
y10 = len(data[data['电影年份'] == '21世纪20年代'])

# 定义饼图的数据
data = [
    ("20世纪30年代", y1),
    ("20世纪40年代", y2),
    ("20世纪50年代", y3),
    ("20世纪60年代", y4),
    ("20世纪70年代", y5),
    ("20世纪80年代", y6),
    ("20世纪90年代", y7),
    ("21世纪00年代", y8),
    ("21世纪10年代", y9),
    ("21世纪20年代", y10),
]

# 创建饼图实例并设置全局配置
pie = Pie() \
    .set_global_opts(
        title_opts=opts.TitleOpts(title="豆瓣电影 Top250 各年代电影数量比例图"),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_top="15%",
            pos_left="85%"
        )
)
colors = ['#ff7f50', '#e9cefa', '#ae70d6', '#e2cd32', '#a495ed',
          '#fa69b4', '#da58d3', '#2e5c5c', '#bfa450', '#45e0d0']


# 设置饼图数据和样式
pie.add(
    "",
    data,
    radius=["40%", "70%"],
    label_opts=opts.LabelOpts(
        formatter="{b}: {c} ({d}%)",
        font_size=12,
        font_weight="bold",
        position="outside",
    ),
).set_colors(colors)

pie.render_notebook()



data = pd.read_csv('豆瓣电影top250.csv')
df = data.sort_values(by='评价人数', ascending=True)
c = (
    Bar()
    .add_xaxis(df['片名'].values.tolist()[-20:])
    .add_yaxis('评价人数', df['评价人数'].values.tolist()[-20:])
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='电影评价人数'),
        yaxis_opts=opts.AxisOpts(name='片名'),
        xaxis_opts=opts.AxisOpts(name='人数'),
        datazoom_opts=opts.DataZoomOpts(type_='inside'),
    )
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
)
c.render_notebook()



data = pd.read_csv('豆瓣电影top250.csv')
country_counts = data['国家/地区'].value_counts()
country_counts.columns = ['国家/地区', '数量']

country_counts = country_counts.sort_values(ascending=True)
c = (
    Bar()
    .add_xaxis(list(country_counts.index)[:])
    .add_yaxis('地区上映数量', country_counts.values.tolist()[:])
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='地区上映电影数量'),
        yaxis_opts=opts.AxisOpts(name='国家/地区'),
        xaxis_opts=opts.AxisOpts(name='上映数量'),
    )
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
)
c.render_notebook()



data = pd.read_csv('豆瓣电影top250.csv')
country_counts = data['国家/地区'].value_counts()
name_map = namemap.nameMap
map = Map(opts.InitOpts(width="700px", height="300px"))
map.add("上榜电影数", [('美国', 112), ('中国', 42), ('日本', 34), ('英国', 20), ('韩国', 10), ('法国', 8), ('意大利', 5), ('德国', 4), ('澳大利亚', 3), ('印度', 2), ('瑞典', 1), ('泰国', 1), ('阿根廷', 1), ('巴西', 1), ('新西兰', 1), ('丹麦', 1), ('伊朗', 1), ('西班牙', 1), ('黎巴嫩', 1), ('爱尔兰', 1)], is_map_symbol_show=True, name_map=name_map,
        maptype="world", label_opts=opts.LabelOpts(is_show=False))  # 地图区域颜色
map.set_global_opts(title_opts=opts.TitleOpts(title='全球各地区上榜电影数'), legend_opts=opts.LegendOpts(is_show=True),
                    visualmap_opts=opts.VisualMapOpts(
                        range_color=["#E0ECF8", "#045FB4"], max_=120)
                    )
map.render_notebook()



# 读取数据
data = pd.read_csv('豆瓣电影top250.csv')
types = '/'.join(data['类型'])  # 转化成以‘/’间隔的字符串
types = types.replace(' ', '')  # 将空格值进行替换
typelist = types.split('/')  # 进行切割
t = list(set(typelist))  # 去除重复
count = []
for i in t:
    count.append(typelist.count(i))  # 统计出现 次数
bar = Bar()
bar.add_xaxis(t)
bar.add_yaxis('电影类型', count)
bar.set_global_opts(
    title_opts=opts.TitleOpts(title="电影类型分布情况"),
    xaxis_opts=opts.AxisOpts(
        name='电影类型', axislabel_opts=opts.LabelOpts(rotate=45)),
    yaxis_opts=opts.AxisOpts(name='数量'),
)
bar.render_notebook()



# 构造词云数据
data = list(zip(t, count))

# 创建词云图实例并添加数据
wordcloud = WordCloud() \
    .add("", data_pair=data, word_size_range=[12, 120], rotate_step=90, pos_left=30) \
    .set_global_opts(title_opts=opts.TitleOpts(title="豆瓣电影 Top250 电影类型词云图"))

# 展示图表
wordcloud.render_notebook()



data = pd.read_csv('豆瓣电影top250.csv')
data.head()
for columns in data.iloc[:, 12:].columns:
    data[columns] = data[columns].str.strip("%").astype(float)/100
y_train = data["评分"].values
x_train = data.iloc[:, 12:].values



# 随机森林回归模型
y_test = y_train
x_test = x_train
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(x_train, y_train)
y_predict_rf = rf.predict(x_test)

# 输出随机森林回归模型结果
print("随机森林回归模型结果：")
print("准确率：", rf.score(x_test, y_test))
print("R2：", r2_score(y_test, y_predict_rf))
print("MSE：", mean_squared_error(y_test, y_predict_rf))
print("MAE：", mean_absolute_error(y_test, y_predict_rf))



line = Line()
line.add_xaxis(range(len(y_test)))
line.add_yaxis("测试数据", y_test, color="red", symbol='none')
line.add_yaxis("预测数据", y_predict_rf, color="blue", symbol='none')
line.set_global_opts(title_opts=opts.TitleOpts(title="测试数据与预测数据对比"),
                     xaxis_opts=opts.AxisOpts(name="电影排行"),
                     yaxis_opts=opts.AxisOpts(min_=8, max_=10, name="评分"),
                     )
line.render_notebook()



# 回归树模型
y_test = y_train
x_test = x_train
dt = DecisionTreeRegressor(random_state=42)
dt.fit(x_train[:100], y_train[:100])
y_predict_dt = dt.predict(x_test)

# 输出回归树模型结果
print("\n回归树模型结果：")
print("准确率：", dt.score(x_test, y_test))
print("R2：", r2_score(y_test, y_predict_dt))
print("MSE：", mean_squared_error(y_test, y_predict_dt))
print("MAE：", mean_absolute_error(y_test, y_predict_dt))



line = Line()
line.add_xaxis(range(len(y_test)))
line.add_yaxis("测试数据", y_test, color="red", symbol='none')
line.add_yaxis("预测数据", y_predict_dt, color="blue", symbol='none')
line.set_global_opts(title_opts=opts.TitleOpts(title="测试数据与预测数据对比"),
                     xaxis_opts=opts.AxisOpts(name="电影排行"),
                     yaxis_opts=opts.AxisOpts(min_=8, max_=10, name="评分"),
                     )
line.render_notebook()



# 梯度提升回归模型
y_test = y_train
x_test = x_train
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(x_train, y_train)
y_predict_gb = gb.predict(x_test)

# 输出梯度提升回归模型结果
print("\n梯度提升回归模型结果：")
print("准确率：", gb.score(x_test, y_test))
print("R2：", r2_score(y_test, y_predict_gb))
print("MSE：", mean_squared_error(y_test, y_predict_gb))
print("MAE：", mean_absolute_error(y_test, y_predict_gb))



line = Line()
line.add_xaxis(range(len(y_test)))
line.add_yaxis("测试数据", y_test, color="red", symbol='none')
line.add_yaxis("预测数据", y_predict_gb, color="blue", symbol='none')
line.set_global_opts(title_opts=opts.TitleOpts(title="测试数据与预测数据对比"),
                     xaxis_opts=opts.AxisOpts(name="电影排行"),
                     yaxis_opts=opts.AxisOpts(min_=8, max_=10, name="评分"),
                     )
line.render_notebook()



