
import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from snownlp import SnowNLP
from tabulate import tabulate
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.commons.utils import JsCode
from collections import Counter
import matplotlib.font_manager as fm
from namemap import namemap
import jieba.analyse
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
    i = requests.get(url, headers=headers)
    soup = BeautifulSoup(i.text, 'lxml')
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
data


data = pd.read_csv('豆瓣电影top250.csv')  # 读取csv文件
year_counts = data['上映年份'].value_counts()  # 统计每个年份的电影数量
year_counts.columns = ['上映年份', '数量']  # 对数据列重命名
year_counts = year_counts.sort_index()  # 根据年份排序
c = (
    Bar()  # 定义柱状图
    .add_xaxis(list(year_counts.index))  # 设置x轴数据
    .add_yaxis('上映数量', year_counts.values.tolist())  # 设置y轴数据
    .set_global_opts(  # 设置全局选项
        title_opts=opts.TitleOpts(title='各年份上映电影数量'),  # 设置图表标题
        yaxis_opts=opts.AxisOpts(name='上映数量'),  # 设置y轴名称
        xaxis_opts=opts.AxisOpts(name='上映年份'),  # 设置x轴名称
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_='inside')], )  # 设置数据缩放选项
)
c.render_notebook()  # 在Notebook中显示图表


# 读取数据
data = pd.read_csv('豆瓣电影top250.csv')

# 统计各个年代的电影数量
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

# 定义饼图的数据，以元组形式存储
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
            orient="vertical",  # 图例垂直排列
            pos_top="15%",  # 图例位置距离顶部的距离
            pos_left="85%"  # 图例位置距离左侧的距离
        )
)

# 定义饼图中各部分的颜色
colors = ['#ff7f50', '#e9cefa', '#ae70d6', '#e2cd32', '#a495ed',
          '#fa69b4', '#da58d3', '#2e5c5c', '#bfa450', '#45e0d0']

# 设置饼图数据和样式
pie.add(
    "",  # 系列名称为空
    data,  # 设置数据
    radius=["40%", "70%"],  # 设置内外半径，形成饼图环形效果
    label_opts=opts.LabelOpts(
        formatter="{b}: {c} ({d}%)",  # 标签格式，b代表数据项名称，c代表数据项值，d代表数据项所占比
        font_size=12,
        font_weight="bold",
        position="outside",
    ),
).set_colors(colors)

pie.render_notebook()


data = pd.read_csv('豆瓣电影top250.csv')

# 按照评价人数从小到大排序
df = data.sort_values(by='评价人数', ascending=True)

# 创建柱状图并设置全局配置
c = (
    Bar()
    # 添加X轴和Y轴的数据
    .add_xaxis(df['片名'].values.tolist()[-20:])
    .add_yaxis('评价人数', df['评价人数'].values.tolist()[-20:])
    # 将XY轴翻转
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='电影评价人数'),
        yaxis_opts=opts.AxisOpts(name='片名'),
        xaxis_opts=opts.AxisOpts(name='人数'),
        datazoom_opts=opts.DataZoomOpts(type_='inside'),
    )
    # 设置系列数据的标签位置
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
)

# 渲染图表并在Jupyter Notebook中显示
c.render_notebook()


# 导入 pandas 库并读取 CSV 文件
data = pd.read_csv('豆瓣电影top250.csv', encoding='utf-8')

# 计算每个导演的作品数量并取前10名
director_counts = data['导演'].value_counts().head(10)

# 绘制条形图
bar = (
    Bar()
    .add_xaxis(director_counts.index.tolist())  # 设置 x 轴的数据
    .add_yaxis("数量", director_counts.tolist())  # 设置 y 轴的数据和标签
    .set_global_opts(title_opts=opts.TitleOpts(title="导演作品数量Top10"),  # 设置全局配置
                     yaxis_opts=opts.AxisOpts(name='数量'),  # 设置 y 轴的名称
                     xaxis_opts=opts.AxisOpts(name='导演', axislabel_opts=opts.LabelOpts(
                         rotate=30)),  # 设置 x 轴的名称和标签旋转角度
                     datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_='inside')])  # 设置数据缩放的类型和配置
)

# 在 Jupyter Notebook 中渲染图表
bar.render_notebook()


data = pd.read_csv('豆瓣电影top250.csv')  # 读取csv文件

country_counts = data['国家/地区'].value_counts()  # 统计各国家/地区上映数量
country_counts.columns = ['国家/地区', '数量']  # 修改列名

country_counts = country_counts.sort_values(ascending=True)  # 按数量升序排序

