import requests
from bs4 import BeautifulSoup
import pandas as pd

# 设置要抓取的网站URL和需要获取的表格列数
url = "https://www.cdu.edu.cn/"
num_columns = 1005

# 发送请求并解析HTML内容
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 找到包含数据的表格元素
table = soup.find("table")

# 找到表格中所有的行，并把每行的数据存储到一个字典中
data = []
for row in table.find_all("tr"):
    columns = row.find_all("td")
    if len(columns) != num_columns:
        continue
    data.append({
        "Time": columns[0].text.strip(),
        "Data 1": columns[1].text.strip(),
        "Data 2": columns[2].text.strip(),
    })

    # 如果已经收集到足够的数据，就退出循环
    if len(data) >= 100:
        break

# 把数据转换为DataFrame并保存为Excel文件
df = pd.DataFrame(data)
df.to_excel("data.xlsx", index=False)