c = (
    Bar()  # 创建柱状图
    .add_xaxis(list(country_counts.index)[:])  # x轴数据为国家/地区名称
    .add_yaxis('地区上映数量', country_counts.values.tolist()[:])  # y轴数据为上映数量
    .reversal_axis()  # 翻转坐标轴
    .set_global_opts(
        title_opts=opts.TitleOpts(title='地区上映电影数量'),  # 设置标题
        yaxis_opts=opts.AxisOpts(name='国家/地区'),  # 设置y轴名称
        xaxis_opts=opts.AxisOpts(name='上映数量'),  # 设置x轴名称
    )
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))  # 设置标签位置
)
c.render_notebook()  # 在notebook中渲染图表


# 导入 Pandas 库，读取 csv 文件
data = pd.read_csv('豆瓣电影top250.csv')

# 计算每个国家/地区上榜电影的数量
country_counts = data['国家/地区'].value_counts()

# 导入名字映射字典
name_map = namemap.nameMap

# 创建地图实例
map = Map(opts.InitOpts(width="700px", height="300px"))

# 添加数据和设置地图属性
map.add("上榜电影数", [('美国', 112), ('中国', 42), ('日本', 34), ('英国', 20), ('韩国', 10), ('法国', 8), ('意大利', 5), ('德国', 4), ('澳大利亚', 3), ('印度', 2), ('瑞典', 1), ('泰国', 1), ('阿根廷', 1), ('巴西', 1),
        ('新西兰', 1), ('丹麦', 1), ('伊朗', 1), ('西班牙', 1), ('黎巴嫩', 1), ('爱尔兰', 1)], is_map_symbol_show=True, name_map=name_map, maptype="world", label_opts=opts.LabelOpts(is_show=False))
map.set_global_opts(title_opts=opts.TitleOpts(title='全球各地区上榜电影数'), legend_opts=opts.LegendOpts(
    is_show=True), visualmap_opts=opts.VisualMapOpts(range_color=["#E0ECF8", "#045FB4"], max_=120))

# 渲染地图并在 Notebook 中显示
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
y_train = data["评分"].values[:200]
x_train = data.iloc[:, 12:].values[:200]


# 随机森林回归模型
y_test = data["评分"].values[200:250]
x_test = data.iloc[:, 12:].values[200:250]
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
line.add_xaxis((range(200, 251)))
line.add_yaxis("测试数据", y_test, color="red", symbol='none')
line.add_yaxis("预测数据", y_predict_rf, color="blue", symbol='none')
line.set_global_opts(title_opts=opts.TitleOpts(title="测试数据与预测数据对比"),
                     xaxis_opts=opts.AxisOpts(name="电影排行", min_=200, max_=250),
                     yaxis_opts=opts.AxisOpts(min_=8, max_=10, name="评分"),
                     )
line.render_notebook()


# 回归树模型
y_test = data["评分"].values[200:250]
x_test = data.iloc[:, 12:].values[200:250]
dt = DecisionTreeRegressor(random_state=42)
dt.fit(x_train, y_train)
y_predict_dt = dt.predict(x_test)

# 输出回归树模型结果
print("\n回归树模型结果：")
print("准确率：", dt.score(x_test, y_test))
print("R2：", r2_score(y_test, y_predict_dt))
print("MSE：", mean_squared_error(y_test, y_predict_dt))
print("MAE：", mean_absolute_error(y_test, y_predict_dt))


line = Line()
line.add_xaxis(range(200, 251))
line.add_yaxis("测试数据", y_test, color="red", symbol='none')
line.add_yaxis("预测数据", y_predict_dt, color="blue", symbol='none')
line.set_global_opts(title_opts=opts.TitleOpts(title="测试数据与预测数据对比"),
                     xaxis_opts=opts.AxisOpts(name="电影排行", min_=200, max_=250),
                     yaxis_opts=opts.AxisOpts(min_=8, max_=10, name="评分"),
                     )
line.render_notebook()


# 梯度提升回归模型
y_test = data["评分"].values[200:250]
x_test = data.iloc[:, 12:].values[200:250]
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
line.add_xaxis(range(200, 251))
line.add_yaxis("测试数据", y_test, color="red", symbol='none')
line.add_yaxis("预测数据", y_predict_gb, color="blue", symbol='none')
line.set_global_opts(title_opts=opts.TitleOpts(title="测试数据与预测数据对比"),
                     xaxis_opts=opts.AxisOpts(name="电影排行", min_=200, max_=250),
                     yaxis_opts=opts.AxisOpts(min_=8, max_=10, name="评分"),
                     )
line.render_notebook()


# url请求文件头
headers = {'User-Agent': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
           'Cookie': 'll="118318"; bid=kpJGK8qHzSk; gr_user_id=8bbbe733-a805-4e58-bc1a-eb1bdc01bb90; douban-fav-remind=1; viewed="10560798_26858577_35751619"; push_noty_num=0; push_doumail_num=0; dbcl2="266513510:sJIduCLSn40"; ck=eKnB; ap_v=0,6.0; frodotk_db="883e05f049a1ab3098ba11d0dce50190"'}

# 构造请求网址
url_1 = "https://movie.douban.com/subject/1292722/comments?start="

url_2 = "&limit=20&sort=new_score&status=P"

# 循环抓取多页，循环变量为start,0,20,40...
i = 0

while True:
    datas = []
    # 拼接url
    # 当i=0时
    url = url_1+str(i*20)+url_2
    print(url)
    # request请求
    html = requests.get(url, headers=headers)

    # Beautifulsoup解析网址
    soup = BeautifulSoup(html.text, 'lxml')

    # 爬取的数据
    # 评论时间
    # 找span标签，找span标签中的class的comment-time
    comment_time_list = soup.find_all('span', attrs={'class': 'comment-time'})

    # 设置循环终止变量
    # 当评论为0时，就结束循环
    if len(comment_time_list) == 0:
        break
    # 评论用户名
    use_name_list = soup.find_all('span', attrs={'class': 'comment-info'})
    # 评论文本
    comment_list = soup.find_all('span', attrs={'class': 'short'})
    # 评分
    rating_list = soup.find_all(
        'span', attrs={'class': re.compile(r"allstar(\s\w+)?")})
    # 点赞人数
    vote_list = soup.find_all('span', attrs={'class': 'votes vote-count'})
    for a, b, c, d, e in (zip(comment_time_list, use_name_list, comment_list, rating_list, vote_list)):
        datas.append({
            '时间': a.string[21:40],
            # 评论用户名，下的a标签
            '用户': b.a.string,
            '评论': c.string,
            '评价': d.get('title'),
            '点赞人数': e.string
        })
    # 写入到文件
    df = pd.DataFrame(datas)
    # 存储为douban_movie.csv
    if not os.path.exists('泰坦尼克号评论.csv'):
        df.to_csv('泰坦尼克号评论.csv', encoding='utf_8_sig',
                  mode='a', index=False, header=True)
    else:
        df.to_csv('泰坦尼克号评论.csv', encoding='utf_8_sig',
                  mode='a', index=False, header=False)
    print('page '+str(i+1)+' has done')
    i = i+1
    time.sleep(3)


def sentiment(content):
    s = SnowNLP(str(content))
    return s.sentiments


data = pd.read_csv("泰坦尼克号评论.csv")
data = data.sort_values(by="点赞人数", ascending=False)
data.head()


# 读取数据
df = pd.read_csv('泰坦尼克号评论.csv',)

# 对评论进行情感分析并加入新列
df['情感分析'] = df['评论'].apply(lambda x: SnowNLP(x).sentiments)
display(df)


# 分词并提取关键词
for index, row in df.iterrows():
    content = row['评论']
    # 分词
    seg_list = jieba.cut(content, cut_all=False)
    # 提取关键词
    keywords = jieba.analyse.extract_tags(
        content, topK=10, withWeight=False, allowPOS=('n', 'vn', 'v', 'ns'))

    pattern = re.compile(r'[\u4e00-\u9fa5]+')  # 匹配中文字符
    clean_keywords = []
    for keyword in keywords:
        keyword = re.findall(pattern, keyword)
        if keyword:
            clean_keywords.append(keyword[0])
    # 将关键词保存到新列中
    df.at[index, '关键词'] = ','.join(clean_keywords)
results = df["关键词"].values


results = str(results).split(',')
counter = Counter(results)
result = sorted(counter.items(), key=lambda x: x[1], reverse=True)
top_k = 10
keywords = [x[0] for x in result[:top_k]]
counts = [x[1] for x in result[:top_k]]
# 画条形图
bar = (
    Bar()
    .add_xaxis(keywords)
    .add_yaxis("出现次数", counts)
    .set_global_opts(title_opts=opts.TitleOpts(title="关键词出现次数排名Top{}".format(top_k)))
)
bar.render_notebook()


# 构造词云数据

# 创建词云图实例并添加数据
wordcloud = WordCloud() \
    .add("", data_pair=result, word_size_range=[12, 120], rotate_step=45, pos_left=30) \
    .set_global_opts(title_opts=opts.TitleOpts(title="关键词词云图"))

# 展示图表
wordcloud.render_notebook()
